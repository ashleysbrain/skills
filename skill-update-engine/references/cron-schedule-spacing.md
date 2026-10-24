# Cron Schedule Spacing

Purpose: keep the update engine and adjacent fleet jobs from colliding on the same minute, especially when multiple cron jobs share the same hourly or 8-hour cadence.

## Spacing rules
- Prefer staggering critical jobs by at least 10 minutes when they run in the same cadence band.
- Avoid same-minute overlaps for jobs that write to shared state, emit reports, or trigger downstream reviews.
- When a new review job is added, check its minute offset against:
  - fleet sync jobs
  - remediation jobs
  - scoring/review jobs
  - health/report generation jobs
- If two jobs must share a cadence, offset them by minute rather than shifting the hour when possible.
- Keep the daily system-review job offset from upstream collection jobs so it runs after new evidence has landed.

## Quick verification
- Compare `next_run_at` timestamps for all enabled jobs in the same window.
- Look for identical minutes across jobs with the same cadence family.
- If a collision exists, shift one job by 10–20 minutes and re-check the next run times.

## Good default pattern
- collection jobs first
- sync / remediation jobs second
- review / scoring jobs third
- human-facing summary jobs last

## Notes
- This is a spacing rule, not a hard safety boundary.
- The exact offset can change; the principle is to avoid accidental contention and give downstream jobs clean inputs.