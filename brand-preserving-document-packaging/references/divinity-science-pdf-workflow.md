# Divinity Science PDF workflow notes

## Session-learned patterns

### Direct HTML to WeasyPrint (no pandoc)
When composing structured content (plans, meeting prep, ops docs), write HTML directly rather than converting through pandoc. Faster and gives pixel-level control.

**Pattern (learned 2026-06-08):**
1. Write branded HTML to `/tmp/ds-doc.html`
2. Render: `weasyprint /tmp/ds-doc.html /output/path/DS-Title-2026-06-08.pdf`
3. Clean up: `rm /tmp/ds-doc.html`
4. Verify: check file exists and size is non-trivial (50-100KB typical for a plan doc)
5. Deliver: `MEDIA:/output/path/DS-Title-2026-06-08.pdf` via Telegram

**What works for DS branding:**
- Black-and-white palette. No blue. No generic corporate colors. Clean and restrained.
- Helvetica/Arial body at 11pt. Strong heading hierarchy (22pt title, 15pt h2, 12pt h3).
- @page footer: "Divinity Science — Confidential" in 8pt grey.
- Callout boxes: light grey background, black left border (not colored).
- Tables: subtle grey header row, light row dividers.
- No logos needed for internal docs. The typography and restraint IS the brand.

**Filename convention:** `DS-{DocumentTitle}-{YYYY-MM-DD}.pdf`
- Date always in the filename
- DS prefix for Divinity Science docs
- No spaces, use hyphens

**Rendering results (2026-06-08):**
- Marketing Ops Plan: 62,805 bytes (clean, 1-section doc)
- Meeting Prep Designers: 98,971 bytes (denser, multiple workflow sections)
- Both rendered without errors via weasyprint

### Pandoc → HTML → WeasyPrint (for long-form markdown)
When the source is raw markdown that needs conversion:
1. `pandoc` for markdown to HTML conversion
2. Wrap in branded HTML shell
3. WeasyPrint for PDF rendering
4. Verify with `pypdf` for page count and file size

This is the path for reports and specs that start as markdown files. Use the direct HTML path for docs you are composing from scratch.

## AI telltale removal checklist
Before finalizing any DS document, scan for:
- Em-dashes (—) — replace with commas, colons, or periods
- "Furthermore", "Moreover", "Additionally", "In conclusion" — remove entirely
- Perfectly balanced three-item lists in every paragraph — break the pattern
- Double spaces — collapse to single
- Markdown artifacts (#, **, *, |, ---) — these should never appear in a PDF
- Raw HTML tags visible in text — means the template has a bug
- "As an AI", "I'd be happy to", "Let me know if" — strip all AI voice

## Verification
- Confirm the PDF file exists
- Check file size is proportional to content (not 0 bytes, not suspiciously tiny)
- Check page count
- Open or inspect the first page to confirm branded styling
- Confirm the filename has a date
- Confirm no AI telltales in the content
