# 8D Skill Selection Rubric

## Purpose
This reference tells the update engine what to look for when selecting skills for the eight dimensions. The goal is not to scatter random skills across the platform. The goal is to build a coherent ladder of skills that starts with awareness, then adds structure, then adds action support, and finally becomes a durable public/open-core skill family.

## Selection philosophy
When choosing a skill to build or release, prefer skills that are:
- immediately useful to a real user
- easy to understand without hidden backstory
- safe to expose publicly
- reusable across days, users, or sessions
- clearly tied to one primary dimension
- measurable or at least observable
- small enough to ship cleanly
- extensible into a family of related skills
- compatible with an open-core boundary

Avoid skills that are:
- too broad to explain in one paragraph
- mostly private calibration logic
- mostly internal infrastructure with no public value
- dependent on one specific user session
- hard to test or hard to review
- likely to leak proprietary heuristics
- trying to solve all eight dimensions at once

## 8D release ladder
Build skills in this order when possible:
1. **Awareness** — help the user see what is happening.
2. **Snapshot / report** — show what changed and what seems dominant.
3. **Guided selection** — help choose the next best action or next best skill.
4. **Support / intervention** — provide structured help without pretending to be the whole system.
5. **Bridge** — connect public utility to private or premium intelligence.
6. **Ops / automation** — internal fleet or workflow helpers that support the broader system.

If a skill skips awareness and jumps straight to complex action, it is usually too early.

## What counts as a good skill
A good candidate skill usually has:
- a clear user problem
- a clear output shape
- a stable workflow
- a single dominant dimension
- a repeatable trigger
- a safe boundary
- an obvious way to test whether it helped

If the candidate cannot explain what it does in plain language, it is probably too vague.

## Selection parameters
Use these parameters when scoring or filtering candidate skills.

### 1. Utility
- Does the skill solve a real, repeated problem?
- Would another user want this without extra explanation?
- Does it create immediate value on first use?

### 2. Dimension fit
- Does the skill clearly belong to one primary 8D dimension?
- Is there a reasonable secondary dimension, but not too many?
- Is the signal strong enough that the dimension is obvious?

### 3. Safety and boundary fit
- Can the skill be released without exposing PHI, private calibration, or hidden internal logic?
- Does the skill avoid diagnosis, treatment, or overclaiming?
- Can the public version stay conservative and honest?

### 4. Reusability
- Can the skill be used more than once?
- Can it support a family of related outputs?
- Can the same structure work across many inputs?

### 5. Self-containedness
- Can the skill work without a long setup path?
- Does it need a lot of outside context to make sense?
- Can it live as a public skill instead of a session note?

### 6. Implementation fit
- Can the skill be written clearly right now?
- Is the logic stable enough to encode?
- Is it small enough to review and ship safely?

### 7. Measurement clarity
- Can the user tell whether it helped?
- Can the agent tell whether it performed well?
- Is there a visible output that can be reviewed?

### 8. Moat preservation
- Does the public version preserve the premium logic boundary?
- Is the open layer useful without giving away the good stuff?
- Can the premium layer add intelligence, memory, automation, or calibration later?

## Recommended scoring rubric
Score each candidate from 0 to 5 on each axis:
- Utility
- Dimension fit
- Safety / boundary fit
- Reusability
- Self-containedness
- Implementation fit
- Measurement clarity
- Moat preservation

General guidance:
- 0–1 = weak fit
- 2–3 = possible but needs refinement
- 4 = strong candidate
- 5 = excellent candidate

A candidate with a high utility score but weak safety score should not be shipped publicly yet.
A candidate with strong safety but weak utility may be useful later, but it is not a priority.

## Dimension-by-dimension skill targets

### PSY — Psychological / emotional state
Look for skills that help the user:
- name the emotional weather
- notice stress load
- identify emotional friction or recovery
- calm the day without overreaching

Good skill examples:
- emotional snapshot
- stress pattern review
- regulation prompt
- mood / friction summary

