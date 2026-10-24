# Render Verification + Render-Path Selection

Proven 2026-08-20 rendering the TSC San Diego designer pack (10pp A4, Fleet Atlas
phenotype). Two lessons: which render path a deliverable deserves, and how to
verify a render headlessly when no vision tool exists.

## Which render path a deliverable gets

| Deliverable class | Path |
|---|---|
| Ordinary internal doc, agent-to-agent output | Render script only (ds-md-to-pdf.py or Bell section API) |
| Teammate/principal/external-facing document they will present or design from | ds-genome-transcription FIRST (phenotype confirmation), then a full creative-chain layout pass (designed cover, hero treatment), script render only as the mechanical last step |

principal correction (2026-08-20, after receiving a script-rendered pack): "didn't go
through the design process flow at all... very plug and play old school, but it's
decent." Decent is the floor. A pack a human teammate works from gets the chain.

Render gates still apply: explicit request only; telltale scan before render.

## Headless verification recipe

Never claim "verified" from the render command's exit status. Run probes and read
the numbers:

```bash
pdfinfo out.pdf | grep -E "Pages|Page size"      # page count + trim size
pdftotext out.pdf - | grep -c "key term"         # key content actually present
pdftotext out.pdf - | grep -cE "\|[^|]+\|"       # flattened-table check: want 0
pdftoppm -png -r 60 -f 1 -l 1 out.pdf /tmp/pg    # cover raster
pdftoppm -png -r 60 -f 6 -l 6 out.pdf /tmp/pg6   # one mid-document content page
```

Then sample pixels with PIL (use the venv python that has WeasyPrint, e.g.
`/<workspace>`):

- Cover: dark-navy samples should dominate (~85%+).
- Content pages: light-paper samples should dominate.
- Gold accents render below a coarse 10px sampling grid; verify gold via
  pdftotext (wordmark/title text present) rather than pixel counting.

## Environment fixes (setup state, not tool verdicts)

- WeasyPrint missing from the venv: `pip install weasyprint` into that venv
  (69.x verified on macOS).
- Render script SyntaxError under Python < 3.12: f-string expressions cannot
  contain backslashes on older interpreters. Check with `ast.parse` before
  assuming the markdown is at fault; move the regex call out of the f-string.
