---
name: ai-organism-biohacking
description: Translate biohacking and health optimization literature into AI organism design patterns. Extracts physiological protocols and maps them to multi-agent system optimization.
version: 1.0.0
author: the principal Williams, the operator agent Agent
---

# AI Organism Biohacking

Use when the user asks to optimize the AI organism's processes using biological analogies, or wants to translate health/biohacking research (Greenfield, Ferriss, Attia, Huberman, Asprey, Johnson, Hof, Patrick, etc.) into organism design patterns.

## When to Use

- User asks to "biohack the organism" or apply health optimization principles to the AI system
- User references a biohacker's work (Greenfield's *Boundless*, Ferriss's *4-Hour Body*, Attia's *Outlive*, etc.) in the context of organism design
- User asks how body parts should flow and work together in the organism
- User wants to audit organism processes against biological system interaction patterns
- Building or optimizing organism cron jobs, scoring pipelines, bus communication, or circadian scheduling

## The Core Thesis

Every optimization principle from human biohacking has a direct analog in multi-agent system design. The mapping is structural, not metaphorical. Both systems are networks of semi-autonomous nodes communicating via signals, regulated by feedback loops, and subject to degradation patterns. Naming components after body parts is NOT enough — the biohacking literature tells us HOW those parts actually communicate, regulate, and fail.

## The Eight Key Sources

| Source | Core Framework | Key Transfer to Organism |
|--------|---------------|-------------------------|
| Greenfield *Boundless* (2020) | 10 interlocking body systems; interactions matter more than any single system | Systems interaction audit; no component optimization in isolation |
| Ferriss *4-Hour Body* (2010) | Minimum Effective Dose (MED); 80/20 rule | Compute budgeting; find the 20% of processes driving 80% of health |
| Attia *Outlive* (2023) | Medicine 3.0 (prevention); Centenarian Decathlon (target-state engineering) | Define healthy steady state, reverse-engineer monitoring |
| Asprey *Super Human* (2019) | Seven pillars of aging; bottleneck identification | Free-energy gate F = cost - T*info_gain is biohacking by another name |
| Huberman (2021-present) | Nervous system = master regulator; dopamine protocol; neuroplasticity framework | Focus phase + consolidation phase; dopamine reward design |
| Johnson Blueprint (2023-present) | Protocol engineering; 300+ biomarkers; data-driven revision | 8D/TWC scoring = our Blueprint; free-energy gate = protocol revision |
| Hof Wim Hof Method | Voluntary autonomic control; breathwork + cold | Autonomic bridge manual override for emergency escalation |
| Patrick FoundMyFitness | Sauna science; heat shock proteins; substrate-first principle | Base infrastructure must work BEFORE adding features |

## The 9 Transferable Protocols

See `references/protocol-catalog.md` for the full protocol catalog with biological mechanisms, organism analogs, and implementation guidance. See `references/greenfield-boundless-body-systems.md` for the 10-system body-system deep dive with specific biomarkers, dosing, and AI transfer patterns extracted from Boundless (2020).

| # | Protocol | Source | Organism Application |
|---|----------|--------|---------------------|
| 1 | HRV → Score Volatility | HRV literature, Hof | Track rolling volatility of dimension scores; low volatility = losing adaptive capacity |
| 2 | Zone 2 → Steady-State Processing | Attia, Greenfield | Most processes at 20-30% compute; burst (VO2 max) for short sprints only |
| 3 | Hormesis → Chaos Engineering | Hof, Asprey | Monthly controlled failures; track recovery time; trending up = STOP |
| 4 | Heat Shock → Refactoring Cycles | Patrick, Greenfield | Weekly degrade-rebuild-verify cycle applied to entire organism |
| 5 | MED → Compute Budgeting | Ferriss | Minimum frequency per process; tag compute_cost; 80/20 waste elimination |
| 6 | Gut-Brain → Multi-Channel Bus | Greenfield, Patrick | alert (vagus), modulation (hormonal), cascade (immune), resource (metabolite) |
| 7 | Dopamine → Reward Function | Huberman | Low stable baseline; intermittent peaks; post-peak dip allowed |
| 8 | Centenarian Decathlon → Target-State | Attia | Define healthy steady state for 90 days; score vs target |
| 9 | Circadian Biology → the specialist engine | Huberman | Morning (high), afternoon (moderate), evening (wind-down), night (rest) |

