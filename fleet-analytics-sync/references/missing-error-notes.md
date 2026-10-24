# Missing Error Messages in Fleet Analytics

The `error_message` field in the `cron_runs` table is often empty or NULL, even when errors occur.
Error analysis must rely on the `error_type` field (typically 'timeout' or 'unknown') rather than specific error messages.
For detailed error diagnosis, check agent session logs or the operator agent gateway logs directly.