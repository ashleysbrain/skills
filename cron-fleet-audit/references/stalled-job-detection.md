# Stalled/Incomplete Job Detection

## Problem
Cron jobs can show "ok" status in `hermes cron list` but the actual agent session may have stalled mid-execution without producing the expected final output (recommendations, updates, summary). This creates a false sense of health — the fleet looks green but critical daily work isn't completing.

## Root Causes
- Token/continuation limits hit during long-running review jobs
- Model timeouts or truncation errors (e.g., "Response remained truncated after 3 continuation attempts")
- Agent hitting a tool limit or error that doesn't crash the cron but stops productive work
- Skill execution paths that don't reach the final summary phase
- **Exploration trap (recurring on V1 Skill Product Review, job `c37a1090869d`):** the agent burns its entire context budget on exploratory filesystem/skill inspection (`ls -la` of reference dirs, checking for attachments, reading template files) and never reaches the actual review/synthesis phase. Observed on Jun 12, Jun 14, **and Jun 15** — three confirmed recurrences with the identical signature: final assistant message is a dangling exploratory sentence with no follow-up (e.g., "Now, let's check if there is an attachments directory…" on Jun 12/14; "Let's check if there is a scripts directory." on Jun 15). The session has 15-18 messages, all tool-exploration, zero recommendations emitted. The trigger is specifically the `8d-snapshot-report` skill, which has 8 references + 1 template; the skill-update-engine's single-job mode reads all of them and stalls. This is a scope/sequencing failure, not a token-limit crash. The permanent fix is in `skill-update-engine` §11.1 — apply a reference-file budget (max 3 files per skill in the scan phase unless it's the primary review target) and require the JSON output block to be emitted before any deep-dive tool use.

## Four Failure Modes (false-health taxonomy)
Jobs can look green in `hermes cron list` for four distinct reasons. Detection differs for each:

1. **Hard error** — `last_status != 'ok'`. Caught by the Error Scan. Easy.
2. **Stall** — `ok` status, but the session ended mid-execution with no final summary (dangling exploratory sentence, empty content + trailing tool_calls). Caught by the marker check below. The exploration trap on `c37a1090869d` (Jun 12/14/15) is this mode.
3. **Narrative-only drift** — `ok` status, session ended cleanly, AND the final assistant message contains a *complete, well-formed report* with all deliverable markers ("Status:", "Next Recommended Release", "Risks", "Confidence", "Summary"). The marker check passes — but the run produced **zero artifact-producing tool calls** (`skill_manage`, `patch`, `write_file`) against a standing quantitative target. Observed Jun 20 on `c37a1090869d`: 7 `read_file` + 2 `search_files` + 5 `terminal` (all read-only), 0 writes, against a target of 3 new skills + 5 updates. The agent *narrated* a recommendation ("Next Recommended Release: 8D Pattern Awareness v1.1.8") without ever applying it. Marker-based detection falsely classifies this as healthy.
4. **Missed schedule trigger** — the scheduler never fired the job at all. There is **no session** to inspect. The `Last run` timestamp is from a previous day, and `Next run` has rolled past the expected slot. Observed Jun 21 on `c37a1090869d`: daily `25 3 * * *` job, last run Jun 20 03:31, next run rolled to Jun 22 03:25 — today's 03:25 slot skipped entirely with zero sessions created. This is invisible to Modes 1–3 detection (which all require a session to exist) and to the 7-day stale-job check (too coarse for critical daily jobs). Detection is purely timestamp-based — see "Missed Schedule Trigger Detection (Mode 4)" below.

**Mode 3 is the sneakiest of Modes 1–3** because the report looks done. The only reliable signal is tallying artifact-producing tool calls and comparing against the job's standing target. See "Artifact-Quantification Check" below.

**Mode 4 is the hardest to catch** because it produces no evidence trail — no session, no error, no output. The only signal is the gap between `Last run` and the expected trigger time derived from the cron expression.

**Mode 5 (content substitution) is visually the most deceptive** because the job ran, produced a file, and the file has non-trivial content — but the content is completely off-topic. The agent's prompt was overwritten, drifted, or the model hallucinated a substitute task. The output looks like a legitimate report but is NOT the expected deliverable. Only structural validation catches it.

## Detection Strategy
The `audit_cron_fleet.py` script now includes `check_stalled_jobs()` which:

