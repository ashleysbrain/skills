# Telegram Attachment Patterns

This reference captures the handoff pattern for reviewable files in Telegram.

## Core pattern

When the user asks for a file to review in Telegram:
- send a real attachment
- keep the caption short
- avoid pasting a filesystem path as the primary delivery

## Good delivery examples

- `MEDIA:/tmp/review-draft.md`
- `MEDIA:/tmp/review-bundle.zip`
- `MEDIA:/tmp/notes-export.pdf`

## When to package as zip

Use a zip when:
- the user wants a single reviewable bundle
- the attachment would be ambiguous as plain text
- the artifact has supporting files
- the text form risks looking like a link or command instead of a file

Do **not** package into a zip when the user explicitly wants to inspect the files separately; send each file as its own attachment instead.

## Handoff caption pattern

Use one short line like:
- `Attached is the markdown file for review.`
- `I packaged the bundle for Telegram review.`
- `Here is the file attachment you asked for.`

## Avoid

- pasting a raw local path as the only message
- sending a long explanation instead of the file
- claiming the file was attached without verifying send success
- making the user guess which item in chat is the real artifact
- if the user says the result is still a link, resend from a clean local copy with a simple filename/extension and verify it behaves like a native attachment before declaring success

## Review checklist

Before sending:
- confirm the file exists locally
- choose the most review-friendly format
- keep the artifact name obvious
- send as a native attachment
- keep the caption brief
