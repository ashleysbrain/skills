# Adversarial Science Review — Rev N (2026-08-03)

## Second-pass orchestrator review (source-code verified)

Panel: multi-agent systems researcher, distributed systems architect, AI/ML systems engineer, scientific methodologist (the specialist engine), Physiomorphic skeptic.

Ground truth verified by reading actual source files:
- `physics_gate.py` — 608 lines, real Python
- `sherman_router.py` — 1051 lines, real CLI with exit codes
- `operator_bus.py` — 394 lines, real SQLite queue
- `BOOT.md` + `AGENTS.md` — binding protocol docs
- `veritas_engine.py` — gate is imported and called

## Purpose

First-pass (rev M) found 8 issues and fixed them. This second pass verified the fixes hold and found what the first pass missed.

## Fix audit

| # | First-pass fix | Second-pass verdict |
|---|---|---|
| 1 | "ungoverned" -> "governance lives in the model, not in the process" | HOLDS |
| 2 | "not via mutual re-evaluation" -> "mutual re-evaluation is optional" | HOLDS |
| 3 | "no mandatory synthesis step" -> "by default" | HOLDS |
| 4 | "organism-scale regulation" -> concrete mechanisms | HOLDS |
| 5 | "mandatory" -> "binding" | BROKEN: "binding" still implies runtime enforcement |
| 6 | "cost exceeds information gain" -> "estimated cost exceeds expected information gain" | HOLDS |
| 7 | "neither could produce alone" -> "designed to exceed... ablation pending" | HOLDS |
| 8 | "at every step" -> "at each stage" | BROKEN: gates only exist in ORDER + EXECUTE |

Score: 6 clean holds, 1 residual issue, 1 broken fix.

## New issues found (first pass missed these)

### N1 CRITICAL: "at each stage" is FALSE

The note said "physics-derived decision gates at each stage." Ground truth: the three physics gates (PRE/FLIGHT/IN/FLIGHT/POST/FLIGHT) exist in EXECUTE only. The free-energy filter is in ORDER. DIGEST, EXCHANGE, and CONSOLIDATE have NO physics-derived decision gates.

The visual was honest (gates shown only under EXECUTE). The NOTE contradicted the visual.

**Fix:** "protocol-mandated SOLVE with physics-derived decision gates in ORDER (free-energy filter) and EXECUTE (pre/in/post-flight gates)"

### N2 CRITICAL: Caption contradicted fix 5

Caption still said "mandatory operator exchange" after fix 5 changed "mandatory" to "binding."

**Fix:** "protocol-mandated operator exchange"

### N3 HIGH: "Binding" implies runtime enforcement

"Binding" in Paxos means quorum enforcement: you cannot commit without it. Here, "binding" means system prompt + exit code + audit trail. An LLM operator CAN skip EXCHANGE at runtime; it is detectable after the fact, not prevented.

**Fix:** Replace "binding" with "protocol-mandated" everywhere (3 locations).

### N4 MEDIUM: "Flagged for skipping it" unclear

Exit code 2 flags generalist drift, not explicitly "skipped EXCHANGE." An operator could skip exchange, produce specialist output, and exit 0 undetected.

**Fix:** "skipping is a protocol violation (exit-code audited)"

### N5 MEDIUM: "Naive agent stitching" is a value judgment

LangGraph with custom validators is not "naive." Frameworks are general-purpose, not naive.

**Fix:** "default agent coordination"

### N6 LOW: "No mandatory protocol" slightly unfair

LangGraph's graph structure IS a protocol once defined. The distinction is no shipped opinionated protocol by default.

**Fix:** "without a shipped opinionated protocol"

### N7 LOW: "Physics-derived" implies measurement at all gates

Only IN-FLIGHT uses measured values. PRE/POST-FLIGHT use caller-estimated scalars.

**Fix (optional):** "PRE/POST-FLIGHT use estimated scalars; IN-FLIGHT uses measured recovery times"

## Skeptic's harder counterexample

Built a full LangGraph StateGraph reproducing every SOLVE stage. Every stage is reproducible with nodes, edges, conditional routing, and Python functions. No primitive is structurally impossible.

**Skeptic concession:** "I can build all of this in LangGraph in a weekend. But I wouldn't have thought to mandate the R1/R2 exchange or implement a critical-slowing detector. The protocol design has value as opinionated architecture. It does not have value as a novel primitive. Label it correctly."

## Physics gate reality check

| Gate | Real code? | Inputs | Strength |
|---|---|---|---|
| PRE-FLIGHT | Yes | Caller-estimated [0,1] scalars | Real computation, subjective inputs |
| IN-FLIGHT | Yes | MEASURED recovery_times: List[float] | Strongest gate. Real statistics on real data. |
| POST-FLIGHT | Yes | Caller-estimated uncertainty [0,1] | Real computation, subjective inputs |

Temperature T: default 0.5, "deadline pressure scalar." NOT thermodynamic.

## Corrected word usage (binding table)

| Word | Do NOT use | Use instead | Why |
|---|---|---|---|
| mandatory | implies runtime enforcement | protocol-mandated | Enforcement is prompt-level + exit-code, not runtime-invariant |
| binding | implies quorum-level enforcement | protocol-mandated | Same reason |
| siloed (for common multi-agent) | false strawman | agents share context via state-passing | AutoGen/LangGraph/CrewAI all share state |
| no exchange | false strawman | mutual re-evaluation is optional, not mandatory | Frameworks CAN do it; they don't require it |
| naive agent stitching | value judgment | default agent coordination | Frameworks are general-purpose, not naive |
| at each stage | false | in ORDER and EXECUTE | Gates only exist in 2 of 5 stages |

## Final gate: SHIP WITH FIXES

4 required fixes (A-D), 2 recommended (E-F). After application, the slide is honest, fair, and shippable.
