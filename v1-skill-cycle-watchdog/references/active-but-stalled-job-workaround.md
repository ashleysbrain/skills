# Active-But-Stalled Job (Mode 7) — Detection and Workaround

## Problem Description

The cron job shows as `[active]` in `hermes cron list` with a valid `Last run` timestamp, but the session directory contains no files newer than that timestamp. The job appears enabled and scheduled but is not actually executing.

**Critical distinction from other modes:**
- **Mode 1 (Job didn't run):** No output file for today — the job simply hasn't executed yet today
- **Mode 6 (Session persistence failure):** Job ran successfully (status: ok) but session output is unavailable
- **Mode 7 (Active-but-stalled):** Job stopped executing entirely — the `Last run` timestamp freezes and never updates

## Detection Protocol

### Step 1: Verify Job Status

```bash
# Check cron job status via the operator agent CLI
hermes cron list | grep "c37a1090869d"
```

Expected output for an active-but-stalled job:
```
c37a1090869d [active]
```

The job shows as `[active]`, but this does NOT guarantee it's actually running.

### Step 2: Verify Session Directory

```bash
# Check the most recent session files
ls <agent-home>/sessions/ | grep "cron_c37a1090869d" | sort | tail -5
```

**Analysis:**
- If the most recent file is from days or weeks ago (e.g., `20260705` but today is `20260720`), the job is stalled
- The `Last run` timestamp from `hermes cron list` will show the last successful execution date
- The `Next run` timestamp may still show a future scheduled time, but it never executes

### Step 3: Confirm Stall Duration

```bash
# Find all session files for this job
find <agent-home>/sessions -name "*c37a1090869d*" -type f -printf "%T@ %p\n" | sort -n | tail -10
```

This shows the actual file timestamps, confirming whether any sessions have been created recently.

## Root Cause Hypotheses

1. **Cron daemon stopped:** The system's cron daemon (or the operator agent cron equivalent) is not running
2. **Schedule lost:** The job's schedule was corrupted or lost from the cron configuration
3. **Silent error loop:** The job starts but errors silently before creating a session
4. **Configuration mismatch:** Job configuration changed but the old process is still running as a zombie
5. **the operator agent cron system failure:** The the operator agent cron subsystem itself is not processing the job queue

## Corrective Actions

### Immediate: Manual Re-Run

```bash
# Manually trigger an immediate run
hermes cron run c37a1090869d
```

This forces the job to execute immediately and generates a new session file.

### Investigation: Check Cron Daemon Status

```bash
# Check if the operator agent cron system is running
hermes cron status

# Or check system cron (if applicable)
ps aux | grep cron
```

### Investigation: Verify Schedule Configuration

```bash
# Check the job's schedule is still valid
hermes cron list | grep -A 5 "c37a1090869d"
```

Look for the `schedule` field and confirm it matches the expected `25 3 * * *`.

### Investigation: Check for Silent Errors

After manual re-run, check the session for any error messages that explain why the job stopped:

```bash
# Find the most recent session file
latest_session=$(ls -t <agent-home>/sessions/cron_c37a1090869d_*.json 2>/dev/null | head -1)

# Check for error messages in the session
grep -i "error\|exception\|failed" "$latest_session"
```

## Gap Calculation

When reporting an active-but-stalled job, calculate the cumulative gap:

```
days_stalled = (current_date - last_successful_run_date)
cumulative_new_skills_gap = days_stalled × 3
cumulative_updates_gap = days_stalled × 5
```

Report both the daily gap (if any) and the cumulative gap for context.

**Example alert:**

```markdown
⚠️ **V1 Skill Product Review — Critical Gap (July 20, 2026)**

**Job:** `c37a1090869d` (Divinity Health V1 Skill Product Review)

**Status:** **STALLED — Not run for 25 days**  
Last successful run: **June 25, 2026 at 03:28 AM**  
Today: **July 20, 2026** — job has not executed

**Gap vs. standing targets:**
| Metric | Target | Actual (today) | Cumulative Gap (25 days) |
|--------|--------|----------------|---------------------------|
| New skill recommendations | 3/day | 0 | **75 missing** |
| Total updates | 5/day | 0 | **125 missing** |

**Next corrective action:** Manually trigger an immediate run:

```bash
hermes cron run c37a1090869d
```

Then verify the job is still enabled on its `25 3 * * *` schedule and investigate why it stopped firing.
```

## Prevention

### Scheduled Watchdog Detection

The v1-skill-cycle-watchdog should run daily (scheduled 1–2 hours after the review job) and check for active-but-stalled conditions:

1. Verify job is `[active]` via `hermes cron list`
2. Check session directory for recent files
3. Calculate days since last session file
4. Alert if stalled for 3+ days (not 1 day to avoid false positives)

### Monitoring Dashboard

Consider adding a visual indicator to fleet monitoring dashboards:
- Green: Job running daily with new session files
- Yellow: Job ran within last 48 hours (investigate)
- Red: No session files for 3+ days (critical — Mode 7 confirmed)

## Related Failure Modes

- **Mode 1 (Job didn't run):** Temporary delay, job executes next cycle
- **Mode 6 (Session persistence failure):** Job runs but output lost
- **Mode 7 (Active-but-stalled):** Job stops executing entirely — this document

## Escalation

If manual re-run succeeds but the job continues to stall:
1. Check for resource constraints (disk space, memory, CPU)
2. Verify the operator agent cron system health
3. Consider recreating the job with the same configuration
4. Escalate to the operator agent core team if the issue persists

## Example Timeline

| Date | Status | Session Files | Gap |
|------|--------|---------------|-----|
| 2026-06-25 | Ran successfully | `cron_c37a1090869d_20260625_032528_*.json` | None |
| 2026-06-26 | Stalled | No new files | 3 new + 5 updates |
| 2026-06-30 | Stalled (5 days) | No new files | 15 new + 25 updates |
| 2026-07-05 | Stalled (10 days) | No new files | 30 new + 50 updates |
| 2026-07-20 | Stalled (25 days) | No new files | 75 new + 125 updates |

The key signal is that no new session files are created despite the job showing as `[active]`.