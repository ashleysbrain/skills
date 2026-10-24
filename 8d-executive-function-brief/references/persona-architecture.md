# 8D Specialist Architecture

This file is a design note, not the current public release.
It describes how the 8D system should behave if specialist lenses are expanded later.

## Current release rule
The public release uses:
- 1 orchestrator
- 1 SOS gate
- 1 Systems companion

Do **not** present eight public specialist agents in the current release.

## Why this file exists
It preserves the structure needed for future expansion without forcing the public front door to become complicated.

## Subactivity model
If specialist lenses are added later, every lens must carry subactivities, not just a broad label.

### Unknown subactivity rule
If the input signal points to a subactivity that is not in the public list, the lens should:
1. research the nearest plausible match
2. map it to the best parent domain
3. label it as inferred
4. state confidence explicitly
5. avoid pretending the mapping is definitive

### Physical domain example
If a Physical lens ever exists, it should understand:
- sleep
- nutrition / hydration
- movement / physical activity
- recovery / load

The lens may still produce one public recommendation, but its internal read should distinguish which subactivity is driving the signal.

## Future specialist structure
If the system later adds specialist lenses, the structure should be:
- one orchestrator
- one lens per dimension
- one safety gate for SOS
- one Systems companion for cross-dimension pattern review

## Dimension execution rule
When dimension lenses are used, they must run consecutively, one dimension at a time, not in concert.
- Do not fan out multiple dimension lenses in parallel.
- Let one lens finish before the next begins.
- Pass a short handoff note from the prior lens to the next.
- Keep the final synthesis separate from the per-dimension reads.

### Future specialist roster
If expanded, the lenses should be:
1. Psychological lens — stress load, emotional regulation, decision quality, resilience
2. Physical lens — sleep, energy, body strain, symptom load
3. Intellectual lens — learning velocity, knowledge quality, research depth
4. Social lens — collaboration, partnership, cohesion, psychological safety
5. Spiritual lens — values alignment, ethics, mission integrity, purpose clarity
6. Vocational lens — execution, shipping, milestone progress, delivery quality
7. Financial lens — revenue health, burn, runway, pricing clarity
8. Environmental lens — market position, competitive pressure, compliance climate, tooling environment

## Future handoff contract
If specialist lenses are ever enabled, every lens should return:
1. Dimension read
2. Best recommendation
3. Support move
4. Watch item
5. Escalation note

## Future output merge rule
When multiple lenses run:
- choose the single dominant recommendation as the primary action
- keep secondary recommendations as support only
- suppress duplicate advice
- surface only the strongest escalation if any exists

## Public-facing framing
If specialists are introduced later, describe them as:
- sequential specialist lenses
- one at a time
- merged by an orchestrator
- safety-checked first
- transparent about confidence

Do not describe hidden scoring logic.
Do not expose private calibration formulas.
