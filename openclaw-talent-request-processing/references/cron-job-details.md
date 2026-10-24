# Cron Job Details for Talent Request Processing

## Schedule
The talent request processing cron job runs every 30 minutes (or as defined in OpenClaw cron configuration).

## Execution Steps
1. Check for new talent request markdown files in `~/.sibling-agent/workspace/intel/agents/talent-requests/`.
2. For each file, evaluate against active agents database.
3. Dispatch to existing agent or initiate new agent spawn.
4. Move processed files to `processed/` directory.
5. Run fleet analytics sync script.
6. Update FORGE and ARBITER journals.
7. Commit changes to git workspace.

## Logging
- Output is logged to the OpenClaw system log.
- Any errors are captured and reported in the next heartbeat.

## Related Files
- `SPAWN-TEMPLATE.md`: Template for new agent profiles.
- `fleet_analytics.py`: Script to synchronize fleet data.
- Journal directories: `~/.sibling-agent/workspace/intel/agents/journal/FORGE/` and `.../ARBITER/`.
