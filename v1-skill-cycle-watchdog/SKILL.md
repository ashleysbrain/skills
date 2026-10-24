---
name: v1-skill-cycle-watchdog
description: Watchdog for the Divinity Health V1 Skill Product Review cycle — validates daily review output against standing targets (3 new skills + 5 updates) and alerts on gaps.
tags: [operations, watchdog, cron-health, skill-cycle, target-compliance]
---

# V1 Skill Cycle Watchdog

Watchdog for the Divinity Health V1 Skill Product Review cycle (job `c37a1090869d`). Validates daily review output against standing targets and alerts on gaps.

## Standing Targets

The daily review cycle has explicit standing targets (updated 2026-07-14):
- **3 recommended new skills per day**
- **5 total updates per day** (includes patches, edits, and support files)
- Target contract is embedded in the cron prompt and skill-update-engine documentation

## Trigger Conditions

- As a scheduled watchdog cron (run 1–2 hours after the review job, e.g., 5 AM CT for a 3:25 AM review)
- After detecting any anomaly in the review job's output file
- When user asks "did the skill review job run today?" or "how are we doing on the 3+5 targets?"

## Validation Procedure

### Step 1: Verify Job Ran

**Primary method: hermes cron list**
```bash
# Check cron job status via the operator agent CLI
hermes cron list | grep "c37a1090869d"
```

**Critical pitfall: State inconsistency between cron list and jobs.json (Mode 6)**

The `hermes cron list` command output can be out of sync with the persisted `<agent-home>/cron/jobs.json` file state. This creates a reliability gap for watchdog monitoring.

**Real example (2026-07-23):**
- `hermes cron list` shows: `Last run: 2026-07-23T03:27:03.496078-05:00  ok`
- `jobs.json` contains: `"last_run": None`, `"last_run_status": None`

This discrepancy makes it impossible to verify whether the job truly ran. The list says it succeeded, but the persisted state says it never ran.

**Detection protocol:**
1. Cross-check list output against jobs.json for each job:
   ```bash
   cat <agent-home>/cron/jobs.json | python3 -c "
   import json, sys
   jobs = json.load(sys.stdin)
   for j in jobs.get('jobs', []):
       if j.get('id') == 'c37a1090869d':
           print(f\"last_run_json: {j.get('last_run')}\")
           print(f\"last_status_json: {j.get('last_run_status')}\")
   "
   ```
2. If list says `last_status='ok'` but jobs.json has `last_run: None`: **FLAG as state consistency failure**
3. Use session_search with pattern `cron_<job_id>_<YYYYMMDD>` to verify whether a session actually exists
4. If session exists: Job ran but state wasn't updated (reconcile manually or re-run)
5. If session doesn't exist: List output is stale/cached, job missed its slot (treat as Mode 4)

**See `cron-fleet-audit/references/state-consistency-check.md`** for full detection protocol and remediation steps.

**Critical pitfall: hermes script syntax errors**

When `hermes cron list` fails with a Python syntax error (e.g., `SyntaxError: invalid syntax` at line 2), this is a script-level issue in the the operator agent CLI binary, not a system outage. The script has a syntax error that prevents execution.

**Corrective action:** Use session_search as the fallback detection method (see Step 1 below). Do not report this as a critical failure or attempt to reinstall the operator agent — the watchdog's job is to detect job status, not to fix the operator agent installation issues.

