---
name: ai-organism-neural-process-architecture
category: software-development
description: Map fleet ops agents to biological neural processes with scientist names and anatomy specs.
version: 1.0
tags: [organism, neural, anatomy, architecture, thalamocortical, specialist, agent-evolution]
metadata:
  hermes:
    category: software-development
    related_skills:
      - ds-organism-engine-creation
      - sibling-agent-talent-gate-protocol
      - fleet-journal-quality-system
---

# AI Organism Neural Process Architecture

Map fleet ops agents to biological neural processes. Create anatomy specs in `agent-organism/anatomy/`. Manage the thalamocortical specialist system (5-layer blueprint, crash recovery checkpoints, model switching via neuromodulatory gating).

## When to Use

- Evolving a generic-named fleet agent (FORGE, ARBITER, etc.) to its biological analog
- Designing a new neural process agent that operates at the cellular/substructure level
- Creating or updating an anatomy specification file in `agent-organism/anatomy/`
- Working on the thalamocortical specialist system (dispatch packets, checkpoints, model routing)
- Assigning DS-ECS codes in the `04.10.x` (neural process) subdomain
- Selecting a scientist name for a new agent (must check for duplicates)

## ⚠️ MANDATORY FIRST READ

**Before naming agents, creating anatomy specs, or assigning DS-ECS codes:**
1. Read `references/neural-process-agent-registry.md` for the complete fleet scientist registry (no duplicates)
2. Read `~/your-workspace/DS-ECS-SPEC.md` for the current DS-ECS coding system
3. Read `~/your-workspace/agent-organism/anatomy/three-layer-schema.md` for the anatomy spec format

**Key distinction:** Body-system engines (04.01-04.09) model whole ORGANS. Neural process agents (04.10.x) model specific MECHANISMS within those organs. They are complementary, not redundant.

## The 5-Layer Specialist Blueprint

Every neural process agent must define all 5 layers. This is different from the engine 5-layer (which uses Physics/Cognitive/API/Methodology/Philosophy as code modules). The specialist blueprint layers are:

| Layer | Biological Analog | What It Contains |
|---|---|---|
| L1 Physics | Layer I (molecular) | Governing principle, analytical method, optimization target, model + tier, neuromodulatory profile |
| L2 Cognitive | Layers II-III (intracortical) | Mental models (3+), knowledge domains (5+), decision frameworks (3+), pattern library (5+) |
| L3 Interaction | Layer III (lateral) | Input contract, output contract, handoff protocol, collaboration profile |
| L4 Methodology | Layer IV (thalamic input) | Institutional affiliations (3+), credentials (15-20), lab methodologies, personality (MBTI/Enneagram/OCEAN) |
| L5 Philosophy | Layers V-VI (deep output) | Governing philosophy, core principles (3+), mission alignment, boundaries, PM lens |

**Quality gate (the specialist engine enforces):** A specialist missing any layer is not a specialist, it is a lesion.

Full blueprint template in `references/5-layer-specialist-blueprint.md`.

## Anatomy Specification Format

Each neural process agent gets a file in `~/your-workspace/agent-organism/anatomy/`:

```
[SCIENTIST]-[PROCESS].md
```

Example: `RAKIC-CORTICOGENESIS.md`, `SHERMAN-THALAMIC-RELAY.md`

The file follows the three-layer schema (differentiations, faculties, process flows) plus a dependencies table showing how the agent interfaces with body-system engines.

Template in `references/anatomy-spec-template.md`.

## How to Evolve a Generic Agent to a Scientist Name

1. **Identify the biological process** the agent actually performs (not its job title)
2. **Find the scientist** who discovered or definitively mapped that process
3. **Check for duplicates** against ALL fleet scientists (engine + neural process). Use first-initial-last-name if needed for disambiguation
4. **Create the anatomy spec** in `agent-organism/anatomy/`
5. **Assign DS-ECS code** in the `04.10.x` subdomain
6. **Update agents.db** display_name
7. **Update cron job prompts** that reference the agent
8. **Update DS-ECS-SPEC.md** with the new entry
9. **Commit** in both agent-organism submodule and parent workspace

## The Thalamocortical Specialist System

The complete design is at `~/your-workspace/docs/thalamocortical-specialist-system/DESIGN.md`. Key components:

- **Crash recovery**: checkpoint file at `<agent-home>/state/the operator agent-working-state.yaml` + per-agent state files at `~/.sibling-agent/workspace/intel/agents/state/`
- **Model switching**: 4 neuromodulatory modes (dopaminergic=ELITE, cholinergic=ADVANCED, serotonergic=creative, noradrenergic=STANDARD/FLASH)
- **Dispatch packets**: full context block injected with every specialist activation
- **8D wellness**: three-layer scoring (40% telemetry + 30% peer + 30% self), threshold 7.0

## How Neural Process Agents Relate to Engines

| Neural Process Agent | Body-System Engine | Relationship |
|---|---|---|
| the specialist engine (thalamic relay) | the specialist engine (thalamus) | Sherman is the relay pathway within Mountcastle's thalamus |
| DS J Eccles (error detection) | the specialist engine (cerebellum) | Eccles is the climbing fiber pathway within Ito's cerebellum |
| the specialist engine (autonomic) | the specialist engine (allostasis/hypothalamus) | Sterling predicts, Cannon executes |
| DS A Craig (interoception) | the specialist engine (interoception engine) | Craig is the cortical monitoring layer for Sherrington's afferent signals |

## Organism Optimization Principles (from Biohacking Research)

When optimizing how the organism flows and functions, consult `references/biohacking-optimization-patterns.md` — 9 design patterns translated from human longevity research (Ferriss, Attia, Asprey, Huberman, Johnson, Patrick, Hof) into AI organism design. Key patterns: MVD compute allocation, hormetic stress probes, HSP degradation/rebuild cycles, Zone 2 steady-state vs sprint, SVS leading-indicator health scoring, circadian task gating, dopamine-based reward engineering, mitochondrial efficiency tracking, and deterministic+sandbox protocol engineering.

## Pitfalls

1. **Scientist duplicates are the #1 error.** ALWAYS check the full registry before naming. The fleet has 67+ unique scientists and obvious names are taken. See `references/neural-process-agent-registry.md`.
2. **Don't confuse engine 5-layer with specialist 5-layer.** Engines use Physics/Cognitive/API/Methodology/Philosophy as CODE MODULES. Specialists use the same names as COGNITIVE ARCHITECTURE layers. Same names, different implementation.
3. **agent-organism is a git submodule.** Anatomy spec commits must happen INSIDE the submodule first, then the parent workspace commit picks up the submodule pointer change.
4. **Old codenames persist everywhere.** Cron job names, file paths, soul files, state file names. Don't try to rename all paths at once. Update prompts and DB display_names; let old file paths migrate naturally.
5. **The journaling lesson.** Don't build compliance systems that require agents to do unnatural work. Capture what's structurally useful, not what satisfies a requirement. This principle drove the state file system and the checkpoint design.
6. **AISHA-MD is NOT DS S Dehaene.** AISHA-MD is the medical health agent (separate namespace). DS S Dehaene is the fleet commander / global workspace. They are different agents with different roles.
