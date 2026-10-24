---
name: agent-consortium-design
description: >-
  Design and build agent consortiums for ANY domain — marketing, health, legal,
  education, operations. A consortium is an ephemeral task-swarm (microbial
  isomorphism) that carries tasks through the organism's process flows from
  intake to output. Covers the generalizable blueprint, selection math,
  decision sequence, pathology reporting, and engine endpoint contracts.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes.tags:
    - consortium
    - agents
    - organism
    - architecture
    - generalizable
  hermes.category: software-development
  hermes.related_skills:
    - marketing-metabolism-production
    - body-part-tackle-workflow
    - organism-integrity-verification
---

# Agent Consortium Design

A **consortium** is a domain-specific task swarm — a group of specialist agents
that forms around a task, carries it through the organism's process flows, and
disbands when complete. Biological isomorphism: **microbial consortium**
(different specialists in symbiotic metabolism of one substrate).

This skill covers the GENERALIZABLE framework. Marketing is the first use case
that proved the pattern. Health, legal, education, operations, or any domain
follows the same blueprint.

## When to Use

- Building a new consortium for a domain that does not yet have one
- Extending an existing consortium with new process flows
- Designing the selection math for agent decision-making
- Specifying engine /process endpoint contracts for sibling-agent
- Creating the decision sequence (formula ordering) for a domain

## Prerequisites

- The organism body parts (engines) for the target domain must exist or be planned
- the specialist engine router must be operational for specialist routing
- The 8D Human Wellness Gate and the specialist engine DNA must be inheritable (they are immutable)

## The 8 Components Every Consortium Contains

| Component | What It Is |
|-----------|-----------|
| Knowledge Layer | Domain research + frameworks + case studies compiled into a curriculum |
| Process Flows | Sequences through organism body parts. A consortium manages MULTIPLE flows. |
| Selection Engine | Deterministic math for choosing which approach to apply (NOT heuristics) |
| Decision Sequence | The exact order agents evaluate, decide, and act (phase-dependent formula ordering) |
| Quality Gates | Hard checks content must pass before output |
| Pathology System | Reporting when body parts are missing or broken |
| Carriage Controller | Executable code that chains the process flows |
| DNA (Immutable) | 8D wellness gate, DS brand markers, healing mission — inherited by ALL consortiums |

## The DNA Every Consortium Inherits

Regardless of domain, every consortium inherits these immutable elements:

1. **8D Human Wellness Gate** — ALL 8 dimensions protected (Physical, Psychological, Intellectual, Social, Spiritual, Vocational, Financial, Environmental). No hierarchy of harm. Any negative score = REJECT.
2. **the specialist engine DNA Markers** — physics-informed, bio-isomorphic, anti-slop, elite standard
3. **Healing Mission** — heal humanity across all 8 dimensions. POSITIVE language only.
4. **Selection Math Structure** — Score = weighted sum, free energy ratio gate, superposition hold
5. **Decision Sequence** — 9 phases from intake to learning
6. **Pathology Reporting** — file orders when body parts are missing/broken

## Multiple Process Flows Per Consortium

A single consortium manages MULTIPLE process flows. Different task types follow
different flows through different body parts.

### Marketing Consortium Example (first instance)

| Process Flow | Task Types | Body Parts |
|-------------|-----------|-----------|
| Content Production | Social posts, newsletters, PDFs | Wernicke, Goethe, Bell, Luria, Boucher |
| Campaign Strategy | Positioning docs, GTM plans | Wernicke, Franklin, Luria |
| Distribution | Publishing to platforms | Harvey, Malpighi/Muller/Selye/Metchnikoff/Gershon |
| Analytics | Performance measurement | Helmholtz, Burnet, Harvey |
| Brand Integrity | IP protection | Allostasis, Franklin, Luria |

## How to Build a New Consortium (5 Phases)

### Phase 1: RESEARCH (before any building)

