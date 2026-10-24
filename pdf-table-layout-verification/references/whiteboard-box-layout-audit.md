# Whiteboard / diagram PDF box-fit audit

Session-derived pattern for layout repair on whiteboard-style PDFs where SVG or positioned text must fit inside labeled boxes.

## What to check
- Use a light background and dark text when the user intends to print.
- Verify the exact delivered PDF, not an earlier draft.
- For each box, check that the text bounding boxes stay inside the box bounds.
- If labels are too long, split them across lines before export instead of relying on tiny fonts.
- Keep the first line as the strongest label and move qualifiers to a second line.
- Re-audit after regeneration; do not assume the fix held.

## Practical inspection loop
1. Generate or update the HTML/SVG.
2. Render the PDF.
3. Inspect the page visually.
4. If the page uses SVG text, check the text positions/bounds against the container geometry.
5. Shorten or wrap labels that bleed past the right edge.
6. Rebuild and re-check the final file.

## Common failure mode
- A single long sentence inside a box looks fine in source but overflows in the rendered PDF.
- Fix by breaking the sentence into 2-3 short lines and lowering the font size slightly if needed.
- Always audit the final artifact before sending it to the user.
