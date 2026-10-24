# Fleet Analytics Sync Output - 2026-06-10

```
FLEET ANALYTICS SYNC — 2026-06-10T17:02:09.798031
============================================================
⚡ Syncing cron jobs from OpenClaw...
  ✗ Failed to query sibling-agent: Expecting value: line 1 column 1 (char 0)
⚡ Syncing session data...
  ✗ the operator agent sessions error: no such table: sessions
  ✓ Synced 51 agent knowledge stores
⚡ Syncing journal compliance...
  ✓ Indexed 1710 journal entries from 236 agent dirs
⚡ Running analytics collection pipeline...
  ✅ Collection complete for 2026-06-10
  
  ============================================================
  TOTALS IN DATABASE:
    task_analytics: 0 rows
    daily_productivity: 7 rows
    session_analytics: 0 rows
  ============================================================
⚡ Taking fleet health snapshot...
  ✓ Snapshot saved for 2026-06-10
    Agents: 80 active / 84 total
    Cron: 124 enabled, 66 erroring, 183 disabled
    Errors (24h): 117 total, 0 rate limit, 17 timeout
    Sessions (24h): 51
    Journal compliance: 1.2%
============================================================
✓ Full sync complete
```