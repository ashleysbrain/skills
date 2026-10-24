# Fleet Analytics Sync Session Learnings – 2026-06-06 (20:15 UTC)

## Sync Command
```bash
python3 ~/.sibling-agent/workspace/intel/agents/database/fleet_analytics.py sync
```

## Output Summary
- Deprecation warnings re `datetime.datetime.utcnow()` (harmless, 8 warnings)
- `✓ Synced 0 cron jobs` (live API empty — persistent since June 3 gateway reset)
- `✗ the operator agent sessions error: no such table: sessions` (expected, non-blocking)
- `✓ Synced 51 agent knowledge stores`
- `✓ Indexed 1710 journal entries from 236 agent dirs`
- `✅ Collection complete for 2026-06-06`
- Fleet health snapshot: Agents 77 active / 81 total, Cron 0/0/0, Errors 0/0/0, Sessions 51, Journal compliance 0.0%

## Key Finding: Model Distribution Sources

When cron_jobs is empty (0 synced), model distribution must come from `agents.primary_model`:

| Model | Agent Count |
|-------|-------------|
| anthropic/claude-haiku-4-5 | 52 |
| anthropic/claude-sonnet-4-6 | 24 |
| anthropic/claude-opus-4-6 | 1 |
| anthropic/claude-opus-4-5 | 1 |
| openai-codex/gpt-5.2 | 1 |
| None (unassigned) | 2 |

**DO NOT use** `agent_sessions.model_used` for model distribution — it is always NULL.
**DO NOT use** `agent_credentials` — that table tracks academic credentials (degrees, publications), not API model assignments.

## Database State (agents.db)
- `agents`: 81 rows (77 active, 4 archived)
- `agent_sessions`: 204 rows (51/day, stable 4 days)
- `journal_entries`: 117,944 rows
- `fleet_health_snapshots`: 53 rows
- `error_log`: 7 rows (all talent-review-insight from June 4, all resolved)
- `cron_jobs`: 0 rows (live API empty since gateway reset)
- `cron_runs`: 0 rows
- `daily_productivity`: 3 rows

## Stable Fleet State (unchanged since June 3-4)
- 0 errors, 0 rate limits, 0 timeouts — fleet is clean
- Sessions stable at 51/day
- Journal compliance calc still broken (reports 0.0%)
- No new critical errors
