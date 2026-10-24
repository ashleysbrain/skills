---
name: delivery-as-received-gate
description: Use when delivering or authoring rendered principal artifacts.
---

# Delivery-As-Received Gate

Applies to every visual artifact sent to the principal (image, PDF, document render)
delivered through Telegram or any chat channel. The delivery channel is part
of the artifact: QA validates the rendered output AS RECEIVED, never the
source file's DOM or the authoring markup. Every failure in this class shipped
from a correct source through a broken capture/delivery pipeline.

## Always-on rules

1. **Never capture a tall multi-section page with one big fixed window.**
   `vh` units scale with the window: a 96vh hero in a 2900px window fills
   ~2800px and pushes every other section out of frame; dark and light
   variants fail identically while the artifact itself is correct. Even
   height-pinned single-pass captures can drop middle bands on very tall
   windows (compositor skip).
2. **Render per section at measured heights.** Live-read each section's
   `offsetHeight` from a real browser first; build one single-section file
   per section (full `<head>` + that section's markup only, replace
   `min-height:96vh` with a small px value on non-hero sections); Chrome
   headless `--screenshot --window-size=1200,<measured h>` each.
3. **Ink-census every raster before it enters a deliverable.**
   ```python
   import numpy as np; from PIL import Image
   a = np.array(Image.open(p).convert('L'))
   rows = (a > 60).sum(axis=1); ink = int((rows > 20).sum())
   ```
   A section with ~0 content rows is a blank delivery regardless of source
   correctness. For tall stitched documents, census each third separately.
4. **One document, not parts.** When the ask is "show me the artifact," the
   deliverable is ONE continuous document: stitch section rasters vertically
   after trimming each one's leading/trailing whitespace; verify continuity
   (largest empty run = design spacing only). Cropping a document into
   multiple chat-sized pieces is a format failure unless asked.
5. **PDF = raster compose when one page is required.** Chrome `--print-to-pdf`
   splits tall pages at its ~2.3k px cap into multiple pages; compose the
   verified rasters instead: `canvas.save('out.pdf','PDF',resolution=144)`.
   Re-read the PDF (pypdf page images via `Image.open(io.BytesIO(im.data))`
   — not the PIL object, it lacks `.read`) and re-census ink. Assert exactly
   one page. And deliver the format the user asked for: a PNG is not a PDF.
6. **Dark themes need a phone legibility preflight**; if the channel renders
   it as a black screen, deliver a channel-adapted render (CSS variable
   override for colors only, content byte-identical), canonical file stays.
7. **Validate the capture instrument once against a known-good render**
   before trusting its output on the real artifact.

## Animated artifacts

- Canonical live form = the HTML file itself (CSS keyframes only; no SMIL,
  no JS; honor `prefers-reduced-motion`). Chat channels cannot display it
  live: state that plainly and deliver the HTML file as the canonical
  artifact. Never strip animation from the canonical artifact for delivery
  convenience — portability passes that remove motion from the live file are
  regressions of a praised property.
- When a portability or QA law forces removing an animation mechanism
  (e.g., a no-JS law strips a canvas animation), rebuild the SAME behavior
  in an allowed mechanism at equivalent richness — per-element staggered
  arrival, individual shimmer, breathing container — never a single uniform
  approximation. Downgrading one section's motion while other sections gain
  animation is a visible regression.
- Stagger per-element timing by MERGING into the one existing style
  attribute: `style="--d:1.234s;animation-delay:var(--d),calc(var(--d)+.6s)"`.
  Appending a second `style=` attribute is silently dropped (HTML honors
  the first) and every element then animates in unison. Audit with
  `re.findall(r'style="[^"]*"[^>]*style="', html)` — must be zero matches.
  Each animation in a comma-separated animation list needs its own delay
  entry.
- Automated/headless Chrome does not advance CSS animation clocks: computed
  styles park at base or reduced-motion values, and
  `--virtual-time-budget` does not move keyframed properties for diff
  purposes. Verify stagger STRUCTURALLY instead: keyframe names resolve in
  the live stylesheet (CSSKeyframesRule list), the animation shorthand
  parses, per-element computed `animationDelay` values differ, and no later
  rule sets a static opacity/width the animations must override. Sampling
  computed opacity in an automated tab proves nothing.
- Paper/PDF carries motion as a PHASE STRIP: one isolated single-section file
  per animation phase with an override style (`animation:none!important` +
  explicit per-phase state), rendered, consecutive-diffed
  (`ImageChops.difference`, >0 changed px proves the override landed; zero
  diff = override never reached the elements), stacked with arrows between
  frames.

## Plain-English comprehension bar

