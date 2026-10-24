# Raster PDF Surgical Editing

Use this reference when a report PDF must be changed without altering layout, spacing, or hierarchy.

## Source-of-truth rule
- Treat the existing rendered PDF as the baseline artifact.
- Preserve the original geometry and text flow unless the user explicitly asks for redesign.
- Do not rebuild the composition from memory if the baseline can be edited directly.

## Recommended sequence
1. Render the baseline page at high resolution.
2. Identify the exact region that contains only the requested label/text.
3. Sample the local background or surrounding fill color.
4. Cover or remove only the requested region.
5. Re-embed the edited image into the PDF.
6. Re-render and verify that only the requested element changed.

## Practical guardrails
- Prefer exact, minimal substitutions over broad cleanup.
- If multiple attempts drift from the baseline, restart from the baseline artifact instead of layering more fixes.
- If the page is raster-only, assume text-layer editing will not preserve the requested shape.
- If the user says "remove only X" or "don't change formatting," treat any spacing or hierarchy change as a failure.

## Verification
- Compare the edited PDF against the baseline render.
- Confirm the requested text/label is gone.
- Confirm the remaining layout, spacing, and visual balance still match the baseline.
- If possible, inspect the edited region at pixel level to ensure no obvious halo or drift.