Selection note:
- Start with awareness and calming structure before deeper intervention.

### PHY — Physical state and recovery
Look for skills that help the user:
- understand sleep, energy, hydration, food, soreness, and recovery
- spot body strain early
- notice when the body is the main limiting factor

Good skill examples:
- sleep and recovery snapshot
- energy/load summary
- hydration or nourishment check
- body-state report

Selection note:
- Keep it conservative and non-diagnostic.
- Prefer observable signals over theory-heavy explanations.

### ENV — Environment and friction
Look for skills that help the user:
- see workspace clutter and interruptions
- reduce friction
- create a calmer setup
- identify environment problems before they become execution problems

Good skill examples:
- environment friction audit
- workspace reset guide
- distraction reduction checklist
- setup readiness report

Selection note:
- A good ENV skill makes the next action easier by reducing drag.

### SOC — Social connection and support climate
Look for skills that help the user:
- understand support, isolation, conflict, repair, and connection quality
- notice relationship strain or reinforcement
- separate support need from emotional overload

Good skill examples:
- connection snapshot
- support / friction review
- relationship climate check
- repair-oriented reflection

Selection note:
- Keep the language careful and avoid pretending to know what others feel.

### SPI — Meaning, values, and purpose
Look for skills that help the user:
- check alignment
- notice loss of direction
- reconnect work to values
- identify meaning drift

Good skill examples:
- alignment check
- purpose reflection
- values clarity prompt
- meaning / direction summary

Selection note:
- This dimension is best handled gently and with humility.

### INT — Intellectual load and cognition
Look for skills that help the user:
- manage focus, reading, analysis, and mental overload
- detect cognitive bottlenecks
- reduce complexity before decision-making

Good skill examples:
- focus load snapshot
- cognitive friction report
- reading / analysis helper
- mental clarity check

Selection note:
- Prefer skills that reduce overload rather than add more abstraction.

### VOC — Vocational output and execution
Look for skills that help the user:
- start tasks
- follow through
- ship work
- track momentum
- finish what was started

Good skill examples:
- execution brief
- task momentum report
- follow-through support
- output / completion tracker

Selection note:
- VOC skills should produce visible action, not just insight.

### FIN — Financial pressure and sustainability
Look for skills that help the user:
- notice money stress
- track resource strain
- assess sustainability
- identify pressure before it becomes panic

Good skill examples:
- money pressure snapshot
- resource sustainability check
- budget friction report
- financial stress summary

Selection note:
- Keep it practical and non-judgmental.

## Skill family pattern
For each dimension, prefer a family like this:
- **core** = the main awareness or reporting skill
- **support** = checklist, guide, or helper layer
- **bridge** = translation to a more advanced or premium workflow
- **ops** = internal automation or maintenance helper

This keeps the public layer clean and gives the agent a clear path for building more capability over time.

## What to prioritize first
If the platform is starting from ground zero, prioritize:
1. awareness skills
2. snapshot / reporting skills
3. safe next-step helpers
4. boundary-safe support skills
5. bridge skills that preserve the moat

This means the first wave should focus on clarity, not complexity.

## What to avoid first
Avoid releasing these too early:
- scoring engines that depend on private calibration
- broad recommendation systems with high downside risk
- anything that looks like a diagnosis engine
- large omnibus skills that mix too many dimensions
- workflows that only make sense inside one private project

## Release decision rule
A candidate skill is ready to move forward when:
- it has one primary dimension
- it is safe to expose
- it has a clear output shape
- it is understandable to another user
- it can be reused later
- it does not leak the premium moat

If it fails any of those, revise it or keep it in the watchlist.

## Agent instruction summary
When selecting skills, the agent should:
- look first for the primary dimension
- score utility, safety, and reusability
- prefer awareness before action
- keep public skills small and coherent
- preserve private calibration for premium layers
- ship the simplest useful version that still feels trustworthy
