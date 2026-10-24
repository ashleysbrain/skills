# Clean PDF Export Checklist

Use this when converting markdown or draft text into a Telegram-ready PDF.

## Checklist
- Remove markdown markers before PDF generation.
- Do not allow raw HTML tags to appear in the rendered PDF text.
- Prefer plain text headings and bullets over literal markup.
- Verify the PDF with text extraction before sending.
- Confirm the title/domain matches the user’s current request.
- If the user corrected the subject matter, update the source text before regenerating the PDF.

## Quick verification patterns
- Search extracted text for `**`, `<b>`, `</b>`, `<i>`, `</i>`.
- Search extracted text for stale subject names from earlier drafts.
- Confirm the file is the requested attachment type and opens cleanly in Telegram.