1. Gather domain knowledge — state of the art, elite institutions, named methodologies, case studies. Use parallel subagents for breadth. Do NOT rush.
2. Extract quantitative math — the formulas, equations, models. How do domain experts measure quality, predict outcomes, make decisions?
3. Compile case studies — who has done this domain brilliantly? What were the specific moves? What transferable principles emerge?

### Phase 2: CURRICULUM (the knowledge layer)

4. Build the domain curriculum — modules covering strategic foundations, audience calibration, approach strategy, format/channel selection, academic rigor.
5. Build the selection math — the deterministic scoring function. What criteria matter for THIS domain? What are the weights? What are the hard gates?

### Phase 3: PROCESS DESIGN (how the organism handles it)

6. Map the process flows — identify ALL flows the consortium will manage. Each goes through different body parts in a specific order.
7. Build the decision sequence — the exact order agents evaluate, decide, act. Which formulas run at which phase?
8. Build the quality gates — what must pass before output? Domain-specific rules.

### Phase 4: INTEGRATION (connecting to the organism)

9. Build the carriage controller — executable code that chains the process flows.
10. Verify all body parts exist and respond — health sweep of every engine in every flow.
11. File pathology orders for missing parts.
12. Wire engine /process endpoints — engines must actually DO something, not just respond to health checks.

### Phase 5: COMPLETION (before any testing)

13. Connect everything end-to-end as executable code — no simulated outputs.
14. Verify full integration — the entire system runs from intake to output to learning without breaks.
15. ONLY THEN test — with a real task. Not before.

**CRITICAL (user correction 2026-06-29):** "You haven't even built and connected the engines yet... you need to build it all the way before that I try." Do NOT push for testing before the system is fully built. Build COMPLETELY, then test. Asking for test ideas while engines are unwired is a physics mindset failure (adiabatic violation).

## The Selection Math (DNA-encoded)

```
Score(P, T) = 0.30*DNA(P) + 0.25*EIGHT_D(P) + 0.20*FIT(P,T)
              + 0.15*EVIDENCE(P) + 0.10*CONTRARIAN(P)
```

Hard gates: 8D < 0 -> REJECT. DNA < 0.5 -> REJECT.
Free energy ratio: F = COST / [Score * (1 + INFO_GAIN)]. F >= 1.0 -> SKIP.
Superposition: hold top 3 candidates, collapse on quality gate measurement.

Weights are domain-adjustable within +-0.05 per generation. The hard gates
and DNA markers are immutable.

See `references/selection-math-detail.md` for the full math spec.
See the marketing instance at `marketing-consortium/src/selection_engine.py`
for executable code.

## The Decision Sequence (9 Phases)

The formulas do NOT run all at once. They apply at different phases:

| Phase | What Happens | Math Applied |
|-------|-------------|-------------|
| 0. Classify | Sort the task | None |
| 1. Hard Gates | 8D + DNA check | None (rules) |
| 2. Philosophy Selection | Score candidates, hold top 3 | Selection function, free energy gate |
| 3. Audience Calibration | Tag awareness, demand state | None (classification) |
| 4. Production | Engines create content | None (creative) |
| 5. Quality Threshold | Anti-slop, brand, awareness checks | Rule-based |
| 6. Prediction | Estimate performance | Bass, K-factor, prospect theory |
| 7. Immediate Measurement | CTR, engagement, dwell | Engagement metrics |
| 8. Delayed Measurement | ROMI, attribution, A/B stats | Statistical + causal |
| 9. Learning | Update system | Bayesian update |

**The phase determines the formula.** The agent never asks "which formula?" —
it asks "what phase am I in?"

See `references/decision-sequence-detail.md` for the full sequence.

## Naming Convention

| Term | Lifecycle | Purpose |
|------|-----------|---------|
| **Consortium** | Ephemeral (forms per task, disbands on output) | Task-swarm of specialists |
| **Consilium** | Permanent (boot identity) | Operator brain-suite |

These are DIFFERENT things. Do not conflate.

## Biological Language Discipline

