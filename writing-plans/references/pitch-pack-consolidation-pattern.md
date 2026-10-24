# Pitch-Pack Consolidation Pattern

## Why this pattern exists
A pitch pack for a complex methodology should not sprawl across many small PDFs. The best default is to consolidate into a small number of artifacts that each have a clear job:

1. **Master brief** — the executive narrative, product wedge, audience framing, and business story.
2. **Technical appendix** — the scoring engine, math, score families, worked examples, and source-of-truth details.

If the audience needs more granularity, add a third document only when the extra split improves comprehension for a specific reader group.

## What worked in the session
- The user asked to reduce the number of documents.
- The previous multi-PDF pack was collapsed into two combined PDFs.
- The master brief bundled the onboarding, executive, product, journey, and business sections.
- The technical appendix taught the scoring system in layers and included a worked example.

## Teaching the scoring system
When the document is educational, do not stop at a formula or a summary line. Explain the path:

- raw evidence
- normalized signals
- dimension scores
- baseline
- confidence
- coupling / interaction terms
- composite score
- state or action

Include at least one worked example with intermediate values so the reader can see how the final number is produced.

## Verification checklist
After generating the PDFs:
- Extract text from the final PDFs.
- Confirm that the score-family language is present.
- Confirm that sub-scores and optional/contextual scores are visible in searchable text.
- Confirm that the worked example heading and intermediate values survived rendering.
- If bullets are lost in extraction, switch to deterministic hyphen-prefixed paragraphs instead of trusting decorative list formatting.

## Packaging rule of thumb
- If the pack is for executives + engineering, use 2 PDFs.
- If the pack is for a large cross-functional audience, use 3 PDFs max.
- Avoid 5+ docs unless each audience really needs a separate entry point.
