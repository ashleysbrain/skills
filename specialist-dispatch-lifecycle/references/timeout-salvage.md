# Subagent timeout: config knob + salvage pattern (verified 2026-08-18)

## Config
<agent-home>/config.yaml -> delegation.child_timeout_seconds. Default 900 caused
three same-day timeouts on multi-lane QA panels (Luria 901s; Lamport 900s with
only 9 API calls completed). Raised to 1800. Check this knob FIRST when a
specialist times out mid-review; do not just re-dispatch into the same ceiling.

## Salvage pattern (timeout already happened)
The live transcript survives: /<workspace><deleg_id>/task-N.log
Complete tool trace with timestamps. Extract:
- "think" lines -> findings/verdicts the child reached
- "result" lines -> raw measurements it actually took
Then independently re-verify every salvaged claim with your own probes and file
the report with an honest disposition line ("timed out at ceiling after
analysis phase; findings salvaged from transcript and verified by operator").
Never propagate child self-claims unverified; never present salvage as
first-author completion.

## Async completion duplicates
The ASYNC DELEGATION BATCH COMPLETE notification for an already-salvaged run
arrives later and carries no new content (status=timeout, no summary). Do not
re-run work on its arrival; verify artifacts on disk instead.

## Parallel dispatch note
Two leaf children in one batch (systems brain + state brain) worked well and
did not clobber each other when both were report-only. Builder fixes should
land BETWEEN passes, not during one (freeze discipline, see
sequential-multi-agent-audit-execution/references/different-brain-qa-sequence.md).
