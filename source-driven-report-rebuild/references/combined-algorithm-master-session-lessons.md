# Combined algorithm-master session lessons

Use this reference when rebuilding a merged algorithm/calculation document for a technical team.

## What the user wanted
- Combine two related calculation documents into one presentable artifact when possible.
- Keep all content, but reorganize it so the team can actually read and discuss it.
- Make every algorithm/section visibly marked with status.
- Show how the algorithms layer together and connect to the open-core architecture.
- Include both the current/in-progress calculations and the future/predictive calculations in one narrative when appropriate.

## Durable lessons
- **Per-section status is mandatory.** Do not only label the top of the document; every algorithm card/section needs its own LIVE / DEV / SPEC / RESEARCH marker.
- **Legibility beats decorative color.** If a section header or badge is rendered in a low-contrast color, change it before delivery and re-check the PDF.
- **Header colors and badge colors are different jobs.** Sometimes the large section headers are fine, but the smaller `layer / model / family` badges need the contrast fix. Check both layers separately.
- **Merged documents still need boundaries.** When combining multiple docs, preserve the distinction between live work, work-in-progress, and future-facing calculations instead of flattening them into one generic bucket.
- **Explicit layering helps technical audiences.** Add a short overview that explains how the algorithms stack, how outputs feed one another, and where the open-core layers end and product logic begins.
- **Evolving algorithms should be called out.** If formulas are not finalized, say so plainly; do not present them as frozen truth.
- **Multi-point inputs should not be flattened.** For 5WH-style or similar fields, treat time, distance, where/location, and related inputs as potentially having multiple points and intermediate calculations.
- **Intentional ordering must be explained.** If a family is left out of numeric order for semantic reasons (for example, a support family staying immediately after TWC), say that in the document so the reader knows the ordering is deliberate.
- **Remove meta-team framing unless the user wants it.** Keep the artifact as a document, not a "team deck," "team version," or similar narration. The content should stand on its own.
- **Format examples as cards, not loose lists.** Cross-dimension cascades, algorithm interlock maps, and quest examples should be boxed or carded so the examples are readable in PDF form.
- **Team-ready format.** Include an opening explanation the team can discuss, plus the specific questions the architecture should answer.

## Suggested rebuild checklist
1. Merge the source docs into one coherent hierarchy.
2. Add or normalize a top-level legend for status/provenance.
3. Add a per-section/per-algorithm status label.
4. Add a layering/connection overview.
5. Mark evolving formulas as provisional where needed.
6. Fix any low-contrast header colors.
7. Expand 5WH-like sections so they show sub-calculations or multiple points where appropriate.
8. Rebuild the PDF and verify the rendered text is readable.
