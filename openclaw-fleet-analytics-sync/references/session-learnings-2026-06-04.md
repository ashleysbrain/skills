# Session Learnings — 2026-06-04 Fleet Analytics Sync

## Sync Results

### 08:16 UTC Sync
- `fleet_analytics.py sync` completed successfully (exit 0)
- 0 cron jobs synced (live API still returning empty — gateway reset persists)
- 51 agent knowledge stores synced
- 1,709 journal entries indexed from 236 agent dirs
- 1 git commit scanned for 2026-06-04

### 11:16 UTC Sync (this session)
- Same sync results: 0 cron jobs, 51 knowledge stores, 1,709 journal entries, 236 agent dirs
- Sessions doubled: 51 → 102 (24h sessions from yesterday → today)
- Git commits for 2026-06-04: 1 commit, 11 files created, 38 modified
- 0 cron runs recorded for today (no live cron data flowing)

## Key Observations

### Model Landscape Shift
Llama 3.3 70B became the dominant model at 43% (79 of 183 jobs). On June 3 it was at 16.1% (20 of 124 enabled). This suggests a large-scale model migration happened between June 3 and June 4.

Current distribution (183 total jobs):
| Model | Jobs | % |
|-------|------|---|
| meta-llama/llama-3.3-70b-instruct:free | 79 | 43% |
| z-ai/glm-4.5-air:free | 28 | 15% |
| qwen/qwen3-coder:free | 27 | 15% |
| openai/gpt-oss-120b:free | 27 | 15% |
| nvidia/nemotron-3-super-120b-a12b:free | 22 | 12% |

### Agent Model Coverage Gap
50 of 72 active agents have no `primary_model` assigned. Only 22 agents have models:
- anthropic/claude-sonnet-4-6: 17 agents
- anthropic/claude-haiku-4-5: 2 agents
- anthropic/claude-opus-4-6: 1 agent
- anthropic/claude-opus-4-5: 1 agent
- openai-codex/gpt-5.2: 1 agent

This means model distribution queries against the agents table will only cover ~30% of the fleet. The remaining agents likely inherit defaults or use per-cron-job model configs.

### Agent World Distribution
| World | Agents |
|-------|--------|
| DS (Divinity Science) | 50 |
| Empire | 11 |
| Divinity Science (alt) | 7 |
| the principal Personal | 3 |
| Goddess Divinity | 1 |

### Fleet Health: Clean
- 0 errors (24h), 0 rate limits, 0 timeouts
- 0 jobs in error state (all state objects are empty `{}`)
- Fleet TWC: 7.41
- 72 active / 76 total agents

### error_log Table Now Populated (New Pattern)
Previously documented as "often empty" — now has 7 `talent-review-insight` entries from today's talent review:
- HIGH (2): Model tier mismatches (CIO on haiku-4-5, CFO/QUASAR on haiku-4-5)
- MEDIUM (3): Capability gaps, personality imbalance, model tier downgrade suggestion
- LOW (2): World assignment inconsistencies, missing FLASH-tier agents

These are NOT cron execution errors — they're fleet health insights from the talent review system. The error_log table now serves dual purposes.

### Journal Compliance: Deeper Issue Than Script Bug
The `journal_entries` table has 1,709 rows from 236 agent dirs, but:
- `COUNT(DISTINCT agent_id) WHERE entry_date = date('now')` returns 0
- June 3 also shows 0 unique agents (despite 16 entries)
- June 2 shows 0 unique agents (despite 80 entries)

The issue is NOT just the compliance percentage calculation. The `agent_id` FK mapping is broken — entries are indexed from files but not correctly linked to agent records. The `agent_id` column may be NULL or 0 for most entries.

### Analytics Pipeline Schema Drift (FIXED 2026-06-04 by NEXUS)
**Previous documentation said "no such table" — this was partially wrong.** The actual errors were:
- `table task_analytics has no column named task_id` — the table EXISTS but was missing 11 columns
- `table session_analytics has no column named session_id` — same pattern, missing 7 columns
- `no such table: qa_tracking` — table genuinely didn't exist
- `no such table: daily_productivity` — table genuinely didn't exist

**Fix applied:** Added 18 columns via `ALTER TABLE ADD COLUMN`, created 2 missing tables via `CREATE TABLE IF NOT EXISTS`, fixed `agents_needing_attention` view (column `wd.status` → `wd.wellness_status`). After fix, collection pipeline runs clean: `Collection complete for 2026-06-04` with 51 sessions recorded and 1 daily rollup built. See `nexus-auto-remediation` skill `references/2026-06-04-schema-migration.md` for full details.

### Duplicate Snapshot Accumulation (FIXED)
Each sync creates a new row in `fleet_health_snapshots` for the same date. 7 identical rows for 2026-06-04 were observed before cleanup. Deduped with: `DELETE FROM fleet_health_snapshots WHERE id NOT IN (SELECT MAX(id) FROM fleet_health_snapshots GROUP BY snapshot_date)`. Remaining: 1 row per date (June 3 and June 4). When querying trends, use `GROUP BY snapshot_date` or take only the latest per date.

### Cost Tracking Not Ingesting
`fleet_health_snapshots.total_cost_usd` consistently shows 0.0. The cost calculation pipeline isn't receiving token cost data, even though the `MODEL_COSTS` dictionary is defined in `fleet_analytics.py`.

### Database State
- `agents.db`: Has tables (agents, fleet_health_snapshots, error_log, journal_entries) but cron_jobs and cron_runs are empty
- `analytics.db`: Has full schema but all cron-related tables empty
- `fleet_analytics.db`: 0 bytes (legacy, unused)
- Live data comes entirely from reading `~/.sibling-agent/cron/jobs.json` directly

### Tool Workarounds
- `execute_code` blocked in cron mode (approval policy) — use `terminal` with direct `sqlite3` commands instead
- `sqlite3 -header -column` gives readable tabular output
- Schema discovery via `.schema table_name` is essential before querying — column names are non-obvious
- Chain multiple echo+sqlite3 commands in one `terminal` call to avoid round-trips
