#!/usr/bin/env python3
"""
PDF Pixel Audit — objective layout verification via rendered-page pixel analysis.

Renders PDF pages to PNG with pdftoppm (poppler), then uses PIL + numpy to
measure actual content extent per row: left gap, right gap, content width as
percentage of page width, and whether margins are even.

This is far more reliable than vision-model analysis for layout debugging:
objective, reproducible, no hallucination risk.

Usage:
    python3 pdf-pixel-audit.py <pdf_file> [page_range] [dpi]

    page_range: e.g. "3" for page 3 only, "2-4" for pages 2-4, omit for all pages
    dpi: resolution (default 200; higher = more precise but slower)

Examples:
    python3 pdf-pixel-audit.py report.pdf 3          # audit page 3
    python3 pdf-pixel-audit.py report.pdf 2-4 150    # audit pages 2-4 at 150dpi
    python3 pdf-pixel-audit.py report.pdf             # audit all pages

Requires: poppler-utils (pdftoppm), Pillow, numpy
    pip install Pillow numpy
    # macOS: brew install poppler
"""
import sys
import subprocess
import tempfile
import os
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("ERROR: pip install Pillow numpy")
    sys.exit(1)


def render_pages(pdf_path, pages, dpi, tmpdir):
    """Render specified PDF pages to PNG files."""
    prefix = str(tmpdir / "page")
    f_flag = pages[0] if pages else 1
    l_flag = pages[-1] if pages else None

    cmd = ["pdftoppm", "-png", "-r", str(dpi)]
    if pages:
        cmd.extend(["-f", str(pages[0]), "-l", str(pages[-1])])
    cmd.extend([pdf_path, prefix])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: pdftoppm failed: {result.stderr}")
        sys.exit(1)

    return sorted(Path(tmpdir).glob("page-*.png"))


def analyze_page(png_path, threshold=245):
    """
    Analyze a rendered page image.

    Returns dict with: page_num, width, height, content_pct,
    margins (list of {y_pct, left_gap, right_gap, even}).
    """
    img = Image.open(png_path)
    arr = np.array(img.convert("RGB"))
    h, w = arr.shape[:2]

    # Count content rows (any pixel darker than threshold)
    step = max(1, h // 500)  # sample every ~2px for speed
    content_rows = sum(1 for y in range(0, h, step) if np.any(arr[y] < threshold))
    content_pct = content_rows / (h / step) * 100

    # Margin scan at 5% intervals
    margins = []
    for y_pct in range(5, 100, 5):
        y = int(h * y_pct / 100)
        row = arr[y]
        non_white = np.where(np.any(row < threshold, axis=1))[0]
        if len(non_white) > 0:
            lg = int(non_white[0])
            rg = int(w - 1 - non_white[-1])
            diff = abs(lg - rg)
            even = diff < 30  # 30px tolerance at 200dpi ≈ 3.8mm
            margins.append({
                "y_pct": y_pct,
                "left_gap": lg,
                "right_gap": rg,
                "diff": diff,
                "even": even,
            })

    # Extract page number from filename
    stem = png_path.stem  # e.g. "page-03"
    try:
        page_num = int(stem.split("-")[-1])
    except ValueError:
        page_num = 0

    return {
        "page_num": page_num,
        "width": w,
        "height": h,
        "content_pct": round(content_pct, 1),
        "margins": margins,
    }


def print_report(results, pages_arg):
    """Print human-readable audit report."""
    print("=" * 60)
    print("PDF PIXEL AUDIT REPORT")
    print("=" * 60)

    for r in results:
        print(f"\n{'─' * 50}")
        print(f"Page {r['page_num']}: {r['width']}x{r['height']}px, "
              f"{r['content_pct']}% content")

        if r["content_pct"] < 15:
            print(f"  ⚠ LOW CONTENT ({r['content_pct']}%) — likely overflow "
                  f"from previous page or near-empty page")

        if not r["margins"]:
            print("  (no content detected)")
            continue

        uneven = [m for m in r["margins"] if not m["even"]]
        if not uneven:
            print("  ✓ ALL MARGINS EVEN")
        else:
            print(f"  ✗ {len(uneven)} UNEVEN MARGIN ROW(S):")
            for m in uneven:
                print(f"    y={m['y_pct']}%: L_gap={m['left_gap']} "
                      f"R_gap={m['right_gap']} (off by {m['diff']}px)")

        # Detailed margin table (always show for requested pages)
        if pages_arg:
            print(f"  {'y%':>4}  {'L_gap':>6}  {'R_gap':>6}  {'Status'}")
            for m in r["margins"]:
                status = "✓ EVEN" if m["even"] else f"✗ OFF"
                print(f"  {m['y_pct']:>4}  {m['left_gap']:>6}  "
                      f"{m['right_gap']:>6}  {status}")

    # Summary
    print(f"\n{'=' * 60}")
    low_pages = [r for r in results if r["content_pct"] < 15]
    uneven_pages = [r for r in results if any(not m["even"] for m in r["margins"])]
    if not low_pages and not uneven_pages:
        print("RESULT: ALL CHECKS PASSED ✓")
    else:
        if low_pages:
            print(f"⚠ LOW-CONTENT PAGES (possible overflow artifacts): "
                  f"{[r['page_num'] for r in low_pages]}")
        if uneven_pages:
            print(f"✗ UNEVEN-MARGIN PAGES: "
                  f"{[r['page_num'] for r in uneven_pages]}")
    print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"ERROR: file not found: {pdf_path}")
        sys.exit(1)

    pages_arg = sys.argv[2] if len(sys.argv) > 2 else None
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 200

    # Parse page range
    pages = None
    if pages_arg:
        if "-" in pages_arg:
            parts = pages_arg.split("-")
            pages = list(range(int(parts[0]), int(parts[1]) + 1))
        else:
            pages = [int(pages_arg)]

    with tempfile.TemporaryDirectory() as tmpdir:
        pngs = render_pages(pdf_path, pages, dpi, Path(tmpdir))
        if not pngs:
            print("ERROR: no pages rendered")
            sys.exit(1)

        results = [analyze_page(p) for p in pngs]
        print_report(results, pages_arg)


if __name__ == "__main__":
    main()
