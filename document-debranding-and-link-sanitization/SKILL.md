---
name: document-debranding-and-link-sanitization
description: Remove a person's name, old brand, or renamed canonical term from a document/source package by updating filenames, markdown text, embedded links, source paths, build scripts, and regenerated PDFs, then verify the clean artifact set while preserving archival records unless normalization is explicitly requested.
tags: [documents, pdf, markdown, links, filenames, sanitization, branding, productivity]
version: 1.0.0
---

# Document Debranding and Link Sanitization

Use this when a document, source, or generated package must be cleaned up so it no longer contains a person's name, old brand, renamed product term, or stale path references in filenames, markdown files, PDFs, source docs, build scripts, or document links.

Reference: see `references/canonical-term-renaming-workflow.md` for the bulk-rename checklist and verification pattern.

## When to use
- A PDF or markdown bundle was generated under a personal name, old brand, or deprecated product term and needs to be neutralized
- File names, folder names, or links must be updated to remove a person’s name or old canonical term
- Companion files, templates, and build scripts need path or title updates to match the new neutral naming
- The deliverable must be checked for residual mentions before sending externally or into Telegram
- A document package was renamed and the old branded artifacts should be removed

## Core workflow
1. Inventory every artifact in the package: source markdown, PDF output, build scripts, templates, and any linked or companion files.
2. Search the whole package for the name or branded identifier, including file contents and file names.
3. Search both the full old phrase and any legacy abbreviation/acronym so you do not miss partial rebrands.
4. Update hard-coded paths in build scripts first if they point at the old branded workspace or old canonical term.
5. Rename the workspace and files to the neutral or new canonical naming scheme when the user is requesting a full brand normalization.
6. Update all hard-coded links, titles, captions, references, and any term-specific labels in source files, templates, scripts, and document links.
7. Patch templates/examples separately so future generated files inherit the new canonical name.
8. Regenerate derived outputs such as PDFs after the rename, and rebuild any companion prompt/template files if their paths or titles changed.
9. Preserve archival or historical artifacts unless the user explicitly asks to normalize them too.
10. Remove stale branded artifacts so only the intended clean set remains.
11. Verify the cleanup with both text search and artifact inspection.
12. If the bundle is delivered to Telegram, confirm the `MEDIA:` path points to the neutral artifact name.

## Practical checks
- Search both file contents and file names, not just one or the other
- Update build scripts first if they reference old paths
- Regenerate PDFs after any rename or title change; do not trust old outputs
- Check companion templates and source markdown for leftover names or links
- If a PDF was already built, verify the text layer for residual names before delivery
- If the package is going to Telegram, confirm the delivered `MEDIA:` path points to the neutral file name

## Verification steps
Use at least two checks:
- `search_files` or terminal search across the package for the old name or brand
- PDF text extraction with `pymupdf`/`fitz` or `pypdf` to confirm the rendered output no longer contains the name
- File listing to confirm old branded filenames are gone
- Optional visual inspection if the rename also changed titles or headers

## Common fixes
- Replace hard-coded directory constants in build scripts
- Update markdown links that still point at old file names
- Regenerate PDFs after renaming source markdown so the title page stays consistent
- Delete old branded PDFs and markdowns so only the neutral versions remain
- If a document title should remain generic, remove the personal name from the title page and metadata too

## Pitfalls
- Do not update only the visible document text and forget filenames
- Do not rename the final PDF without rebuilding it if the title or metadata still shows the old name
- Do not leave old artifacts in the directory, since downstream delivery can pick them up by accident
- Do not assume a search miss in one file means the whole package is clean
- Do not forget companion templates or prompt files that may still contain the old brand

## Overlap notes
- `nano-pdf` covers editing existing PDFs, but not full package renaming or link cleanup
- `pdf-table-layout-verification` covers PDF layout and readability, but not debranding or file hygiene
- `telegram-pdf-bundle-delivery` covers packaging for Telegram, but not sanitizing names and paths
- `external-content-qa-pipeline` overlaps on final review, but this skill is specifically about debranding and artifact cleanup

## Output rule
When the cleanup is complete, report the neutral file paths and confirm that the old branded names are gone from both file names and content.
