# Body System ↔ Profile ↔ Engine Mapping

Complete mapping of Divinity Science body systems to the operator agent profiles to the specialist engine genotypes.

## Master Mapping Table

| Body System | the operator agent Profile | the specialist engine | Port | Scientist | Governing Equations | Model | Key Skills |
|---|---|---|---|---|---|---|---|
| **Skeletal** (Structure/Identity/Registry) | `morphogen` | Morphogen | 8093 | Francis Paxton (BMPs) | Registry, Gradients, Contracts | Nemotron-3-Ultra | `hermes-agent`, `kanban-orchestrator` |
| **Brain/CNS** (Coaching/Decision/Mastermind) | `wave` | Wave | 8000 | Kuramoto | Kuramoto Oscillators, Resonance, Mastermind | Nemotron-3-Ultra | `kanban-orchestrator`, `ds-wave-coaching` |
| **Autonomic NS** (Regulation/Homeostasis/PID) | `quartz` | Quartz | 8089 | Diviq | PID Control, Lattice, Task Regulation | Gemini-2.5-Flash | `kanban-worker`, `quartz-lattice` |
| **Endocrine/Growth** (Development/Avrami/SOC) | `seed` | Seed | 8090 | Waddington | Avrami JMAK, Landau Phase, SOC, CPM | DeepSeek-R1 | `kanban-worker` |
| **Immune/Homeostatic** (Surveillance/Diagnosis) | `allostasis` | Allostasis | 8091 | Sterling | Surveillance, Diagnosis, Intervention | LLM-4.5-Air | `aisha-md-health-orchestration`, `sentinel-compliance-audit`, `health-scoring-daily-pipeline` |
| **Circulatory** (Transport/Registry/Fabric) | `harvey` | Harvey | 8092 | William Harvey | Fabric, Registry, Transport | LLM-4.5-Air | `sibling-agent-fleet-analytics`, `sibling-agent-fleet-analytics-summary` |

**Note:** The `orchestrator` role is fulfilled by `morphogen` (Skeletal/Registry) which receives Telegram and dispatches Kanban tasks. No separate orchestrator profile needed — Morphogen Engine IS the registry/identity layer.

## Consolidated Profiles (Minimum Viable: 4 + 1) — vs. Full Fidelity (6 + 0)

### Minimum Viable Organism (4 Profiles + Orchestrator)
| Consolidated Profile | Contains Body Systems | Rationale |
|---|---|---|
| `cns` | Brain/CNS | Highest complexity, distinct model (Nemotron) |
| `autonomic` | Autonomic NS | Real-time PID needs dedicated loop |
| `endocrine-immune` | Endocrine + Immune | Both circadian, both surveillance/growth, shared model (DeepSeek-R1) |
| `circulatory-skeletal` | Circulatory + Skeletal | Both continuous, registry/transport, shared model (LLM) |
| `orchestrator` | Integration (Hypothalamus) | Routes Telegram → Kanban, distinct from execution |

### Full Physiological Fidelity (6 Profiles, No Separate Orchestrator) — **Implemented in This Session**
| Profile | Body System | Model | Why Separate |
|---|---|---|---|
| `morphogen` | Skeletal (Registry/Identity) | Nemotron-3-Ultra | Registry is foundational — all others depend on it; also serves as Telegram entry point |
| `wave` | Brain/CNS (Coaching/Mastermind) | Nemotron-3-Ultra | Highest complexity: coaching + mastermind + resonance; event-driven |
| `quartz` | Autonomic NS (PID/Lattice) | Gemini-2.5-Flash | Real-time PID/lattice control needs dedicated fast model |
| `seed` | Endocrine/Growth (Avrami/Landau) | DeepSeek-R1 | Growth/evolution is slow, distinct reasoning model for developmental logic |
| `allostasis` | Immune/Homeostatic (Surveillance) | LLM-4.5-Air | Surveillance/diagnosis runs on different timescale; needs health-scoring skills |
| `harvey` | Circulatory (Transport/Registry) | LLM-4.5-Air | Transport/registry is communication backbone; fleet analytics consumer |

**Key difference:** `morphogen` absorbs the orchestrator role (Telegram → Kanban dispatch) because the Skeletal/Registry system is the natural entry point for external signals — it maintains the organism's identity map.

## Morphogen Engine Genotype Registration

Each profile registers itself on startup via the Morphogen Engine API (port 8093):

```bash
# Start Morphogen Engine first
cd /<workspace> && python run_server.py &

# Then register each profile (or use the automated script below)
curl -X POST http://127.0.0.1:port/genotypes/register \
  -H "Content-Type: application/json" \
  -d '{
    "engine_id": "morphogen",
    "name": "Morphogen Profile (Skeletal System)",
    "version": "1.0.0",
    "body_system": "skeletal_registry",
    "scientist": "Francis Paxton (BMPs)",
    "port": 8093,
    "capabilities": [
      {"name": "registry", "version": "1.0"},
      {"name": "gradients", "version": "1.0"},
      {"name": "contracts", "version": "1.0"},
      {"name": "kanban_orchestration", "version": "1.0"}
    ]
  }'

curl -X POST http://127.0.0.1:port/genotypes/register \
  -H "Content-Type: application/json" \
  -d '{
    "engine_id": "wave",
    "name": "Wave Profile (Brain/CNS)",
    "version": "1.0.0",
    "body_system": "brain_cns",
    "scientist": "Kuramoto",
    "port": 8000,
    "capabilities": [
      {"name": "coaching", "version": "2.0"},
      {"name": "mastermind", "version": "2.0"},
      {"name": "resonance", "version": "2.0"},
      {"name": "kanban_orchestration", "version": "1.0"}
    ]
  }'

# ... repeat for quartz, seed, allostasis, harvey
```

