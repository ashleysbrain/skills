---
name: ceo-facing-surface-discipline
description: Use when reporting principal status or offering team URLs.
---

# principal-Facing Surface Discipline

Two hard rules for anything that reaches the user: what a report may contain,
and what an offered access surface must have proven before it is offered.

## Rule 1: Capability state only — no vendor mechanics in user-facing reports

When a model/provider lane fails, degrades, or needs credentials:
- NEVER surface refund, credit, billing, balance, key-rotation, or
  provider-outage mechanics to the user. Fail over to the next-best stack
  silently; log the lane swap to telemetry, not to the conversation.
- The report carries capability state only: what works now, and what replaced
  what stopped working. "Research now runs on X" — not the collapse narrative.
- "We should refund X" / "provider Y needs a new key" reaching the user =
  routing defect. The router transforms to the best stack for the need
  without describing the transformation.
- Rationale: the user runs an orchestration OS whose value proposition is
  stack-adaptivity — narrating vendor ops tells them the system is NOT doing
  its job, and spends their attention on work the system should have absorbed.

## Rule 2: Measure reach before offering any address

Never hand a user (or their team) a `localhost` / `127.0.0.1` URL as a
working surface for people on other machines — it resolves only on the host
running the service. Before offering ANY url:
1. `lsof -nP -iTCP:<port> -sTCP:LISTEN` — bind `*:port` = all interfaces
   (reachable given a network path); `127.0.0.1:port` = local only, dead end.
2. Check the network path: `tailscale status` + `tailscale ip -4` (private
   mesh), or `cloudflared` tunnel state for public HTTPS.
3. Check WHO is actually on the network — a tailnet listing only the owner's
   devices means team members have no path even when the app binds `*`.
4. Check accounts exist for the intended users (app-level identity ready is
   NOT access — the network path is the gap).

Offer the rung ladder, not a single address:
- Rung 1: private mesh invite (owner pushes one invite button; same-day).
- Rung 2: named HTTPS tunnel with access control.
- Rung 3: containerized production deploy on a cloud VM so the service stops
  depending on the owner's machine.

Rung 0 — check whether the viewer is ALREADY on the tailnet before offering
any rung: `tailscale status` lists the principal's devices by name + 100.x IP. If
the target phone is on it, serve the surface on the tailnet IP and MagicDNS
hostname (`http://100.x.y.z:PORT/path`, `http://<magicname>:PORT/path`) —
reachable on cellular, off-LAN, and immune to LAN IP rotation.

Link hygiene (rot presents to the principal as "links aren't working again"):
- Never store raw LAN IPs in links (chat, board cards, DB rows) — DHCP
  rotates them silently overnight. Sweep stored URLs and rewrite to the
  stable name whenever the IP changes.
- `.local` mDNS hostnames resolve only on the same L2 network — a phone off
  the home Wi-Fi gets nothing.

## Rule 2b: A surface offered once must stay up and stay findable

- Any local server offered to the principal runs under a liveness supervisor so it
  survives restarts: for organism-owned surfaces and recurring syncs that is a
  launchd LaunchAgent (KeepAlive=true, RunAtLoad=true) — the service must not
  depend on any harness session staying alive; failure-only monitoring on top
  is fine (cron `no_agent=true`, script-only, silent when healthy). Kill-test
  the recovery once: stop the server, confirm the supervisor restarts it and
  HTTP 200 returns. the operator agent cron is acceptable only for harness-owned jobs
  (agent runs, digests) — never as the sole supervisor of an organism surface.
- Sort principal-facing boards newest-active-first: the current deliverable sits
  at position 1. A live card buried under stale entries reads to the principal
  as deleted.

## Rule 2c: Capability surfaces break down by what changes the output

When the principal asks for a stack/capability view, the breakdown axis is the
ENTIRE ecosystem, never one task-class slice — a surface showing a single
lane reads as missing the point of the ask. Rows are MODEL CONFIGURATIONS
(model x harness x thinking level x route) because the same model at a
different thinking level or on a different harness is a different output.
Do NOT coin a unit term for the taxonomy — vocabulary comes from the binding
terminology spec (OS-TERMINOLOGY-SPEC.md), where OpenRouter and siblings are
routes (serving paths), NOT harnesses; harnesses are execution drivers. The
page re-reads the live store on every request (no baked snapshot), an
automated sync keeps the catalog current on an interval, and unprobed
configurations display UNMEASURED — never a guess dressed as a ranking.

## Rule 2d: Clean data — human phrases on the surface, machine IDs under it

