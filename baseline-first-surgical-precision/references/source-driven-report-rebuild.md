# Source-Driven Report Rebuild

Use this when the user wants a PDF/report corrected *and* wants the result to stay editable for future changes.

## Rule
If the deliverable already exists as a flattened PDF/image and the user asks for a narrow visual/content change that should remain editable later, do not keep layering raster edits unless that is the only viable short-term path. Rebuild from the editable source of truth and regenerate the PDF.

## Workflow
1. Find the original editable source (`.md`, template, HTML, etc.).
2. Apply the requested change in source, not in the rendered output.
3. Keep the page geometry and layout stable unless the user explicitly asks for redesign.
4. Regenerate the PDF from the source.
5. Verify the new PDF text/output to confirm the requested labels/content are gone.
6. Preserve the source file so future edits are straightforward.

## Report-specific note
For the 8D user-facing report workflow, the reusable renderer lives at:
- `scripts/render_user_facing_report.py`

That renderer is the preferred path when the user asks to:
- omit section headers or labels
- keep the report editable
- preserve the existing page structure while changing only the requested text

## Pitfalls
- Editing the flattened PDF when the user explicitly wants future editability
- Redesigning spacing or hierarchy while doing a narrow source change
- Assuming a visually close raster fix is good enough when the source is available
- Forgetting to verify that the regenerated PDF no longer contains the removed labels

## Verification
- Confirm the source file contains the intended edit.
- Confirm the regenerated PDF reflects the source change.
- Confirm the change did not drift the layout unnecessarily.
