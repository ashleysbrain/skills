# Raster Label Removal Workflow (Session Note)

Use this when the user marks multiple headers or labels on a raster-only report PDF and wants them removed without changing the rest of the page.

## Observed rule
- Treat the user-provided screenshot or markup as the ground truth for *which* labels to remove.
- Do not assume only the first visible section label is in scope if the user circled several.
- Keep the page geometry untouched; edit only the label pixels.

## Reliable sequence
1. Start from the clean baseline PDF render.
2. Render the page to a high-resolution image.
3. Use OCR to enumerate all visible `SECTION xx` labels and confirm the target set.
4. Remove only the exact label regions the user indicated.
5. Preserve nearby headers, corner artwork, titles, and body spacing.
6. Re-render the PDF and OCR-check that the target labels are gone.
7. Visually compare the upper-left corner and other untouched regions against the baseline.

## Practical pitfall
A local repair can still be wrong if it erases the wrong line or creeps into the page corner. Verify the non-target regions explicitly, especially the upper-left header area, before delivery.

## Verification pattern
- OCR should no longer return the removed section labels.
- The remaining headings should still read correctly.
- The top-left corner, title block, and section spacing should match the baseline render except for the removed labels.
