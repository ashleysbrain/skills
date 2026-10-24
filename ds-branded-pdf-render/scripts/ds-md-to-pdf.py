#!/usr/bin/env python3
"""DS branded markdown-to-PDF renderer. Fleet Atlas palette, WeasyPrint.
Usage: python3 ds-md-to-pdf.py <input.md> <title> <subtitle> <output.pdf>"""
import re, os, sys
from datetime import datetime

def inline_fmt(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text

def is_sep(cells): return all(re.match(r'^[-:\s]+$', c) for c in cells)
def parse_row(l):
    l = l.strip()
    if l.startswith('|'): l = l[1:]
    if l.endswith('|'): l = l[:-1]
    return [c.strip() for c in l.split('|')]

def table_html(lines):
    rows = [parse_row(l) for l in lines if '|' in l]
    if not rows: return ''
    h = rows[0]; d = [r for r in rows[1:] if not is_sep(r)]
    s = '<table class="ds-table"><thead><tr>' + ''.join(f'<th>{inline_fmt(c)}</th>' for c in h) + '</tr></thead><tbody>'
    for r in d: s += '<tr>' + ''.join(f'<td>{inline_fmt(c)}</td>' for c in r) + '</tr>'
    return s + '</tbody></table>'

def md_to_body(md):
    md = re.sub(r'^# .+\n', '', md, count=1)
    codes = []
    def stash(m):
        codes.append(m.group(2)); return f'\x00C{len(codes)-1}\x00'
    md = re.sub(r'```(\w*)\n(.*?)```', stash, md, flags=re.DOTALL)
    out = []; lines = md.split('\n'); i = 0
    while i < len(lines):
        s = lines[i].strip()
        if '|' in s and i+1 < len(lines) and '|' in lines[i+1].strip() and not is_sep(parse_row(s)):
            tl = [s]; j = i+1
            while j < len(lines) and '|' in lines[j].strip(): tl.append(lines[j].strip()); j += 1
            out.append(table_html(tl)); i = j; continue
        if s.startswith('### '): out.append(f'<h3>{inline_fmt(s[4:])}</h3>'); i+=1; continue
        if s.startswith('## '): out.append(f'<h2>{inline_fmt(s[3:])}</h2>'); i+=1; continue
        if re.match(r'^-{3,}$', s): out.append('<hr>'); i+=1; continue
        if s.startswith('- ') or s.startswith('* '):
            items = []
            while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                items.append(f'<li>{inline_fmt(lines[i].strip()[2:])}</li>'); i+=1
            out.append('<ul>'+''.join(items)+'</ul>'); continue
        if re.match(r'^\d+\.\s', s):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                plain = re.sub(r"^\d+\.\s*", "", lines[i].strip()); items.append(f'<li>{inline_fmt(plain)}</li>'); i+=1
            out.append('<ol>'+''.join(items)+'</ol>'); continue
        if not s: i+=1; continue
        pl = [s]; j = i+1
        while j < len(lines):
            n = lines[j].strip()
            if not n or n.startswith('#') or n.startswith('- ') or n.startswith('* ') or re.match(r'^\d+\.\s',n) or re.match(r'^-{3,}$',n) or ('|' in n and j+1<len(lines) and '|' in lines[j+1]): break
            pl.append(n); j+=1
        out.append(f'<p>{inline_fmt(" ".join(pl))}</p>'); i=j
    body = '\n'.join(out)
    for idx, c in enumerate(codes):
        body = body.replace(f'\x00C{idx}\x00', f'<pre><code>{c.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")}</code></pre>')
    return body

def build(title, subtitle, md):
    now = datetime.now().strftime('%B %d, %Y')
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title}</title><style>
@page{{size:A4;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;color:#1a2e2e;font-size:11px;line-height:1.65;background:#fff}}
.cover{{background:linear-gradient(135deg,#0a1e2e 0%,#0d3b3b 40%,#062323 100%);min-height:297mm;width:210mm;page-break-after:always;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}}
.cover::before{{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:radial-gradient(circle at 30% 40%,rgba(255,215,0,0.08) 0%,transparent 50%),radial-gradient(circle at 70% 60%,rgba(0,168,150,0.06) 0%,transparent 50%)}}
.cc{{text-align:center;z-index:1;padding:40px}}
.dm{{color:#ffd700;font-size:14px;letter-spacing:8px;font-weight:700;margin-bottom:30px;padding-bottom:15px;border-bottom:1px solid rgba(255,215,0,0.3);display:inline-block}}
.ct{{color:#fff;font-size:52px;font-weight:200;letter-spacing:-1.5px;margin-bottom:8px;line-height:1.1}}
.cs{{color:#4ad6b4;font-size:16px;font-weight:300;letter-spacing:2px;margin-bottom:8px}}
.cd{{color:rgba(255,255,255,0.4);font-size:12px;margin-top:50px}}
.cv{{color:rgba(74,214,180,0.5);font-size:10px;margin-top:8px;font-family:'Courier New',monospace}}
.page{{padding:45px 50px}}
h2{{color:#0a3b3b;font-size:17px;font-weight:700;margin-top:28px;margin-bottom:10px;padding-bottom:6px;border-bottom:2px solid #ffd700;page-break-after:avoid}}
h2:first-of-type{{margin-top:0}}
h3{{color:#0d8b6e;font-size:12.5px;font-weight:700;margin-top:16px;margin-bottom:6px;page-break-after:avoid}}
p{{font-size:10.5px;color:#37474f;line-height:1.7;margin-bottom:8px}}
strong{{color:#0a3b3b;font-weight:700}}em{{color:#0d8b6e;font-style:italic}}
code{{background:#f0f6f4;color:#0a3b3b;padding:1px 5px;border-radius:3px;font-family:'Courier New',monospace;font-size:9.5px;border:1px solid #d8e8e4}}
pre{{background:#062323;color:#4ad6b4;padding:14px 18px;border-radius:6px;overflow-x:auto;margin:10px 0;page-break-inside:avoid;border-left:3px solid #0d8b6e}}
pre code{{background:none;border:none;color:#4ad6b4;padding:0;font-size:9px;line-height:1.5}}
.ds-table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:9px;page-break-inside:avoid}}
.ds-table thead{{background:#0a1e2e}}.ds-table th{{color:#ffd700;padding:7px 9px;text-align:left;font-weight:700;font-size:8.5px;letter-spacing:0.5px;text-transform:uppercase;border:1px solid #0d3b3b}}
.ds-table td{{padding:6px 9px;border:1px solid #d8e8e4;color:#37474f;vertical-align:top;line-height:1.5}}
.ds-table tbody tr:nth-child(even){{background:#f7fbfa}}
ul,ol{{margin-left:22px;margin-bottom:10px}}li{{font-size:10.5px;color:#37474f;line-height:1.7;margin-bottom:4px}}
hr{{border:none;border-top:1px solid #d8e8e4;margin:20px 0}}</style></head><body>
<div class="cover"><div class="cc"><div class="dm">DIVINITY SCIENCE</div><h1 class="ct">{title}</h1><div class="cs">{subtitle}</div><div class="cd">{now}</div><div class="cv">DS-ECS &middot; &phi;=1.618034</div></div></div>
<div class="page">{md_to_body(md)}</div></body></html>'''

if __name__ == '__main__':
    md_path, title, subtitle, pdf_path = sys.argv[1:5]
    md = open(md_path).read()
    h = build(title, subtitle, md)
    hp = pdf_path.replace('.pdf','.html'); open(hp,'w').write(h)
    from weasyprint import HTML; HTML(filename=hp).write_pdf(pdf_path)
    print(f"PDF: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
