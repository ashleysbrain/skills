# Memory Layering and Reuse

## Durable rule
- Prefer one **canonical shared memory** file plus per-engine/per-persona **delta memories**.
- Do **not** assume a memory file automatically imports or merges another memory file unless the loader explicitly does that.
- A plain text reference like `See ../shared-baseline.md` is only a human link, not an automatic include.

## Recommended structure
- `memory/shared-baseline.md` — stable facts common to all engines/personas
- `memory/<engine>.md` — engine-specific exceptions, lane rules, and local facts
- `memory/<engine>-project.md` — optional project-scoped overlay when needed

## Best practice
- Keep the shared file small and stable.
- Put only differences in the engine file.
- If automatic reuse is needed, add a merge/generation step that renders the final memory file from the shared base plus the engine delta.

## Pitfall
- Don’t depend on nested references for critical instructions unless the runtime is known to resolve them.
