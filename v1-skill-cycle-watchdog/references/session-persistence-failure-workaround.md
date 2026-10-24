# Session Persistence Failure Workaround

**Date:** 2026-07-19 (updated)
**Job ID:** c37a1090869d (Divinity Health V1 Skill Product Review)

## Problem

Cron job runs successfully (`hermes cron list` shows `status: ok`), but the session output cannot be retrieved via `session_search`. This indicates a session storage layer failure where the job executed but its output was not persisted to the session database.

## Symptoms

1. **Job status appears healthy:**
   ```bash
   hermes cron list | grep "c37a1090869d"
   # Shows: Last run: 2026-07-18T03:27:01... ok
   ```

2. **Session directory shows no files for today's date:**
   ```bash
   ls <agent-home>/sessions/ | grep "cron_c37a1090869d" | grep "20260718"
   # Returns: Empty
   ```

3. **Session search cannot find the output:**
   ```python
   session_search(query="cron_c37a1090869d_20260718", limit=5)
   # Returns: Empty results or no relevant sessions
   ```

4. **Historical gap observed:**
   - Last accessible session file: 2026-07-05 (or similar older date)
   - Multiple days of sessions missing despite successful job runs

## Impact

- Watchdog cannot validate daily targets (3 new skills + 5 updates)
- Cannot extract counts from missing session output
- Blind spots in daily review cycle validation
- May indicate underlying session storage infrastructure issue

## Detection Protocol

### Step 1: Verify Job Ran
```bash
hermes cron list | grep "c37a1090869d"
```
Look for:
- `Last run: <today's date>... ok`
- `Next run: <tomorrow's date>`
- `[active]` status

### Step 2: Check Session Storage

**Method A: Check sessions directory for specific date pattern**
```bash
# Check for session files matching today's date pattern
ls <agent-home>/sessions/ | grep "cron_c37a1090869d" | grep "$(date +%Y%m%d)"
# If empty → No session files for today's run
```

**Method B: Check for recent session files (last 24 hours)**
```bash
# Check for recent session modifications using mtime
find <agent-home>/sessions -name "*c37a1090869d*" -mtime -1
# If empty → No session files created in last 24 hours
```

**Method C: List all session files for this job**
```bash
# List all session files for the job
ls <agent-home>/sessions/ | grep "cron_c37a1090869d"
# Check modification dates
ls -lt <agent-home>/sessions/ | grep "cron_c37a1090869d" | head -5
```

