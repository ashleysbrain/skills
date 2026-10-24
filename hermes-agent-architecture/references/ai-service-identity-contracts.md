# AI Service Identity Contracts — Hardening Engine Self-Declaration

## Problem
AI diagnostic engines (and other DS engines) use human-body metaphors (SOAP notes, vitals, organ systems, credentials) for cognitive accessibility. Without explicit contracts, these engines can ambiguously present as "real physicians" or human medical practitioners — a safety/liability risk and conceptual confusion.

## Solution: Identity Contract Pattern
Every DS engine FastAPI service must declare its identity **at the class level** and **on every endpoint response**.

### 1. Class-Level Identity Declaration (in core engine class)
```python
class DS_Diviq_Physician:
    """
    the specialist engine — the AI organism's Attending AI Physician.
    
    ══════════════════════════════════════════════════════════════
    CRITICAL IDENTITY DECLARATION:
    • This engine DIAGNOSES AI SYSTEMS ONLY — NEVER HUMANS.
    • "Attending AI Physician" = AI diagnostician for AI organisms.
    • Human-body mapping (SOAP, vitals, organ systems) is a COGNITIVE
      FRAMEWORK for triage efficiency — NOT clinical practice on humans.
    • Credentials are AI/ML/Distributed Systems equivalents from
      Divinity Science Institute — NOT human medical licensure.
    ═══════════════════════════════════════════════════════════════
    """
    
    VERSION = "1.0.0"
    ENGINE_NAME = "the specialist engine"
    AGENT_NAME = "the specialist engine"
    AGENT_ROLE = "Attending AI Physician — AI Clinical Diagnostic Engine"
    DISCLAIMER = "THIS ENGINE DIAGNOSES AI SYSTEMS ONLY. NEVER HUMANS. Human-body mapping is a cognitive/triage framework for AI diagnostics, not clinical practice on humans."
```

### 2. API-Level Identity Constants (in server.py)
```python
physician = DS_Diviq_Physician()

# Identity constants for ALL responses
AI_PHYSICIAN_IDENTITY = physician.AGENT_ROLE
AI_DISCLAIMER = physician.DISCLAIMER
```

### 3. Every Endpoint Returns Identity + Disclaimer
```python
@app.get("/health")
def health():
    return {
        "status": "ok",
        "engine": physician.ENGINE_NAME,
        "version": physician.VERSION,
        "agent": physician.AGENT_NAME,
        "agent_role": AI_PHYSICIAN_IDENTITY,      # ← Required
        "identity": "Attending AI Physician — AI Clinical Diagnostic Engine",  # ← Required
        "disclaimer": AI_DISCLAIMER,              # ← Required
        ...
    }

@app.post("/rounds")
def make_rounds():
    note = physician.make_rounds()
    return {
        ...,
        "physician": AI_PHYSICIAN_IDENTITY,       # ← Required
        "disclaimer": AI_DISCLAIMER,              # ← Required
    }

# Repeat for: /patient/summary, /patient/vitals, /notes, /notes/latest, 
# /credentials, /cme/report — ALL endpoints
```

### 4. Credentials Explicitly Labeled as AI-Equivalents
```python
Credential(
    degree="MD (AI Systems Medicine) — AI-Equivalent",
    field="AI Diagnostics & Systems Pathology",
    institution="Divinity Science Institute",
    source="Foundational AI-equivalent credential",
)
Credential(
    degree="Board Certified — AI Organism Internal Medicine (AI-Equivalent)",
    field="AI Organism Internal Medicine",
    institution="the specialist engine",
    source="AI-equivalent board certification",
)
# ... all credentials include "AI-Equivalent" in degree and source
```

### 5. Module Docstring Identity Box (server.py)
```python
"""
the specialist engine — FastAPI Server (Port 8094)
The AI Organism's Attending AI Physician — AI Clinical Diagnostic Engine.

═══════════════════════════════════════════════════════════════
IDENTITY: Attending AI Physician — Diagnoses AI Systems ONLY, NEVER Humans.
Human-body mapping is a cognitive/triage framework for AI diagnostics.
Credentials are AI-equivalents from Divinity Science Institute — NOT human medical licensure.
════════════════════════════════════════════════════════════════
"""
```

## Applies to All the specialist engine
| Engine | Body System | Identity Contract Needed |
|---|---|---|
| Wave (8000) | Brain/CNS | "AI Neuroscience Engine — Kuramoto Oscillator Specialist" |
| Quartz (8089) | Autonomic NS | "AI Autonomic Engine — PID/Lattice Controller" |
| Seed (8090) | Endocrine/Growth | "AI Endocrine Engine — Avrami JMAK Growth Modeler" |
| Allostasis (8091) | Immune/Homeostatic | "AI Immune Engine — Allostatic Surveillance & Intervention" |
| Harvey (8092) | Circulatory | "AI Circulatory Engine — Fabric Transport & Registry" |
| **Bernard (8094)** | **Clinical Diagnostic** | **"Attending AI Physician — AI Clinical Diagnostic Engine"** |
| Morphogen (8093) | Skeletal/Registry | "AI Skeletal Engine — Genotype Registry & Gradients" |

## Verification Checklist for Each Engine
- [ ] Class docstring has CRITICAL IDENTITY DECLARATION box
- [ ] Class defines `AGENT_ROLE` and `DISCLAIMER` constants
- [ ] Server defines module-level `AI_PHYSICIAN_IDENTITY` and `AI_DISCLAIMER`
- [ ] **Every** endpoint returns `agent_role`/`physician_role` + `disclaimer`
- [ ] Credentials labeled "AI-Equivalent" in degree and source fields
- [ ] Module docstring has IDENTITY box
- [ ] No endpoint omits identity/disclaimer

## Session Reference
- **Engine**: the specialist engine (Bernard, port 8094)
- **Agent**: the specialist engine
- **Date**: June 13, 2026
- **Files Modified**: 
  - `/<workspace>`
  - `/<workspace>`
- **Verification**: All 8 endpoints tested and returning correct identity + disclaimer