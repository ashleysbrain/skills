# Repo boundary and doc-label normalization

## Session lesson
When the user corrects the owning repo or product-line boundary, the fix is not just a wording change. Audit the repo scope first, then normalize labels across the canonical docs bundle and remove accidental edits from the wrong repo before finishing.

## What this looked like in practice
- The canonical engine repo was the Divinity Science `ds-wave-coaching-engine` repository.
- The docs had mixed labels (`the specialist engine Engine`, `8D Coaching`, `Divinity Science`) across the README, docs index, and section headers.
- The safe repair was:
  1. identify the correct owning repo
  2. roll back stray edits in the wrong repo
  3. normalize the top-level repo label
  4. normalize the section headers and `Label:` lines in the core docs
  5. verify no stale repo-name matches remain

## Verification habit
When cleaning up a named engine/lane or repo boundary:
- search the repo for the old and new names
- check the README, docs index, and core spec files as one bundle
- confirm the final artifact uses one naming system consistently

## Reminder
This is a curation pattern, not a one-off fix. Apply it whenever a repo-owned agent package or docs bundle gets renamed, re-homed, or split across product lines.