#!/usr/bin/env python3
"""Generate a daily responsibilities PDF with AISHA-MD amber/sienna styling.

Usage: gen_daily_pdf.py <input.md> <output.pdf>

Minimal markdown->HTML converter tailored to the daily responsibilities template
(H1/H2/H3, blockquotes, checkbox lists, pipe tables, inline bold/italic/code/strike,
horizontal rules). Renders via weasyprint with the canonical amber/sienna palette.

This script is designed to be copied to /tmp/gen_daily_pdf.py by the 10 AM
post-standup cron job — /tmp/ is ephemeral so expect to (re)install it every run.

Requires: pip install weasyprint
"""
import sys
import re
from pathlib import Path

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("ERROR: weasyprint not installed. Run: pip install weasyprint", file=sys.stderr)
    sys.exit(1)


def md_to_html(md_text: str) -> str:
    """Minimal markdown-to-HTML converter tailored to the responsibilities format."""
    lines = md_text.split("\n")
    html_parts = []
    in_table = False
    in_list = False
    table_header_done = False

    def close_list():
        nonlocal in_list
        if in_list:
            html_parts.append("</ul>")
            in_list = False

    def close_table():
        nonlocal in_table, table_header_done
        if in_table:
            html_parts.append("</table>")
            in_table = False
            table_header_done = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Headings
        if stripped.startswith("# "):
            close_list(); close_table()
            html_parts.append(f"<h1>{escape(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            close_list(); close_table()
            html_parts.append(f"<h2>{escape(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            close_list(); close_table()
            html_parts.append(f"<h3>{escape(stripped[4:])}</h3>")
        # Blockquote
        elif stripped.startswith(">"):
            close_list(); close_table()
            q = stripped.lstrip(">").strip()
            html_parts.append(f"<blockquote>{inline(q)}</blockquote>")
        # Tables
        elif "|" in stripped and stripped.startswith("|"):
            close_list()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # Separator row like |---|---|
            if all(re.match(r"^:?-+:?$", c) for c in cells if c):
                i += 1
                continue
            if not in_table:
                html_parts.append("<table>")
                in_table = True
                table_header_done = False
            tag = "th" if not table_header_done else "td"
            row = "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells)
            html_parts.append(f"<tr>{row}</tr>")
            table_header_done = True
        # Checkbox list
        elif stripped.startswith("- [ ]") or stripped.startswith("- [x]") or stripped.startswith("- [X]"):
            close_table()
            if not in_list:
                html_parts.append("<ul class='checklist'>")
                in_list = True
            checked = "checked" if stripped[3].lower() == "x" else ""
            text = stripped[5:].strip()
            box = "☑" if checked else "☐"
            html_parts.append(f"<li class='{'done' if checked else ''}'><span class='box'>{box}</span> {inline(text)}</li>")
        elif stripped.startswith("- "):
            close_table()
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{inline(stripped[2:])}</li>")
        elif stripped == "---":
            close_list(); close_table()
            html_parts.append("<hr>")
        elif stripped == "":
            close_list(); close_table()
        else:
            close_list(); close_table()
            html_parts.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_list(); close_table()
    return "\n".join(html_parts)


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s: str) -> str:
    s = escape(s)
    # Bold
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    # Italic (single-asterisk, not matching bold)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    # Inline code
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    # Strikethrough
    s = re.sub(r"~~(.+?)~~", r"<del>\1</del>", s)
    return s


CSS_STYLES = """
@page {
    size: Letter;
    margin: 0.75in 0.75in 0.75in 0.75in;
    @bottom-center {
        content: "AISHA-MD · Daily Responsibilities · page " counter(page) " of " counter(pages);
        font-family: Georgia, serif;
        font-size: 8pt;
        color: #8B4513;
    }
}
body {
    font-family: Georgia, "Palatino Linotype", serif;
    color: #3b2a1a;
    font-size: 10.5pt;
    line-height: 1.45;
    background: #fdf8f2;
}
h1 {
    font-family: "Helvetica Neue", Arial, sans-serif;
    color: #A0522D;
    border-bottom: 3px solid #D2691E;
    padding-bottom: 6px;
    margin-top: 0;
    font-size: 22pt;
    letter-spacing: 0.5px;
}
h2 {
    font-family: "Helvetica Neue", Arial, sans-serif;
    color: #8B4513;
    background: linear-gradient(90deg, #FFE4B5 0%, #fdf8f2 100%);
    padding: 6px 10px;
    border-left: 4px solid #CD853F;
    margin-top: 22px;
    margin-bottom: 10px;
    font-size: 13pt;
    text-transform: uppercase;
    letter-spacing: 1px;
}
h3 {
    color: #A0522D;
    font-size: 11.5pt;
    margin-top: 16px;
    margin-bottom: 6px;
}
blockquote {
    border-left: 4px solid #D2691E;
    background: #FFF8DC;
    padding: 8px 14px;
    margin: 10px 0;
    font-style: italic;
    color: #5a3a20;
}
ul {
    padding-left: 1.2em;
    margin-top: 4px;
    margin-bottom: 8px;
}
ul.checklist {
    list-style: none;
    padding-left: 0.4em;
}
ul.checklist li {
    margin: 3px 0;
    padding: 2px 4px;
}
ul.checklist li .box {
    color: #D2691E;
    font-size: 12pt;
    margin-right: 6px;
}
ul.checklist li.done {
    color: #8B7355;
    text-decoration: line-through;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 8px 0 14px 0;
    font-size: 9.5pt;
}
th {
    background: #D2691E;
    color: #fff;
    padding: 6px 10px;
    text-align: left;
    border: 1px solid #A0522D;
}
td {
    padding: 5px 10px;
    border: 1px solid #DEB887;
    background: #FFF8DC;
}
tr:nth-child(even) td {
    background: #FAEBD7;
}
hr {
    border: none;
    border-top: 1px dashed #CD853F;
    margin: 14px 0;
}
strong { color: #8B4513; }
em { color: #A0522D; }
code {
    background: #FFE4B5;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: "SF Mono", Consolas, monospace;
    font-size: 9.5pt;
    color: #5a3a20;
}
p { margin: 6px 0; }
"""


def main():
    if len(sys.argv) != 3:
        print("Usage: gen_daily_pdf.py <input.md> <output.pdf>", file=sys.stderr)
        sys.exit(1)
    md_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2])
    md_text = md_path.read_text(encoding="utf-8")
    body_html = md_to_html(md_text)
    html_doc = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Daily Responsibilities</title></head>
<body>{body_html}</body></html>"""
    HTML(string=html_doc).write_pdf(str(pdf_path), stylesheets=[CSS(string=CSS_STYLES)])
    print(f"Wrote {pdf_path}")


if __name__ == "__main__":
    main()
