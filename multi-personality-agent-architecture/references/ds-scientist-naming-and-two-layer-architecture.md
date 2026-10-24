# DS + Scientist Naming Convention & Two-Layer Board/Agent Architecture

## Overview

This document captures the established patterns for Divinity Science agent naming and the two-layer advisory architecture, derived from the June 2026 research board and execution panel build session.

---

## DS + Scientist Naming Convention

**Rule:** Agent name = `DS` + **Scientist whose discovery embodies the agent's function**

The scientist is not just an inspiration — their specific discovery/breakthrough IS the function the agent performs.

### Established Agents (June 2026)

| Agent | Scientist | Discovery → Function |
|-------|-----------|---------------------|
| **the specialist engine** | J. Robert Oppenheimer | Manhattan Project coordination → **Research orchestration** |
| **the specialist engine** | Eugene Garfield | Science Citation Index, scientometrics → **Literature review & evidence mapping** |
| **the specialist engine** | Herbert Simon | Bounded rationality, consilience (econ+CS+psych) → **Cross-dimensional synthesis / Third Mind** |
| **the specialist engine** | Isaac Asimov | 500+ books, master of clarity across sciences → **Technical writing & science communication** |
| **the specialist engine** | Judea Pearl | Causal inference (do-calculus), Bayesian networks → **Quantitative analysis & causal inference** |
| **the specialist engine** | Claude Shannon | Information theory, signal extraction from noise → **Competitive intelligence & horizon scanning** |
| **the specialist engine** | Karl Popper | Falsifiability, critical rationalism → **Methodology quality & research integrity (VETO POWER)** |
| **the specialist engine** | Vannevar Bush | Created NSF, "Science: The Endless Frontier" → **Grant writing & funding strategy** |
| **the specialist engine** | *Agent name for Bernard Engine* | Clinical physician role |
| **the specialist engine** | William Harvey | Blood circulation (1628) → **Circulatory fabric / message bus** |
| **the specialist engine** | Francis Paxton | Bone Morphogenetic Proteins → **Skeletal / Morphogen registry** |
| **the specialist engine** | Peter Sterling | Allostasis (stability through change, 1988) → **Immune / Allostasis engine** |
| **the specialist engine** | Conrad Waddington | Epigenetic landscape → **Endocrine / Seed engine** |
| **the specialist engine (Quartz)** | *Agent name for Crystal Engine* | PID/Lyapunov stability → **Autonomic NS / Crystal engine** |
| **the specialist engine** | Yoshiki Kuramoto | Coupled oscillators → **Brain / Wave engine** |

### Anti-Patterns (What NOT to Do)

❌ **Generic descriptive names:** `DS ResearchLead`, `DS LiteratureReviewer`, `the specialist engine`
❌ **Scientist as decoration:** Using a famous name without functional mapping
❌ **Invented names:** `the specialist engine`, `the specialist engine` — unless the scientist's discovery maps to function
❌ **My-generated alternatives:** The user explicitly rejected my generated names in favor of the exact names from their screenshots

### Verification Checklist for New Agents

- [ ] Scientist's specific discovery directly maps to agent function
- [ ] Name follows `DS` + `ScientistLastName` format
- [ ] User has approved the name (if from their specification)
- [ ] Function documented in agent's facts with "Discovery → Function" line

---

## Two-Layer Architecture: Boards Advise → Agents Execute

### Layer 1: Executive Boards (Advise Only)

**Human mirrors with defined methodologies** — they produce recommendations, never execute.

