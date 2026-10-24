# Baseline Verification for Proprietary TWC Scoring

When using the baseline file for drift detection in proprietary TWC scoring, always verify that the baseline TWC value matches the stored TWC for that date in the database.

## Why
The baseline file (e.g., `~/your-workspace/health-private/algorithm-integrity-baseline.json`) is used to detect drift. If the baseline value does not match the stored TWC for the same date, drift calculations will be incorrect.

## How to Verify
1. Read the baseline file to get the baseline date and TWC value.
2. Query the `daily_scorecard` table for the TWC score on that date.
3. Compare the values. If they differ, investigate the cause (e.g., baseline file outdated, database entry incorrect, etc.) before proceeding with drift analysis.

## Example Verification Query
```bash
# Read baseline file
cat ~/your-workspace/health-private/algorithm-integrity-baseline.json

# Query database for the same date
sqlite3 ~/your-workspace/health-private/ashley_unified_health.db "
  SELECT date, twc_score FROM daily_scorecard WHERE date = '<baseline-date>';
"
```

## Notes
- The baseline file is versioned and should be updated when the baseline changes.
- Do not assume the baseline file is always correct; verify against the source of truth (the database).