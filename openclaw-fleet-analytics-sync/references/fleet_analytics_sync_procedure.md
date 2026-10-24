# Fleet Analytics Sync Procedure

## Purpose
Sync live data from OpenClaw into the analytics database and generate a fleet health summary.

## Command
```bash
python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync
```

## Expected Output
The script prints a structured summary including:
- Number of cron jobs synced
- Status distribution (enabled/error/disabled)
- Top errors (by consecutive errors)
- Model distribution
- Journal compliance percentage
- Additional snapshot metrics (agents active/total, errors 24h, sessions 24h)

## Key Fields to Report
- **Cron jobs synced**: from "Synced X cron jobs"
- **Status distribution**: 
  - Enabled: count of jobs with `enabled=1`
  - Erroring: subset of enabled with `consecutiveErrors > 0`
  - Disabled: jobs with `enabled=0`
- **Top 5 errors**: list of job names with highest `consecutive_errors`
- **Model distribution**: counts per model from `cron_jobs.model`
- **Journal compliance**: percentage from health snapshot (or 0.0% if none)
- **Additional metrics**: agents active/total, errors (24h), sessions (24h) from the health snapshot

## Pitfalls
- The script may fail if the the operator agent sessions table is missing (prints "the operator agent sessions error: no such table: sessions") – this does not stop the sync.
- Ensure the OpenClaw CLI (`sibling-agent`) is available in PATH; the script uses it internally for some queries but the main sync uses direct database reads.
- The analytics database path is hardcoded to `~/.sibling-agent/workspace/intel/agents/database/agents.db`.
- If the script exits with non-zero, check for missing dependencies or database lock.

## Verification
After sync, you can verify by querying the database:
```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT status, COUNT(*) FROM cron_jobs GROUP BY status;"
```