# Fleet Analytics Sync Session — 2026-06-08

## Key Finding: Live API Now Returning Jobs

After weeks of "0 cron jobs synced", the OpenClaw CLI is now returning live job data:
- `sibling-agent cron list --json` returns 307 jobs
- Sync reports: `✓ Synced 124 cron jobs` (enabled+erroring), 183 disabled = 307 total
- cron_jobs table fully populated with model, status, and error data

This means model distribution queries now work against `cron_jobs.model` instead of falling back to `agents.primary_model`.

## New Query Pattern: Model + Status Breakdown

The most useful query for identifying provider-level issues:

```sql
SELECT
  model,
  COUNT(*) as job_count,
  SUM(CASE WHEN status = 'enabled' THEN 1 ELSE 0 END) as enabled,
  SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as erroring,
  SUM(CASE WHEN status = 'disabled' THEN 1 ELSE 0 END) as disabled
FROM cron_jobs
GROUP BY model
ORDER BY job_count DESC;
```

Result revealed: **72 of 79 qwen3-next-80b:free jobs are erroring** — likely degraded model on OpenRouter free tier.

## `models` Subcommand Is Useless

`python3 fleet_analytics.py models` just prints the help/usage text. It does NOT show model distribution. Always query `cron_jobs` table directly.

## Error Trend Analysis: Use Peak Per Day

Multiple snapshots per day make naive comparison misleading. The correct pattern:

```sql
SELECT snapshot_date, MAX(total_errors) as peak_errors
FROM fleet_health_snapshots
WHERE snapshot_date >= date('now', '-7 days')
GROUP BY snapshot_date
ORDER BY snapshot_date DESC;
```

Today's data showed errors climbing from 229→546 across same-day snapshots — the peak-per-day pattern correctly captures the real trend.

## Subcommand Pitfalls

- `report` re-syncs everything (~15s). After running `sync`, use direct DB queries instead.
- `models` prints help text, not data.
- `errors` works but shows different aggregation than DB queries.
- `health` also re-syncs before displaying.

## Current Fleet State (14:16 UTC)

| Metric | Value |
|--------|-------|
| Cron jobs synced | 307 |
| Enabled (healthy) | 30 |
| Erroring | 94 |
| Disabled | 183 |
| Active agents | 77/81 |
| Errors (24h) | 546 |
| Fleet TWC | 7.41 |
| Journal compliance | 0.0% (known bug) |
| Top erroring model | qwen3-next-80b:free (72/79 jobs erroring) |
