# Recent Artifact Retrieval for 8D Snapshot Reports

Use this when the user asks to *show* the latest report or asks for "the one you worked on last night."

## Retrieval sequence
1. Check recent session context for the report task, filename, or PDF name.
2. Look for the newest rendered artifact in the workspace or `/tmp` when the session context is incomplete.
3. Prefer the most recent verified artifact whose name matches the report theme.
4. Verify content by extracting text from the PDF or reading the markdown before delivery.

## Verification cues
- The report title should match the requested theme.
- The body should include the intended update, such as quick wins, movement notes, or baseline comparison language.
- If more than one candidate exists, choose the newest verified one and note that briefly.

## Pitfall
Do not deliver an older draft just because it is the first matching filename. Recent report tasks often leave multiple variants behind.

## Discrepancy rule
If you find both a passive-only scorecard and a verified rescore for the same date, treat the passive-only output as a freshness check, not the canonical report. Prefer the verified rescore when it is newer, warning-free, and explicitly labels the artifact as final/canonical.
