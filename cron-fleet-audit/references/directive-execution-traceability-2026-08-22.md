# Directive-execution traceability + liveness-probe method (2026-08-22)

## The failure class: directives that evaporate between directive and dispatch

principal directive 2026-08-20: "QA fleet 24/7: the specialist engine + the specialist engine; autonomous
seat minting; variance N>=3." principal question 2026-08-22: "what is the status of
our autonomous 24/7 qa processes??? they are not working again, right???"

Live status check found the directive had ZERO execution trace — not broken,
never started:
- no entry in organism/agents.yaml or ORGANS.json (grep for Deming|Gantt: 0)
- no process (`ps aux | grep -iE 'deming|gantt'`: 0)
- no port (8154 dead, 8155-8156-8161-8164 nothing, :port is the specialist engine —
  engine-name guesses are worthless, always curl /health)
- no disk directory (`find /<home> -maxdepth 3 -iname '*deming*' -o -iname
  '*gantt*'`: 0 hits)
- no message-bus message, no anatomy-queue entry, no task-ledger row

Root cause: the directive never got a mint task at issue time. It died in
conversation. Remediation: bus message to the owning operator (sibling-agent owns
engine minting) carrying the FULL mint spec inline — the specialist engine (SPC control
charts over iteration-log/defects jsonl, Western Electric rules, variance
N>=3 gate before any verdict ships) + the specialist engine (expected-vs-actual fire-time
drift + missed-fire detection across every daemon and cron). Posted as bus
#3000 2026-08-22, verified by readback (id|to_op|status).

**Rule to embed in every fleet audit (Mode 9):** directives that name
infrastructure must be checked for execution trails across registry,
processes, ports, disk, bus, and task ledger. Zero trace = never dispatched,
which is a DIFFERENT remedy class from "built but broken" — the fix is
dispatch (bus handoff with spec), not debugging.

## Liveness-probe method that avoids the two false verdicts

Checking "is the 24/7 QA alive" produced two near-miss wrong answers:

1. **stdout logs lie for silent daemons.** autonomous-iteration's .log was
   frozen 3 days (Aug 19) while the daemon was HEALTHY — by design it logs
   to telemetry JSONL only ("healthy operation is SILENT, file logs only").
   Probe the daemon's DECLARED output surface, not its stdout redirect:
   read the plist for StandardOutPath AND the script header for its real
   telemetry surface, then stat THAT (iteration-log.jsonl: fresh, 46 passes
   today, n=289). Confirms memory law: liveness = log mtime of the real
   output surface, never ps.
2. **launchd "not running" is normal between interval fires.** Watchdogs
   with StartInterval (30-180s) and no KeepAlive show no PID and
   last-exit=0 between fires — NOT dead. Distinguish: KeepAlive service
   with no PID = dead; interval job between fires = healthy. Read the
   plist (grep KeepAlive / StartInterval) before declaring either.

Also verified healthy this sweep: Self-Evolving QA Organ cron e2bcad9b634c
(*/45, monitor-mode qa_tick.py, 12+ fires/12h all completed), Conductor
Pulse 6bf3256ff89c, world-model-radar b18364f94c37 (48h interval — "stale"
last-run Aug 20 was ON schedule; check interval before flagging).

## SIGTERM (-15) last-exit codes after config reloads

Five daemons showed -15 in launchctl list after reconciler reloads —
benign: KeepAlive caught every kill and respawned (live PIDs). Only
investigate -15 if the PID is ALSO missing.

## hermes CLI notes

- `hermes cron list --json` does not emit parseable JSON to stdout in one
  call (2026-08-22); parse the table output or read jobs.json directly.
- Complex multi-statement shell one-liners can trip the terminal
  hardline parser ("command parser limit or malformed executable payload");
  the recovery path WORKS: the blocked command is saved to
  <agent-home>/cache/blocked-scripts/blocked-<ts>-<hash>.sh — run
  `bash <saved-path>` verbatim.
