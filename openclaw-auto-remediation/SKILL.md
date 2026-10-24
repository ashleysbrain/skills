---
name: sibling-agent-auto-remediation
description: Run the closed-loop auto-remediation cycle for OpenClaw agent fleet.
category: devops
---

# OpenClaw Auto-Remediation Skill

This skill provides a procedure to run the closed-loop auto-remediation cycle for the OpenClaw agent fleet, as performed by NEXUS (E-026).

## Steps

1. Sync live data: Run `python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync` before executing this skill
2. Auto-fix errors: 
   - List cron jobs: `sibling-agent cron list --json`
   - For each job with consecutiveErrors >= 3:
     * If error is rate_limit and model is anthropic/claude-sonnet-4-6:
         - For Scan jobs: switch to google/gemini-2.5-flash
         - For Brief jobs: switch to anthropic/claude-haiku-4-5
         - Otherwise: switch to google/gemini-2.5-flash
     * If error is timeout: increase timeout to 1200 seconds (only if current timeout < 1200)
3. Auto-spread load: 
   - Count jobs per model (from the payload.model field)
   - If any model has >40 active jobs, redistribute the lowest-priority ones (highest consecutiveErrors) to alternative models.
4. Cost optimization:
   - Check for expensive models (opus) on simple tasks (Scan, Brief, backup) and migrate to sonnet tiers.
5. Predictive: 
   - Check for agents with declining performance (3+ consecutive runs slower than average)
   - Skipped if historical performance data is not available in task_analytics table
6. Data reconciliation: 
   - Handled by the fleet analytics sync step (syncs agent knowledge stores)
7. Update fleet health snapshot: 
   - Done during the sync step

## Notes

- The script assumes the OpenClaw CLI is available and the user has appropriate permissions.
- The JSON structure of `sibling-agent cron list --json` is expected to be an object with a key "jobs" containing an array of job objects.
- Each job object has: `id`, `name`, `enabled`, `payload` (contains `model`, `timeoutSeconds`), `status`, and a nested `state` object.
- **Error data is nested inside `state`**: `state.consecutiveErrors`, `state.lastRunStatus`, `state.lastDiagnostics.summary`. Top-level `consecutiveErrors` and `lastRunStatus` fields do NOT exist on the job object. Always access via `j.get('state', {}).get('consecutiveErrors')`.
- The top-level `status` field IS present and valid (\\\"error\\\", \\\"idle\\\", etc.).
- The timeout fix only applies if the current timeout is less than 1200 seconds to avoid unnecessary updates.
- Error type descriptions: see `references/error_types.md`
## Change Log
## Change Log

## Change Log\n\n- 2026-06-11: Initial version based on NESUS (E-026) auto-remediation cycle.\n- 2026-06-12: \n  - Updated script to properly access nested state fields for error data\n  - Added check to only increase timeout if current timeout < 1200 seconds\n  - Clarified that fleet analytics sync should be run before executing the skill\n  - Improved predictive step documentation to note data requirements\n  - Enhanced error handling and logging throughout the script\n  - Fixed timeout fix to use --timeout-seconds instead of --timeout in the script
- 2026-06-12: 
  - Updated script to properly access nested state fields for error data
  - Added check to only increase timeout if current timeout < 1200 seconds
  - Clarified that fleet analytics sync should be run before executing the skill
  - Improved predictive step documentation to note data requirements
  - Enhanced error handling and logging throughout the script

## Scripts

- `scripts/auto_remediation.py`: A Python script that implements the auto-remediation cycle with improved error handling and timeout logic.