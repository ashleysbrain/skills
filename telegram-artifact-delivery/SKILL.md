---
name: telegram-artifact-delivery
description: Use when sending files, drafts, or review artifacts to Telegram so the recipient gets a real attachment in chat, not a pasted path or bare link.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [telegram, delivery, attachment, review, artifact, file-sharing, productivity]
    related_skills: [telegram-pdf-bundle-delivery, document-debranding-and-link-sanitization, powerpoint, ocr-and-documents]
---

# Telegram Artifact Delivery

## Overview

Use this skill when the user wants to *review a file in Telegram* or receive a draft as a chat attachment.

The goal is simple: send a **real file attachment** that opens cleanly in Telegram and is easy to review. Do not rely on a pasted local path, a raw filesystem string, or a bare markdown link when the user asked for a file.

This is a delivery skill, not a content-writing skill. It governs how the artifact is packaged and sent.

## When to Use

Use this skill when the user asks to:
- send a draft for review in Telegram
- attach a markdown, text, PDF, zip, or other file to chat
- receive the actual file instead of a link
- bundle one or more files for inspection in Telegram
- convert a local artifact into a Telegram-friendly attachment

## What This Skill Is Not

This skill is **not**:
- a document authoring guide
- a file-format conversion spec for every possible target
- a general messaging skill for conversational replies
- a substitute for the user explicitly wanting plain text in chat

## Delivery Principle

If the user asked for a file, deliver a file.

Preferred order:
1. Send the artifact as a native attachment.
2. If the platform is likely to render the text path or filename awkwardly, package the artifact into a cleaner attachment format.
3. If the artifact is a single reviewable text file, keep the review copy simple and named clearly.

## Practical Rules

- Use the `MEDIA:` form with a local file path when sending an attachment.
- Prefer a real local artifact over pasting the contents into chat when the user asked for review by file.
- If a plain text path is likely to be mistaken for a link or looks ambiguous in chat, package the artifact into a zip or another attachment-friendly format first.
- Make the caption short and explicit: say what the file is and that it is attached.
- Do not claim the user received the file unless the send action succeeds.
- For coaching handoffs or future-reference briefs, create a clean local PDF first, verify it exists, then send the PDF and keep the chat message focused on the next-step coaching bullets.
- For executive forwarding packets, remove obvious AI telltales, preserve the user’s preferred terminology, and keep the artifact legible to a human CTO/board reader.
- If the user asks for a reviewable profile or credential document, treat it as a *field-accuracy* pass: preserve the existing structure, make surgical edits only, and verify the updated fields are present before delivery.
- If the user wants a *formatted PDF*, strip markdown/HTML artifacts before export; do not leave raw `**`, `<b>`, `</b>`, or similar markup in the rendered PDF text.
- After generating a PDF from markdown or other source text, verify the extracted text matches the requested domain/name and does not contain accidental assistant telltales.
- When a PDF is meant for signoff on a specific section (e.g. one agent or one profile), inspect the rendered/extracted text for that section before sending so you can confirm the intended fields changed and unrelated sections stayed untouched.
- If the user wants to *read while they speak* (for example, they are about to send a voice reply), include a concise thread-readable text version alongside the attachment. The text should be short enough to scan quickly; the attachment can carry the fuller version.
- If the artifact was edited upstream in HTML or Markdown and exported to PDF, regenerate the PDF from the source file and verify the rendered PDF text before sending. Check both sides of the change: expected additions are present, and renamed or removed names are absent from the attachment itself.

## Document Versioning Convention (Mandatory)

All PDF deliverables sent to Telegram MUST use versioned filenames. Generic names like "morning brief" or "thesis.pdf" are unacceptable.

**Format:** `{DOC_TYPE}_v{MAJOR}.{MINOR}_{YYYY-MM-DD}T{HHMM}.pdf`

**Document type prefixes:**
- `THESIS` — Product thesis, strategy documents
- `CEO_BRIEF` — principal daily briefs, board briefs (always prefix CEO_ so other panels can have their own briefs)
- `BOARD_BRIEF_{PANEL}` — Panel-specific briefs (e.g., `BOARD_BRIEF_MARKETING`)
- `CHECKLIST` — Action checklists, MVP checklists
- `REVIEW` — Board review outputs
- `SCORECARD` — TWC/8D scoring outputs
- `SPEC` — Technical specifications
- `TALENT` — Talent requests, agent profiles
- `FOUNDER_NARRATIVE` — Founder story documents

