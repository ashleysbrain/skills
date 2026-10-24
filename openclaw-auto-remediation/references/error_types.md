# Error Types Observed in OpenClaw Cron Jobs

During the auto-remediation cycle, the following error types have been observed in the `state.lastErrorReason` field:

- `timeout`: The agent run exceeded the configured timeout seconds.
- `rate_limit`: The model provider returned a rate limit error (HTTP 429).
- `model_not_found`: The specified model is not available or not recognized by the provider.
- `connection_error`: Generic connection issues (often underlying timeout or network problems).

Each error type may require different remediation strategies. The current skill handles `timeout` and `rate_limit` (for specific models). `model_not_found` errors are not automatically fixed and should be investigated manually (e.g., check model name spelling, provider availability).
