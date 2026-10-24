---
name: muse-worker-organ
description: Use when running work through Muse the actuation organ.
version: 1.0.0
author: the operator agent Agent
license: MIT
provenance: agent
metadata:
  hermes:
    tags: [muse, actuation, browser, linkedin, intake]
---

# Muse worker organ (actuation + LinkedIn metabolism)

## When to Use

- Any task that runs work THROUGH Muse, the actuation organ with a browser:
  claiming muse-lane ledger tasks, patrolling the principal's LinkedIn feed for
  science, dispatching browser actions through the ActionContract path.
- Diagnosing "why isn't Muse working" / "she needs to take on tasks" class
  reports (process, activation, session, or queue gaps).
- Extending Muse's verb set, safety scope, or the LinkedIn metabolism loop.

Class of task: anything that runs work THROUGH Muse, the actuation organ
with a browser. Claiming lane tasks, patrolling the principal's LinkedIn feed,
dispatching browser actions, or answering "why isn't Muse working".

## Architecture (what exists)

- Organ dir `/<workspace>`: `intake.py` (claims
  muse-lane ledger rows, actuates, closes with outcome), the dispatcher
  (ActionContract path: schema check, safety matrix, nonce, audit log),
  `linkedin_metabolism.py` (feed patrol), `stores/` (actuations.jsonl,
  intake-queue.json, li-metabolism-state.json, li-seen-posts.json).
- Motor path: TWO Chromes, never conflated. The gateway's automation Chrome
  (headless, CDP :9223, profile `<agent-home>/cache/browser-chrome-profile`)
  auto-respawns under launchd — never kill-loop it. The principal-login Chrome is a
  SEPARATE HEADED instance on its own port (:9224) with its own persistent
  profile and `--remote-allow-origins` (the CDP websocket refuses connections
  without that flag); all LinkedIn-session work targets the headed instance.
  Patrol verbs are READ-ONLY (navigate, scroll, eval-read); never like, post,
  or DM.
- All loops wire into the single research tick (`research_scan_tick.sh`);
  no new crons for Muse work.
- **Tick invocations of Muse modules must pin the working directory.** The tick runs `python3 -m organism.muse.intake`, and `-m` resolves against the invoker's cwd — when the tick fires from a cwd other than the workspace root, the import dies with `ModuleNotFoundError: No module named 'organism'` while manual runs (always from the root) pass, so the defect hides from desk testing and only bites scheduled runs. Wrap every `-m organism.*` call in the tick as `(cd /<workspace> && python3 -m organism.muse.intake)`. Prove the fix by running the exact tick line standalone (exit 0), never by running the module from your own shell — your shell's cwd IS the workspace, so an unpatched line passes your test and fails the schedule. Check the tick's log mtime against the schedule: a log that stopped updating while siblings update means its line is dying, not idle.

## Procedure for new Muse work

1. Mint tasks with a lane containing `muse`; intake matches with LIKE, so a
   provisional lane string still matches. Normalize on the query side,
   never the mint side.
2. Intake is claim-once: rows transition to done with claimed_by set; a row
  with nothing motor to do is surfaced-and-closed with an outcome note,
   never re-eaten on the next tick.
3. Dispatch browser acts through the ActionContract path (write contract
  JSON, invoke the dispatcher); reads ride safety_class benign. The v1
  gate refuses system and destructive surfaces pending an explicit principal
   scope ruling; do not widen the verb set without one.
4. State files are the truth. The metabolism state records
   `needs_ceo_login` when the feed redirects to /login: a no-op WITH a
   recorded reason, never a silent skip and never a crash.

## Session law (the blocker that recurs)

The automation Chrome profile has NO LinkedIn session until the principal signs
in once inside its window. Cookie import from the principal's own Chrome is
structurally impossible, not merely disallowed: Chrome encrypts cookie
values with a profile-bound safe_storage key from the Keychain, so a copied
Cookies file decrypts to garbage in any other profile. When the feed
redirects to /login: record the flag, surface the login tab (CDP
/json/activate plus open -a), and state the one human step ONCE; the patrol
self-starts on the next tick after login. Do not probe the principal's own
browser cookie stores beyond confirming a session exists — the decrypted
value never touches the agent.

