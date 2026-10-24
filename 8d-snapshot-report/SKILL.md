---
name: 8d-snapshot-report
description: Use when the user wants a concise, non-diagnostic 8D snapshot report that compares current notes against a baseline and explains change without overclaiming trend or certainty.
version: 1.0.15
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [health, 8d, snapshot, baseline, trend, reporting, non-diagnostic, open-core]
    related_skills: [8d-pattern-awareness, open-core-skill-architecture, scientific-methodology-review-and-consolidation]
---

# 8D Snapshot Report

## Purpose
Use this skill when the user wants a report-oriented 8D output that is explicitly baseline-aware.

This skill is a support layer for `8d-pattern-awareness` in the health-reporting lane, and a release-review overlay for the V1 skill product lane.
It does not replace the main 8D review skill; it sharpens the comparison layer so the agent can describe what changed, what stayed stable, and what is uncertain.

The output should be clear, compact, and human-readable.
It should feel like a trustworthy snapshot, not a diagnosis, not a dashboard, and not a generic wellness summary.

## Manifest

The following files are part of this skill's support structure:

- `templates/snapshot-report-template.md`
- `references/baseline-comparison.md`
- `references/release-guidance.md`
- `references/release-positioning.md`
- `references/release-review-lane.md`
- `references/handoff-bundle.md`
- `references/handoff-and-retrieval.md`
- `references/recent-artifact-retrieval.md`
- `references/report-style-calibration.md`
- `references/snapshot-test-suite.md`
- `scripts/verify-manifest.sh`

## When to Use
Use this skill when the user asks to:
- compare today against yesterday or another prior note
- identify change over time
- produce a snapshot report or check-in summary
- understand whether the current pattern is improving, stable, or worsening
- distinguish a one-off note from a repeated pattern
- review the *skill product* or release surface when the task is about the V1 report/agent-brain family rather than personal health scoring

For product/release review mode, keep the same baseline discipline but shift the object of review to the current skill anchor, its references, and its immediate release ecosystem. Use the newest verified artifact first when the user asks to *show* the report.

Do **not** use this skill when:
- the user only wants a one-time note interpretation with no comparison
- there is no baseline and no prior context to compare against
- the request is really about diagnosis, treatment, or emergency care
- the evidence is too thin to support any meaningful comparison

## Core Comparison Rule
A snapshot report must answer two separate questions:
1. What is happening now?
2. What has changed versus the best available baseline?

Do not merge those into one vague impression.
Do not call something a trend unless the evidence supports trend language.

## Baseline Selection Order
Use the most truthful baseline available, in this order:
1. A user-stated baseline
2. The most recent comparable note or check-in
3. A small rolling window summary from prior entries
4. No baseline, if nothing comparable exists

If a baseline is weak or mismatched, say so plainly.
If there is no baseline, output a snapshot only and label it as such.

## Baseline Quality Levels
Treat the comparison strength like this:
- **Strong baseline**: same metric, similar conditions, recent, repeatable
- **Moderate baseline**: mostly comparable, but not identical
- **Weak baseline**: sparse, old, or condition-mismatched
- **No baseline**: only one data point or nothing comparable

Never hide the baseline quality.

## Comparison Dimensions
When comparing the current state to baseline, check:
- direction: better, worse, same, or unclear
- stability: steady, fluctuating, or drifting
- magnitude: small, moderate, or large only when the evidence supports it
- confidence: how reliable the comparison is
- relevance: whether the change actually matters

If the source does not support a magnitude estimate, do not invent one.

## Output Shape
A good snapshot report should usually include:

1. **Snapshot**
   - one or two lines about the current state
   - name the most important 8D dimensions

2. **Baseline used**
   - state the baseline source in plain language
   - label its quality

3. **What changed**
   - list only the meaningful deltas
   - separate actual change from unchanged areas

4. **8D movement**
   - note which dimensions moved up, down, or stayed stable
   - keep the mapping narrow and conservative

5. **Confidence**
   - high / medium / low
   - explain why briefly

6. **What this likely means**
   - a short, non-diagnostic interpretation
   - avoid overfitting one data point into a story

7. **Safe next step**
   - one low-risk action the user can actually do

8. **What would change the reading**
   - one missing piece of data, if helpful

## Comparison Language
Use language like:
- "compared with yesterday, sleep looks worse and energy is lower"
- "the pattern is stable, but confidence is limited because the baseline is sparse"
- "this looks improved relative to the last check-in, but the sample is small"
- "no trend claim yet; this is only one point"

Avoid language like:
- "the data proves"
- "definitely improving"
- "this always means"
- "the trend is clear" when it is not

## Baseline Comparison Guardrails
- Do not claim a trend from a single point
- Do not compare unlike things as if they were the same metric
- Do not convert one dramatic change into a full pattern story
- Do not inflate confidence when the baseline is weak
- Do not invent numbers, scores, or percentages
- Do not turn comparison into diagnosis

## Red Flags
If the input contains urgent medical warning signs, stop the snapshot report and escalate appropriately.
Do not continue pattern comparison past a clear safety issue.

## Quality Bar
A valid report should be readable in under a minute and should clearly answer:
- what is happening now
- what changed
- how strong the comparison is
- what the safest next step is

