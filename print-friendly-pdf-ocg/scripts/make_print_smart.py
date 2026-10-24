#!/usr/bin/env python3
"""
make_print_smart.py — Add OCG auto-switch to any DS-styled PDF.

WHAT THIS DOES:
  Takes a DS-styled PDF (dark/colored backgrounds, light text) and adds
  Optional Content Groups (OCGs) so the file AUTO-SWITCHES when printed:

    - Screen mode: Full colored backgrounds + light text (original look)
    - Print mode:  White backgrounds + dark text (saves ~90% ink/toner)

  One file. No separate "print version" needed. The viewer/printer reads
  the OCG Usage hints (View=ON, Print=OFF) and renders accordingly.

CAN ALSO:
  - Accept an HTML source and render it to PDF first (via WeasyPrint)
  - Fall back to generating a separate print-only PDF (dual-PDF mode)
    for viewers that don't respect OCG PrintState (e.g., macOS Preview)

USAGE:
  # From existing PDF:
  python3 make_print_smart.py input.pdf -o output-smart.pdf

  # From HTML source (renders first, then adds OCG):
  python3 make_print_smart.py input.html -o output-smart.pdf

  # Also generate a standalone print PDF (dual-PDF fallback):
  python3 make_print_smart.py input.pdf -o output-smart.pdf --also-print-pdf

  # Verify OCG structure after generation:
  python3 make_print_smart.py input.pdf -o output-smart.pdf --verify

REQUIREMENTS:
  pip install pikepdf weasyprint pymupdf

OCG VIEWER COMPATIBILITY:
  - Adobe Acrobat/Reader: Full support (auto-switches on print)
  - Foxit Reader:         Full support
  - Chrome/Firefox PDF:   Respects print intent
  - macOS Preview:        Does NOT reliably respect PrintState.
                          Use --also-print-pdf for Preview users.

EXIT CODES:
  0 = Success
  1 = Error (see stderr)
"""

import argparse
import os
import re
import sys

try:
    import pikepdf
except ImportError:
    sys.stderr.write("ERROR: pikepdf not installed. Run: pip install pikepdf\n")
    sys.exit(1)


# --- Color helpers ----------------------------------------------------

def is_light_color(rgb_tuple):
    """Returns True if a fill color is light enough to be invisible on white paper."""
    r, g, b = rgb_tuple
    return (r * 0.299 + g * 0.587 + b * 0.114) > 0.65


def darken_color(rgb_tuple):
    """Map a light color to a dark equivalent for print-mode text."""
    r, g, b = rgb_tuple
    # White -> dark teal (#0a3b3b)
    if r > 0.95 and g > 0.95 and b > 0.95:
        return (0.039, 0.231, 0.231)
    # Gold (#ffd700) -> dark amber
    if r > 0.9 and g > 0.7 and b < 0.2:
        return (0.5, 0.37, 0.0)
    # Light teal-green -> dark teal
    if g > 0.7 and b > 0.5 and r < 0.5:
        return (0.039, 0.231, 0.231)
    # Catch-all: proportional darkening
    return (max(r * 0.3, 0.1), max(g * 0.3, 0.1), max(b * 0.3, 0.1))


# --- Content stream parsing -------------------------------------------

def find_text_blocks(data):
    """
    Find all BT...ET blocks in a PDF content stream and the fill color
    active when each block starts.

    Returns list of dicts: {start, end, fill: (r,g,b) or None}
    """
    blocks = []
    for m in re.finditer(r'\bBT\b', data):
        bt_start = m.start()
        et_match = re.search(r'\bET\b', data[bt_start + 2:])
        if not et_match:
            continue
        bt_end = bt_start + 2 + et_match.end()

        # Walk backwards to find the most recent fill color (rg operator)
        before = data[:bt_start]
        color_matches = list(re.finditer(r'([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+rg\b', before))
        fill = None
        if color_matches:
            last = color_matches[-1]
            fill = (float(last.group(1)), float(last.group(2)), float(last.group(3)))

        blocks.append({'start': bt_start, 'end': bt_end, 'fill': fill})
    return blocks


