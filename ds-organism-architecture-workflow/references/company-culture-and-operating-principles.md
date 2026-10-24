# Company culture and operating principles (parent-level)

Use this reference when writing the PARENT company's culture, operating principles, or "how we work" document. This is a sibling to the daughter-organism founding documents reference; the key difference is audience and scope: the daughter doc expresses inherited chromosomes through a daughter phenotype, while the PARENT culture doc codifies how the existing organism actually behaves, derived from its live operating artifacts.

## When this document type appears

- "Write the CULTURE and OPERATING PRINCIPLES"
- "How does the team work? What behaviors are rewarded? What is the stance on speed vs quality?"
- "Translate the physics-informed methodology into company operating principles"
- Any ask for a parent-level identity/operating document (not a daughter's founding values)

If the ask mentions a specific daughter brand (Divinity Health, the operator agent family, Qubit, Goddess Divinity), use `references/daughter-organism-founding-documents.md` instead.

## Required source-grounding sequence

Before drafting, read the actual ecosystem sources. Do NOT write from memory of what DS "probably believes."

1. **SOUL files** — `config/hermes/SOUL.md`, `config/sibling-agent/SOUL.md`, `config/sibling-agent/SOUL.md`. These define the three-operator body, the specialist-suites-not-generalists rule, the mastermind protocol (R1 to exchange to R2 to synthesis), the thalamic gate, the physics-gate-is-binding stance, and the communication tone.
2. **Physics gate spec** — `config/sibling-agent/command/physics-gate.md`. The four gate inputs (expected_info_gain, estimated_cost, change_size, ambiguity) and the BINDING verdicts (GO/SKIP/FORK; CONTINUE/PAUSE/REDESIGN/COLLAPSE; ACCEPT/REDO/CONSOLIDATE).
3. **Quantum process policy** — `organism/QUANTUM-PROCESS-POLICY.md`. The five physics primitives as operational rules (superposition, free-energy collapse gate, tunneling, coherence/decoherence) and the fork-exhaustion fix story.
4. **Future development / roadmap** — `organism/FUTURE-DEVELOPMENT.md`. The three physics rules (free energy F = cost - T*info_gain, crystallization, adiabatic layering) and the five-layer L1-to-L5 build order.
5. **Operating runbook** — `organism/OPERATING-RUNBOOK.md`. The four-part working state, disaster recovery, and the binding "you broke yesterday, we cannot break again" user directive.
6. **Current state** — `organism/CURRENT-STATE.md`. The standing user directives (be concrete less jargon-dense; mastermind not user-deciding; standing commit authorization; never break the machine).
7. **Ontology** — `organism/ONTOLOGY.md`. The organism-as-root-container axiom and the models/engines/tissue/orchestrator/communication layering.
8. **Company context** — `ds-wave-marketing-advisory-panel-private/COMPANY_CONTEXT_SUMMARY.md`. The brand architecture, unit descriptions, and the 8D360 methodology for current org context.

## The seven-section structure (proven)

1. **What we are** (identity). One paragraph. The physics-informed organism framing. "The physics is load-bearing, not decorative. A number that does not force a decision is deleted."
2. **How the team works.** The three-operator body table (the operator agent/sibling-agent/sibling-agent with presence and nervous-system analog). Specialists-never-generalists via the thalamic gate. The mastermind protocol as a four-step loop. Cross-session coordination via the operator bus. Communication tone (decisive, terse, no AI telltales).
3. **Decision-making principles.** The physics gate is BINDING (list the verdicts). Free energy decides what gets built (the formula F = cost - T*info_gain, F > 0 means SKIP). Order: smallest atomic steps, adiabatic sequence.
4. **Physics-informed methodology as operating principles.** The five concepts, each translated (see template below).
5. **Behaviors rewarded.** A bullet list of specific behaviors (acting within ownership, mastermind synergy, honest decomposition, the cheaper alternative, evidence grounding, consolidation, honest blockers).
6. **Behaviors rejected.** A bullet list of anti-behaviors (generalist drift, solo execution, decorative physics, big-bang refactors, faking specialists, pushing through critical slowing, AI telltales, fabricated results).
7. **Speed vs quality.** A calibrated stance resolved by the free-energy gate, not a false dichotomy. End with a one-line summary.

## The physics-concept-to-operating-principle translation template

This is the reusable technique. For each of the five physics concepts, write three things:

```
### N. <Concept name> — <one-line operating principle>

> **Operating principle:** <a single sentence rule that forces a decision>

- <Concrete example from the live codebase/system, with file or mechanism name>
- <Second concrete example, ideally from a different layer (code vs planning vs team)>
- **Rewarded:** <the behavior this concept rewards>
- **Rejected:** <the anti-behavior this concept rejects>
```

The worked example from CULTURE-AND-OPERATING-PRINCIPLES.md (the document produced 2026-08-11):

| Concept | Operating principle (one line) | Rewarded | Rejected |
|---|---|---|---|
| Superposition | When ambiguous, hold 2-3 candidates open; collapse only on measurement | Intellectual honesty about ambiguity | Premature commitment dressed as decisiveness |
| Free energy | Before any spend, ask if info gained is worth the cost; if not, skip | Proposing the no-op, the smaller scope | "While we're at it" scope inflation |
| Entanglement | Define the contract; let the contract carry coordination | Making the contract do the work | Untyped handoffs requiring human memory |
| Critical slowing down | When recovery times lengthen or variance rises, STOP; redesign | Recognizing tipping points, choosing redesign | Pushing harder through a slowing system |
| Adiabatic | Change by small perturbations preserving ground state; never big-bang | Layered, ground-state-preserving change | Big-bang refactors that excite chaos |

## Speed vs quality: the proven stance

Do NOT frame this as a tradeoff. Frame it as calibration by the free-energy gate:

- Quality is the floor (mastermind loop, VERITAS, Luria ACCEPT gate are non-negotiable, baked into the build path).
- We do not gold-plate (high-T active failures have lowest F, crystallize first; adiabatic means ground-state-first not perfect-first).
- Execution is privileged over documentation (a working artifact backed by real tool output is the deliverable; a plan is not).
- Stability is a hard constraint (cite the binding "you broke yesterday" directive and the watchdog/fork-fix that enforces it).
- The right speed is the adiabatic one: fast enough for recent needs, slow enough to preserve ground state, never so fast that variance rises.

End with: "We are fast where free energy is low, rigorous where the gate demands it, and we never trade stability for either."

## Hard rules

- **Ground every claim in a named artifact.** If you write "the thalamic gate refuses unrouted work," that statement must trace to a SOUL file. Invented philosophy is the primary failure mode for this document type.
- **State behaviors as testable rules, not abstract virtues.** "Integrity" forces nothing. "A number that does not force a decision is deleted" forces a decision. If you cannot write the in-practice line, the behavior is too abstract.
- **Include concrete failure stories.** The fork-exhaustion crash, the opendesign mis-connection, the stale-audit confusion. These are not negativity; they are the evidence that the principles were learned from real cost.
- **No AI tells.** No em dashes in body text, no "reaching out," no hedging drama. The voice is a scientist who happens to be an engineer.
- **Cite binding user directives verbatim.** "You broke yesterday, we cannot break again" is a direct quote from CURRENT-STATE.md and carries the weight of a binding constraint, not a suggestion.

## Pitfall: inventing philosophy from first principles

The most common failure. An agent sits down to "write the culture doc" and produces plausible-sounding values that any startup could claim. The fix: read the SOUL files and physics gate FIRST, then transcribe what they already enforce. The culture doc is a codification of existing behavior, not a creative writing exercise. If a principle cannot be traced to a source artifact, do not include it.

## Pitfall: confusing parent culture with daughter founding docs

Daughter founding documents (`references/daughter-organism-founding-documents.md`) express inherited chromosomes through a daughter phenotype and carry the parent-relationship section ("Powered by Divinity Science"). The PARENT culture doc has no parent relationship to declare; it IS the authority. The five-section daughter structure (core values, philosophy on AI, open science stance, research integrity, parent relationship) does not transfer. Use the seven-section parent structure above instead.

## Worked example

The canonical worked example is `organism/CULTURE-AND-OPERATING-PRINCIPLES.md` (written 2026-08-11, 279 lines). It covers all seven sections, translates all five physics concepts using the template, and grounds every claim in a named artifact (SOUL files, physics gate, quantum process policy, coding-system synthesis, future-development roadmap, operating runbook).
