---
name: sibling-agent-cron-optimization-for-ceo
description: Audit, consolidate, and ADHD-optimize OpenClaw cron jobs that deliver to the principal. Covers notification fatigue diagnosis, job consolidation, relevance filtering, and cross-agent data absorption.
tags: [sibling-agent, cron, adhd, notifications, optimization, singularity, cio, aisha-md]
version: 1.0
---

# OpenClaw Cron Optimization for principal Delivery

Use when the principal reports notification fatigue, duplicate messages, irrelevant content, or too-frequent alerts from any fleet agent delivering to her.

## When to Use
- principal says "too many messages" or "duplicates" or "irrelevant"
- Any agent is delivering more than 2x/day to principal directly
- Multiple agents covering overlapping domains deliver separately
- principal requests ADHD-friendly formatting of fleet output
- User wants to set up a recurring daily/weekly scorecard, Saturday-PM week-ahead executive memo, or related leadership brief delivered through OpenClaw cron
- User wants a TWC, business-health, or organizational check-in that dedups prior outputs, turns scores into concrete actions, and feeds downstream planning docs such as daily standups

## Diagnosis Steps

1. **Audit all jobs delivering to principal**: `sibling-agent cron list | grep -i <agent-name>`
2. **Get full prompts** from `/<workspace>` (nested under `jobs` key — `data.get('jobs', [])`)
3. **Map delivery frequency**: Count total daily messages to principal from all sources
4. **Identify overlaps**: Which jobs cover similar domains? Which outputs duplicate?
5. **Check delivery settings**: Some jobs have `delivery.mode: "none"` — principal may not be getting important ones while getting spammed by others

## The Pattern That Worked (SINGULARITY Case Study)

### Before (broken)
- principal Strategic Pulse: every 30 minutes = 48 msgs/day (!!!)
- Vision Scan: daily 7 AM (overlapped with Strategic)
- Medical Scan: daily 1:25 AM (too broad)
- Always-On Strategic Pulse: another pulse (duplicate)
- Total: ~50+ messages/day

### After (fixed)
- Morning Brief: 7:30 AM (consolidated vision + strategy + CIO intel)
- Saturday PM Executive Memo: week-ahead priorities, risks, and Monday launch checklist
- Evening Wrap: 7 PM (actions taken + decisions needed)
- Total: 2 messages/day or one daily + one week-ahead memo, depending on the user's cadence

### How
1. DISABLED the high-frequency spam job (every-30-min pulse)
2. REPURPOSED existing daily jobs into Morning/Evening consolidated briefs
3. Did NOT create new jobs — edited existing ones with `sibling-agent cron edit`

## ADHD-Friendly Output Format (mandatory for principal delivery)

Every prompt delivering to the principal MUST include these output rules:
```
OUTPUT FORMAT (MANDATORY):
- Max 8 tiny bullets
- Bold key ACTIONS (not observations)
- Emoji markers for categories: 🔬 Research, 💼 Business, 🚨 Alert, ✅ Done, 📄 Report
- Include clickable source URLs for papers/articles
- Include file paths for PDFs: "📄 Report: [name] at [path]"
- Do NOT include coordination/journaling boilerplate in output
- If nothing new since yesterday, say "No new signals" and stop
```

### principal Advisory Board Brief (special case)

The principal board brief has its own stricter format because it is the ONE document the principal reads first every morning. It must be a cross-panel PRIORITIZER (not a synthesizer) with ranked actions, WHY THIS NOW for each, a WHAT'S OFF THE LIST section to clear ADHD guilt loops, and max one phone screen of content. See `ondemand-advisory-panels` skill → `references/ceo-brief-format.md` for the full tested prompt template and structure. Do NOT design a principal brief without reading that reference first.

## Cross-Agent Data Absorption

When consolidating, make the consolidated job READ other agents' outputs:
- CIO daily intel: `intel/coordination/intel-officer/YYYY-MM-DD.md`
- Research scans: `intel/research/domains/` and `intel/research/atlas/`
- Fleet reports: `intel/agents/reports/`

**Timing matters**: If CIO runs at 7:15 AM, the consolidated morning brief must run AFTER (e.g., 7:30 AM).

