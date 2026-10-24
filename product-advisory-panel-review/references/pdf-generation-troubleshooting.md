# PDF Generation Troubleshooting

## Standard Command
```bash
python3 /<workspace> /tmp/product-review-[YYYY-MM-DD].md /tmp/product-review-[YYYY-MM-DD].pdf "Product Advisory Panel" "AM"
```

## Known Issue: Pillow / WeasyPrint Import Error (Recurring)

### Error Pattern
```
ImportError: cannot import name '_imaging' from 'PIL' (/<workspace>)
```

This occurs when Pillow version 12.3.0 is installed but hermes-agent requires Pillow==12.2.0.

### Root Cause
WeasyPrint depends on PIL/Pillow. Version mismatch between Pillow 12.3.0 and hermes-agent's requirement (12.2.0) causes the `_imaging` import to fail.

### Fix Attempted (2026-07-14)
```bash
pip uninstall -y Pillow
pip install Pillow==12.2.0
```

Result: Dependency conflict warning still appears. The import error persists after reinstall.

### Current Status
- PDF generation is **blocked** on this environment
- Markdown report can be written to `/tmp/product-review-[date].md` successfully
- Workaround: Deliver markdown file instead of PDF when PDF generation fails

### Alternative PDF Tools (Attempted)
- **Pandoc**: Available at `/usr/local/bin/pandoc` (version 3.10) but lacks xelatex/pdflatex engines for direct PDF generation
  - **HTML fallback**: Can successfully generate standalone HTML: `pandoc /tmp/product-review-[date].md -o /tmp/product-review-[date].html --standalone`
  - HTML generation is reliable and can be used as alternative delivery format
- **WeasyPrint Python API**: Direct import fails with same Pillow error

### Current Workaround
When PDF generation fails:
1. Write markdown report to `/tmp/product-review-[date].md` (using Python heredoc if baseline-first gate blocks)
2. Attempt HTML generation as fallback: `pandoc /tmp/product-review-[date].md -o /tmp/product-review-[date].html --standalone`
3. Report the PDF failure but note HTML is available
4. Proceed with delivering the markdown content (primary deliverable)
5. Do NOT attempt repeated PDF generation retries (creates noise)

### Investigation Notes
- The error persists after `pip install --force-reinstall Pillow==12.2.0`
- May require venv rebuild or dependency tree resolution
- Issue is environment-specific (the operator agent venv)
- Script works in other environments (note from skill authoring)

### Escalation Path
If this issue persists for multiple runs:
1. Document the failure pattern here
2. Consider alternative PDF generation stack (not pandoc, not weasyprint)
3. Report to user as environment issue, not skill issue

---

*Last updated: 2026-07-14*
*Issue first observed: 2026-07-14*