# Project Modes / Lenses

Session-derived notes for temporary project-scoped overlays on stable agent personas.

## Pattern

Use a **project mode** (or **lens**) when the user wants a temporary, additive layer on top of an existing persona or rostered agent.

- **Core persona stays stable**
- **Project layer is additive only**
- **One active project mode at a time**
- **Project mode expires** when the project ends or scope changes
- Prefer short names like **Mode** or **Lens** over longer labels like Shield

## Recommended fields

- `mode`: internal or registry name for the overlay state
- `label`: human-readable name shown to the user
- `lens`: short descriptor of the work focus
- `scope`: what work the overlay may touch
- `activation`: what turns it on
- `exit`: what turns it off
- `rules`: guardrails that prevent persona drift

## Practical defaults

- Default overlay should not replace the base persona
- The overlay should be narrow enough to be auditable
- If the user asks for a project-specific version of an existing agent, prefer an overlay before inventing a permanent new persona
- If the user wants the panel first, present the roster/dispatch panel first and wait for approval before doing research or synthesis

## Dispatch metadata from the session

When the roster is stored in JSON or a database, the useful shape is a `personaLayers` block with an explicit active mode:

```json
{
  "personaLayers": {
    "base": {"label": "stable core persona"},
    "task": {"label": "short-lived execution lens"},
    "project": {"label": "mission-scoped overlay"}
  }
}
```

Selection rule:
- resolve `base` vs `task` vs `project` *before* dispatch
- use `task` for narrow bounded execution
- use `project` for mission-wide overlays and initiative tracking
- keep the base persona stable so the analytics layer can attribute work correctly

## Display / UX cue

Show the active project mode explicitly in agent cards, profile drawers, or dispatch panels so the user can see:
- what is core identity
- what is temporary project context
- when the overlay is active
