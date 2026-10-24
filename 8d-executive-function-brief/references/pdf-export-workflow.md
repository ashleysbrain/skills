# PDF export workflow for revised 8D briefs

## When to use
Use this note when the user asks for a PDF deliverable of the latest 8D revisions or any public/open-core update that must be shown in a shareable document.

## Required pipeline
1. Build the PDF from the current canonical skill and references, not from memory.
2. If the user wants the latest revisions, export the full content rather than a short abstract unless they explicitly ask for a summary.
3. Render with a local PDF engine that preserves headings and readable body text.
4. Verify the PDF by extracting text from the rendered file and checking that the revised wording is present.
5. Deliver the file in chat with `MEDIA:/absolute/path/to/file.pdf`.

## Verification checks
- Confirm the file exists and is a valid PDF.
- Confirm page count and file size are reasonable for the requested content.
- Extract text from the PDF and search for the revised phrases.
- If the requested wording is missing, regenerate before delivery.

## Pitfalls
- Do not deliver a PDF that is only a lightweight abstract if the user asked to see the latest revisions.
- Avoid stylesheet collisions when using ReportLab defaults; use unique style names.
- Do not treat a successful file write as proof that the content is visible in the PDF; verify by text extraction.