1. **Identifies critical daily jobs** by keyword matching on job names (V1 Skill Product Review, Advisory Boards, SENTINEL, VITALS, NEXUS, etc.)
2. **Cross-references with session data** — requires a session JSON mapping job_id → {last_message_preview, session_id, message_count}
3. **Checks for final summary markers** in the last assistant message:
   - "recommend", "update", "new skill", "gap", "target"
   - "drift", "corrective action", "summary", "delivered"
   - "completed", "status:", "drift against"
4. **Flags as stalled** if critical job + session exists + no final summary markers

## Interactive Detection Recipe (no pre-built session_data.json needed)
When running detection interactively (e.g. a watchdog cron job), produce the job→session mapping on the fly:

1. `hermes cron list` — get the job_id and `last run` timestamp/status.
2. `hermes sessions list --source cron --limit 30` — map job_id to session_id. The session ID follows the format `cron_<job_id>_<YYYYMMDD>_<HHMMSS>`. Match on the job_id segment.
3. `session_search(session_id="cron_<id>_<date>_<time>")` — read the full session. The output can be large (>100KB); it's persisted to a temp file — use a JSON parse to extract the final assistant message and its `content` vs `tool_calls` keys.

   **⚠️ Scroll window gap (2026-06-27):** When using `session_search` in scroll mode (with `around_message_id` + `window`), the returned messages are a ±N window centered on the anchor. If you anchor on the user prompt (first message), the final substantive assistant message may fall OUTSIDE the window. For example, a session with 25 messages anchored on msg 217312 with window=20 returns msgs 217312–217332, but the actual final report is msg 217336. The scroll's last assistant message appears empty/truncated — a false stall signal. **When the scroll's last assistant message is empty or the content_len is suspiciously small, fall back to direct SQLite query:**
   ```
   python3 << 'PYEOF'
   import sqlite3, os
   db = os.path.expanduser('<agent-home>/state.db')
   conn = sqlite3.connect(db)
   rows = conn.execute(
       "SELECT id, content FROM messages WHERE session_id=? AND role='assistant' "
       "AND content IS NOT NULL AND content != '' ORDER BY id DESC LIMIT 3",
       (session_id,)
   ).fetchall()
   for r in rows:
       print(f"=== id={r[0]} len={len(r[1])} ===")
       print(r[1][:3000])
       print()
   PYEOF
   ```
   This reliably gets the actual final assistant message regardless of scroll window position. The `messages` table stores every message with its full content; `session_search` scroll is a convenience view, not the authoritative source.

4. Inspect the **last assistant message** (from the scroll OR the DB query, whichever gave the real final message):
   - **Stalled signature:** content is an incomplete sentence (often ending in "…" or a dangling "Now, let's check…") with no follow-up tool call, OR content is empty string with only `tool_calls` and no subsequent messages. No final report markers present.
   - **Healthy signature:** final assistant message contains deliverable markers ("recommend", "target", "gap", "drift", "status:", "completed", etc.).

Note: `hermes cron list` shows `ok` for these stalled jobs — the `ok` status only means the process exited cleanly, NOT that the deliverable was produced. Always inspect the session's final message.

## Artifact-Quantification Check (Mode 3: narrative-only drift)
Use this when a job has a standing *quantitative* target (e.g. "3 new skills + 5 updates per day", "≥1 PR reviewed", "N items triaged"). The marker check from the Interactive Recipe above will pass for narrative-only drift — the report is complete and well-formed — so you must go one layer deeper and count what the agent actually *did*, not what it *said*.

**Recipe (interactive / watchdog):**
1. Run the Interactive Detection Recipe steps 1–3 to load the session JSON.
2. Tally tool calls by name across all assistant messages. In Python on the parsed `messages` list:
   ```python
   from collections import Counter
   types = Counter()
   for m in msgs:
       if m.get("role") == "assistant" and m.get("tool_calls"):
           for tc in m["tool_calls"]:
               name = tc.get("name") or (tc.get("function", {}) or {}).get("name")
               types[name] += 1
   ```
3. Classify each tool as **artifact-producing** (`skill_manage`, `patch`, `write_file`, `terminal` *only when it writes* — treat bare `terminal` as read-only unless inspecting command args) vs **read-only** (`read_file`, `search_files`, `terminal`-inspect, `web_search`, `web_extract`, `session_search`).
4. Compare artifact-producing count (and, for skill jobs, the subset that are `skill_manage` with action `create`/`patch`/`edit`) against the job's standing target.

**Drift signature (Mode 3):** final assistant message has all deliverable markers AND artifact-producing count == 0 (or far below target) AND read-only count is high. The agent described work it never executed.

**Healthy signature:** artifact-producing count meets target. A report with zero writes against a nonzero target is drift even if every summary marker is present.

