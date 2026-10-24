# Runtime package consistency audit — the specialist engine case note

## Why this note exists
A repo can look healthy if README and docs read cleanly, while the runtime-facing wrapper still omits a critical startup read. This session caught that exact mismatch in the the specialist engine coaching-engine package.

## Durable lesson
When maintaining an agent/package bundle, audit these together:
- repo README / docs index
- runtime-facing wrapper files
- canonical docs that the wrapper says it reads at startup

If the wrapper advertises advisor categories or public scoring, the startup-read list should include the docs that define:
- aliasing / canonical naming
- public-only scoring rubrics
- category distinctions

## Example pattern
In this session, the runtime wrapper was aligned by adding the missing canonical reads for:
- `docs/your-org/coaching-engine/aliasing-schema.md`
- `docs/your-org/coaching-engine/public-twc-rubric.md`

## Curation tip
Record this as a *bundle-consistency* lesson, not as a one-off file fix. The reusable skill is the audit pattern: wrapper + index + canonical docs must agree.
