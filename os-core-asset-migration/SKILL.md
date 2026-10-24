---
name: os-core-asset-migration
category: devops
description: "Use when moving harness-bound scripts to OS-core."
version: 1.0.0
---

# OS-Core Asset Migration (the OS OS)

Move diagnostic/watchdog scripts out of harness profiles (`<agent-home>/scripts`,
`~/.config/sibling-agent`) into OS-core (`~/your-org/organism/`,
`your-stack/gates/`) without breaking the crons and launchd daemons that
call them. the operator agent is a swappable harness; anything the body needs after a
brain-switch (`organism/switch-brain.sh`) cannot live in the brain.

## Placement principle (one question)

**Does the body need it after a brain transplant?**
- YES autonomous reflex → `organism/diagnostics/` (canonical), shim in harness
- YES method gate → `your-stack/gates/` (versions with the method)
- NO, harness-personal → stays in the harness profile
- Doesn't exist yet as an engine → BUILD-OUT list, not a migration

Read FIRST: `~/your-org/organism/DIAGNOSTIC-ASSET-PLACEMENT.md` —
the live manifest (homes, staged wave queue, principal-settle items).

## Pattern (adiabatic: canonical copy first, shim second, binding untouched)

1. **Map bindings before moving**: `grep -rl <script> <agent-home>/cron/jobs/
   ~/Library/LaunchAgents/`. Zero bindings = dead code → retire flag, do NOT
   migrate. Note WHO invokes it and HOW (daemon_loop? cron wrapper? launchd?).
2. **Parameterize hardcoded paths in the canonical copy first** (env seams:
   `DS_ORGANISM_ROOT`, `DS_OPERATOR_BUS`, `DS_RADAR_STATE`, `DS_NOTIFY_ENV`).
   Scripts resolving siblings via `Path(__file__).parent` break on move.
3. **Copy to canonical** (`cp -p`). Do not move.
4. **Replace the original with a POLYGLOT shim** (below) — never plain bash.
5. **Verify BOTH invocation modes** and match pre-migration exit behavior.
6. **Update the manifest + post handoff** on the operator bus.

## THE SHIM TRAP (verified near-miss 2026-08-20)

`daemon_loop.py` runs `.py` children as `/usr/bin/env python3 <path>`, so a
bash shim SyntaxErrors EVERY TICK for every supervised daemon (8 daemons
affected; caught before any tick fired). The shim must be valid sh AND valid
Python at once:

```
#!/bin/sh
''''exec /usr/local/bin/python3 -- "$0" "$@" # '''
import runpy, sys
runpy.run_path("/<workspace><script>.py", run_name="__main__")
```

- sh reads line 2 as: empty-string + `exec python3 -- "$0" "$@"` + comment.
- Python reads line 2 as a harmless adjacent-string expression, then runpy.
- Do NOT hand-modify the quoting. `ast.parse` every shim after writing.
- If the canonical script resolves a sibling (e.g. operator_bus.py beside
  it), inject the env seam from the shim before runpy:
  `os.environ.setdefault("DS_OPERATOR_BUS", "<canonical bus path>")`.

## Order (supervisor LAST)

Shim all children first. `daemon_loop.py` resolves children from
`<agent-home>/scripts` and moves only when nothing it supervises still lives
there. Thin cron wrappers that subprocess canonical logic (telemetry_*_cron,
radar_registry_bridge, bus_hygiene_wrapper) are correctly-placed harness
glue — leave them.

## Verification gates

- `ast.parse` each shim (catches quoting damage).
- Execute via `/usr/bin/env python3 <shim>` AND direct `./<shim>`.
- Behavior gate: exit codes + telemetry match pre-migration run (rc=2 =
  honest operator-down finding, NOT a failure).
- Gate/spam testing: count bus rows before/after each forced cycle.

## Pitfalls

- **Swallowed `except: pass` lies.** A gate returning False can mean
  "blocked", "posted but Linear failed", OR "your probe dict was malformed".
  Instrument the internal path before concluding the gate is broken
  (2026-08-20: two false alarms caused by my own malformed probe dicts).
- **Siblings edit the same trees.** Check mtime/inode before editing;
  same-inode mirror = patch once, both trees update; same-name-different-hash
  = drift → reconcile, never overwrite.
- **Oversized inline terminal payloads** hit the hardline blocklist. The
  recovery path is printed in the error:
  `bash /<workspace><id>.sh` — use it, do not
  retry inline.
- **Probe residue**: close synthetic Linear issues (`close_health_issue`)
  and `operator_bus.py complete <id>` every bus row you created testing.

## References

- `references/alert-dedup-physics.md` — cooldown/dedup design for bus
  emitters (zero-surprisal rule, ack-churn failure mode, raw_decode).
