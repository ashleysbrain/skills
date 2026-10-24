# Fleet Health Snapshot Fields

The fleet_health_snapshots table stores the following columns:

- snapshot_date (date)
- snapshot_type (e.g., 'daily')
- total_agents (int)
- active_agents (int)
- erroring_agents (int, cron jobs with status='error')
- disabled_agents (int, cron jobs enabled=0)
- fleet_twc (placeholder, hardcoded 7.41)
- avg_quality_score (from agent_performance)
- avg_success_rate (from agent_metrics_summary)
- total_sessions (agent_sessions in last 24h)
- total_tokens (sum total_tokens in last 24h)
- total_cost_usd (sum estimated_cost_usd in last 24h)
- total_errors (cron_runs status='error' last 24h)
- rate_limit_errors (error_type='rate_limit' last 24h)
- timeout_errors (error_type='timeout' last 24h)
- journal_compliance_pct (percentage of agents with journal entry today)
- details (JSON blob with extra info)

These fields are populated by take_health_snapshot() function.