# Adversarial Science Review — Rev M (2026-08-03)

Panel: multi-agent systems researcher, distributed systems architect, AI/ML systems engineer, scientific methodologist (the specialist engine), Physiomorphic skeptic.

**Method:** Orchestrator subagent read ACTUAL SOURCE CODE (not summaries):
- `physics_gate.py` (608 lines, real Python with real math)
- `sherman_router.py` (1051 lines, real CLI with real exit codes 0/2/3)
- `operator_bus.py` (394 lines, real SQLite message queue)
- `the operator agent/organism/config/sibling-agent/BOOT.md` + `AGENTS.md`
- `veritas_engine.py` usage (gate imported and called)

Result: 8 PASS, 8 REVISE, 0 FAIL across 16 claims. Architecture is real. Fixes are precision/honesty, not capability fabrication.

## Claim Table

### Model-Centric Column

| # | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|
| 1 | "single output path: one model's answer, produced in isolation" | PASS | By definition a single LLM call produces one output. "Produced in isolation" is fair. | None. |
| 2 | "general-purpose but ungoverned" | REVISE | Production LLMs have output validators, guardrails (Llama Guard, OpenAI moderation), constitutional AI, RLHF, structured-output schemas. "Ungoverned" is a strawman. The distinction is WHERE governance lives (model-level vs protocol-level). | "general-purpose. governance lives in the model, not in the process." |
| 3 | "single dependency: if the core degrades, the whole path degrades" | PASS | Architecturally true. Single point of failure, N=1 replicas. | None. |

### Common Multi-Agent Column

| # | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|
| 4 | "agents share context via state-passing, not via mutual re-evaluation" | REVISE | LangGraph supports `add_conditional_edges` (agent B CAN re-evaluate agent A). AutoGen GroupChat supports conversable agents that critique. "Not via mutual re-evaluation" is false as universal. What IS fair: in most common usage patterns, agents pass state forward without mandatory bidirectional re-evaluation. | "agents CAN share context bidirectionally, but mutual re-evaluation is optional, not a mandatory protocol step" |
| 5 | "no mandatory synthesis step" | REVISE | LangGraph reducers/Channel combiners CAN be structurally required. "No mandatory synthesis" is false for well-architected LangGraph. What's true: no universal mandatory synthesis across all frameworks; most make it optional by default. | "no mandatory synthesis step by default, most frameworks make it optional" |
| 6 | "assembled result from separate agent outputs" | PASS | Fair. Sequential pipelines assemble from individual contributions. | None. |
| 7 | "coordination through task routing, not organism-scale regulation" | REVISE | "Organism-scale regulation" is undefined jargon to the audience at slide 2. Replace with concrete mechanisms. | "coordination without mandatory protocol, background health monitoring, or physics-gated execution" |

### Physiomorphic Column

| # | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|
| 8 | DIGEST stage | PASS | Verified against BOOT.md. Reads sibling work + operator bus before editing. Real SQLite infrastructure. Meaningfully different from generic context loading: mandates reading sibling specifically. | None. |
| 9 | "mandatory mastermind exchange" | REVISE | Two enforcement layers exist: (1) sherman_router.py --gate produces real exit codes (0=GO, 2=REFUSED, 3=HANDOFF). (2) BOOT.md/AGENTS.md declare it binding. BUT both are prompt-level + convention-level, NOT runtime-invariant-level. An LLM operator CAN skip exchange silently. This is fundamentally different from Paxos (protocol cannot complete without quorum). "Mandatory" in Paxos = mechanical enforcement. "Mandatory" here = prompt says so + audit trail. | "binding by protocol, operators flagged for skipping it" |
| 10 | ORDER: "drop steps where cost exceeds information gain" | REVISE | Verified: `physics_gate.py:166-168` has `free_energy = cost - T * info_gain; F > 0 -> SKIP`. Formula IS real Python. BUT inputs (`expected_info_gain`, `estimated_cost`, `change_size`) are caller-provided [0,1] estimates, NOT measured from system. Temperature T defaults to 0.5, described as "deadline pressure scalar" — NOT thermodynamic temperature. Formula is structurally isomorphic to Helmholtz free energy (F = E - TS) but operates on normalized estimates. | Add: "(F = cost - T x info_gain, caller-estimated inputs)" |
| 11 | EXECUTE: "one specialist at a time, routed by thalamic gate" | PASS with caveat | Verified: sherman_router.py maps task keywords to 27+ engine directories, queries methodology.py, returns personality + model + sub-agents. Exit code 2 if no specialist matches. Real mechanical routing. "Thalamic gate" is metaphor for this CLI. | Add footnote: "Thalamic gate = specialist router (the specialist engine). Routes each task to one engine specialist; refuses unrouted generalist work." |
| 12 | Three physics gates (PRE/IN/POST-FLIGHT) | REVISE (most important finding) | Split verdict by gate: PRE-FLIGHT: real formula, caller-estimated inputs. IN-FLIGHT: **strongest gate** — takes `recovery_times: List[float]` (actual measured durations), computes real linear regression slope + variance ratio + lag-1 autocorrelation. Real statistics on real data. POST-FLIGHT: real delta computation, but pre/post uncertainty are caller-estimated [0,1]. Slide presents all three as equivalent in rigor. They are not. | Add note: "Physics gates combine measured signals (in-flight: recovery-time statistics from real operation durations) with estimated signals (pre/post-flight: caller-reported [0,1] scalars). The verdicts are binding; the inputs are a mix of measured and operator-estimated." |
| 13 | CONSOLIDATE: "one output neither operator could produce alone" | REVISE | Unfalsifiable as stated. Requires ablation (run A solo, B solo, A+B exchange, compare). No ablation study exists in codebase. Design thesis, not proven result. | "designed to exceed what either operator produces alone (ablation validation pending)" |
| 14 | Is SOLVE fundamentally different from CI/CD or LangGraph? | REVISE (verdict on novelty) | Skeptic + distributed systems conclude: SOLVE is structurally isomorphic to a LangGraph StateGraph with 5 sequential nodes + conditional edges + shared State. What LangGraph does NOT have by default: (1) specific physics formulas, (2) operator bus as real message queue between two persistent operators, (3) autonomic background monitoring. Pipeline SHAPE is not novel. Specific mechanisms are. | Do not claim protocol SHAPE is novel. Claim specific mechanisms: "SOLVE is a 5-stage protocol (structurally similar to any sequenced pipeline). What's different: each stage carries specific physics-derived decision functions and the mastermind exchange enforces bidirectional operator re-evaluation." |

