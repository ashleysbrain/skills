---
name: flow-stack-routing
description: "Use when classifying user input into stacked process flows."
---

# Flow-Stack Routing (input-gate orchestrator)

Class-level skill for classifying any user input at intake and emitting an
ORDERED STACK of process flows for the conduction layer to dispatch. The
intake surface (Telegram, desktop, CLI) becomes the orchestrator at the
moment of input; this skill governs the deterministic decision core
(`organism/flow_stack_router.py`) and any edit to it.

## Procedure
1. **Census existing intake machinery before adding a router** — grep the
   organism tree for existing intake/triage/route modules and BUILD ON them
   (extend the routing table, add the stacking layer) rather than placing a
   parallel classifier beside them.
2. **Classify intent, then emit the stack.** Classes and their canonical
   stacks:
   - science referral (any link from the principal) → research ingest → resonance
     check → studio draft → claim-check gate → AI-tells gate → paste-ready out
   - one-off question → wave coaching engine → direct answer out
   - research question → research flow → wave synthesis → direct out
   - build order → ledger mint (owner organism named) → conduction dispatch
     → receipt out
   - writing request → studio chain → claim-check → AI-tells → paste-ready out
   - status query → telemetry measured-read → direct out
   - unrouted → hand to the intake triage organ, surface default
3. **Hold superposition on ambiguity**: keep up to two secondary candidate
   stacks within one signal of the primary; collapse only on the cheaper
   probe. Never guess-and-commit on a borderline input.
4. **Run the selftest after every rule edit** — the router ships with a
   selftest of real historical inputs; a rule reordered for one new case can
   break a previously passing case.

## Rules and pitfalls
- **Order regex rules by intent specificity; the bare question mark is the
  LAST and most constrained rule.** Build orders arrive phrased as questions
  ("can we do it where...") and end in `?`; a loose `\?$` rule placed above
  the build-order rule steals them. Constrain the weak rule
  (`^(what|why|how|...)\b[^.]{0,80}\?$` — short, no build verbs).
- **A link from the principal is a referral and a GO ORDER** — never a curiosity to
   park; classify it to the referral stack immediately.
- **The router decides, the dispatcher executes** — never let the classifier
   itself run flows; it emits the stack, conduction dispatches it.
- **Deterministic patterns only** in the classifier; a semantic layer may
  override, never invent, classes.
- **Output is gated symmetrically** — every stack ends in a gate + out stage
  (claim-check, AI-tells scan); no stack ends at a raw draft.
