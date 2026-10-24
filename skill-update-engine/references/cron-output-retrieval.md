# Cron output retrieval for review jobs

When a scheduled review job runs but `session_search` only returns compacted, partial, or older context, recover the actual run output from the local the operator agent state database before concluding the report is missing.
## Preferred lookup order

1. Search `session_search` for the job id or job name.
2. If the hit is only a summary, locate the matching cron session in `<agent-home>/state.db`.
3. Read the `messages` table for the latest `cron_<job_id>_...` session.
4. Use the final assistant message in that session as the review result.
5. If a tool message contains `<persisted-output>`, follow the saved file path to recover the full payload.

## Watchdog cron output lookup

When the watchdog itself is the cron job being monitored (e.g., `cron_31e90033684f_...` for the V1 Skill Cycle Watchdog), use the same lookup order. The watchdog's final assistant message contains its alert decision, which should match the template in `references/watchdog-monitoring-pattern.md`.

## Useful SQLite pattern
```sql
select session_id, id, role, content
from messages
where session_id like 'cron_<job_id>_%'
order by timestamp desc, id desc;
```

## What to verify
- The cron session is the newest one for that job id.
- The final assistant message actually contains the review summary, not just a handoff or plan.
- Any target counts in the report are compared against the standing daily quota before alerting.

## Pitfalls
- `session_search` may surface an earlier or compacted session that mentions the same job name but is not the latest run.
- A compacted summary can mention the right job id while hiding the actual review output.
- Do not stop at the first discover result if the output looks like metadata only; verify against `state.db`.
