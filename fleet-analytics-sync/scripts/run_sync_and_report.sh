#!/bin/bash
# Fleet Analytics Sync and Report Script
# Runs the sync and outputs a summary report

set -e

echo "=== Fleet Analytics Sync and Report ==="
echo "Starting sync at $(date)"
echo

# Run the sync
python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync 2>&1 | tee /tmp/fleet_sync_output.log
SYNC_EXIT=${PIPESTATUS[0]}

echo
echo "=== Sync Output ==="
tail -20 /tmp/fleet_sync_output.log
echo

# Check if sync succeeded
if [ $SYNC_EXIT -ne 0 ]; then
    echo "Sync failed with exit code $SYNC_EXIT"
    exit $SYNC_EXIT
fi

echo "=== Summary Report ==="
echo "Timestamp: $(date)"
echo

# Query analytics database for summary
ANALYTICS_DB=~/.sibling-agent/workspace/intel/agents/database/analytics.db
AGENTS_DB=~/.sibling-agent/workspace/intel/agents/database/agents.db

if [ -f "$ANALYTICS_DB" ]; then
    echo "--- Analytics Database ---"
    # Total cron jobs
    TOTAL_JOBS=$(sqlite3 "$ANALYTICS_DB" "SELECT COUNT(*) FROM cron_jobs;" 2>/dev/null || echo "Error")
    echo "Total cron jobs in analytics.db: $TOTAL_JOBS"
    
    # Status distribution
    echo "Status distribution:"
    sqlite3 "$ANALYTICS_DB" "SELECT status, COUNT(*) FROM cron_jobs GROUP BY status;" 2>/dev/null || echo "  Error querying status"
else
    echo "Analytics database not found: $ANALYTICS_DB"
fi

echo
if [ -f "$AGENTS_DB" ]; then
    echo "--- Agents Database ---"
    # Active agents
    ACTIVE_AGENTS=$(sqlite3 "$AGENTS_DB" "SELECT COUNT(*) FROM agents WHERE status = 'active';" 2>/dev/null || echo "Error")
    echo "Active agents: $ACTIVE_AGENTS"
    
    # Cron job status from agents.db (alternative source)
    echo "Cron job status from agents.db:"
    sqlite3 "$AGENTS_DB" "SELECT status, COUNT(*) FROM cron_jobs GROUP BY status;" 2>/dev/null || echo "  Error querying status"
    
    # Top errors last 24h
    echo "Top error types (last 24h):"
    sqlite3 "$AGENTS_DB" "SELECT error_type, COUNT(*) as count FROM cron_runs WHERE started_at >= datetime('now', '-24 hours') AND status IN ('error', 'timeout') GROUP BY error_type ORDER BY count DESC LIMIT 5;" 2>/dev/null || echo "  Error querying errors"
    
    # Model distribution
    echo "Model distribution (latest):"
    sqlite3 "$AGENTS_DB" "SELECT tier, agent_count, percentage FROM model_tier_distribution WHERE review_date = (SELECT MAX(review_date) FROM model_tier_distribution);" 2>/dev/null || echo "  Error querying model distribution"
else
    echo "Agents database not found: $AGENTS_DB"
fi

echo
echo "=== Report Complete ==="