# Session Learnings: Fleet Analytics Sync - 2026-06-03

## Key Observations

### 1. agents.db Was Recreated (Data Loss)

The agents.db was recreated between the June 2 sync and this session. Evidence:
- Only 2 fleet_health_snapshots, both from 2026-06-03 (17:55 and 20:15)
- cron_jobs table: 0 rows
- cron_runs table: 0 rows (was 125K+)
- journal_entries: 3,418 rows (was 1.81M)
- error_log: 0 rows
- agent_personas: 0 rows (was 385)

Previous historical data is gone. The sync script ran successfully against the empty DB and created new (empty) snapshots.

**Reporting implication:** Error deltas comparing last sync (136 errors recorded in `last_error_count.txt`) to current (0) are meaningless. The "improvement" is an artifact of data loss.

### 2. Live API Returns 0 Jobs (Gateway Empty)

`sibling-agent cron list --json` returns:
```json
{"jobs": [], "total": 0, "offset": 0, "limit": 50, "hasMore": false}
```

This is consistent with the June 2 observation but now compounded by the DB recreation. The OpenClaw gateway's cron subsystem appears to have been reset.

### 3. Static jobs.json Root Is Now a Plain List

The static file `/<workspace>` now has the root as a JSON array (not `{"jobs": [...]}`):

```python
import json
with open('/<workspace>') as f:
    data = json.load(f)
isinstance(data, list)  # True
```

183 jobs total. All `state` objects are empty `{}` — no runtime state preserved in the static file.

### 4. New Model Landscape

All enabled jobs now use free-tier models exclusively. Previous paid models (Anthropic, Google Gemini) are completely gone:

| Model | Jobs |
|-------|------|
| openrouter/z-ai/glm-4.5-air:free | 28 |
| openrouter/qwen/qwen3-coder:free | 27 (NEW) |
| openrouter/openai/gpt-oss-120b:free | 27 (NEW) |
| openrouter/nvidia/nemotron-3-super-120b-a12b:free | 22 |
| openrouter/meta-llama/llama-3.3-70b-instruct:free | 20 |

### 5. Job Count Drop

Static file has 183 jobs (124 enabled, 59 disabled), down from ~392 on May 31. This may reflect:
- Fleet consolidation
- Removal of disabled/stale jobs
- Gateway migration that only preserved a subset

### 6. Delivery Mode Distribution

From static file:
- `announce`: 87 jobs
- `none`: 96 jobs

### 7. Sync Script Output vs Reality

Sync reported: "0 enabled, 0 erroring, 0 disabled" — this is because the live API returned 0 jobs and the DB is empty.

Static file shows: 124 enabled, 59 disabled, 0 erroring.

**The sync snapshot numbers cannot be trusted when both the live API is empty AND the DB was recreated.** Use the static file as the only available data source.

## Queries That Worked

```sql
-- Check if DB was recreated (low snapshot count = recreated)
SELECT COUNT(*) FROM fleet_health_snapshots;
SELECT MIN(snapshot_date), MAX(snapshot_date) FROM fleet_health_snapshots;

-- Verify tables exist but are empty
SELECT COUNT(*) FROM cron_jobs;
SELECT COUNT(*) FROM cron_runs;

-- Journal entries in recreated DB
SELECT COUNT(*) as entries, COUNT(DISTINCT agent_id) as agents
FROM journal_entries WHERE DATE(created_at) = DATE('now');

-- Compare with analytics.db (may have older pre-computed data)
SELECT * FROM cron_error_insights ORDER BY created_at DESC LIMIT 3;
```

## Static File Parsing Pattern

```python
import json
from collections import Counter

with open('/<workspace>') as f:
    data = json.load(f)

# Handle both root shapes
jobs = data if isinstance(data, list) else data.get('jobs', [])

enabled = [j for j in jobs if j.get('enabled')]
disabled = [j for j in jobs if not j.get('enabled')]

# Model distribution
models = Counter()
for j in enabled:
    model = j.get('payload', {}).get('model', 'unknown') or 'unknown'
    model = model.strip('"')  # Clean extra quoting
    models[model] += 1
```
