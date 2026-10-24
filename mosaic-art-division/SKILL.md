---
name: mosaic-art-division
version: 1.0.0
author: the operator agent Agent
license: MIT
description: Use when building organism icons, clips, or art direction.
metadata:
  hermes:
    tags: [art, icons, butterfly, brand, mosaic, creative-production]
---

# the OS Art Division (icon → clip → movie program)

## When to Use

- Any task touching organism icons, the butterfly mark, logo personalization, spin-up icons, clips, movies, dynamic macOS icons, or fleet art direction.
- Building or editing the `/art` board, the program doc, or the spin-up icon generator.

This is a standing division of the platform, not a task queue: the living identity of every organism the OS births, from first breath to feature film.

## The arc (stage order)

0. **Movement zero (seed, exists):** `brand/mosaic-os/iterations/butterfly-evolution.svg` — pure-SMIL 9s three-movement tempo (LINEAGE sketch → GEOMETRY → LIVING). Everything grows from this file; do not regenerate it, extend it.
1. **Day-1 spin-up icon:** every new organism gets a 2D single-weight line butterfly at birth (generator below), in the CURRENT line color of the succession.
1b. **Living icon (deterministic drift):** `src/living_icon_engine.py` renders an organism's daily living frame straight from ledger state — wingspan scales with the count of `stage='tri:closed'` ledger rows, mosaic cell count with the count of ACTIVE spine directives, and a per-day salt hashed from that day's state. Same history, same butterfly; never the same month twice. Never backfill past days with approximate state — render today's frame from LIVE state only and show lineage via the actual dated artifacts (a lineage filmstrip = one `<g>` cell per real dated frame plus the living frame).
1c. **Lifecycle begins at hatch:** an organism's render is its TRUE life stage — egg → larva (instars) → chrysalis (with eclosion progress) → imago (wings unfurl through an eclosion window). All organisms share the same species form up to eclosion. Stage truth is wall-clock, but the hatch itself is NEVER wall-clock-gated: on first view the whole pre-birth sequence PLAYS fast (~8s crossfade egg → larva → chrysalis → eclosion → species form) before live personalization grows on top. A principal-facing surface must never sit parked on a bare egg awaiting real days — start mid-hatch if the organism is young.
2. **Personalization drift:** lived history mutates the RIGHT-wing tessellation over time; left wing stays the ordered phi grid. Drift applies ONLY from the organism's own eclosion (birth) onward — organisms are identical until they are born, then diverge.
3. **Clip compiler:** personalized frames → unique short clip per user/business.
4. **Movie:** full per-user/per-business film (later horizon; clip compiler is the prerequisite).

## Always-on program laws

