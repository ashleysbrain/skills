# Report Header Box Coverage and Editable Rebuild

Use this when a user approves a specific visual baseline of the 8D report and then asks for a narrow header fix or an editable rebuild.

## Core lesson
If section numbers or similar label text are leaking outside the intended header chip/box, do not treat that as a cosmetic afterthought. It means the header treatment is not fully covering the source text.

## Preferred fix order
1. Treat the approved visual baseline as the source of truth for layout, spacing, and palette.
2. Make the smallest source-level change that preserves that layout.
3. If the report must remain editable, rebuild from the editable source instead of patching the flattened PDF again.
4. Ensure the header chip/background fully contains all label text, including numeric prefixes like `Section 01`.
5. Verify both visually and by PDF text extraction that the leaked label text is gone.

## Pitfalls
- Rebuilding the composition in a way that changes the approved layout
- Fixing the wrong layer when the real issue is chip/background coverage
- Assuming a visually acceptable render is correct without checking text extraction
- Reintroducing the section-number leak while making the file editable

## Useful verification
- PDF text extraction should not contain the removed section-number text.
- The rendered page should still match the approved baseline’s structure and style.