**Mode 3b — honest-zero with completeness rationalization (distinct corrective action):** A variant where the job does NOT narrate fake work, but instead *honestly* reports zero artifacts and self-justifies the skip by declaring its scope "complete." Signature: the output JSON carries `new_skills_recommended: 0, updates_generated: 0` plus a self-reported `shortfall_label` like `"philosophical"` / `"complete"` / `"maintenance-only"` with a reason such as "core pair assessed as complete; no new market signals." The artifact-quantification check still flags it (zero writes, nonzero target), but the **corrective action differs from vanilla Mode 3**:
- Vanilla Mode 3 (dishonest narrative): tell the job to actually *execute* the work it described.
- Mode 3b (honest-zero rationalization): the job genuinely believes there is nothing to do — **re-running produces the same zero**. The fix is to **widen the job's scan scope** (e.g. expand from a single product pair to the full registry/directory) so real candidates exist to synthesize. A standing daily cadence target is incompatible with a "scope is complete" stance; either the scope is too narrow or the target is wrong.
- **Compounding signal:** if a strategic directive expanding scope landed mid-session and the job *acknowledged* it but still shipped zero, that confirms the scope-widening did not take effect in-cycle — the next run must start from the expanded scope, not the narrow one.

Observed Jun 25 on `c37a1090869d`: `new_skills_recommended: 0, updates_generated: 0, shortfall_label: "philosophical"`, despite a fleet-wide scope directive arriving in the same session. Corrective action for the next run: retarget the review profile from `v1-health-review` (single pair) to fleet-wide scope before the daily target of 3+5 is achievable.

**Watchdog framing:** when this is detected, the alert should state the target, the actual artifact count, and the next corrective action (e.g. "next run must synthesize ≥3 candidates from market signals and apply them via skill_manage, not just describe them"). Do not reschedule the job or ask the user — surface the gap and the corrective instruction.

## Missed Schedule Trigger Detection (Mode 4)

Use this when a recurring job has a known cron schedule but you need to verify it actually fired today. Modes 1–3 all require a session to inspect; Mode 4 has no session because the scheduler never invoked the job.

**Recipe (interactive / watchdog):**

1. From `hermes cron list`, extract for each recurring job:
   - `Schedule` (cron expression, e.g. `25 3 * * *`)
   - `Last run` (timestamp)
   - `Next run` (timestamp)
2. Compute the most recent expected trigger time from the cron expression relative to the current time.
   - For daily jobs (`H M * * *`): expected trigger = today at `H:M`. If current time > `H:M` today and `Last run` date < today, the slot was missed.
   - For interval jobs (`every Nh`): if `now - Last run` > N hours, a trigger was missed.