### Comparison / Banner

| # | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|
| 15 | "mandatory protocol with physics gates at every step" | REVISE | Three problems: (1) "Mandatory" implies runtime enforcement; actual is prompt + exit-code level. (2) "At every step" is imprecise — gates are available but called explicitly, not auto-wrapping. BOOT.md says "degradation-graceful" if gate fails to import. (3) Inputs are mix of measured and estimated. | "binding protocol with physics-derived decision gates at each stage" |
| 16 | Would a distributed systems architect say "genuinely novel" or "just a distributed transaction with extra steps"? | Narrowly novel, not revolutionary | SOLVE is a well-structured workflow with domain-specific decision functions. NOT a new distributed protocol (like Paxos/Raft). IS more structured than naive agent stitching. Genuinely distinguishing primitives: (1) in-flight critical-slowing-down detector (real statistics on measured recovery times), (2) mastermind exchange as mandatory bidirectional re-evaluation, (3) autonomic background layer. | Do not claim novelty beyond what's earned. Accurate: "A structured execution protocol with two mechanisms absent from common multi-agent frameworks: a measured critical-slowing-down detector and a mandatory bidirectional mastermind exchange." |

## Physics Gate Reality Check

| Gate | Real code? | Inputs measured or estimated? | Strength |
|---|---|---|---|
| PRE-FLIGHT | Yes, real Python | Caller-estimated [0,1] scalars | Real computation, subjective inputs |
| IN-FLIGHT | Yes, real Python | **Measured** recovery_times: List[float] | **Strongest.** Linear regression + variance ratio + autocorrelation on real data |
| POST-FLIGHT | Yes, real Python | Caller-estimated uncertainty [0,1] | Real computation, subjective inputs |

Temperature T: default 0.5, described as "deadline pressure scalar." In `_compute_free_energy` intake mode it is hardcoded 1.0. NOT thermodynamic temperature. Hyperparameter.

## Skeptic's LangGraph Counterexample

The skeptic built:
```
LangGraph StateGraph:
  - Node "digest": reads shared State, checks sibling's last output key
  - Node "exchange": conditional edge — if sibling has R1, read before producing R2
  - Node "order": applies cost-benefit filter
  - Node "execute": conditional routing to specialist subgraphs
  - Node "consolidate": reducer merges both operators' outputs
```

Skeptic's claim: "This does everything Physiomorphic does."

Panel's verdict: capability set IS reproducible. What it does NOT reproduce:
1. In-flight critical-slowing-down gate on measured recovery times (~30 lines of Python, reproducible)
2. Mandatory R1->R2 exchange (LangGraph can implement but doesn't require; reproducible as convention)
3. Autonomic background layer (reproducible as sidecar)

The real distinction: Physiomorphic's contribution is NOT a new capability. It is a **specific, opinionated protocol that mandates practices** that multi-agent frameworks *allow but do not require*. The contribution is protocol design + enforcement posture, not a structurally absent primitive.

Skeptic's final position: "I can build all of this in LangGraph in a weekend. But I wouldn't have thought to mandate the R1/R2 exchange or implement a critical-slowing detector. The protocol design has value as opinionated architecture. It does not have value as a novel primitive. Label it correctly."

## 8 Required Fixes (all precision/honesty, zero capability fabrication)

1. "ungoverned" -> "governance lives in the model, not in the process"
2. "not via mutual re-evaluation" -> "mutual re-evaluation is optional, not a mandatory protocol step"
3. "no mandatory synthesis step" -> "no mandatory synthesis step by default"
4. "organism-scale regulation" -> concrete mechanisms (no mandatory protocol, no background monitoring, no physics-gated execution)
5. "mandatory mastermind exchange" -> "binding by protocol, operators flagged for skipping it"
6. Add "(F = cost - T x info_gain, caller-estimated inputs)" to free-energy claim
7. "one output neither operator could produce alone" -> "designed to exceed what either operator produces alone (ablation validation pending)"
8. "mandatory protocol with physics gates at every step" -> "binding protocol with physics-derived decision gates at each stage"

## What Must NOT Be Claimed

- Runtime-level enforcement (it's prompt-level + exit-code-level)
- Physics gates use measured physical quantities (in-flight does; pre/post-flight use caller estimates)
- "Neither operator could produce alone" as proven (it's a design thesis)
- Pipeline shape is novel (specific mechanisms are; the shape isn't)

## Gate: SHIP WITH FIXES

Architecture is real. Fixes are precision and honesty. After applying 8 text replacements, the slide is defensible against any expert who reads the source code.
