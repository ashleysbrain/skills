# WeasyPrint layout pitfalls for report rebuilds

## Symptom
A PDF build can fail with an `AssertionError` from `weasyprint/layout/page.py` complaining about an empty page (`page_is_empty`).

## Observed trigger pattern
- `min-height: 100vh` on the page wrapper
- Nested `display: grid` / `flex` layouts inside the first page
- Complex card layouts that leave WeasyPrint with no printable flow content on page 1

## Reliable fix pattern
1. Remove `min-height: 100vh` from the page wrapper.
2. Convert the highest-level layout containers from grid/flex to normal block flow.
3. Add explicit `margin-top` / `margin-bottom` spacing between sections after flattening the layout.
4. Retry the PDF build.

## Verification
- Regenerate the PDF and confirm a nonzero file size.
- Open the HTML in a browser and inspect the first page visually.
- Use screenshot/vision review if the artifact is meant for team presentation.

## Reproduction note
In the 8D Qubit AI Agent TWC family-algorithms deck, the PDF build succeeded only after flattening `.grid`, `.subgrid`, `.split`, and `.chips` into block flow and removing the page-level `min-height`.
