# Error Interpretation for Fleet Analytics Sync

## Common Errors
1. **the operator agent sessions error: no such table: sessions**
   - Occurs when the the operator agent sessions database is missing or not initialized.
   - Non-fatal; sync continues for other data.
   - Check if `<agent-home>/hermes_sessions.db` exists.

2. **Deprecation warnings: datetime.datetime.utcnow() is deprecated**
   - These warnings do not affect functionality but should be addressed.
   - Fix: Use `datetime.now(datetime.UTC)` for timezone-aware timestamps.

3. **Sync errors in output**
   - Look for lines with `✗` in the sync output.
   - Example: `✗ the operator agent sessions error: no such table: sessions`
   - Other errors may indicate actual failures in data collection.

## Checking Error Logs
The `error_log` table in `agents.db` contains detailed error records.
Query example:
```sql
SELECT error_type, error_message, COUNT(*) as count
FROM cron_runs
WHERE datetime(ended_at) >= datetime('now', '-1 day')
  AND (status='error' OR error_type IS NOT NULL)
GROUP BY error_type, error_message
ORDER BY count DESC;
```

## Top Errors (24h)
Typically, the most common error is `timeout` indicating agent execution timeouts.