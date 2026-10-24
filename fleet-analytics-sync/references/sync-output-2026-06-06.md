# Fleet Analytics Sync Output - 2026-06-06

```
FLEET ANALYTICS SYNC — 2026-06-06T11:16:50.603746
============================================================
⚡ Syncing cron jobs from OpenClaw...
  ✗ Failed to query sibling-agent: Expecting value: line 1 column 1 (char 0)
⚡ Syncing session data...
  ✗ the operator agent sessions error: no such table: sessions
  ✓ Synced 51 agent knowledge stores
⚡ Syncing journal compliance...
  ✓ Indexed 1710 journal entries from 236 agent dirs
⚡ Running analytics collection pipeline...
  ✅ Collection complete for 2026-06-06
  
  ============================================================
  TOTALS IN DATABASE:
    task_analytics: 0 rows
    daily_productivity: 3 rows
    session_analytics: 0 rows
  ============================================================
⚡ Taking fleet health snapshot...
  ✓ Snapshot saved for 2026-06-06
    Agents: 72 active / 76 total
    Cron: 0 enabled, 0 erroring, 0 disabled
    Errors (24h): 0 total, 0 rate limit, 0 timeout
    Sessions (24h): 51
    Journal compliance: 0.0%
============================================================
✓ Full sync complete
```