# Treatment Dispatch Pipeline Session — 2026-06-17

## Context

the principal sent a voice note asking whether the Self-Healing engine should be moved under the Clinical engine (Bernard). Her reasoning: "as Bernard diagnoses something, the self-healing engine kicks in to actually heal it."

## Voice Note Transcript

> "Self-Healing is different from Allostasis, but should it move under Clinical? So that as Bernard diagnoses something, the self-healing engine kicks in to actually heal it. Body heals in many ways. Should self-healing go as something under the clinical engine?"

## Analysis Performed

### Engine State Comparison (live data)

| Engine | Key Fields | Status |
|--------|-----------|--------|
| Self-Healing (:port) | `dimensions_tracked: 8, all_converged: False` | Actively correcting |
| Allostasis (:port) | `meta_healthy: True, vitals: {}` | Sensing, not collecting yet |
| Clinical (:port) | 5-seat specialist panel, severity assessment | Actively diagnosing |

### Biological Reasoning

In the human body:
1. **Detection** → Interoception senses something's off
2. **Diagnosis** → Clinical figures out what's wrong
3. **Healing** → Multiple body systems coordinate to fix it:
   - Immune (Burnet) fights infection
   - Skin (Unna) closes wounds
   - Blood (Harvey) delivers resources
   - Morphogen (Turing) regenerates tissue
   - Allostasis adjusts set points

Self-Healing is step 3 — the orchestrator. If placed under Clinical, it implies healing only happens after diagnosis. But the body heals constantly without diagnosis.

## What Was Built

### `treatment_dispatch.py` Module

Created at `ds-self-healing-engine/src/orchestrator/treatment_dispatch.py`. Provides:

- `parse_clinical_assessment()` — extracts actionable problems from Clinical engine assessment
- `match_problem_to_systems()` — keyword-matches findings to body-system engines
- `create_treatment_plan()` — full pipeline: assessment → parsed problems → dispatch plan
- `execute_treatment_plan()` — sends healing signals to target body systems
- Severity → intervention strength mapping (stable=0.0, critical=1.0)

### New Endpoints on Self-Healing

- `POST /v1/diagnose` — receive clinical diagnosis + auto-dispatch
- `POST /v1/treatment/plan` — dry-run treatment plan
- `POST /v1/treatment/dispatch` — execute treatment

### Body-System Dispatch Table

| System | Port | Treats |
|--------|------|--------|
| Burnet | 8100 | infection, pathogen, immune, inflammation |
| Unna | 8097 | barrier, wound, skin, integrity |
| Harvey | 8092 | perfusion, circulation, cardiac, blood |
| Morphogen | 8093 | tissue, regeneration, repair, growth |
| Beaumont | 8094 | metabolic, nutrition, digestion |
| Haldane | 8098 | respiratory, oxygen, gas, breathing |
| Bright | 8096 | toxin, waste, renal, filtration |
| Sutherland | 8099 | hormone, endocrine, cortisol |
| Hill | 8106 | muscle, bone, force, locomotion |

## Test Results

### Test 1: Simulated immune threat (elevated pathogen_load)
- Cushing seat detected: severity=warning
- Self-Healing parsed 2 problems from 2 seats
- Created 5-dispatch treatment plan
- All 5 target body systems contacted successfully (HTTP 200)
- Result: 5 dispatched, 0 failed

### Test 2: Stable organism
- All seats: severity=stable
- Self-Healing correctly returned: "no_treatment_needed"
- No dispatches sent

## Registry Update

Self-Healing entry updated in ecs.py with:
- `receives_diagnoses_from: "ds-clinical-engine"`
- `dispatches_to: [burnet, unna, harvey, morphogen, beaumont, haldane, bright, sutherland, hill]`

## Key Decision: Wire, Don't Merge

Self-Healing stays a separate engine because:
1. Body heals without diagnosis (constant autonomous repair)
2. Clinical is one input source, not the only one (Allostasis also triggers)
3. Healing is distributed across multiple body systems
