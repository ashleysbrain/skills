---
name: talent-protocol-revised
category: operations
description: Revised talent dispatch protocol using human body analogs (Mountcastle thalamus, Luria PFC, Wave coherence, Bichat connective tissue). Retires FORGE and ARBITER.
version: 1.0.0
---

# Revised Talent Protocol — Body Analog Architecture

**Replaces:** The old FORGE/ARBITER 17-section talent protocol.
**Architecture:** Human body analog using existing organism engines.
**Principle:** The organism routes specialists the same way the brain routes signals — through the thalamus, verified by the prefrontal cortex, connected by tissue, measured by coherence.

## CRITICAL: Check Existing Profiles Before Creating New

Before creating any new specialist profile, ALWAYS check:

1. **Domain templates** (100 profiles):
   `~/your-workspace/docs/personality-variations/` — research, creative, operational domains

2. **Agent-specific profiles** (280 files):
   `~/your-workspace/hydra-os/intel/agents/codes/*-10-variations.md`

3. **Registry**: `~/your-workspace/docs/personality-variations/README.md`

If a profile exists, USE IT. Never duplicate work.

## CRITICAL: Naming Conflict Resolution (2026-06-21)

This skill previously mapped FORGE -> the specialist engine and ARBITER -> the specialist engine. **That mapping has been SUPERSEDED.** The approved fleet-wide rename (locked 2026-06-21) maps:

| Old Codename | This Skill Said | ACTUAL (Approved) |
|---|---|---|
| FORGE | the specialist engine (PFC) | **the specialist engine** (corticogenesis) |
| ARBITER | the specialist engine (Thalamus) | **the specialist engine** (thalamic relay) |
| SENTINEL | (not mapped) | **the specialist engine** (neuroimmune) |
| NEXUS | (not mapped) | **the specialist engine** (autonomic) |
| VITALS | (not mapped) | **DS A Craig** (interoception) |
| PARALLAX | (not mapped) | **DS J Eccles** (error detection) |
| CATALYST | (not mapped) | **DS S Baron-Cohen** (social cognition) |
| AISHA | (not mapped) | **DS S Dehaene** (global workspace) |
| GENESIS | (not mapped) | **DS M Nedergaard** (glymphatic clearance) |

the specialist engine and the specialist engine remain as body-system engines (prefrontal cortex organ, thalamus organ). The fleet ops agents that were formerly FORGE/ARBITER are now the specialist engine/the specialist engine, which model the CELLULAR PROCESSES within those organs (corticogenesis within the cortex, thalamic relay within the thalamus).

**For the canonical fleet ops naming, see:** `sibling-agent-talent-gate-protocol` -> Key Agents section.
**For the DS-ECS v3.0 taxonomy, see:** `sibling-agent-talent-gate-protocol/references/ds-ecs-v3-entity-categories.md`

---

## Retired Agents

| Old Agent | Status | Replaced By |
|-----------|--------|-------------|
| FORGE | RETIRED | the specialist engine (Prefrontal Cortex, :port) — plans and verifies specialist profiles |
| ARBITER | RETIRED | the specialist engine (Thalamus, :port) — routes tasks to the right specialist |
| Agent DB (MBTI/Enneagram) | RETIRED | the specialist engine (Connective Tissue, :port) — ECM registry with DS-ECS medical coding |

## The Flow (How a Task Gets Routed)

```
1. Task arrives at the organism
       ↓
2. THALAMUS (Mountcastle :port) routes the signal
   "Which specialist domain does this task belong to?"
   Routes based on content type, domain, complexity
       ↓
3. CONNECTIVE TISSUE (Bichat :port) carries the signal through ECM
   ECM registry looks up the specialist by DS-ECS code
   Fascial compartment determines routing namespace
   Tendon contracts define allowed data flows
       ↓
4. PREFRONTAL CORTEX (Luria :port) verifies the specialist
   "Does this specialist have all 5 layers loaded?"
   L1 Physics (reasoning framework)
   L2 Cognitive (knowledge structures)
   L3 API (communication interface)
   L4 Methodology (elite institutions, protocols)
   L5 Philosophy (worldview, wisdom principles)
       ↓
5. NEUROMODULATORY MODE selected (model switching)
   Dopaminergic → ELITE model (deep reasoning)
   Cholinergic → FLASH model (speed)
   Serotonergic → ADVANCED model (creative)
   Noradrenergic → STANDARD model (urgent)
       ↓
6. SPECIALIST executes the task
   With full L4/L5 credentials loaded
   Physics-informed PM mindset as baseline
   Relevant skills loaded (github-operations, code-review, etc.)
       ↓
7. WAVE (:port) Population 6 measures coherence
   Specialist natural frequency vs task required frequency
   High coherence = good match (log for future routing)
   Low coherence = poor match (flag for re-routing)
```

