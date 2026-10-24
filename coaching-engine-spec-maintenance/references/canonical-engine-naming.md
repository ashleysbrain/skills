# Canonical Engine Naming

Session-derived naming rule for the Divinity Science coaching/healing docs.

## Rule

When the repo owns an engine, use the actual canonical engine name in titles, prose, and runtime-facing wrappers.

- Use `8D Coaching` for the coaching system.
- Use `8D Heal AI` for the healing system.
- Use `the specialist engine` for the coach agent.
- Use `the specialist engine` for the doctor agent.

## Avoid

Avoid leaving generic descriptions in place when the engine has a canonical name.

Examples of generic descriptions to replace:
- coaching engine
- algorithm engine
- healing engine
- trajectory engine
- system description that omits the canonical engine name

## Practical checks

Before finishing a naming pass, search for:
- `coaching engine`
- `algorithm engine`
- `healing engine`
- mixed titles that pair a canonical system name with a generic subtitle

Then update:
- doc titles
- opening paragraphs
- runtime wrapper files like `AGENT.md` and `SOUL.md`
- subtitles/abstracts in generated HTML or PDFs
