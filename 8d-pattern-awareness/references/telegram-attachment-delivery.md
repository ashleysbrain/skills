# Telegram attachment delivery for review artifacts

When the user asks to see the actual markdown/document in Telegram, package the artifact as a `.zip` and send the zip attachment rather than relying on a raw `.md` file path alone.

Why:
- The zip is easier for the user to open and review reliably.
- It preserves the exact file contents without format surprises.
- It works well for skill review cycles where the user wants to inspect the real document.

Pattern:
1. Copy the latest markdown into a temporary review folder or file.
2. Create a zip that contains the markdown file with a clear filename.
3. Deliver the zip as the Telegram attachment.
4. If the user asks for the document itself, reference the attached zip, not a link.
