Session-specific troubleshooting learnings from 2026-06-05 fleet analytics sync:

1. Database file locations:
   - Use `find ~/.sibling-agent -name "*.db" -type f` to locate all relevant database files
   - Key databases: analytics.db, fleet_analytics.db, journal_compliance.db, agents.db

2. Table discovery:
   - Use `sqlite3 /path/to/db.db ".tables"` to list all tables
   - Use `sqlite3 /path/to/db.db "PRAGMA table_info(table_name);"` to see column names

3. Common column name mismatches:
   - In error_log table: the timestamp column is named `occurred_at`, not `timestamp`
   - In fleet_health_snapshots table: journal compliance column is named `journal_compliance_pct`, not `journal_compliance`

4. Query examples that worked:
   - Count cron jobs: `SELECT COUNT(*) as total_cron_jobs FROM cron_jobs;`
   - Check error log structure: `PRAGMA table_info(error_log);`
   - Check cron jobs structure: `PRAGMA table_info(cron_jobs);`
   - Check fleet health snapshots: `PRAGMA table_info(fleet_health_snapshots);`

5. When sync reports "0 cron jobs synced":
   - This may indicate the OpenClaw gateway returned empty results, not necessarily that there are no cron jobs configured
   - Always verify by checking the database directly: `sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db "SELECT COUNT(*) FROM cron_jobs;"`
   - Also check the static jobs.json file: `ls -la /<workspace>` and examine its structure

6. Deprecation warnings:
   - The script shows multiple `datetime.datetime.utcnow() is deprecated` warnings
   - These are non-critical but indicate the script should be updated to use timezone-aware objects
   - See references/deprecation_warnings.md for details