Session-window custody rules (each earned the hard way):

- A window the principal must type into must be a HEADED Chrome instance — a
  `--headless=new` automation Chrome renders no visible window on any screen,
  so "I don't see it" is the guaranteed outcome regardless of tab activation.
  Launch headed on a dedicated port BEFORE asking the principal to log in.
- Never kill or restart a browser while a login/auth tab is open in it: the
  principal's fresh session lives in that window, and a process kill destroys
  credentials they just typed, forcing a re-login they already did once.
  Check open tab URLs for a login path before any browser restart.
- Wrong-account one-tap recovery: "Sign in with Google" on the LinkedIn form
  hijacks into the OS account chooser and lands the wrong identity. Close the
  Google tab, reload the plain email+password form, verify it is clean via
  CDP (formReady true, email field empty), and tell the principal to ignore the
  one-tap button.

## LinkedIn metabolism contract (standing principal order)

Patrol reads the feed; a science-signal filter promotes posts; promoted
posts register to the corpus (sr-li fingerprint ids); every
comment-candidate mints a gated BUILD row (comments are builds, not a
lesser lane; full GENOME clause, prior-scan receipt). Comments deliver to
the board as paste-ready text; Muse NEVER posts. The
studio-generates/principal-posts law survives automation. Coverage target: more
ground than the principal can scroll manually.

## Pitfalls

- CDP /json/new tabs can die silently right after creation; navigate INTO
  an existing about:blank tab found via /json/list instead of minting new
  tabs.
- LinkedIn pages stall Runtime.evaluate on the automation CDP; prefer curl
  and og: meta capture for static reads (see research-referral-ingestion)
  and use Muse's browser only where the session is the point.
- AppleScript against native apps from a headless session times out (-1712)
  or hangs; never build a flow on osascript window queries, and always
  timeout-guard AppleScript calls.
- A navigate that reports "url confirmed=False" usually means the tab
  landed on an authwall or login redirect; read the actual tab URL from
  /json/list before concluding the verb failed.
- Fingerprint dedupe (hash of first N chars of post text) is what makes the
  patrol idempotent; never register promoted posts without checking the
  seen-set first.
- Extract feed posts by TEXT STRUCTURE, not CSS selectors: LinkedIn rotates
  and obfuscates class names and container attributes dynamically, so
  `div[data-id]` and `.feed-shared-update-v2` can return 0 against a live,
  fully-rendered feed (a bodyText of ~14k chars proves the feed loaded; 0
  posts after that means the selectors rotted, not that the session died).
  Anchor on stable text structure instead: actor blocks read name, bullet,
  headline with a U+2022 bullet separator, so find text nodes containing that
  separator and walk up the DOM chain to the post container.
- Write REAL unicode characters into embedded JS source, never escape
  sequences assembled in Python — a Python string write of backslash-u-2022
  lands in the file as literal backslash text, and the JS `includes()` check
  then silently never matches (syntax checks pass, zero posts extracted).
  The same replacement text breaks `re.sub` itself, which raises on the
  backslash-u template. Type the actual character in the source.
- Claim-state honesty: a loop whose runtime dependency is unsatisfied
  (login, activation, human-only gate) is ARMED, not BUILT; report the
  blocker state and let the ledger state carry the truth. Answer disbelief
  with receipts pulled live in the same turn (line counts, wiring grep,
  ledger rows with state, fresh run output). Related onboarding law: a
  capability connected at the principal's request arrives ready to work on
  connection day ("connect and go"), never "connect, then train" — pre-seed
  its queue, pre-prove its verbs, and dispatch a first real task before
  reporting the connection; surface any human-only activation step at
  connection time, not after the principal asks why nothing ran.
