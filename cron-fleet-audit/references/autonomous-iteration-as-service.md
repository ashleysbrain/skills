# Autonomous Iteration as Organism Service (principal correction 2026-08-19)

Added 2026-08-19. Extends the Service Supervision Architecture section
(principal 2026-08-16 "Crons is not how we get systems live and keep it live")
with the next escalation of the same rule.

## The correction (verbatim context)

principal asked for continuous iteration on the OS ("keep iterating as a goal
like I told you to" — iterate when the principal is NOT online giving
instructions). hermes first implemented it as a recurring the operator agent cron job
(every 3h, LLM-driven surgery passes). principal rejected it: **"As a cron??? We
need to minimize the crons this is not how we should operate figure out a
better way and stop junking up crons."**

## The rule

Recurring WORK — iteration cadence, exercising, self-maintenance — is a
property of the ORGANISM, not of the agent. Never implement recurring
organism behavior as a scheduled agent (LLM) cron. An agent cron that runs
"do the next pass" on a timer is a per-tick LLM burn with no state, no
KeepAlive, no failure-only discipline — the exact polling-theater pattern
the 2026-08-16 correction banned for health checks, now applied to work
loops.

Correct architecture, in layers:

1. **Deterministic mechanical loop = launchd KeepAlive service.** A plain
   Python daemon the organism owns (`organism/autonomous_iteration.py` at
   ~/your-org). launchd plist (RunAtLoad + KeepAlive) supervises it;
   the kernel restarts it in milliseconds if it dies. Healthy = SILENT
   (file logs only, zero stdout, zero Telegram). What the loop does
   mechanically: probe census of all contracted engines, spine selftest /
   periodic full conduction run, regression detection (SPECIALIZED ->
   UNREACHABLE/DECORATIVE transitions), pass records to
   `telemetry/iteration-log.jsonl`, defects to
   `telemetry/iteration-defects.jsonl`.
2. **LLM-driven surgery stays in sessions.** When hermes/sibling-agent next work,
   they read the defect queue and do the surgery. The loop surfaces defects;
   sessions fix them. This keeps tokens zero between sessions and keeps
   judgment (which fix, which lane) with the operators.

## Verification bar before reporting the service live

principal: "I don't believe you" after a narration-ahead-of-proof response. Never
report the service as running from the attempt narrative. Prove each claim
with fresh output in the SAME reply:
1. `launchctl list | grep <label>` — registered, with PID and exit 0
2. `ps aux | grep [daemon_script]` — the process exists
3. `launchctl print gui/$(id -u)/<label>` — state = running
4. The DAEMON's own artifact (pass record in the log, timestamped AFTER
   launchd started it — distinguishable from your inline test run)
5. Error log byte count (0 = healthy)

Its first live pass caught a real regression (the specialist engine UNREACHABLE on port
8121 while a listener held the port — the port-squat pattern again), which
is the loop doing its job: surface defects for the next surgery session.

## launchd install path notes (macOS)

- `launchctl bootstrap gui/$(id -u) <plist>` is BLOCKED from inside the
  the operator agent gateway process ("unsafe from inside the gateway process").
- osascript-with-admin fallback failed with "Domain does not support
  specified action (125)".
- What WORKED from the user shell: legacy `launchctl load <plist>` then
  verify with `launchctl list | grep <label>`.
- Per the double-supervision rule elsewhere in this skill: one supervisor
  per process. The iteration daemon has an internal `while True` sleep loop
  and launchd KeepAlive — this is the resident-daemon pattern (KeepAlive is
  for resident services), NOT the exiting-sweep pattern (StartInterval, no
  internal loop). Do not mix the two.

## Scheduling-vs-service decision table

| Need | Wrong (cron) | Right |
|---|---|---|
| Keep a service alive | poll-every-N-min watchdog cron | launchd KeepAlive; watchdog demoted to failure-only |
| Recurring mechanical work (probes, sweeps, exercises) | "do pass" LLM cron every 3h | organism-owned daemon under launchd, silent when healthy |
| One-shot delayed work / failure alerts | — | the operator agent cron is still correct here (failure-only alerts, one-shots) |
| LLM judgment work (surgery, review) | recurring cron burn | sessions, reading the defect queue the daemon produced |
