# Fleet Analytics Sync Process

## What the Sync Does
The `fleet_analytics.py` script performs the following steps:

1. **Sync Cron Jobs**
   - Reads cron job definitions from OpenClaw's cron system
   - Updates the `cron_jobs` table in `agents.db`
   - Tracks status: enabled, error, disabled

2. **Sync Session Data**
   - Attempts to sync the operator agent sessions (if available)
   - Updates session-related tables
   - Logs error if the operator agent sessions database missing

3. **Sync Journal Compliance**
   - Scans agent journals for today's entries
   - Updates `journal_entries` table
   - Calculates compliance percentage

4. **Run Analytics Collection Pipeline**
   - Aggregates data for analytics tables
   - Updates `daily_productivity`, `task_analytics`, etc.

5. **Take Fleet Health Snapshot**
   - Records daily snapshot in `fleet_health_snapshots`
   - Includes agent counts, cron status, error rates, journal compliance

## Output Interpretation
The script prints progress with emojis:
- ⚡: Step in progress
- ✓: Step completed successfully
- ✗: Step encountered an error (may be non-fatal)

Final output shows:
- Totals in database (task_analytics, daily_productivity, session_analytics)
- Fleet health snapshot summary

## Database Location
All data is stored in:
`~/.sibling-agent/workspace/intel/agents/database/agents.db`

The `fleet_analytics.db` file is legacy and not used.