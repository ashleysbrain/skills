# Session Learnings: 2026-06-05

## Fleet Analytics Sync Summary
- **Sync Command**: `python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync`
- **Sync Output Highlights**:
  - Synced 0 cron jobs (live API returned empty)
  - Synced 51 agent knowledge stores
  - Indexed 1709 journal entries from 236 agent dirs
  - Analytics collection pipeline completed successfully
  - Fleet health snapshot: 72 active / 76 total agents
  - Cron status: 0 enabled, 0 erroring, 0 disabled
  - Errors (24h): 0 total, 0 rate limit, 0 timeout
  - Sessions (24h): 51
  - Reported journal compliance: 0.0% (known calculation bug)

## Key Findings & Queries

### 1. Cron Jobs Table Empty
- **Query**: `SELECT COUNT(*) FROM cron_jobs;` → 0 rows
- **Verification**: Confirmed via direct SQLite query after sync
- **Note**: Live `sibling-agent cron list --json` returned empty array, indicating gateway cron subsystem may be reset or empty. Static `jobs.json` file should be consulted for job definitions.

### 2. Model Usage Tracking
- **Agent Sessions Model Query**: 
  ```sql
  SELECT model_used, COUNT(*) FROM agent_sessions 
  WHERE model_used IS NOT NULL 
  GROUP BY model_used;
  ```
  → **Result**: Empty output (no rows with non-null model_used)
- **Alternative Approaches**:
  - **Cron Runs** (actual execution): 
    ```sql
    SELECT cj.model, COUNT(*) as cnt
    FROM cron_runs cr
    JOIN cron_jobs cj ON cr.cron_job_id = cj.id
    WHERE cr.started_at >= datetime('now', '-24 hours')
    GROUP BY cj.model
    ORDER BY cnt DESC;
    ```
  - **Task Analytics** (task-level usage):
    ```sql
    SELECT model_used, COUNT(*) as cnt
    FROM task_analytics
    WHERE started_at >= datetime('now', '-1 day')
    GROUP BY model_used
    ORDER BY cnt DESC
    LIMIT 15;
    ```

### 3. Journal Compliance Calculation
- **Snapshot Issue**: `fleet_health_snapshots.journal_compliance_pct` reports 0.0% due to calculation bug
- **Accurate Manual Query** (last 24h active agents):
  ```sql
  SELECT 
      COUNT(DISTINCT agent_id) as agents_with_journal,
      (SELECT COUNT(*) FROM agents) as total_agents,
      ROUND(100.0 * COUNT(DISTINCT agent_id) / (SELECT COUNT(*) FROM agents), 2) as compliance_pct
  FROM journal_entries
  WHERE DATE(created_at) = '2026-06-04';
  ```
  → **Result**: 21 agents with journal entries out of 76 total = **27.63% compliance**

### 4. Fleet Health Snapshot Verification
- **Latest Snapshot Query**:
  ```sql
  SELECT * 
  FROM fleet_health_snapshots 
  ORDER BY snapshot_date DESC, created_at DESC 
  LIMIT 1;
  ```
- **Fields to Verify**: total_errors, timeout_errors, rate_limit_errors, total_sessions, journal_compliance_pct

## Recommendations for Future Syncs

1. **When Cron Jobs Table is Empty**:
   - Verify live API: `sibling-agent cron list --json`
   - Consult static file: `~/.sibling-agent/cron/jobs.json` (handle both list and dict wrapper formats)
   - Use static file for job definitions and model distribution, but note state data (consecutive errors, last run) may be stale

2. **Model Usage Analysis**:
   - Prefer `cron_runs` table for actual cron execution model usage
   - Use `task_analytics` for task-level model usage
   - Do not rely on `agent_sessions.model_used` for usage statistics (frequently NULL)

3. **Journal Compliance Reporting**:
   - Always calculate manually using direct `journal_entries` queries
   - Use 7-day active agent compliance for trend analysis:
     ```sql
     SELECT 
         COUNT(DISTINCT CASE WHEN entry_date >= date('now', '-7 days') THEN agent_id END) * 100.0 / 
         COUNT(DISTINCT agent_id) as compliance_pct
     FROM journal_entries;
     ```

4. **Sync Verification Steps**:
   - After sync, verify: 
     ```bash
     # Check cron jobs count
     sqlite3 agents.db "SELECT COUNT(*) FROM cron_jobs;"
     
     # Check latest snapshot
     sqlite3 agents.db "SELECT snapshot_date, total_errors, active_agents FROM fleet_health_snapshots ORDER BY created_at DESC LIMIT 1;"
     
     # Check journal entries today
     sqlite3 agents.db "SELECT COUNT(DISTINCT agent_id) FROM journal_entries WHERE DATE(created_at) = '$(date +%Y-%m-%d)';"
     ```

## Session-Specific Notes
- **Deprecation Warnings**: Multiple `datetime.datetime.utcnow()` deprecation warnings in sync output - non-functional but should be fixed in script
- **the operator agent Sessions Error**: Expected `✗ the operator agent sessions error: no such table: sessions` - sync continues successfully
- **Analytics Pipeline**: Collection completed successfully indicating schema fixes from 2026-06-04 are effective
- **Error Log**: Contains 7 `talent-review-insight` entries from today's talent review process (review the `error_log` table for structured fleet insights)