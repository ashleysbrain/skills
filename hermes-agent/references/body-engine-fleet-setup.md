# Body Engine Fleet Setup — the operator agent Profile Architecture for Divinity Science

## Overview
This reference documents the correct the operator agent profile architecture for running the DS 4-engine fleet (Wave, Quartz, Diviq, Seed) plus Morphogen registry, with a single patient interface profile.

## The 4-Engine Fleet (from ds-genesis-engine/VERSION.md)

| Engine | Port | Body System | Scientist | Capability |
|--------|------|-------------|-----------|------------|
| **Wave** | 8000 | Brain/CNS | Kuramoto | Coaching, Resonance, Mastermind |
| **Quartz** | 8089 | Autonomic NS | Diviq | Lattice, Tasks, PID Control |
| **Diviq (Self-Healing)** | 8091 | Immune/Homeostatic | Sterling | Surveillance, Diagnosis, Intervention |
| **Seed** | 8090 | Endocrine/Growth | Waddington | Avrami/JMAK, Landau, SOC, CPM |

**Morphogen Engine** (port 8093) = Skeletal/Registry — registers all 4 engines, provides identity/contracts/gradients.

## the operator agent Profile Fleet

### Builder Fleet (5 profiles — one per engine + registry)
| Profile | Builds | Model | Key Skills |
|---------|--------|-------|------------|
| `morphogen` | Morphogen Engine (registry) | Nemotron-3-Ultra | hermes-agent, kanban-orchestrator |
| `wave` | Wave Engine (coaching) | Nemotron-3-Ultra | hermes-agent, kanban-orchestrator |
| `quartz` | Quartz Engine (tasks/PID) | Gemini-2.5-Flash | hermes-agent, kanban-worker |
| `seed` | Seed Engine (product dev) | DeepSeek-R1 | hermes-agent, kanban-worker |
| `diviq` | Diviq Engine (self-healing) | LLM-4.5-Air | aisha-md-health-orchestration, sentinel-compliance-audit |

### Patient Interface Fleet (1 profile)
| Profile | Purpose | Model | Key Skills |
|---------|---------|-------|------------|
| `principal-interface` | Single Telegram/voice contact → calls engine APIs → returns coaching | Nemotron-3-Ultra | aisha-md-health-orchestration, hermes-agent |

## Critical Routing Rule: Sensory Input → Brain/CNS (Wave)

**Physiological principle:** Sensory neurons → spinal cord → brainstem → thalamus → cortex (Wave). The skeleton (Morphogen) provides structural identity but does NOT receive sensory input.

```bash
# CORRECT: Telegram routes to Wave (brain)
hermes config set telegram.default_profile "wave"

# WRONG: Telegram routes to Morphogen (skeleton)
hermes config set telegram.default_profile "morphogen"
```

## Setup Commands

```bash
# 1. Create builder profiles (cloned from default)
hermes profile create morphogen --clone
hermes profile create wave --clone
hermes profile create quartz --clone
hermes profile create seed --clone
hermes profile create diviq --clone

# 2. Configure models
hermes -p morphogen config set model.default "openrouter/nvidia/nemotron-3-ultra:free"
hermes -p wave config set model.default "openrouter/nvidia/nemotron-3-ultra:free"
hermes -p quartz config set model.default "openrouter/google/gemini-2.5-flash"
hermes -p seed config set model.default "openrouter/deepseek/deepseek-r1:free"
hermes -p diviq config set model.default "openrouter/z-ai/glm-4.5-air:free"

# 3. Install skills (copy from main skills dir)
# Builder skills
cp -r skills-library/autonomous-ai-agents/hermes-agent <agent-home>/profiles/morphogen/skills/
cp -r skills-library/autonomous-ai-agents/hermes-agent <agent-home>/profiles/wave/skills/
cp -r skills-library/autonomous-ai-agents/hermes-agent <agent-home>/profiles/quartz/skills/
cp -r skills-library/autonomous-ai-agents/hermes-agent <agent-home>/profiles/seed/skills/
cp -r skills-library/autonomous-ai-agents/hermes-agent <agent-home>/profiles/diviq/skills/

cp -r skills-library/devops/kanban-orchestrator <agent-home>/profiles/morphogen/skills/
cp -r skills-library/devops/kanban-orchestrator <agent-home>/profiles/wave/skills/
cp -r skills-library/devops/kanban-worker <agent-home>/profiles/quartz/skills/
cp -r skills-library/devops/kanban-worker <agent-home>/profiles/seed/skills/
cp -r skills-library/operations/aisha-md-health-orchestration <agent-home>/profiles/diviq/skills/
cp -r skills-library/compliance/sentinel-compliance-audit <agent-home>/profiles/diviq/skills/

# 4. Create patient interface profile
hermes profile create principal-interface --clone
hermes -p principal-interface config set model.default "openrouter/nvidia/nemotron-3-ultra:free"
cp -r skills-library/autonomous-ai-agents/hermes-agent <agent-home>/profiles/principal-interface/skills/
cp -r skills-library/operations/aisha-md-health-orchestration <agent-home>/profiles/principal-interface/skills/

# 5. Route Telegram to Wave (brain)
hermes config set telegram.default_profile "wave"
hermes gateway restart

# 6. Start Morphogen Engine registry
cd ~/your-workspace/ds-morphogen-engine && python run_server.py &

# 7. Register engines with Morphogen (auto-happens on server startup via KNOWN_ENGINES)
curl http://127.0.0.1:port/organism/map
```

## Common Pitfalls

1. **Routing Telegram to Morphogen** — Morphogen is the skeleton/registry, not the brain. Sensory input must enter through Wave (CNS).
2. **Adding extra engines** — The fleet is 4 engines + Morphogen registry. No "Bernard engine," no "Harvey engine" (circulatory is handled by Harvey transport inside Morphogen, not a separate profile).
3. **Creating patient fleet mirroring builder fleet** — Overcomplicates. One patient interface profile calls engine APIs directly.
4. **Forgetting to restart gateway after config change** — `hermes gateway restart` required for Telegram routing changes.
5. **Running multiple gateway instances** — Kill stale processes: `pkill -f "gateway run"` before restart.

## Verification Checklist

- [ ] `hermes profile list` shows 6 profiles: morphogen, wave, quartz, seed, diviq, principal-interface
- [ ] `curl http://127.0.0.1:port/organism/map` returns 5 engines (wave, quartz, seed, diviq, morphogen)
- [ ] Telegram message routes to Wave profile (check gateway logs: `inbound message: platform=telegram`)
- [ ] Each builder profile has correct model and skills installed
- [ ] Patient interface profile can call engine APIs (test: `curl http://127.0.0.1:port/health` from principal-interface session)