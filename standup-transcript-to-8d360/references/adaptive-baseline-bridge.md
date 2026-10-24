# Adaptive Baseline Bridge for 8D360 Standups

Session-derived notes for baseline-aware scoring.

## Core rule
A transcript or voice note is not converted directly into the final TWC. It should be routed through:
1. transcript/evidence parsing
2. baseline-aware normalization
3. adaptive calibration/baseline lookup
4. 8D calculator engine (`calculator.py` via `score_from_evidence.compute_twc()`)
5. DB persistence of both score and baseline metadata

## What to persist
When available, persist these on the daily row:
- `baseline_version`
- `baseline_source`
- `baseline_bridge`
- `coherence`
- `synergy`
- `coupling_sum`
- `score_engine` (expected: `calculator_v3`)

## User-specific lesson
Do not let the availability of the complex coupling engine tempt you into using guessed 1-10 values as final truth. Those values are only an intermediate estimate. The bridge must be evidence-first and baseline-aware.

## Transcript path lesson
For solo standups and voice notes, combine the transcript adapter's richer signal extraction with the baseline bridge before computing TWC. If the first pass looks too close to a generic weighted average, the bridge is too weak.

## Verification
- Dry-run the scoring path and inspect coherence/synergy output.
- Confirm the DB row carries baseline metadata, not just score values.
- If the live result still resembles the simplistic scorer, revisit the transcript adapter signals before changing the calculator.
