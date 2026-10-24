# Philosophical Shortfall Pattern

## Definition

A **philosophical shortfall** occurs when the review engine runs successfully and produces a nominal report, but the output counts (new_skills_recommended, updates_generated) are below target because the skill family being reviewed is **coherent and complete** — not because of a pipeline failure or structural problem.

## When This Occurs

This pattern is expected for **stable, maintenance-phase skill families** where:
- The core skills have reached a stable, coherent state
- No gaps or deficiencies exist in the current implementation
- The engine correctly determines that adding new skills or updates would be artificial
- The edit-first policy is working as designed — the engine finds no genuine gaps requiring new surface area

## Example: Divinity Health V1 Skill Family

The V1 skill family (`8d-pattern-awareness` + `8d-snapshot-report`) has consistently reported:
- new_skills_recommended: 0
- updates_generated: 0
- pipeline_status: "nominal"
- shortfall_label: "philosophical"
- shortfall_reason: "V1 core + support pair assessed as complete; maintenance-only cycle"

This pattern has persisted across multiple consecutive review cycles (2026-07-11, 2026-07-12, 2026-07-13, 2026-07-14) because the family is genuinely complete for its current scope.

## Watchdog Routing Rule

Per skill-update-engine §R15 and §13.2:
- When `shortfall_label == "philosophical"`, the watchdog MUST downgrade the alert to informational (or suppress if `pipeline_status == "nominal"`)
- Daily alerting on philosophical shortfalls is **alert fatigue**
- Escalate only after 3+ consecutive days with the same root cause as a **target-calibration issue**, not a pipeline issue

## Corrective Action Options

When a philosophical shortfall persists, consider:

1. **Target profile revision**: Revise the standing target to match maintenance-phase cadence (e.g., "0 new / 0–2 updates per day" instead of "3 new / 5 updates per day")

2. **Scope expansion**: Expand the review scope to adjacent skill domains beyond the core family being reviewed

3. **Acceptance**: If the family is truly complete, acknowledge that zero-delivery cycles are correct behavior and stop expecting volume from a stable system

## Distinguishing from Structural Shortfalls

| Type | Label | Meaning | Response |
|------|-------|---------|----------|
| Philosophical | `shortfall_label: "philosophical"` | Family is coherent, no genuine gap exists | Downgrade to informational or suppress |
| Structural | `shortfall_label: "structural"` | Scan failed, sources unavailable, model error, or pipeline stall | Alert and investigate |

## JSON Block Format

The engine's report includes a JSON block (Section 13.1 contract) that classifies the shortfall:

```json
{
  "new_skills_recommended": 0,
  "updates_generated": 0,
  "target_profile": "divinity-health-v1-review",
  "shortfall_label": "philosophical",
  "shortfall_reason": "V1 core + support pair assessed as complete; maintenance-only cycle",
  "pipeline_status": "nominal",
  "candidates_unique": 0,
  "patches_shipped": 0
}
```

The watchdog should parse this block and route accordingly — do not treat all zero-count gaps as failures.

## Reference

- skill-update-engine §R15: Target-profile mismatch with edit-first policy
- skill-update-engine §13.1: Engine report output format (required fields)
- skill-update-engine §13.2: Watchdog alert template routing rules