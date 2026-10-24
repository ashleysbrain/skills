# Combined algorithm master rebuild lessons (2026-06-02)

Use this note when rebuilding combined technical algorithm documents for presentation or audit review.

## What the user wanted
- Merge multiple related algorithm/calculation documents into one coherent artifact when possible.
- Keep the original source material intact; prefer additive edits over deletions.
- Make the document readable for a technical team, not just visually polished.
- Make the status of *every* algorithm explicit.
- Show how algorithms layer together and how they connect to the surrounding architecture/open-core stack.
- Make the original/base algorithm visible near the front so reviewers can immediately identify the foundation.
- Separate multi-point fields like 5WH-style time/location/path inputs into sub-points and intermediate calculations instead of flattening them.

## Practical lessons
- Put a status marker on each calculation card/section: `LIVE`, `DEV`, `SPEC`, or `RESEARCH`.
- Put provenance at the formula level when the document mixes public science and product-defined logic.
- Preserve family numbering/order unless you intentionally renumber the whole doc.
- If one family must stay out of numeric order, keep it stable and add a note rather than renumbering just one item.
- Front-load the original/base algorithm as an anchor section instead of burying it later in the family stack.
- If a section header or badge is hard to read, fix contrast in the rendered artifact and re-check the PDF.
- If the PDF text layer misses a visible heading, inspect the rendered page blocks/coordinates before assuming the source edit failed.
- For 5WH-like inputs, show sequences/paths/points-in-time explicitly, not as one scalar per label.
- For combined algorithm documents, include a short overview that explains how the pieces layer together and how they relate to the architecture/open-core boundary.
- If the document includes open-core framing, separate public scientific transparency from proprietary thresholds, tuning, and ranking.

## Source and build notes
- Keep the source document additive: append addenda, repair cards, or companion sections instead of deleting the original sections.
- If formulas are emitted from Python f-strings and include literal braces or set notation, escape braces first (`{{ }}`) before rebuilding.
- Verify the actual PDF, not just the HTML.
- For dense repair pages, verify the final pages with text extraction and rendered inspection; some headings render visibly but may fragment in the text layer.

## Reusable checklist
1. Confirm the source files and the intended combined scope.
2. Add per-section status and provenance labels.
3. Preserve the original base algorithm visibly near the front.
4. Separate multi-point fields into sub-calculations.
5. Add an overview that explains the layer stack and architecture boundary.
6. Rebuild the artifact.
7. Verify the rendered PDF, the text layer, and the readability of compact badges/headers.
