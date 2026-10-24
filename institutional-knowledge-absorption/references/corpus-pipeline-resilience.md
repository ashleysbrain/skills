# Corpus Pipeline Resilience Architecture

The 3-script audit→fixer→watchdog chain that makes the absorption pipeline
self-healing. Created 2026-07-06 after a discovery job failed silently for a
week (provider failover to depleted OpenRouter account).

## Architecture

```
Every 4h (no_agent, zero tokens):
  corpus_watchdog.py
    ├── 1. Runs corpus_health_audit.py
    │     ├── Reads <agent-home>/cron/jobs.json for job statuses
    │     ├── Queries canon.db for queue state, stale claims, failed items
    │     ├── Checks DB integrity (pragma, FTS count, orphaned sources)
    │     └── Returns JSON: {health, actions_needed, warnings, ...}
    │
    ├── 2. If actions include auto-fixable items:
    │     Pipes audit JSON to corpus_auto_fixer.py stdin
    │     ├── UNSTUCK_CLAIMS → resets claims >48h back to pending
    │     └── RETRY_FAILED_ITEMS → resets failed items to pending
    │     Then re-runs audit to confirm resolution
    │
    └── 3. Decision:
          ├── HEALTHY or auto-fixed → SILENT (exit 0, prints nothing)
          ├── WARNING (non-critical) → prints warning, exit 0
          └── CRITICAL (needs agent) → prints alert, exit 1
               The cron delivery carries the alert to the user

Every 8h (llm-vendor-glm, agent):
  Corpus Fixer Agent
    ├── Reads corpus_health_audit.py output
    ├── RERUN_DISCOVERY → browses MIT/Stanford/Yale catalogs, adds courses
    ├── RERUN_ABSORPTION → manually extracts + syncs stuck claimed items
    └── Re-runs audit to verify health restored
```

## Scripts (all in knowledge-canon/)

### corpus_health_audit.py
Diagnoses the pipeline state. Outputs JSON.

```bash
# Full audit
python3 corpus_health_audit.py

# Key output fields:
# - health: HEALTHY | WARNING | CRITICAL
# - exit_code: 0 (healthy) | 1 (warning) | 2 (critical)
# - actions_needed: [UNSTUCK_CLAIMS, RERUN_DISCOVERY, ...]
# - queue: {pending, claimed, absorbed, failed, stale_claims, canon_totals}
# - failed_items: [{id, title, url, institution, domain}]
```

### corpus_auto_fixer.py
Mechanical repairs. No agent needed.

```bash
# Reset stale claims (>48h) back to pending
python3 corpus_auto_fixer.py unstuck

# Reset all failed items back to pending
python3 corpus_auto_fixer.py retry-failed

# Full DB integrity check
python3 corpus_auto_fixer.py integrity

# Rebuild FTS search index
python3 corpus_auto_fixer.py rebuild-fts

# Auto-fix mode: read audit JSON from stdin, fix everything reported
python3 corpus_health_audit.py | python3 corpus_auto_fixer.py
```

### corpus_watchdog.py
Orchestrator. Chains audit + fixer. This is the cron entry point.

```bash
python3 corpus_watchdog.py
# Silent if healthy/auto-fixed
# Prints alert if agent needed
```

## Cron jobs

| Job | ID | Schedule | Type |
|-----|----|----------|----|
| Health Watchdog | 86cc83a4cc5d | every 4h | no_agent script |
| Fixer Agent | 29969388f482 | every 8h | llm-vendor-glm agent |

## Reproducing this pattern for other pipelines

The 3-script pattern generalizes to any cron-driven pipeline:

1. **Audit script:** reads job statuses from `<agent-home>/cron/jobs.json`, checks
   the pipeline's DB/queue for stuck items, verifies integrity. Outputs JSON
   with health level + actions_needed array.

2. **Fixer script:** handles mechanical repairs (SQL updates, index rebuilds,
   cache clears). Each action is a named function callable standalone or via
   stdin-piped audit JSON.

3. **Watchdog script:** runs as `no_agent: true` cron. Chains audit→fixer,
   stays silent when resolved, escalates when an agent is needed. Zero tokens
   burned on healthy runs.

4. **Fixer agent cron:** runs on a non-OpenRouter provider (llm-vendor-glm preferred).
   Handles actions requiring browser/LLM. Re-audits after fixing.

## Biological isomorphism: the specialist engine regulatory loop

The audit→fixer→watchdog chain maps to the allostatic regulatory loop and is
formally owned by the specialist engine (the specialist engine, DS-ECS-SUB-04.02.01-v1.1.0,
port 8091).

| Layer | Bio equivalent | DS system |
|-------|---------------|-----------|
| Audit | Allostatic sensing (detect deviation from setpoint) | corpus_health_audit.py |
| Auto-fixer | Glymphatic clearance (remove waste/stale items) + immune reset | corpus_auto_fixer.py |
| Watchdog | Allostatic escalation (when correction insufficient) | corpus_watchdog.py |
| Fixer agent | Immune response (agent-level repair) | Fixer Agent cron |

The watchdog POSTs corpus vitals to the specialist engine on every tick:
```
POST http://localhost:port/vitals/allostasis
{
  "health_status": "critical" | "ok",
  "custom_metrics": {
    "subsystem": "knowledge_canon_absorption",
    "health": "HEALTHY" | "WARNING" | "CRITICAL",
    "queue_pending": N,
    "queue_claimed": N,
    "stale_claims": N,
    "actions_needed": [...]
  }
}
```

If the Allostasis engine is down, the watchdog degrades gracefully and
continues functioning standalone. The POST uses `urllib.request` (stdlib,
no external deps). The engine returned `{"severity":"normal","engine":"allostasis"}`
when tested 2026-07-06.

### Mitigation-aware audit (false-positive prevention)

The audit checks whether a failed cron job's work was completed out-of-band
(e.g., via delegate_task or manual fix). If discovery cron failed but the
queue has 20+ pending items, the audit downgrades from CRITICAL to WARNING
instead of triggering the fixer agent unnecessarily.

```python
if discovery["last_status"] == "error":
    pending = queue.get("pending", 0)
    if pending >= 20:
        # Mitigated out-of-band — downgrade
        warnings.append("Discovery cron failed but queue populated out-of-band")
    else:
        critical = True
        actions_needed.append("RERUN_DISCOVERY")
```

## Known schema details

The `absorption_queue` table columns (verified 2026-07-06):
`id, title, url, source_type, institution, course_code, domain, faculty,
dimension_8d, priority, status, claimed_at, completed_at, result_note,
error_reason, retry_count, created_at, tags`

Note: the column is `retry_count`, NOT `attempts`. Do not reference non-existent
columns in UPDATE statements.

## Provider failover chain

Cron jobs configured for google-gemini-cli can silently fall back to OpenRouter
when gemini has issues. If OpenRouter credits are depleted, this produces
HTTP 402. The fixer agent is pinned to llm-vendor-glm to avoid this entirely.