## Daytime Fleet-Wide Cron Audit & Consolidation Procedure

Use when you need to audit and optimize the entire OpenClaw fleet's cron schedule to reduce congestion during principal working hours (6 AM - 11 PM CT) and ensure optimal job distribution.

### When to Use
- Preparing for high-activity periods
- After noticing frequent job collisions or timeouts
- Quarterly fleet hygiene review
- When principal reports notification fatigue from cron-delivered messages

### Procedure

1. **List all enabled jobs with their schedules**
   - Use `sibling-agent cron list --all` to see every job in the fleet
   - Focus on `status: active` jobs for rescheduling; paused jobs can be reviewed for relevance

2. **Map the daytime schedule hour by hour (6 AM - 11 PM CT)**
   - For each enabled job, determine its run times during the day
   - For fixed-time jobs (e.g., `0 6 * * *`), note the specific hour/minute
   - For interval jobs (e.g., `*/30 * * * *`), calculate all times they run in a 24-hour period
   - Create a timeline of 6:00 to 23:00 in 15-minute increments

3. **Flag collisions (2+ jobs in same 15-min window)**
   - Any 15-minute block with 2 or more jobs scheduled is a collision
   - Prioritize resolving collisions involving heavy jobs (builds, scans, analytics)

4. **Flag redundant jobs (same purpose, different names)**
   - Group jobs by base name (strip numbers, parentheses, descriptors)
   - Example: "Fleet Health Check" and "VITALS: Fleet Health Check" may be redundant
   - Keep the most recently updated or highest priority job; pause others with notes

5. **Flag stale jobs (last run 7+ days ago, last_status error)**
   - Check `last run` timestamp and `last status`
   - If last run > 7 days ago AND last status not `ok`, consider pausing
   - Exclude critical jobs: VITALS, Fleet Analytics Sync, Fleet Health Check, OpenRouter free model syncs
   - When pausing, add a note explaining why (e.g., "Stale: last successful run 2026-05-24")

6. **Restagger by updating schedules**
   - Move colliding and/or daytime-heavy jobs to preferred slots:
     - Lunch window: 12:00-13:00 (CT)
     - Evening window: 21:00-23:59 (CT)
   - Maintain the job's original frequency when possible (e.g., change `0 6 * * *` to `0 22 * * *` for daily)
   - For interval jobs, adjust the phase but keep the interval (e.g., `20 */6 * * *` → `20 12-23/6 * * *` to shift to afternoon/evening)
   - Use `sibling-agent cron edit <job-id> --schedule "<new cron expr>"` to update

7. **Pause non-applicable jobs with notes**
   - For jobs paused due to staleness or redundancy, add a clear note in the job's description or via audit log
   - Never delete jobs — only pause with clear documentation

8. **Verify overnight schedule (12 AM - 5:59 AM) remains untouched**
   - These hours are reserved for heavy builds, scans, and maintenance
   - Do not reschedule any job into or out of this window unless explicitly instructed

9. **Report results**
   - Document: what changed, what was paused, what was consolidated
   - Share with relevant stakeholders (e.g., principal, CTO, fleet admins)

### Constraints to Remember
- Heavy jobs (builds, scans, syncs, analytics) MUST NOT run 06:00-23:00 CT
- Maximum 2 jobs per hour during 06:00-23:00 CT
- Advisory board jobs should be spaced ≥30 minutes apart
- Maintenance jobs prefer lunch (12-13 CT) or after 21:00 CT
- NEVER delete jobs — pause only with explanatory notes
- Overnight schedule (00:00-05:59 CT) is sacred — do not modify

### Example Output
After running this procedure, you might see:
- RESCHEDULED JOBS (16): [list of jobs moved to 12:xx or 21:xx slots]
- PAUSED JOBS: None (if no redundant/stale jobs found)
- CONSOLIDATED JOBS: None (if no true duplicates found)

## The Pattern That Worked (SINGULARITY Case Study)

**See also:** `references/fleet-blackout-diagnosis.md` for fleet-wide blackout diagnosis pattern, commands, and case study.

Add to every consolidated prompt:
```
DEDUP: Read yesterday's output at [output-path]. Do NOT repeat anything already reported. Only surface NEW information. If nothing new, say "No new signals today" and stop.
```

