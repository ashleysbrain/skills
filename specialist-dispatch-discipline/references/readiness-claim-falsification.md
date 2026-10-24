# Readiness-Claim Falsification — reference (2026-08-16 gap-map QA session)

The digest-before-dispatch pattern and the readiness-claim kill list, from the session where a formally-rigorous specialist analysis (Lamport seat, interconnect gap map) rested on instrumentation that does not exist.

## The failure pattern
Lamport's interconnect gap analysis was internally rigorous — correct formal gaps (no global event order, belief double-spend, no 2PC-for-code, the well-formed-confident-wrong fault class), correct white-space mapping. But its claims about OUR readiness referenced telemetry the engine does not have. The analysis would have propagated into the preprint as "we already compute X."

## Digest-before-dispatch (the mechanical step the parent runs FIRST)
Before dispatching any specialist whose deliverable will assert what our systems "already" do:
1. `grep -n` the actual engine for each telemetry field / log / interface the claims will rest on.
2. Record what EXISTS vs what is merely NAMED in docs/plans.
3. Embed the digest results in the falsifier's dispatch as ground truth.

Proven digest (canonical_coupling_ai.py, 478 lines, 2026-08-16):
- Telemetry consumed: per-dimension lists (PIPE: tool_failure_rate, api_latency_p95, stale_reference_rate, context_age_hours; RES: tokens_per_task_normalized, model_tier_routing_accuracy, retry_abandon_ratio, cost_trajectory_slope, budget_adherence_pct; INTER: handoff_rework_rate...)
- NO timestamped event log at engine level — the only {timestamp, spec, v1} append is the 30-day validation/shadow log for formula comparison
- NO belief/world-state capture anywhere
- NO rejection/mutation log — "rollback" appears only in the v1-formula deprecation policy
- NO clock/skew capture — api_latency_p95 is the only latency-adjacent field

## The verdict format that worked (Popper, 7 claims)
Each claim: SURVIVES / QUALIFIES (how) / DIES, plus corrected build order, the single most dangerous overclaim for the preprint, and the true prerequisite chain.

Results that session:
1. "HLC skew computable from existing traces TODAY" — DIES. Skew needs pairwise event timestamps across nodes; the engine has one scalar p95 from one clock. A latency percentile is not a clock reading.
2. "Curvature spikes precede desynchronization" — QUALIFIES, fatally as stated. Circular until an independent desync label exists; scores fold the same telemetry that would register desync.
3. "We already compute the rejection signal" — DIES, most dangerous. The engine is a pure function: scores in, scalar out. Threshold readout != rejection. One reviewer probe finds this and everything else inherits the doubt.
4. "Coupling IS consensus-health" — DIES as identity. A hand-set matrix over one system's dimension scores; consensus requires >=2 agents' beliefs, the engine represents zero beliefs.
5. "SYNC+TRUST scoring on existing telemetry" — QUALIFIES. A proxy yes; the real dimensions need an instrumentation sprint first.
6. "6+1 -> 6+3 in the preprint" — QUALIFIES, dangerously. Preprint stays 6+1 grounded; 6+3 is future work ONLY, or scope creep enters the funding plan's critical path.
7. "Landscape guarantees none of the four properties" — SURVIVES with tightened definition: checkpointing = state restoration (resume/replay); the claim is invariant-enforcing rejection with causal ordering. Reword before publishing or a reviewer kills it.

## Prerequisite-0: build it the same session
The corrected build order named prerequisite-0 (event capture). It was built immediately, not scheduled:
- `organism/event_capture.py` — append-only {ts, counter, node, type, payload}, thread-safe, pure telemetry substrate, no scoring logic
- Hooked into `composite()` via a guarded `_emit_event("score_call", ...)` import (try/except so standalone use still works)
- PROVEN: a live scoring call (composite=0.9736) landed in organism/event_log.jsonl with node + timestamp
- Accumulation starts the day the gap is found, not the day someone needs the data

Full corrected build order: 0-event-capture -> 1-mine the 30-day shadow log for backfill -> 2-SYNC proxy labeled PROXY -> 3-REJECT as dispatcher-level mutation gate (new code, NOT engine) -> 4-TRUST after weeks of belief data -> 5-HLC last.

## Transferable rules
- A specialist's strategy can be directionally right while its readiness claims are fiction. Falsify the claims, keep the strategy, build the missing prerequisite immediately.
- Every "already / today / for free" adverb in a specialist deliverable is a claim requiring digest verification.
- Scoring engines measure; they do not enforce. Never let a readout be described as a gate in public artifacts.
- Public artifacts (preprints, pitches) carry only grounded claims; ungrounded dimensions are future work by name.