**Examples:**
- `THESIS_v1.0_2026-06-10T1145.pdf`
- `CEO_BRIEF_v1.0_2026-06-10T0600.pdf`
- `BOARD_BRIEF_MARKETING_v1.0_2026-06-10T1000.pdf`
- `FOUNDER_NARRATIVE_v1.0_2026-06-10T1230.pdf`

**Version rules:** Major (vX.0) = fundamental restructure. Minor (vX.Y) = updates within same scope. Patch (vX.Y.Z) = typo fixes only.

**Auto-versioning:** Check if a vX.0 for this date already exists. If yes, increment minor. First of its kind today = v1.0.

## Verification Checklist

For PDF review artifacts, do a quick text check before sending:
- confirm the target name/section appears in the PDF text
- confirm the revised phrases appear in the PDF text
- confirm the original structure is intact and only the intended section changed
- confirm the filename follows the versioning convention above
- only then attach the PDF in chat


## Support Files

- `references/coaching-handoff-packaging.md` — concise packaging pattern for review briefs that need both a durable PDF and a Telegram coaching handoff.
- `references/clean-executive-packet-pattern.md` — hygiene checklist for voice-note-derived forwarding packets (terminology, AI-tell removal, PDF verification).
- `references/pdf-review-verification.md` — quick verification checklist for regenerated PDFs made from editable source files.

## Common Pitfalls

1. **Pasting a local path into chat**
   - Fix: send the file itself as an attachment.

2. **Sending a bare link when the user asked for a file**
   - Fix: use a local artifact and attach it.

3. **Using a format that is hard to review in Telegram**
   - Fix: package it more cleanly, often as a zip or another native attachment.

4. **Forgetting the review use case**
   - Fix: keep the file name obvious and the caption minimal.

5. **IMAGE DELIVERY FAILURES — MEDIA: renders as text or image doesn't appear (2026-08-07)**
   - **Symptom**: You write `MEDIA:/path/to/file.png` and the user says "you didn't send it," "I can't see it," "you're sending the link info but not an actual image," or just "?" — even though the file exists and is valid.
   - **Root cause**: Intermittent. The Telegram gateway sometimes fails to process the MEDIA: directive, especially after multiple deliveries in a single session. PNG files fail more often than JPEG.
   - **Fix sequence (use in order)**:
     1. Ensure the file is JPEG, not PNG. Convert: `img.convert('RGB').save(path, 'JPEG', quality=95)`
     2. Copy to a completely new, unique filename (never reuse a path you already sent).
     3. If still failing, write the file to a different directory (e.g., `<agent-home>/cache/images/` instead of `~/`).
     4. Verify the file exists with `ls -la` and `file` before retrying.
   - **Do NOT**: paste the MEDIA: tag multiple times in a row for the same path. Each retry should use a fresh unique path.
   - **JPEG over PNG**: JPEG delivers more reliably on Telegram for photographic/complex images. PNG works for screenshots and simple graphics but is unreliable for processed photo output.

6. **Showing a result on desktop when the user is mobile (2026-07-18)**
   - **Symptom**: The user asks to "see" or "show me" something, and you open it in a desktop browser or take a desktop screenshot — but the user is on their phone and the desktop is invisible to them.
   - **Signal**: The user says "send it to telegram," "I'm working off there," "I can't see this," or you know from context they're not at the computer.
   - **Fix**: Deliver the content TO Telegram via `hermes send --to telegram "<message>"`. If the user needs a link, put the link INSIDE the Telegram message text so they can tap it directly. The the operator agent desktop UI is not a delivery channel when the user is on their phone.
   - **When they want a visual preview** (e.g., "show me the mobile interface"): take a screenshot on the desktop, then send the screenshot FILE to Telegram via `hermes send --to telegram "MEDIA:/path/to/screenshot.png"`. Do not describe the screenshot — deliver the actual image.

## Quality Bar

A good Telegram delivery:
- visibly behaves like a file in chat
- is easy to open or download
- matches the user’s request for a reviewable artifact
- does not make the user hunt for hidden content

## Support File

See `references/telegram-attachment-patterns.md` for packaging notes, examples, and handoff patterns.
