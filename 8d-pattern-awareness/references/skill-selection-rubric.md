# 8D Skill Selection Rubric

This reference helps the agent choose *what to build next* for the 8D skill family.

## Goal
Prefer skills that help the user see, understand, and safely act on one dimension at a time.

## Selection order
Build skills in this order:
1. Awareness
2. Snapshot / report
3. Safe next-step helper
4. Support / intervention
5. Bridge to premium intelligence
6. Ops / automation

## Good candidate signals
A candidate is stronger when it has:
- one primary 8D dimension
- a clear user problem
- a clear output shape
- repeatable use
- safe public exposure
- low setup friction
- room for a family of related skills
- a clean open-core boundary

## Scoring parameters
Score each candidate 0–5 on:
- utility
- dimension fit
- safety / boundary fit
- reusability
- self-containedness
- implementation fit
- measurement clarity
- moat preservation

## Dimension fit guidance
- **PSY**: emotional weather, stress load, regulation, calm
- **PHY**: sleep, recovery, hydration, food, energy, body strain
- **ENV**: friction, clutter, interruptions, setup quality
- **SOC**: support, conflict, loneliness, repair, connection
- **SPI**: meaning, values, purpose, alignment, direction
- **INT**: focus, reading, mental overload, analysis, clarity
- **VOC**: execution, initiation, momentum, follow-through, completion
- **FIN**: money pressure, resources, sustainability, budget strain

## Release rules
- Start with awareness before action.
- Keep the public skill small and readable.
- Do not ship a broad recommendation engine before the safer reporting layer exists.
- Move private calibration, hidden scoring, and premium logic out of the public skill.
- If the candidate is too broad, split it into a family and move the details into references.

## What to avoid
- omni-skills that try to cover all eight dimensions at once
- diagnosis-like language
- private heuristics exposed in the public layer
- one-session artifacts that do not generalize
- unclear outputs that are hard to review

## Use with the main skill
Use this rubric when deciding which 8D-related skills to release, refine, or keep in the watchlist.