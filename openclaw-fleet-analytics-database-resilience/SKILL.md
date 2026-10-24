---
name: sibling-agent-fleet-analytics-database-resilience
description: Skill for making the OpenClaw fleet analytics sync resilient to database schema issues.
---
# OpenClaw Fleet Analytics Database Resilience

Skill for making the OpenClaw fleet analytics sync resilient to database schema issues, particularly missing tables like `sessions`.

## When to Use
When the fleet analytics sync encounters errors due to missing database tables (e.g., `no such table: sessions`) and you want to ensure the sync continues gracefully while addressing the root cause.

## Steps
1. **Run the fleet analytics sync** as usual:
   ```bash
   python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync
   ```
2. **If you encounter an error like `no such table: sessions`**:
   - The sync will continue but skip session data (as seen in the output).
   - After the sync completes, investigate the database schema.
3. **Check the database schema**:
   ```bash
   sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db ".schema"
   ```
4. **If the `sessions` table is missing**, create it based on the expected schema (refer to the the operator agent Agent documentation or the application source for the exact schema).
5. **Optionally, add a preventive check** to the fleet analytics sync script to create missing tables automatically (see the `references/` directory for an example patch).

## Known Issues
- The `sessions` table may be missing if the the operator agent Agent database was initialized without the session tracking feature enabled.
- Creating the table manually may require matching the exact schema used by the operator agent Agent.

## References
- See `references/sessions-table-schema.md` for the expected schema of the `sessions` table.
- See `references/sync-script-patch.md` for an example patch to the fleet analytics sync script that auto-creates missing tables.

## Troubleshooting
If the sync still fails after creating the table, check for:
- Permission issues on the database file.
- Other missing tables (run `.schema` to see all tables).
- Version mismatches between the fleet analytics script and the database schema.
