# Agent roster layout audit notes

Session-derived notes for wide roster / persona-matrix PDFs.

## What worked
- Use A4 landscape for wide roster matrices.
- Keep margins at 0.5in or slightly above when the report includes long credential blocks and 10-option personality chips.
- Put a compact roster index near the front, then group the detailed cards by category / world / family.
- Treat cards as the primary unit, not just one giant table, when the content is dense.
- Render at least one early dense page and one late dense page. The late pages are where clipped chips, badge overflow, or hidden footer drift tends to appear.
- Check the outer edges of the page visually, not just the text layer.

## Layout pitfalls observed
- A page can look fine on the index section while later profile pages get cramped.
- Small pill badges and numbered personality chips can be the first things to clip even when the card border still fits.
- Right-edge overflow can hide inside visually acceptable tables until a rendered PNG is inspected.

## Verification checklist
- Confirm the rightmost column is fully visible.
- Confirm badge rows and personality chips are not touching the page edge.
- Confirm late-page cards still have breathing room below the title and within the card body.
- Confirm the footer page number is visible on both early and late pages.
- Confirm the exported companion catalog / JSON matches the visible PDF roster count.
