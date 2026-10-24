# Additional Notes for Fleet Analytics Troubleshooting

## Common Issues and Fixes

### Issue: "no such table: sessions" during sync
- **Cause**: The sessions table in the target database (analytics.db) has not been created yet.
- **Fix**: This is normal if the sync script is in the process of creating tables. The agents.db still contains the agent and cron data. Re-run the sync after a few moments, or check agents.db for immediate data.

### Issue: analytics.db shows 0 rows for cron_jobs but agents.db shows data
- **Cause**: The sync script may have failed to write to analytics.db after reading from agents.db.
- **Fix**: Check the sync script's output for errors. Ensure the script has write permissions to the analytics.db file. Consider running the sync manually to see any error messages.

### Issue: Missing recent data in fleet_health_snapshots
- **Cause**: The snapshot may not have been generated yet, or there is a delay in the sync process.
- **Fix**: Check the timestamp of the most recent snapshot in agents.db. If the data is recent in agents.db but not in analytics.db, the sync script may have a bug in the snapshot transfer.

## Best Practices

1. **Always check agents.db first** for real-time data.
2. **Monitor the sync script's output** for any errors.
3. **Regularly vacuum and analyze** the databases to maintain performance.
4. **Backup** the databases before making any manual changes.

## Related Documentation
- OpenClaw Fleet Analytics Design Document (internal)
- Schema Reference: https://internal.sibling-agent.dev/schemas/analytics