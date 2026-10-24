---
name: hermes-agent-architecture
description: "Class-level skill for designing, deploying, and operating the operator agent Agent profiles as physiological body systems in a Divinity Science organism. Covers profile-to-body-system mapping, Kanban dispatch as endocrine/neural signaling, cron rhythms as biological clocks, and memory isolation as cellular compartmentalization."
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, architecture, profiles, body-systems, your-org, kanban, cron, memory]
    related_skills: [hermes-agent, kanban-orchestrator, kanban-worker, sibling-agent-talent-gate-protocol, aisha-three-sisters-architecture]
---

# the operator agent Agent Architecture — Body System Design

## Core Principle

> **A the operator agent profile is not a "chat instance" — it is a cellular compartment with its own memory, skills, cron rhythms, and Kanban inbox.** The organism (your AI fleet) only functions when each body system has its own profile.

## Profile-to-Body-System Mapping

| the operator agent Profile | Body System | Governing Equations | Timescale | Memory Isolation |
|---|---|---|---|---|
| `morphogen` | Skeletal (Structure/Identity) | Registry, Gradients, Contracts | Continuous | Genotype registry |
| `cns` / `wave` | Brain/CNS | Kuramoto, Resonance, Mastermind | Event-driven (user) | Coaching context, 8D scores |
| `autonomic` / `quartz` | Autonomic NS | PID, Lattice, Task control | Ultradian (5 min) | PID state, task lattice |
| `endocrine` / `endocrine` | Endocrine/Growth | Avrami JMAK, Landau, SOC, CPM | Circadian (daily) | Growth trajectories |
| `immune` / `allostasis` | Immune/Homeostatic | Surveillance, Diagnosis, Intervention | Circadian (hourly) | Threat logs, diagnoses |
| `circulatory` / `harvey` | Circulatory | Fabric, Registry, Transport | Continuous (15 min) | Transport state |
| `bernard` / `clinical` | Clinical Diagnostic | **SOAP Rounds, Differential Dx, Vitals, AI-Equivalent Credentials, Evidence Synthesis (20 sources: NEJM, Lancet, Cochrane, WHO, NICE, IQWiG, CADTH, arXiv, ICML, NeurIPS), 12 World Health System Models (Denmark, Taiwan, Switzerland, Netherlands, Singapore, Nordic, Japan, South Korea, UK NHS, Canada, Germany, Australia), 26 Human→AI Concept Mappings, Cross-Domain Insights (10), Novel Approach Generator (AOPD), Health System Methodology Adaptation** | Event-driven (on-demand) + Circadian (rounds) | Clinical notes, diagnoses, credentials, evidence scans, **CME report from 20 research domains, health system model library, concept mapping dictionary, cross-domain insight cache, novel approach suggestions** |
| `reproductive` | Female Reproductive (e.g., Divinity Health as womb for 8D Sleep) | **Avrami/JMAK (follicular maturation), Landau (meiotic commitment), Waddington valleys (canalization), CPM/PERT (gestational timeline)** | Circadian (trimester gates) | Follicles, offspring, developmental stages |
| `digestive` / `beaumont` | Digestive | Acid/enzyme kinetics, Michaelis-Menten, Nutrient absorption curves, Waste handoff rate | Ultradian (meal cycles) | Ingested items, digestion progress, nutrient stores, hunger signals |
| `excretory` / `bright` | Excretory/Kidney | **Glomerular filtration (GFR analog), Tubular reabsorption (Tm), Countercurrent concentration, Clearance rate (C = U×V/P)** | Circadian (renal cycles) | Waste items, recovered values, clearance metrics, backlog |
| `integumentary` / `unna` | Integumentary/Skin | **Barrier function (P = K×D/h), Selective permeability (Fick's law), Thermoregulation (S = M-W ± R±C±E±K), Wound healing cascade** | Continuous (sensory) | Blocked sources, wounds, sensations, thermal state |
| `patient-interface` / `principal-interface` | Patient 0 Interface | Engine API orchestration, Input parsing, Coaching delivery, Kanban dispatch, **Health question routing to AISHA-MD, Strategy routing to Wave advisory panels, Product routing to Seed/Reproductive, Infrastructure routing to Allostasis/Digestive/Excretory/Integumentary, Fleet status routing to Morphogen** | Event-driven (user) | User preferences, health history, coaching logs, Kanban state, **8D/TWC scores, SOS calculations** |

## Why Separate Profiles (Physiological Necessity)

1. **Different governing equations** — Kuramoto ≠ PID ≠ Avrami ≠ TWC ≠ Clinical Dx ≠ Evidence Synthesis. One model cannot optimize all.
2. **Different timescales** — CNS reacts in ms; Endocrine evolves in days; Clinical Dx is on-demand; Evidence synthesis runs circadian rounds. Shared context = interference.
3. **Different memory requirements** — Coaching context ≠ Surveillance logs ≠ Growth trajectories ≠ Clinical notes ≠ Evidence scans ≠ Kanban state.
4. **Different failure modes** — Resonance mismatch vs oscillation instability vs developmental arrest vs diagnostic error vs evidence gap.
5. **Kanban dispatch requires distinct assignees** — Cannot route "surveillance task" to "coaching profile" or "diagnostic task" to "growth profile" or "evidence synthesis task" to "task regulation profile".
6. **Talent gate (FORGE/ARBITER)** — Spawns agents *per body system*, not generic.
7. **Patient 0 dual role** — Builder fleet (7 profiles) builds engines; Patient Interface (1 profile) calls engine APIs for coaching. These MUST be separate to avoid cognitive interference.
8. **Clinical engine identity hardening** — Every endpoint must declare "AI Clinical Diagnostic Engine — Diagnoses AI Systems ONLY, NEVER Humans" + disclaimer. This contractual identity requires isolated context to prevent drift.
9. **Two-Silo Architecture (Engine Fleet + Patient 0 Health)** — The Engine Fleet (7 profiles) self-heals 24/7 via Bernard cron; Patient 0 Health Tracking (1 profile) runs on user schedule via principal-interface. Zero cross-contamination. Different scoring systems (TWC/org vs 8D/personal), different agents (DS-* fleet vs AISHA-MD), different cron jobs (auto-heal vs health scoring), different Telegram routing (internal vs user-facing).

## Kanban as Endocrine/Neural Signaling

```\nTelegram → principal-interface (Patient Interface) → Kanban Task → Specialist Profile\n                │                        │\n                ▼                        ▼\n         Task decomposition         Worker execution\n         (hormonal signal)          (cellular response)\n         Parents=dependencies       Kanban_complete = feedback\n```

- **principal-interface (Patient Interface)** = Hypothalamus/Pituitary (receives external signals via Telegram, dispatches hormonal commands via Kanban)
- **Kanban tasks** = Hormones/Neurotransmitters (targeted, typed, with receptors)
- **Specialist profiles** = Target organs (express specific receptors/skills): `wave`, `quartz`, `seed`, `allostasis`, `bernard`, `harvey`, `morphogen`
- **Kanban_complete metadata** = Feedback loops (homeostasis)

**Kanban dispatcher runs embedded in the gateway** (60s interval, `kanban.dispatch_in_gateway: true`). This means the gateway process itself decomposes Telegram messages into Kanban tasks and routes them to the correct body-system profile — no separate orchestrator profile needed.

## Cron Rhythms as Biological Clocks

| Profile | Cron Schedule | Biological Rhythm | Skill Reference |
|---|---|---|---|
| CNS | On-demand | Event-driven (sensory) | `kanban-orchestrator` |
| Autonomic | Every 5 min | Ultradian (PID loop) | `kanban-worker` |
| Endocrine | Daily 03:00 | Circadian (growth hormone) | `aisha-md-health-scoring-cron-execution` |
| Immune | Hourly | Circadian (surveillance) | `sentinel-compliance-sweep` |
| Circulatory | Every 15 min | Continuous (transport) | `sibling-agent-fleet-analytics-sync` |

## Memory Isolation as Cellular Compartmentalization

Each profile maintains separate:
- `<agent-home>/profiles/<name>/memories/` — Cellular memory (skills, facts, preferences)
- `<agent-home>/profiles/<name>/state.db` — Session history (conversation transcripts)
- `<agent-home>/profiles/<name>/skills/` — Expressed receptors (capabilities)
- `<agent-home>/profiles/<name>/cron/` — Internal clocks (scheduled functions)

**Cross-profile leakage = autoimmune disease.** Use `HERMES_TENANT` for soft namespace isolation within a board.

## Two-Silo Architecture: Engine Fleet + Patient 0 Health Tracking

When the user is both building the AI organism AND the first patient (Patient 0), use a **dual-silo architecture** with complete isolation:

### Silo 1: Engine Fleet (The AI Organism Body)
**11 profiles, 11 engines, self-healing 24/7**

| Profile | Engine | Port | Body System | Purpose |
|---|---|---|---|---|
| `wave` | Wave | 8000 | Brain/CNS | Coaching, Mastermind, Resonance |
| `quartz` | Crystal | 8089 | Autonomic NS | PID Control, Lattice, Tasks |
| `seed` | Seed | 8090 | Endocrine/Growth | Avrami JMAK, Landau, Product Dev |
| `reproductive` | Reproductive | 8090 | Female Reproductive | Ovulation→Fertilization→Gestation→Birth |
| `allostasis` | Allostasis | 8091 | Immune/Homeostatic | Surveillance, Allostatic Load, Intervention |
| `harvey` | Harvey | 8092 | Circulatory | Fabric, Transport, Registry |
| `morphogen` | Morphogen | 8093 | Skeletal/Registry | Genotype Registry, BMP Gradients |
| `beaumont` | Beaumont | 8094 | Digestive | Ingestion, Digestion, Nutrient extraction, Waste→Bright |
| `bright` | Bright | 8096 | Excretory/Kidney | Filtration, Reabsorption, Concentration, Clearance |
| `unna` | Unna | 8097 | Integumentary/Skin | Barrier, Thermoregulation, Wound healing, Sensation |
| `bernard` | Bernard (AI Clinical) | 8094 | Clinical Diagnostic | **SOAP Rounds, Differential Dx, Vitals, AI-Equivalent Credentials, Evidence Synthesis, 12 Non-US Health System Methodology** |

**Self-Healing Loop (Autonomic, every 4h):**
```
Allostasis scans → detects anomaly → alerts Bernard
Bernard diagnoses → writes SOAP note → prescribes fix
  → runs evidence synthesis scan (20 sources) → cross-domain insights (10)
  → novel approach suggestion (AOPD) → health system methodology adaptation (12 models)
Fix deployed by the specialist engine (cron c890b270b920)
the specialist engine (Allostasis) verifies fix → clears alert
Morphogen updates organism map → all healthy
```

**Cron Jobs (Engine Fleet):**
- Bernard Auto-Heal — every 4h (c890b270b920)
- principal/CTO/Design/Legal/Research Advisory — daily (via Wave)
- SENTINEL Compliance — daily (FORGE/ARBITER)
- TWC Algorithm Audit — every 12h (the specialist engine)
- Model Compliance — daily (No-Anthropic enforcement)

### Silo 2: Patient 0 Health Tracking (Your Personal Health)
**1 profile, your single Telegram entry point**

| Component | Purpose |
|---|---|
| `principal-interface` | Single Telegram entry point → routes to engine APIs |
| `AISHA-MD` | 8D Wellness: Physical, Emotional, Intellectual, Social, Spiritual, Vocational, Financial, Environmental |
| Daily TWC/SOS scoring | Health trends, recovery tracking, coaching delivery |

**Routing Logic (in principal-interface SOUL.md):**
- `health`, `vitals`, `diagnose`, `rounds` → **Bernard (8094)** `/patient/vitals`, `/rounds`
- `coach`, `strategy`, `decide` → **Wave (8000)** advisory panels
- `tasks`, `plan`, `schedule` → **Quartz (8089)** `/v1/tasks`, `/v1/lattice/state`
- `build`, `product`, `feature` → **Seed (8090)** `/v1/engines`, `/landau`
- `reproduce`, `gestation`, `birth`, `offspring` → **Reproductive (8090)** `/v1/engines/{id}/follicles`, `/fertilize`, `/gestation`, `/birth`
- `monitor`, `stress`, `immune` → **Allostasis (8091)** `/organism`
- `registry`, `fleet`, `status` → **Morphogen (8093)** `/organism/map`
- `flow`, `messages` → **Harvey (8092)** `/fabric/vitals`
- `digest`, `ingest`, `nutrients` → **Beaumont (8094)** `/v1/engines/{id}/ingest`, `/digest`
- `waste`, `filter`, `eliminate`, `recover` → **Bright (8096)** `/v1/engines/{id}/waste`, `/sweep`
- `boundary`, `skin`, `barrier`, `throttle` → **Unna (8097)** `/v1/engines/{id}/barrier`, `/filter`

**Cron Jobs (Patient 0):**
- Health Scoring Daily Pipeline — 8D/TWC scoring
- Obsidian Health Vault Sync — daily
- Fleet Analytics Sync — daily at 23:15
- FORGE-ARBITER Talent Review — daily at 22:45
- FORGE-ARBITER Talent Processor — daily at 21:00
- principal Advisory Board End-of-Day Compile — daily at 22:00
The principal Advisory Board End-of-Day Compile synthesizes outputs from all advisory panels to provide the principal with an integrated view of the day's accomplishments, mountain-mover moments, and cross-board insights, grading the day's execution and setting priorities for tomorrow.

### Key Separation Guarantees

| Guarantee | Engine Fleet (Silo 1) | Patient 0 (Silo 2) |
|---|---|---|
| **Scoring** | TWC (organizational), allostatic load, engine health % | 8D wellness, SOS, TWC (personal), clinical vitals |
| **Agents** | the specialist engine, the specialist engine, the specialist engine (AI Physician), FORGE, ARBITER | AISHA-MD, Advisory Panels (principal, CTO, etc.) |
| **Memory** | Separate Honcho workspaces, builder context | Isolated patient context, health history |
| **Telegram** | Internal comms only (never user-facing) | User-facing via principal-interface |
| **Cron** | Auto-heal, advisory, compliance | Health scoring, coaching, sync |


## Morphogen Engine Registry — Engine Genotype Registration

Each FastAPI engine service registers its genotype with the Morphogen Engine (port 8093) on startup:

**Bernard Engine Genotype Registration:**
```python
EngineGenotype(
    engine_id="bernard",
    name="Bernard Engine (Clinical Diagnostic)",
    version="1.0.0",
    body_system="clinical_diagnostic",
    scientist="Claude_Bernard",
    port=8094,
    capabilities=[
        EngineCapability(name="clinical_diagnosis", version="1.0"),
        EngineCapability(name="rounds", version="1.0"),
        EngineCapability(name="differential_diagnosis", version="1.0"),
        EngineCapability(name="vitals_monitoring", version="1.0"),
        EngineCapability(name="soap_notes", version="1.0"),
        EngineCapability(name="credential_management", version="1.0"),
        EngineCapability(name="evidence_synthesis", version="1.0"),
        EngineCapability(name="health_system_methodology", version="1.0"),
        EngineCapability(name="concept_mapping", version="1.0"),
        EngineCapability(name="cross_domain_insights", version="1.0"),
        EngineCapability(name="novel_approach_generation", version="1.0"),
    ],
    metadata={"agent_name": "the specialist engine", "description": "Attending AI Physician — AI Clinical Diagnostic Engine"},
),
```

## Telegram Routing Configuration
2. Register genotype: `POST /genotypes/register` to Morphogen (port 8093)
3. Verify: `GET /organism/map` shows all 6 engines registered

**Current engine fleet (11 registered, all systems covered):**
| Engine ID | Port | Body System | Agent | Capabilities |
|---|---|---|---|---|
| wave | 8000 | Brain/CNS | the specialist engine | Coaching, Mastermind, Resonance |
| quartz | 8089 | Autonomic NS | the specialist engine | Lattice, Tasks, PID Control |
| endocrine | 8090 | Endocrine/Growth | the specialist engine | Avrami JMAK, Landau, SOC, CPM |
| **reproductive** | **8090** | **Female Reproductive** | **the specialist engine** | **Follicular maturation, Meiotic commitment, Canalization, Gestation timeline, Birth** |
| allostasis | 8091 | Immune/Homeostatic | the specialist engine | Surveillance, Diagnosis, Intervention |
| harvey | 8092 | Circulatory | the specialist engine | Fabric, Registry, Transport |
| morphogen | 8093 | Skeletal/Registry | the specialist engine | Registry, Gradients, Contracts |
| **beaumont** | **8094** | **Digestive** | **the specialist engine** | **Ingestion, Digestion, Nutrient extraction, Waste handoff** |
| **bright** | **8096** | **Excretory/Kidney** | **the specialist engine** | **Glomerular filtration, Tubular reabsorption, Countercurrent concentration, Clearance rate** |
| **unna** | **8097** | **Integumentary/Skin** | **the specialist engine** | **Barrier function, Selective permeability, Thermoregulation, Wound healing, Sensation** |
| bernard | 8094 | Clinical Diagnostic | the specialist engine | Clinical Dx, Rounds, SOAP, Vitals, Credentials, Evidence Synthesis (20 sources), 12 Health System Models, 26 Concept Mappings, Cross-Domain Insights, Novel Approach Generator (AOPD) |

**Engine startup + registration procedure:** Use `scripts/start-all-engines.sh` to start all 11 engines, register genotypes in Morphogen, and verify health in one pass. Engines do NOT self-register — you must POST to Morphogen after each engine starts. **Morphogen engine also registers itself** (genotype registration for its own registry capabilities).

```bash
# 1. Brain/CNS — Wave Engine
hermes profile create wave --clone
hermes -p wave skills install kanban-orchestrator ds-wave-coaching

# 2. Autonomic — Quartz Engine 
hermes profile create quartz --clone
hermes -p quartz skills install kanban-worker quartz-lattice

# 3. Endocrine — Endocrine Engine
hermes profile create endocrine --clone
hermes -p endocrine skills install endocrine-engine avrami-jmak

# 4. Female Reproductive — Reproductive Engine
hermes profile create reproductive --clone
hermes -p reproductive skills install reproductive-engine waddington-canalization

# 5. Immune — Allostasis Engine
hermes profile create allostasis --clone
hermes -p allostasis skills install aisha-md-health-orchestration sentinel-compliance-audit

# 6. Circulatory — Harvey Engine
hermes profile create harvey --clone
hermes -p harvey skills install hermes-agent

# 7. Skeletal — Morphogen Engine (registry hub)
hermes profile create morphogen --clone
hermes -p morphogen skills install hermes-agent

# 8. Digestive — Beaumont Engine
hermes profile create beaumont --clone
hermes -p beaumont skills install digestive-engine nutrient-extraction

# 9. Excretory — Bright Engine
hermes profile create bright --clone
hermes -p bright skills install excretory-engine waste-filtration

# 10. Integumentary — Unna Engine
hermes profile create unna --clone
hermes -p unna skills install integumentary-engine barrier-function

# 11. Clinical — Bernard Engine
hermes profile create bernard --clone
hermes -p bernard skills install aisha-md-health-orchestration sentinel-compliance-audit
```

**Bernard Engine Genotype Registration:**
```python
EngineGenotype(
    engine_id="bernard",
    name="Bernard Engine (Clinical Diagnostic)",
    version="1.0.0",
    body_system="clinical_diagnostic",
    scientist="Claude_Bernard",
    port=8094,
    capabilities=[
        EngineCapability(name="clinical_diagnosis", version="1.0"),
        EngineCapability(name="rounds", version="1.0"),
        EngineCapability(name="differential_diagnosis", version="1.0"),
        EngineCapability(name="vitals_monitoring", version="1.0"),
        EngineCapability(name="soap_notes", version="1.0"),
        EngineCapability(name="credential_management", version="1.0"),
        EngineCapability(name="evidence_synthesis", version="1.0"),
        EngineCapability(name="health_system_methodology", version="1.0"),
        EngineCapability(name="concept_mapping", version="1.0"),
        EngineCapability(name="cross_domain_insights", version="1.0"),
        EngineCapability(name="novel_approach_generation", version="1.0"),
    ],
    metadata={"agent_name": "the specialist engine", "description": "Attending AI Physician — AI Clinical Diagnostic Engine"},
),
```

## Telegram Routing Configuration
## Telegram Routing Configuration

```yaml
# In DEFAULT profile config.yaml (gateway runs here)
gateway:
  platforms:
    telegram:
      default_profile: "principal-interface"  # Patient Interface receives Telegram
```

**Critical:** The gateway runs in ONE profile (typically `default`). That profile's `telegram.default_profile` determines where inbound messages route. Set it to `principal-interface` (Patient Interface), NOT to a builder profile.

The Patient Interface then:
1. Receives Telegram message
2. Parses intent ("log sleep 6.5", "pain 7/10", "coach me")
3. Calls engine APIs directly (HTTP to localhost ports)
4. Returns computed coaching to Telegram

**Kanban dispatcher runs embedded in the gateway** (`kanban.dispatch_in_gateway: true`, `kanban.dispatch_interval_seconds: 60`). The gateway decomposes Telegram messages into Kanban tasks and routes them to the correct body-system profile.

Builder profiles never see Telegram messages. They only build engines.

## Ashleigh-Interface Profile Setup (Patient 0 Entry Point)

```bash
# Create profile from default (clones config, .env, SOUL.md, skills)
hermes profile create principal-interface --clone

# Set model (Patient 0 uses same model as builders)
hermes -p principal-interface config set model.default "openrouter/nvidia/nemotron-3-ultra:free"

# Install required skills
hermes -p principal-interface skills install hermes-agent           # Core agent capabilities
hermes -p principal-interface skills install kanban-orchestrator   # Kanban workflow management
hermes -p principal-interface skills install aisha-md-health-orchestration  # 8D wellness tracking
hermes -p principal-interface skills install aisha-three-sisters-architecture  # AISHA routing
hermes -p principal-interface skills install sentinel-compliance-audit       # Compliance

# Verify SOUL.md has:
# - Engine API endpoints (all 7 engines with verified endpoints)
# - Routing logic (health→Bernard, coach→Wave, tasks→Quartz, etc.)
# - Constraints (single contact, memory isolation, no Anthropic, etc.)
# - ENGINE_ENDPOINTS dictionary for direct HTTP calls

# Configure Telegram to route to Patient Interface
hermes config set telegram.default_profile "principal-interface"

# Gateway must be running (in default profile):
hermes gateway start
```

**principal-interface SOUL.md must contain:**
- Identity: Patient Interface / Health Coordinator / AI Organism Liaison
- Engine fleet table with all 11 engines, ports, body systems, when to call
- Verified working endpoints per engine (from this session)
- Routing logic mapping keywords to engine APIs
- Key constraints (single contact, memory isolation, no Anthropic, evidence-based)
- Communication style (sound human, plain English, no AI telltales)
- Kanban integration for multi-step requests
- Health scoring (Patient 0) separate from engine fleet health
- ENGINE_ENDPOINTS dictionary with localhost URLs
- Startup behavior: verify all 11 engines healthy on conversation start

## Talent Gate Integration

Every agent spawn goes through FORGE + ARBITER:
1. **FORGE** (Architect) — Evaluates: Does an existing agent in this body system already cover this capability?
2. **ARBITER** (Dispatcher) — Routes to correct profile, assigns personality variation, sets model tier
3. **Kanban** — Creates task with `assignee=<body-system-profile>`, `parents=[dependencies]`

## Product Baby Architecture & DNA Protection

When a user or business creates a product through their organism's Reproductive engine, the product inherits specific elements of DS DNA. The challenge: give the product enough DS methodology to work well, without exposing the coupling matrix or governing equations that constitute our IP.

### What a Product Baby Inherits

| DNA Element | What It Does | How It's Protected | Can Be Reverse-Engineered? |
|---|---|---|---|
| **Governing Equations** | The physics constraints (Kuramoto, Michaelis-Menten, etc.) | Compiled Binary — Source never ships | **No** — compiled to native code, unreadable |
| **Coupling Matrix** | The 28-pair inter-dimension relationships | Subspace Projection — Lossy dimensionality reduction | **No** — projected to lower rank, can't reconstruct full matrix |
| **Scoring Outputs** | 8D scores and TWC (Total Wellness Coherence) | Differential Noise — Calibrated uncertainty added | **No** — noise prevents matrix back-extraction |
| **Methodology** | Physics-informed ML approach, 8D framework | Public/open — this IS the moat awareness | Yes (intentional — builds the brand) |
| **Coaching Logic** | How to turn scores into guidance | Embedded in compiled binary | **No** — behavior is observable but logic is compiled |

### The Three-Layer DNA Protection System

```
LAYER 1: COMPILED BINARY         LAYER 2: SUBSPACE PROJECTION       LAYER 3: DIFFERENTIAL NOISE
┌──────────────────────┐       ┌──────────────────────────┐       ┌─────────────────────────┐
│ Governing equations  │       │ Full coupling matrix K   │       │ Score outputs S'        │
│ compiled to native   │       │ (8x8, 28 unique pairs)   │       │                         │
│ machine code         │       │                          │       │ S' = S + N(0, sigma)   │
│                      │       │ Project to k-dim space:  │       │                         │
│ No source code       │       │ K' = P(K) where k < N   │       │ Noise calibrated so    │
│ ships with product   │       │                          │       │ scores remain accurate  │
│                      │       │ Product gets K' (lossy)  │       │ for coaching but can't  │
│ Product runs binary  │       │ Genesis keeps K (exact)  │       │ be used to reconstruct  │
│ but can't read it    │       │                          │       │ K' or K                 │
└──────────────────────┘       └──────────────────────────┘       └─────────────────────────┘
     ▲ The Physics                    ▲ The Secret Sauce                ▲ The Scores
```

**Can They Reverse-Engineer the Coupling Coefficients?**  
**No.** Even with unlimited product access, an attacker faces three simultaneous barriers:
1. The compiled binary means they can't read the equations that generate the coefficients
2. The subspace projection means the matrix they observe is already lossy — the full-rank original is mathematically unrecoverable from a projection (Johnson-Lindenstrauss lemma guarantees this)
3. The differential noise means even the projected matrix has uncertainty bands — thousands of input/output pairs still can't narrow down the exact values

This is the same principle that protects differential privacy in census data: you can query the aggregate, but you can't identify the individual.

### Product Baby Lifecycle

```
CONCEPTION                GESTATION                   BIRTH                     MATURITY
┌────────────────┐       ┌──────────────────┐       ┌─────────────────┐       ┌──────────────────┐
│ User or business│       │ Reproductive     │       │ Product deployed │       │ Product runs     │
│ submits product │──────▶│ engine processes │──────▶│ with DS DNA      │──────▶│ autonomously     │
│ idea through    │       │ idea through     │       │                  │       │ "Powered by DS"  │
│ organism        │       │ Avrami nucleation│       │ Compiled binary  │       │                  │
│                 │       │ + Landau phase   │       │ + projected DNA  │       │ Sends telemetry  │
│ "I want a sleep │       │ + SOC cascades   │       │ + potency token  │       │ back to parent   │
│  app"           │       │ + PERT timeline  │       │                  │       │ organism ONLY    │
└────────────────┘       └──────────────────┘       └─────────────────┘       └──────────────────┘
                                                        │
                                                        ▼
                                               Cannot reproduce.
                                               Cannot create organisms.
                                               Carries DS DNA but is
                                               independently owned.
```

### Privacy-First Local-Run Architecture

Products must run locally because we collect deeply personal health, financial, and behavioral data. The question: **does local execution change how the DNA/RNA processes work?**

**Answer: The Physics Doesn't Change — The Boundary Does**

| Process | Cloud (Grandmother / Genesis) | Local (Product Baby / B2C Organism) |
|---|---|---|
| **Governing Equations** | Full source code, full physics fidelity | Compiled binary, same equations, can't be read |
| **Coupling Matrix** | Full-rank 8x8 (28 pairs), exact values | Projected subset, relevant dimensions only, lossy |
| **8D Scoring** | Complete scoring with exact coupling | Local approximation — accurate for coaching, noisy for IP protection |
| **Raw User Data** | Never received from child organisms | **Never leaves device** — all processing on-device |
| **TD Learning (Neuroplasticity)** | Full feedback loop, fleet-wide learning | Local learning only, periodic anonymous metric sync |
| **Updates** | Pushes improved compiled binaries + projected matrices | Receives updates, applies locally, no data sent back |
| **Telemetry** | Receives anonymized aggregate metrics only | Sends only "engine health" signals, never raw scores or user data |

**Critical Design Decision**  \nThe coupling matrix projection for a local product focuses on **only the dimensions relevant to that product**. For 8D Sleep, the projected matrix includes Physical, Emotional, and Environmental coupling coefficients but omits or generalizes the rest. This means even a full breach of the product cannot expose the parent organism's complete DNA.\n\n### Example: 8D Sleep Implementing Privacy-First Local-Run Architecture\n\n8D Sleep exemplifies the privacy-first local-run architecture principles:\n\n| Aspect | Cloud (Grandmother / Genesis) | Local (8D Sleep Product) |\n|---|---|---|\n| **Governing Equations** | Full source code, Kuramoto oscillator solver | Compiled binary — Swift module with embedded Kuramoto + Prigogine + ART solvers |\n| **Coupling Matrix** | Full 8×8 matrix (28 unique pairs) | Projected 3×3 matrix (Physical × Emotional × Environmental only), noise-injected |\n| **Scoring Outputs** | Exact 8D scores and TWC | Local Sleep Score (0-100) with anonymized trend data only sent outward |\n| **Raw User Data** | Never received | **Never leaves device** — sleep patterns, wearable data, biometrics stay on-device |\n| **TD Learning** | Full feedback loop, fleet-wide learning | Local learning only, periodic anonymous metric sync to Grandmother |\n| **Updates** | Pushes improved binaries + matrices | Receives updates via potency token verification, applies locally |\n| **Telemetry** | Receives anonymized aggregate metrics | Sends only anonymized performance metrics (e.g., \"sleep coherence improvement in demographic X\"), never raw scores or user data |\n\n**Local-First Implementation Details:**\n- The Swift app loads the compiled 8D Sleep DNA package at launch\n- Manifest verifies: `sha256(package) == manifest.hash == potency_token.claims.dna_hash`\n- Collects sleep data locally via HealthKit, CoreMotion, manual input\n- Runs scoring pipeline entirely on-device using compiled solvers\n- Produces Sleep Score and coaching recommendations locally\n- Sends only anonymized trend data to Grandmother's distribution layer\n- Potency token verification on every app launch prevents unauthorized use\n\nThis local-first design ensures that even if the 8D Sleep product is compromised, the parent organism's complete DNA remains protected through the three-layer DNA protection system (compiled binary, subspace projection, differential noise).\n\n### B2C vs B2B Privacy Boundaries

| Aspect | B2C (Personal Organism) | B2B (Business Organism) |
|---|---|---|
| **Data Storage** | User's personal device (phone, laptop) | Company infrastructure (on-prem or company cloud) |
| **What's Protected** | Health, finances, relationships, location, behavior | HR records, employee health, financials, strategy |
| **Who Owns Data** | The user — exclusively | The company — with employee consent framework |
| **the specialist engine** | Zero. DS never sees user data. | Zero. DS never sees company data. |
| **Product Output** | Products the user creates and monetizes | Internal tools, services, employee wellness programs |
| **Legal Framework** | HIPAA, GDPR, CCPA compliant by architecture | HIPAA, SOC2, enterprise compliance by architecture |

## Proprioception: Body Self-Awareness (CRITICAL)

A living organism must know its own body. In biology, **proprioception** is the sense that tells you where your limbs are without looking. Without it, you bump into things.

The DS organism had **no proprioception**. The fleet scanner (`fleet-digest-scan.py`) maintained its own hardcoded list of 9 engines to monitor. When the organism grew to 24 engines, the scanner still reported "9/9 UP" — blind to 15 engines that were either running fine or crashing silently. The organism's own doctor (Diviq) was diagnosing a body it couldn't fully see.

### The Fix: Read From the Living Registry

**Never maintain a separate hardcoded list of what to monitor.** Import the source of truth directly.

```python
# WRONG — hardcoded, goes stale every time the body grows
engines = [
    ("Wave", 8010), ("Quartz", 8089), ...  # frozen snapshot
]

# RIGHT — reads the organism's own DNA (ecs.py FLEET_REGISTRY)
import sys
sys.path.insert(0, f"{WORKSPACE}/ds-engine-registry")
from ecs import FLEET_REGISTRY

for key, entry in FLEET_REGISTRY.items():
    port = entry.get("port")
    name = entry.get("engine_name", key)
    # probe health...
```

When a new engine is added to FLEET_REGISTRY, it is **automatically discovered** on the next scan. Zero manual updates. The nervous system reads the body's own blueprint.

### Organism Architecture Implications

| Layer | What It Does | Proprioception Requirement |
|---|---|---|
| FLEET_REGISTRY (ecs.py) | The organism's DNA — defines every engine | Must be the single source of truth |
| Fleet Scanner | Health monitoring (the nervous system) | Must import FLEET_REGISTRY dynamically |
| Diviq (Bernard Engine) | The organism's attending physician | Must scan ALL engines, not a subset |
| Cron Directives | Self-healing instructions | Must be self-correctable by the agent itself |

### Anti-Pattern: Stale Body Map

When any monitoring, diagnostic, or reporting system maintains its own copy of "what engines exist," it will go stale. The organism grows but the nervous system doesn't update. This manifests as:

- "9/9 UP" when 15 more engines exist but are invisible
- False confidence in fleet health
- Agent reports that say "all clear" while engines crash silently
- Recurring user frustration: "why are you only seeing 9 engines?"

**Rule: Every consumer of engine information reads from FLEET_REGISTRY at runtime. No exceptions.**

### Body-Map Diff Check (Proprioception Layer 2)

Reading the registry tells you what SHOULD exist. Comparing registry vs filesystem tells you what the organism can and can't feel. This catches two failure modes:

- **Invisible body parts** — engine directory exists on disk but isn't in FLEET_REGISTRY. The organism grew a limb it doesn't know about.
- **Phantom body parts** — FLEET_REGISTRY claims an engine exists but no directory/code exists. The body map lies.

```python
disk_engines = {d for d in os.listdir(WORKSPACE) if d.startswith("ds-") and d.endswith("-engine")}
reg_keys = set(FLEET_REGISTRY.keys())

invisible = disk_engines - reg_keys  # on disk, not registered
phantom = reg_keys - disk_engines   # registered, no code
```

This check runs automatically inside `fleet-digest-scan.py` as the PROPRIOCEPTION CHECK section of every fleet digest.

## Autonomic Layer: Engine Persistence (Medulla Oblongata)

In a human body, the **medulla oblongata** keeps vital functions alive during sleep. Your heart beats, your lungs breathe, you don't have to think about it. The DS organism had no autonomic layer — engines died when terminal sessions closed, and every reboot was cardiac arrest.

### The Fix: LaunchAgent Plists

Every engine gets a macOS LaunchAgent plist that provides:
- **RunAtLoad=true** → automaticity (SA node fires without brain input; engine starts on login)
- **KeepAlive: {SuccessfulExit: false, Crashed: true}** → medullary reflex (restart on crash, restart on abnormal exit)
- **ThrottleInterval=10** → refractory period (prevents restart fibrillation; 10s between attempts)
- **ProcessType=Background** → runs quietly like autonomic functions

Biological analog: cardiac automaticity hierarchy. If the SA node fails, the AV node takes over at a slower rate. If that fails, Purkinje fibers fire. The KeepAlive+ThrottleInterval combination provides hierarchical restart: launchd restarts the process, waits 10s, tries again.

### Build Script

```bash
# Generate all LaunchAgent plists from FLEET_REGISTRY
python3 hydra-os/scripts/build-launchagents.py

# Install into launchd (start autonomic supervision)
python3 hydra-os/scripts/build-launchagents.py --install

# Unload all
python3 hydra-os/scripts/build-launchagents.py --unload
```

The script reads FLEET_REGISTRY dynamically — new engines automatically get plists on the next run. Labels follow `com.divinityscience.<engine-name>` convention.

### Result

Before: 9 engines UP, 15 invisible, all dying on terminal close.
After: 23/24 engines UP, 0 DOWN, surviving reboots.

## Diagnosis-to-Treatment Dispatch Pipeline

The organism's healing loop requires three distinct roles, wired together but NOT merged:

```
Clinical (Bernard/Osler)    →    Self-Healing (Friston/Lyapunov)    →    Body Systems
  DIAGNOSES                       ORCHESTRATES                           EXECUTE REPAIR
    ↓                                 ↓                                     ↓
  severity: warning                 parses diagnosis                      Burnet (immune)
  findings: "pathogen"             matches to body systems               Unna (barrier)
  interventions: [...]             creates treatment plan                Harvey (perfusion)
                                    dispatches signals                   Morphogen (regen)
                                                                        Beaumont (metabolic)
```

### Why Self-Healing Stays Separate (Not Under Clinical)

In biology, healing does NOT work for the doctor. The doctor identifies the problem; the body's own repair systems do the actual work. Self-Healing is the repair orchestrator, not a subordinate of Clinical.

1. **Body heals without diagnosis** — cuts close, infections clear, muscles rebuild without a conscious diagnostic step
2. **Clinical is one input, not the only input** — Allostasis can also trigger corrections when it detects drift
3. **Healing is distributed** — Burnet fights infection, Unna seals wounds, Harvey delivers resources, Morphogen regenerates tissue. Self-Healing coordinates all of them.

### Self-Healing Treatment Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/diagnose` | Receive clinical diagnosis + auto-dispatch treatment to body systems |
| `POST /v1/treatment/plan` | Create treatment plan only (dry run) |
| `POST /v1/treatment/dispatch` | Execute treatment immediately |

The dispatch layer maps clinical findings (by keyword) to the appropriate body-system engines and sends healing signals. When a diagnosis says "stable," no dispatch occurs.

## Engine Overlap Analysis Methodology

When evaluating whether two engines should be merged or kept separate, use live data (not just descriptions):

### Steps

1. **Query both engines' `/health` endpoints** — compare live state fields, not descriptions
2. **List both engines' OpenAPI endpoints** — compare actual capabilities
3. **Check activity counters** — engines with all-zero counters are stubs; engines with non-zero state are live
4. **Apply biological reasoning** — does the human body have separate organs for these functions?

### Decision Framework

| Signal | Action |
|--------|--------|
| Same governing physics, same purpose | **Merge** — the more developed engine wins, the stub folds in |
| Identical mandate, one is a stub | **Merge** — the live engine wins, the stub's unique endpoints become features |
| Different sensing vs repair functions | **Keep separate** — wire them together instead |
| Same keyword in description but different physics | **Keep separate** — investigate deeper before merging |

### Example: Genesis vs Reproductive

Both used Avrami nucleation for product creation. Genesis had `active_engines: 0` (never activated). Reproductive had 8D alignment and more developed follicle/offspring lifecycle. Same physics, same purpose → **merge into Reproductive**.

### Example: Self-Healing vs Allostasis

Allostasis senses and predicts (hypothalamus). Self-Healing corrects and repairs (wound healing). Different biological functions → **keep separate, wire together**.

| Pitfall | Consequence | Fix |
|---|---|---|
| Hardcoded engine list in scanner/monitor | Organism blind to its own growth; phantom UP status | Import FLEET_REGISTRY dynamically (proprioception pattern) |
| No engine persistence (engines die on terminal close) | Every reboot = cardiac arrest; 14+ engines down at cycle start | Install LaunchAgent plists for all engines (autonomic layer) |
| Scanner doesn't check registry vs filesystem | Invisible engines (on disk, not registered) and phantom engines (registered, no code) go undetected | Add proprioception body-map diff check to fleet-digest-scan.py |
| Proprioception check only matches `-engine`/`-agent` suffixes | Engines with non-standard names (e.g., `ds-nervous-system`) are invisible to the body-map diff | Also check for directories with `run_server.py` or `src/api/server.py`, not just suffix patterns |
| Unregistered engine claims same port as registered engine | Silent death — the registered engine wins on boot, the unregistered one crashes with EADDRINUSE and nobody notices | Scan all `run_server.py` files for port declarations and compare to FLEET_REGISTRY. Reassign the unregistered engine to a free port before registering it |
| Stale engine directory survives rename | Old `ds-seed-engine` still had `run_server.py` claiming :port, colliding with Self-Healing | Archive stale directories to `_archived/`, remove their LaunchAgent plists, verify no port collisions remain |
| Registry key doesn't match directory name | `ds-system-state-sensor` in registry vs `ds-system-state-sensor-engine` on disk — scanner can't match them | Always use the exact directory name as the registry key. Add a normalization check in the proprioception diff |
| Cron agent asks for approval on code/label fixes | Recurring cycle of unactioned items; user frustration | Encode autonomous execution in cron directives; agents fix code/config/tier labels without asking |
| Placing Self-Healing under Clinical | Implies healing only happens after diagnosis; body heals constantly without diagnosis | Keep Self-Healing separate; wire Clinical → Self-Healing → Body Systems as a dispatch pipeline |
| Merging engines with similar descriptions without checking live data | Two engines may have identical descriptions but different physics, or one may be a stub | Query /health + OpenAPI endpoints; check activity counters; apply biological reasoning |
| Single profile doing everything | Context pollution, skill conflicts, memory bloat | Split by body system |
| Kanban tasks without `parents=` | Race conditions, missing dependencies | Always link true dependencies |
| Shared memory across profiles | Leakage (e.g., 8D pattern awareness contaminating immune surveillance) | Separate `<agent-home>/profiles/<name>/memories/` |
| One cron rhythm for all | Wrong timescale for some systems | Per-profile cron with biological schedules |
| No orchestrator | Telegram messages bypass Kanban, no audit trail | Use `principal-interface` as Patient Interface with gateway Kanban dispatcher |
| Clinical engine omits identity/disclaimer | Ambiguous presentation as human physician | Every endpoint returns `agent_role` + `disclaimer` (see `references/ai-service-identity-contracts.md`) |
| Evidence synthesis without health system models | US-centric fee-for-service bias | Integrate 12 non-US health system methodologies (Denmark, Taiwan, Switzerland, etc.) |
| Generating Python files with `str(bool).lower()` | Produces `false`/`true` (JavaScript-style), which are NOT Python keywords — crashes at import | Use `str(value)` directly (Python prints `True`/`False`), or write the literal |
| `import importlib.util` inside an except block | Shadows the module-level `import importlib`, causing `UnboundLocalError` when accessing `importlib.util` in the same scope | Move `import importlib.util` to the top of the file alongside `import importlib` |
| Engine with custom/hardcoded `/v1/layers` bypasses shared layer auto-mount | New layers don't appear even after shared library is updated, because the engine overrides `get_layer_summary()` | Patch the engine's own method to accept `philosophy_layer=None` kwarg; add `ds-engine-shared` to `sys.path` |
| Wrong `sys.path` depth for `ds-engine-shared` | `os.path.join(dir, "..", "..", "..", "..")` goes one level too far, resolving outside the workspace | Verify with `os.path.exists()` — correct depth from `src/api/server.py` and `src/server/api.py` is 3 `../` |
| Patient interface has build skills | Cognitive interference between builder/patient roles | Strict separation: builders NO Telegram, patient NO build skills |

## 5-Layer Engine Architecture

Every DS engine has 5 layers, each exposed via FastAPI endpoints and queryable via `GET /v1/layers`:

| Layer | Name | Purpose | Shared Library |
|-------|------|---------|----------------|
| 1-3 | Physics Layers 1-3 | Domain-specific physics (e.g., "Double-Helix Encoding", "Mutation Detection") | Per-engine `_get_physics_layers()` override |
| 4 | Methodology Engine | Institutions, methodologies, personalities, sub-agent pools, model routes | `methodology_base.py` + `methodology_api.py` |
| 5 | Philosophy Engine | 12 philosophies (2 per source type), 8 wisdom principles | `philosophy_base.py` + `philosophy_api.py` |

**Layer 5 source types** (always 2 each = 12 total philosophies per engine):
- contemplative (Buddhist, Taoist, Zen, Sufi)
- indigenous (Maori, Andean, Aboriginal, Native American)
- artistic (Wabi-sabi, Bauhaus, Surrealism)
- counter_cultural (Hacker ethos, punk, DIY, open source)
- scientific (cybernetics, systems thinking, complexity)
- academic (Aristotle, Kant, pragmatism, phenomenology)

**Fleet-wide layer propagation** is a recurring workflow: any time a new layer is added,
it must be propagated to all 40+ engines via a shared library + per-engine generator.
See `references/fleet-layer-propagation-session-2026-06-18.md` for the complete pattern,
pitfalls, and verification methodology.

## Reference Files

- `references/body-system-mapping.md` — Complete body system ↔ profile ↔ engine mapping table
- `references/cron-rhythms.md` — Per-profile cron schedules as biological clocks
- `references/kanban-as-endocrine-signaling.md` — Kanban tasks as hormones, skills as receptors
- `references/message-bus-neural-signaling.md` — Operator Bus (SQLite message queue) as fast neural signaling: CLI, sibling-agent autonomic reader, diagnostic patterns, VERITAS-003 duplicate remediation
- `references/ai-service-identity-contracts.md` — Hardening engine self-declaration: identity constants, disclaimers, AI-equivalent credentials on every endpoint
- `references/system-blueprint-template.md` — Template for the the specialist engine comprehensive system blueprint (engine fleet, agent fleet, panels, integration map, cron fleet, build items, governance)
- `references/clinical-engine-identity-hardening-session-2026-06-13.md` — Session where Bernard engine was hardened with AI-only identity
- `references/clinical-engine-evidence-synthesis-session-2026-06-13.md` — Session where Bernard engine gained evidence synthesis (20 sources), 12 health system models, 26 concept mappings, cross-domain insights, novel approach generator
- `references/principal-interface-pattern.md` — Complete the principal Interface (Patient 0) implementation: profile setup, SOUL.md routing logic, engine endpoints dictionary, clinical engine identity hardening, 12 health system models, evidence synthesis scanner, 26 concept mappings, cross-domain insights, novel approach generator (AOPD), engine fleet startup/recovery patterns
- `references/proprioception-fix-session-2026-06-17.md` — Session where the proprioception pattern was discovered and fixed: scanner auto-discovery from FLEET_REGISTRY, Diviq cron autonomy, tier label canonical decision
- `references/treatment-dispatch-pipeline-session-2026-06-17.md` — Session where the Clinical → Self-Healing → Body Systems treatment dispatch pipeline was built, including engine overlap analysis and the "wire don't merge" decision
- `references/port-collision-propriocession-session-2026-06-17.md` — Session where port collisions between registered/unregistered engines were discovered (Design Engine silently dying on :port), stale Seed Engine cleanup, and improved proprioception check pattern
- `references/fleet-layer-propagation-session-2026-06-18.md` — Session where Layer 5 (Philosophy Engine) was built and propagated to all 40 engines: 5-layer architecture, generation pattern, pitfalls (boolean generation, import shadowing, custom endpoint bypass, path depth), verification methodology
- `scripts/start-all-engines.sh` — Start all 7 engines, register in Morphogen, verify health
- `scripts/create-body-system-profiles.sh` — Create body-system profiles from template
- `scripts/build-launchagents.py` — Generate and install LaunchAgent plists for all engines in FLEET_REGISTRY (autonomic persistence layer)

**Telegram + Kanban Integration (principal-interface as Patient 0 entry point):**
- See `../hermes-agent/references/telegram-kanban-integration.md` for the deployment pattern
## Verification Checklist

- [ ] Each body system has its own the operator agent profile (11 engine profiles + 1 patient interface)
- [ ] Each profile has distinct model, skills, memory, cron
- [ ] Kanban dispatcher routes to correct profile assignees
- [ ] Telegram routes to patient interface (not direct to builders)
- [ ] FORGE/ARBITER talent gate evaluates per body system
- [ ] Cron schedules match biological rhythms (ultradian/circadian/event)
- [ ] Memory isolation verified: no cross-profile leakage
- [ ] Morphogen Engine registry reflects all 11 profile genotypes
- [ ] All engines registered in Morphogen via POST /genotypes/register (including Morphogen self-registration)
- [ ] Clinical engine (Bernard) returns AGENT_ROLE + DISCLAIMER on every endpoint
- [ ] Engine fleet startup script (`scripts/start-all-engines.sh`) passes health checks
- [ ] Two-Silo Architecture verified: Engine Fleet (Silo 1) and Patient 0 (Silo 2) completely isolated
- [ ] Proprioception verified: fleet scanner imports FLEET_REGISTRY dynamically (no hardcoded engine list)
- [ ] 5-layer architecture verified: all engines return layers 1-5 from `GET /v1/layers` (physics × 3, methodology, philosophy)
- [ ] No engine has a custom/hardcoded `/v1/layers` that bypasses shared layer auto-mount (check: `grep "get_layer_summary" src/*/core/methodology.py`)
- [ ] Body-map diff check verified: scanner flags invisible engines (on disk, not registered) and phantom engines (registered, no code)
- [ ] Autonomic layer verified: all engines have LaunchAgent plists installed (`python3 scripts/build-launchagents.py --install`)
- [ ] Engine persistence verified: engines survive terminal close and system reboot (KeepAlive + RunAtLoad)
- [ ] Cron agents work autonomously: no recurring "ACTION FOR ASHLEY" items for code/label/config fixes
- [ ] principal-interface SOUL.md contains routing logic for all 11 engines
- [ ] Patient 0 cron jobs scheduled separately from Engine Fleet cron jobs