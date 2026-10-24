#!/usr/bin/env python3
"""
verify_print_smart.py — Independently verify an OCG print-smart PDF works.

Runs 4 checks against an OCG-smart PDF and its original source PDF:

  1. OCG structure    — exactly 3 layers with correct View/Print states
                        (bg: ON/OFF, screen-text: ON/OFF, print-text: OFF/ON)
  2. Screen fidelity  — smart (all layers ON) renders pixel-identical ink %
                        to the original (abs diff < 1.0%), same page count
  3. Print reduction  — print-simulation (BaseState=OFF, print-text ON)
                        shows a meaningful ink cut vs original (>= 30%)
  4. Text preservation— word count via pdftotext is identical original vs
                        print-sim (proves zero text loss, the strongest
                        invariant — catches the silent rg-injection bug)

WHY THIS EXISTS:
  A skill's self-reported "Validated Results" table is a claim, not proof.
  Re-run this against any SMART pdf + its original before trusting it or
  telling the user it works. Catches: missing OCGs, inverted states,
  screen-mode drift, the rg-injection bug (dark duplicates not rendering),
  and text loss from over-aggressive wrapping.

USAGE:
  python3 verify_print_smart.py original.pdf smart.pdf

REQUIRES: pikepdf, Pillow, numpy, pdftoppm (poppler), pdftotext (poppler)

EXIT: 0 if all 4 checks pass, 1 otherwise.
"""
import sys
import os
import glob
import subprocess
import tempfile

import pikepdf
from PIL import Image
import numpy as np


def measure_ink(pdf_path, dpi=72, threshold=245):
    """Render PDF to grayscale PNGs and return (ink_pct, page_count)."""
    prefix = tempfile.mktemp(prefix="ver_ink_")
    for f in glob.glob(f"{prefix}*.png"):
        os.remove(f)
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), pdf_path, prefix],
        check=True, capture_output=True,
    )
    imgs = sorted(glob.glob(f"{prefix}*.png"))
    total_px = ink_px = 0
    for p in imgs:
        arr = np.array(Image.open(p).convert("L"))
        total_px += arr.size
        ink_px += int((arr < threshold).sum())
        os.remove(p)
    pct = ink_px / total_px * 100 if total_px else 0.0
    return pct, len(imgs)


def make_print_sim(smart_path):
    """Create a print-simulation PDF: flip OCG states to exactly what a
    spec-compliant printer does (read Usage hints -> set visibility)."""
    pdf = pikepdf.open(smart_path)
    d = pdf.Root.OCProperties.D
    d.BaseState = pikepdf.Name.OFF
    d.ON = [pdf.Root.OCProperties.OCGs[2]]            # print-text visible
    d.OFF = [pdf.Root.OCProperties.OCGs[0],
             pdf.Root.OCProperties.OCGs[1]]           # bg + screen-text hidden
    out = tempfile.mktemp(suffix=".pdf")
    pdf.save(out)
    pdf.close()
    return out


def word_count(pdf_path):
    """Extract text via poppler and count whitespace-separated tokens."""
    r = subprocess.run(
        ["pdftotext", pdf_path, "-"], capture_output=True, text=True
    )
    return len(r.stdout.split())


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: verify_print_smart.py original.pdf smart.pdf\n")
        sys.exit(1)
    orig, smart = sys.argv[1], sys.argv[2]
    for p in (orig, smart):
        if not os.path.exists(p):
            sys.stderr.write(f"ERROR: {p} not found\n")
            sys.exit(1)

    all_ok = True
    print("=" * 72)

    # --- Check 1: OCG structure -----------------------------------------
    pdf = pikepdf.open(smart)
    oc = pdf.Root.OCProperties
    expected = [("/ON", "/OFF"), ("/ON", "/OFF"), ("/OFF", "/ON")]
    actual = []
    for g in oc.OCGs:
        u = g.get("/Usage", {})
        actual.append((
            u.get("/View", {}).get("/ViewState", "-"),
            u.get("/Print", {}).get("/PrintState", "-"),
        ))
    n_ocgs = len(oc.OCGs)
    struct_ok = n_ocgs == 3 and actual == expected
    all_ok &= struct_ok
    status = "PASS" if struct_ok else "FAIL"
    print(f"[{status}] OCG structure: {n_ocgs} layers, states {actual}")
    pdf.close()

    # --- Check 2: Screen fidelity ---------------------------------------
    oink, no = measure_ink(orig)
    sink, ns = measure_ink(smart)
    fidelity_ok = abs(oink - sink) < 1.0 and no == ns
    all_ok &= fidelity_ok
    status = "PASS" if fidelity_ok else "FAIL"
    print(f"[{status}] Screen fidelity: orig {oink:.1f}% vs smart {sink:.1f}%"
          f" ({no}pp/{ns}pp, drift {abs(oink-sink):.2f}%)")

    # --- Check 3: Print ink reduction -----------------------------------
    psim = make_print_sim(smart)
    pink, _ = measure_ink(psim)
    cut = (oink - pink) / oink * 100 if oink else 0
    # 30% floor: documents with little background + dark text legitimately
    # cut less. If cut < 30%, the doc may not have needed OCG treatment,
    # or the background-wrapping heuristic missed shading objects.
    ink_ok = cut >= 30
    all_ok &= ink_ok
    status = "PASS" if ink_ok else "FAIL"
    print(f"[{status}] Print ink reduction: {oink:.1f}% -> {pink:.1f}%"
          f" ({cut:.0f}% cut)")

    # --- Check 4: Text preservation (catches the rg-injection bug) ------
    wc_o = word_count(orig)
    wc_p = word_count(psim)
    text_ok = wc_o == wc_p and wc_o > 0
    all_ok &= text_ok
    status = "PASS" if text_ok else "FAIL"
    verdict = "identical" if text_ok else "MISMATCH"
    print(f"[{status}] Text preservation: {wc_o} vs {wc_p} words ({verdict})")
    if not text_ok and wc_o > wc_p:
        print("         -> Text LOST in print mode. Likely the rg-injection")
        print("            bug: dark duplicates never rendered. See SKILL.md")
        print("            Pitfalls section 'CRITICAL: The rg injection bug'.")

    os.remove(psim)
    print("=" * 72)
    print(f"Overall: {'ALL PASS' if all_ok else 'FAILURES PRESENT'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
