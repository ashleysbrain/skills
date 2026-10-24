# Printable Math PDF Verification Pattern

Use this reference when producing a research/strategy document that must print cleanly as a PDF and include display math, equations, or code-block-style formula sections.

## Goal

Turn a source document into a print-ready PDF and verify that:

- the math is readable, not collapsed into garbled inline text
- page breaks do not bury equations in awkward places
- title, headings, and section flow remain legible
- metadata or stray fields do not leak into the rendered output

## Recommended workflow

1. Treat the markdown/HTML source as the source of truth.
2. Generate the PDF from that source using the existing local converter/wrapper.
3. Open the PDF and inspect at least:
   - page 1 for title, subtitle, and metadata cleanliness
   - one page containing the densest math section
4. Use both visual inspection and extracted text checks:
   - visual: confirm equations are separated from prose and readable at normal zoom
   - text: confirm the exact phrases that matter for the release narrative and math contract appear in the extracted text
5. If you see stray metadata or layout artifacts, patch the source and regenerate from source again.

## What to look for visually

- Formula blocks should have clear vertical spacing above and below.
- Display equations should not be fused into paragraphs.
- Long equations should wrap safely or be split into multiple lines.
- Section headings should remain distinct from equations.
- Page thumbnails should show the math sections as intentional blocks, not dense noise.

## Common pitfalls

- A YAML author/affiliation field can render as stray text if the template mishandles metadata.
- Overly long single-line formulas can become unreadable when rendered to PDF.
- A document can look fine in markdown but fail in PDF if the converter does not preserve spacing.
- Don’t stop after the PDF opens; verify the rendered math and the extracted text.

## Session-derived example

In the Divinity Science behavioral physics docs, the best result came from:

- writing the source markdown first
- generating the PDF from the markdown
- visually checking a page with layered equations
- patching stray metadata in the source when it appeared in the rendered PDF
- regenerating and rechecking until the math blocks were clean

## Reuse note

This pattern applies to any research brief, whitepaper, launch memo, or meeting handout where mathematical notation must survive into a printable artifact.