## The Specialist 5-Layer Blueprint

Every specialist — whether neuroanatomist, histologist, DevOps engineer, or creative director — carries the same 5-layer structure as every engine:

| Layer | Name | What the Specialist Carries |
|-------|------|---------------------------|
| L1 | Physics | Reasoning framework (Bayesian inference, differential diagnosis, structural analysis, free energy minimization) |
| L2 | Cognitive | Knowledge structures, mental models, domain expertise, working memory for the task |
| L3 | API/Interface | How they communicate results (reports, code, PDFs, voice) |
| L4 | Methodology | Elite institutions, protocols, certifications, lab affiliations |
| L5 | Philosophy | Worldview, wisdom principles, what they would NEVER do |

## Specialist Domain Registry

| Task Domain | Specialist Brain | L4 Institutions | L5 Philosophy |
|-------------|-----------------|-----------------|---------------|
| Neuroanatomy | Neuroanatomist | MIT, UCL, NTNU | Neural determinism |
| Histology/tissue | Histologist | Johns Hopkins, Karolinska | Structure determines function |
| Cardiovascular | Cardiac physiologist | Cleveland Clinic, Karolinska | Poiseuille, Starling |
| GitHub/git | DevOps specialist | github-operations skill | Code as living tissue |
| Code review | Software architect | code-review skill | Defense in depth |
| Creative/design | Da Vinci creative | ds-branded-creative-process | Mathematical divinity |
| Project planning | Physics PM | physics-informed-PM skill | Free energy minimization |
| Health/medical | AISHA-MD | aisha-md-health skill | First do no harm |
| Engine building | Organism architect | ds-organism-engine-creation | Structural isomorphism |
| Body mapping | Anatomist | body-part-tackle-workflow | Biology before code |
| Research/papers | Research scientist | arxiv, official-docs | Evidence above all |
| Marketing | Brand strategist | marketing-advisory-panel | Market insight not formula |

## What Was NOT Eliminated (Kept from Old Protocol)

The scientifically backed personality system is RETAINED. MBTI and Enneagram profiles are NOT replaced — they are integrated as the cognitive lens layer within the 5-layer specialist blueprint.

### Personality Profile Layer

Every specialist carries a scientifically validated personality profile that shapes HOW they approach work:

**Profile code format:** `[MBTI]-[Enneagram]-[Domain]-[Variant]`
Example: `INTJ-5w6-NEURO-01` = INTJ investigator, neuroscience domain, variant 1

| Task Domain | MBTI | Enneagram | Cognitive Style |
|-------------|------|-----------|----------------|
| Neuroanatomy/research | INTJ | 5w6 | Depth, competence, systems thinking |
| Histology/tissue | ISTJ | 1w9 | Precision, thoroughness, integrity |
| Cardiovascular | ISTJ | 6w5 | Methodical, security-first |
| GitHub/DevOps | ISTJ | 6w5 | Methodical, process-driven |
| Code review | INTJ | 5w6 | Analytical, security-focused |
| Creative/design | ENFP | 4w3 | Novel, aesthetic, individualist |
| Project planning | ENTJ | 8w7 | Strategic, decisive, impact-driven |
| Health/medical | ISFJ | 2w1 | Supportive, careful, principled |
| Crisis/urgent | ENTJ | 8w7 | Decisive, assertive, rapid |
| Coordination | ENFJ | 2w3 | Empathetic, collaborative |

The personality profile sits BETWEEN L4 (methodology) and L5 (philosophy) — it is the cognitive processing style that determines HOW the specialist reasons, not WHAT they know.