1. **B2C + B2B full arc; B2BU personalization IN SCOPE through the semantic gates.** Every organism gets its own logo evolving from the the OS root, derived through gated research on the user (name → candidate symbols → research filter → user gate). B2BU organisms keep the standard b2b icon as the honest interim state until they pass their symbol gate — never hash-random marks, never personalization without the gate. Check the CURRENT segmentation law in `ART-DIVISION-PROGRAM.md` before building; the principal amends it by order.
2. **Filter-down, never hand-tune.** One art direction iterates AT THE TOP and re-expresses itself per organism, like a genome expressed per cell. Never adjust a single organism's style outside a direction change.
3. **GENOME geometry law:** mirror in SHAPE, never in DETAIL — left wing orderly phi grid, right wing irregular tessellation, both clipped to the same mirrored outline. Line-only for day-1 icons: one stroke weight, no fills, no gradients; gold appears in state changes only, never static assets.
3b. **Line color is a succession constant, not a per-render choice.** The line gene lives as ONE constant in EACH generator (`SIGNAL`/`YELLOW` in the spinup and living engines) — currently butterfly yellow `#f5c518`; the teal `#4ad6b4` gene is archived in the dated lineage frames. A color change is a lineage event: update the constant in EVERY generator, append an `iterations/iterations.json` entry, and never restyle past dated frames (they are receipts, not assets). New organisms spin up from the current succession color.
4. **Motion is a user-desire flag, never a default.** Dynamic icon-square (macOS) shows the clip or a variation (cloud-art / lined / AI-filter) only when platform tech allows and the user wants motion; still icon = current geometry frame.
5. **Program homes:** doc `brand/mosaic-os/ART-DIVISION-PROGRAM.md`; board `b-art` served at `/art` (stage cards; movement zero inlines its SVG so it animates on the board); roster served at `/roster`; ledger lane `creative-production`. Owners across the full arc: Goethe (geometry/drift math), Tawara (clip rhythm), Da Vinci (production), Luria (gate), Wernicke (story each clip tells).
6. **principal-facing icons are ALWAYS LIVE.** Any surface showing an organism's icon renders it from the deterministic engine at REQUEST time (the `/roster` tab is the canonical shape) — never serve a cached PNG/raster of a butterfly. The living engine's numbers (receipts, spine laws, day salt) move daily; a cached render is a false receipt. Adding an organism to the roster is one line in the roster list inside the surface's renderer — no db card, no stored asset.
6b. **Hero-slot layout law: the LIVE render is the hero, and the controls sit ABOVE it.** On any toggle/gallery surface (the `/art` stage-0 shape): toggle chips first, then ONE large live butterfly of the selected organism (request-time render from the same engine as the grove — "one butterfly that is toggled and they must ALL BE LIVE"). Switching the toggle swaps the organism and the art updates with it. A static asset (the evolution film, any cached SVG) must NEVER occupy the hero slot — the recurring drift is the static film colonizing the top of the card with the toggles and the live renders buried small underneath it; a static film's lawful home is the Lineage section below, as the sketch that started the genome. Verify the layout programmatically, never by eyeball: index of the first toggle-chip id < index of the first `<svg` in the page slice, live-view div count == organism count, and the hero render carries the large size while the caption names the organism.

7. **Interconnected organisms share ONE scene.** `/scene` renders every organism flying a seeded path on a single shared canvas with gold threads between connected pairs (threads pulse when both ends are live); pre-imago forms stay low near the ground line, imagos fly high. Grow the scene's composition as real interconnections grow — it is the vehicle for interconnected-organism scenes.
8. **Human taste is recorded, never invented.** Art direction comes from the principal's saved taste decisions: the taste console on `/art` persists every slider/color choice (timestamped) to `boards/taste-profile.json`, and renderers read it live — the accumulated saves ARE the taste model. Bring the console to the principal at the earliest moment and drive direction WITH them, never invent direction alone; a geometrically correct render that reads 'AI-basic / super basic' is a defect. The ugly-beautiful register is valued — do not smooth it away.
9. **Scenes are bigger than the butterfly — behavior-driven and ALWAYS positive.** The butterfly becomes a small, detailed, strategic part of a larger living environment tailored to the user+organism pair. The user's measured behaviors drive the scene's growth — the environment is a portrait of behavior over time, never a static backdrop. POSITIVITY INVARIANT: however unhealthy the data, the art must INSPIRE — adversity renders as dawn/buds/storm-passing/opening, never decay, judgment, or shame; the data→art map is monotone toward hope (low signals render as MORE encouragement — new buds, clearing sky — never as less life).
10. **Live cards are DRAWN by the client, never swapped.** A live card is the browser building geometry from raw path data every frame: lines draw themselves (stroke-dashoffset animation), wings beat continuously, the butterfly flies (drift + bob + bank), earned marks sway — one rAF loop owns all motion for every organism on the page. The server ships DATA (paths, hatch frames, pulse) and the client owns every frame. Shipping finished server-rendered frames and crossfading their opacity is a still-image slideshow — no amount of extra frames makes it live; it reads as fake repetition.
10b. **Wing detail is CLIPPED INSIDE the silhouette — geometric vocabulary, not organic.** Wing marks come from the design's geometric vocabulary (triangles, quads, pentagons, bars, rings, mosaic tiles), never organic branch-squiggle generators. Every mark is born inside its wing group with a per-wing `clipPath` (the wing outline) so detail stays within the butterfly shape at every flap angle — a mark that could spill outside the wing at full beat is a defect even when its coordinates look plausible. Verify containment with browser `getBBox()`/`getBoundingClientRect()` spill measurement against the wing group (all four sides ≈0), never a hand-rolled numeric bbox over `d` strings — relative `h`/`v` commands and arc radii/flag params make naive regex bboxes wildly wrong.
10c. **Tempo ramps: slow start, accelerating as the scenario builds.** Wingbeat frequency is not a constant — integrate a ramp as earned marks accumulate, ease-out so it never jumps or reverses. **PERCEIVED RATE LAW: a beat computed as `|cos(phase)|` completes TWO visual strokes per phase cycle — perceived flap rate is 2× the phase frequency. Tune `f` for the PERCEIVED stroke period, never the phase rate (a 1.15 Hz phase reads as 2.3 flaps/s — principal rejected that tuning as "still flapping really really fast" twice). Working tuning: phase 0.05 Hz at hatch rising to 0.15 Hz settled = one visible stroke per ~10s building to one per ~3.3s — gliding-flight calm.** Accumulate the phase per frame (`S.ph += 2π·f·dt`, dt clamped) rather than computing `cos(2π·f·t)` from wall time — a time-derived phase cannot ramp frequency without a discontinuity. Flight bob and mark sway ride the same integrated phase so the whole body moves as one. Verify by counting scale minima per multi-second window in real Chrome (strokes per second should sit an order of magnitude below 1 and rise window-over-window), never by phase arithmetic alone.
10d. **The live engine's mark parser reads `d` + `data-side` only.** Any payload element that is not a `<path d>` is invisible in the live render: rects/polygons/lines/circles parse as empty paths and silently vanish. Emit every mark as `<path d="..." data-side="r|l" stroke fill stroke-width>` — convert other shape elements to path `d` server-side (rect → `M x y h w v h -w Z`, polygon → `M` + `L` joins + `Z`, circle → two half-arcs endpoint-to-endpoint) before shipping. Carry `fill` through when tiles are filled; dropping it renders the tile layer outline-only.
10e. **Arc paths: build them with named format kwargs, never interleaved positionals.** A `.format(...)` whose positional stream and named slots interleave mis-binds — radii land where coordinates belong and a ring draws as a giant slash across the canvas (clipping hides the extent, so the defect survives visual containment checks). Write arcs all-named (`.format(x0=..., x1=..., cy=..., r=...)`) and verify in-browser that ring bboxes are square (width == height).