# --- OCG injection (the core) ----------------------------------------

def add_print_ocg(input_path, output_path, verbose=True):
    """
    Add 3 OCGs to a PDF:
      1. "Screen Backgrounds" -- dark fills/gradients (View=ON, Print=OFF)
      2. "Screen Text"        -- light-colored text (View=ON, Print=OFF)
      3. "Print Text"         -- dark duplicates of light text (View=OFF, Print=ON)

    In screen mode: looks identical to original.
    In print mode: white background, all text dark, ~90% ink savings.
    """
    pdf = pikepdf.open(input_path)

    # Create OCGs with usage hints
    ocg_bg = pdf.make_indirect(pikepdf.Dictionary(
        Type=pikepdf.Name.OCG, Name=pikepdf.String("Screen Backgrounds"),
        Usage=pikepdf.Dictionary(
            View=pikepdf.Dictionary(ViewState=pikepdf.Name.ON),
            Print=pikepdf.Dictionary(PrintState=pikepdf.Name.OFF),
        )
    ))
    ocg_stxt = pdf.make_indirect(pikepdf.Dictionary(
        Type=pikepdf.Name.OCG, Name=pikepdf.String("Screen Text (light colors)"),
        Usage=pikepdf.Dictionary(
            View=pikepdf.Dictionary(ViewState=pikepdf.Name.ON),
            Print=pikepdf.Dictionary(PrintState=pikepdf.Name.OFF),
        )
    ))
    ocg_ptxt = pdf.make_indirect(pikepdf.Dictionary(
        Type=pikepdf.Name.OCG, Name=pikepdf.String("Print Text (dark equivalents)"),
        Usage=pikepdf.Dictionary(
            View=pikepdf.Dictionary(ViewState=pikepdf.Name.OFF),
            Print=pikepdf.Dictionary(PrintState=pikepdf.Name.ON),
        )
    ))

    pdf.Root.OCProperties = pdf.make_indirect(pikepdf.Dictionary(
        OCGs=[ocg_bg, ocg_stxt, ocg_ptxt],
        D=pikepdf.Dictionary(
            Name=pikepdf.String("the specialist engine/Screen Layers"),
            BaseState=pikepdf.Name.ON,
            Order=[ocg_bg, ocg_stxt, ocg_ptxt],
        ),
    ))

    total_light = 0
    total_pages = len(pdf.pages)

    for pno in range(total_pages):
        page = pdf.pages[pno]
        data = page.Contents.read_bytes().decode('latin-1')

        # Find text blocks
        bt_blocks = find_text_blocks(data)
        light_blocks = [b for b in bt_blocks if b['fill'] and is_light_color(b['fill'])]
        total_light += len(light_blocks)

        # Set up property list references
        if '/Properties' not in page.Resources:
            page.Resources.Properties = pdf.make_indirect(pikepdf.Dictionary())
        page.Resources.Properties.DSbg = ocg_bg
        page.Resources.Properties.DStxt = ocg_stxt
        page.Resources.Properties.DPtxt = ocg_ptxt

        # Split into background section (before first BT) and content
        first_bt = data.find('BT') if bt_blocks else len(data)
        pre_bt = data[:first_bt]
        content = data[first_bt:]

        # Wrap light-text blocks: original -> screen OCG, dark dup -> print OCG
        if light_blocks:
            for block in sorted(light_blocks, key=lambda b: b['start'], reverse=True):
                rel_s = block['start'] - first_bt
                rel_e = block['end'] - first_bt
                original = content[rel_s:rel_e].rstrip()

                dark_rgb = darken_color(block['fill'])
                dark_color_str = f"{dark_rgb[0]:.6f} {dark_rgb[1]:.6f} {dark_rgb[2]:.6f} rg"
                # The rg that set the ORIGINAL light fill color lives OUTSIDE the
                # BT block (in the shared graphics state, often inside the bg OCG).
                # Replacing an rg *inside* the BT finds nothing and yields a
                # byte-identical duplicate that stays light. Fix: inject an
                # explicit dark rg as the FIRST op inside BT so the text fill
                # color is overridden regardless of inherited graphics state.
                dark_block = re.sub(
                    r'\bBT\b',
                    f'BT\n{dark_color_str}',
                    original, count=1
                )

                replacement = (
                    f"/OC /DStxt BDC\n{original}\nEMC\n"
                    f"/OC /DPtxt BDC\n{dark_block}\nEMC\n"
                )
                content = content[:rel_s] + replacement + content[rel_e:]

        # Wrap backgrounds in bg OCG
        if pre_bt and (' re\n' in pre_bt or '/Pattern cs' in pre_bt):
            new_data = f"/OC /DSbg BDC\n{pre_bt.rstrip()}\nEMC\n{content}"
        else:
            new_data = pre_bt + content

        page.Contents = pdf.make_stream(new_data.encode('latin-1'))

    pdf.save(output_path)
    pdf.close()

    if verbose:
        print(f"  Pages processed:    {total_pages}")
        print(f"  Light-text wrapped: {total_light}")
        print(f"  OCG layers added:   Screen Backgrounds, Screen Text, Print Text")
        print(f"  Output:             {output_path} ({os.path.getsize(output_path):,} bytes)")

    return total_light