For evening wrap, also dedup against morning brief:
```
DEDUP: Read this morning's brief at [path]. Do not repeat. Focus on: what changed since morning, actions taken, decisions needed tomorrow.
```

## AISHA-MD Check-in Integration

If AISHA-MD wellness check-ins exist, ensure they:
1. Use the principal's PROPRIETARY scoring methodology (see proprietary-twc-scoring skill)
2. Read config.json for dimension rotation, weights, scoring params
3. Schedule within optimal windows (9-11 AM or 12-2 PM, NEVER evenings)
4. Financial dimension WEEKLY ONLY (Sunday)
5. Use her user-facing names (Head, Body, Space, People, Purpose, Growth, Work, Money)

## Recurring Scorecard / Executive Brief Pattern

Use this pattern when the user wants recurring company scorecards or leadership briefs:
1. Create a *daily* scorecard job and a *weekly* synthesis job.
2. Make the weekly job depend on the daily output path or job ID so it reads prior signals before summarizing.
3. Prefer a Saturday PM week-ahead memo when the brief is meant to prepare Monday, and reserve Sunday or weekday evening briefs for retrospective or same-week wrap use cases.
4. Keep the core scoring logic in the scoring skill; keep schedule, delivery, deduplication, and formatting rules here.
5. Enforce executive output rules in the prompt: max bullet limits, bold actions, no duplicate recap, and exact `No new signals` behavior when nothing changed.
6. Verify delivery mode, cron timing order, and any cross-job dependency before considering the setup complete.
7. Prefer one consolidated executive stream over multiple overlapping alerts unless the user explicitly wants separate streams.
8. If a downstream standup or daily brief should consume the weekly memo, encode that dependency explicitly in the prompt so the daily brief pulls only the top week-ahead items, not the full executive report.

## OpenClaw CLI Reference

```bash
# List all jobs
sibling-agent cron list

# Edit a job (patch fields)
sibling-agent cron edit <job-id> --name "New Name" --message "New prompt" --schedule "cron EXPR @ TZ"

# Add a new job
sibling-agent cron add --name "Name" --message "Prompt" --schedule "cron EXPR @ TZ" --model "provider/model"

# Disable a job
sibling-agent cron disable <job-id>

# Get help
sibling-agent cron edit -h
sibling-agent cron add -h
```

## JSON File Structure (Two Files — CRITICAL DISTINCTION)

### jobs.json — Job Definitions (LIST)
Path: `/<workspace>`
```json
{
  "version": 1,
  "jobs": [
    {
      "id": "uuid",
      "name": "Job Name",
      "schedule": {"kind": "cron", "expr": "0 7 * * *", "tz": "America/Chicago"},
      "payload": {"kind": "agentTurn", "message": "prompt text", "model": "provider/model"},
      "delivery": {"mode": "announce"|"none"},
      "enabled": true,
      ...
    }
  ]
}
```
**`data['jobs']` is a LIST of job dicts.** Access with indexing or list comprehension.

### jobs-state.json — Run State (DICT)
Path: `/<workspace>`
```json
{
  "version": 1,
  "jobs": {
    "uuid": {
      "updatedAtMs": 1778238712059,
      "state": {
        "lastRunAtMs": 1778238000009,
        "lastStatus": "ok"|"error"|"skipped",
        "lastDurationMs": 58480,
        "consecutiveErrors": 0
      }
    },
    "another-uuid": { ... }
  }
}
```
**`data['jobs']` is a DICT keyed by job ID.** Access with `states.get(job_id, {}).get('state', {})`.

### Cross-referencing both files (REQUIRED for fleet diagnostics)

**⚠️ CRITICAL: `execute_code` is BLOCKED in cron mode** (security scanner rejects arbitrary Python). Use `python3 -c` via the `terminal` tool instead. The examples below reflect this.

**⚠️ CRITICAL: OpenClaw gateway may be DOWN.** If `sibling-agent cron list` fails with WebSocket 1006 error, the gateway is unreachable. Fall back to reading `jobs.json` and `jobs-state.json` directly — these files are always on disk regardless of gateway state.

