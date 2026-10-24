# PENDING SKILL.md PATCH — your-stack-operations (from QA-31..34 session, 2026-08-18)

Curator: apply this to SKILL.md "Package map" section (insert after the
task→workstream bullet). Refused by _read_before_write guard in background
session; parked here per standing practice.

## Insert after the task→workstream mapping bullet

- **Engine work surfaces** (QA-31..34): `organism/engine_dispatch.py` +
  `stores/engine-contracts.json` = the efferent limb (ledger task ->
  routing_gate specialist WITH a port -> dialect-correct POST -> result to
  ledger+bus). `gates/engine_liveness_sentinel.py` = liveness patrol feeding
  telemetry/events.jsonl (without it health-overrides stay empty and dead
  engines route as healthy). NEVER trust engine self-reports — all-green on
  empty output is the verified fleet pathology; use differential probes
  (opposite inputs + determinism + echo) before wiring any engine:
  `references/engine-specialization-probes-2026-08-18.md`.

## Also consider adding to "Iteration protocol" (step 7)

7. **All-night/iteration passes**: rotate a DIFFERENT elite specialist per
   phase, record the rotation in the report header (L9 dogfood), and end
   EVERY pass by writing NEXT PASS GOALS into audit/RUN-RECORD.md so the
   next brain starts warm. Verify sibling closures by falsification, never
   self-reports.

(Rationale: principal standing directive 2026-08-18 "iterate as a goal without
stopping... different brains every process". The reference file
engine-specialization-probes-2026-08-18.md already carries the detail.)
