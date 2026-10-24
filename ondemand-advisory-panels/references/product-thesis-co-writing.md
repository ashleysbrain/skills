# Product Thesis Co-Writing with Advisory Panels

Session: 2026-06-10
Canonical artifact: `ds-wave-product-advisory-panel-private/PRODUCT_THESIS_V1_LOCKED.md`

## The Process

1. **Load the right board** (Product Advisory Panel, not Marketing or principal)
2. **Load the coach profiles** (Marty Cagan for product operating model, April Dunford for positioning)
3. **Ask the user 3 questions before writing** (wedge, segment, competitive alternative)
4. **Adjust questions for product stage** (pre-launch = ask about interest/reachouts, not user attachment)
5. **Before writing ANY "what we'll build" section, search the codebase.** Run `search_files` on hydra-os/products/ and hydra-os/scripts/ for existing implementations. the principal has already built extensive algorithms. The thesis must reflect what EXISTS.
6. **Write the thesis around the engine's adaptive nature** (not a single-dimension wedge) when the product is an adaptive coaching engine
7. **Include the platform + engine architecture** (Divinity Health platform, the specialist engine engine inside it)
8. **Generate PDF** via markdown→HTML→weasyprint pipeline (pandoc+xelatex fails on this system, no LaTeX engine)

## Key Decisions from This Session

- **Wedge:** The engine adapts. It coaches whatever dimension the user needs. Not one dimension. All of them. The wedge is the intelligence, not the dimension.
- **Segment:** Behavioral, not demographic. "Woken Frustrated" — people who've had a major life event, tried everything, found it all unscientific. Not gender-specific.
- **Category:** "AI Health Coach" (April Dunford's Create New Game strategy)
- **Competitive alternative:** The 8-app scatter (users cobble together 8+ apps manually)
- **Platform:** Divinity Health consumer app (the principal, CTO) with the specialist engine engine inside

## What Was Already Built (do not recommend rebuilding)

All in `hydra-os/products/principal-8d-tracker/`:
- calculator.py (729 lines) — All 8 dimensions with named physics models + coupling matrix (28 pairs)
- scoring_pipeline.py (290 lines) — Full autonomous scoring pipeline
- rescore_engine.py (1,072 lines) — Deterministic rescore with unit tests
- adhd_ef_compass_v3.py — Sigmoid psychometric response curves
- autonomous_overlay.py — Confidence/coverage/freshness overlays
- unified_pipeline.py, operational_layer.py, support_subscores.py
- Total: 8,400+ lines across 22 Python files

## PDF Generation (tested working)

```bash
python3 -c "
import markdown
md = open('SOURCE.md').read()
html = markdown.markdown(md, extensions=['tables', 'fenced_code'])
full = '<!DOCTYPE html><html><head><meta charset=\"utf-8\"><style>
body{font-family:Helvetica,Arial,sans-serif;font-size:11px;line-height:1.5;margin:35px auto;max-width:700px;color:#222}
h1{font-size:18px;border-bottom:2px solid #333;padding-bottom:6px}
h2,h3{font-size:13px;margin-top:18px;color:#444}
blockquote{border-left:3px solid #999;padding-left:10px;color:#555;font-style:italic}
strong{color:#111}
hr{border:none;border-top:1px solid #ccc;margin:14px 0}
</style></head><body>' + html + '</body></html>'
with open('/tmp/output.html','w') as f: f.write(full)
"
weasyprint /tmp/output.html /tmp/output.pdf
```

Note: pandoc + xelatex fails (no LaTeX engine installed). Use weasyprint instead.
