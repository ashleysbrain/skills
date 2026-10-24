# 8d-snapshot-report Stall Pattern — Observed Failure & Remediation

## Context
This reference documents a **repeatedly observed failure mode** in the Divinity Health V1 Skill Product Review job (`c37a1090869d`) when running the skill update engine in single-job mode.

## Failure Signature

| Attribute | Value |
|-----------|-------|
| **Job ID** | `c37a1090869d` |
| **Job Name** | Divinity Health V1 Skill Product Review |
| **Schedule** | `25 3 * * *` (03:25 AM CDT daily) |
| **Skills Loaded** | `skill-update-engine`, `open-core-skill-architecture`, `hermes-agent` |
| **Stall Point** | Inspecting `8d-snapshot-report` references (8 refs + 1 template + 1 script = 10 support files) |
| **Session ID Pattern** | `cron_c37a1090869d_YYYYMMDD_HHMMSS` |
| **Observed Stall Time** | ~03:30:36 CDT (≈5 min after start) |
| **Cron Status** | Shows "ok" — false green |
| **Watchdog Job** | `31e90033684f` (V1 Skill Cycle Watchdog) |

## Root Cause
The `8d-snapshot-report` skill has **10 support files** across `references/`, `templates/`, and `scripts/`. In single-job mode, the engine's scan phase attempts to read all reference files for each skill inspected. When `8d-snapshot-report` is encountered, the reference inspection budget is exceeded, the session hits token/time limits, and the agent terminates **before emitting the required JSON monitoring block** (per §13.1 contract).

## Observed Watchdog Behavior
The watchdog (`31e90033684f`) ran **6 times** on 2026-06-12 (06:05, 10:05, 12:05, 14:05, 16:05, 18:05 CDT). Each run:
- Correctly identified the stall (session ended mid-execution at 03:30:36)
- Reported structural shortfall: 0/3 new skills, 0/5 updates
- Recommended corrective action: `hermes cron run c37a1090869d`
- **Did not emit the required JSON block** — output was human-readable only
- Classified as "structural" shortfall (pipeline stall) but without machine-parseable evidence

## Required JSON Block (Missing in All Runs)
Per §13.1, the engine **must** emit this block even when stalled:

```json
{
  "new_skills_recommended": 0,
  "updates_generated": 0,
  "target_profile": "v1-health-review",
  "shortfall_label": "structural",
  "shortfall_reason": "Single-job execution stalled on 8d-snapshot-report reference inspection (10 support files); session terminated before candidate synthesis",
  "pipeline_status": "stalled",
  "candidates_unique": 0,
  "patches_shipped": 0
}
```

## Remediation Protocol

### Immediate (when watchdog alerts)
1. **Re-run with resume hint**: `hermes cron run c37a1090869d` with prompt: "Resume from scan phase; skip already-inspected skills including 8d-snapshot-report"
2. **Verify JSON block emission**: Confirm the re-run emits the §13.1 JSON block before any narrative output

### Short-term (next review cycle)
1. **Add timeboxing** to the review job prompt per §11.1 mitigations:
   - Scan phase: max 5 skill inspections, max 3 reference files per skill
   - Emit JSON block **first** (as early output), then proceed
   - If >60% session budget spent on reference reading without candidates → abort, emit JSON with `pipeline_status: "stalled"`
2. **Add reference-file budget**: Skip deep inspection for skills with >10 support files unless primary target

### Structural (pipeline redesign)
1. **Migrate to native multi-stage pipeline**: Split into separate cron jobs per role (ARBITER → FORGE → SCOUT → NEXUS → PARALLAX → SENTINEL) as designed in §11
2. **Stagger cron minute offsets** per §6 (cron-schedule-spacing.md) to prevent collision
3. **Pin engine cron jobs to paid fallback model** per Risk R1 (free model volatility)

## Watchdog Contract Compliance Gap
The watchdog job `31e90033684f` should:
- Emit the **exact alert templates** from `watchdog-monitoring-pattern.md`
- For structural shortfall: use the "Structural shortfall (alert)" template
- For philosophical shortfall: downgrade to informational (no daily alert) per R15
- **Parse the engine's JSON block** for `shortfall_label` — if `philosophical`, suppress daily alert after 3+ consecutive days with same root cause

## Related Files
- `skill-update-engine/SKILL.md` §11.1 (Single-Job Execution Mode)
- `skill-update-engine/SKILL.md` Risk R16 (Single-job execution stall on reference-heavy skills)
- `references/watchdog-monitoring-pattern.md` (JSON block format & alert templates)
- `references/cron-schedule-spacing.md` (stagger offsets)
- `8d-snapshot-report` skill (10 support files — primary stall trigger)

## Recurrence Log
| Date | Watchdog Runs | Review Job Status | Gap | Action Taken |
|------|---------------|-------------------|-----|--------------|
| 2026-06-12 | 6 (06:05–18:05) | Stalled at 03:30:36 | 0/3 new, 0/5 updates | None — alert only |
| 2026-06-11 | — | Completed 03:43 but short | 0/3 new, 1/5 updates | — |
| **2026-06-13** | **1 (08:09)** | **Completed 03:42, status "ok"** | **0/3 new, 1/5 updates** | **Watchdog emitted custom format (not exact template); engine JSON block still missing** |
| **2026-06-14** | **1 (03:25 AM start)** | **Stalled — session `cron_c37a1090869d_20260614_032512` contains only initial prompt, no assistant output** | **0/3 new, 0/5 updates** | **Watchdog reported structural shortfall; same stall point as 06-12** |

---
*Added 2026-06-12 after 6 watchdog cycles observed identical structural stall on 8d-snapshot-report references. Updated 2026-06-13 — job completed but JSON block contract still violated; watchdog output format non-compliant. Updated 2026-06-14 — 3rd consecutive day of same stall pattern (06-12 stalled, 06-13 completed but no JSON, 06-14 stalled again). This pattern will persist until single-job timeboxing or multi-stage migration is implemented.*