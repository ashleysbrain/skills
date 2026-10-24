# Adaptive baseline bridge

## Purpose
Capture the session-specific rule that 8D/TWC rescoring must be baseline-aware, not a fixed 1-10 guess.

## Canonical flow
1. Load the user's baseline seed from `calibration.json`.
2. Treat baselines as versioned and driftable, not static.
3. Build a small structured evidence payload from the message/transcript.
4. Apply the baseline-aware bridge to adjust the raw dimension estimates.
5. Run `compute_twc()` so the full coupling matrix, coherence, and synergy still apply.
6. Persist baseline metadata alongside the score.

## DB fields added for traceability
- `baseline_version`
- `baseline_source`
- `baseline_bridge`

## Practical rule
If the text parser emits flat/neutral dimensions that contradict the evidence, do not use those numbers directly. Use the adaptive baseline bridge and then call the coupled TWC engine.

## Drift rule
Baselines can change over time. Always preserve the previous baseline snapshot/history and treat the current calibration as the active version for scoring.