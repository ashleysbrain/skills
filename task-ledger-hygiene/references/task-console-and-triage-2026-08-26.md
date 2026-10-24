# Task Console + Autonomous Triage — 2026-08-26 session

## The console (the OS Task Console, :port)

Stdlib-only `ThreadingHTTPServer` daemon (`task_console.py` in
relabel-work/), launchd `com.divinity.task-console` (KeepAlive, RunAtLoad,
pins `/usr/local/bin/python3` = 3.14 per plist law). Views: Needs You /
All Tasks / Calendar (scheduler.db queue + launchd census) / Organisms
(live fleet census) / Research (ledger research rows) / OS Chat (proxies
POST :port/v1/medical/chat). principal APPROVED the typography: 14px base,
13.5px titles, 11.5px meta, single-accent dark theme. Reuse it.

Write-back loop (verified live): Approve/Reject buttons → ledger
`ceo-approve`/`ceo-reject` event (actor `ceo/human`) + state transition +
message-bus `ceo-ruling` message via `organism/operator_bus.py post()`
(bus msg #4268 confirmed). Bus-down never blocks the ruling itself
(try/except around the bus post).

## Census law: registries, never memory

principal correction: "21 organs????? not correct... there are organ systems
way more than this." The organism is ~96 ECS engines across 15+ body
systems plus separate registries (55 flows, 10 pinned laws, 12 equations,
13 isomorphisms, 2,135 tasks). NEVER hardcode a fleet list or port map.
Parse `your-org/organism/ENGINE_REGISTRY.yaml` (canonical;
`agent-organism/ENGINE_REGISTRY.yaml` is a moved-stub) at request time:
`- directory:` starts a block; capture engine_name/port/body_system/
ds_ecs_code; int-coerce port inside try/except (registry carries
non-numeric ports for cron-fired engines). Probe each port's /health.
Full-fleet liveness: 85/86.

## Console bugs found live (fix patterns)

1. **Truncating /health JSON before parsing** (`decode()[:400]`) marked
   every long-payload engine "down" (3/21 false vs 21/21 true). Never
   truncate before json.loads.
2. **Apostrophe through Python→JS embedding**: `organism\'s` in a Python
   string inside a JS single-quoted string collapses to `organism's` →
   "Unexpected identifier 's'" kills the whole script block. Fix: no
   apostrophes in embedded-HTML JS strings, or restructure escaping.
   Gate with the served-page syntax check (see headless-ui-qa-batteries).
3. **Stale daemon after edit**: `launchctl kickstart -k` served OLD code
   (module cached at process start). Full `bootout` + `bootstrap` after
   any source edit to a daemon serving embedded HTML.
4. **rows_json assumed uniform columns** — research view SELECTed fewer
   columns than the shared serializer read → IndexError. Guard with
   `.get`-style access or select the full column set everywhere.

## Scope law (principal correction)

A single-purpose queue page was "way off" — the principal surface family is
multi-view (organisms toggle, calendar, OS chat, research) and MUST be
built ON the existing platform family (gg-ops-platform :port/:port/:port,
circadian conductor :port, Simard :port). Typography approved; scope
rejected. Always census existing live surfaces before building a new one
(matches the standing "build ON existing, never blank-slate" law).

## Autonomous decision triage (the 35→6 pass)

See SKILL.md "Needs-you triage" section. Key evidence rows: 19
auto-approvals each citing the principal order quoted verbatim inside the
task's own detail field; CURRENCY KILL executed on its pre-registered
2-idle-cycles criterion; 2 fleet claims; 8 scanner triage applied.
Residual genuinely-human 6: whisper swap (principal interface latency), backup
destination (money), Parag x2 (external human), nav rename (naming law),
OIDC client JSON (credential).

## Delegation outcome note

S1 (taxonomy ruling, background) returned AFTER its output file had
already been consumed and applied — late async reports must be diffed
against applied state, not re-applied blind. One kind_flag ID was wrong
(T-260819-0190 vs actual T-260821-0190); verify specialist-cited IDs
against the DB before filing them.
