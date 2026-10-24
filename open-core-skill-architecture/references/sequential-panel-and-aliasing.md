# Sequential Panel Review and Canonical Persona Aliasing

This reference captures a reusable pattern for coaching panels and public-figure-inspired advisor personas.

## Sequential panel review

When a workflow uses multiple advisors or lenses:
1. Determine the user's actual need first, without assuming the domain.
2. Select only the advisors whose lanes match that need.
3. Run the advisors one at a time, in sequence.
4. Keep each advisor inside its lane.
5. If a context needs a new lane, expand the panel rather than forcing an out-of-scope answer.
6. Synthesize all individual outputs into one user-facing result.

## Canonical persona aliasing

When an advisor is inspired by a real-world public figure:
- never use the real person's name as the agent name
- assign a canonical DS-prefixed alias instead
- keep the alias consistent across users
- do not create duplicate aliases for the same persona
- make the alias describe the persona or role, not the real person

## Suggested naming shape

- `the specialist engine`
- `the specialist engine`
- `the specialist engine`
- `the specialist engine`
- `the specialist engine`

## Anti-patterns

- assuming the user is a principal when the intake did not say so
- running multiple advisor lenses concurrently when the workflow calls for sequential review
- emitting raw panel notes instead of one synthesized recommendation
- using real names for public-figure-inspired personas
- creating multiple aliases for the same canonical brain
