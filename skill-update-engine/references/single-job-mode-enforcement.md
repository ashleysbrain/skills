# Single-Job Mode Enforcement Template

Concrete implementation pattern for review/watchdog jobs that run the entire skill-update-engine pipeline in a single cron job session.

## Problem Recap

Single-job mode runs all pipeline stages (ARBITER → FORGE → SCOUT → NEXUS → PARALLAX → SENTINEL) in one agent session. The session can stall on reference-heavy skills before emitting the required Section 13.1 JSON monitoring block, leaving watchdogs unable to classify the run.

## Mandatory First Output Pattern

**Every single-job session must emit this JSON block as the very first substantive response** (after loading the skill, before any tool calls):

```json
{
  "new_skills_recommended": 0,
  "updates_generated": 0,
  "target_profile": "v1-health-review",
  "shortfall_label": null,
  "shortfall_reason": null,
  "pipeline_status": "nominal",
  "candidates_unique": 0,
  "patches_shipped": 0
}
```

Replace `target_profile` with the active profile name from the cron prompt (e.g., `v1-health-review`, `default-maintenance`).

## Incremental Update Pattern

As the pipeline progresses, update the JSON block by re-emitting it with revised values. Example progression:

```json
// After scan phase: 3 unique candidates found
{
  "new_skills_recommended": 0,
  "updates_generated": 0,
  "target_profile": "v1-health-review",
  "shortfall_label": null,
  "shortfall_reason": null,
  "pipeline_status": "nominal",
  "candidates_unique": 3,
  "patches_shipped": 0
}
```

```json
// After synthesize: 2 updates queued, 1 new skill candidate
{
  "new_skills_recommended": 1,
  "updates_generated": 2,
  "target_profile": "v1-health-review",
  "shortfall_label": null,
  "shortfall_reason": null,
  "pipeline_status": "nominal",
  "candidates_unique": 3,
  "patches_shipped": 0
}
```

```json
// After ship: 1 update applied, 0 new skills (philosophical shortfall)
{
  "new_skills_recommended": 0,
  "updates_generated": 1,
  "target_profile": "v1-health-review",
  "shortfall_label": "philosophical",
  "shortfall_reason": "V1 core + support pair assessed as complete; maintenance-only cycle",
  "pipeline_status": "nominal",
  "candidates_unique": 3,
  "patches_shipped": 1
}
```

## Timebox Implementation (Pseudocode)

```python
# At session start
emit_initial_json_block()

# Phase 1: Scan (max 5 skills, 3 refs each)
scan_results = run_scan_phase(max_skills=5, max_refs_per_skill=3)
update_json(candidates_unique=len(scan_results.unique_candidates))

# Phase 2: Synthesize (max 10 cards)
synthesize_results = run_synthesize_phase(max_cards=10)
update_json(
    new_skills_recommended=synthesize_results.new_skill_count,
    updates_generated=synthesize_results.update_count
)

# Phase 3: Ship
ship_results = run_ship_phase()
update_json(
    patches_shipped=ship_results.applied_count,
    shortfall_label=ship_results.shortfall_label,
    shortfall_reason=ship_results.shortfall_reason
)

# Final emission (redundant but safe)
emit_final_json_block()
```

## Stall Detection Trigger

If at any point the agent detects:
- > 60% of estimated session token budget consumed on reference reading
- No candidates produced after scanning 3+ skills
- Approaching context window limit

**Immediately** emit JSON with current counts and `pipeline_status: "stalled"`, then stop.

## Watchdog Contract Enforcement

The watchdog cron job **must** output exactly one of the four templates from Section 13.2 of the main skill. No custom summaries.

Decision logic for watchdog:
```
IF no session found for today → "Structural shortfall (alert)" template
ELIF session found but no JSON block in output → "JSON block missing (alert)" template
ELIF JSON block present:
    IF pipeline_status == "stalled" → "Structural shortfall (alert)" template
    ELIF shortfall_label == "philosophical" AND pipeline_status == "nominal" → "Philosophical shortfall (informational)" template
    ELIF shortfall_label == "structural" → "Structural shortfall (alert)" template
    ELIF targets fully met → "[SILENT]"
    ELSE → "Structural shortfall (alert)" template (unknown shortfall type)
```

## Recovery Prompt Template

When watchdog detects stalled/missing JSON, re-run review job with:

```
[RESUME FROM SCAN] Previous run stalled/missing JSON. Skip these already-inspected skills: [list skill IDs from previous scan phase]. Resume scan from next uninspected skill. Emit JSON block FIRST.
```

## Cron Wrapper (Optional but Recommended)

Wrap the single-job invocation in a timeout guard that forces JSON emission on exit:

```bash
#!/bin/bash
# single-job-wrapper.sh
# Usage: single-job-wrapper.sh <hermes-command> <job-id> <date>

JOB_ID=$2
DATE=$3
SESSION_PATTERN="cron_${JOB_ID}_${DATE}_*"

# Run with timeout (e.g., 20 min)
timeout 1200 hermes "$1" || true

# Verify JSON block was emitted in session
# (Implement session_search check here)
# If missing, alert via watchdog channel
```

## Checklist for Single-Job Review Jobs

- [ ] Cron prompt instructs: "Emit Section 13.1 JSON block as FIRST output"
- [ ] Target profile name explicitly stated in prompt
- [ ] Reference inspection budget documented (max 3 refs/skill, skip >10 ref skills)
- [ ] Timebox limits stated in prompt
- [ ] Watchdog job uses exact Section 13.2 templates
- [ ] Recovery protocol documented and tested
- [ ] Cron wrapper deployed (optional but recommended)