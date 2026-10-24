# Iteration-Cap Salvage — MR13/MR14 Sessions (2026-08-19)

Companion to the timeout-salvage pattern. A specialist that hits
`max_iterations` is a DIFFERENT failure class than timeout: the work is
DONE, the report file is NOT written.

## Observed case (the specialist engine, MR14-C build-lane audit)

- Status line: `status=completed, TRUNCATED: hit max_iterations — work
  may be incomplete`. 50 api_calls over 1769s; the specialist spent its
  budget on deep live probes (watched 3 cron boundaries fire-or-not,
  kickstarted the build loop, traced bus consumption) and never reached
  the report-write step.
- The final summary the harness captures began: "Report file NOT yet
  written... Full report content is below for the parent to persist at
  <audit path>." — specialists near the cap self-triage into this mode.

## Salvage procedure

1. The truncated harness delivery names a full-summary file:
   `<agent-home>/cache/delegation/subagent-summary-<N>-<timestamp>.txt`.
   Read it — it carries the complete report (grade, numbered findings,
   severities, remediation order, restore-state obligations).
2. Persist it VERBATIM to the audit path the specialist specified,
   with a provenance note in the header: "reviewer hit iteration cap
   before the file write; content persisted verbatim from the
   reviewer's final summary by <operator>."
3. If the summary is thin, the live transcript is the second source:
   `<agent-home>/cache/delegation/live/<deleg>/task-<N>.log`, and
   `grep -E "think"` tail lines carry conclusion fragments.
4. ACTION the restore-state obligations: probe specialists that mutated
   prod during verification (snapshots in /tmp, marked items, posted bus
   rows) leave explicit restore instructions in the summary. Execute
   them — the kickstart case left `build-queue.yaml.pre14c` to restore
   and stranded-state to rescue.

## Why not re-dispatch

A re-dispatch re-derives 30 minutes of live probing AND likely
reproduces the cap (the probe depth is what consumed the budget). The
content is already captured; persisting it is mechanical extraction,
which is orchestrator work, not specialist authorship.

## Prevention for future dispatches

When a brief demands deep live probing AND a written report, add to the
contract: "Write the report file EARLY at 70% budget with findings so
far, then continue probing and amend." Report-first ordering converts
iteration-cap deaths into partial-delivery successes.
