# Adversarial Science Review — Rev J (2026-08-02)

Panel: pedantic neuroscientist, neuromorphic computing engineer, systems physiologist, multi-agent systems researcher, Popper falsification auditor.

Web search and delegation were both credit-blocked (xAI 403, Nous 402, llm-vendor 429). Review conducted from established domain knowledge.

## Grounding sources

- Mead, C. (1990). *Neuromorphic Electronic Systems*. Proc. IEEE.
- Standard neuroanatomy textbooks (Marieb, Tortora): neuron structure, myelination, saltatory conduction.
- Multi-agent frameworks: AutoGen, CrewAI, LangGraph documentation and architecture patterns.
- Physiomorphic AI: the principal Williams / Divinity Science field claim.

## Slide 1 corrections (6 findings)

| # | Was | Now | Why |
|---|---|---|---|
| 1 | "inspired by the nerve cell" | "inspired by neurons and synapses" | Neuromorphic emulates neural networks and synaptic physics, not one cell type |
| 2 | (no disclaimer) | "Placement on the body is illustrative, not anatomical" | Prevents false biological correspondence claim from hostile reviewer |
| 3 | "neural-scale computing" caption | KEPT | Correct: refers to neural substrate level, not one neuron. Does not imply single-neuron systems |

### Neuron anatomy verification (all PASS)

| Label | Points to | Correct |
|---|---|---|
| dendrites | branching input tree | YES |
| soma | cell body (contains nucleus, integrates signals) | YES |
| axon | long output process (transmits action potentials) | YES |
| myelin sheath | insulating internodal segments (Schwann PNS / oligodendrocytes CNS) | YES |
| node of Ranvier | unmyelinated gaps between internodes (Na+ channels, saltatory conduction) | YES |

### Scale comparison nuance

Neuromorphic systems use NETWORKS of spiking neurons (Loihi: 128 cores, thousands of neurons each; TrueNorth: 4096 cores, 1M neurons). Showing one neuron on the left is a pedagogical simplification for scale comparison, not a claim that neuromorphic = single neuron. The "neural-scale" caption communicates the substrate level, not a count.

### Body tech-analog mapping audit

The six labels (SPECIALISTS, COORDINATION, REGULATION, RECOVERY, DEFENSE, TIMING) mapped to body regions are **metaphorical architecture analogs, not anatomical correspondences.** A neuroscientist could challenge why REGULATION sits on the mid-torso (maps to nothing specific anatomically). The "illustrative, not anatomical" disclaimer resolves this.

## Slide 2 corrections (5 findings)

| # | Was | Now | Why |
|---|---|---|---|
| 1 | "few system-level diagnostics" | "diagnostics typically focused on output quality, not whole-system health" | Some model-centric systems have telemetry; gap is system-level scope, not zero |
| 2 | "fragile when load concentrates" | "single dependency: if core degrades, path degrades" | Models handle throughput fine; weakness is single-point dependency, not raw capacity |
| 3 | "regulation often local, not whole-system" | "coordination exists but is not a first-class regulatory subsystem" | Fairer: acknowledges coordination exists, just not as organism-level architecture |
| 4 | "sense drift, repair the path to output" | "designed to detect drift and adjust the path to output" | "Repair" implies demonstrated self-healing; "designed to" claims architectural intent |
| 5 | "whole-system diagnostics" | "diagnostics as a system-level role monitoring coordination and regulation across modules" | Defines what it means instead of undefined marketing language |

## Multi-agent fairness audit

| Framework | Has regulation? | Has diagnostics? | Slide fair? |
|---|---|---|---|
| AutoGen | Role-level conversation management | Basic logging | Yes: no system-level regulation layer |
| CrewAI | Task delegation, role hierarchy | Task status tracking | Yes: no organism-level diagnostics |
| LangGraph | Graph-based flow, checkpointing | State persistence | Closest to Physiomorphic but still lacks regulation/recovery/defense as first-class architectural subsystems |

The slide 2 comparison is fair as long as column 2 says "COMMON MULTI-AGENT" and does not claim ALL multi-agent systems lack these capabilities. LangGraph with full orchestration is the gray area.

## Overclaim risk register

| Risk | Severity | Mitigation |
|---|---|---|
| "repair" implies self-healing capability | HIGH | Changed to "designed to detect drift and adjust" |
| "nerve cell" singular misrepresents neuromorphic field | HIGH | Changed to "neurons and synapses" |
| "fragile" implies models fail under load | MEDIUM | Changed to "single dependency" framing |
| "whole-system diagnostics" undefined | MEDIUM | Defined as system-level monitoring role |
| Body placement implies anatomical correspondence | LOW-MEDIUM | Added illustrative disclaimer |

## Final gate

**SHIP WITH FIXES APPLIED.** All 6 fixes are text corrections in prompts. No structural changes needed.
