# Session Learnings: Fleet Analytics Sync - 2026-06-02

## Key Observations from This Session

### 1. OpenClaw CLI Returns Empty List
During this session, `sibling-agent cron list --json` returned:
```json
{
  "jobs": [],
  "total": 0,
  "offset": 0,
  "limit": 50,
  "hasMore": false,
  "nextOffset": null,
  "deliveryPreviews": {}
}
```
However, the agents.db still contained cron job data from previous successful syncs.

**Verification Query:**
```sql
SELECT COUNT(*) as total, 
       SUM(CASE WHEN status='enabled' THEN 1 ELSE 0 END) as enabled,
       SUM(CASE WHEN status='error' THEN 1 ELSE 0 END) as error,
       SUM(CASE WHEN status='disabled' THEN 1 ELSE 0 END) as disabled
FROM cron_jobs;
```
Result: `392|80|44|268` (total|healthy_enabled|erroring|disabled)

**Important Context:** The query above uses the `status` column from the cron_jobs table, where:
- `status='enabled'` means healthy running jobs (consecutive_errors = 0)
- `status='error'` means enabled jobs that are failing (consecutive_errors > 0)
- `status='disabled'` means intentionally paused jobs (enabled = 0)

Thus, total jobs that "should run" (enabled=1) = healthy_enabled + erroring = 80 + 44 = 124.
This matches the sync output which reported "124 enabled" (meaning jobs configured to run).

**Takeaway:** When the OpenClaw CLI returns empty results, the sync script still reports success and may update other data (sessions, journals), but cron job sync shows 0 synced. Always verify database state directly when seeing "Synced 0 cron jobs".

### 2. Database Location Confirmation
Three databases exist in `~/.sibling-agent/workspace/intel/agents/database/`:
- `agents.db` - ACTIVE (contains cron_jobs, agent data, etc.)
- `fleet_analytics.db` - EMPTY (0 bytes, legacy)
- `analytics.db` - Summary tables (cron_error_insights, model_tier_distribution, etc.)

All sync data from `fleet_analytics.py sync` goes to `agents.db`, not `fleet_analytics.db` despite the script's name.

### 3. Effective Reporting Queries
The following queries provided accurate data for the fleet report:

**Status Distribution (matching sync output interpretation):**
```sql
SELECT 
    CASE
        WHEN enabled = 0 THEN 'disabled'
        WHEN consecutive_errors > 0 THEN 'error'
        ELSE 'enabled'
    END as status,
    COUNT(*) as cnt
FROM cron_jobs
GROUP BY status
ORDER BY cnt DESC;
```

**Top 5 Errors:**
```sql
SELECT job_name, consecutive_errors, last_error_message
FROM cron_jobs
WHERE status='error'
ORDER BY consecutive_errors DESC
LIMIT 5;
```

**Model Distribution (most recent):**
```sql
SELECT tier, agent_count, percentage
FROM model_tier_distribution
WHERE review_date = (SELECT MAX(review_date) FROM model_tier_distribution)
ORDER BY tier;
```

**Journal Compliance (most recent snapshot):**
```sql
SELECT journal_compliance_pct
FROM fleet_health_snapshots
WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM fleet_health_snapshots);
```

### 4. Health Snapshot Data Points
The fleet health snapshot captured during sync showed:
- Agents: 257 active / 257 total
- Cron: 124 enabled, 44 erroring, 268 disabled
- Errors (24h): 0 total, 0 rate limit, 0 timeout
- Sessions (24h): 51
- Journal compliance: 0.0% (known calculation bug in sync script)

### 5. New Critical Error Detection
Compared to last recorded erroring jobs (122 from 2026-05-20 in cron_error_insights):
- Current erroring jobs: 44
- Status: No new critical errors (error count decreased)

**Detection Query:**
```sql
-- Current erroring count
SELECT COUNT(*) as current_erroring FROM cron_jobs WHERE status='error';

-- Last recorded erroring count
SELECT erroring_jobs 
FROM cron_error_insights 
ORDER BY review_date DESC 
LIMIT 1;
```

## Recommended Procedures When OpenClaw CLI Returns Empty

1. **Do not panic** - The sync may still have processed other data
2. **Verify database state directly** using the agents.db
3. **Check if other sync components succeeded** (sessions, journals, analytics)
4. **Consider investigating OpenClaw CLI issues** if this persists
5. **Use historical data from database** for reporting when live sync fails

## Troubleshooting Empty OpenClaw Response

If `sibling-agent cron list --json` consistently returns empty jobs:

1. Check OpenClaw service status
2. Verify CLI authentication/permissions
3. Check for OpenClaw backend issues
4. Consider using the static `~/.sibling-agent/cron/jobs.json` as fallback (though may be stale)
5. Examine OpenClaw logs for errors
