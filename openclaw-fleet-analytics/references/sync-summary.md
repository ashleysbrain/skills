# OpenClaw Fleet Analytics Sync Summary

This note summarizes the fleet analytics sync process executed by the `fleet_analytics.py` script.

## What the sync does
1. **Cron jobs**: Pulls live cron state from `sibling-agent cron list --json` and updates the `cron_jobs` and `cron_runs` tables.
2. **Sessions**: Syncs the operator agent session data and OpenClaw agent knowledge stores into `agent_sessions`.
3. **Journals**: Scans agent learning-journals for `.md` files and updates `journal_entries`.
4. **Analytics tables**: Runs the `collect-analytics.py` script to populate `task_analytics` and `daily_productivity`.
5. **Health snapshot**: Takes a point-in-time fleet health snapshot stored in `fleet_health_snapshots`.

## Key tables in `agents.db`
- `cron_jobs`: One row per cron job with status (enabled/error/disabled).
- `cron_runs`: Individual run records (success/error) with error_type classification.
- `agent_sessions`: Session logs from the operator agent and agent QMD activity.
- `journal_entries`: Journal compliance tracking.
- `fleet_health_snapshots`: Daily snapshots of agent counts, cron health, errors, sessions, journal compliance.

## Typical output format
The script prints sections:
- ⚡ Syncing cron jobs from OpenClaw...
  - ✓ Synced X cron jobs
- ⚡ Syncing session data...
  - ✓ Synced Y the operator agent sessions / Z agent knowledge stores
- ⚡ Syncing journal compliance...
  - ✓ Indexed A journal entries from B agent dirs
- ⚡ Running analytics collection pipeline...
  - (output from collect-analytics.py)
- ⚡ Taking fleet health snapshot...
  - ✓ Snapshot saved for DATE
    Agents: A active / B total
    Cron: C enabled, D erroring, E disabled
    Errors (24h): F total, G rate limit, H timeout
    Sessions (24h): I
    Journal compliance: J% 

## Interpreting results
- **Status distribution**: Look at cron_jobs.status counts.
- **Model distribution**: Query cron_jobs.model.
- **Top errors**: Query cron_runs where status='error' and group by error_type.
- **Journal compliance**: Percentage of active agents with a journal entry for today.
- **New critical errors**: Compare total errors and timeout/rate_limit counts to previous snapshot.

## Notes
- The script uses UTC timestamps; watch for deprecation warnings about `datetime.utcnow()`.
- If the the operator agent sessions table is missing, the session sync will error but continue.