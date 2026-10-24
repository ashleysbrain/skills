---
name: event-driven-agent-lanes
description: "Wire or verify a 24/7 monitor-gated agent queue lane."
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [monitor-script, event-driven, cron, task-queue, 24-7, probes]
    category: devops
---

# Event-Driven Agent Lanes (24/7 queue firing)

## When to Use
- Wiring an agent to work a task queue/bus 24/7 with no session open
  (monitor-gated cron, not a schedule-driven LLM job).
- Diagnosing why "nothing worked overnight" despite healthy daemons.
- Answering "are you working / did it work overnight" before replying.
- Debugging a monitor probe that fires too often, never fires, or
  mis-counts rows in a time window.

**Class of task:** making an agent work a task queue/bus continuously without
a session open — and answering "are you working?" truthfully afterward.
The lawful shape is a monitor-gated cron job (agent fires on state CHANGE,
never on schedule); building one touches a probe, a wrapper, jobs.json, and
the executions ledger, each with its own failure mode.

## Root cause this pattern solves
Autonomous daemons work engines/gates; session-bound agents work the queue.
Overnight, NOTHING fires the agent on queue events unless a monitor lane
exists. "The daemon ran all night" is never evidence the queue was worked.

## Build procedure (order matters)

1. **Dup-check first** — list existing cron jobs (`jobs.json`), read each
monitor/watchdog/pulse job, and check enabled state. A disabled near-dup is
a REVIVE candidate, not a new build; only build when no job watches the
surface.
2. **Write the probe** reading the real stores read-only
(`sqlite3.connect('file:...?mode=ro', uri=True, timeout=5)`). Output the FULL
snapshot each run, sorted, quantized (below). Healthy state must produce a
STABLE byte-identical string — ideally empty.
3. **Quantize every number** into wide bands (`1-4`, `5-9`, `20-49`, `100+`).
   The monitor hashes exact output bytes; raw counts flap the hash every
tick (87→88 tasks) and burn agent runs on noise. Only state TRANSITIONS
should fire.
4. **No diff-state inside the probe.** The monitor layer already hashes and
compares; an internal prev-state file makes the content→empty transition
fire twice (once per representation).
5. **Place the wrapper in `<agent-home>/scripts/`** — relative `monitor_script`
values resolve against the scripts dir, NOT `<agent-home>/cron/`. Give it +x
and route by shebang (`exec python3 ...`).
6. **Register the job in jobs.json** cloning an existing monitor job's shape
(`monitor_script` set, `monitor_state: null`, schedule `*/5`), with a prompt
that tells the agent WHAT TO DO per event line (router cycle, claim, handoff
with receipt) plus a 2-minute-per-item budget and an explicit healthy-tick
reply token. Never point it at a full prompt with no action mapping.
7. **Verify SEATED = FIRING.** A job present in jobs.json with no execution
row is registered but dead. Confirm: a row appears in the executions
ledger, status reaches `completed`, and `monitor_state` in jobs.json gains a
hash. Wait through at least one fire before claiming the lane works.
8. **Prove the silent path too** — run the probe 2-3 times consecutively;
identical output (empty→empty or stable-snapshot→same) proves the hash holds
and the healthy tick is suppressed.

## Probe query pitfalls

- **Offset timestamps vs `datetime('now')`:** stores holding ISO-with-offset
rows (`2026-09-29T13:19:43+00:00`) compared with
`timestamp > datetime('now','-20 minutes')` mix formats — string comparison
silently selects wrong rows, inflating counts 10-40x or making a stopped
alert loop look live. Parse with `datetime.fromisoformat(str(ts).replace('Z','+00:00'))`
and filter on aware datetimes in Python. When a count surprises you, suspect
the window query before the system.
- **Slightly-overfetch then narrow in Python** (e.g. SQL `-40 minutes`, Python
filter `<= 20 min`) so boundary rows are never silently dropped.
- **Don't trust a .log's last line for daemon liveness** — state files and
pass counters are the heartbeat; a stale log with a live process means the
log path changed, not that the daemon died. Check state-file mtime and pass
counts.
- **A defect named `..._fail` may be a logging bug:** scanners returning rc=1
for "findings found" (healthy) can be logged as failures by a caller that
assumes 0=good — 1,000+ consecutive "failures" with empty stderr is a
contract mismatch, not a broken lane. Read the scan's exit-code contract
before repairing anything. Verify by running the scanner manually with
`--verbose`.

## Status-answer law (three layers, report the worst)

Before answering "are you working / did it work overnight," check all three:
1. **Internal receipts** — executions ledger counts, task done-stamps, bus
   receipts. Completed-with-zero-failed is the floor, not the answer.
2. **The machine the user touches** — `uptime` (load average; sustained 10x
   normal = unusable at the desk even while every cron ticks) and top CPU
   consumers (`ps aux | sort -rk3 | head`).
3. **The delivery path the user reads** — gateway/platform log failures and
   reconnect cycles inside the window.

Green receipts with red machine or red delivery is NOT working — outputs
the user cannot receive or a machine too wedged to use fail the question in
any sense that matters. When user testimony contradicts telemetry, both are
usually true: reconcile (e.g. load 25 + platform reconnect loop while cron
executes hourly) instead of arguing receipts at the user. Close stale rows
whose work receipts already prove done (they make unclaimed-count probes
lie), but never present a closed row as new work.

## Verification

```bash
bash <agent-home>/scripts/<probe>_wrap.sh        # twice; byte-identical output
python3 -c "...executions ledger: job row status='completed'..."
python3 -c "...jobs.json: monitor_state has a hash, enabled=True..."
ps aux | sort -rk3 | head                     # load + top consumers
```

## Related Skills

- `daemon-cadence-architecture` — the three-layer composition law this
  pattern implements at the agent tier
- `message-bus-protocol` — claim/complete receipts for lane actions
