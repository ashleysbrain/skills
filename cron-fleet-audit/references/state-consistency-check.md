# State Consistency Check (Mode 6)

## Problem

The `hermes cron list` command output can be out of sync with the persisted `<agent-home>/cron/jobs.json` file state. This creates a **reliability gap** for watchdog monitoring jobs that depend on accurate run status.

### Real Example (2026-07-23)

Job `c37a1090869d` (Divinity Health V1 Skill Product Review):

**`hermes cron list` output:**
```
Last run: 2026-07-23T03:27:03.496078-05:00  ok
```

**`jobs.json` file content:**
```python
"last_run": None
"last_run_status": None
```

The list command claims the job ran successfully today, but the persisted state says it never ran. A watchdog job checking this job cannot verify output counts against targets because:
1. The source of truth (`jobs.json`) says "never ran"
2. But the session actually exists (found via `session_search(query="cron_c37a1090869d")`)
3. The discrepancy makes it unclear whether the job truly ran, the list is stale, or the file update failed

This is **worse than a simple error** — it's a **silent state inconsistency** that masks the actual problem.

## Root Causes

1. **Cached list output**: The `hermes cron list` command may read from an in-memory cache that isn't synced to disk after each job run
2. **Failed file write**: The job runner may have executed the session but failed to update `jobs.json` with the result (write error, permission issue, or process killed mid-write)
3. **Race condition**: The list command reads while a job is updating `jobs.json`, reading a partially-written or old state
4. **Manual intervention**: Someone manually edited `jobs.json` or re-ran a job without updating the state file

## Detection

### Automated Check

For each job in the cron fleet:

1. **Extract list output data**: Parse `hermes cron list` to get:
   - `last_run_list` (timestamp)
   - `last_status_list` ('ok', 'error', null)

2. **Read jobs.json directly**:
   ```bash
   cat <agent-home>/cron/jobs.json | python3 -c "
   import json, sys
   jobs = json.load(sys.stdin)
   for j in jobs.get('jobs', []):
       if j.get('id') == 'TARGET_JOB_ID':
           print(f\"last_run_json: {j.get('last_run')}\")
           print(f\"last_status_json: {j.get('last_run_status')}\")
   "
   ```

3. **Compare**:
   - If `last_status_list == 'ok'` AND `last_run_json is None`: **FLAG as state consistency failure**
   - If `last_run_list` timestamp exists but `last_run_json is None`: **FLAG as state consistency failure**
   - If `last_status_list` != `last_status_json`: **FLAG as state mismatch** (less severe but still suspicious)

### Session Verification

When a state consistency failure is detected:

1. **Search for the session**: Use `session_search` with pattern `cron_<job_id>_<YYYYMMDD>`:
   ```bash
   session_search(query="cron_c37a1090869d_20260723", limit=1, sort="newest")
   ```

2. **Check session exists**: 
   - If session exists and has a final assistant message: The job **did run**, but `jobs.json` wasn't updated
   - If session does NOT exist: The list output is **stale/cached**, and the job actually missed its slot (Mode 4)

## Remediation

### Case A: Session Exists (ran, but state not updated)

**Option 1: Manual state reconciliation** (preferred for critical jobs)
```python
import json
from pathlib import Path
from datetime import datetime

jobs_path = Path.home() / ".hermes" / "cron" / "jobs.json"
jobs_data = json.loads(jobs_path.read_text())

# Find and update the job
for job in jobs_data["jobs"]:
    if job["id"] == "TARGET_JOB_ID":
        job["last_run"] = "2026-07-23T03:27:03.496078-05:00"
        job["last_run_status"] = "ok"
        # Optionally capture session_id if available
        job["last_run_session_id"] = "cron_TARGET_JOB_ID_20260723_032710"
        break

jobs_path.write_text(json.dumps(jobs_data, indent=2))
```

**Option 2: Re-run the job** (if state update is unreliable)
```bash
hermes cron run TARGET_JOB_ID
```
This forces a fresh run and creates a new state entry. Downside: wastes API calls if the original run actually produced valid output.

### Case B: Session Does Not Exist (list is stale, job missed slot)

Treat as **Mode 4 (Missed Schedule Trigger)** — the scheduler never fired the job:

1. **Check for clustered misses**: Did other jobs in the same time window also miss?
   - If yes: Systemic scheduler/gateway outage. Check gateway logs, systemd service status.
   - If no: Isolated issue specific to this job.

2. **Manual run** (for critical daily jobs):
   ```bash
   hermes cron run TARGET_JOB_ID
   ```

3. **Investigate scheduler**:
   - Check if the scheduler service is running: `systemctl status hermes-cron` (if applicable)
   - Check scheduler logs for errors around the expected trigger time
   - Verify the cron schedule syntax is valid (`cron "25 3 * * *" --test`)

### Case C: State Mismatch (different statuses, both non-null)

If `last_status_list == 'ok'` but `last_status_json == 'error'` (or vice versa):

1. **Trust `jobs.json`**: The persisted file is the source of truth. The list output may be cached or stale.
2. **Verify session**: Search for the session to see what actually happened.
3. **If session shows error**: The list output is wrong; ignore it and use `jobs.json` state.
4. **If session shows success**: The `jobs.json` update failed; reconcile manually (Case A, Option 1).

## Prevention

### For Cron Fleet Owners

1. **Audit schedule**: Add a weekly state consistency check to your cron audit script. Detect drift before it breaks watchdogs.
2. **Watchdog resilience**: Design watchdogs to handle inconsistent state gracefully — don't assume `jobs.json` is always up-to-date.
3. **Reconciliation job**: Add a weekly reconciliation job that cross-checks `hermes cron list` against `jobs.json` and auto-fixes discrepancies.

### For the operator agent Cron System (Platform-Level Fix)

1. **Atomic state updates**: Ensure `jobs.json` is written atomically (write to temp file, then `os.replace()`) to prevent partial writes.
2. **Sync on write**: Flush any in-memory cache to disk immediately after each job run.
3. **State verification**: After each job run, verify the persisted state matches what was written. If not, log a warning and retry.
4. **List source of truth**: Make `hermes cron list` always read from `jobs.json` directly, never from cache.

## Watchdog Impact

Watchdog jobs that verify output counts against targets (e.g., "3 new skills + 5 updates per day") are **blocked** by state inconsistency:

- If `jobs.json` says `last_run: None`, the watchdog cannot locate the session to count artifacts
- If the list says it ran but the state disagrees, the watchdog doesn't know which source to trust
- The watchdog may alert incorrectly ("job never ran") when it actually did, or miss a real problem ("job ran") when it didn't

**Recommendation**: Add a Mode 6 state consistency check to all cron fleet watchdog scripts before attempting artifact quantification or target comparison.

## References

- See `SKILL.md` → "State consistency check (Mode 6)" for the health check integration
- See Mode 4 (missed trigger) in `references/stalled-job-detection.md` for session verification when the job never fired
- See `references/cron-output-format.md` for the `jobs.json` file structure and parsing approach