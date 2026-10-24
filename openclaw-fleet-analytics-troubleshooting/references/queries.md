# Useful Queries for Fleet Analytics Troubleshooting

## Status distribution (enabled/error/disabled)
SELECT status, COUNT(*) as count 
FROM cron_jobs 
GROUP BY status;

## Total cron jobs synced
SELECT COUNT(*) FROM cron_jobs;

## Most recent fleet health snapshot
SELECT snapshot_date, total_agents, active_agents, erroring_agents, disabled_agents, 
       total_errors, rate_limit_errors, timeout_errors, total_sessions, journal_compliance_pct
FROM fleet_health_snapshots
ORDER BY snapshot_date DESC
LIMIT 1;

## Top 5 error types in the last day
SELECT error_type, COUNT(*) as count 
FROM error_log 
WHERE occurred_at >= datetime('now', '-1 day')
GROUP BY error_type 
ORDER BY count DESC
LIMIT 5;

## Total errors in last 24 hours
SELECT COUNT(*) FROM error_log 
WHERE occurred_at >= datetime('now', '-1 day');

## Model usage distribution (from cron_jobs)
SELECT model, COUNT(*) as count 
FROM cron_jobs 
WHERE model IS NOT NULL
GROUP BY model 
ORDER BY count DESC;

## Journal compliance percentage from latest snapshot
SELECT journal_compliance_pct
FROM fleet_health_snapshots
ORDER BY snapshot_date DESC
LIMIT 1;