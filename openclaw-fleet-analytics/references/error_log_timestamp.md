# Error Log Timestamp Column Usage

When querying the `error_log` table in the OpenClaw fleet analytics database, use the `occurred_at` column for time-based filters, not `timestamp`.

## Correct Usage
```sql
SELECT error_message, COUNT(*) as cnt
FROM error_log
WHERE occurred_at > datetime('now', '-1 day')
GROUP BY error_message
ORDER BY cnt DESC
LIMIT 5;
```

## Incorrect Usage (will return no results)
```sql
SELECT error_message, COUNT(*) as cnt
FROM error_log
WHERE timestamp > datetime('now', '-1 day')  -- Wrong column name
GROUP BY error_message
ORDER BY cnt DESC
LIMIT 5;
```

## Table Schema Reference
The `error_log` table has the following relevant columns:
- `id` (INTEGER)
- `agent_id` (INTEGER)
- `persona_id` (INTEGER)
- `session_id` (TEXT)
- `cron_job_id` (TEXT)
- `error_type` (TEXT)
- `error_message` (TEXT)
- `error_context` (TEXT)
- `resolved` (BOOLEAN)
- `resolved_at` (TIMESTAMP)
- `resolution_note` (TEXT)
- `severity` (TEXT)
- `user_impact` (BOOLEAN)
- `occurred_at` (TIMESTAMP) ← USE THIS COLUMN FOR TIME FILTERS

Note: There is no `timestamp` column in this table.