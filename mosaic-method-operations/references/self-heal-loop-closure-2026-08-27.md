# Self-Heal Loop Closure + Context-Free Button Fix — 2026-08-27

## Incident timeline (defect reached principal twice)
1. 08-26 evening: principal clicks the text bar to type; console registers it as
   an approval (false-input capture). P0 minted (T-260827-0027) covering
   event-capture fix + context-block requirement. Fix claimed by a lane…
2. 08-27 ~21:00: principal reports "buttons again with no idea what they're for."
   The claimed fix had STALLED — never completed, never live-verified.
3. principal ruling: "When issues get identified we MUST SELF HEAL AND EVOLVE
   MOVING FORWARD." → loop-closure law minted (T-260827-0164).

## Root cause found in the live emitter (the real lesson)
The decision cards in `conduction_daemon.py` (serving :port) already had a
4-field context system: `what` / `why_you` / `if_approved` / `if_rejected`,
rendered by `conductor_screen.py` lines ~816-825 ONLY when the fields are
non-empty. The bug: the FALLBACK path (when a task was minted without a
`ceo_brief`) populated `what` from the title but left `why_you`,
`if_approved`, `if_rejected` as EMPTY STRINGS → cards rendered as
title + bare buttons. Context-free buttons were a fallback-with-holes,
not a missing feature. The first dispatched fix (event-capture) was aimed
at the WRONG layer — dispatching a fix without root-causing in the live
emitter code wasted a rotation.

## The fix (pattern to reuse)
Patch the fallback so ALL FOUR fields always populate from the task record
(title-derived what/if-approved/if-rejected text beats blank). Then:
1. `python3 -c "import ast; ast.parse(open(<file>).read())"` — syntax check.
2. Backup first (`cp file file.bak-contextfix`).
3. Restart daemon: `launchctl kickstart -k gui/$(id -u)/<label>` — the
   label is NOT guessable; find it via `launchctl list | grep -i conduction`
   (actual: `com.your-org.conduction-daemon`).
4. LIVE VERIFY against the data endpoint the UI actually fetches — for the
   conductor surface that is `http://localhost:port/api/immune`, key
   `rulings_pending`; assert every pending ruling has all four ceo_brief
   fields truthy. Paths like `/needs-you` or `/api/rulings` do NOT exist;
   enumerate real paths from `do_GET` routing in the daemon source, or from
   `fetch(` calls in conductor_screen.py (e.g. `rulings_pending` appears in
   the getJSON error-whitelist — that's how the endpoint was found).

## Closure law (now binding)
- Minted ≠ handled. Handled = live-verified on the principal-facing surface,
  evidence attached (probe output / click log), fixer never self-certifies.
- Same defect class reaching principal twice → auto-escalate + daily digest until
  dead.
- Claimed fixes past deadline → automatic re-dispatch; silent stalls are
  defects themselves.
- principal-caused delays NEVER de-prioritize or rush work: severity is a
  property of the defect, not of the waiter's patience (principal explicit
  08-27: "don't rush to get me what I need… continue the physics
  prioritization").
