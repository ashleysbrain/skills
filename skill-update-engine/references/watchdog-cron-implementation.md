# Watchdog Cron Job Implementation — V1 Skill Cycle Watchdog

This document specifies the exact implementation for the watchdog cron job (`31e90033684f`) that monitors the Divinity Health V1 Skill Product Review job (`c37a1090869d`).

## Cron Job Configuration

| Field | Value |
|-------|-------|
| **Job ID** | `31e90033684f` |
| **Name** | V1 Skill Cycle Watchdog |
| **Schedule** | `5 */2 * * *` (every 2 hours at :05) |
| **Target Job** | `c37a1090869d` (Divinity Health V1 Skill Product Review) |
| **Target Schedule** | `25 3 * * *` (03:25 AM CDT daily) |
| **Target Profile** | `v1-health-review` |
| **Deliver** | `origin` |

## Required Prompt for Watchdog Cron Job

The watchdog cron job **must** use this exact prompt structure:

```
[IMPORTANT: You are running as a scheduled cron job. DELIVERY: Your final response will be automatically delivered to the user — do NOT use send_message or try to deliver the output yourself. Just produce your report/output as your final response and the system handles the rest. SILENT: If there is genuinely nothing new to report, respond with exactly "[SILENT]" (nothing else) to suppress delivery. Never combine [SILENT] with content — either report your findings normally, or say [SILENT] and nothing more.]

You are a watchdog for the Divinity Health V1 Skill Product Review cycle.

Your job throughout the day:
- Check whether the daily review job `c37a1090869d` has run and whether the latest output is consistent with the standing target:
  - 3 recommended new skills per day
  - 5 updates per day total
- Use session_search and/or cronjob list to inspect the latest run/output for the review job.
- Compare the current day's status against the target and report only actionable drift.
- If the cycle is on track and there is nothing to report, output exactly `[SILENT]`.
- If the review job has not run yet, if the output is missing, or if the day is short on the target counts, output a concise alert with the gap and the next corrective action.
- Do not reschedule jobs or ask the user questions.
- Do not mention internal chain-of-thought.
- Keep the output concise and user-facing.
```

## Required Output Format (MANDATORY)

The watchdog **must** emit output matching one of the four templates from `references/watchdog-monitoring-pattern.md` exactly. No custom formats.

### Decision Logic

1. **Retrieve review job session**: Use `session_search` with query `cron_c37a1090869d` sorted newest.
2. **Check for engine JSON block**: Look for the §13.1 JSON block in the review job's output.
3. **Classify shortfall**:
   - If JSON block present: read `shortfall_label` (`structural` or `philosophical`)
   - If JSON block missing: classify as `JSON block missing` (contract violation)
   - If review job not run: classify as `not run`
4. **Emit matching template**:
   - Targets fully met → `[SILENT]`
   - Structural shortfall → Structural shortfall (alert) template
   - Philosophical shortfall → Philosophical shortfall (informational) template
   - JSON block missing → JSON block missing (alert) template
   - Job not run → Structural shortfall (alert) template with "not run"

### Template Parameters

| Parameter | Source |
|-----------|--------|
| `<job_id>` | `c37a1090869d` |
| `<date>` | Today's date (YYYY-MM-DD) |
| `<time>` | Review job's actual run time from cron list / session |
| `shortfall_reason` | From engine JSON block, or inferred: "Single-job execution stalled on reference-heavy skill" / "Family reviewed as coherent; maintenance-only cycle" / "Engine did not emit required JSON block" |
| Delivered counts | From engine JSON block (`new_skills_recommended`, `updates_generated`), or manual extraction if JSON missing |

## Today's Run Analysis (2026-06-13)

| Aspect | Observation |
|--------|-------------|
| Review job run | Yes, 03:25–03:42 AM CDT, status "ok" |
| Engine JSON block emitted | **No** — contract violation |
| New skills delivered | 0 (target 3) |
| Updates delivered | 1 (target 5) — version fix in `8d-snapshot-report/references/release-positioning.md` |
| Pipeline status | Completed but short; deep reference inspection (24 files in 8d-pattern-awareness, 8 in 8d-snapshot-report) |
| Shortfall classification | **Cannot auto-classify** — JSON block missing |

### Required Watchdog Output for Today

Since the engine JSON block is missing, the watchdog **must** emit the "JSON block missing (alert — contract violation)" template:

```
The review job `c37a1090869d` ran but the engine report did not emit the required JSON block (section 13.1 contract). Watchdog cannot auto-classify shortfall.

**Manual inspection required:** Retrieve the session `cron_c37a1090869d_20260613_032526` and extract counts by hand.
```

## Compliance Checklist for Watchdog Runs

- [ ] Uses exact prompt structure above
- [ ] Retrieves latest review job session via `session_search`
- [ ] Checks for engine JSON block (§13.1) in review job output
- [ ] Classifies shortfall using `shortfall_label` if JSON present
- [ ] Emits **exactly one** of the four templates from `watchdog-monitoring-pattern.md`
- [ ] No custom formatting, no extra narrative, no chain-of-thought
- [ ] Outputs `[SILENT]` only when targets fully met (both counts at or above target)

## Remediation for Review Job

The review job (`c37a1090869d`) must be updated to:

1. **Emit JSON block first** (per §11.1 mitigation #2) — before any narrative output
2. **Timebox scan phase** — max 5 skill inspections, max 3 reference files per skill
3. **Add stall detection** — if >60% session budget on reference reading without candidates, abort and emit JSON with `pipeline_status: "stalled"`
4. **Migrate to multi-stage pipeline** (long-term) — separate cron jobs per role per §11 design

## Related Files

- `skill-update-engine/SKILL.md` §11.1 (Single-Job Execution Mode), §13.1 (Engine Report Output Format), §13.2 (Watchdog Alert Template)
- `references/watchdog-monitoring-pattern.md` (JSON block format & alert templates)
- `references/8d-snapshot-report-stall-pattern.md` (observed stall root cause)
- `references/cron-output-retrieval.md` (session lookup procedure)
- `references/single-job-mode-enforcement.md` (concrete implementation template for single-job mode)