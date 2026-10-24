#!/usr/bin/env python3
"""
print_friendly.py — Shared module for generating print-friendly PDFs.

Every DS PDF generator imports this to automatically produce a pure-white
print version alongside the screen version. No separate script or cron needed.

Usage from any generator:

    from print_friendly import render_print_pdf, generate_dual_pdf
    generate_dual_pdf(html_string, screen_path, print_path)

Wiring into a new generator (add at the end of your build function):

    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ds-wave-shared', 'scripts'))
    from print_friendly import render_print_pdf, print_path_for
    render_print_pdf(html_string, print_path_for(output_path))
"""

import os
import re

# The print CSS that actually works.
# CRITICAL: must override CSS *variables* (--cream, --surface, etc) at :root
# AND kill gradients/rgba/var() usages. The naive `background: white
# !important` alone leaves var(--surface) tinted surfaces intact in
# WeasyPrint, producing the "still off-white" bug.
# Verified: drops tint coverage from ~85% to <0.1% on 125-page documents.
PRINT_CSS = """
<style id="ds-print-mode-force">
/* 1. Override ALL theme variables to pure white */
:root {
  --cream: #ffffff !important;
  --surface: #ffffff !important;
  --surface-alt: #ffffff !important;
  --card: #ffffff !important;
  --card-alt: #ffffff !important;
  --bg: #ffffff !important;
  --bg-alt: #ffffff !important;
  --background: #ffffff !important;
  --border: #cccccc !important;
  --border-light: #dddddd !important;
}
/* 2. Kill ALL backgrounds universally (catches var(), rgba, gradients, inline) */
* {
  background: #ffffff !important;
  background-color: #ffffff !important;
  background-image: none !important;
}
body, html {
  background: #ffffff !important;
  background-color: #ffffff !important;
  background-image: none !important;
}
/* 3. Darken text that was designed for tinted/dark backgrounds */
[style*="color:#fff"], [style*="color:#ffffff"],
[style*="color: #fff"], [style*="color: #ffffff"],
[style*="color:white"], [style*="color: white"] {
  color: #1a1a2e !important;
}
[style*="color:#ffd700"], [style*="color: #ffd700"],
[style*="color:gold"] {
  color: #806000 !important;
}
[style*="color:#8a6d1f"], [style*="color: var(--gold)"] {
  color: #5a4400 !important;
}
[style*="color:#2d6867"], [style*="color: var(--teal)"] {
  color: #1a4040 !important;
}
[style*="color:#4ad6b4"], [style*="color: #4ad6b4"] {
  color: #0a3b3b !important;
}
/* 4. Ensure print-friendly table rows and code blocks */
tr:nth-child(even) td {
  background: #f8f8f8 !important;
}
pre, code {
  background: #f5f5f5 !important;
  color: #1a1a2e !important;
}
</style>
"""


def inject_print_css(html: str) -> str:
    """
    Take any HTML string and return a print-friendly version.

    Injects the aggressive CSS that overrides theme variables and kills
    all backgrounds, then strips inline background declarations that
    survived (catches var(), gradients, rgba).
    """
    if '</head>' in html:
        html = html.replace('</head>', PRINT_CSS + '</head>', 1)
    else:
        html = PRINT_CSS + html

    html = re.sub(r'background-image\s*:\s*[^;"}]+;?', '', html)
    html = re.sub(
        r'background\s*:\s*(?:var\([^)]+\)|#[0-9a-fA-F]+'
        r'|linear-gradient\([^)]+\)|radial-gradient\([^)]+\)'
        r'|rgba?\([^)]+\))\s*;?',
        '', html
    )

    return html


def render_print_pdf(html: str, output_path: str) -> str:
    """
    Render a print-friendly PDF from an HTML string.

    Args:
        html: The same HTML used for the screen PDF.
        output_path: Where to save the print PDF.

    Returns:
        The output path.
    """
    from weasyprint import HTML

    print_html = inject_print_css(html)
    HTML(string=print_html).write_pdf(output_path)
    print(f"  Print PDF: {output_path} ({os.path.getsize(output_path):,} bytes)")
    return output_path


def generate_dual_pdf(html: str, screen_path: str, print_path: str | None = None) -> tuple:
    """
    Generate both screen and print PDFs from one HTML string.

    Args:
        html: The full HTML document string.
        screen_path: Output path for the normal (screen) PDF.
        print_path: Output path for the print PDF.
                    If None, derives from screen_path (inserts -PRINT before .pdf).

    Returns:
        (screen_path, print_path) tuple.
    """
    from weasyprint import HTML

    HTML(string=html).write_pdf(screen_path)
    print(f"  Screen PDF: {screen_path} ({os.path.getsize(screen_path):,} bytes)")

    if print_path is None:
        print_path = print_path_for(screen_path)

    render_print_pdf(html, print_path)

    return screen_path, print_path


def print_path_for(screen_path: str) -> str:
    """Derive the standard print PDF path from a screen PDF path."""
    base, ext = os.path.splitext(screen_path)
    return f"{base}-PRINT{ext}"


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: print_friendly.py <input.html> <output-print.pdf>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        html = f.read()
    render_print_pdf(html, sys.argv[2])
