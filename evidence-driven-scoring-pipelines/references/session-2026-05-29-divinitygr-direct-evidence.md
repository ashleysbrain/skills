# DivinityGR direct-evidence rollout notes

## What changed
- The active scoring path must not use a covert 1–10 bridge as the scientific input layer.
- The complex engine (`calculator_v3` / `calculator.py`) should receive native inputs directly.
- Any bounded 1–10 values are display/storage normalization only.

## Key lesson
If the score looks too low or too generic, the bug is usually upstream evidence coverage, not the engine math.

## Verified design pattern
1. Evidence adapters collect raw signals.
2. Field-level inference maps evidence into native calculator inputs.
3. The complex calculator runs once.
4. Optional support overlays (nutrition, sexual health, EF/ADHD) are applied after the core run.
5. Persistence writes engine/version/baseline metadata for auditability.

## Next evidence-source adapters to add
- Calendar: meetings, deep-work blocks, cancellations, travel, recovery windows
- Wearables: sleep, resting HR, HRV, steps, activity load
- Finance/spending: purchases, category drift, stress spending, savings behavior
- Messages/social graph: interaction cadence, support, conflict, isolation, reciprocity
- Tasks/quests: completion history, streaks, overdue items, goal progress

## Pitfalls
- Do not compensate for missing evidence by inflating scores.
- Do not let transcript heuristics overwrite stronger source data.
- Do not treat display normalization as scientific scoring.