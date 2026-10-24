# Sample Fleet Analytics Sync Output

This is a representative sample of the output from running `python3 fleet_analytics.py sync`. Note that deprecation warnings about `datetime.utcnow()` may appear but do not affect functionality.

```
============================================================
FLEET ANALYTICS SYNC — 2026-06-02T11:02:34.475695
============================================================
⚡ Syncing cron jobs from OpenClaw...
  ✓ Synced 0 cron jobs
⚡ Syncing session data...
  ✗ the operator agent sessions error: no such table: sessions
  ✓ Synced 51 agent knowledge stores
⚡ Syncing journal compliance...
  ✓ Indexed 1708 journal entries from 236 agent dirs
⚡ Running analytics collection pipeline...
  ✅ Collection complete for 2026-06-02
  
  ============================================================
  TOTALS IN DATABASE:
    task_analytics: 14007 rows
    daily_productivity: 14 rows
    session_analytics: 714 rows
  ============================================================
⚡ Taking fleet health snapshot...
  ✓ Snapshot saved for 2026-06-02
    Agents: 257 active / 257 total
    Cron: 124 enabled, 44 erroring, 268 disabled
    Errors (24h): 0 total, 0 rate limit, 0 timeout
    Sessions (24h): 51
    Journal compliance: 0.0%
============================================================
✓ Full sync complete
```

Key sections:
- **Sync progress**: Shows each phase (cron jobs, session data, journal compliance, analytics collection).
- **Totals in database**: Current row counts in core analytics tables.
- **Fleet health snapshot**: Current status of agents, cron jobs, errors, sessions, and journal compliance.