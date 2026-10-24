# Live adversarial probe verification for daemons/fixes (2026-08-25 session)

Companion to `false-done-marks-and-spy-verification-2026-08-25.md` (sections 1-5 there).
This file: the full probe recipe for daemon/fix claims, proven live on the
Glia conduction daemon (T-260824-0649/T-260825-0150).

## The failure it prevents
A fix demoed with a hand-picked probe whose values happen to match the fix's
own assumptions. Live case: daemon harvest filter matched exact origin
`ceo-directive`; my demo probe used exactly that string, so the demo
"passed" — while every REAL principal task (minted by taxonomy as `ceo:<topic>`)
stayed invisible. User: "I don't believe the overnight starvation problem
is fixed." The skepticism was correct.

Second defect the probe exposed: parser crashed on non-numeric task IDs
(`L12B`) — in serve mode that exception is SILENT daemon death (try/except
backoff loop, no alert, no state advance).

## The probe recipe (proven)
1. **Read the real producer's format FIRST.** Open the taxonomy/schema/enum
   the actual system uses (e.g. `stores/task-taxonomy.json`: kinds, lanes,
   origin_prefixes). Never hand-craft a probe that matches your filter's
   assumption — that tests your assumption, not the system.
2. **Mint the probe via the official API** (`gates/task_ledger.submit(conn,
   title=..., kind=..., lane=..., origin='ceo:<topic>', created_by=...)`).
   Raw `INSERT INTO tasks` is rejected by the birth-certificate /
   single-write-path gate anyway (bus #3623 law), and submit() validates
   kind/lane/origin against the taxonomy — which is exactly the format
   check that catches the happy-path-assumption bug.
3. **Snapshot daemon state file BEFORE** (e.g. `stores/glia/cycle-state.json`).
4. **After patching: manual-cycle smoke test** (`python3 daemon.py cycle`)
   BEFORE restarting the service. Serve-mode try/except swallows crashes
   into silent death; the manual cycle surfaces them with a traceback.
5. **Restart via `launchctl kickstart -k gui/501/<label>`**, wait one poll
   interval, re-read the state file.
6. **Verdict criteria:** state `cycles` advanced AND (probe claimed OR
   visible lane count grew). A probe NOT claimed due to arbitration
   tie-loss (equal severity, older id wins) is correct queue behavior, not
   starvation — check the lane query result, not just `last_claim`.

## Daemon hardening lessons from the same session
- Safe-parse ALL id-like fields: non-numeric ids (`L12B`, `L12A`) appear in
  production ledgers. A `_num()` try/except helper returning None beats
  inline `int(...)` in every arithmetic site (census loop AND target id).
- Event-driven daemons: trigger on (ledger mtime, bus max-id) changes; poll
  trigger STATE every ~20s, never the heavy work (anti-cron law: silence =
  health, escalation = failure-only alert after N idle cycles).
- launchd KeepAlive plist + logs; verify PID via `launchctl list | grep`.

## Related sections (same skill)
- `references/false-done-marks-and-spy-verification-2026-08-25.md` §1-5:
  false done-marks, docstring-dead-code spy pattern, count decomposition,
  session-search-before-asking.
