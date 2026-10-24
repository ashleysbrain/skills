# Error Types in Cron Runs

The fleet analytics script categorizes errors based on the error message:

- rate_limit: contains "rate_limit" or "overloaded"
- timeout: contains "timeout"
- auth: contains "auth"
- unknown: anything else or empty

These categories are used in error reporting and health snapshots.

To reduce errors:
- Investigate rate_limit errors: consider adjusting schedule or checking API limits.
- Timeout errors: increase timeout thresholds or optimize the job.
- Auth errors: verify credentials and tokens.