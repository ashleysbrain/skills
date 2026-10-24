# Explanation of Databases in OpenClaw Fleet Analytics

## analytics.db
- Located at: `~/.sibling-agent/workspace/intel/agents/database/analytics.db`
- Purpose: Stores aggregated analytics data for reporting and dashboards.
- Tables include: `agent_personas`, `cron_runs`, `journal_entries`, `agent_sessions`, `daily_cost_rollup`, `model_tier_distribution`, `cron_error_insights`, `error_log`, `personality_distribution`, `cron_jobs`, `fleet_health_snapshots`, `talent_insights`.
- Note: This database may show 0 rows for some tables immediately after a sync if the aggregation hasn't completed or if the sync script encountered issues.

## agents.db
- Located at: `~/.sibling-agent/workspace/intel/agents/database/agents.db`
- Purpose: Stores raw agent and cron job data, including configurations, runs, errors, and snapshots.
- Tables include: `active_agents_full`, `audit_log`, `personalities`, `agent_credentials`, `credential_pools`, `personality_performance`, `agent_leaderboard`, `cron_jobs`, `qa_tracking`, `agent_metrics_summary`, `cron_runs`, `review_panels`, `agent_performance`, `daily_cost_rollup`, `session_analytics`, `agent_sessions`, `domain_performance`, `task_analytics`, `agent_training`, `error_log`, `training_queue`, `agent_wellness`, `fleet_health_snapshots`, `wellness_dashboard`, `agents`, `journal_entries`, `agents_needing_attention`, `panel_reviewers`.
- Note: This database is the source of truth for agent configurations and cron job status. The fleet analytics sync script reads from here to populate analytics.db.

## Why Check agents.db?
When the fleet analytics sync script reports empty tables in analytics.db, the data is often still present in agents.db. This can happen due to:
- Timing issues: The sync script may have read from agents.db but not yet written to analytics.db.
- Selective sync: Some tables in analytics.db are only populated under certain conditions.
- Script errors: The sync script may have encountered an error after reading from agents.db but before writing to analytics.db.

Therefore, for real-time troubleshooting, always check agents.db first.