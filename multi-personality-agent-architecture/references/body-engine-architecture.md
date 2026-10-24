# Body-Engine Architecture Mapping

## 4-Engine Fleet + Morphogen Registry (from ds-genesis-engine/VERSION.md)

| Engine | Port | Body System | Scientist | Capability | Builder Profile |
|--------|------|-------------|-----------|------------|-----------------|
| **Wave** | 8000 | Brain/CNS | Kuramoto | Coaching, Resonance, Mastermind | wave |
| **Quartz** | 8089 | Autonomic NS | Diviq | Lattice, Tasks, PID Control | quartz |
| **Diviq (Self-Healing)** | 8091 | Immune/Homeostatic | Sterling | Surveillance, Diagnosis, Intervention | diviq |
| **Seed** | 8090 | Endocrine/Growth | Waddington | Avrami/JMAK, Landau, SOC, CPM | seed |
| **Morphogen** | 8093 | Skeletal/Registry | Francis Paxton | Identity, Contracts, Gradients | morphogen |

## Key Principles

1. **Sensory input → Brain first** — Telegram routes to Wave (Brain/CNS), not Morphogen (Skeleton)
2. **Builder fleet = 1 profile per engine** — Each builder profile owns one FastAPI service
3. **Patient interface = 1 profile** — Single `principal-interface` profile calls all engine APIs
4. **No patient agent fleet needed** — Engine math lives in FastAPI, not in the operator agent agents
5. **Harvey (Circulatory, port 8092) is extra** — Not in 4-engine fleet; remove or repurpose

## Morphogen Engine Registration (server.py KNOWN_ENGINES)

```python
KNOWN_ENGINES = [
    EngineGenotype(
        engine_id="morphogen",
        name="Morphogen Engine",
        version="1.0.0",
        body_system="skeletal_registry",
        scientist="Francis_Paxton",
        port=8093,
        capabilities=[
            EngineCapability(name="registry", version="1.0"),
            EngineCapability(name="gradients", version="1.0"),
            EngineCapability(name="contracts", version="1.0"),
        ],
    ),
    EngineGenotype(
        engine_id="wave",
        name="Wave Engine",
        version="2.0.0",
        body_system="brain_cns",
        scientist="Kuramoto",
        port=8000,
        capabilities=[
            EngineCapability(name="coaching", version="2.0"),
            EngineCapability(name="mastermind", version="2.0"),
            EngineCapability(name="resonance", version="2.0"),
        ],
    ),
    EngineGenotype(
        engine_id="quartz",
        name="Quartz Engine",
        version="2.0.0",
        body_system="autonomic_ns",
        scientist="Diviq",
        port=8089,
        capabilities=[
            EngineCapability(name="lattice", version="2.0"),
            EngineCapability(name="tasks", version="2.0"),
            EngineCapability(name="pid_control", version="2.0"),
        ],
    ),
    EngineGenotype(
        engine_id="diviq",
        name="Diviq Engine (Self-Healing)",
        version="1.0.0",
        body_system="immune_homeostatic",
        scientist="Sterling",
        port=8091,
        capabilities=[
            EngineCapability(name="surveillance", version="1.0"),
            EngineCapability(name="diagnosis", version="1.0"),
            EngineCapability(name="intervention", version="1.0"),
        ],
    ),
    EngineGenotype(
        engine_id="seed",
        name="Seed Engine",
        version="2.0.0",
        body_system="endocrine_growth",
        scientist="Waddington",
        port=8090,
        capabilities=[
            EngineCapability(name="avrami_jmak", version="2.0"),
            EngineCapability(name="landau_phase", version="2.0"),
            EngineCapability(name="soc", version="2.0"),
            EngineCapability(name="cpm", version="2.0"),
        ],
    ),
]
```

## Patient Interface Profile

```bash
# Single profile for the principal's Telegram/voice interface
hermes profile create principal-interface --clone
hermes -p principal-interface config set model.default "openrouter/nvidia/nemotron-3-ultra:free"
hermes -p principal-interface skills install aisha-md-health-orchestration hermes-agent kanban-orchestrator

# Route Telegram here
hermes config set telegram.default_profile "principal-interface"
```

This profile's job:
1. Receive Telegram/voice/photos
2. Parse intent ("log sleep 6.5", "pain 7/10", "coach me")
3. Call engine APIs directly (HTTP to localhost:port, :port, :port, :port, :port)
4. Return computed coaching to user

## Telegram Routing Fix

```bash
# FIX: Route Telegram to Wave (Brain/CNS), not Morphogen
hermes config set telegram.default_profile "wave"
hermes gateway restart
```

**Why:** In physiology, sensory input → spinal cord → brainstem → thalamus → cortex (Wave). The skeleton (Morphogen) provides structural identity but doesn't receive sensory input.