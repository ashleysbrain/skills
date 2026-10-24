# Butterfly Live-Engine Laws

## Vocabulary
- Wing detail = geometric marks only: triangles, quads, pentagons, bars, rings. Each generation builds from the prior design's shapes. Never introduce free-form branch/squiggle generators — they read as 'neuron shapes' and break lineage.

## Containment (structural, not mathematical)
- Marks are born inside per-wing SVG groups; each wing group carries its own clipPath. No detail can spill outside the wing silhouette at any flap angle.
- Route each mark to its wing's clip via data-side="l"|"r" on the wing groups.
- Skip per-mark bbox math: relative h/v commands and arc parameters break naive parsers; the clip makes the math unnecessary anyway.

## Tempo
- Tune the PHASE rate f, never the flap count. When wing amplitude uses |cos(phase)|, perceived flap rate = 2f — the absolute value doubles frequency. Slow look: f ≈ 0.05 Hz at hatch ramping to ≈ 0.15 Hz at cruise.
- Movement starts slow and gradually accelerates as the artistic scenario builds; tie the ramp to scenario-build progress, not wall-clock.

## Liveness
- One rAF loop: stroke-dashoffset draw-on at birth + continuous motion forever. Still-frame swaps are rejected on sight.

## Engine/parser quirks
- The live parser reads only `d` attributes — convert rect/polygon shapes to path `d` before injecting.
- Ring marks: two half-arcs ('A r r 0 1 0 …'), never one arc with swapped radii/coords (renders as giant slashes).
- Build JS templates with .replace, not .format — braces in SVG path data break .format.

## Verification (real Chrome, not screenshots alone)
- node --check the extracted JS before injecting.
- Count rendered marks + tiles; measure tile spill px on all four sides (expect 0); measure strokes/sec in two windows to confirm the ramp.

## Patching the renderer (app_shell_v3.py)
- Locate the section anchors before patching: the art page assembles as
  cards -> lives_html (`One genome, many lives`) -> grove -> lineage, and the
  final html concat is one multi-line expression — patch by asserting the
  EXACT existing string (copy it from a sed -n read of the assembly lines,
  not from memory; a paraphrased anchor fails the assert and aborts safely).
- Insert new sections by defining their html var BEFORE the lives_html
  anchor and splicing into the assembly expression with explicit string
  concatenation lines — never reformat the surrounding expression.
- boards.db is gitignored: commit code changes in app_shell_v3.py, but a
  DB write (card inserts, event backfills) needs `git add -f` or stays
  uncommitted — state which in the commit plan.
- Restart the boards service (launchctl kickstart -k) and re-verify the
  rendered page BEFORE reporting: a syntax-OK patch can still miss the
  anchor subtly and leave the section absent.
