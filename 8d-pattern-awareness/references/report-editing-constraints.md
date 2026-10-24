# Report Editing Constraints

This note captures user-corrected editing constraints for 8D Pattern Awareness report generation.

## Session-learned editing rule
When the user asks for a formatting fix, preserve the existing layout and only change the exact requested field(s). Do not redesign the PDF, rebalance spacing, change box geometry, or swap the visual hierarchy unless the user explicitly asks for that.

If the user says "change just the red," treat that as a one-variable edit: keep the blue intact, keep roundedness and spacing intact, and touch only the red accent.

If the user points to a specific baseline PDF or says "go back to that version," treat that artifact as the visual source of truth and match it before making the requested color-only change.

## Narrow-edit examples
- If the user says "do not change the formatting," keep the same page structure, spacing, block layout, and box geometry.
- If the user says "just change the red to yellow," keep everything else identical and edit only the red accent. Leave blue, spacing, box shape, and hierarchy unchanged.
- If the user says "delete the section number," remove that numbering without renaming the sections or altering the rest of the header style.
- If the user says "go back to that version," use the user-provided baseline as the template and change only the requested field.

## Practical pitfall
A well-intended cleanup can still be wrong if it changes the feel of the document. Treat the existing report as the baseline unless the user asks for a redesign.

## Structure-preserving color-only workflow
When the user says the structure must stay identical and only the accent color should change, do **not** rebuild the PDF layout from scratch if that risks text-flow drift.

Preferred order:
1. Keep the original PDF or rendered page as the source of truth.
2. Make only the minimum visual change needed to swap the accent color.
3. Preserve x/y placement, spacing, box geometry, and hierarchy exactly.
4. Verify the output against the baseline for layout drift before delivery.

If a regeneration changes line breaks, section spacing, or the apparent center of the page, treat that as a failed method and switch to a preservation-first approach.
