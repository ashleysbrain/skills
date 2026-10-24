---
name: sibling-agent-fleet-analytics-sync
description: Sync live cron job and agent data from OpenClaw into the the operator agent analytics database.
category: sibling-agent
---

# OpenClaw Fleet Analytics Sync

Sync live cron job and agent data from OpenClaw into the the operator agent analytics database.

## When to Use
- Run this skill to refresh the analytics database with current OpenClaw state.
- Useful before generating reports, health snapshots, or debugging cron errors.

## Steps
1. Ensure you have access to the OpenClaw CLI (`sibling-agent`) and the the operator agent analytics database.
2. Execute the fleet analytics sync script:
   ```bash
   python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync
   ```
3. Verify the script completed successfully (exit code 0) and look for the summary output.
4. Optionally, run a report to see the updated stats:
   ```bash
   python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py report
   ```

## Expected Output
The sync script prints sections:
- `⚡ Syncing cron jobs from OpenClaw...` with a count of synced jobs.
- `⚡ Syncing session data...` (may show an error if the sessions table missing; this is non‑fatal).
- `⚡ Syncing journal compliance...`
- `⚡ Running analytics collection pipeline...`
- `⚡ Taking fleet health snapshot...` with a snapshot of agents, cron status, errors, sessions, and journal compliance.

## Verification
After sync, you can check the database directly:
```bash
# Count cron jobs by status
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT status, COUNT(*) as cnt FROM cron_jobs GROUP BY status;"

# Journal compliance for today
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT COUNT(DISTINCT agent_id) FROM journal_entries WHERE entry_date = DATE('now');"

# Latest health snapshot
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT snapshot_date, erroring_agents, journal_compliance_pct FROM fleet_health_snapshots ORDER BY snapshot_date DESC LIMIT 1;"
```

Optionally, run the fleet analytics report to see a formatted summary:
```bash
python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py report
```

Also, note that if the analytics collection pipeline shows zero rows for task_analytics or session_analytics, the collect-analytics script may have encountered an error; check its output for details.

## Pitfalls
- The `sibling-agent cron list --json` command may return empty or invalid JSON if the OpenClaw gateway is not running or there is a communication issue. Verify that the OpenClaw gateway is active and that you can run `sibling-agent cron list --json` manually to see the output.
- The sessions table may be missing in some environments, causing a `no such table: sessions` error. This does not halt the sync; session data will simply be omitted.
- Ensure the script is executable and the Python environment has any required dependencies (usually none beyond stdlib).
- If the OpenClaw CLI is not in PATH, use the full path or ensure `~/.sibling-agent` is in your PATH.
- The analytics collection step (`collect-analytics.py`) may fail silently, resulting in zero rows in `task_analytics`, `daily_productivity`, or `session_analytics`. Check the script's output for any error messages; it may require additional dependencies or have path issues.
- The script may emit `DeprecationWarning` messages about `datetime.utcnow()`; these are non-fatal and do not affect sync success.

## Related Skills
- `sibling-agent-fleet-analytics-report` – generate a full report after sync.
- `sibling-agent-fleet-analytics-health` – capture a health snapshot.
- `sibling-agent-fleet-analytics-errors` – analyze errors across the fleet.
