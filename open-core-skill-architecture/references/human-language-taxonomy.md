# Human-Language Taxonomy Reference

Use this when a public skill needs a mapping dictionary, cue bank, or domain taxonomy that would otherwise bloat the umbrella SKILL.md.

## Rule of thumb
- Keep the umbrella skill focused on the workflow class.
- Put the long list of cues, examples, and edge cases in `references/`.
- Use the language people actually say out loud.
- Start from transcripts, notes, and user phrases; avoid AI-shaped jargon as the primary cue list.
- Keep abbreviations and technical labels as the internal anchor, but make the surface cues human-first.

## Good pattern
- Internal label: the concise dimension or category name.
- Reference cues: everyday phrases, slang, shorthand, and common complaints a human would naturally use.
- Mapping note: one short line explaining why the cue maps there.

## Guardrails
- Do not invent a new taxonomy because the wording feels incomplete.
- Do not rename the dimensions just to make the list look smarter.
- Do not treat keyword matching as diagnosis or certainty.
- Do not let one-off examples become a hidden scoring system.

## When to split into references
Split the detailed mapping out of SKILL.md when:
- the cue bank is long
- the taxonomy is reused across multiple outputs
- the skill needs to stay class-level and releaseable
- the mapping benefits from iterative tuning without rewriting the umbrella
