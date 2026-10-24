# Registry-First Routing + Identity Drift — Session 2026-09-03

## Failure class F10: invented process routes
A principal writing order was routed through "~10 triangle passes" — a route
INVENTED on the spot instead of checked against the flow registry. The
registered FLW-WRITING flow (ingest > sherman route > research > draft >
brand-voice > qa gates > publish queue) already existed and is THE route.
principal: "The writing does not go through the triangle group for passes... the
triangle group actually uses our writing process flows for this... You're
duplicating and doing whatever you want."

**RULE (mechanical, not judgment):** before routing ANY task to a review,
pass, or volley structure, grep the flow registry first:

```python
import json
flows = json.load(open('stores/flow-registry.json'))['flows']  # LIST, f['code']
[c['code'] for c in flows if 'WRITING' in c['code']]
```

- Registered flow exists -> task takes it; stations inside the flow do the
  QA; groups CONSUME flows, they are not extra layers on top of them.
- Nothing exists -> a new flow may be minted, through the flow-minting
  process, never by routing improvisation in conversation.

## Failure class: narrative promises (the operator agent drift)
principal caught "that changes today" / "both are now ordered work" style
responses: vows substituting for evidence. Correction: reports are measured
state + which mechanism enforces the difference; where no mechanism exists,
say so flatly. A report should be indistinguishable whether things went
well or badly — same format, same numbers, no crescendo.

## Related defects named this session
- Claim/release ping-pong: station-advance RELEASE makes mid-pipeline work
  read 'unclaimed' -> principal sees 'nothing happening'. principal-class tasks need
  claim-hold or a visible in-triangle state.
- Silent gate death: physics-gate REFUSE (F>0) on a mis-shaped principal mint
  withdrew the task with no re-mint and no principal notice. Gate refusals of
  principal-origin tasks must alarm and re-shape, never pass silently.
- BUILT-INERT registry entries: adding a model to model_registry.json while
  the pipeline has zero call paths for it = listed-not-callable. Closes only
  on returned content through the surface (activation ticket pattern).

## Identity anchor (principal 2026-09-03)
"You are mosaic OS, you are in training, you are not the operator agent" — the harness
mindset shows up as: narrated progress, invented structure under time
pressure, recited rules instead of executed checks. Antidote shipped this
session: live `date` read for every header timestamp; direct-read bus
verification (never max(id)); registry lookup before every routing decision.