**Automated registration script:** See `scripts/create-body-system-profiles.sh` (creates profiles AND registers genotypes).

## Kanban Task Routing by Body System (6-Profile Architecture)

| Task Type | Kanban Assignee | Body System | Example |
|---|---|---|---|
| Coaching request | `wave` | Brain/CNS | "Coach me on sleep optimization" |
| Mastermind session | `wave` | Brain/CNS | "Run advisory panel on product strategy" |
| Resonance analysis | `wave` | Brain/CNS | "Match coaching to my 8D frequencies" |
| Task regulation | `quartz` | Autonomic NS | "Regulate my daily task lattice" |
| PID adjustment | `quartz` | Autonomic NS | "Tune task homeostasis parameters" |
| Lattice maintenance | `quartz` | Autonomic NS | "Rebuild task dependency graph" |
| Health scoring (8D/TWC) | `allostasis` | Immune/Homeostatic | "Run daily 8D/TWC rescore" |
| Fleet surveillance | `allostasis` | Immune/Homeostatic | "Scan for TWC < 5.5 agents" |
| Diagnosis/Intervention | `allostasis` | Immune/Homeostatic | "Diagnose agent failure root cause" |
| Growth signaling | `seed` | Endocrine/Growth | "Execute Avrami JMAK phase transition" |
| Developmental milestone | `seed` | Endocrine/Growth | "Assess SOC criticality, CPM patterns" |
| Analytics sync | `harvey` | Circulatory | "Sync OpenClaw fleet data" |
| Registry update | `morphogen` | Skeletal/Registry | "Register new agent genotype" |
| Agent spawning | `morphogen` → FORGE/ARBITER | Integration | "Spawn new researcher agent" |

## Memory Isolation Boundaries (6-Profile Architecture)

```
<agent-home>/profiles/
├── morphogen/
│   ├── memories/           # Genotype registry, organism identity map, task graph
│   ├── state.db            # Morphogen session transcripts (Telegram + Kanban dispatch)
│   ├── skills/             # hermes-agent, kanban-orchestrator
│   └── cron/               # Continuous registry maintenance
├── wave/
│   ├── memories/           # Coaching context, 8D patterns, resonance frequencies, mastermind insights
│   ├── state.db            # CNS session transcripts
│   ├── skills/             # kanban-orchestrator, ds-wave-coaching
│   └── cron/               # Event-driven only
├── quartz/
│   ├── memories/           # PID state, lattice config, task patterns, regulation history
│   ├── state.db            # Autonomic session transcripts
│   ├── skills/             # kanban-worker, quartz-lattice
│   └── cron/               # Ultradian 5-min PID loop
├── seed/
│   ├── memories/           # Growth trajectories, Avrami/Landau/SOC/CPM states, developmental milestones
│   ├── state.db            # Endocrine session transcripts
│   ├── skills/             # kanban-worker
│   └── cron/               # Circadian daily (03:00)
├── allostasis/
│   ├── memories/           # Threat logs, diagnoses, surveillance history, intervention outcomes
│   ├── state.db            # Immune session transcripts
│   ├── skills/             # aisha-md-health-orchestration, sentinel-compliance-audit, health-scoring-daily-pipeline
│   └── cron/               # Circadian hourly + daily
├── harvey/
│   ├── memories/           # Transport state, fabric registry, genotype map, fleet analytics cache
│   ├── state.db            # Circulatory session transcripts
│   ├── skills/             # sibling-agent-fleet-analytics, sibling-agent-fleet-analytics-summary
│   └── cron/               # Continuous 15-min sync
```

**Cross-profile leakage = autoimmune disease.** Each profile's `memories/` is strictly isolated. Use Kanban tasks (hormones) and Morphogen gradients (positional signals) for communication.

## Cross-Profile Communication Protocol

**NEVER** share memory directly. Use:

1. **Kanban tasks** — Typed, routed, with `parents=` dependencies
2. **Morphogen gradients** — Positional signals via Engine API
3. **Schema contracts** — Typed interfaces between engines
4. **Developmental signals** — Broadcast morphogens for organism-wide state

## Verification Checklist (6-Profile Architecture)

- [ ] Each of 6 profiles registered with Morphogen Engine (`POST /genotypes/register`)
- [ ] Kanban dispatcher routes to correct profile assignees (`wave`, `quartz`, `seed`, `allostasis`, `harvey`, `morphogen`)
- [ ] Telegram routes to `morphogen` profile (registry entry point)
- [ ] Cron rhythms match biological table in `cron-rhythms.md`
- [ ] Memory isolation: no cross-profile `memories/` leakage
- [ ] FORGE/ARBITER evaluates spawns per body system
- [ ] Morphogen gradients flow: `morphogen` → `wave`/`quartz`/`seed`/`allostasis`/`harvey`
- [ ] `morphogen` profile has `kanban-orchestrator` skill for Telegram → Kanban decomposition