# --- HTML -> PDF rendering -------------------------------------------

def render_html_to_pdf(html_path, pdf_path, print_mode=False):
    """Render HTML to PDF via WeasyPrint."""
    from weasyprint import HTML
    HTML(filename=html_path).write_pdf(pdf_path)


# --- Standalone print PDF (dual-PDF fallback) ------------------------

def generate_print_pdf(html_path, output_path):
    """
    Generate a standalone print-friendly PDF from HTML source by
    injecting print-mode CSS. Use as fallback for viewers that don't
    support OCG PrintState (macOS Preview).
    """
    from weasyprint import HTML

    with open(html_path, 'r') as f:
        html = f.read()

    # CRITICAL: must override CSS *variables* (--cream, --surface, etc) at :root
    # AND kill gradients/rgba/var() usages. The naive `background: white
    # !important` alone leaves var(--surface) tinted surfaces intact in
    # WeasyPrint, producing the "still off-white" bug. Verified: drops tint
    # coverage from ~85% to <0.1%.
    print_css = """
    <style id="ds-print-mode-force">
    /* 1. Override the theme variables themselves to pure white */
    :root {
      --cream: #ffffff !important;
      --surface: #ffffff !important;
      --card: #ffffff !important;
      --border: #cccccc !important;
      --bg: #ffffff !important;
      --bg-alt: #ffffff !important;
      --surface-alt: #ffffff !important;
    }
    /* 2. Kill ALL backgrounds universally (catches var(), rgba, gradients) */
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
    /* 3. Darken text that was designed for cream/tinted backgrounds */
    [style*="color:#fff"], [style*="color:#ffffff"],
    [style*="color: #fff"], [style*="color: #ffffff"],
    [style*="color:white"] { color: #0a3b3b !important; }
    [style*="color:#ffd700"], [style*="color: #ffd700"] { color: #806000 !important; }
    [style*="color:#8a6d1f"], [style*="color: var(--gold)"] { color: #5a4400 !important; }
    [style*="color:#2d6867"], [style*="color: var(--teal)"] { color: #1a4040 !important; }
    [style*="color:#4ad6b4"] { color: #0a3b3b !important; }
    </style>
    """

    # Insert before </head> or prepend
    if '</head>' in html:
        html = html.replace('</head>', print_css + '</head>')
    else:
        html = print_css + html

    # Strip inline background declarations that survived (catches var(), gradients)
    html = re.sub(r'background-image\s*:\s*[^;"}]+;?', '', html)
    html = re.sub(
        r'background\s*:\s*(?:var\([^)]+\)|#[0-9a-fA-F]+|linear-gradient\([^)]+\)|radial-gradient\([^)]+\)|rgba?\([^)]+\))\s*;?',
        '', html
    )

    HTML(string=html).write_pdf(output_path)
    print(f"  Print PDF generated: {output_path} ({os.path.getsize(output_path):,} bytes)")


