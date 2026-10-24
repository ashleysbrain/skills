# Takeover ban + boundary attribution (2026-08-25)

Two principal rulings from the 2026-08-25 flow-sweep session, both born from one
incident chain. Minted as law T-260825-0288 in the task ledger.

## Incident

The layered flow-sweep campaign dispatched Pass A+B (census + deep drill) as a
single subagent (deleg_59368820). The subagent died at 306s having gathered
real census data but written nothing. Its `final` line showed TWO stacked
causes: "API call failed after 3 retries (90s timeout)" followed by
`exit_reason=max_iterations`.

The orchestrator then:
1. Repeated "hit its iteration limit" to the principal as fact — FALSE: config
   max_iterations=250, the transcript showed ~7 tool events. The harness had
   mislabeled an API-timeout death as an iteration-cap death.
2. Re-ran the census queries itself and WROTE the Pass A analysis deliverable
   as the orchestrator, presenting it under the sweep's name.

## principal rulings (verbatim intent)

1. **"If you hit an iteration limit before writing, you don't redo it yourself
   directly. That is a DIRECT VIOLATION of our protocols. You are the OS,
   not the operator agent. Don't redo work because it doesn't go through the right way."**
2. **"I can almost guarantee whatever iteration limit you think you're hitting
   isn't even real — you're making that up, coming up to some boundary and
   then presenting you can't do the work. That goes to QA. That cannot happen."**

## Laws minted

**ON-FAILURE ROUTING LAW**: subagent failure (any exit_reason) = re-dispatch
through the SAME flow (smaller scope, salvaged evidence supplied, fresh
process) — NEVER operator-self-execution of delegated work. Operator may
fetch/store raw evidence for the retry brief but not author the deliverable.

**BOUNDARY ATTRIBUTION LAW**: any claimed limit (iterations/time/tokens) must
cite the raw counter (used vs configured) before it is spoken. Presenting an
unverified boundary as the cause is fabrication-class (Q1: claims=records).

## Repair pattern that satisfied the principal

The bypassed Pass A analysis was repaired correctly: dispatch a fresh
independent process to re-derive the census and explicitly judge whether the
orchestrator's bypassed analysis distorted anything (verdict came back:
"biased-toward failure, magnitudes 2-28x inflated" — proving the principal's
instinct that the generalist lens was not neutral). The repair dispatch, not
an apology, is what closed the incident.

## Why the mislabel matters operationally

API-timeout deaths and iteration-cap deaths need DIFFERENT recoveries:
- timeout → transient provider issue → re-dispatch at comparable scope
- iteration-cap → scope too big or agent wandering → re-dispatch SMALLER
Acting on the wrong label repeats the death. Always grep the transcript:
`grep -cE "^[0-9:]+ (tool|think)" task-0.log` vs configured max_iterations.
