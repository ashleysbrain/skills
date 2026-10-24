# Vision-audit reliability: screenshot verification you can trust

Added 2026-08-31 after a principal correction ("you didn't screenshot this to
triple check your work") — structure checks (grep, node --check, curl
asserts) had been reported as verification while rendering defects
shipped. General technique for any headless UI QA battery.

## The stack (all three layers, never one)

1. SCREENSHOT (ground truth): Playwright, system Chrome via
   executable_path (chromium is often absent from ms-playwright cache on
   this host; /Applications/Google Chrome.app works). Full viewport for
   layout context + element-locator/clip screenshots of the changed
   region.
2. DOM MEASUREMENT (arbitrator): getBoundingClientRect on the elements
   in question — gaps, overlap, containment. When vision and pixels
disagree, MEASUREMENT WINS. Observed: vision claimed a tab strip
   overlapped; measured gaps were 7-8px uniform, zero overlap — pure
   hallucination.
3. VISION READ (describer): good at "what does this look like", bad at
   counts and geometry. Use it to describe, then confirm every concrete
   claim it makes with a measurement before believing it.

## Vision provider quirks (observed 2026-08-31)

- PNG shot at device_scale_factor=2 → rejected/failed reads. Shoot at 1x
  or convert: PIL Image.open(...).convert('RGB').save(path, quality=88).
- Intermittent duplicate/empty results — retry the call once before
  concluding anything.
- Small zoomed crops audit reliably; full-page asks invite confabulated
  defects ("faint grid pattern" nobody could find at pixel level).

## Text claims: DOM, not grep

Verifying visible text with curl|grep counts JS comments and dead code.
Read document textContent of the served page (or the specific element's
innerText) for "does the user see X" questions. Real case: grep found
"database view" once — it was a code comment; the visible header was
already clean, but only the DOM check proved it.

## Workflow shape

- Deploy first? NO: syntax-gate the edited source, deploy, then run the
  battery against the SERVED page (stale-module serving is real).
- For every principal-visible change: full-viewport shot + zoom-crop of the
  changed region + measurement of any spacing/overlap claim + DOM text
  check of changed labels. Report "verified" only after pixels.
- Regression coupling: batteries re-run prior-fix checks too when
  changes share a file/daemon.

## Polling pages: wait_for_load and the beat race (2026-08-31)

Dashboards that self-refresh on a timer (e.g. a 5s `setInterval` beat
rebuilding innerHTML) break the standard battery assumptions:

- **`wait_until='networkidle'` never fires** — the poller keeps the
  network busy forever and the battery times out at goto. Use
  `wait_until='domcontentloaded'` + a fixed sleep (4-6s).
- **Panels render on the BEAT, not on click.** A tab switch that merely
  sets `window.__VIEW` fires its data fetch only on the next tick of the
  refresh loop. A screenshot taken 1-2s after the click catches an empty
  panel — which reads exactly like a render defect. Probes: wait ≥2 beat
  cycles (10-12s) before declaring a panel dead; if still empty, call the
  loader directly (`page.evaluate("() => loadImmune()")`) and check
  whether the fetch fires — that splits "render bug" from "beat race" in
  one step. (Observed: panel empty for 3 probes, then 5 fetches + full
  render after a direct loader call — no defect at all.)
- **Element-ref churn:** geometry-read + click in the same JS tick
  (already the law for re-render loops) — applies to every probe on a
  polling page.

## Native title-tooltips never appear in screenshots (2026-08-31)

`title="..."` tooltips are drawn by the OS/browser chrome, not the DOM,
  so hovering + screenshotting PROVES NOTHING about tooltip content —
vision will (correctly) report "no tooltip visible". To verify a tooltip
  limb: read the attribute via DOM
  (`el.getAttribute('title')`) and assert its exact content instead.
If a change's whole purpose is human-visible-on-hover, consider an
in-page tooltip component at build time; otherwise DOM-read is the
  verification.

## Schedule display law for periodic processes (2026-08-31)

principal asked "why was the system QA done over 40 hours ago??" — the QA
engine was healthy (idle-by-design inside its 48h write-ahead window,
next passes hours away), but the surface showed only AGE (`live · 46h`),
which reads as neglect. Rule for any surface that displays a periodic
process: **show the period, not just the age** — `live · 46h · next in
2.2h` kills the misread at zero cost. Mirror the engine's own threshold
constant (single source of truth; compute `next = threshold − age`, floor
at 0) rather than shipping a second schedule that can drift.
