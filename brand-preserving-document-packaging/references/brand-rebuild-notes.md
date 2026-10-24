# Brand Rebuild Notes

Session notes for brand-preserving PDF rebuilds.

## What worked
- The original Divinity Science logo asset was available at `/<workspace> Science/DivinityScienceLogo1.png`.
- The logo’s dominant colors sampled to a gold/charcoal identity:
  - gold accent: `#FFCD38` (RGB 255, 205, 56)
  - charcoal body/text: `#4A4A4A` (RGB 74, 74, 74)
- Rebuilding the document pack from markdown/HTML with WeasyPrint was more reliable than trying to patch an already-generated PDF.
- Applying the same theme to the combined pack and each standalone PDF kept the brand consistent.
- Verification that each rendered PDF had the logo on the first page and a non-trivial page count caught layout regressions quickly.

## Practical rebuild recipe
1. Locate the original logo or approved brand asset in the source material.
2. Sample the logo for dominant colors instead of inventing a new palette.
3. Re-render the source docs with a shared HTML/CSS theme.
4. Apply the logo to the cover and/or running header.
5. Produce both the combined pack and the individual PDFs if the user asked for both.
6. Verify page count and image presence with PDF inspection.

## Verification signals
- Combined pack and standalone PDFs all use the same logo and accent color.
- First page includes the logo image when expected.
- Headers, cover rule, and headings consistently use the brand accent.
- The final artifacts are regenerated files, not stale edits to a prior PDF.
