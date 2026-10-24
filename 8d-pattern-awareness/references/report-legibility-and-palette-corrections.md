# Report Legibility and Palette Corrections

Session-learned guardrails for the 8D user-facing report surface.

## Visual corrections
- Do not keep the content collapsed into the middle of the page.
- Spread the content naturally across the 8.5x11 page while keeping line spacing readable.
- Avoid overly airy line spacing; the page should feel filled, not sparse.
- If the user says the page is too centered or underused, widen the text distribution before trying to compress further.

## Color corrections
- Use the documented Divinity Science palette, not a generic bright yellow.
- Treat gold as a restrained accent, not the main fill color.
- If a rendered color is wrong, re-check the palette source before generating another version.

## Recommendation block behavior
- Dimension recommendations should be regenerated from the current day’s signal map.
- Each dimension card should read like a specialist brain for that dimension, not a static template.
- Keep only the dimensions supported by the current evidence.

## Verification
- Render and inspect the PDF for page fill, line spacing, and palette match.
- Confirm the recommendation cards change when the input signal changes.