- Use "process flow" not "spine" — the spine is a real anatomical structure
- Use "output" not "birth" — not everything is birthed
- Verify isomorphisms BEFORE building artifacts
- See `body-part-tackle-workflow` skill for full anatomical language rules

## Memory Discipline

Project state belongs in files, git, and the operator bus — NOT in the the operator agent
2,200-char persistent memory buffer. The buffer holds ONLY: user identity,
communication style, standing rules, current priority. Everything else flows to
DS O'Keefe (hippocampus, T2 semantic store) or session search (T1 episodic).

User correction (2026-06-29): "you can't keep deleting memories like that...
it's a process flow, I don't know why that needs to go to memory."

## Pitfalls

- **Never use heuristics when MATH exists** — agent decisions need deterministic scoring
- **Never confuse 8D human wellness with system health** — the gate measures what content does TO THE HUMAN. User correction (2026-06-29): "Is it wellness for AI or is this wellness for humans? It's got to be healthy for the HUMAN."
- **ALL 8 dimensions protected, no hierarchy of harm** — not just 3 or 4. User expanded from 3 to 4 to ALL 8 across multiple corrections (2026-06-29/30). Any negative score on ANY dimension = automatic REJECT.
- **Positive mission language only** — User correction (2026-06-29): remove "not going to blow up the world." Use positive framing: "heal humanity across all 8 dimensions."
- **Never test before building completely** — build every layer, connect everything, THEN test. User correction (2026-06-29): "You haven't even built and connected the engines yet... you need to build it all the way."
- **Never put project state in persistent memory** — use files, git, bus, or O'Keefe. User correction (2026-06-29): "you can't keep deleting memories like that."
- **Never force the number of framework categories** — let research surface what it naturally finds. User correction (2026-06-29): "Why are there eight categories? Are you trying to fit only eight?"
- **Never use anatomical terms as metaphors** — "spine" means spine, "birth" means birth
- **Embedding rule: NEVER Anthropic** — any other provider fine (Gemini, OpenAI, NVIDIA NIM, local). User correction (2026-06-29): "The only thing I was getting at was to never use Anthropic."
- **Verify ALL claims against real state** — when ANY operator claims work is done, curl the port, check the registry, reproduce the test. User correction (2026-06-30): organism caught sibling-agent claiming fleet startups that never happened.
- **NPR config agents are NOT HTTP engines** — 29 NPR agents are config-based, not FastAPI servers. Health sweeps that ping their ports report false "down" states. User correction (2026-06-30): "I believe the 30+ down aren't even down… I think you're wrong again."
- **One exocrine gland with modes, not multiple organs per platform** — distribution to multiple platforms is ONE organ (the specialist engine) with ductal modes, not 5 separate engines. User correction (2026-06-29).

## First Instance: Marketing Consortium

The marketing consortium at `~/your-workspace/marketing-consortium/` is the
first built instance of this blueprint. It contains:

- 3-layer research (practitioner + academic + case studies): 458 lines
- 14-module curriculum: 536 lines
- Selection math + executable engine: 357 lines + 429 lines code
- 44 quantitative formulas across 3 tracks: 413 lines
- 9-phase decision sequence: 252 lines
- Pathology order system: 264 lines
- Engine /process endpoint contract: 162 lines
- Carriage controller: 522 lines code
- Git committed (23 files, 3572 lines)

Build status: hermes domain COMPLETE. Awaiting sibling-agent for /process endpoint
wiring + distribution organ builds.

## Related Skills

- `operations/marketing-metabolism-production` — the marketing organs themselves (what the consortium drives tasks THROUGH)
- `body-part-tackle-workflow` — how to build new body parts the consortium needs
- `organism-integrity-verification` — immune-system-style verification of organism claims
- `infrastructure/okeefe-memory-routing` — T2 memory routing + DS prefix rule + verification protocol

## References

- `references/selection-math-detail.md` — full selection math spec
- `references/decision-sequence-detail.md` — full 9-phase decision sequence
- `references/ds-till-stem-cell-reserve.md` — the specialist engine engine replacement system + twin organism architecture + sleep cycle design
