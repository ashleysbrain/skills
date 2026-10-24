# Pipeline Coverage Gap - 2026-06-02

## Observation
During the VERITAS-ALGO integrity check on 2026-06-02, a pipeline coverage gap was identified:

- Only 3 out of the last 7 days have data in the daily_scorecard table
- This indicates missing scores for recent days

## Context
This finding aligns with the documented "Pipeline coverage gap" pitfall mentioned multiple times in the health-scoring-daily-pipeline skill and related skills.

## Related Skills and Documentation
This issue is referenced in:
- proprietary-twc-scoring skill (mentioned twice)
- health-scoring-daily-pipeline skill (mentioned multiple times)
- qubit-gr-8d360-scoring-pipeline skill
- rescore-engine-usage skill

## Required Action
When pipeline coverage gaps are identified, the correct procedure (per the skills) is:

1. **Do NOT backfill automatically** - This could compromise data integrity
2. **Check for available evidence sources** for the missing dates:
   - Standup transcripts
   - Voice memos
   - Other health data sources
3. **Process available evidence through the scoring pipeline** before considering the day complete
4. **Only leave days blank if no evidence exists** - Missing days should remain blank only when there is genuinely no data to process

## Implementation Notes
This is not just a data issue but a procedural one. The integrity check itself should include verification of this pipeline coverage gap and reporting on it, but the actual processing of missing data should be handled by the appropriate scoring pipeline (likely via AISHA-MD or related processes).

The VERITAS-ALGO integrity check should flag this gap but not attempt to fill it, as doing so would violate the core principle of not backfilling automatically.