## Day-1 icon generator

`brand/mosaic-os/src/organism_spinup_icon.py` — deterministic from the organism id:

```
cd brand/mosaic-os
python3 src/organism_spinup_icon.py --org <organism-id> --out /tmp/<id>-day1.svg
```

- Same seed → byte-identical SVG (drift has a stable starting point).
- Different seeds → different right-wing tile sets (org-unique marks).

## Pitfalls

- Personalization mutates the RIGHT wing only — the left phi grid is the conserved gene; drifting both destroys lineage recognizability.
- B2BU personalization ships ONLY through the semantic gate sequence below — never free drift; until gate pass, the standard b2b icon is the honest state.
- **No mark renders without semantics.** A geometric tile thrown onto a wing by hash alone is a defect, not art — marks derive from the user's information (name, values, lifecycle stage) through the symbol library, or fall back to geometric-abstract growth marks. Never hash-only.

## Gate law (semantic derivation — the anti-"shapes without meaning" law)

Full law lives in `brand/mosaic-os/ART-DIVISION-PROGRAM.md` (GATE LAW section); the engine-readable symbol library is `brand/mosaic-os/symbol_semantic_library.json` (cited entries: symbol, meaning, archetypes, cultural caveats, source). Condensed:

- **G0 root genome gate** — every geometric element of the butterfly mapped to a meaning (phi grid = inherited order; irregular tessellation = lived uniqueness; mirror in shape never detail = lineage constant; gold = state-change only). Published dos/don'ts. principal reviews the root before any organism renders.
- **G1 identity research** (per organism, automated) — harvest user info, semiotic map against the library, vacant-territory check vs fleet marks.
- **G2 concept gate** — the required artifact: 2-3 written directions, each argued "based on the user's information, this is the most appropriate answer because..." citing G1; media-independence test (survives silhouette, 1-color, 24px favicon); user confirms before any drawing.
- **G3 derivation gate** — mark generated ONLY from the root genome; lineage verified computationally (distance-from-root within bounds).
- **G4 craft/decode gate** — scale tests, positive-form check, REVERSE semiotic decode (what will a viewer actually read?). Curation over generation.
- **G5 evolution gate** — which parameters may drift, at what cadence, gated on new research; each evolution cycle re-runs G1-G4. Marks accumulate as a visual biography (bud → bloom → fruiting branch); rank/age encoded by size and radial position.
- **Hard gates inside the pipeline:** POSITIVE GATE (affirmational meanings only; decay/judgment/danger/morbidity hard-rejected — "wasp" maps to guardian-of-the-hive, never sting), USER GATE (nothing commits to the genome until the user confirms; rejection blacklists that symbol for that organism), RENDER CONSTRAINT (stroked single-weight path, wing-cell clipped, legible at 24px; monograms only mark type allowed on the body axis).
- **12-month KDP arc** (root → per-organism symbol gates → first personalized frames → first clip → movie horizon) and the **24/7 cadence** (nightly research passes; principal gates by exception only: succession color, genome law, positivity risk, segmentation, split verdicts) are defined in the program doc.

