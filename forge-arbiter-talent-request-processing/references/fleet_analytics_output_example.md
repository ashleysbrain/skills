# Example Fleet Analytics Sync Output

============================================================
FLEET ANALYTICS SYNC — 2026-06-09T09:13:51.290180
============================================================
⚡ Syncing cron jobs from OpenClaw...
  ✓ Synced 124 cron jobs
⚡ Syncing session data...
  ✗ the operator agent sessions error: no such table: sessions
  ✓ Synced 51 agent knowledge stores
⚡ Syncing journal compliance...
  ✓ Indexed 1710 journal entries from 236 agent dirs
⚡ Running analytics collection pipeline...
  ✅ Collection complete for 2026-06-09

  ============================================================
  TOTALS IN DATABASE:
    task_analytics: 0 rows
    daily_productivity: 6 rows
    session_analytics: 0 rows
  ============================================================
⚡ Taking fleet health snapshot...
  ✓ Snapshot saved for 2026-06-09
    Agents: 80 active / 84 total
    Cron: 124 enabled, 100 erroring, 183 disabled
    Errors (24h): 267 total, 0 rate limit, 26 timeout
    Sessions (24h): 51
    Journal compliance: 0.0%
============================================================
✓ Full sync complete