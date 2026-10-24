# Repo Disambiguation Lesson

## Trigger
The user says you are in the wrong repo, the wrong lane, or the wrong branded branch of a repo.

## Lesson
Do not trust the first exact-match search result.

## Workflow
1. Search for the canonical files that define the lane:
   - runtime wrapper / agent entrypoint
   - docs index / mirror
   - primary spec or soul file
2. Search adjacent product families or sibling lanes for naming collisions.
3. Compare the bundle, not just one file.
4. If the user corrected the owning repo, treat that as a boundary fix, not just a path fix.
5. Summarize the canonical repo only after the bundle agrees.

## What this avoids
- reopening a secondary or stray lane by mistake
- mixing product-panel docs into principal coaching docs
- treating a first-hit search result as authoritative
- narrating the wrong repo as if it were the right one

## Example from this session
The user wanted the personal principal coaching advisory board details and history, not the secondary product-panel files. The correct lane was the the specialist engine principal coaching bundle:
- `agents/ds-wave/SOUL.md`
- `docs/ds-wave/chat-thread-mirror.md`
