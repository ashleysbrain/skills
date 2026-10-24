# Per-calculation provenance and status tags

Use this checklist when rebuilding technical algorithm PDFs or companion docs that mix published science with Divinity Science / product-defined logic.

## What to tag on every calculation or layer
- `status`: LIVE / SPEC / DEV / RESEARCH
- `provenance`: published science / Divinity Science / hybrid
- `layer connection`: what upstream layer feeds it and what downstream layer consumes it
- `scope note`: whether the formula is finalized or intentionally evolving

## Required presentation rules
- Do not leave status only at the document top; repeat it on each algorithm card, layer header, or equation block.
- If a single label like `where`, `when`, or `distance` may represent multiple points, paths, or intervals, state that explicitly and show the intermediate calculations.
- If a header badge or section title is hard to read, treat contrast/color as a rendering defect and fix it before delivery.
- When merging future and in-progress calculations into one document, keep the families visually separated while still cross-linking them in the overview.

## Useful wording
- "This calculation is live and currently in use."
- "This calculation is product-defined and still evolving."
- "This layer is hybrid: it combines published methods with Divinity Science scoring rules."
- "This input is not a single scalar; it may expand into multiple time/location/distance points before scoring."

## Verification
- Check that every equation block has a visible status and provenance label.
- Check that the overview still explains how the layers stack together.
- Check that the rendered PDF keeps the headers readable on the actual page, not just in source HTML.
