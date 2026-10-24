# Compact PDF from Markdown Source — Proven Pipeline

## Session: 2026-06-07
## Source: 8D360 Competitive Landscape Report (210 pages, US Letter)

## Problem
User asked to reduce a 210-page PDF to fewer pages without deleting any content. The PDF was generated from markdown with pandoc + weasyprint using 2.5cm margins and ~10pt body font.

## Solution
Rebuild from markdown source with compact CSS instead of N-up imposition.

### Pipeline
```bash
cd /<workspace>

pandoc 8D360-Competitive-Landscape-Report-2026-06-06.md \
  -f markdown+pipe_tables -t html5 \
  --standalone --embed-resources \
  --metadata "title=8D360 Competitive Landscape Report" | \
  python3 -c "
import sys
html = sys.stdin.read()
css = '''
@page { size: letter; margin: 0.4in 0.5in 0.4in 0.5in; }
body { font-family: 'Hiragino Sans','Helvetica Neue',Arial,sans-serif;
       font-size: 7.5pt; line-height: 1.25; color: #1a1a1a; }
h1 { font-size: 13pt; margin-top: 12pt; margin-bottom: 4pt; font-weight: 700;
     color: #0d1b2a; border-bottom: 1.5pt solid #0d1b2a; padding-bottom: 3pt; }
h2 { font-size: 10pt; margin-top: 10pt; margin-bottom: 3pt; font-weight: 700;
     color: #1b263b; }
h3 { font-size: 8.5pt; margin-top: 8pt; margin-bottom: 2pt; font-weight: 700;
     color: #415a77; }
p { margin-top: 2pt; margin-bottom: 2pt; }
ul, ol { margin-top: 2pt; margin-bottom: 2pt; padding-left: 14pt; }
li { margin-bottom: 1pt; }
blockquote { margin: 4pt 0; padding: 3pt 8pt; border-left: 2pt solid #415a77;
             background: #f8f9fa; font-size: 7pt; }
table { border-collapse: collapse; width: 100%; margin: 3pt 0; font-size: 7pt; }
th { background: #0d1b2a; color: white; padding: 2pt 4pt; font-weight: 700;
     text-align: left; }
td { padding: 2pt 4pt; border-bottom: 0.5pt solid #ddd; vertical-align: top; }
img { max-width: 100%; max-height: 120pt; margin: 3pt 0; }
hr { border: none; border-top: 0.5pt solid #ccc; margin: 6pt 0; }
'''
html = html.replace('</head>', f'<style>{css}</style></head>')
print(html)
" > /tmp/compact.html

weasyprint /tmp/compact.html /<workspace>
```

### Results
- **Original**: 210 pages, ~1.2MB, margins 2.5cm, body font 9.5–10.5pt
- **Compact**: 78 pages, ~30MB, margins 0.4in, body font 7.0–7.5pt
- **Reduction**: 63% fewer pages, all content and 40 inline images preserved
- **Readability**: 7.5pt is readable on screen; minimum usable body font is ~7pt

### Key decisions
- Chose CSS rebuild over N-up imposition because N-up at 2-up would produce ~105 pages at ~5pt effective font (borderline unreadable), while CSS rebuild at 7.5pt gives both fewer pages AND better readability.
- Accepted larger file size (30MB vs 1.2MB) because images were kept at full resolution. Trade-off: content fidelity over file size.
- Used `max-height: 120pt` on images to prevent any single image from consuming a full page.

### Verification commands
```python
import fitz
doc = fitz.open("compact.pdf")
print(f"Pages: {doc.page_count}")
# Spot-check font sizes on middle page
page = doc[39]
for b in page.get_text("dict")["blocks"]:
    if b["type"] == 0:
        for line in b["lines"]:
            for span in line["spans"]:
                print(f"  {span['size']:.1f}pt: {span['text'][:50]}")
```
