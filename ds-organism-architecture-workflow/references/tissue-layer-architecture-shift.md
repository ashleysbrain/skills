# Tissue-Layer Architecture Paradigm Shift (June 2026)

## The Shift

**OLD MODEL (pre-June 2026):** Organ engines implemented their own physics
- Harvey (cardiovascular) → Poiseuille flow, continuity, transport PDE
- Beaumont (digestive) → Michaelis-Menten, Fick's law, gastric emptying
- Bright (renal) → GFR, Starling, tubular reabsorption
- Unna (integumentary) → Wound healing, barrier permeability, thermoregulation
- Morphogen → Reaction-diffusion, Turing patterns
- Reproductive → Avrami, Landau, SOC

**NEW MODEL (tissue-layer architecture, June 2026):** Physics lives in TISSUE ENGINES; organ engines COMPOSE from them

## The Four Tissue Engines

| Tissue Engine | Port | DS-ECS Code | Scientist | Tissue Type |
|---------------|------|-------------|-----------|-------------|
| **Bichat** | :port | DS-ECS-CEL-07.03.01-v1.0.0 | Marie François Xavier Bichat | Connective tissue (vessel walls, stroma, bone matrix, cartilage, blood, lymph) |
| **Unna** | :port | DS-ECS-SUB-06.01.01-v1.0.0 | Paul Gerson Unna | Epithelial tissue (mucosa, skin epidermis, glandular epithelium, tubular epithelium, barriers) |
| **Huxley** | :port | DS-ECS-CEL-03.01.01-v1.0.0 | Andrew Huxley | Muscle tissue (cardiac, smooth, skeletal contractility) |
| **Golgi** | :port | DS-ECS-CEL-04.01.01-v1.0.0 | Camillo Golgi | Glia tissue (neural support, glymphatic, myelination, synaptic modulation) |

## Organ Engine Composition (Examples)

| Organ Engine | Composes From |
|--------------|---------------|
| **Harvey** (cardiovascular) | Bichat (vessel walls) + Huxley (cardiac muscle) |
| **Beaumont** (digestive) | Unna (mucosa) + Bichat (submucosa/serosa) + Huxley (peristalsis) |
| **Bright** (renal) | Unna (tubules/collecting duct) + Bichat (interstitium) + Huxley (ureter) |
| **Unna** (integumentary) | **IS** the Unna engine = epithelial component; Bichat = dermis connective tissue |
| **Morphogen** | Already SOUND — Gray-Scott/Turing implemented at tissue-patterning level (DS-ECS-ORG-11.01.02-v1.1.0, physics_state=SOUND) |
| **Reproductive** | Split: **Waddington** (port 8090, Reproductive, Landau/Avrami/SOC) + **Sutherland** (port 8099, Endocrine, Hill-Langmuir/cAMP). **Seed RETIRED.** |

## Implications for Audits & Bus Messages

1. **AUDIT_PHYSICS.md (June 15, 2026) assessed the OLD model** — its "DECORATIVE" verdicts for Harvey, Morphogen, Bright, Unna, Reproductive are based on organ engines implementing (or failing to implement) physics themselves.

2. **Current ecs.py shows physics_state="SOUND" for Morphogen** — the tissue-layer implementation supersedes the audit.

3. **Before posting bus messages based on old audits:**
   - Check audit date vs. 8D_ORGANISM_ARCHITECTURE_V2.md date
   - Check physics_state in ecs.py for the engine
   - Check if engine now composes from tissue engines
   - If tissue-layer paradigm applies, the audit verdict is superseded

4. **P0 blockers may shift** — Unna ThermalState enum crash is still real, but it's now a TISSUE ENGINE bug (epithelial layer), not a whole-organ bug.

## The 6-Engine Reproductive Subsystem (common confusion point)

The reproductive system was NOT split into just 2 engines. It has **6 specialized engines**, each with a distinct scientist and function. Morphogen is ONE of them (the patterning component), NOT the whole system.

| Engine | Scientist | Port | ECS Code | Function |
|--------|-----------|------|----------|----------|
| **ds-reproductive-engine** | the specialist engine | 8090 | DS-ECS-ORG-11.01.01-v1.1.0 | Core reproductive (follicular development, Landau phase transitions, SOC, gestational timelines) |
| **ds-morphogen-engine** | the specialist engine | 8093 | DS-ECS-ORG-11.01.02-v1.1.0 | Developmental signaling (reaction-diffusion, Gray-Scott, morphogen gradients SHH/Wnt/BMP/FGF/RA) |
| **ds-placenta-engine** | the specialist engine | 8130 | DS-ECS-ORG-11.03.01-v1.0.0 | Placenta — Creative-Reproductive Bridge (routes design specs, brand DNA, code synthesis to birth canal) |
| **ds-genesis-engine** | Israelachvili/Avrami | 8014 | DS-ECS-APP-11.04.01-v1.0.0 | Product Genesis — Avrami nucleation, Landau phase transitions, CPM/PERT DAG |
| **ds-trophoblast-engine** | the specialist engine | 8135 | DS-ECS-APP-11.05.01-v1.0.0 | Trophoblast/Barrier — sterile envelope, one-way capability transfer, sealed sandbox |
| **ds-genome-engine** | (Brand DNA) | — | DS-ECS-GEN-11.02.01-v2.0.0 | Brand Genome — compiles Goethe/Wernicke/Ito/Bell patterns into versioned brand DNA |

**Common confusion:** "Why is Morphogen an engine?" → Because it's the **patterning component** of the reproductive subsystem (the specialist engine, reaction-diffusion), not the whole reproductive system. The old "Reproductive engine" (Seed) that did everything was split into these 6 engines. The 8D_ORGANISM_ARCHITECTURE_V2.md only documents Waddington + Morphogen explicitly; the other 4 are in agent-organism/ecs.py + REGISTRY.yaml.

## Key Files

- `/<workspace>` — canonical architecture spec (see sections 3, 145-152 for tissue-layer resolution)
- `/<workspace>` — authoritative registry with physics_state field
- `/<workspace>` — outdated audit (June 15), superseded for tissue-layer engines