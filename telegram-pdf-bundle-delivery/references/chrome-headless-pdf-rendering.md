# Chrome Headless PDF Rendering (CSS Grid/Flexbox Support)

When WeasyPrint can't handle your CSS (it doesn't support CSS Grid, Flexbox,
`display: grid`, or modern CSS features), Chrome headless is the best
alternative on macOS. It renders HTML with a real browser engine, so all
CSS works perfectly.

## When to use Chrome over WeasyPrint

| Feature | WeasyPrint | Chrome Headless |
|---------|-----------|-----------------|
| CSS Grid | Not supported | Full support |
| Flexbox | Partial | Full support |
| `background-clip: text` | Not supported | Full support |
| Gradient text | Not supported | Full support |
| Complex card layouts | Partial | Full support |
| `radial-gradient` overlays | Not supported | Full support |
| Installation needed | pip install | Already on macOS |

## Command

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless \
    --disable-gpu \
    --no-sandbox \
    --print-to-pdf=/path/to/output.pdf \
    --print-to-pdf-no-header \
    "file:///absolute/path/to/input.html"
```

Notes:
- `--print-to-pdf-no-header` suppresses Chrome's default URL/date footer
- The `file://` protocol requires an absolute path
- Chrome logs warnings (keychain, display link) to stderr — these are harmless
- Output is A4 portrait by default; control via `@page { size: ... }` in CSS

## Page control in CSS

```css
@page {
    size: A4;
    margin: 0;           /* zero margin for full-bleed cover pages */
}
.page {
    page-break-after: always;
    min-height: 297mm;   /* forces each section to fill a page */
}
```

For sections that should start on a new page:
```css
.page-break {
    page-break-before: always;
}
```

## Verification

After rendering, verify with PyMuPDF (fitz):

```python
import fitz
doc = fitz.open('output.pdf')
print(f'Pages: {len(doc)}')
for i, page in enumerate(doc):
    text = page.get_text()[:80]
    print(f'  Page {i+1}: {text[:60]}...')
doc.close()
```

## Design preferences (user-specific)

The user prefers:
- Dark blue-green backgrounds (#0a1e2e, #0d3b3b) for cover pages
- Gold accents (#ffd700) for numbers and highlights
- Teal/green secondary (#0d8b6e, #4ad6b4)
- Clean typography with light font weights for large titles
- Stats displayed as large gold numbers with small labels

## Known issue: letter-spacing breaks text extraction

Chrome sometimes renders text with CSS `letter-spacing` that breaks string
matching in extracted text. When verifying content in the output PDF via
`page.get_text()`, search for individual words or remove letter-spacing from
critical elements that need to be machine-readable.
