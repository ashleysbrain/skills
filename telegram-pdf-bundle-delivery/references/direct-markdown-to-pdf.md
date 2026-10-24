# Direct Markdown-to-PDF Fallback Recipe

Use this when the user wants a PDF of a markdown spec and HTML templating is unnecessary or unavailable.

## Reliable path
1. Read the source markdown from an absolute path.
2. Parse basic block types:
   - headings
   - paragraphs
   - bullets
   - numbered lists
   - code fences
   - tables
3. Render with `reportlab.platypus.SimpleDocTemplate`.
4. Keep the document visually simple and mobile-friendly.
5. Verify the result before delivery:
   - file exists
   - file size is non-trivial
   - first bytes are `%PDF-`
6. Deliver via `MEDIA:/absolute/path/to/file.pdf`.

## Practical notes
- Use a centered title block and clear section headings.
- Preserve code blocks with a monospaced font and a shaded background when possible.
- Keep table fonts small enough to fit on phone screens.
- Prefer absolute paths so Telegram delivery is unambiguous.

## Verification snippet
```bash
python - <<'PY'
from pathlib import Path
p = Path('/absolute/path/to/output.pdf')
print(p.exists(), p.stat().st_size)
with p.open('rb') as f:
    print(f.read(5))
PY
```
