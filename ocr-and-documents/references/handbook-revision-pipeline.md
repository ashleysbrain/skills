# Handbook Revision Pipeline

Use this pattern when turning source PDFs/DOCX notes into polished handbook deliverables.

## Intake and extraction
- For text PDFs, use `fitz`/PyMuPDF to extract page text quickly.
- For scanned or complex PDFs, prefer an OCR-capable extractor first when available.
- For DOCX files, if `python-docx` is unavailable, unzip the `.docx` and read `word/document.xml` directly with `zipfile` + regex over `<w:t>` nodes.

## Content audit
- Extract the first few pages plus the full page list to identify:
  - role labels that need cleanup
  - title hierarchy and section order
  - contact blocks / owner names
  - any outdated or risky language
- Search the source text for:
  - authority titles (e.g. COO vs Chief of Staff)
  - legal boundaries (“not legal advice”)
  - compliance-sensitive terms
  - excluded terms the user explicitly does not want in the public doc

## Rebuild
- Draft each audience version separately when the user requests multiple doc types:
  - employee
  - intern
  - volunteer
  - crisis/support protocol
- Keep the audience-specific handbook focused on:
  - who it is for
  - expectations
  - support contacts
  - external resources
  - acknowledgment language
- Use a consistent neutral/gold visual theme for executive handbooks when exporting to PDF.

## PDF generation
- Markdown + WeasyPrint is a practical path for fast, polished PDFs.
- Verify the resulting PDF with PyMuPDF:
  - page count
  - first-page text
  - file size
- If a generated PDF looks duplicated on page 1, check whether the title was included both in the markdown body and the HTML wrapper header.

## Packaging and delivery
- When the user wants a complete handoff, create:
  - `.md` source files
  - `.pdf` exports
  - a revision summary
  - a single zip bundle
- Verify the zip exists before claiming completion.
