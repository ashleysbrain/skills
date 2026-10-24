# TWC History Table Issue - 2026-06-02

## Observation
During the VERITAS-ALGO integrity check on 2026-06-02, the twc_history table was found to have data but with empty values for key tracking fields:

- Table exists and has date/TWC/label entries
- However, pcm, csi, deficit_penalty, and momentum fields are empty/NULL
- This confirms the issue reported: "twc_history table not populated by current pipeline (discovered 2026-06-01 VERITAS-ALGO)"

## Context
The twc_history table is meant to store:
- TWC (Total Wellness Composite)
- PCM (Principal Component Metric)
- CSI (Coherence Stability Index)
- deficit_penalty
- momentum
- label

Without PCM, CSI, deficit_penalty, and momentum data, the momentum tracking (momentum coefficient=0.05) and PCM/CSI computation features are offline.

## Related Pitfalls
This issue is documented in the proprietary-twc-scoring skill:
- "twc_history table not populated by current pipeline (discovered 2026-06-01 VERITAS-ALGO) — The current scoring pipeline writes TWC to daily_scorecard but does NOT write to twc_history. This means momentum tracking (momentum coefficient=0.05) and PCM/CSI computation features are offline. The pipeline needs a reconnect step."

## Action Required
The scoring pipeline needs to be updated to populate the twc_history table with all required fields, not just TWC, date, and label. Specifically, it needs to compute and store:
- PCM (Principal Component Metric)
- CSI (Coherence Stability Index)
- deficit_penalty
- momentum

This reconnect step is necessary to restore the full functionality of the TWC history tracking features.