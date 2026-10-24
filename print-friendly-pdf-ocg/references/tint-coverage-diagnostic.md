# Tint-Coverage Diagnostic: Detecting the "Still Off-White" Bug

## The Problem

When generating a print-friendly PDF from HTML with CSS-variable-based
theming, the naive `background: white !important` rule produces a PDF that
**looks white** but still lays down toner. The aggregate ink% metric
(everything below brightness 245) can read "improved" while the page is
still cream-tinted — because the tint is so close to white that it's
invisible to the eye but still prints as a full-page color fill.

## The Diagnostic

Instead of (or in addition to) measuring aggregate ink%, measure the
**pixel-level presence of specific target tints** and the **pure-white
ratio**. This directly detects whether CSS variables were overridden.

```python
import subprocess, glob, tempfile, os
from PIL import Image
import numpy as np
from collections import Counter

def tint_coverage(pdf_path, targets, page=1, dpi=100):
    """
    Render one page and measure pixel-level presence of specific tints.

    Args:
        pdf_path: PDF to analyze
        targets: dict of {label: (r,g,b)} e.g. {"surface": (0xf5,0xf2,0xea)}
        page: page number (1-indexed)
        dpi: render resolution

    Returns: dict of {label: percentage_of_page}
    """
    prefix = tempfile.mktemp(prefix="tint_")
    for f in glob.glob(f"{prefix}*.png"):
        os.remove(f)
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), "-f", str(page), "-l", str(page),
         pdf_path, prefix],
        check=True, capture_output=True
    )
    img = glob.glob(f"{prefix}*.png")[0]
    arr = np.array(Image.open(img).convert("RGB"))
    os.remove(img)
    total = arr.shape[0] * arr.shape[1]

    results = {}
    for label, rgb in targets.items():
        diff = np.abs(arr.astype(int) - np.array(rgb)).sum(axis=2)
        results[label] = int((diff < 12).sum()) / total * 100

    # Also report dominant quantized colors
    flat = arr.reshape(-1, 3)
    q = (flat // 8 * 8)  # quantize to 8-step buckets
    dom = Counter(map(tuple, q[::97])).most_common(3)
    results["_dominant"] = [(f"#{r:02x}{g:02x}{b:02x}", pct * 97)
                             for (r, g, b), pct in dom]
    return results
```

## Usage

```python
# DS document theme tokens
TARGETS = {
    "pure_white":      (0xff, 0xff, 0xff),
    "cream_#faf8f3":   (0xfa, 0xf8, 0xf3),
    "surface_#f5f2ea": (0xf5, 0xf2, 0xea),
    "card_#eee9dc":    (0xee, 0xe9, 0xdc),
}

orig = tint_coverage("DS-Master-Atlas.pdf", TARGETS)
print_pdf = tint_coverage("DS-Master-Atlas-PRINT.pdf", TARGETS)
```

## Interpretation

| Metric | Pass | Fail |
|--------|------|------|
| `pure_white` | >95% | <90% (CSS var override failed) |
| `surface_#f5f2ea` | <0.1% | >50% (body gradient survived) |
| `cream_#faf8f3` | <0.2% | >10% (card surfaces survived) |

**Why aggregate ink% is insufficient:** A page with 85% `#f5f2ea` coverage
(brightness 244) reads as ~85% "ink" at threshold 245 but ~13% "ink" at
threshold 240. Neither tells you the page is actually cream-tinted. Only
the tint-specific pixel count reveals the truth.

## Real Example (DS-Master-Atlas, 2026-06-20)

```
ORIGINAL:
  pure_white:     0.0%
  surface_#f5f2ea: 84.80%   <-- body gradient covers entire page
  dominant:       #f0f0e8

PRINT (CSS-var override applied):
  pure_white:     97.5%
  surface_#f5f2ea: 0.04%    <-- gone
  dominant:       #f8f8f8 (= #ffffff after quantization)
```

The CSS-variable override at `:root` dropped surface tint from 84.8% to
0.04%. The aggregate ink metric went from 30.4% to 13.7% — which looked
like "mostly text" but could have hidden surviving tints. The tint-specific
measurement proved the backgrounds were truly gone.
