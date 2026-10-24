# Vertical stack PDF layout lesson

Session lesson:
- In combined algorithm/gamification PDFs, a section that looked fine in HTML still rendered with cards drifting into a right-side column.
- The fix was to replace grid-based containers for the final PDF sections with block flow.
- For dense card lists like an algorithm interlock map or quest examples, use:
  - `display: block`
  - child cards at `width: 100%`
  - `break-inside: avoid` and `page-break-inside: avoid`
  - no `grid-column` span overrides in the final artifact
- Verify the rendered PDF with text-block coordinates, not page count alone:
  - inspect the exact target pages
  - confirm each card's left edge stays aligned to the left margin
  - confirm the widest text block stays within the page boundary
- When rebuilding a combined artifact, confirm no source content was dropped by checking the full page count and the presence of each major section after regeneration.