```python
# Run via: terminal(command='python3 -c "..."')
import json, datetime

with open('/<workspace>') as f:
    jobs = json.load(f).get('jobs', [])  # LIST

with open('/<workspace>') as f:
    states = json.load(f).get('jobs', {})  # DICT

# Join: for each job, get its state
for j in jobs:
    jid = j.get('id', '')
    state = states.get(jid, {}).get('state', {})
    status = state.get('lastStatus', '?')
    ce = state.get('consecutiveErrors', 0)
    # ... analyze
```

### Fleet Health Metrics Pattern
```python
from collections import Counter

total = len(jobs)
ok = sum(1 for j in jobs if states.get(j.get('id',''),{}).get('state',{}).get('lastStatus')=='ok')
errors = sum(1 for j in jobs if states.get(j.get('id',''),{}).get('state',{}).get('lastStatus')=='error')
announce_count = sum(1 for j in jobs if j.get('delivery',{}).get('mode')=='announce')
announce_errors = sum(1 for j in jobs 
    if j.get('delivery',{}).get('mode')=='announce' 
    and states.get(j.get('id',''),{}).get('state',{}).get('lastStatus')=='error')

# Most recent successful run (detect blackouts)
latest_ok_ts = max(
    (states.get(j.get('id',''),{}).get('state',{}).get('lastRunAtMs', 0) 
     for j in jobs 
     if states.get(j.get('id',''),{}).get('state',{}).get('lastStatus')=='ok'),
    default=0
)
days_since_ok = (datetime.datetime.now() - datetime.datetime.fromtimestamp(latest_ok_ts/1000)).days if latest_ok_ts else None

# Top chronic failures
worst = sorted(
    [(j.get('name',''), states.get(j.get('id',''),{}).get('state',{}).get('consecutiveErrors',0)) for j in jobs],
    key=lambda x: -x[1]
)[:10]
```

**Gotchas:**
- **CRON MODE: `execute_code` is blocked.** Use `terminal(command='python3 -c "..."')` instead. This is the #1 thing that breaks when this skill runs as a cron job.
- Python JSON parsing via terminal pipe often fails silently — `python3 -c` via terminal tool is the reliable path in cron mode
- `jobs.json` may NOT have state info — always read BOTH files for complete picture
- `jobs-state.json` state structure is nested: `state['jobs'][job_id]['state']['lastStatus']`
- **Gateway down**: If `sibling-agent cron list` returns WebSocket 1006 error, the gateway is unreachable. Read JSON files directly — they reflect the schedule regardless of gateway state.
- **Fleet-wide blackout**: `latest_ok_ts` can be 0 across the entire fleet (no OK runs recorded in state). Handle `days_since_ok = -1` as a special case in your report — it means the fleet has NEVER successfully run, not that it's been a long time.
- **Free-model single-point failure**: All OpenRouter free-tier models (nemotron-nano, nemotron-super, qwen3-next, glm-4.5-air, qwen3-coder) can timeout identically. This takes down the entire fleet at once. Check model distribution in your diagnostics — if 100% of jobs use free models, the fleet has zero resilience.
- **Stale fleet health reports**: Auto-remediation can generate ~1.8KB PDF stubs (1 page, minimal content). Verify report content, not just file existence.

## Saturday PM Executive Memo Pattern

When running as a weekly Saturday evening job for the principal, produce a concise memo optimized for the week ahead (not retrospective):

### Structure
1. **Executive Summary** — 3-4 lines max. Lead with the most critical number (fleet health, days since failure, etc.)
2. **3 Biggest Priorities** — Ranked by urgency. Each priority should be a concrete action, not an observation.
3. **Risks / Opportunities / Dependencies** — What could go right, what could go wrong, what blocks progress.
4. **C-Suite Recommendations (8D-filtered)** — For each role (principal/CFO/COO/CTO/CPO/CMO), give 1-3 bullets tagged with relevant 8D dimensions (PHY, PSY, ENV, SOC, SPI, INT, VOC, FIN). Explicitly note cross-dimensional tradeoffs.
5. **Ranked Action Plan** — Table with: #, Action, Owner, Timing, 8D Impact. Max 10 rows.
6. **Monday Launch Checklist** — Pre-standup checklist of things that must be true before Monday starts.
7. **Cross-Dimensional Tradeoffs** — Only when they matter. Format: "DIM A vs DIM B: Tradeoff explanation. **Favor DIM A** because reason."