If Step 1 shows success (status: ok, today's date in Last run) but Step 2 shows no recent files for today's date → **Session persistence failure detected.**

### Step 3: Attempt Session Search

**Method A: Search by job ID and date pattern**
```python
from datetime import datetime
session_search(
    query=f"cron_c37a1090869d_{datetime.now().strftime('%Y%m%d')}",
    sort="newest",
    limit=5
)
```

**Method B: Search by job name**
```python
session_search(
    query="Divinity Health V1 Skill Product Review",
    sort="newest",
    limit=10
)
```

If session_search returns empty results or does not find today's run despite successful job status → **Confirmation of storage failure.**

### Key Indicator

**Confirmed Mode 6 Failure:**
```
hermes cron list → Last run: 2026-07-18T03:27:01... ok
ls <agent-home>/sessions/ | grep "cron_c37a1090869d" | grep "20260718" → (empty)
session_search(query="cron_c37a1090869d_20260718") → No results
```

This indicates the job executed successfully but its output was not persisted to the session database.

## Corrective Actions

### Immediate (Same Day)

**Option A: Manual Re-run with Local Delivery**
```bash
# Re-run the cron job manually to regenerate output
hermes cron run c37a1090869d
```
Then immediately check:
```bash
ls -la <agent-home>/sessions/ | grep "c37a1090869d" | tail -1
```

**Option B: Check System Storage**
```bash
# Verify session database exists and is writable
ls -la <agent-home>/sessions/sessions.db
sqlite3 <agent-home>/sessions/sessions.db ".tables"

# Check disk space
df -h <agent-home>

# Check session directory permissions
ls -ld <agent-home>/sessions/
```

**Option C: Alert on Gap**
If manual re-run is not possible, alert the user:
```
WATCHDOG ALERT: Divinity Health V1 Skill Product Review

Issue: Daily review job c37a1090869d ran successfully (status: ok), but session output is unavailable. Cannot verify today's performance against targets.

Gap: 3 new skills (UNKNOWN), 5 updates (UNKNOWN)

Corrective Action: Manually verify the session output or re-run the job to regenerate.
```

### Short-term (Within 24-48 hours)

1. **Investigate the operator agent session storage system:**
   ```bash
   # Check the operator agent logs for session storage errors
   tail -100 <agent-home>/logs/*.log | grep -i "session"

   # Verify the operator agent version
   hermes version
   ```

2. **Test session persistence:**
   ```bash
   # Create a test session
   hermes chat --non-interactive "test session persistence"

   # Verify it persists
   ls -la <agent-home>/sessions/ | tail -1
   ```

3. **Check for database corruption:**
   ```bash
   # Check session DB integrity
   sqlite3 <agent-home>/sessions/sessions.db "PRAGMA integrity_check;"
   ```

### Long-term (Root Cause Resolution)

1. **Monitor session storage health:**
   - Add session storage checks to cron-fleet-audit
   - Alert when session files are missing despite successful job runs

2. **Implement fallback delivery:**
   - Configure cron jobs to deliver output to multiple locations (local + session DB)
   - Add file-based output as backup when session storage fails

3. **Upgrade the operator agent if needed:**
   - Check if session persistence bugs are fixed in newer versions
   - Test upgrade in staging before production

## Root Cause Hypotheses

### Hypothesis 1: Session Database Corruption
- **Evidence:** Missing session files despite successful runs
- **Test:** Run `sqlite3 <agent-home>/sessions/sessions.db "PRAGMA integrity_check;"`
- **Resolution:** Restore from backup or rebuild database

### Hypothesis 2: the operator agent Daemon Outage During Job Run
- **Evidence:** Job executes but session not persisted
- **Test:** Check the operator agent daemon logs around job run time
- **Resolution:** Ensure daemon is running; add daemon health checks

### Hypothesis 3: Disk Space or Permission Issues
- **Evidence:** Cannot write session files
- **Test:** Check `df -h <agent-home>` and `ls -ld <agent-home>/sessions/`
- **Resolution:** Free disk space or fix permissions

### Hypothesis 4: Session Storage API Change
- **Evidence:** Sessions missing after specific date (e.g., after Jul 5, 2026)
- **Test:** Check the operator agent changelog for session storage changes
- **Resolution:** Update watchdog to use new session storage API

### Hypothesis 5: Session File Rotation or Cleanup Policy
- **Evidence:** Sessions exist briefly then disappear
- **Test:** Monitor session directory during and after job run
- **Resolution:** Adjust retention policy or implement archiving

## Watchdog Alert Format

When session persistence failure is detected:

```
WATCHDOG ALERT: <Job Name>

Issue: Daily review job <job_id> ran successfully (status: ok), but no session output is available. The session database shows a run occurred, but the actual review content cannot be retrieved.

Gap: Cannot verify today's performance against targets:
- 3 recommended new skills per day — UNKNOWN
- 5 updates total per day — UNKNOWN

Evidence:
- Job Last run: <timestamp>... ok
- Session files found: 0 (checked via ls <agent-home>/sessions/)
- session_search results: Empty

Corrective Action: Manually verify the session output by checking the local delivery destination or running the review job manually today to regenerate the output. Investigate why session persistence failed despite job success status.
```

## Related Skills

- `v1-skill-cycle-watchdog`: Primary watchdog that detects this mode
- `cron-fleet-audit`: Fleet-wide cron health monitoring
- `sibling-agent-auto-remediation`: Automated remediation for cron failures

## References

- Session discovery workaround: `references/session-discovery-workaround.md`
- Cron output location pitfall: `references/cron-output-location-pitfall.md`
- Stalled job detection: `cron-fleet-audit/references/stalled-job-detection.md`
- JSON block extraction: `references/json-block-extraction.md`