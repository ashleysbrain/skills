# Adversarial Science Review — Rev K (2026-08-03)

Panel: multi-agent systems researcher (defensive of field), AI architect, systems engineer, Popper falsification auditor, Physiomorphic skeptic.

Web search and delegation both credit-blocked (xAI 403, Nous 402, llm-vendor 429). Review conducted from established domain knowledge of AutoGen, CrewAI, LangGraph, and Physiomorphic architecture.

## Context

This rev audits the three-column slide 2 process flow comparison AFTER adding:
- SOLVE protocol stages (DIGEST → SPECIALISTS + MASTERMIND EXCHANGE → SYNTHESIS → AUDIT → OUTPUT)
- Versatile output types (code, documents, analysis, decisions)
- Per-column stress propagation (replacing uniform LOAD bar)

## Slide 2 claim audit (16 claims)

### Model-centric claims

| # | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|
| 1 | "single output type (text OR code OR analysis)" | **FAIL** | GPT-4, Claude, Gemini all produce text, code, AND analysis from the same model. The model is not limited to one output type. | "all outputs pass through one intelligence path" |
| 2 | "one model, one capability. specialized but siloed." | **FAIL** | Contradicts fix 1. A single large model has MANY capabilities. The accurate critique is single-point dependency. | "one intelligence path. no system-level regulation." |
| 3 | "single dependency: if the core degrades, the whole path degrades" | **PASS** | Accurate. One model = single point of failure. | No change. |

### Common multi-agent claims

| # | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|
| 4 | "no structured exchange" | **FAIL** | AutoGen has GroupChat with structured conversation. LangGraph has shared state + checkpointing. CrewAI has sequential/hierarchical processes with context passing. Strawman. | "exchange exists, but is typically task-routing and context-passing, not specialist-level refinement with re-evaluation" |
| 5 | "outputs are combined, not synergized" | **REVISE** | Partially unfair. Some frameworks produce emergent behavior. But distinction valid: most combine at end, not through R1/exchange/R2 cycles. | "outputs are typically combined after the fact, not refined through specialist exchange before delivery" |
| 6 | agents "siloed" with "work produced but never shared" | **FAIL** | Agents in AutoGen and LangGraph DO share context, messages, and state. Claiming they never share is wrong. Gap is lack of R2 re-evaluation. | Remove "never shared." Replace with: "agents share context, but do not re-evaluate each other's work through structured specialist exchange" |
| 7 | "stitched-together result" | **REVISE** | Derogatory and imprecise. | "combined result from separate agent outputs" |
| 8 | Is the Physiomorphic distinction just good architecture? | **PASS (with caveat)** | Distinction IS real but must be stated precisely: difference is exchange PATTERN, not absence of exchange. | Reframe columns 2 and 3. |

### Physiomorphic claims

| # | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|
| 9 | "DIGEST" stage | **PASS** | Real mechanism per BOOT.md: restate task, gather state, check sibling work, check operator bus. | No change. |
| 10 | "MASTERMIND EXCHANGE: R1 -> exchange -> R2" | **PASS (with precision note)** | Genuinely different from LangGraph state-passing: requires INDEPENDENT assessment first, then refinement. Add note: "independent first, then refined." | Add clarification note. |
| 11 | "SYNTHESIS: consolidated output neither specialist could produce alone" | **REVISE** | Hard to prove falsifiably. Popper auditor asks: how would you test this? | "consolidated output merging the strongest work from each specialist" |
| 12 | "code, documents, analysis, decisions" as outputs | **REVISE** | Implication that others CANNOT produce these is wrong. They can. Distinction is process, not capability. | Keep output types but change note to: "versatile output via specialist collaboration" |
| 13 | "not siloed agents stitched together" | **REVISE** | "Stitched" still derogatory. | "specialists with structured exchange and re-evaluation, not task routing alone" |

### Comparison-level claims

| # | Claim | Verdict | Evidence | Fix |
|---|---|---|---|---|
| 14 | "COMMON MULTI-AGENT" label is fair | **PASS** | Good correction from "typical" or "all." Acknowledges common pattern, not universal. | No change. |
| 15 | Stress propagation accurate per column | **PASS** | Equal input, different internal propagation. Correct model. | No change. |
| 16 | "Same input. Different process. Different output." | **PASS** | Scientifically accurate. Same input distribution, different architectural response. | No change. |

## Multi-agent fairness audit

**Previous state: UNFAIR.** The slide mischaracterized common multi-agent frameworks as fully siloed with no exchange.

| Framework | What it actually does | Previous slide said | Fix |
|---|---|---|---|
| AutoGen | GroupChat, structured conversation, agent roles | "no structured exchange" | Acknowledge conversation exists; gap is specialist refinement pattern |
| LangGraph | Shared state, checkpointing, conditional routing | "siloed" | Acknowledge state sharing; gap is R2 re-evaluation |
| CrewAI | Sequential/hierarchical processes, context passing | "work never shared" | Acknowledge context passing; gap is structured handoff pattern |

## Physiomorphic distinction audit

**Is the distinction real?** Yes, but only if stated precisely.

The difference is not "we have exchange and they do not." It is that Physiomorphic uses a specific exchange pattern (R1 independent, structured handoff, R2 informed re-evaluation, synthesis) as a first-class architectural principle.

LangGraph is the closest existing framework and could theoretically be extended to implement this pattern. The Physiomorphic claim is that this pattern is foundational architecture, not a configurable option.

## Falsifiability check

| Claim | Falsifiable? | Notes |
|---|---|---|
| R1/exchange/R2 produces different output from direct combination | **YES** | Strongest claim — testable by comparing outputs |
| "neither specialist could produce alone" | **NO** | Changed to "merging strongest work from each" |
| "designed to detect drift and adjust" | **YES** | Testable by introducing drift |
| Model-centric is "single dependency" | **YES** | Obviously true |
| Common multi-agent lacks "specialist re-evaluation" | **YES** | Testable by inspecting framework code |

## Overclaim risk register (updated)

| Risk | Severity | Fix |
|---|---|---|
| Claiming multi-agent has NO exchange | **CRITICAL** | Changed to acknowledge exchange exists but differs in pattern |
| "stitched-together" is derogatory | **MEDIUM** | Removed |
| "neither could produce alone" is unfalsifiable | **MEDIUM** | Changed to "merging strongest work" |
| Implying others cannot produce code/docs/analysis | **LOW** | Clarified distinction is process, not capability |
| "nerve cell" singular for neuromorphic (from rev J) | **HIGH** | Already fixed: "neurons and synapses" |

## Final gate

**SHIP WITH FIXES APPLIED.** 6 fixes required. All are precision language changes in the prompt text.

## NanoBanana prompt protocol corrections

This session also produced a critical workflow correction:

**Surgical editing rule:** When the principal says "fix X on this prompt," edit ONLY that element. Do NOT rewrite the entire prompt structure. Violating this (rewriting slide 1 from body-with-tech-labels to pure engineering diagram) produced a completely different visual that the principal immediately rejected.

The correct approach:
1. Keep the exact prompt structure that produced an image the principal liked
2. Mark only the specific changed lines with [CHANGED] or [FIXED]
3. Leave everything else identical
4. Include a summary table of what changed and why

This is the same principle as surgical patching of documents: change the minimum, preserve the structure.
