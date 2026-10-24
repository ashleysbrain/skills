# Class-Level Skill Shape

Use this pattern when deciding whether to create or revise a skill:

## Default shape
- One umbrella skill per durable workflow class.
- Rich `SKILL.md` for the reusable operating model.
- Session-specific details, examples, quirk logs, and rollout notes go in `references/`.
- Use `templates/` for starter artifacts and `scripts/` for deterministic checks.

## Good signals for an umbrella
- The workflow will recur across sessions.
- Multiple narrow ideas are clearly variants of the same class.
- The public output can be described as a stable user promise.
- The skill needs a consistent release boundary or upgrade path.

## Bad signals for a new narrow skill
- It only makes sense for one session or one incident.
- It names a single bug, ticket, error string, or release artifact.
- It duplicates an existing workflow with a different surface label.

## Preferred maintenance pattern
1. Update the umbrella `SKILL.md` first.
2. Move detailed examples or session-specific material into `references/`.
3. Add templates/scripts only when they are reusable across sessions.
4. If two skills overlap, note the overlap in the umbrella instead of fragmenting the library.

## Release hygiene
- Prefer class-level packaging over one-off entries.
- Keep the main skill readable and stable.
- Let the references absorb the churn.
