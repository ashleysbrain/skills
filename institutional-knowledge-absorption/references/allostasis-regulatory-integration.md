# Allostasis Regulatory Integration for the Corpus Pipeline

## The Biological Isomorphism

The corpus audit/fix system maps to the **allostatic regulatory loop**, owned
by the specialist engine (the specialist engine, DS-ECS-SUB-04.02.01-v1.1.0, port 8091).

Allostasis = achieving stability through change (Sterling & Laughlin 2015).
The body doesn't maintain a fixed setpoint; it PREDICTS demand and adjusts
before deviation occurs. The regulatory loop has three phases:

| Phase | Corpus Script | Biological Analog | Token Cost |
|-------|--------------|-------------------|------------|
| SENSING | corpus_health_audit.py | Baroreceptor / chemoreceptor detection | Zero (pure Python) |
| CORRECTION | corpus_auto_fixer.py | Glymphatic clearance (stale waste removal) + immune reset | Zero (SQL operations) |
| ESCALATION | corpus_watchdog.py | Autonomic escalation (sympathetic activation) | Zero (script logic) |

When the watchdog detects that auto-fixing cannot resolve the issue, it
escalates by printing an alert that triggers the Fixer Agent cron job
(agent-required actions: RERUN_DISCOVERY, RERUN_ABSORPTION).

## How the Vitals POST Works

The watchdog reports corpus health as a custom_metric to the specialist engine:

```
POST http://localhost:port/vitals/allostasis
{
  "health_status": "critical" | "ok",
  "custom_metrics": {
    "subsystem": "knowledge_canon_absorption",
    "health": "HEALTHY" | "WARNING" | "CRITICAL",
    "queue_pending": N,
    "queue_claimed": N,
    "queue_absorbed": N,
    "queue_failed": N,
    "stale_claims": N,
    "actions_needed": [...],
    "last_absorption": "timestamp"
  }
}
```

the specialist engine accepts this via its `/vitals/{engine_id}` endpoint using the
`ALLOSTASIS` engine_id (self-arm). The engine returns `{"severity": "normal"}`.

**Graceful degradation:** If the specialist engine is down, the watchdog catches the
connection error and continues functioning standalone. The vitals POST is
for organism-level visibility, not for watchdog operation. The watchdog is
self-contained.

## Generalizing This Pattern to Other Cron Pipelines

Any cron-driven pipeline that can silently fail should use the same pattern:

1. **AUDIT script** — reads job status from `<agent-home>/cron/jobs.json`, checks
   the pipeline's own DB/state for staleness, outputs JSON health report
2. **AUTO-FIXER script** — handles mechanical repairs (reset stale state,
   retry failed items, rebuild indexes). Zero tokens, zero agents.
3. **WATCHDOG script** — chains audit + fixer, POSTs vitals to the specialist engine,
   escalates only when agent intervention is genuinely needed
4. **FIXER AGENT cron** — the effector arm that handles agent-required actions
   (browser navigation, LLM reasoning). Pin to llm-vendor-glm to avoid OpenRouter
   credit exhaustion failover.

The biological mapping:
- Pipeline = a subsystem (like blood glucose regulation, or body temperature)
- Audit = the sensor (baroreceptor, thermoreceptor)
- Auto-fixer = local homeostatic mechanism (glymphatic clearance, sweating)
- Watchdog = central regulatory loop (hypothalamus comparing sensor to setpoint)
- Fixer agent = effector organ activation (muscle shivering, adrenal release)
- the specialist engine = the regulatory brain that owns the loop and predicts demand
