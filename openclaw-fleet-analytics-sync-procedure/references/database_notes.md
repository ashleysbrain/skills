# Database Notes for Fleet Analytics Sync

## Actual Database Used
The `fleet_analytics.py` script uses `agents.db` located at:
`~/.sibling-agent/workspace/intel/agents/database/agents.db`

Not `fleet_analytics.db` (which remains empty).

## Tables Updated
- `cron_jobs`: Cron job definitions and status
- `cron_runs`: Individual run records
- `error_log`: Error entries
- `fleet_health_snapshots`: Daily health snapshots
- `journal_entries`: Journal compliance tracking
- `agents`: Agent metadata

## Unused Database
`fleet_analytics.db` is not used by the sync script and remains at 0 bytes.

## the operator agent Sessions
The script attempts to access a the operator agent sessions database (`hermes_sessions.db`) which may not exist, causing an error if missing. This is non-fatal and logged as "the operator agent sessions error: no such table: sessions".

## Deprecation Warnings
The script produces multiple `datetime.utcnow()` deprecation warnings. These should be fixed by using timezone-aware objects.
