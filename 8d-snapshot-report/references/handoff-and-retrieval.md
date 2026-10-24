# Handoff and Retrieval Guide

# 8D Snapshot Report Handoff Bundle

Use this when the user asks to see what the document looks like *if run*, or when they say the release note alone is not enough.

## Required bundle when demonstrating the skill
Include:
1. **Test pack**
   - covers strong baseline, weak baseline, no baseline, mixed movement, trend bait, and red-flag escalation
2. **Live smoke test**
   - a concrete mock input
   - the baseline used
   - the rendered report output in the exact report shape
3. **Release note**
   - optional appendix only
   - not the primary deliverable when the user wants to see the actual workflow output

## Rule
Do not stop at a release note if the user asked to see the skill in action.
Show the output shape as if the skill had run.

## Verification
Before handing off, confirm that the live smoke test includes:
- Snapshot
- Baseline used
- What changed
- 8D movement
- Confidence
- What this likely means
- Safe next step
- What would change the reading

# Recent Artifact Retrieval for 8D Snapshot Reports

Use this when the user asks to *show* the latest report or asks for \"the one you worked on last night.\"

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