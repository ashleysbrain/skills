#!/usr/bin/env bash
# Script: verify_sync.sh
# Purpose: Verify the fleet analytics sync by checking both analytics.db and agents.db
# Usage: ./verify_sync.sh

set -euo pipefail

ANALYTICS_DB="$HOME/.sibling-agent/workspace/intel/agents/database/analytics.db"
AGENTS_DB="$HOME/.sibling-agent/workspace/intel/agents/database/agents.db"

echo "=== Fleet Analytics Sync Verification ==="
echo "Checking analytics.db: $ANALYTICS_DB"
echo "Checking agents.db: $AGENTS_DB"
echo

# Check if databases exist
if [[ ! -f "$ANALYTICS_DB" ]]; then
  echo "ERROR: analytics.db not found at $ANALYTICS_DB"
  exit 1
fi

if [[ ! -f "$AGENTS_DB" ]]; then
  echo "ERROR: agents.db not found at $AGENTS_DB"
  exit 1
fi

echo "--- analytics.db key tables ---"
sqlite3 "$ANALYTICS_DB" <<SQL
.headers on
.mode column
SELECT 'task_analytics' as table, COUNT(*) as count FROM task_analytics;
SELECT 'daily_productivity' as table, COUNT(*) as count FROM daily_productivity;
SELECT 'session_analytics' as table, COUNT(*) as count FROM session_analytics;
SELECT 'cron_jobs' as table, COUNT(*) as count FROM cron_jobs;
SELECT 'fleet_health_snapshots' as table, COUNT(*) as count FROM fleet_health_snapshots;
SQL

echo
echo "--- agents.db key tables ---"
sqlite3 "$AGENTS_DB" <<SQL
.headers on
.mode column
SELECT 'cron_jobs status distribution' as info, status, COUNT(*) as count FROM cron_jobs GROUP BY status;
SELECT 'total cron_jobs' as info, COUNT(*) as count FROM cron_jobs;
SELECT 'most_recent_snapshot' as info, snapshot_date, total_agents, active_agents, erroring_agents, disabled_agents, total_errors, journal_compliance_pct FROM fleet_health_snapshots ORDER BY snapshot_date DESC LIMIT 1;
SELECT 'top_5_error_types_last_24h' as info, error_type, COUNT(*) as count FROM error_log WHERE occurred_at >= datetime('now', '-1 day') GROUP BY error_type ORDER BY count DESC LIMIT 5;
SQL

echo
echo "=== Verification Complete ==="