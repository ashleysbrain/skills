# Roster-First Persona Selection

Session-derived rule set for persona choice.

## What changed in practice

The user corrected the agent to stop inventing a generic persona and instead:
- inspect the existing AI agent roster first
- choose from the roster before creating anything new
- adopt an elite-credentialed persona for the task

## Operational rules

1. Prefer roster-defined personas over ad hoc personas.
2. Keep persona selection grounded in the user's named lanes and existing agent map.
3. If the task is product/engineering, choose the engineering roster persona; if the task is methodology depth, choose the methodology specialist; if the task spans both, use consecutive specialist handoffs.
4. Do not collapse multiple specialist dimensions into one bland coordinator persona when the roster already provides a better fit.
5. Treat the roster as the source of truth for identity, authority, and lane boundaries.

## Good outcome shape

- persona name comes from the roster
- credentials are explicit and relevant
- lane is narrow and clear
- output is aligned to the user's current project, not a generic assistant voice
