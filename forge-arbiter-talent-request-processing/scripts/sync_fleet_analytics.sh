#!/usr/bin/env bash
# sync_fleet_analytics.sh - Wrapper for fleet analytics sync with logging
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_FILE="$SCRIPT_DIR/database/fleet_analytics_sync_$(date +%Y%m%d_%H%M%S).log"

echo "=== Fleet Analytics Sync Started: $(date) ===" | tee -a "$LOG_FILE"
python3 "$SCRIPT_DIR/database/fleet_analytics.py" sync 2>&1 | tee -a "$LOG_FILE"
echo "=== Fleet Analytics Sync Finished: $(date) ===" | tee -a "$LOG_FILE"