Look for:
- `Last run: 2026-07-13T03:27:38... ok` (or today's date)
- `Next run: 2026-07-14T03:25:00-05:00` — critical for distinguishing between "not yet run" vs "missed run"
- Job must be `[active]`

**Critical pitfall: Interpreting "Not Yet Run Today" vs "Missed Run"**

When `Last run` shows yesterday's date, you MUST check current time against the job's scheduled run time to correctly classify the state:

**Two scenarios:**

1. **"Not Yet Run Today" (normal timedependent behavior):**
   - Current time is BEFORE the job's scheduled run time (e.g., 02:00 AM for a 03:25 AM job)
   - `Last run` shows yesterday's date
   - `Next run` shows today's timestamp in the future
   - This is NOT a failure mode — output suppression signal: `[SILENT]`

2. **"Missed Run" (failure mode):**
   - Current time is AFTER the job's scheduled run time (e.g., 10:00 AM for a 03:25 AM job)
   - `Last run` shows yesterday's date (or older)
   - `Next run` shows today's timestamp that has already passed
   - This IS a failure — job should have run but didn't
   - Alert with gap and corrective action: `hermes cron run c37a1090869d`

**Detection protocol:**
```python
from datetime import datetime, time

# Parse Last run timestamp (from `hermes cron list` output)
last_run_str = "July 20, 2026 at 03:25 AM"
last_run_date = datetime.strptime(last_run_str, "%B %d, %Y at %I:%M %p").date()

# Job scheduled for 03:25 AM daily
scheduled_time = time(3, 25)

# Check current time
now = datetime.now()
now_time = now.time()
now_date = now.date()

if now_time < scheduled_time and now_date > last_run_date:
    # Scenario 1: Not yet run today (normal)
    classification = "Timedependent"
    should_alert = False
elif now_time >= scheduled_time and now_date > last_run_date:
    # Scenario 2: Missed run (failure)
    classification = "Missed Run"
    should_alert = True
    corrective_action = "hermes cron run c37a1090869d"
```

**Alert classification for each scenario:**

**Scenario 1 - Timedependent (normal):**
```
### Gap Classification

**Timedependent** — The review job has not executed yet today. No output is available to compare against standing targets.

### Next Corrective Action

Wait for the job to run at its scheduled time. If the job fails to execute or produces no output by end of day, investigate the cron schedule and job configuration.
```
Output: `[SILENT]` (suppress delivery)

**Scenario 2 - Missed Run (failure):**
```
**V1 Skill Product Review Alert**

**Date:** July 21, 2026  
**Review Job:** c37a1090869d (Divinity Health V1 Skill Product Review)

**Status: Job not yet run today**

The daily review job has not executed for July 21. Last confirmed run was July 20, 03:25 AM.

**Previous Day (July 20) Performance:**
- New skills recommended: target 3, actual 0 (gap: 3)
- Total updates: target 5, actual 0 (gap: 5)

**Corrective Action:**
Manually trigger the review job: `hermes cron run c37a1090869d`
```
Output: Alert the user (deliver the message)

**Critical distinction:** Always compare current time against scheduled run time. Never rely solely on `Last run` date without temporal context.
**Fallback method: Session database search**

Search for the job's latest cron session using session_search with the job ID prefix pattern:

```python
# Search for today's session using the cron_<job_id>_YYYYMMDD pattern
session_search(
    query="cron_c37a1090869d_20260723",
    sort="newest",
    limit=5
)
```

**Critical pitfall: Session naming convention variation**

The watchdog must check BOTH naming patterns when searching for today's session:
1. `cron_<job_id>_<YYYYMMDD>` — standard format (e.g., `cron_c37a1090869d_20260723`)
2. `cron_<job_id>_<YYYYMMDD>_<HHMMSS>` — timestamped format (e.g., `cron_c37a1090869d_20260723_032544`)

**Best practice (2026-08):** Search for the review job title or content rather than relying on session ID patterns. Use:
```python
session_search(query="Divinity Health V1 Skill Product Review", limit=5, sort="newest")
```
This returns the actual review session even if the naming convention changes, and avoids confusing review sessions with watchdog sessions (which have job ID `31e90033684f`).

See `references/session-discovery-pattern-august-2026.md` for detailed evidence of the multi-session confusion pattern.

If BOTH patterns return zero results AND current time is after the scheduled run time, this confirms the job has not run today (Mode 1: Job didn't run).

**Detection protocol:**
```python
# Try pattern 1: cron_<job_id>_YYYYMMDD
result1 = session_search(query="cron_c37a1090869d_20260723", limit=5, sort="newest")

# Try pattern 2: cron_<job_id>_YYYYMMDD_HHMMSS
result2 = session_search(query="cron_c37a1090869d_20260723_", limit=5, sort="newest")

if result1["count"] == 0 and result2["count"] == 0:
    # No session found for today — job hasn't run
    if current_time > scheduled_run_time:
        # Mode 1 confirmed: Job didn't run (failure)
        alert_with_corrective_action()
    else:
        # Normal: Not yet run today (time-dependent)
        output_silent()
```

**Critical pitfall: hermes cron output command does not exist**

The skill documentation historically referenced a `hermes cron output <job_id>` command, but this subcommand is NOT available in the the operator agent CLI. Attempting it will fail with:

```
hermes cron: error: argument cron_command: invalid choice: 'output' (choose from 'list', 'create', 'add', 'edit', 'pause', 'resume', 'run', 'remove', 'rm', 'delete', 'status', 'tick')
```

**Workaround:** Use session_search to find the cron session and read its output, or check the structured output from the review job's own session when it runs.

### Critical pitfall: session_search results exceed size limits

When session_search results exceed the size limit, they are persisted to a temporary file. The watchdog will see a message like:
```
This tool result was too large (596,131 characters, 582.2 KB).
Full output saved to: /var/folders/s7/vr8dmw9n7tn2f0wm_7phmslr0000gn/T/hermes-results/call_<hash>.txt
```

**Direct workaround from the watchdog's perspective:**
The watchdog script cannot access the temp file path shown in the error message because it varies per session. Instead, use the pattern shown in Step 2 to extract the JSON monitoring block from the persisted session content.

**For agents with access to the persisted file path:**
Read the persisted file and use Python regex parsing as shown in Step 2. The JSON block extraction method is more reliable than plain-text regex because it extracts structured data with shortfall_label classification.

See `references/session-search-size-limit-workaround.md` for detailed patterns and examples.

### Step 2: Extract Actual Counts (Primary Method: File-Based When Available)

**Extraction preference heuristic:**

1. **File-based extraction** (primary when available): Grep cron output directory for JSON fields — fastest, most reliable when directory exists
2. **session_search with job title** (fallback): Search for "Divinity Health V1 Skill Product Review" — works even if file paths change
3. **session_search with job ID pattern** (last resort): `cron_c37a1090869d_YYYYMMDD` — fragile if naming convention changes

**File-based extraction (preferred when directory exists):**

```bash
# Check directory exists and contains today's file
if [ -d <agent-home>/cron/output/c37a1090869d ]; then
  today_file=$(ls <agent-home>/cron/output/c37a1090869d/$(date +%Y-%m-%d)_*.md 2>/dev/null)
  if [ -n "$today_file" ]; then
    # Extract JSON monitoring fields
    grep -E "new_skills_recommended|updates_generated|shortfall_label|pipeline_status" "$today_file"
  fi
fi
```

**Observed working output (2026-08-07):**
```
  "new_skills_recommended": 0,
  "updates_generated": 0,
  "shortfall_label": "philosophical",
  "shortfall_reason": "V1 core + support pair (8d-pattern-awareness + 8d-snapshot-report) assessed as coherent and complete; maintenance-only cycle",
  "pipeline_status": "nominal",
```

**See also:** `references/cron-output-file-structure-observed.md` for detailed file structure, naming convention, and historical pattern extraction patterns.

**Session-based extraction (fallback when directory doesn't exist):**

When the cron output directory is not accessible, extract the JSON block from session_search results:

```python
import json
import re
from pathlib import Path

# The session_search results for cron_c37a1090869d are saved to a temp file
# Path format: /var/folders/.../hermes-results/call_<hash>.txt

# Read the persisted session output
with open('/var/folders/s7/vr8dmw9n7tn2f0wm_7phmslr0000gn/T/hermes-results/call_<hash>.txt', 'r') as f:
    content = f.read()

# Extract JSON block from the assistant's final response
# Pattern 1: Find JSON object with monitoring fields
json_match = re.search(
    r'\{\s*"new_skills_recommended"\s*:\s*\d+.*?"pipeline_status"\s*:\s*"[^"]+".*?\}',
    content,
    re.DOTALL
)

if json_match:
    try:
        data = json.loads(json_match.group(0))
        new_skills = data.get("new_skills_recommended", 0)
        updates = data.get("updates_generated", 0)
        status = data.get("pipeline_status", "unknown")
        shortfall_label = data.get("shortfall_label", "structural")
    except json.JSONDecodeError:
        # Fallback: parse plain text if JSON is malformed
        skills_match = re.search(r'(?i)"new_skills_recommended"\s*:\s*(\d+)', content)
        updates_match = re.search(r'(?i)"updates_generated"\s*:\s*(\d+)', content)
        new_skills = int(skills_match.group(1)) if skills_match else 0
        updates = int(updates_match.group(1)) if updates_match else 0
else:
    # Fallback: grep for key-value pairs in the persisted file
    skills_match = re.search(r'(?i)"new_skills_recommended"\s*:\s*(\d+)', content)
    updates_match = re.search(r'(?i)"updates_generated"\s*:\s*(\d+)', content)
    new_skills = int(skills_match.group(1)) if skills_match else 0
    updates = int(updates_match.group(1)) if updates_match else 0
```

**Critical insight:** The review job emits its counts in a structured JSON monitoring block. When session_search results are too large and persisted to a temp file, extract the JSON block directly from the persisted file content rather than parsing plain text. This is more reliable because:
- The JSON block is a structured contract (Section 13.1)
- It includes shortfall_label for distinguishing philosophical vs. structural gaps
- It includes pipeline_status for confirming nominal operation
- It survives session truncation better than plain-text patterns

**See `references/json-block-extraction.md` for complete robust extraction methods including handling multiple JSON blocks, validation, and edge cases.**

**Critical pitfall: Cron output file location accessibility varies**

**Context:** The cron output directory `<agent-home>/cron/output/<job_id>/` may or may not exist depending on the operator agent version, cron configuration, and job setup. The watchdog must detect which state applies and adapt its extraction method accordingly.

**Three modes to detect:**

| Mode | Symptom | What it means | Extraction method |
|------|---------|---------------|-------------------|
| **Directory doesn't exist** | `test -d <agent-home>/cron/output/c37a1090869d` fails | Cron output location changed, job not configured to write files, or the operator agent version difference | Use session_search as primary; do not attempt file-based access |
| **Directory exists but files missing** | Directory present but no file for today's date | Job didn't run, failed silently, or wrote to a different location | Investigate job execution (check `hermes cron list`, session_search for today) |
| **Directory exists with valid files** | Directory present + today's timestamp file exists + grep extracts JSON fields | **Normal operation** — file-based extraction is viable and preferred | File-based extraction is the best option; faster and more reliable than session_search |

**Detection protocol:**
```bash
# Check directory exists
if [ -d <agent-home>/cron/output/c37a1090869d ]; then
  # Check for today's file
  today_file=$(ls <agent-home>/cron/output/c37a1090869d/$(date +%Y-%m-%d)_*.md 2>/dev/null)
  if [ -n "$today_file" ]; then
    # Mode 3: File-based extraction available
    grep -E "new_skills_recommended|updates_generated|shortfall_label|pipeline_status" "$today_file"
  else
    # Mode 2: Directory exists but no files today
    echo "Directory exists but no output for today - investigate job execution"
  fi
else
  # Mode 1: Directory doesn't exist - use session_search
  echo "Directory not accessible - fallback to session_search"
fi
```

**Extraction preference heuristic:**
1. **File-based extraction** (primary): Grep cron output directory for JSON fields — fastest, most reliable when directory exists
2. **session_search with job title** (fallback): Search for "Divinity Health V1 Skill Product Review" — works even if file paths change
3. **session_search with job ID pattern** (last resort): `cron_c37a1090869d_YYYYMMDD` — fragile if naming convention changes

**File-Size Anomaly Check (Step 5) and Step 2a:** These sections are ONLY invalid in Mode 1 (directory doesn't exist). In Mode 3 (directory exists with valid files), file-based methods are the preferred extraction path. Do not remove these sections; instead, guard them with directory existence checks.

**Observed working example (2026-08-07):**
- Directory exists: `<agent-home>/cron/output/c37a1090869d/`
- Contains 7 timestamped files: `2026-08-01_07-10-24.md` through `2026-08-07_03-27-27.md`
- Grep successfully extracted: `new_skills_recommended: 0`, `updates_generated: 0`, `shortfall_label: "philosophical"`
- Historical pattern extraction worked by looping through files to identify 7-day philosophical shortfall streak

**See also:** `references/cron-output-file-structure-observed.md` for detailed observed file structure, naming convention, and extraction patterns.

### Step 2a: Fallback Structural Marker Check (File-Based)

If session_search is unavailable or the persisted output is corrupted, fall back to checking the cron output file for structural markers:

```bash
# Check for required section headers and JSON fields
grep -c "## RECOMMENDED NEW SKILLS" /<workspace>$(date +%Y-%m-%d)_*.md
grep -c "new_skills_recommended" /<workspace>$(date +%Y-%m-%d)_*.md
grep -c "pipeline_status" /<workspace>$(date +%Y-%m-%d)_*.md
grep -c "updates_generated" /<workspace>$(date +%Y-%m-%d)_*.md
```

Expected: All counts >= 1. Zero matches on ANY required marker = **content substitution confirmed** — the agent produced output for the wrong task (prompt drifted or was overwritten).

### Step 3: Extract Actual Counts Against Targets

The output contains a JSON block (Section 13.1 contract in skill-update-engine) with the actual counts:

```bash
# Extract the JSON block and parse counts
grep -A 10 '"pipeline_status"' /<workspace>$(date +%Y-%m-%d)_*.md | grep -E "(new_skills_recommended|updates_generated)"
```

Alternatively, use Python for reliable parsing:

```python
import json, re, pathlib

output_file = pathlib.Path.home() / ".hermes/cron/output/c37a1090869d" / f"{date.today()}_*.md"
content = output_file.read_text()

# Extract JSON block using regex (Section 13.1 format)
json_match = re.search(r'```json\s*({[^`]+})\s*```', content, re.DOTALL)
if json_match:
    data = json.loads(json_match.group(1))
    new_skills = data.get("new_skills_recommended", 0)
    updates = data.get("updates_generated", 0)
    status = data.get("pipeline_status", "unknown")

    print(f"Target: 3 new + 5 updates")
    print(f"Actual: {new_skills} new + {updates} updates")
    print(f"Status: {status}")
```

### Step 4: Calculate Gap

```
new_skills_gap = max(0, 3 - new_skills_recommended)
updates_gap = max(0, 5 - updates_generated)
```

## Alert Framing

Report the gap with:
- The target (3 new + 5 updates)
- The actual counts (new_skills_recommended, updates_generated)
- The gap size (new_skills_gap, updates_gap)
- The shortfall_label from the JSON block ("philosophical" vs "structural")
- The corrective action (re-run the job if stall/substitution detected; otherwise surface the gap and expect next run to catch up)

**DO NOT reschedule jobs or ask the user questions.** The watchdog's role is detection and framing, not remediation. Remediation is handled by other agents or manual intervention.

## Pattern Recognition: Persistent Shortfalls

### 3+ Day Escalation Rule

When a philosophical shortfall persists across **3+ consecutive days**, the watchdog must escalate from gap reporting to **target-calibration issue alerting**.

**Rationale:** Daily gap alerts on a correctly functioning system create alert fatigue. The signal is not "job is failing" — it's "targets do not match reality."

**Escalation format:**
```markdown
### Gap Classification

**Philosophical** — The family is coherent and complete. The targets (3 new skills + 5 updates/day) do not match the reality of what the Divinity Health V1 skill family actually requires.

### Pattern Observed

This shortfall has persisted for multiple days. The review job is running successfully and producing output, but consistently reports zero new skills and zero updates against standing targets that do not align with the actual market signal cadence or the current state of the skill family.

### Next Corrective Action

Recalibrate the targets in the skill-update-engine configuration for the Divinity Health V1 review cycle to match the actual cadence of market signals and the stable state of the existing skill family, or adjust the job to focus on quality monitoring rather than volume-based production.
```

**Implementation:** Track consecutive philosophical shortfalls and only escalate after day 3. See `references/persistent-philosophical-shortfall.md` for full pattern documentation and example alerts.

## Common Pitfalls

### Treating Philosophical Shortfalls as Failures

**Problem:** When a review job reports `new_skills_recommended: 0` and `updates_generated: 0` but `pipeline_status: "nominal"` and `shortfall_label: "philosophical"`, naive watchdogs treat this as a critical failure and alert daily.

**Root Cause:** The watchdog is not parsing the JSON block's `shortfall_label` field and therefore cannot distinguish between:
- Philosophical shortfalls: the family is coherent and complete — zero delivery is correct behavior
- Structural shortfalls: the pipeline failed or stalled — zero delivery indicates a problem

**Fix:** Always parse the `shortfall_label` field from the JSON block. When `shortfall_label == "philosophical"`:
- Downgrade the alert to informational (or suppress if `pipeline_status == "nominal"`)
- Only escalate after 3+ consecutive days with the same root cause as a target-calibration issue
- See `references/philosophical-shortfall-pattern.md` for detailed guidance and example patterns
- See `references/persistent-philosophical-shortfall.md` for escalation format and corrective action framing

**Evidence:** The Divinity Health V1 skill family has correctly reported "family complete" with philosophical shortfalls across 2026-07-11 through 2026-07-15. Watchdogs that fail to parse `shortfall_label` generate daily alert fatigue on a correctly functioning system.

## Detection Modes and Corrective Actions

| Mode | Symptoms | Corrective Action |
|------|----------|-------------------|
| **Job didn't run** | No output file for today, or file missing entirely | Check cron scheduler status and job configuration; consider manual re-run |
| **Hard error** | `last_status != 'ok'` | Investigate error details in session; fix root cause |
| **Stall (Mode 2)** | Session ends mid-execution with dangling exploratory sentence, no final summary markers | Re-run the job to complete the cycle |
| **Narrative-only drift (Mode 3)** | Complete report with markers but 0 artifact-producing tool calls | Tell job to actually execute the work it described; next run must produce skills/updates |
| **Missed trigger (Mode 4)** | `Last run` predates expected trigger, no session created | Check for systemic scheduler/gateway outage; re-run manually |
| **Content substitution (Mode 5)** | Required structural markers = 0, file contains wrong content (e.g., fleet management strategy) | Verify cron prompt hasn't been overwritten; re-run with correct prompt |
| **Session persistence failure (Mode 6)** | hermes cron list shows job ran successfully (status: ok), but session_search cannot retrieve the session output. Session database shows no recent files for the job despite successful execution. | Detect via filesystem check: ls <agent-home>/sessions/ | grep "cron_c37a1090869d" | grep "$(date +%Y%m%d)" returns empty. Verify with find <agent-home>/sessions -name "*c37a1090869d*" -mtime -1. If job status is ok but no recent files exist → Mode 6 confirmed. Corrective actions: Check session storage system (disk space, permissions, database integrity), manually re-run job to regenerate output, or investigate the operator agent session persistence layer. Alert may indicate transient session storage outage or configuration change. See references/session-persistence-failure-workaround.md for full detection protocol and root cause hypotheses. |
| **Active-but-stalled (Mode 7)** | hermes cron list shows job as [active] with valid Last run timestamp, but session directory contains no files newer than that timestamp. The job appears enabled but stopped executing entirely. | Detection protocol: Verify job is [active], then check session directory: ls <agent-home>/sessions/ | grep "cron_c37a1090869d" | sort | tail -5. If most recent file predates expected schedule by days/weeks → Mode 7 confirmed. Critical distinction: Unlike Mode 1 (job hasn't run yet today), Mode 7 is sustained failure where Last run freezes. Root causes: Cron daemon stopped, schedule lost, silent errors, the operator agent cron system failure. Corrective action: Manual re-run: hermes cron run c37a1090869d. Calculate cumulative gap: (days_stalled × 3) new skills + (days_stalled × 5) updates missing. See references/active-but-stalled-job-workaround.md for full detection protocol and investigation steps. |
| **Transient provider error (Mode 8)** | Job fired on schedule but `last_status` shows a `RuntimeError` / HTTP error (e.g. `HTTP 429: Rate limit reached`), AND the session exists with `message_count == 1` (only the prompt, zero assistant content — the model call was killed before it produced output). No engine report JSON block is emitted because no review actually ran. | **Classification: structural-but-transient** (NOT philosophical, NOT a stall). Alert once with the day's gap (-3 new / -5 updates); expect self-clear on the next scheduled run when the rate-limit window resets or the provider recovers. Do NOT manually re-run on first occurrence. Escalation trigger: if the SAME transient error recurs on consecutive scheduled runs, it flips from transient to persistent — investigate provider quota, concurrent-job contention, or sustained outage. The `message_count == 1` marker cleanly distinguishes Mode 8 from Mode 1 (no session at all), Mode 6 (ran ok but session unrecoverable), and Mode 7 (active but stopped for days). Observed 2026-08-01 on `c37a1090869d`: `HTTP 429`, session `cron_c37a1090869d_20260801_070902` had only the prompt message. See cron-fleet-audit → "Transient provider errors (Mode 8)" for the general pattern. |

## File-Size Anomaly Check (Fast Pre-Filter)

Before deep inspection, compare today's output file size against the rolling baseline (last 5–7 runs):

```bash
# Get today's size
today_size=$(stat -f%z /<workspace>$(date +%Y-%m-%d)_*.md 2>/dev/null)

# Get baseline (last 5 runs)
baseline_avg=$(ls -lh /<workspace>*.md | tail -5 | awk '{sum+=$5} END {print sum/NR}')

# Calculate deviation
deviation=$(( (today_size - baseline_avg) * 100 / baseline_avg ))

# Flag if >40% smaller or >60% larger
if [ $deviation -lt -40 ] || [ $deviation -gt 60 ]; then
    echo "WARNING: File size anomaly detected. Deviation: ${deviation}%"
fi
```

This is a fast signal but not conclusive — legitimate short cycles exist. Always follow up with the structural marker check for definitive diagnosis.

## Output Format

Produce a concise alert with this structure:

```
## V1 Skill Cycle Watchdog — YYYY-MM-DD

**Target:** 3 new skills + 5 updates

**Actual:** X new skills + Y updates

**Gap:** (3-X) new skills + (5-Y) updates

**Status:** [ON TRACK | GAP DETECTED | CRITICAL FAILURE]

[Gap details and corrective action]
```

If everything is on track, output exactly `[SILENT]` to suppress delivery (this is the watchdog's suppression signal).

## Related Skills

- `cron-fleet-audit`: Fleet-wide health checks including stalled job detection and Mode 3–5 failure modes
- `skill-update-engine`: The daily skill review engine itself — defines the targets and output contract
- `sibling-agent-auto-remediation`: Closed-loop remediation for cron job failures

## References

- See `references/philosophical-shortfall-pattern.md` for distinguishing between philosophical shortfalls (coherent families) vs. structural shortfalls (pipeline failures) and the correct watchdog routing rules
- See `references/json-block-extraction.md` for robust methods to extract the Section 13.1 JSON monitoring block from large cron output files (handles multiple JSON blocks, multiline JSON, and validation)
- See `references/cron-output-file-structure-observed.md` for observed cron output directory structure, file naming convention, and file-based extraction patterns (2026-08-07)
- See `references/session-discovery-workaround.md` for fallback patterns when `session_search` exceeds size limits or cron output location has changed
- See `references/session-search-size-limit-workaround.md` for handling persisted session output files when session_search results are too large
- See `references/session-persistence-failure-workaround.md` for detecting and handling Mode 6 failures where job succeeds (status: ok) but session output is unavailable due to storage layer issues
- See `references/active-but-stalled-job-workaround.md` for detecting and handling Mode 7 failures where job shows as [active] but stopped executing entirely — includes detection protocol, root cause hypotheses, and gap calculation
- See `references/cron-output-location-pitfall.md` for the critical pitfall of assuming cron output file paths exist — always use session_search instead of direct file system access to cron output directories
- See `cron-fleet-audit/references/stalled-job-detection.md` for the full failure mode taxonomy (Modes 1–5) including content substitution detection
- See `skill-update-engine` §13.1 for the JSON output block contract and standing target specification
- See `skill-update-engine` §R15 and §13.2 for target-profile mismatch guidance and philosophical shortfall routing rules