| Board | Human Advisors | Primary Agent | Agent Code |
|-------|---------------|---------------|------------|
| principal | Satya Nadella, Tim Cook, Teresa Torres, Saeju Jeong, Reed Hastings, Indra Nooyi, Jamie Dimon | SINGULARITY | EXE-CHF-ALL-L7-C5-P3-T5-001 |
| COO | Tim Cook, Gwynne Shotwell, Ruth Porat, Sheryl Sandberg, Angela Ahrendts | NEBULA | EXE-LED-OPS-L7-C5-P3-T5-001 |
| CPO | Marty Cagan, Eric Ries, BJ Fogg, April Dunford, Eric Topol | AURORA | DS-LED-PRD-L6-C4-P2-T5-001 |
| CTO | Andrew Ng, Nicole Forsgren, Will Larson, Eric Topol, Balaji Srinivasan | PULSAR | DS-LED-TEC-L6-C4-P2-T5-001 |
| CRO | Elad Gil, Aaron Ross, Jill Rowley, Mark Roberge, Dan Steinman, Madhavan Ramanujam | SOLAR FLARE | DS-LED-REV-L6-C4-P6-T5-001 |
| CMO | April Dunford, Mark Hyman, Dave Asprey, Steve Krug, Sahil Bloom | SUPERNOVA | DS-LED-MKT-L6-C4-P2-T5-001 |
| CSO | (Elite Conclave) | EVENT HORIZON | DS-LED-STR-L6-C4-P1-T5-001 |
| **Research** | **an external bioinformatics advisor, Stuart Hameroff, Vivek Murthy, Einstein, Feynman, Damasio, Ostrom, Kahneman, Margulis, Wiener** | **DARK MATTER** | **RES-DSP-COR-L5-C3-P3-T4-001** |

### Layer 2: the specialist engine (Execute)

**Elite agents with full credentials** — they take action on board recommendations.

| Engine | Body System | Port | Agent | Agent Code |
|--------|-------------|------|-------|------------|
| Wave | Brain / CNS | 8000 | the specialist engine | (coaching engine) |
| Crystal | Autonomic NS | 8089 | the specialist engine (Quartz) | (task/lattice engine) |
| Seed | Endocrine | 8090 | the specialist engine | (growth engine) |
| Allostasis | Immune | 8091 | the specialist engine | (homeostatic regulation) |
| Harvey | Circulatory | 8092 | the specialist engine | (message fabric) |
| Morphogen | Skeletal | 8093 | the specialist engine | (genotype registry) |
| Bernard | Clinical | 8094 | the specialist engine | (physician) |
| Clinical | Research Execution | — | the specialist engine et al. | (execution panel) |

### Routing Rules (Hard Constraints)

1. **Boards ADVISE only** — they never execute directly
2. **Board output → assigned agent → agent executes**
3. **Cross-board topics route to COO (NEBULA)** who orchestrates
4. **Escalations go to principal (SINGULARITY) → then to the principal**
5. **Agent fleet reports back via principal-DAILY-ACTIONS.md**

### Workflow

```
Board meets → produces recommendation
    ↓
Recommendation written to board's output file
    ↓
Executive Task Manager (Crystal Lattice) ingests all board outputs
    ↓
Lattice prioritizes and assigns to agent fleet
    ↓
Agents execute → report results → lattice rebalances
```

---

## Research Board + Research Execution Panel Pattern

### Research Board (Layer 1 - Advisory)

**Workspace:** `ds-wave-research-board` (Honcho)

**10 Advisors covering all 8D:**

| Advisor | 8D Specialty | Domain |
|---------|-------------|--------|
| Dr. an external bioinformatics advisor | INTELLECTUAL (AI) + VOCATIONAL | AI Research / Precision Medicine |
| Dr. Stuart Hameroff | PHYSICAL (quantum bio) + SPIRITUAL | Consciousness Physics |
| Dr. Vivek Murthy (Surgeon General) | SOCIAL + EMOTIONAL + PHYSICAL | Public Health / Connection |
| Albert Einstein | PHYSICAL + INTELLECTUAL | Theoretical Physics |
| Richard Feynman | PHYSICAL + VOCATIONAL + INTELLECTUAL | Quantum Mechanics / Teaching |
| Antonio Damasio | EMOTIONAL + PHYSICAL + SPIRITUAL | Neuroscience of Emotion |
| Elinor Ostrom | SOCIAL + ENVIRONMENTAL + VOCATIONAL | Commons Governance |
| Daniel Kahneman | INTELLECTUAL + EMOTIONAL + VOCATIONAL | Cognitive Architecture |
| Lynn Margulis | ENVIRONMENTAL + PHYSICAL + SPIRITUAL | Symbiogenesis / Evolution |
| Norbert Wiener | **ALL 8D via CYBERNETICS** | Control/Feedback Systems |

**Each advisor has full 12-section methodology:**
1. Identity, 2. Core Philosophy, 3. Dimension Specialty, 4. Methodology, 5. Input Requirements, 6. Output Format, 7. Coupling Rules, 8. Phase Alignment Criteria, 9. Escalation Triggers, 10. Validation Protocol, 11. Learning Loop, 12. Boundary Conditions