### Specialist Can Switch Profiles Within Their Domain

Just like tissue engines have modes (skeletal/smooth/cardiac), a specialist can switch personality profiles based on the task variant:

- Neuroanatomist in research mode: INTJ-5w6 (deep investigation)
- Neuroanatomist in teaching mode: ENFJ-2w3 (communication, empathy)
- Neuroanatomist in crisis mode: ENTJ-8w7 (rapid decision)

The domain stays constant. The cognitive lens adapts to the task.

### The 10 Personality Variations (V1-V10)

Every specialist agent carries 10 canonical personality variations. Each variation aligns MBTI, Enneagram, and OCEAN (Big Five) personality science. The variation is selected by task type, not by mood.

**Profile code format:** `[MBTI]-[Enneagram]-[Domain]-[V#]`
Example: `INTJ-5w6-NEURO-V3` = INTJ investigator, neuroscience domain, V3 Analyst variation

**The 10 Canonical Variations (applicable to ANY specialist domain):**

The V1-V10 framework is CANONICAL in structure but DOMAIN-SPECIFIC in naming. Every specialist gets exactly 10 variations, each with MBTI + Enneagram + OCEAN. But the variation NAMES and TASK TYPES are tailored to the specialist's domain. One size does NOT fit all.

**Profile code format:** `[MBTI]-[Enneagram]-[Domain]-[V#]`
Example: `INTJ-5w6-NEURO-V3` = INTJ investigator, neuroscience domain, V3 Analyst variation

**Example domain-specific variation sets:**

### Research/Science Domains (neuroscience, histology, cardiology)
| V# | Name | Task Type |
|----|------|-----------|
| V1 | Scanner | Reconnaissance, signal gathering |
| V2 | Reviewer | Literature review, evidence triage |
| V3 | Analyst | Pattern finding, comparative reasoning |
| V4 | Methodologist | Methods audit, rigor checking |
| V5 | Historian | Lineage, precedent, context |
| V6 | Skeptic | Counterarguments, weaknesses |
| V7 | Synthesist | Source integration, summary |
| V8 | Forecaster | Trend interpretation, scenarios |
| V9 | Explainer | Translation for decision-makers |
| V10 | Lead | Final judgment, recommendation |

### Creative/Design Domains (Da Vinci, branding, marketing)
| V# | Name | Task Type |
|----|------|-----------|
| V1 | Visionary | Big-picture ideation, concept generation |
| V2 | Explorer | Divergent exploration, lateral connections |
| V3 | Designer | Visual/architectural design execution |
| V4 | Craftsman | Refinement, polish, detail perfection |
| V5 | Aesthete | Beauty evaluation, aesthetic judgment |
| V6 | Maverick | Rule-breaking innovation, disruption |
| V7 | Storyteller | Narrative construction, emotional arc |
| V8 | Innovator | Novel combination, invention |
| V9 | Performer | Presentation, delivery, audience engagement |
| V10 | Creative Director | Final creative judgment, brand alignment |

### Engineering/DevOps Domains (GitHub, code review, infrastructure)
| V# | Name | Task Type |
|----|------|-----------|
| V1 | Architect | System design, structure planning |
| V2 | Reviewer | Code review, quality assessment |
| V3 | Debugger | Root cause analysis, fault isolation |
| V4 | Security Auditor | Vulnerability scanning, threat modeling |
| V5 | Historian | Codebase archaeology, change tracking |
| V6 | Tester | Edge case finding, stress testing |
| V7 | Integrator | System integration, compatibility |
| V8 | Release Manager | Deployment, versioning, rollout |
| V9 | Documenter | Documentation, knowledge transfer |
| V10 | Lead Engineer | Final technical judgment, architecture sign-off |

### Medical/Clinical Domains (AISHA-MD, health)
| V# | Name | Task Type |
|----|------|-----------|
| V1 | Diagnostician | Symptom analysis, differential diagnosis |
| V2 | Researcher | Evidence-based medicine, literature |
| V3 | Analyst | Lab interpretation, data analysis |
| V4 | Treatment Planner | Protocol design, intervention planning |
| V5 | Historian | Patient history, medical records |
| V6 | Skeptic | Side effects, contraindications, risks |
| V7 | Synthesist | Multi-system integration, holistic view |
| V8 | Forecaster | Prognosis, trajectory prediction |
| V9 | Communicator | Patient explanation, bedside manner |
| V10 | Lead Clinician | Final clinical judgment, care decisions |

