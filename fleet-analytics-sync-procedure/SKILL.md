--- 
name: fleet-analytics-sync-procedure
description: Procedure for syncing OpenClaw fleet analytics data into the analytics database and reporting summary.
version: 1.0
domain: devops
---

# Fleet Analytics Sync Procedure

This skill outlines the steps to run the fleet analytics sync engine, verify the sync, and report key metrics including cron job counts, status distribution, model distribution, top errors, and journal compliance.

## When to Use

- Run as a scheduled cron job to keep fleet analytics up to date.
- On-demand when you need a fresh snapshot of fleet health.
- After making changes to cron jobs or agent configurations to verify impact.

## Steps

1. **Run the sync script**
   ```bash
   python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync
   ```
   This will:
   - Sync cron jobs from OpenClaw (`sibling-agent cron list --json`)
   - Sync the operator agent session data
   - Sync journal compliance
   - Run analytics collection pipeline
   - Take a fleet health snapshot

2. **Verify sync success**
   Check the output for:
   - `✓ Synced X cron jobs`
   - No critical errors in the sync steps (except expected the operator agent sessions error if table missing)
   - Final line: `✓ Full sync complete`

3. **Query the analytics database for summary**
   Use SQLite to extract the following from `~/.sibling-agent/workspace/intel/agents/database/agents.db` (main cron jobs table) and other tables as needed.

   ### Cron job counts and status
   ```sql
   SELECT status, COUNT(*) FROM cron_jobs GROUP BY status;
   ```
   Expected statuses: `enabled`, `error`, `disabled`.

   ### Model distribution (top 5)
   ```sql
   SELECT model, COUNT(*) as cnt 
   FROM cron_jobs 
   WHERE model != '' 
   GROUP BY model 
   ORDER BY cnt DESC 
   LIMIT 5;
   ```

   ### Top errors (by consecutive errors)
   ```sql
   SELECT job_name, consecutive_errors, last_error_message 
   FROM cron_jobs 
   WHERE consecutive_errors > 0 
   ORDER BY consecutive_errors DESC 
   LIMIT 5;
   ```

   ### Recent error types (last 24h)
   ```sql
   SELECT error_type, COUNT(*) as cnt 
   FROM cron_runs 
   WHERE status='error' 
     AND started_at > datetime('now', '-1 day') 
   GROUP BY error_type 
   ORDER BY cnt DESC;
   ```

   ### Journal compliance (today)
   ```sql
   -- Assuming journal_entries table exists with entry_date
   SELECT COUNT(DISTINCT agent_id) 
   FROM journal_entries 
   WHERE entry_date = date('now');
   ```
   Then compute percentage: `(journaled_today / active_agents) * 100`.

4. **Report the summary**
   Format as:
   ```
   FLEET ANALYTICS SYNC SUMMARY
   ============================
   Cron Jobs Synced: <number>
   Status Distribution:
     - Enabled: <count>
     - Erroring: <count>
     - Disabled: <count>
   Model Distribution (top 5):
     1. <model1>: <count>
     2. <model2>: <count>
     ...
   Top 5 Errors (by consecutive errors):
     1. <job_name>: <consecutive_errors> <error_type>
     ...
   Journal Compliance: <percentage>%
   Critical Errors: <note if any new critical errors appeared>
   ```

5. **Flag new critical errors**
   - Compare the current error list with the previous sync (if available).
   - Highlight any errors that have appeared or worsened since last sync.
   - In this session, all errors were timeout errors indicating connectivity issues with model providers.

## Pitfalls

- **Timeout errors dominating**: If most errors are `timeout`, investigate network connectivity to model providers (e.g., OpenRouter) and consider increasing `timeoutSeconds` in cron job payloads.
- **Database schema mismatches**: The sync script expects certain tables (e.g., `cron_jobs`, `agent_sessions`). If missing, run the sync script multiple times or check initialization scripts.
- **Journal compliance zero**: Ensure journal directories exist under `~/your-workspace/hydra-os/intel/agents/learning-journals` and that agent names match directory names.
- **the operator agent sessions error**: The error `no such table: sessions` in the operator agent sync is benign if you don't use the operator agent session storage; it does not affect cron job sync.

## Verification

After running the sync, verify that:
- The `cron_jobs` table contains entries matching the output of `sibling-agent cron list --json`.
- The `fleet_health_snapshots` table has a row for today.
- No unexpected errors appear in the script output (except the the operator agent sessions table note).

## Related Skills

- `sibling-agent-fleet-analytics-sync`: Lower-level sync invocation.
- `hermes-agent`: For configuring the operator agent Agent itself.
- `debug-voice-transcription-gateway`: If voice transcription issues arise.

---