Source methods behind the gate sequence (for extending it): MIT Media Lab shared-grid family marks, Bierut media-independence + evolution-container, Scher immerse-then-draw, Opera Australia every-variable-carries-meaning, Studio Dumbar evolving-core-symbol + AI guardrails, OpenAI Blossom philosophy-first dos/don'ts, dynamic-identity taxonomy (declare the variation mechanism), commercial semiotics (cultural decode before render), vacant-territory gap analysis, and the IASDR finding that in generative identity work the skilled work is the VETTING, not the generating.
- A dead client animator hides behind live-looking server fallbacks — verify by asserting state ONLY the animator produces (a stamp that transitions through hatch labels, growth-group children increasing over time); server-rendered 'live' copy and HTTP 200 both pass while the script is dead.
- Style DOMParser-parsed SVG with `setAttribute` only — `el.style.width` throws on a parsed svg root (no computed style until adopted into the live document), and a `.catch(function(){})` on the fetch chain swallows the throw silently, so the animator dies with zero console output.
- Hide and reveal through the SAME channel — a CSS `style="opacity:0"` is NOT undone by an SVG presentation attribute `opacity="1"` because CSS declarations beat presentation attributes; every hatch frame then plays invisible while the animator, stamps, and aria-labels all look alive. Set/clear opacity via the style attribute on both sides.
- Paint proof is `getComputedStyle(el).opacity` plus `getBoundingClientRect().width > 0` on the live element — never aria-label, stamp text, or growth-group counts alone. Labels are server data that mutate while paint is dead; a label-based check reported "hatched and visible" over a full screen of opacity-0 frames. On toggle surfaces, non-selected organism views measure 0×0 by design — click that organism's toggle before asserting its visibility.
- Guard board item renderers against NULL `seq` (`seq = int(seq or 0)`) and always pass `seq` when filing items — one NULL-seq row crashes the whole board render with `NoneType.__format__` and the route 404s.
- After ANY edit to the generator, re-verify determinism (two runs byte-identical via `cmp`) and seed divergence (two orgs differ) — a broken seed silently changes every existing organism's icon identity.
- The living engine's `render()` returns the output PATH, not the SVG text — embedding its return value directly puts a literal `/dev/null` (or whatever path) into the page as text while everything still returns 200. Read back the file it wrote, then embed. Verify a served slot programmatically (grep for `<svg` inside the slot slice), not by status code.
- Verify color successions by PIXEL-SAMPLING the raster or XML-auditing the SVG, never by eyeballing one render: decode the PNG deterministically (struct+zlib) and count pixels in the old vs new hue band, or count old/new hex refs inside each cell `<g>` of the SVG. `qlmanage -t` on an UNCHANGED filename serves a STALE cached thumbnail — a recolored asset can read as the old color purely from cache. Force a fresh raster via a unique filename, or treat the SVG source as ground truth.
- Stage cards on `/art` need explicit `id` + `seq` (slug-id law) and the board registered in the `boards` table, or they never render.
- Verify any fetch+rAF animator in real Chrome via playwright — drive the page for several seconds, then count animated nodes — because `--dump-dom --virtual-time-budget` does not execute fetch+rAF loops and falsely reports zero growth; a status-200 curl proves nothing about animation.
- Structural probes that index SVG groups positionally break when the document gains a `<defs>` — derive the group index from the live `querySelectorAll('g')` order at probe time instead of hard-coding indices from an earlier page shape; a defs-shifted read returns `transform: null` and fakes a dead-animator verdict.
- `<script>` blocks extracted for `node --check` still carry their `<script>`/`</script>` wrappers — strip them first or the check dies on `Unexpected token '<'` and a working script looks broken.
- Serve-side mark generators and the live parser must share ONE vocabulary contract: when the generator emits shapes the parser cannot read (or attributes it drops, like `fill`), the live render diverges from the static design while both pass their own checks. Test the pair together — payload from the API, parsed by the real client engine, asserted in real Chrome.
- An embedded animator can pass `node --check` and still NEVER RUN: one function short a closing `}` shifts every trailing scope, the tail `})();` closes an inner function instead of invoking the IIFE, and the top-level calls (`tick(); setInterval(...)`) end up inside a function body nothing calls — page serves the static fallback with ZERO console output. Signature: script present in the DOM, manual `eval` of its text works, no console lines from that script (while other page scripts DO run). Diagnose with a cumulative brace-balance scan per line; assert top-level statements sit at depth 1 inside the IIFE and the last non-empty line is `})();`.
- Batch renderer patches through a Python script with ASSERTED anchors (read the exact assembly lines first via sed -n; a paraphrased anchor fails the assert and aborts before any write) — a hand-typed in-place edit on a 3,000-line renderer file risks paraphrase drift; the assert-first pattern makes every patch all-or-nothing.