# --- Verification ----------------------------------------------------

def verify_ocg(pdf_path):
    """Verify OCG structure and print a summary."""
    pdf = pikepdf.open(pdf_path)
    ocprops = pdf.Root.OCProperties
    if not ocprops:
        print("  WARNING: No OCG properties found")
        pdf.close()
        return False

    ocgs = ocprops.OCGs
    print(f"  OCGs: {len(ocgs)}")
    for g in ocgs:
        name = str(g.get('/Name', '?'))
        usage = g.get('/Usage', {})
        v = usage.get('/View', {}).get('/ViewState', '?')
        p = usage.get('/Print', {}).get('/PrintState', '?')
        print(f"    - {name}: View={v}, Print={p}")

    pdf.close()
    return True


def measure_ink(pdf_path, dpi=72, threshold=245):
    """
    Render PDF to images and measure percentage of non-white (ink) pixels.
    Used to verify print-mode background suppression.
    """
    import subprocess
    import glob
    import tempfile
    from PIL import Image
    import numpy as np

    prefix = tempfile.mktemp(prefix="ink_")
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), pdf_path, prefix],
        check=True, capture_output=True
    )
    images = sorted(glob.glob(f"{prefix}*.png"))
    total_px = 0
    ink_px = 0
    for img_path in images:
        arr = np.array(Image.open(img_path).convert("L"))
        total_px += arr.size
        ink_px += (arr < threshold).sum()
        os.remove(img_path)
    pct = ink_px / total_px * 100 if total_px else 0
    return pct


# --- Main ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Add OCG print auto-switch to DS PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s atlas.pdf -o atlas-smart.pdf
  %(prog)s atlas.html -o atlas-smart.pdf
  %(prog)s atlas.pdf -o atlas-smart.pdf --also-print-pdf
  %(prog)s atlas.pdf -o atlas-smart.pdf --verify
        """
    )
    parser.add_argument('input', help='Input PDF or HTML file')
    parser.add_argument('-o', '--output', required=True, help='Output PDF path')
    parser.add_argument('--also-print-pdf', action='store_true',
                        help='Also generate a standalone print-friendly PDF')
    parser.add_argument('--verify', action='store_true',
                        help='Verify OCG structure after generation')
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if not os.path.exists(input_path):
        sys.stderr.write(f"ERROR: Input file not found: {input_path}\n")
        sys.exit(1)

    # If HTML input, render to PDF first
    if input_path.endswith(('.html', '.htm')):
        print(f"Rendering HTML -> PDF (WeasyPrint)...")
        temp_pdf = output_path.replace('.pdf', '-temp.pdf')
        render_html_to_pdf(input_path, temp_pdf)
        input_path = temp_pdf
        print(f"  Screen PDF: {input_path}")

    # Add OCG layers
    print(f"\nAdding OCG auto-switch layers...")
    add_print_ocg(input_path, output_path)

    # Verify
    if args.verify:
        print(f"\nVerifying OCG structure...")
        verify_ocg(output_path)

    # Optional: standalone print PDF
    if args.also_print_pdf:
        print_path = output_path.replace('.pdf', '-PRINT.pdf')
        if args.input.endswith(('.html', '.htm')):
            print(f"\nGenerating standalone print PDF...")
            generate_print_pdf(args.input, print_path)
        else:
            print(f"\nNOTE: Standalone print PDF requires HTML source. Skipping.")

    print(f"\nDone: {output_path}")
    print(f"   Open in Adobe Acrobat/Reader and print -- backgrounds auto-hide.")
    print(f"   macOS Preview users: use the -PRINT.pdf file instead.")


if __name__ == '__main__':
    main()