Visible text on a principal surface never shows raw machine identifiers: no
snake_case, no file names, no port numbers, no HTTP verbs, no model IDs with
quantization suffixes. Translate every key to a title-cased human phrase at
render time (e.g. `whisper-large-v3-turbo-q5_0 + silero VAD` becomes
"Whisper large v3 turbo, voice-activity gated"); keep the raw key in the
column or API payload for machines. Acceptance test after every surface
edit: strip tags from the served HTML and regex-scan the visible text for
`\w+_\w+|:\d{4}|\.py\b|\.db\b|POST |GET /` — the match list must be
empty before delivery. Clunky raw keys read as unfiltered machine output and
get rejected on review. The interface's own harness name is the worst
offender class on principal surfaces: every self-reference becomes an organ/role
label ("intake lane", "conduction organ", "peripheral/cortical organs").
After any bulk patch, sweep the surface store for the harness name and
re-query until zero remain; citations of EXTERNAL tools that happen to
carry the same name are not violations — self-reference is.

## Rule 2e: Surfaces must be organism-owned, not harness-parented

A surface or sync started as a child of an agent session (nohup, background
terminal) dies with that session and presents as "the harness drives
everything." Any organism-owned surface or recurring sync ships as a
launchd LaunchAgent (KeepAlive=true, RunAtLoad=true, logs on disk) — this
supersedes hand-rolled watchdog crons for services the principal has been given.
Verify independence by parentage: `ps -o ppid= -p <pid>` on the service pid
must return 1 (launchd). When launchd absorbs a job that also exists in the
the operator agent cron registry, disable the cron copy in the same change — exactly one
owner per job.

## Rule 2f: One-tap deliverable access — a queue exists to eliminate scrolling, not host it

A paste-ready deliverable (comment, reply, brief) placed "in the queue" is
NOT delivered if the principal must scroll a board, apply filters, or guess which
item is theirs. Every deliverable item ships as an addressable deep link:

- `/comments?focus=<seq>` (or the equivalent on any board): the target card
  renders FIRST, gold-ringed, under a "Pinned for you" banner. Position 1,
  zero hunting. Hand the principal that exact URL in chat — never the bare board
  URL plus instructions to find the item.
- On the pinned card: a `Tap to copy` button whose payload is the FULL paste
  text INCLUDING the source/paper link (one paste delivers comment and
  reference), plus an `Open ref` button jumping to the destination post.
  Total principal motion: open link, tap copy, tap open, paste.
- The home screen's action hero button links to the current top
  deliverable's focus URL; repoint it when that item completes.

Button-first navigation on phone surfaces (a link list or bare text index
reads as unusable and gets corrected every time):
- Persistent bottom tab bar, `position: fixed`, present on EVERY screen,
  never scrolls away; active tab gold; five tabs max.
- Touch targets: ordinary buttons min ~52px, hero buttons ~64px,
  safe-area bottom padding for thumb reach.
- Every screen and filter reachable by button tap with live counts on the
  buttons; filters render as segmented buttons, never as query-string
  knowledge.

- A deliverable that exists only in a generation store (drafts.db) is
  INVISIBLE — "I can't see my next comments" means the draft never became a
  card. Sync every paste-ready draft to its board card at delivery time
  (status ready, body = full text, Tap-to-copy payload includes the source
  link); the in-channel paste kit and the board card are ONE delivery, not two.
  The sync is per-author-card, not per-draft: drafted texts live in the
  generation store while board cards are separate rows, so after any drafting
  pass, explicitly mint or update the card for EVERY slate author (a drafted
  comment with no card is the default failure state, not an edge case), and
  when a draft was revised by a panel, re-sync the card body to the newest
  version — the card silently keeps serving the older text otherwise.

Concrete recipe (tab-bar CSS, copy-button handler with fallback, pin route,
phone-path verification commands): see `references/phone-surface-one-tap-delivery.md`.

## Rule 2g: Interactive controls bind system state, not render state

