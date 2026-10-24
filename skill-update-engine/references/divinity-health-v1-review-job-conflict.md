# Divinity Health V1 Review Job — Prompt/Skill Conflict

## Problem
The cron job `c37a1090869d` (Divinity Health V1 Skill Product Review) uses the `skill-update-engine` skill but its prompt contains a directive that **directly contradicts** the skill's operating rules.

### Conflicting Directives

| Source | Directive |
|--------|-----------|
| **Review job prompt** (jobs.json, line ~939) | "If there is no meaningful change today, say so clearly and return `[SILENT]`." |
| **skill-update-engine** (§6, line 118; R17) | "The engine must **NEVER** emit `[SILENT]` — it is a producer, not an observer. Even when targets are met, emit the §13.1 JSON block with `pipeline_status: \"nominal\"`. Only the *watchdog* may emit `[SILENT]`." |

## Observed Failure Pattern
- **Recurring stall**: Job runs at 03:25 AM, cron status `ok`, but session contains only the prompt (0 assistant turns)
- **Dates observed**: Jun 12, 14, 16, 18, 22 (5+ consecutive occurrences)
- **Root cause**: Engine receives `[SILENT]` directive → treats it as valid "met target" signal → emits `[SILENT]` → watchdog receives no metrics → reports structural shortfall (0/3 new, 0/5 updates)
- **Secondary stall**: Even when engine runs, it overspends context budget exploring reference files (8d-snapshot-report has 10+ support files) and terminates before synthesizing recommendations (R16)

## Required Fix
The review job prompt must be updated to:
1. **Remove** the `[SILENT]` instruction
2. **Require** the §13.1 JSON block as first substantive output (per §11.1 single-job mode contract)
3. **Enforce** reference inspection budget (max 3 files/skill, skip deep inspection for skills with >10 support files unless primary target)
4. **Timebox** each phase and emit partial JSON with `pipeline_status: "stalled"` if timebox expires

## Watchdog Integration withiwatchdog Behavior (Correct)
The watchdog cron job `31e90033684f` (V1 Skill Cycle Watchdog) correctly:
- Detects missing/zero-output runs
- Classifies shortfall as structural (not philosophical) when JSON block absent
- Uses the exact alert templates from §13.2
- Does not emit `[SILENT]` when targets unmet

## Reference
- skill-update-engine §11.1 (Single-Job Execution Mode)
- skill-update-engine R16 (Single-job execution stall on reference-heavy skills)
- skill-update-engine R17 (Producer/observer confusion: engine emits `[SILENT]`)
- skill-update-engine §13.1 (Engine Report Output Format)
- skill-update-engine §13.2 (Watchdog Alert Template)