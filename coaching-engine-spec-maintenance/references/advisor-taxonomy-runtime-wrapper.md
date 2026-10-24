# Advisor taxonomy and runtime-wrapper notes

## Durable lessons from the the specialist engine coaching-engine pass

### Runtime-facing package
A coaching-engine agent is not complete if it only has documentation. When there is a live agent package, verify the runtime-facing files too.

For the specialist engine, the runtime-facing package is:
- `agents/ds-wave/SOUL.md` — identity, voice, behavior, advisor rules
- `agents/ds-wave/AGENT.md` — runtime wrapper, startup reads, activation rules, verification checklist

### Advisor taxonomy
Keep the advisor categories explicit and separate:
1. **General coaching advisors**
   - best-in-field / best-in-niche for the coaching area
   - grounded in peer-reviewed philosophy and science
   - highly credentialed, which may include university research, academic or professional affiliations, and/or certifications

2. **Public human-figure mirror advisors**
   - public TWC scores
   - public-source brain/style/skillset
   - public news / public-information-only basis
   - DS-prefixed descriptive names

3. **Narrow specialist advisors**
   - narrow focus, but still highly credentialed and elite within the lane
   - may include university research, academic or professional affiliations, and/or certifications
   - do not downgrade them just because the scope is narrow

### Activation rule
- Fresh summon: ask the first useful question.
- Background continuation: resume from current state.
- Resumed after handoff: load the handoff summary first, then continue from the preserved session state.

### Activation-mode coverage drift (found 2026-06-03)
The most common coherence failure: operational docs (process-flow.md, state-machine.md) define all 3 activation modes, but identity/behavior docs (SOUL.md, AGENT.md, README.md, question-flow.md) only reference 2. The verification checklist in SOUL.md and AGENT.md also omitted the 3rd mode. Fix: after any mode definition change, search every file in the package for the activation-mode phrasing and confirm all 3 appear.

### Naming consistency (found 2026-06-03)
State-machine.md used "live background continuation" while all other files used "already running in the background." Canonical phrasing is "already running in the background." Always align naming to one canonical form across the entire doc set.

### Verification habit
When updating a coaching-engine package, verify both:
- the docs/spec layer
- the live runtime-facing package/files

Search for the exact category names and activation phrases to ensure the rule landed in the live text.