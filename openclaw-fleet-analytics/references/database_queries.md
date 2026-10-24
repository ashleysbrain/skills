# Fleet Analytics Database Queries

## Queries Used in Recent Sync Session

### Status Distribution (from agents.db)
```sql
SELECT status, COUNT(*) as count FROM cron_jobs GROUP BY status;
```
Returns: disabled|268, enabled|14, error|110

### Top 5 Errors (from cron_runs - last 24h)
```sql
SELECT 
    COALESCE(NULLIF(error_message, ''), 'unknown_error') as error_message,
    COUNT(*) as count
FROM cron_runs
WHERE status = 'error'
    AND started_at > datetime('now', '-1 day')
GROUP BY error_message
ORDER BY count DESC
LIMIT 5;
```
Returns: 
- model_not_found: 1721
- [empty]: 1174  
- timeout: 139

### Model Distribution (for cron jobs)
```sql
SELECT model, COUNT(*) as count
FROM cron_jobs
WHERE model IS NOT NULL AND model != ''
GROUP BY model
ORDER BY count DESC
LIMIT 5;
```
Returns various models with counts (specific counts not captured in output)

### Journal Compliance Check
```sql
SELECT journal_compliance_pct
FROM fleet_health_snapshots
WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM fleet_health_snapshots)
ORDER BY created_at DESC
LIMIT 1;
```
Returns: 0.0% (from fleet health snapshot)

### Error Tracking Baseline Comparison
```bash
# Get baseline from tracking file
BASELINE=$(cat ~/.sibling-agent/workspace/intel/agents/database/last_error_count.txt 2>/dev/null || echo 0)
# Get current error count from last 24h (from cron runs)
CURRENT=$(sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT COUNT(*) FROM cron_runs WHERE status='error' AND started_at > datetime('now', '-1 day');")
# Calculate new errors
NEW_ERRORS=$((CURRENT - BASELINE))
echo "Baseline errors (from last sync): $BASELINE"
echo "Current errors (last 24h): $CURRENT"
echo "New errors: $NEW_ERRORS"
```

### New Error Types Detection
```sql
SELECT COUNT(DISTINCT error_message) FROM error_log WHERE occurred_at > '$LAST_SYNC';
```
Where LAST_SYNC comes from last_sync.timestamp file

## Schema References

### cron_jobs table
- status: enabled/disabled/error/paused
- consecutive_errors: integer count
- last_error_message: text
- last_error_at: timestamp
- model: text (e.g., "gemini-2.5-flash", "nvidia/nemotron-3-super-120b-a12b:free")

### cron_runs table
- cron_job_id: foreign key to cron_jobs
- started_at: timestamp
- ended_at: timestamp  
- status: success/error/timeout/cancelled
- error_type: text
- error_message: text
- model_used: text
- cost_usd: real

### error_log table
- error_type: text (e.g., "system_auth_failure")
- error_message: text description
- error_context: text
- occurred_at: timestamp
- critical: boolean (0/1)

### fleet_health_snapshots table
- snapshot_date: date
- total_agents: integer
- active_agents: integer
- cron_enabled: integer
- cron_erroring: integer
- cron_disabled: integer
- total_errors_24h: integer
- rate_limit_errors_24h: integer
- timeout_errors_24h: integer
- total_sessions_24h: integer
- journal_compliance_pct: real
- fleet_twc: real
- avg_quality_score: real
- avg_success_rate: real