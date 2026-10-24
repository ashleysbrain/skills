# ReportLab Layout Alignment Verification

Use this when building PDFs with ReportLab where Table elements serve as visual bars, headers, or colored blocks alongside Paragraph flowables. These two element types use different sizing mechanisms and can silently misalign.

## The problem
- `Paragraph` flowables automatically respect page margins and indent from them.
- `Table` elements size to their `colWidths` parameter, which is independent of page margins.
- If `colWidths` are hardcoded (e.g., `5.8*inch`), they will not match the actual content area when margins differ, causing bars to appear narrower or wider than the text block.

## The fix
```python
from reportlab.lib.pagesizes import letter

PAGE_W = letter[0]  # 612 pt
LEFT_M = 2.5 * cm
RIGHT_M = 2.5 * cm
USABLE = PAGE_W - LEFT_M - RIGHT_M  # ~465pt

# Use USABLE for every Table:
# Full-width single bar:
bar = Table([[content]], colWidths=[USABLE])

# Multi-column bar (columns must sum to USABLE):
bar = Table([[num, title, time]], colWidths=[0.6*inch, USABLE - 0.6*inch - 1.0*inch, 1.0*inch])

# Evidence key-value rows:
kv = Table([[label, value]], colWidths=[1.4*inch, USABLE - 1.4*inch])
```

## Verification with PyMuPDF
After building the PDF, verify alignment programmatically:
```python
import fitz
doc = fitz.open('output.pdf')
page = doc[0]  # check first content page

# All filled rectangles should share the same x-start and x-end
drawings = page.get_drawings()
for d in drawings:
    fill = d.get('fill')
    rect = d.get('rect')
    if fill and rect:
        width = rect[2] - rect[0]
        print(f'fill={fill} x={rect[0]:.1f} to {rect[2]:.1f} (width={width:.1f})')

# Body text blocks should sit inside the bar boundaries
blocks = page.get_text('dict')['blocks']
for b in blocks[:5]:
    if b['type'] == 0:
        bbox = b['bbox']
        print(f'text x={bbox[0]:.1f} to {bbox[2]:.1f}')
```

All rectangles and text blocks should share consistent x-start (~margin) and x-end (~page_width - margin) values.
