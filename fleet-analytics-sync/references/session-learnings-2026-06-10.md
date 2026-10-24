# Session Learnings — 2026-06-10 (Second Sync)

## Sync Results
- 124 cron jobs synced from OpenClaw API
- 51 agent knowledge stores synced
- 1,710 journal entries indexed from 236 agent dirs
- 80 active / 84 total agents
- 40 registered personas (AISHA x10, COSMOS x10, DSWAVE x10, FORGE x10)

## Critical Finding: Both DBs Empty Despite Successful Sync

The sync completed (exit 0, "Full sync complete") but:

- `fleet_analytics.db` = **0 bytes** (completely empty file)
- `analytics.db` = 184KB (has schema with 13 tables but **all tables empty**)
- `PRAGMA table_info()` shows tables exist: `fleet_health_snapshots`, `cron_jobs`, `cron_runs`, `error_log`, `journal_entries`, `agent_personas`, `agent_sessions`, `talent_insights`, `model_tier_distribution`, `cron_error_insights`, `personality_distribution`, `daily_cost_rollup`, `sqlite_sequence`
- `SELECT COUNT(*) FROM <every_table>` = 0 for all tables

**Implication**: All data analysis had to come from alternative sources, not SQL queries.

## Data Source Hierarchy (When DBs Are Empty)

1. **Sync script stdout** — the most reliable immediate source. Contains status distribution, top errors, model distribution, journal compliance, sessions count.
2. **`cron_jobs.json`** (1.3MB) — raw API dump. Structure: `{"jobs": [...], "total": N, "offset": 0, "limit": N, "hasMore": false}`. Each job nested under `jobs` array.
3. **`cron_errors_previous.json`** — list of dicts (NOT a dict). Format: `[{"name": "...", "consecutiveErrors": N, ...}, ...]`.
4. **`last_error_count.txt`** — single integer (previous error count). Value: 859.
5. **`last_analytics_sync.txt`** — ISO timestamp of last sync. Value: `2026-05-21T23:12:34.901625`.

## cron_jobs.json Job Object Structure

Key fields for analytics:
```
job.name                    — human-readable name
job.enabled                 — boolean
job.payload.model           — assigned model (config intent)
job.state.lastStatus        — "error" | "success" | "skipped"
job.state.consecutiveErrors — integer
job.state.lastError         — full error string
job.state.lastErrorReason   — "model_not_found" | "auth" | "timeout" etc.
job.state.lastDiagnostics   — detailed diagnostics object
job.state.lastDiagnostics.summary — truncated error summary
job.state.nextRunAtMs       — epoch ms
job.state.lastRunAtMs       — epoch ms
```

## Fleet Status (This Sync)

### Status Distribution (from raw JSON, live jobs only)
- error: 123 (99.2%)
- skipped/other: 1

Note: All 124 jobs exist but only 1 was non-erroring. The sync report showed "124 enabled, 76 erroring, 183 disabled" which totals 383 = historical count from agents.db, not the 124 live jobs.

### Model Distribution (from payload.model — config intent)
1. openrouter/google/gemini-2.5-flash-preview-05-20: 41
2. openrouter/anthropic/claude-3-5-sonnet-20241022: 40
3. anthropic/claude-haiku-4-5: 21
4. openrouter/z-ai/glm-4.5-air: 19
5. Other (gemma, llama): 3

This differs from the sync report's model distribution which showed free-tier models that actually resolved (llama-3.3-70b, glm-4.5-air, nemotron, qwen3) — those are the failover models, not the config models.

### Top Erroring Jobs
1. hydra-hourly-dispatcher: 253 consecutive
2. SINGULARITY Always-On Strategic Pulse: 219 consecutive
3. 8d360-repo-ip-audit: 191 consecutive
4. AISHA the operator agent Brief: 98 consecutive
5. VITALS 8D Product Review: 66 consecutive

### Error Root Causes (from lastErrorReason)
- model_not_found: 85
- unknown (auth/billing): 38

### Auth Failure Cascade (Root Cause)
1. **Anthropic OAuth revoked** (auth_permanent): All claude-* models returning 403
2. **Z-AI token expired**: All llm-vendor/glm-* failing with 401, then cooldown cascade
3. **Google Gemini unknown models**: gemini/gemini-2.5-flash/pro returning "Unknown model"
4. **Google Gemini CLI crash**: `spawnSync sysctl ENOENT` in gemini-cli (Node.js bug)
5. **OpenRouter billing limit**: Key returning 403 "Key limit exceeded"
6. **Invalid model reference**: `nvidia/nvidia/llama-3.3-nemotron-super-49b-v1:free` (doubled prefix)

### Journal Compliance
1.2% (1 of 84 agents journaled). Expected given fleet-wide outage.

## Error Comparison Pattern

To compare with previous snapshot using `cron_errors_previous.json`:
```python
import json
with open('cron_errors_previous.json') as f:
    prev_errors = json.load(f)  # This is a LIST, not a dict
prev_map = {e.get('name', ''): e.get('consecutiveErrors', 0) for e in prev_errors if isinstance(e, dict)}
# Then compare with current: curr_map = {j['name']: j['state']['consecutiveErrors'] for j in data['jobs'] if j['state']['consecutiveErrors'] > 0}
```
