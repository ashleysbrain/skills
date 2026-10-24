# Watchdog Metrics Extraction Template

Use this template when a watchdog or monitor job must extract delivery counts and pipeline status from a skill update engine run (e.g., Divinity Health V1 Skill Product Review).

## 1. Extraction Sequence

1. Get the cron job entry: use hermes cron list and locate the job by name or ID.
2. Find the most recent session: session_search query = "<job name or ID>" sort=newest limit=1.
3. Read the latest run output: read the session transcript and find the engine’s report section.

## 2. Required Fields to Extract

From the engine’s report, locate the JSON block per §13.1 and extract:

- `new_skills_recommended`: integer (candidate skills synthesized this cycle)
- `updates_generated`: integer (patches, reference additions, manifest fixes)
- `target_profile`: string (active target name for the run)
- `pipeline_status`: one of nominal, degraded, stalled
- `shortfall_label`: required when either count is below target; one of structural or philosophical
- `shortfall_reason`: one-sentence explanation when shortfall_label=philosophical
- `candidates_unique`: integer (after dedup)
- `patches_shipped`: integer (applied this cycle)

If the JSON block is missing, use the manual reconstruction recipe in watchdog-state-db-reconstruction.md. Do not default to zero.

## 3. Compare Against Targets

Use the target_profile’s declared targets (e.g., 3 new skills, 5 updates). Compute the gap for each metric.

## 4. Classify the Gap

- Structural shortfall: engine did not run, scan failed, sources unavailable, model error, or pipeline stall (stalled status, JSON missing, or no candidates). Alert required.
- Philosophical shortfall: engine ran and completed, but the family is complete; edit-first policy correctly found no new-skill gap. Downgrade to informational; escalate only after 3+ consecutive days with the same root cause as a target-calibration issue.

## 5. Alert Rendering (Allowed Deliveries)

- All targets met and pipeline_status=nominal: emit exactly [SILENT] and nothing else.
- Any gap present: use the §13.2 template verbatim for the gap type; include the explicit "Next corrective action".
- JSON block missing: emit the "JSON block missing" template from §13.2 verbatim.
- Do not combine [SILENT] with content.

## 6. Example Use

- For a job with target_profile="v1-health-review" (3 new, 5 updates) and delivered (0, 0) with no JSON block: classify as structural, emit the "JSON block missing" template.
- For a job with delivered (0, 3), shortfall_label=philosophical, pipeline_status=nominal: emit the philosophical shortfall template; do not daily-alert unless >3 consecutive days.

## 7. Cross-References

- §13.1 JSON block contract
- §13.2 Watchdog alert templates
- watchdog-state-db-reconstruction.md
- single-job-mode-enforcement.md