# Fleet Analytics Sync Notes for Forge/Arbiter Talent Patrol

During the talent patrol, after processing requests, we run the fleet analytics sync.

Command: `python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync`

Possible errors:
  - Database table missing (e.g., sessions, task_analytics, cron_runs, cron_jobs)
  - These errors may indicate that the Hydra OS database is not initialized or the schema is outdated.

Handling:
  - If the sync fails with database errors, note the errors in the patrol report.
  - Consider the patrol complete otherwise (if talent requests were processed or none found).
  - Do not block the patrol on fleet analytics sync failures unless they indicate a systemic issue that prevents talent request processing.

See also: the fleet analytics sync script may need to be run in the context of a fully initialized OpenClaw/Hydra OS environment.