3. Confirm by checking `Next run`: if `Next run` is set to the *next* cycle after today (not today), today's cycle was skipped.
4. **Cluster check**: scan all other jobs in the same time window (±30 min of the missed job's scheduled time). If multiple jobs missed their slots, this indicates a systemic scheduler/gateway outage, not a per-job failure.

**Detection shortcut for daily jobs:** if `Last run` date < today AND `Next run` date > today → missed trigger. This works because the scheduler only rolls `Next run` forward after a slot passes.

**Watchdog framing:** report the missed slot with the date, the expected trigger time, the last actual run, and the corrective action (manual re-run or investigate scheduler/gateway downtime). Note whether other jobs in the same window also missed their slots — clustered misses change the corrective action from "re-run this job" to "investigate why the scheduler was down during that window."

**Observed example (Jun 21, 2026):** `c37a1090869d` (Divinity Health V1 Skill Product Review, `25 3 * * *`):
- Last run: `2026-06-20T03:31:07` (yesterday)
- Next run: `2026-06-22T03:25:00` (tomorrow)
- Today's 03:25 CDT slot: **missed, no session created**
- Other jobs in the 03:00–04:00 window also showed stale last-run timestamps, suggesting a broader scheduler gap around that time.

## Content Substitution Detection (Mode 5)

Use this when a job has run and produced an output file, but the file's content is not the expected deliverable. The agent completed its session successfully but produced output for the wrong task — the prompt was overwritten, drifted, or the model hallucinated a substitute.

**Why Modes 1–4 miss this:** Mode 1 checks status (job is "ok"). Mode 2 checks for stall markers (the file has a complete report). Mode 3 checks artifact counts (the file has substantial content, 38KB+). Mode 4 checks for missed triggers (the job fired). All four pass — the output file exists, is non-empty, and the session completed cleanly. The problem is the *content type*, not the *content existence*.

**Recipe (interactive / watchdog):**

1. **File-size anomaly check (fast signal):** Compare today's output file size against the rolling baseline (last 5–7 runs). A significant deviation (>40% smaller or >60% larger) is suspicious. Observed Jun 28 on `c37a1090869d`: 38KB vs rolling average ~140KB (73% smaller). Size alone is not conclusive (legitimate short cycles exist) but flags the file for deeper inspection.

2. **Structural marker check (definitive):** Grep the output file for expected structural markers specific to the job's deliverable contract. These are the section headers, JSON field names, or report blocks the job MUST produce:
   ```
   grep -c "Skill Product Review" output_file.md
   grep -c "new_skills_recommended" output_file.md
   grep -c "pipeline_status" output_file.md
   ```
   Zero matches on ANY required marker = content substitution confirmed. This is the definitive test — no false positives from legitimate short cycles.

3. **Content inspection (triage):** Read the first 60 lines to identify what the output actually contains. Common substitution patterns:
   - Fleet management strategy documents (agent swapped to organism-level planning instead of skill review)
   - Generic system architecture documents (agent produced a blueprint instead of a targeted review)
   - Re-skills (agent dumped skill-update-engine instructions back as output instead of executing them)

4. **Baseline comparison (severity assessment):** Compare the first 10 lines of today's output against yesterday's known-good output. If the document title, header structure, or opening paragraph is completely different, the substitution is total (not partial).

**Detection shortcut for watchdogs:** For any job with a known deliverable contract (JSON block with specific fields, a required section header, or a report template), a single `grep -c` on a required marker is the fastest definitive check. If the marker count is 0 and the file is non-empty, it's Mode 5.

**Observed example (Jun 28, 2026):** `c37a1090869d` (Divinity Health V1 Skill Product Review):
- Output file: `2026-06-28_03-27-14.md`, 38KB, 433 lines
- File size: 73% below rolling baseline (~140KB) → flagged
- Structural markers: `Skill Product Review` = 0, `new_skills_recommended` = 0, `pipeline_status` = 0 → confirmed
- Content: "the specialist engine Strategy" document (organism-level blueprint, completely off-topic)
- Root cause: prompt drift — the model produced a strategic planning document instead of the daily skill review
- Corrective action: check the cron prompt for job `c37a1090869d` to verify it still contains the skill-update-engine instructions and the V1 health review scope; re-run if the prompt is intact.

**Watchdog framing:** report the gap against the standing target (e.g. "3 new skills + 5 updates = 0/0, full miss") plus the content substitution diagnosis ("output was X, expected Y"). Include the corrective action: verify the prompt hasn't been overwritten, then re-run. Do not attempt to reschedule or fix the prompt — surface the finding.

## Session Data Format (for batch/scripted audits)
Provide a JSON file with structure:
```json
{
  "c37a1090869d": {
    "session_id": "cron_c37a1090869d_20260612_032533",
    "last_message_preview": "We see that the search includes the SKILL.md and all references and the template file. So the templates directory exists and has at least the template file. Now, let's check for scripts and attachments in 8d-snapshot_report.",
    "message_count": 32,
    "ended_at": "2026-06-12 03:30:36"
  }
}
```

## Integration
Run the audit with session data:
```bash
python scripts/audit_cron_fleet.py \
  --input cron_jobs.json \
  --session-data session_data.json \
  --output audit_report.md
```

## Remediation
When a stalled job is detected:
1. Re-run the job manually: `hermes cron run <job_id>` — this completes today's cycle but does NOT prevent recurrence.
2. If it stalls again, check the session for the truncation/error point and identify whether it's the exploration trap (see Root Causes).
3. **For the exploration trap specifically** (the recurring `c37a1090869d` pattern), re-running alone has failed 3× (Jun 12, 14, 15). Apply the permanent fix: edit `skill-update-engine` §11.1 to enforce a reference-file budget (max 3 files per skill in the scan phase unless it's the primary review target) and require the JSON output block to be emitted *before* any deep-dive exploratory tool use. This front-loads the deliverable so a context-budget exhaustion still leaves the cycle's required output intact.
4. Consider reducing scope or increasing token limits for that job (weaker fix; only use if the §11.1 budget isn't applicable).
5. For watchdog jobs: the watchdog itself should detect and alert on this pattern (as implemented in V1 Skill Cycle Watchdog).

## Related Skills
- `v1-skill-cycle-watchdog` — already implements this detection for the V1 Skill Product Review job
- `sibling-agent-bulk-cron-healing` — bulk remediation for erroring/stalled jobs
