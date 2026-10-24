# Fleet Analytics Sync Notes

## Sync Command Output
The sync script outputs:
- Synced cron jobs count
- Session data sync status
- Journal compliance indexing
- Analytics collection pipeline completion
- Fleet health snapshot with metrics:
  - Agents active/total
  - Cron enabled/erroring/disabled
  - Errors (24h) total, rate limit, timeout
  - Sessions (24h)
  - Journal compliance percentage

## Key Database Tables
- `cron_jobs`: status (enabled, disabled, error, paused)
- `cron_runs`: status (success, error, timeout, cancelled), error_type
- `error_log`: severity (low, medium, high, critical), error_type
- `model_tier_distribution`: tier, agent_count, percentage
- `daily_productivity`: daily aggregates
- `fleet_health_snapshots`: daily snapshot

## Useful Queries
### Cron Job Status Distribution
```sql
SELECT status, COUNT(*) FROM cron_jobs GROUP BY status;
```

### Top Error Types (Last 24h)
```sql
SELECT error_type, COUNT(*) as count 
FROM cron_runs 
WHERE started_at >= datetime('now', '-24 hours') 
AND status IN ('error', 'timeout') 
GROUP BY error_type 
ORDER BY count DESC 
LIMIT 5;
```

### Model Distribution (Latest)
```sql
SELECT tier, agent_count, percentage 
FROM model_tier_distribution 
WHERE review_date = (SELECT MAX(review_date) FROM model_tier_distribution);
```

### Active Agents
```sql
SELECT COUNT(*) FROM agents WHERE status = 'active';
```

### Journal Compliance (Latest)
```sql
SELECT * FROM daily_productivity ORDER BY date DESC LIMIT 1;
```

## Pitfalls
- Deprecation warnings for `datetime.utcnow()` are non-fatal.
- Missing the operator agent sessions table results in sync error but continues.
- Ensure analytics database is writable.
