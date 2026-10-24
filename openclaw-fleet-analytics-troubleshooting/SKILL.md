---
name: sibling-agent-fleet-analytics-troubleshooting
description: Troubleshooting guide for OpenClaw fleet analytics sync issues
category: devops
---
## OpenClaw Fleet Analytics Troubleshooting Guide

This skill provides procedures for diagnosing and resolving issues with the OpenClaw fleet analytics synchronization engine.

### AI Organism Engine Fleet Diagnostics

When troubleshooting fleet analytics issues, remember that the OpenClaw system depends on an underlying AI organism (engine fleet) that must be healthy for proper operation. Fleet analytics problems often stem from engine-level issues rather than analytics configuration.

#### Engine Fleet Health Check Procedure
1. **List all expected engines**: Refer to organism specification for required engines
2. **Check running status**: `ps aux | grep -i 'engine\|server\|uvicorn' | grep -v grep`
3. **Verify port bindings**: Scan expected port ranges for listeners
4. **Test health endpoints**: Query `/health` or root endpoints on each engine port
5. **Check source integrity**: Verify engine source directories are complete and uncorrupted
6. **Look for resource exhaustion**: Check CPU, memory, disk usage on host

#### Common Engine Fleet Issues Affecting Analytics
- **Port conflicts preventing engine startup**:
  - Symptom: Analytics show missing data from specific body systems
  - Diagnosis: `lsof -i :<expected_port>` shows wrong process or conflict
  - Resolution: Identify conflicting processes, reassign engines to free ports
- **Engine import/path errors**:
  - Symptom: Engine process starts then immediately exits
  - Diagnosis: Check engine logs for ModuleNotFoundError or ImportError
  - Resolution: Fix import paths in run_server.py (e.g., correct module references)
- **Stale processes holding ports**:
  - Symptom: New engine instances fail to bind to expected ports
  - Diagnosis: `lsof -i :<port>` shows old PID that should be dead
  - Resolution: Kill stale processes with `kill <PID>` before restart
- **Partial engine fleet operation**:
  - Symptom: Analytics show data from some body systems but not others
  - Diagnosis: Mix of running and dead engines in process list
  - Resolution: Identify missing engines and address their specific startup issues

#### Workflow Integration with Agent Operations
When performing fleet analytics troubleshooting:
1. Always begin with organism-level health checks before diving into analytics configuration
2. Correlate analytics gaps with specific engine downtime
3. Document both engine fixes and analytics configuration changes
4. Verify that resolving engine issues closes the analytics gaps
5. Remember that the agent's effectiveness depends on the health of its entire operational environment

This holistic approach prevents treating symptoms while the underlying organism remains impaired.
When running the fleet analytics sync script (`fleet_analytics.py sync`), you may encounter empty tables in the analytics database (`analytics.db`). This skill provides troubleshooting steps to locate the actual data in the agents database (`agents.db`).

## Trigger Conditions
- The fleet analytics sync script reports 0 rows in tables like `task_analytics`, `daily_productivity`, or `session_analytics`.
- You need to verify cron job status, error distribution, model usage, or journal compliance.
- The `fleet_health_snapshots` table in `analytics.db` appears empty or missing recent data.

## Steps
1. **Verify which database contains the data**
   - The sync script writes to multiple databases:
     - `~/.sibling-agent/workspace/intel/agents/database/analytics.db` (for aggregated analytics)
     - `~/.sibling-agent/workspace/intel/agents/database/agents.db` (for raw agent and cron data)
   - If `analytics.db` shows empty tables, check `agents.db` for the source data.

2. **Check agents.db for cron job status**
   ```sql
   -- Status distribution (enabled/error/disabled)
   SELECT status, COUNT(*) as count 
   FROM cron_jobs 
   GROUP BY status;
   
   -- Total cron jobs synced
   SELECT COUNT(*) FROM cron_jobs;
   ```

3. **Check fleet health snapshot**
   ```sql
   -- Most recent fleet health snapshot
   SELECT snapshot_date, total_agents, active_agents, erroring_agents, disabled_agents, 
          total_errors, rate_limit_errors, timeout_errors, total_sessions, journal_compliance_pct
   FROM fleet_health_snapshots
   ORDER BY snapshot_date DESC
   LIMIT 1;
   ```

4. **Check for recent errors (last 24 hours)**
   ```sql
   -- Top 5 error types in the last day
   SELECT error_type, COUNT(*) as count 
   FROM error_log 
   WHERE occurred_at >= datetime('now', '-1 day')
   GROUP BY error_type 
   ORDER BY count DESC
   LIMIT 5;
   
   -- Total errors in last 24 hours
   SELECT COUNT(*) FROM error_log 
   WHERE occurred_at >= datetime('now', '-1 day');
   ```

5. **Check model distribution (if needed)**
   ```sql
   -- Model usage distribution (from cron_jobs)
   SELECT model, COUNT(*) as count 
   FROM cron_jobs 
   WHERE model IS NOT NULL
   GROUP BY model 
   ORDER BY count DESC;
   ```

6. **Check journal compliance**
   ```sql
   -- Journal compliance percentage from latest snapshot
   SELECT journal_compliance_pct
   FROM fleet_health_snapshots
   ORDER BY snapshot_date DESC
   LIMIT 1;
   ```

## Notes
- The `fleet_analytics.py sync` script may populate `analytics.db` with aggregated data over time, but real-time operational data is often immediately available in `agents.db`.
- If you encounter the error "no such table: sessions" during sync, it indicates the sessions table hasn't been created yet in the target database—this is normal early in the sync process; the agents.db will still contain the agent and cron data.
- Always verify the timestamp of the data you're checking to ensure it's recent enough for your needs.\n- When analyzing erroring cron jobs, check for NULL agent_id and persona_id in the cron_jobs table, as this indicates the job is not linked to any specific agent or persona and may point to a configuration issue in the OpenClaw gateway or sync process.

## Related Skills
- `sibling-agent-fleet-analytics-sync` - For running the synchronization process
- `agents-db-query` - For general agent database queries