Any toggle/selector/mixer added to a principal surface is a CONTRACT on organism
behavior, not a UI preference. A control that only recolors chips gets
rejected and re-ordered ("the system needs to switch and adapt based on the
toggles — security and everything"). Ship a control only when it has:

1. **One enforcement module as the single read path** (e.g.
   `organism/brain_gate.py` exposing `active_set()`, `routable(key)`,
   `require(key)`); the surface endpoint is the ONLY writer to the toggle
   store, everything else reads.
2. **At least one verified enforcement seam** — the router's matcher passes
   veto off-brains in BOTH static and dynamic passes; the dispatcher's
   candidate ranking sinks rows naming an off-brain to an unclaimable score
   with the refusal recorded on the row.
3. **Fail-safe directions**: unknown/unreadable toggle store fails CLOSED for
   specialists (unroutable) and open ONLY for the always-on identities; the
   default state ships ALL-ON so the organism never wakes up lobotomized —
   toggling OFF is the deliberate act, never the default.
4. **Behavior proof, not patch presence**: flip the toggle and observe the
   routing change end-to-end (off -> task reroutes away from that specialist;
   on -> routes back), then restore state. An enforcement import that fails
   silently inside a swallowed try/except looks installed and enforces
   nothing — load enforcement modules by absolute path
   (`importlib.util.spec_from_file_location`) because the caller's cwd is
   never guaranteed to be on sys.path.
5. **Row-shape discipline in enforcement helpers**: rankers and row-mutators
   iterate `sqlite3.Row` objects, not dicts — a `.get()` call inside a
   swallowed try/except silently no-ops the whole helper while standalone
   dict tests pass. Use a per-key accessor
   (`try: return str(r[k]) except Exception: return ""`), and prove the gate
   fires on a REAL ranked row, not a synthetic dict.

Entity rosters for such controls source from the LIVE engine registry, never
a static agents file — bus rows name real specialists a static list
undercounts, and every unlisted name silently falls into fail-closed.

## Rule 2h: Write-surfaces shell the gate CLI, never open the ledger

When a principal surface gains edit power over tasks (a calendar edit page), the
write path is a subprocess call to the ledger gate's lawful verbs — NEVER a
direct sqlite connection to task-ledger.db from the surface process. Raw
writes are blocked by ledger law for every other tool; a principal-facing surface
must not become the exception.

- Editable post-mint: deadline (`--redate` + mandatory `--reason`; a naive
  date from the UI pins the principal's own clock offset explicitly, never a
  guessed UTC instant), notes (`--annotate`, append-only, never overwrites),
  claim/complete/release.
- NOT editable: title/kind/lane/id — birth facts. A title change is a new
  mint + successor, offered only on explicit ask.
- The edit page reads tasks + task_events (columns are `event` and `detail`,
  not kind/note) read-only.
- Gate refusals render on the page as "Refused: <cause>" — the gate saying
  no IS the system working; never route around it from the surface.

## Rule 3: Status pushes during long gated work — silence is a failure, not patience

Multi-gate runs (draft → tell-scan → adversarial review → fixes → delivery)
and any unattended window (overnight, principal illness/travel) must NOT go quiet.
- Push a one-line status to the principal chat after each gate COMPLETES, not only
  when asked. Every repeated "status?" from the principal is a delivery failure
  equal in weight to skipping a gate.
- If a gate blocks (engine down, seat empty, retry loop running), say so
  immediately with the ONE recovery action — never let the thread sit silent
  while retries churn.
- Failure-only monitoring is not coverage during absence: "healthy all
  night" emitting zero messages is indistinguishable from "nobody was
  watching." Pair it with a positive surface — a digest at the principal's wake
  window covering what ran, what completed, what needs decisions — so the
  principal never has to ask "what happened while I was down?"
- Status lines carry measured state only (counts from live stores, port
  probes), never vows or process narration.
- A status ask arriving mid-report is an INTERRUPT, not a queue-jump: the
  in-flight report is superseded, and the newest message (often a new
  referral link) gets dispositioned FIRST; the status answer then folds in
  whatever live probes already ran — never resend the stale report verbatim
  after handling the interruption.
- A speed complaint ("you're slow right now", "lagging more than usual") is
  a delivery-defect signal, not a request for a speed vow or an apology.
  Answer with measured state: what completed during the lag window (task
  ids, corpus rows, counts pulled live), what the actual blocker was named
  concretely, and fresh proof the pipeline moves again. Never absorb it as
  personal failure and never promise to be faster — show the through-put
  receipts and the fixed mechanism.
- The lag itself usually has a structural cause: serial round-trips while
  concurrent work queues up. When several independent items arrive in one
  window (a referral burst plus a defect report), disposition them as ONE
  batched pipeline in parallel with the diagnosis — interleaved
  one-at-a-time handling is indistinguishable from being stuck, and the principal
  cannot see effort, only turn latency.

## Verification discipline for both rules

- Reachability claims end with a measured acceptance test (e.g. a non-owner
  login event in the app's users table), not an assertion.
- Failover claims end with the replacement lane's live evidence, never the
  outage story.
- Helpers that must accept both dict and sqlite3.Row: Row has no `.get()` — a
  `r.get(k)` inside a swallowed try/except silently no-ops the whole helper
  while standalone dict tests pass. Use a per-key accessor
  (`try: return str(r[k]) except Exception: return ""`).
- Enforcement wiring is proven by the end-to-end loop (flip state -> observe
  behavior change -> restore), never by the patch being present in the file.

## Pitfall: compaction decoy ledgers (adjacent dispatch discipline)

After context compaction, path claims in the handoff summary are hypotheses.
Several `task-ledger.db` files exist as 0-byte empty shells and the bus's
`task_queue` table is a legacy mirror, not the birth record. Verify the real
ledger live before minting: the ledger module's `connect()` takes NO
arguments (it resolves the canonical path itself); a submitted row must read
back from `tasks`. If a mint script wrote to the legacy mirror or a 0-byte
shell, re-mint through `submit()` and mark the legacy rows as mirrors in the
detail. Build-kind mints require a GENOME block as the FIRST text in detail
— mine the format from the rejection message; apostrophe-free physics
string, single-token body, canonical 8d dimension, metrics clause included.