For any explainer artifact: a human must be able to take in what is going on
at a glance. Plain declarative captions over every graphic ("every dot is
one seat; the center is the root"), labels that name the thing not the
statistic, a why-it-matters line per section. Jargon metrics stay only with
their plain-English gloss attached. Complexity of the system is never an
excuse: the assignment IS the translation.

Meet the bar by rewriting the MEANING-BEARING sentences, not by relabeling:
- Open each section with what the thing IS in household words (a tree, a
  funnel, a postage stamp vs an oak).
- Convert statistics to human frequencies: a rank-correlation pair becomes
  "right 98 times out of 100 vs 65 — flat memory gets one in three wrong."
- State consequences in the reader's terms: recalling the wrong cousin,
  distant cousins filed as next-door neighbors.
- Close with a one-sentence whole story.
A pass that adjusts labels while keeping the original technical sentences
is cosmetic and does not meet the bar.

## Subject-of-data naming

Every artifact states explicitly WHICH entity its data belongs to. Verify
the ground truth (e.g., embedding paths rooted at one organism) before
labeling; a taxonomy label one level above the data (ecosystem language on
single-organism data) is a defect a reader catches immediately.

## Charts must reflect the real dataset

A chart in a delivered exhibit is generated from the measured data itself,
never a synthetic/idealized stand-in (a perfect-doubling census like
1/2/4/8/16/32/64 is the signature of placeholder geometry). When the shape
of a chart changes because placeholder data was replaced with real data,
the delivery message states the old census, the new census, and that the
method/metrics are unchanged — the reader asks "did the science change?"
and the answer separates data correction from method change. Rebuild
recipes, census-verification snippets, and depth-naming workflow:
`references/data-provenance.md`.

## Animation coverage and honesty

"All animated" means every element family, not every section except the
ones that were hard: inventory each family (hero dots, chart edges, chart
nodes, bars, gauges, connectors, rim) and each must carry motion whose
TIMING encodes data (growth order = BFS depth; cramped timing = the
distortion itself). Restoring one section's animation while others stay
static, or approximating a rich removed animation with one uniform effect,
is a visible regression. Motion that encodes nothing is decoration — veto
it. See `references/data-provenance.md` for delay derivation.

## Paired comparison charts must differ visibly

Two side-by-side boxes arguing a contrast (flat vs curved, before vs
after) fail when both render as near-identical line balls at chat size.
Measure the drawn extents (x-range of marks vs canvas) before delivering;
if the two frames differ by less than ~2x in spread or the difference
lives only in cramming, add labeled verdict lines INSIDE each frame
("all 127 branches squeezed into 19% of the page" vs "every branch keeps
its true length") and distinct annotation colors. The claim must be
readable from the pixels, not from the surrounding prose.

## Verify the DRAWN geometry, not the source numbers

A caption claim about the rendered chart ("edges shrink to 9%", "24 groups",
"rings are measured") must be verified by MEASURING THE SVG/PNG GEOMETRY
ITSELF — parse the delivered markup's coordinates, compute the actual edge
lengths by depth, count the actual groups — never by checking only the
source dataset the caption was written from. The two diverge: a sourced
number can be true of the data and false of the drawing (a 9% factor true
of the curved disc's (1-r^2) while the flat box's drawn edges measured
~110% of root — the flat box's real defect was room collapse between
full-length edges, a different phenomenon needing different words). When
a caption fails drawn-geometry verification, fix the WORDS to the measured
drawing, not the drawing to the words — and re-hash the artifact, since
text edits change the delivery hash.

Cross-harness verification (a triangle/pinball pass) arrives as a verdict
batch: apply ONLY the named surgical edits, then re-run the delivery gate
on the changed artifact in the same session — an interrupted or unverified
re-render leaves a delivered sha that no longer matches the canonical file,
and the next delivery must rebuild from the current file, not from the
last-verified raster.

## Support file

- `references/data-provenance.md` — chart provenance: placeholder-data
  detection, real-tree rebuild recipe, depth-naming, shape-change messaging.

## Failure signatures

- Dark render, low mean, ink in one band → window/vh trap.
- Light render 0.0% non-white in a region → same trap; fix the instrument,
  not the theme.
- All phase rasters identical → override CSS never landed (injection point,
  specificity, or target outside the capture window).
- Staggered elements animate in unison → per-element delay lived in a
  duplicate style attribute the parser dropped; merge into one attribute.
- A selector-based animation edit matches MORE elements than intended when a
  broad attribute selector (e.g. `circle[fill="none"]`) hits guide rings in
  hero graphics that merely SHARE the attribute with the target family —
  before applying, count matches per container and scope by ancestor
  (.treebox vs hero) or class, or the edit animates the wrong family and the
  defect only shows at the gate.
- Mid-batch self-edits can introduce duplicate `class`/`style` attributes
  (an insertion helper appends instead of merging) — after every apply pass,
  grep for doubled attributes on the same tag; HTML silently honors the
  first and the new state never lands.
- Automated tab shows animated elements frozen at base values → animation
  clock never ran; verify structurally, do not ship based on the probe.
- DOM counts correct, render empty → capture pipeline, always.
- A named claim in the raster (seat name, schedule cadence, "first caller")
  contradicts the live registry/cron spec → the caption was written from
  narrative memory, not from the store: grep the live registry for every
  named claim before shipping.
