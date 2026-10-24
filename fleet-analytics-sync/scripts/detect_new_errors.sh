#!/usr/bin/env bash
# Script to detect new critical errors in cron jobs since last run.
# Outputs list of newly erroring job IDs and names.

set -euo pipefail

DB_PATH="$HOME/.sibling-agent/workspace/intel/agents/database/agents.db"
STATE_FILE="$HOME/.hermes/fleet_analytics_last_erroring_jobs.txt"

# Get current erroring job IDs
CURRENT_ERRORS=$(sqlite3 "$DB_PATH" "SELECT job_id FROM cron_jobs WHERE status='error';" | sort | uniq | grep -v '^$' || true)
CURRENT_COUNT=$(echo "$CURRENT_ERRORS" | wc -l)

# Read previous errors if file exists
if [ -f "$STATE_FILE" ]; then
    PREVIOUS_ERRORS=$(cat "$STATE_FILE" | sort | uniq | grep -v '^$' || true)
else
    PREVIOUS_ERRORS=""
fi
PREVIOUS_COUNT=$(echo "$PREVIOUS_ERRORS" | wc -l)

# Compute new errors: those in CURRENT_ERRORS but not in PREVIOUS_ERRORS
NEW_ERRORS=$(comm -23 <(echo "$CURRENT_ERRORS") <(echo "$PREVIOUS_ERRORS") | grep -v '^$' || true)
NEW_COUNT=$(echo "$NEW_ERRORS" | wc -l)

echo "Current erroring job count: $CURRENT_COUNT"
echo "Previous erroring job count: $PREVIOUS_COUNT"

if [ -n "$NEW_ERRORS" ]; then
    echo "🚨 NEW CRITICAL ERRORS DETECTED SINCE LAST SYNC:"
    echo "$NEW_ERRORS" | while read jobid; do
        JOB_NAME=$(sqlite3 "$DB_PATH" "SELECT job_name FROM cron_jobs WHERE job_id='$jobid';")
        echo "  - $jobid ($JOB_NAME)"
    done
else
    echo "✅ No new critical errors since last sync."
fi

# Update state file with current errors
echo "$CURRENT_ERRORS" > "$STATE_FILE"