### Research Execution Panel (Layer 2 - Execute)

**Workspace:** `ds-wave-research-execution-final` (Honcho)

**8 Agents (DS + Scientist naming):**

| Agent | Scientist | Function |
|-------|-----------|----------|
| the specialist engine | J. Robert Oppenheimer | Research Execution Lead |
| the specialist engine | Eugene Garfield | Literature Review & Evidence Mapping |
| the specialist engine | Herbert Simon | Cross-Dimensional Synthesis / Third Mind |
| the specialist engine | Isaac Asimov | Technical Writing & Science Communication |
| the specialist engine | Judea Pearl | Quantitative Analysis & Causal Inference |
| the specialist engine | Claude Shannon | Competitive Intelligence & Horizon Scanning |
| the specialist engine | Karl Popper | Methodology Quality / VETO GATE |
| the specialist engine | Vannevar Bush | Grant Writing & Funding Strategy |

### Honcho API Pattern for Board/Panel Creation

```bash
# 1. Create board workspace
POST /v3/workspaces { "id": "ds-wave-research-board" }

# 2. Add advisors as peers
POST /v3/workspaces/{workspace_id}/peers { "id": "gil-alterovitz", "facts": [...] }

# 3. Create board session
POST /v3/workspaces/{workspace_id}/sessions { 
  "id": "research-board-activation-001",
  "participants": ["gil-alterovitz", ...],
  "metadata": { "mode": "advisory" }
}

# 4. Create execution panel workspace
POST /v3/workspaces { "id": "ds-wave-research-execution-final" }

# 5. Add execution agents as peers
POST /v3/workspaces/{workspace_id}/peers { "id": "ds-oppenheimer", "facts": [...] }

# 6. Create execution session
POST /v3/workspaces/{workspace_id}/sessions {
  "id": "research-execution-panel-final-001",
  "participants": ["ds-oppenheimer", ...],
  "metadata": { "mode": "execution", "board": "ds-wave-research-board" }
}

# 7. Send activation message
POST /v3/workspaces/{workspace_id}/sessions/{session_id}/messages {
  "messages": [{ "peer_id": "ds-oppenheimer", "content": "..." }]
}
```

---

## Engine Body-System Metaphors

| Engine | Body System | Port | Scientist | Agent |
|--------|-------------|------|-----------|-------|
| **Wave** | Brain / CNS | 8000 | Yoshiki Kuramoto | the specialist engine |
| **Crystal** | Autonomic NS | 8089 | *PID/Lyapunov* | the specialist engine (Quartz) |
| **Seed** | Endocrine / Growth | 8090 | Conrad Waddington | the specialist engine |
| **Allostasis** | Immune / Homeostatic | 8091 | Peter Sterling | the specialist engine |
| **Harvey** | Circulatory | 8092 | William Harvey | the specialist engine |
| **Morphogen** | Skeletal | 8093 | Francis Paxton | the specialist engine |
| **Bernard** | Clinical / Homeostasis | 8094 | Claude Bernard | the specialist engine |

**Naming Rule:** Engine = Scientist's Discovery; Agent = DS + Scientist

---

## Key Corrections from Session (Do Not Repeat)

1. **User rejected my generated names** — Use EXACT names from user screenshots/specification
2. **User corrected Clinical → Bernard Engine** — Claude Bernard (homeostasis), agent the specialist engine
3. **User corrected Quartz → Crystal Engine** — Task engine, agent the specialist engine (Quartz)
4. **User corrected Research Execution Panel names** — Must match screenshot exactly
5. **Two-layer architecture is mandatory** — Boards advise, agents execute
6. **Step-by-step careful building** — User wanted deliberate process, not rushed
6. **All engines must understand 8D methodology** — Even if human 8D doesn't apply, AI 8D does
7. **Credential auto-update pipeline** — Standing order for all board advisors

---

## Session Artifacts

- `ds-wave-research-board` — 10 advisors, session `research-board-activation-001`
- `ds-wave-research-execution-final` — 8 agents, session `research-execution-panel-final-001`
- `ds-wave-clinical-engine` — Bernard Engine, peer `ds-diviq`
- All running on Honcho (port 8000) with verified health checks