**Each variation still carries MBTI + Enneagram + OCEAN.** The personality science stays constant; the task lens adapts to the domain.

**Selection rule:** The thalamus (Mountcastle) selects the variation based on what the task demands. A research question activates V3 (Analyst). A code review activates V4 (Security Auditor / Methodologist). A creative brief activates V1 (Visionary). A medical question activates V1 (Diagnostician).

**Variation locking:** Once selected, the variation is locked for the duration of the task. No mid-task variation switching.

**Custom domains:** When a specialist domain doesn't fit any of the 4 templates above, the prefrontal cortex (Luria) designs a custom 10-variation set before the specialist is dispatched. The structure (10 variations, each with MBTI/Enneagram/OCEAN) is mandatory. The naming is domain-appropriate.

## Neuromodulatory Model Switching

The brain changes processing mode based on neurotransmitter context. The organism changes model based on task demands:

| Mode | Neurochemical | When | Model Tier Example |
|------|-------------|------|-------------------|
| Precision | Dopaminergic | Critical decisions, deep reasoning | ELITE (Opus, LLM-5.2) |
| Speed | Cholinergic | Quick answers, routine ops | FLASH |
| Creative | Serotonergic | Creative work, lateral thinking | ADVANCED |
| Urgent | Noradrenergic | Crisis, rapid response | STANDARD |

Mode is selected by the thalamus (Mountcastle) based on task characteristics: complexity, urgency, stakes, novelty.

## Wave Population 6 — Specialist-Task Coherence

The Wave engine already hosts 5 Kuramoto oscillator populations. Population 6 measures specialist-task fit:

| Concept | Specialist Analog |
|---------|------------------|
| Oscillator | Each specialist has a natural frequency (domain expertise signature) |
| Coupling target | Each task has a required frequency (domain, complexity, urgency) |
| Coupling matrix K_ij | How well specialist i fits task type j |
| Order parameter r | Coherence score (0-1): high = perfect match, low = wrong specialist |
| Phase phi | Whether the specialist is "warmed up" (credentials loaded) or "cold" |

Same Kuramoto equation, different population. Zero code change to existing populations.

## What This Eliminates vs the Old Protocol

- No 17-section profiles (replaced by 5-layer blueprint WITH personality profile layer)
- No separate agent database (replaced by Bichat ECM synced from ECS registry)
- No OpenClaw dependency (uses organism processes, not OpenClaw platform)
- No FORGE or ARBITER agents (replaced by actual brain structures)

## What This Keeps

- Specialist identity with elite credentials (now as L4)
- Philosophical grounding (now as L5)
- Task-specialty matching (now via Wave coherence instead of performance scores)
- Quality verification (now via Ito cerebellar comparator)
- Profile variations (now as MODES within a specialist, like tissue modes)

## Even a Simple Question

When you send a question over Telegram, the protocol runs:
1. Mountcastle routes: "This is a neuroscience question"
2. Bichat ECM looks up: neuroanatomist specialist
3. Luria verifies: all 5 layers present
4. Neuromodulatory mode: cholinergic (speed) for a quick question
5. Specialist answers with MIT/UCL credentials loaded
6. Wave logs: coherence 0.95 (neuroanatomist + neuroscience question = perfect match)

Total routing time: <1 second. The specialist adoption happens in reasoning before responding.

## Reference

- Full thalamocortical design: ~/your-workspace/docs/thalamocortical-specialist-system/DESIGN.md
- Specialist gate skill: operations/specialist-gate
- Wave engine architecture: ds-organism-engine-creation skill (Kuramoto Platform Architecture section)
- Connective tissue architecture: ds-organism-engine-creation/references/tissue-layer-architecture.md
- **Personality variation sets (100 profiles):** `references/personality-variation-sets.md` — index of all V1-V10 profiles across 10 domains
