#!/bin/bash
# VERITAS-ALGO Liveness Check
# Use BEFORE running any audit to verify the watchdog is alive.
# If staleness >48h, flag as MATERIAL ISSUE in audit verdict.
#
# Usage: ./references/veritas-algo-liveness-check.sh
#
# Exit codes: 0=alive (<48h), 1=stale (>=48h), 2=log file not found

LOG_FILE="/<workspace>"
STALENESS_HOURS=48

if [ ! -f "$LOG_FILE" ]; then
    echo "ERROR: Integrity log not found at $LOG_FILE"
    exit 2
fi

# Extract the latest report date (pattern: "VERITAS-ALGO INTEGRITY REPORT — YYYY-MM-DD")
LATEST_REPORT=$(grep -m 1 "VERITAS-ALGO INTEGRITY REPORT —" "$LOG_FILE" | sed -E 's/.*VERITAS-ALGO INTEGRITY REPORT — ([0-9]{4}-[0-9]{2}-[0-9]{2}).*/\1/')

if [ -z "$LATEST_REPORT" ]; then
    echo "ERROR: No VERITAS-ALGO reports found in log"
    exit 2
fi

# Calculate hours since last report
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LAST_REPORT_EPOCH=$(date -j -f "%Y-%m-%d" "$LATEST_REPORT" +%s)
    CURRENT_EPOCH=$(date +%s)
    HOURS_SINCE=$(( (CURRENT_EPOCH - LAST_REPORT_EPOCH) / 3600 ))
else
    # Linux (date command syntax differs)
    LAST_REPORT_EPOCH=$(date -d "$LATEST_REPORT" +%s)
    CURRENT_EPOCH=$(date +%s)
    HOURS_SINCE=$(( (CURRENT_EPOCH - LAST_REPORT_EPOCH) / 3600 ))
fi

echo "VERITAS-ALGO liveness check:"
echo "  Latest report: $LATEST_REPORT"
echo "  Hours stale:   $HOURS_SINCE"
echo "  Threshold:     $STALENESS_HOURS hours"

if [ $HOURS_SINCE -ge $STALENESS_HOURS ]; then
    echo "STATUS: ❌ WATCHDOG DEAD — staleness >= $STALENESS_HOURS hours"
    echo "ACTION:  Escalate as MATERIAL ISSUE — immediate restart required"
    exit 1
else
    echo "STATUS: ✅ WATCHDOG ALIVE — staleness < $STALENESS_HOURS hours"
    exit 0
fi