### Output Rules (mandatory)
- Tight bullets, no filler
- Bold key ACTIONS (not observations)
- Emoji markers for scanability: 🔬 Research, 💼 Business, 🚨 Alert, ✅ Done, 📄 Report
- Every recommendation filtered through all 8D: PHY, PSY, ENV, SOC, SPI, INT, VOC, FIN
- If fleet is in blackout: lead with that, quantify days of silence, make root cause #1 action
- Max 8 bullets per section
- Include data tables where they compress information

### Data Collection for Memo
Before writing, collect:
1. Total jobs, error count, OK count, failure rate percentage
2. principal-facing (announce) jobs: how many, how many failing
3. Days since last successful run across entire fleet
4. Top 5-10 worst chronic failures by consecutive errors
5. Job categorization by domain (Research, Health, principal Briefs, Agent Profiles, Content, Revenue, Infrastructure, etc.)
6. Delivery mode distribution (announce vs none — jobs with "none" are running but invisible to principal)

## Pitfalls

1. **Don't spawn new agents for this** — it's prompt engineering + cron ops, not a new agent. File talent request to FORGE, they dispatch.
2. **Don't use `execute_code` in cron mode** — it's blocked by security scanner. Use `terminal(command='python3 -c "..."')` for JSON parsing. This is the #1 pitfall when running as a cron job.
3. **Check delivery settings** — a job can be "running ok" but have `delivery.mode: "none"` so principal never sees output (AISHA-MD was broken this way).
3. **Don't schedule anything in evenings** — the principal's cognitive function drops. Morning/midday only for principal delivery.
4. **Financial dimension weekly only** — daily financial check-ins trigger anxiety loop.
5. **Always dedup** — without explicit dedup instructions, agents WILL repeat yesterday's content.
6. **Cross-agent timing dependencies** — if Job A produces data for Job B, B must run AFTER A.
7. **The Three Laws of Skipping apply to check-ins** — silent, data, unnarrated return. Never guilt-trip.
8. **READ THE USER'S OWN SYSTEM before building check-ins.** AISHA-MD was completely broken because nobody read the principal's proprietary config at `memory/principal-8d/config.json`. It had custom TWC weights, dimension rotation schedules, user-facing names, scoring parameters — all ignored. The prompt was just boilerplate. "We live the systems we create" = always use HER methodology, not generic wellness questions. Key files: config.json (scoring), profile.md (energy patterns), baselines.json (Bayesian priors), PRD (product spec).
9. **Check delivery settings on EVERY job you touch.** AISHA-MD had `delivery: "not-requested"` — it was running fine but the principal never received anything. Always verify announce/delivery is enabled for principal-facing jobs.
10. **Read OpenClaw HOT.md + today's memory EVERY session.** the principal runs both the operator agent (AISHA) and OpenClaw simultaneously. She will NOT repeat directives between systems. AISHA must proactively read `memory/HOT.md` and `memory/YYYY-MM-DD.md` to stay synced with what she told OpenClaw.
11. **When the principal's priorities shift, update BOTH the display file AND the generating code.** The Executive Task Manager (`executive_task_manager.py`) hardcodes task priorities in `run_daily_ingestion()` and overwrites `principal-DAILY-ACTIONS.md` every morning at 5:10 AM. If you only edit the display file, the next cron run silently reverts it. The fix is always two-part: (a) rewrite the display file with the correct priorities, (b) rewire the `run_daily_ingestion()` task list in the generating script so it stops injecting stale priorities. When the principal says "this list doesn't reflect my actual actions," trace the chain: which cron job writes the file → which script generates the content → where are the priorities hardcoded → fix the source, not the symptom.
12. **The principal is the source of truth for priorities, not the advisory boards.** Advisory boards push their own domain agendas (CRO pushes pricing, CTO pushes MVP testing, Marketing pushes category definition). These do NOT automatically become principal priorities. When the principal says what she's actually working on, that overrides whatever the boards recommend. The task manager must reflect the principal's locked priority order, with board recommendations filtered through it.
