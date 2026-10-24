---
name: sibling-agent-fleet-analytics-summary
description: Extract and summarize key fleet analytics data from OpenClaw's analytics database after running a sync operation
trigger:
  - Need to report fleet health status after running fleet_analytics.py sync
  - Regular monitoring of OpenClaw fleet analytics data
  - Identifying new critical errors in cron job executions
applies_to:
  - OpenClaw fleet administrators
  - System health monitoring
  - Cron job oversight
---

# OpenClaw Fleet Analytics Summary Skill

## Purpose
Extract and summarize key fleet analytics data from OpenClaw's analytics database after running a sync operation. Provides consistent reporting on cron job status, error trends, model distribution, and journal compliance.

## When to Use
- After running `fleet_analytics.py sync` to get current fleet status
- For regular fleet health monitoring and reporting
- When needing to identify new critical errors since last sync
- For preparing fleet health summaries for stakeholders

## Prerequisites
- OpenClaw installation at `~/.sibling-agent`
- Fleet analytics database at `~/.sibling-agent/workspace/intel/agents/database/agents.db`
- Basic SQL query knowledge

## Steps

### 1. Run Fleet Analytics Sync + Report (single command)

For automated/scheduled reports, use the `report` command which runs sync internally:

```bash
python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py report
```

This outputs: agents, personas, cron status, top 10 errors, model distribution, sessions, journal compliance, health snapshot, task analytics, and a 3-day daily productivity trend.

**If you already ran `sync` separately**, skip re-running and query the database directly for specific sections.

### 2. For Day-Over-Day Error Comparison

The `report` command does NOT include error deltas. Use one of these methods:

**Method A: `last_error_count.txt` (fastest)**
```bash
cat ~/.sibling-agent/workspace/intel/agents/database/last_error_count.txt
# Compare with current erroring job count from report output
```

**Method B: Fleet health snapshots**
```sql
SELECT snapshot_date, total_errors, created_at
FROM fleet_health_snapshots
ORDER BY created_at DESC LIMIT 5;
```

### 3. Extract Specific Sections (if needed)

Connect to agents.db for targeted queries:

```sql
-- Status distribution (computed from enabled + consecutive_errors)
SELECT
    CASE
        WHEN enabled = 0 THEN 'disabled'
        WHEN consecutive_errors > 0 THEN 'error'
        ELSE 'enabled'
    END as status,
    COUNT(*) as count
FROM cron_jobs
GROUP BY status;

-- Top 5 errors
SELECT job_name, consecutive_errors, last_error_message
FROM cron_jobs
WHERE consecutive_errors > 0
ORDER BY consecutive_errors DESC
LIMIT 5;

-- Model distribution
SELECT model, COUNT(*) as cnt
FROM cron_jobs WHERE model IS NOT NULL AND model != ''
GROUP BY model ORDER BY cnt DESC;
```

### 4. Format Summary Report
Structure output as:
```
## OpenClaw Fleet Analytics Sync Report
**[DATE TIME UTC]**

### Sync Summary
| Item | Result |
|---|---|
| Cron jobs synced | [count] |
| Agent knowledge stores | [count] |
| Journal entries indexed | [count] |
| Sessions (24h) | [count] |
| Task analytics rows | [count] |
| Fleet TWC score | [score] |

### Cron Job Status Distribution
| Status | Count |
|---|---|
| Enabled | [count] |
| Error | [count] |
| Disabled | [count] |

### Top 5 Errors (by consecutive failures)
[table]

### Model Distribution (across cron jobs)
[table]

### Daily Productivity Trend
[table with last 3 days: completed, failed, sessions, commits, active agents]

### Journal Compliance
[percentage]% — [count] agents journaled today

### Critical Flags
[Any new critical errors, systemic issues, or significant changes]
```

## Verification
- Confirm sync script completed without fatal errors
- Verify database queries return expected data types
- Check that status counts add up to total cron jobs
- Validate percentages are within 0-100 range

## Troubleshooting
- **"no such table: sessions" error**: This is expected - the operator agent session table may not exist. Sync continues successfully.
- **Empty results from fleet_analytics.db**: This DB is 0 bytes. Always query `analytics.db` or `agents.db` instead.
- **analytics.db can also be fully empty**: Even after successful sync, all 13 tables in `analytics.db` may have 0 rows (schema exists but no data persisted). When this happens, use three fallback sources: (1) sync script stdout, (2) `cron_jobs.json` raw dump (`data['jobs']` array), (3) `last_error_count.txt` + `cron_errors_previous.json` for trends.
- **cron_jobs.json is a list-of-dicts API response**: Structure is `{"jobs": [...], "total": N, ...}`. Access jobs via `data['jobs']`, not `data.values()`. Each job's error state is at `job['state']['consecutiveErrors']` and model at `job['payload']['model']`.
- **cron_errors_previous.json is a list, not a dict**: Parse with `prev_map = {e['name']: e['consecutiveErrors'] for e in prev_errors}`.
- **Permission errors**: Verify read access to ~/.sibling-agent/workspace/intel/agents/database/
- **No journal data**: Check that JOURNALS_PATH environment variable is set correctly
- **`diff-errors` subcommand doesn't exist**: Use `errors` command or compare snapshots from `fleet_health_snapshots` table
- **`report` re-runs sync**: If you already synced, the `report` command will re-sync (adds ~10-15s). For already-synced data, query agents.db directly.
- **`cron_errors_previous.json` has empty error messages**: This file is a flat list of `{job_id, last_error_message}` objects where error messages are often empty strings. Not useful for error comparison — use `last_error_count.txt` or `fleet_health_snapshots` instead.

## Skill Overlap Note

This skill overlaps significantly with `sibling-agent-fleet-analytics-sync`. The sync skill contains comprehensive reference material (DB schema, field mappings, query patterns, pitfalls). This skill focuses on the operational workflow: run sync → extract metrics → format report. For deep debugging or schema questions, prefer the sync skill.

## Output Example
See the actual sync output for formatting reference.

## Related Skills
- sibling-agent-fleet-coordination-journaling-push: For journal compliance specifics
- sibling-agent-fleet-analytics-sync: For alternative sync approaches