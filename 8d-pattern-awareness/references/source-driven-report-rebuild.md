# Source-Driven Report Rebuild

Use this workflow when a report needs layout, label, or header cleanup but the underlying content should stay editable.

## When to use
- You need to remove or rename labels/headers.
- The PDF or flattened output should be regenerated from source.
- The user expects the document to remain editable for future revisions.

## Workflow
1. Edit the source document, not the flattened PDF.
2. Remove unwanted headers, labels, or boilerplate in the source.
3. Regenerate the PDF or rendered artifact from the edited source.
4. Verify the regenerated text no longer contains the removed labels.
5. If the user asked for an exact reproduction of an approved artifact, use the golden-master reproduction workflow instead.

## Pitfalls
- Do not keep patching flattened output for recurring structural changes.
- Do not assume a visual change is complete until the extracted text is rechecked.
- If a layout fix is only cosmetic, prefer source edits plus regeneration over manual post-processing.
