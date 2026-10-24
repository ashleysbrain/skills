# 2026-06-06 — ADHD reorder + patch-over-rewrite

## Durable lesson
When the user delivers nonlinear spoken instructions, especially while frustrated, do not execute them in literal order. Reconstruct the dependency order first.

## Failure mode to prevent
- User asks for one tweak.
- Agent regenerates the whole document or whole section.
- Earlier approved edits are overwritten.
- User has to restate the same constraint multiple times.

## Correct operating pattern
1. Identify the canonical artifact currently in force.
2. Extract the requested delta only.
3. Mark locked or approved content that must survive untouched.
4. Reorder the work into the implementation sequence that avoids clobbering prior edits.
5. Patch locally.
6. Verify that only intended scope changed.

## Phrase-level cues that should trigger this pattern
- "tweak one thing"
- "do surgical edits"
- "don't redo the entire document"
- "I'm bouncing all over the map"
- "put this in the right order"
- frustration about circular work or overwritten edits

## Application beyond documents
This applies to plans, agent profiles, workflows, system audits, and multi-phase implementations. Separate:
- audit/review
- questions for the user
- next audit pass
- synthesis plan
- implementation

Do not collapse those phases unless the user explicitly asks for a combined pass.
