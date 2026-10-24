# Telegram artifact resend pattern

Use this pattern when the user says to update and send files again:

- Treat the attached files as the source of truth when the screenshot or message names them explicitly.
- Make the edit in the actual artifact file first.
- Verify the file contents with a search/readback.
- When sending files in Telegram, use the exact file path with `MEDIA:/absolute/path/to/file`.
- If no Telegram home channel is configured, list targets first and send to an explicit target (for example, `telegram:Its Her`).
- Prefer sending the real attachment files over describing them in text.

This is a delivery workaround, not a product rule: it exists so the user receives the actual updated artifacts, not a summary.