## Verification checklist

- [ ] `/art` renders after changes (curl the route, grep for stage titles); movement zero animates inline
- [ ] Generator: byte-identical rerun + seed-divergence both hold
- [ ] Color succession: new assets pixel-count 0 in the retired gene band; SVG audit confirms lineage cells keep the old gene
- [ ] Hatch PLAYS on first view AND PAINTS: real-Chrome playwright wait, assert stamp/aria transitions through hatch stages to the imago species form within ~10s, growth marks accumulate, AND `getComputedStyle(svg).opacity === '1'` with rendered width > 0 per organism (label checks alone pass while frames are invisible)
- [ ] Liveness verified by FRAME-TO-FRAME GEOMETRY DIFF in real Chrome: sample the animated root's `transform` (and total drawn-path count) at ≥3 intervals ≥0.5s apart — every consecutive sample must differ. Opacity, stamp, and child-count checks all pass on a frozen slideshow; only geometry that changes between samples proves the engine draws.
- [ ] Any scene render keeps the positivity invariant: no decay/judgment imagery keyed to low health signals — low signals must ADD encouragement
- [ ] Surface changes logged via `events` row `kind='design-major'` (design_changes is a view)
- [ ] Any B2BU-adjacent feature checked against the segmentation law before build (the CURRENT text in ART-DIVISION-PROGRAM.md, not this file's summary — principal amends by order; research seats dispatched under a stale copy of the law will plan the wrong routing)
- [ ] Any new wing mark passed the semantic gate chain (or is the geometric-abstract fallback) — hash-derived tiles are a defect even when geometrically valid

## Learning journal (the AI's art education, visible)

The organism's art education is a first-class surface: a "Learning journal" section on `/art`
reads the boards events ledger (kinds design-major/design-minor/gate/ceo-journal-jump),
newest first, and renders each entry with its WHY as a "learned:" line. The education runs
BOTH directions — the principal's verdicts land as lessons, the organism's redraws land as
measurements; show both, because the surface exists to make the self-teaching visible to
the user too (an Emerson-style two-way education). Rules:
- The journal SELF-UPDATES from the events table — never hand-maintain prose; a new design
  event appears on the next render with zero extra work.
- Write every art lesson as an events row whose body carries `what changed why: <the
  verdict/mechanism that taught it>` — the "why:" split is what the renderer keys on; a
  body without it renders with no learned line.
- Seed the journal by backfilling the arc's real lessons (principal verdicts + physics of the
  fix) as events rows with kind design-major/design-minor — the section must open as an
  education in progress, never an empty shell.
- Skip noise bodies (`status set`, `QA probe`) — they are bookkeeping, not learning.
- Verify in real Chrome: heading present, entries render, zero console errors.