## User-first output rule
Do not write the report like an analyst summary. Lead with the user's lived experience, the friction they are feeling, and the action that would help most. If the first draft sounds generic or could apply to anyone, rewrite it to be more concrete and user-facing. Match the style to `references/report-style-calibration.md`: compact, healing-centered, clinical-clean, and premium without heavy headers or excessive whitespace. If the user requests a narrow edit to an existing PDF or report, preserve the baseline layout exactly and change only the requested field(s); see `8d-pattern-awareness` for the color-only / no-reflow workflow (the editing-constraints reference lives in that skill's references directory).

When the report is rendered as a PDF, keep the spacing tight but not cramped, spread the content naturally across the page, and do not add a top banner that explains the document is generated.

## Reference Bundle
This skill ships with these support files:
- `references/snapshot-examples-and-tests.md` — sample outputs, test cases, and guidance for snapshot reports
- `templates/snapshot-report-template.md` — one-page fill-in template for the final report shape
- `references/release-guidance.md` — routing index to release positioning and review lane references
- `references/handoff-bundle.md` — what to include when the user wants the skill shown in action, not just summarized
- `references/report-style-calibration.md` — shared visual and tone rules for the compact premium PDF report
- `references/recent-artifact-retrieval.md` — retrieval-first workflow and stale-versus-canonical report handling

## Release Identity
- `8D Snapshot Report — support — v1.0.14 — 2026-06-29`
- Public role: baseline-aware 8D reporting layer
- Public promise: compare the current note to the best available baseline and keep the output honest, compact, and non-diagnostic

## Release Verification

Before releasing, run the verification script to ensure the manifest list in SKILL.md matches the actual files in references/, templates/, scripts/, and attachments/ directories.

Also, verify that the release identity in the SKILL.md matches the release identity in any reference files that contain it (such as references/release-positioning.md). Grep for the version pattern across all reference files: if any file carries a stale version tag, it will silently contradict the SKILL.md release identity. Fix by updating all copies to match, or (better) collapsing duplicate content into a routing index so the version lives in one canonical place.

## Common Pitfalls
1. **Calling a trend too early**
   - Fix: require enough comparable points or say the trend is not established.
2. **Hiding a weak baseline**
   - Fix: label the baseline quality directly.
3. **Mixing unlike data**
   - Fix: compare like with like and narrow the scope.
4. **Inventing numbers**
   - Fix: stay qualitative unless the source already provides a real measurement.
5. **Turning comparison into diagnosis**
   - Fix: stay non-diagnostic and escalate red flags instead.
6. **Stopping at a release note when the user asked for the actual output**
   - Fix: include a live smoke test document that renders the report as if run, and use the release note only as a supplement.
7. **Treating a stale passive-only scorecard as canonical when a verified rescore exists**
   - Fix: compare freshness flags, source mode, and warnings first; if a canonical rescore is newer, verified, and warning-free, use that artifact and call the stale output a discrepancy.

8. **Neglecting to verify the support file manifest**
    - Fix: run the verification script `scripts/verify-manifest.sh` periodically to ensure the manifest list in SKILL.md matches the actual files in references/, templates/, scripts/, and attachments/ directories.

9. **Reference-heavy skill stalls update engine scans**
    - This skill has 8 references + 1 template + 1 script = 10 support files. When the skill-update-engine runs in single-job mode and inspects this skill during the scan phase, the agent can stall reading all reference files before producing candidates or emitting the monitoring JSON block.
    - Observed: Divinity Health V1 Skill Product Review job `c37a1090869d` stalled at 03:30 AM CDT while reading this skill's references, producing 0/3 new skills and 0/5 updates.
    - Fix: The skill-update-engine should implement a reference-file budget (max 3 files per skill unless it's the primary review target) and emit the JSON monitoring block early. See `skill-update-engine` Section 11.1 for mitigation details.

10. **Reference file content duplication**
    - When a reference file contains full inline copies of content from sibling reference files, one copy silently drifts out of sync when the canonical source is updated. This produces version and heading inconsistencies that are hard to spot in a manifest check.
    - Observed (2026-06-30): `release-guidance.md` contained full copies of both `release-positioning.md` and `release-review-lane.md`, including stale version tags (`v1.0.11` while SKILL.md was at `v1.0.14`) and duplicate heading structures.
    - Fix: collapse the duplicating file into a routing index that points to the canonical sources. Keep one authoritative file per topic. Detection: if two sibling references share >50% body text, refactor the duplicator into a pointer.

## Verification Checklist
- [ ] Baseline source is named
- [ ] Baseline quality is labeled
- [ ] Change is separated from confidence
- [ ] Trend language is not used from a single point
- [ ] No invented percentages, scores, or hidden weights
- [ ] One safe next step is included
- [ ] Red flags escalate immediately
- [ ] Template and examples match the skill output shape
- [ ] If a stale passive-only artifact conflicts with a canonical rescore, the report names the discrepancy and uses the verified rescore as canonical

## Recent Artifact Retrieval
When the user asks to *show* the latest 8D report rather than regenerate it, prefer a retrieval-first workflow:
1. Search recent session context for the matching report task or filename.
2. Inspect the freshest rendered artifact in the workspace or `/tmp` if the session context is ambiguous.
3. Verify the file contents by extracting text from the PDF/MD before delivering it.
4. If multiple candidates exist, choose the newest verified artifact with the closest title match and say so briefly.
5. If a passive-only or stale scorecard conflicts with a verified rescore, privilege the verified rescore and label the stale artifact as a pipeline discrepancy.

This avoids handing over a stale draft when a newer rendered version already exists.

## References

The complete file listing is in the **Manifest** section above. For descriptions of key support files, see the **Reference Bundle** section.