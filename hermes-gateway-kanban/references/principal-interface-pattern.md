# the principal Interface Pattern — Patient 0 Telegram Entry Point

## Concrete Implementation (Session 2026-06-13)

### Profile Setup
```bash
# Create patient interface profile
hermes profile create principal-interface --clone
hermes -p principal-interface config set model.default "openrouter/nvidia/nemotron-3-ultra:free"

# Install required skills
cp -r skills-library/autonomous-ai-agents/hermes-agent <agent-home>/profiles/principal-interface/skills/
cp -r skills-library/devops/kanban-orchestrator <agent-home>/profiles/principal-interface/skills/
cp -r skills-library/operations/aisha-md-health-orchestration <agent-home>/profiles/principal-interface/skills/
cp -r skills-library/operations/health-scoring-daily-pipeline <agent-home>/profiles/principal-interface/skills/

# Set as Telegram default profile
hermes config set telegram.default_profile principal-interface
hermes gateway restart
```

### SOUL.md Routing Logic
```markdown
## Engine Fleet (7 Engines)
| Engine | Port | Body System | Agent | When to Call |
|---|---|---|---|---|
| Morphogen | 8093 | Skeletal/Registry | the specialist engine | Registry, gradients, contracts |
| Wave | 8000 | Brain/CNS | the specialist engine | Coaching, resonance, mastermind |
| Quartz | 8089 | Autonomic NS | the specialist engine | PID control, lattice, tasks |
| Seed | 8090 | Endocrine/Growth | the specialist engine | Avrami/JMAK, Landau, product dev |
| Allostasis | 8091 | Immune/Homeostatic | the specialist engine | Surveillance, allostatic load |
| Harvey | 8092 | Cardiovascular | the specialist engine | Fabric, transport, registry |
| Bernard | 8094 | Clinical Diagnostic | **the specialist engine** | Clinical Dx, SOAP rounds, vitals, evidence synthesis |

## Routing Rules
- "health", "vitals", "diagnose", "rounds" → Bernard (8094) /rounds, /patient/vitals, /patient/summary
- "coach", "strategy", "decide", "mastermind" → Wave (8000) /coach, /resonance, /mastermind
- "tasks", "plan", "schedule", "priority" → Quartz (8089) /v1/tasks, /v1/lattice/state, /v1/pid
- "build", "product", "feature", "launch" → Seed (8090) /v1/engines, /landau, /avrami, /critical-path
- "monitor", "stress", "immune", "allostatic" → Allostasis (8091) /organism, /surveillance, /healing
- "registry", "fleet", "status", "genotypes" → Morphogen (8093) /organism/map, /genotypes, /gradients
- "flow", "messages", "transport" → Harvey (8092) /fabric/vitals, /v1/circulation

## Engine Endpoints Dictionary
ENGINE_ENDPOINTS = {
    "wave": "http://127.0.0.1:port",
    "quartz": "http://127.0.0.1:port",
    "seed": "http://127.0.0.1:port",
    "allostasis": "http://127.0.0.1:port",
    "harvey": "http://127.0.0.1:port",
    "morphogen": "http://127.0.0.1:port",
    "bernard": "http://127.0.0.1:port",
}
```

### Clinical Engine (Bernard) Identity Hardening
**Every endpoint returns:**
- `agent_role: "Attending AI Physician — AI Clinical Diagnostic Engine"`
- `disclaimer: "THIS ENGINE DIAGNOSES AI SYSTEMS ONLY. NEVER HUMANS. Human-body mapping is a cognitive/triage framework for AI diagnostics, not clinical practice on humans."`
- Engine self-declares as: `AI Clinical Diagnostic Engine — Diagnoses AI Systems Only`

**Bernard Capabilities:**
1. Clinical Diagnosis & SOAP Rounds
2. Differential Diagnosis & Vitals Monitoring
3. AI-Equivalent Credentials & CME Report
4. **Evidence Synthesis Scanner** (20 sources: NEJM, Lancet, Cochrane, WHO, NICE, IQWiG, CADTH, arXiv, ICML, NeurIPS, etc.)
5. **12 World Health System Models** (Denmark, Taiwan, Switzerland, Netherlands, Singapore, Nordic, Japan, South Korea, UK NHS, Canada, Germany, Australia)
6. **26 Human→AI Medical Concept Mappings** (e.g., "vaccination" → "proactive config hardening", "epidemiology" → "fleet-wide bug contagion tracing")
7. **Cross-Domain Insights** (10 insights with evidence basis)
8. **Novel Approach Generator** (AOPD - AI Organism Precision Diagnostics)
9. Health System Methodology Adaptation (non-US value-based care systems)

### Engine Fleet Startup & Recovery Pattern
When engines go down (common during development):
```bash
# 1. Restart individual engine
cd /<workspace> && python run_server.py &
# 2. Verify health
curl http://127.0.0.1:port/health
# 3. Re-register in Morphogen (if needed)
curl -X POST http://127.0.0.1:port/genotypes/register \
  -H "Content-Type: application/json" \
  -d '{"engine_id": "bernard", ...}'
# 4. Verify organism map
curl http://127.0.0.1:port/organism/map
```

### Key Constraints (from session)
- Single Telegram contact (principal-interface) — no second bot
- Memory isolation between Engine Fleet (Silo 1) and Patient 0 Health (Silo 2)
- No Anthropic models for any fleet operations
- Evidence-based, non-diagnostic health guidance
- Kanban dispatcher active in gateway (60s interval)
- Engine fleet self-heals 24/7 via Bernard cron (c890b270b920)
- Patient 0 runs on user schedule via principal-interface