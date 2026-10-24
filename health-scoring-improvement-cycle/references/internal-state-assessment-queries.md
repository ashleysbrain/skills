# Internal State Assessment Queries for Health Scoring Improvement Cycles

These queries are used to assess the current state of the scoring system during improvement cycles.

## Current Methodology State

```sql
-- Activity database maturity
SELECT COUNT(*) FROM master_activities WHERE is_active=1;

SELECT primary_dimension, COUNT(*) 
FROM master_activities WHERE is_active=1 
GROUP BY primary_dimension;

SELECT COUNT(DISTINCT date) 
FROM daily_scorecard 
WHERE date >= date('now', '-90 days');

-- Interaction matrix state
SELECT COUNT(*) FROM interaction_matrix;

SELECT AVG(value), MIN(value), MAX(value) 
FROM interaction_matrix;

-- Engine inventory
SELECT name FROM sqlite_master WHERE type='table';

-- Check for scoring methodology docs (requires file system access)
-- This would typically be done outside SQLite
```

## Formatted Output Commands

For clean, sorted dimension balance output:
```bash
printf '%s\n' "Dimension balance:" $(sqlite3 "/<workspace>" "SELECT primary_dimension || ':' || COUNT(*) FROM master_activities WHERE is_active=1 GROUP BY primary_dimension" | sort -t: -k2 -nr)
```

## Usage in Improvement Cycles

These queries should be run at the beginning of each health scoring improvement cycle to establish baseline metrics before identifying improvement opportunities.

Key metrics to track:
- Total active activities (target: 120-160)
- Dimension balance (target: 15-20 per dimension)
- 90-day scoring coverage (target: ≥60 days)
- Interaction matrix pairs (should be 28 for 8 dimensions)
- Average interaction value (should be in reasonable range, typically 0.1-0.3)

Reference: Used in horizon scan procedure step 1 and health scoring improvement cycle procedure step 1.