#!/usr/bin/env python3
"""
the specialist engine Creative Process — PDF Generator
Converts markdown to styled PDF using the specialist engine CSS + weasyprint.

Usage:
    python3 ds-pdf.py <input.md> <output.pdf> [title]

Requirements:
    pip install weasyprint markdown

The CSS applies the specialist engine palette (warm gold accents, clean typography,
ultra-thin headings) to match all DS-branded PDFs per genome Ch5.4.
"""
import sys
import subprocess
from pathlib import Path

def markdown_to_html(md_path: str) -> str:
    """Convert markdown to HTML body content."""
    result = subprocess.run(
        ['python3', '-c', f"""
import markdown
with open('{md_path}') as f:
    print(markdown.markdown(f.read(), extensions=['tables', 'fenced_code', 'toc']))
"""],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"python-markdown not available, using fallback", file=sys.stderr)
        return simple_md_to_html(Path(md_path).read_text())
    return result.stdout

def simple_md_to_html(md: str) -> str:
    """Fallback markdown conversion without external deps."""
    import re
    md = re.sub(r'^### (.+)$', r'<h3>\1</h3>', md, flags=re.MULTILINE)
    md = re.sub(r'^## (.+)$', r'<h2>\1</h2>', md, flags=re.MULTILINE)
    md = re.sub(r'^# (.+)$', r'<h1>\1</h1>', md, flags=re.MULTILINE)
    md = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md)
    md = re.sub(r'\*(.+?)\*', r'<em>\1</em>', md)
    md = re.sub(r'```[\s\S]*?\n```', lambda m: f'<pre>{m.group(0)[3:-3]}</pre>', md)
    md = re.sub(r'`(.+?)`', r'<code>\1</code>', md)
    lines = md.split('\n')
    html_lines = []
    in_table = False
    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(set(c) <= set('- :') for c in cells):
                continue
            if not in_table:
                html_lines.append('<table>')
                in_table = True
                html_lines.append('<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>')
            else:
                html_lines.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        else:
            if in_table:
                html_lines.append('</table>')
                in_table = False
            html_lines.append(line)
    if in_table:
        html_lines.append('</table>')
    return '\n'.join(html_lines)

def build_pdf(md_path: str, pdf_path: str, title: str = "Divinity Science"):
    """Convert markdown -> styled HTML -> PDF via weasyprint."""
    from weasyprint import HTML

    body_html = markdown_to_html(md_path)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
/* the specialist engine PDF CSS — Da Vinci Creative Process */
@page {{
    size: A4;
    margin: 2cm 2.5cm;
    @bottom-center {{
        content: "Divinity Science";
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 8pt;
        color: #5a6a8a;
        letter-spacing: 1px;
    }}
    @bottom-right {{
        content: counter(page);
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 8pt;
        color: #5a6a8a;
    }}
}}

body {{
    font-family: 'Helvetica Neue', -apple-system, sans-serif;
    font-size: 10.5pt;
    line-height: 1.7;
    color: #2a2a3a;
}}

h1 {{
    font-size: 22pt;
    font-weight: 200;
    letter-spacing: 0.5px;
    color: #1a1a2e;
    margin-top: 30pt;
    margin-bottom: 8pt;
    border-bottom: 1px solid rgba(232, 213, 160, 0.3);
    padding-bottom: 6pt;
}}

h2 {{
    font-size: 14pt;
    font-weight: 400;
    letter-spacing: 0.3px;
    color: #1a1a2e;
    margin-top: 24pt;
    margin-bottom: 8pt;
}}

h3 {{
    font-size: 11.5pt;
    font-weight: 500;
    color: #2a2a3a;
    margin-top: 18pt;
    margin-bottom: 6pt;
}}

p {{
    margin-bottom: 8pt;
}}

strong {{
    font-weight: 600;
    color: #1a1a2e;
}}

em {{
    font-style: italic;
}}

code {{
    font-family: 'SF Mono', 'Monaco', monospace;
    font-size: 9pt;
    background: rgba(232, 213, 160, 0.08);
    padding: 1px 4px;
    border-radius: 3px;
    color: #4a3a1a;
}}

pre {{
    background: #f8f6f0;
    border: 1px solid rgba(200, 190, 170, 0.15);
    border-radius: 6px;
    padding: 12pt;
    font-size: 8.5pt;
    line-height: 1.5;
    overflow-x: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
}}

pre code {{
    background: none;
    padding: 0;
    color: #2a2a3a;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0;
    font-size: 9.5pt;
}}

th {{
    text-align: left;
    padding: 6pt 8pt;
    border-bottom: 2px solid rgba(232, 213, 160, 0.4);
    font-weight: 500;
    color: #1a1a2e;
}}

td {{
    padding: 6pt 8pt;
    border-bottom: 1px solid rgba(200, 190, 170, 0.12);
    vertical-align: top;
}}

tr:nth-child(even) td {{
    background: rgba(248, 246, 240, 0.5);
}}

hr {{
    border: none;
    border-top: 1px solid rgba(200, 190, 170, 0.2);
    margin: 18pt 0;
}}

tr {{
    page-break-inside: avoid;
}}

h1:first-of-type {{
    margin-top: 0;
    font-size: 28pt;
    border-bottom: 2px solid rgba(232, 213, 160, 0.5);
    padding-bottom: 10pt;
}}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

    HTML(string=html).write_pdf(pdf_path)
    print(f"PDF generated: {pdf_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ds-pdf.py <input.md> <output.pdf> [title]")
        sys.exit(1)
    md_path = sys.argv[1]
    pdf_path = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else "Divinity Science"
    build_pdf(md_path, pdf_path, title)
