# PDF Review Verification Checklist

Use this when a review artifact is edited in HTML/Markdown and then exported to PDF for Telegram delivery.

## Checklist

- Regenerate the PDF from the source file after edits.
- Verify the rendered PDF, not just the source HTML.
- Confirm the expected replacements are present in the PDF text.
- Confirm removed names / old labels are absent from the PDF text.
- Check that the agent label, role label, and operating-rule block all survived export.
- If the user asked for a clean review copy, send the PDF itself via `MEDIA:` rather than a filesystem path.

## Good verification targets

For persona / roster packets, check for:
- renamed agent prefix or canonical label
- removed human names from role lines
- updated introductory rules / blueprint lines
- preserved personality variation blocks
- preserved certification / methodology lines

## Practical note

A source edit is not complete until the exported PDF reflects it. If the PDF is the thing the user will inspect, validate the PDF text directly before sending it.
