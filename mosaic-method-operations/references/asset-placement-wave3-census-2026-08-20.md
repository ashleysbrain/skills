# OS-core asset placement — wave-3 census method (2026-08-20)

Session record for migrating diagnostic assets from `<agent-home>/scripts`
to OS-core (`organism/diagnostics/`). Waves 1-2 (9 scripts) landed
earlier; this file captures the wave-3 census method that decides what
moves, what shims, and what dies.

## The census (run before ANY migration)

For each candidate script, measure three properties:

1. **Boundness** — is it referenced by a the operator agent cron job
   (`<agent-home>/cron/jobs.json`: `script` / `monitor_script` fields) or a
   launchd plist (`~/Library/LaunchAgents/*.plist` `<string>` args)?
   Bound = keep at resolvable path or leave a shim.
2. **External references** — grep the skill library, scripts dir,
   organism/, your-stack/ for the basename. Zero refs + not bound =
   retirement candidate, NOT migration material. Migrating dead code
   launders it into OS-core.
3. **Shim status** — already a re-export shim (header mentions
   organism/ + shim/canonical, or `#!/bin/sh` polyglot)?

## Observed census results (2026-08-20, 56 scripts)

- 24 BOUND to cron/launchd (incl. all telemetry_*_cron wrappers, gate-*,
  qa_tick, daemon_loop) — these keep `<agent-home>/scripts/` paths; migrate
  only via polyglot shim, never a plain move.
- 23 unbound: 2 already shims (operator_bus.py, operator_bus_import.py),
  2 DEAD (watermark_removal.py, watermark_removal_v2.py — zero refs,
  one-off image experiments) → moved to
  `organism/migrations/retired-2026-08-20/` (archive, not delete).
- Remaining ~19 alive-and-referenced but unbound = the true wave-3
  migration list (gate-ceo/coo/cto/design/marketing/product/science,
  brain_integrity_gate, corpus_*, honcho-deriver-watchdog, etc.).

## Rules that carry

- **Retire before you migrate.** Dead code goes to
  `organism/migrations/retired-<date>/` — archive discipline, never rm.
- **Bound scripts migrate as polyglot shims** (valid sh header + python
  body) because `daemon_loop` invokes children via
  `/usr/bin/env python3 <path>` while cron invokes via bash. A pure-Bash
  or pure-Python shim breaks one of the two callers.
- **Free-energy gate**: a script with zero refs and zero bindings has
  F > 0 for migration — the move is pure cost with no info gain.

## Inverse bookkeeping lie (same session)

Tasks shipped in git but left `open` in the ledger, and tasks BUILT+LIVE
but still `claimed` with empty outcomes, are the same class of lie as
fabricated numbers — the ledger misreports reality in both directions.
Close bookkeeping with evidence: commit hashes (git log -S), live
endpoint curls, DB row counts. Examples closed this session:
T-260819-0030 (shipped 95f223c/fadf47a, ledger open), T-260819-0031
(login/me/logout live on :port, ws_users 4 rows, outcome empty).
