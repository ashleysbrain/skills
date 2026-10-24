# Fleet Analytics Sync: Detailed Reporting

When running the fleet analytics sync, the script outputs a summary that includes:
   - Number of cron jobs synced
   - Status distribution (enabled, erroring, disabled)
   - Journal compliance

However, for more detailed information such as:
   - Top 5 errors (by message)
   - Model distribution
   - Error trends

you need to query the agents.db database directly.

Example queries:

   -- Total errors in the last 24h
   SELECT COUNT(*) FROM cron_runs WHERE status='error' AND started_at > datetime('now', '-1 day');

   -- Top 5 error messages in the last 24h
   SELECT error_message, COUNT(*) as cnt
   FROM cron_runs
   WHERE status='error' AND started_at > datetime('now', '-1 day')
   GROUP BY error_message
   ORDER BY cnt DESC
   LIMIT 5;

   -- Model distribution in the last 24h
   SELECT model_used, COUNT(*) as cnt
   FROM cron_runs
   WHERE started_at > datetime('now', '-1 day')
   GROUP BY model_used
   ORDER BY cnt DESC;

   -- Error types distribution (if error_type is populated)
   SELECT error_type, COUNT(*) as cnt
   FROM cron_runs
   WHERE status='error' AND started_at > datetime('now', '-1 day')
   GROUP BY error_type
   ORDER BY cnt DESC;

   -- Journal compliance percentage (if available in the fleet_health_snapshots table)
   SELECT journal_compliance_pct
   FROM fleet_health_snapshots
   WHERE snapshot_date = date('now')
   ORDER BY id DESC
   LIMIT 1;