## Research Workflow

### Phase 1: Parallel Deep Research
Fan out 2-3 subagents for deep reading of primary sources. Each subagent:
- Searches web for the specific author's core frameworks
- Extracts key protocols, mechanisms, and transferable principles
- Returns a structured summary with source citations

### Phase 2: Consolidation
While subagents research, the main agent:
- Drafts the analysis structure (protocols, mapping, priority stack)
- Reads live organism code to ground the translation (not just metaphor)
- Cross-references with existing design docs (coupling V2, COUPLING_V2_PHYSICS_DESIGN.md, etc.)

### Phase 3: Deliverable
- Write the consolidated analysis to `~/your-workspace/BIOHACKING-THE-AI-ORGANISM.md`
- Post build specs to operator bus for sibling-agent handoff where code changes are needed
- Update this skill's protocol catalog with any new protocols discovered

## Body System → Organism Gap Analysis

Run this mapping to identify where the organism is missing physiological flow patterns:

| Body System | Organism Analog | What's Usually Working | What's Usually Missing |
|------------|----------------|----------------------|------------------------|
| Nervous | Sherman, Wernicke, Andreasen | Routing dispatch | Neuroplasticity tracking; focus/alertness cycles |
| Cardiovascular | Harvey, heartbeat watchdog | Heartbeat runs | HRV analog (score volatility); bus load measurement |
| Endocrine | Coupling matrix | Pair coupling exists | Slow hormonal signaling; dopamine protocol |
| Mitochondrial | Compute allocation | Implicit in cron | MED optimization; efficiency metric |
| Digestive | Operator bus | Bus exists | Multi-channel; cascade propagation |
| Immune | Critical slowing watchdog | Detection exists | Hormesis cycles; immune memory |
| Sleep/Recovery | the specialist engine, context compression | Engine runs | Ultradian cycle; deep sleep phase |
| Musculoskeletal | Engine processes | Running | Dependency health monitoring |
| Detox | Skill curator, memory purge | Skills archived | Heat-shock cycles for code |
| Skin/Barrier | Security, auth | Protected | Permeability control |

## Priority Stack Methodology

Rank interventions by free energy: F = cost - T*info_gain.

- **Tier 1 (F << 0, immediate):** Wire base infrastructure (substrate-first), add volatility metrics, multi-channel bus, circadian bands
- **Tier 2 (-1 < F < 0, high impact):** Hormesis cron, heat-shock refactoring, MED budgeting, target-state engineering, sparse coupling
- **Tier 3 (F approx 0, medium):** Dopamine reward protocol, dependency health, bus permeability

## The Missing Piece

**We measure components in isolation. The biohacking movement measures INTERACTIONS.**

Specific gaps to address:
- Transfer entropy (dimension A precedes B) — code exists in twc_coupling_physics.py but not run regularly
- Situational modifiers (context vector from V2 design)
- Organism-level volatility (HRV analog)
- Recovery time from stressors

**Measure what interacts, not just what exists.** That is the frontier.

## Pitfalls

- Do NOT just name components after body parts without wiring their interactions
- Do NOT cite design docs as evidence — only live code, DB state, and running processes count
- Do NOT optimize one system in isolation — Greenfield's lesson: the interactions are the bottleneck
- Do NOT skip the "substrate first" principle (Patrick) — base infrastructure must work before adding features
- Do NOT conflate DENSE triples (all 56 from pair kappas) with SPARSE triples (biology-justified with free-energy gate) — they are different approaches; keep dense as null model, layer sparse on top

## Related Skills

- `divinity-health/your-org-organ-mapping` — naming conventions, ECS registration, rename checklist
- `body-part-tackle-workflow` — deep anatomical mapping + ECS registration for body parts
- `operations/8d360-unified-scoring-pipeline` — unified 8D scoring calculator
- `operations/propaganda-twc-scoring` — proprietary TWC scoring formula
- `creative/the operator agent-creative-production-spine` — the operator agent organism creative nervous system
