# Fleet-Wide Blackout Diagnosis Pattern

## Symptoms
- All 121+ enabled jobs showing `lastStatus: "error"`
- Error reason: `timeout` across all jobs
- `sibling-agent cron list` may fail (gateway WebSocket 1006)
- Zero successful runs recorded in `jobs-state.json` (latest_ok_ts = 0)
- Fleet health reports are empty stub PDFs (~1.8KB, 1 page)

## Root Causes (ranked by likelihood)

### 1. Free-Model Single-Point Failure
All jobs using `openrouter/*:free` models that all timeout identically. Check model distribution:
```python
models = Counter(j.get('payload',{}).get('model','none') for j in enabled_jobs)
# If 100% free models = zero fallback resilience
```
**Fix**: Add paid model slots ($15-30/month) or local model fallback (Ollama).

### 2. Gateway Down
WebSocket 1006 abnormal closure. Gateway not accepting connections.
**Fix**: `sibling-agent doctor`, restart gateway, or read JSON files directly for diagnosis.

### 3. Rate Limit Exhaustion
High-frequency jobs (e.g., `*/15 * * * *`) burn through rate limits before lower-priority jobs can run.
**Fix**: Pause the high-frequency job. Check `consecutiveErrors` — if one job has 100+, it's the culprit.

## Diagnostic Commands (cron-safe — use terminal tool)
```bash
# Fleet status summary (no execute_code needed)
cd /<workspace> && python3 -c "
import json, datetime
from collections import Counter
with open('jobs.json') as f: jobs = json.load(f).get('jobs', [])
with open('jobs-state.json') as f: states = json.load(f).get('jobs', {})
enabled = [j for j in jobs if j.get('enabled', True)]
ok = sum(1 for j in enabled if states.get(j.get('id',''),{}).get('state',{}).get('lastStatus')=='ok')
err = sum(1 for j in enabled if states.get(j.get('id',''),{}).get('state',{}).get('lastStatus')=='error')
models = Counter(j.get('payload',{}).get('model','none') for j in enabled)
reasons = Counter(states.get(j.get('id',''),{}).get('state',{}).get('lastErrorReason','?') for j in enabled)
worst = sorted([(j.get('name','?'), states.get(j.get('id',''),{}).get('state',{}).get('consecutiveErrors',0)) for j in enabled], key=lambda x:-x[1])[:5]
print(f'ENABLED:{len(enabled)} OK:{ok} ERR:{err} FREE_PCT:{models.get(\"openrouter/...\")/len(enabled)*100:.0f}%')
print(f'ERROR_REASONS:{dict(reasons.most_common(3))}')
print(f'WORST:'); [print(f'  {c}x {n}') for n,c in worst if c > 0]
"
```

## Executive Memo Language (when reporting blackout)
Lead with the blackout numbers. Use "total sensory deprivation" framing — the principal needs to understand this isn't notification fatigue, it's a complete intelligence failure. Include the table showing days since last run, error rate %, and model dependency analysis.

## Case Study: June 2026 Blackout
- 124 total jobs, 121 enabled, 119 erroring (98.3%)
- 0 successful runs fleet-wide, 6 days since last run
- All jobs on 5 OpenRouter free models, all timing out
- SINGULARITY Always-On Pulse: 122 consecutive errors (15-min interval = 96 attempts/day on dead models)
- Intel officer briefs stopped May 28, workspace frozen since March
- Fleet health reports generating empty 1.8KB PDFs (monitoring theater)
