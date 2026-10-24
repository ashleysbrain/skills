# Conductor surface (:port) surgical edits — 2026-08-31

Session: principal orders 08-31 — FLOW-page dropdown leak fix, calendar
drawers that action items, physics-ranked dispatch mint (T-260831-0051),
FLOW de-clump (group-by), header declutter. Three surface fixes shipped.

## The surface's shape

- organism/conductor_screen.py = ONE Python file holding
  CONDUCTOR_SCREEN_HTML (~3600 lines: HTML + CSS + inline JS as a raw
  string). Edits are string surgery inside Python, not template files.
- Served by organism/conduction_daemon.py under launchd label
  com.your-org.conduction-daemon (listens :port). Python caches
  the imported module — edits do NOT go live until restart:
  launchctl kickstart -k gui/(uid)/com.your-org.conduction-daemon
  (~3s to re-listen).

## Deploy discipline (a syntax bug shipped before this existed)

1. Edit the .py file.
2. BEFORE kickstart: extract the script blocks from the EDITED FILE (not
   the stale server) and run node --check on them. A JS block comment
   placed between string-concatenation terms is a SYNTAX ERROR (comment
   inside an expression); python lint cannot see it because it lives
   inside a python string. Comments go BETWEEN complete statements only.
   (Shipped bug: this exact class reached the live surface; caught only by
   post-deploy node check.)
3. Duplicate-ID check: for every id you touch, the id must appear EXACTLY
   once in the served HTML. Real case: a new panel was given the id
   ft-views while a saved-views select already owned it — browsers bind
   only the first; logic breaks with zero errors shown. Rename panels
   distinctly (ft-viewspanel).
4. AFTER kickstart: re-fetch the live page, re-run structural asserts AND
   node --check on the SERVED js (guards stale-module serving).

## Escaping layers (python to HTML to JS-in-HTML)

When a python replace() writes JS containing backslash sequences
  (escaped quotes, regex digit classes), count the backslashes at the
  SERVED layer, not the source layer — three transformations sit between
  intent and browser. Verify regex literals byte-for-byte in the fetched
  page.

## Pattern: control-pile collapse (FLOW filter bar)

Symptom: more than ~6 controls in one flex-wrap row wrap into a tall
  stack that shoves content down and bleeds across sections (principal: long
  list of dropdowns on the upper left leaking into other sections).
Fix: two toggle buttons (Filters / Views) plus hidden panels (CSS class
  toggling display none/flex). KEEP ALL ORIGINAL SELECT IDs in the DOM so
  render logic reading them is untouched — zero JS logic changes, pure
  re-housing. Active-filter count badge refreshed in the render tail.
  Search + row count stay always-visible in the top bar.

## Pattern: dense-table de-clump (group-by)

Symptom: principal pastes the page back with "this information is all clumped
  together" — hundreds of undifferentiated rows read as noise even when
  every filter works.
Fix: a Group-by select (stage / lane / state / kind / none) whose change
  re-renders the table with one sticky section header row per group
  (CSS: tr.ftgroup td { position:sticky; top:<column-header-height>px;
  background:var(--panel2); color:var(--gold) }) plus a count badge per
group, and the footer count extended to "N of M rows · K groups".
DEFAULT = the field that exposes process truth (stage), so the flat
database view becomes the process-flow view with one control. Measured
result: 400-row pile resolved into 13 groups and surfaced the real
bottleneck (323/400 sitting at tri:review) as a UI-level discovery.
Implementation shape: in renderFlowTable, after sort, if group key set,
walk rows and emit a group-header row whenever the key changes; body
rows unchanged; sticky offsets stack (column header top:0, group header
top:<header height> — measure, do not guess).

## Pattern: header declutter

Symptom: H2 title + span subtitle with float:right renders as smashed
together text ("databasen viewevery row live"). Floats inside flex-less
headers are a defect class on this surface.
Fix: h2 { display:flex; align-items:baseline; justify-content:space-
between; gap:12px; flex-wrap:wrap }, span drops float, gains
font-size:11.5px + dim color so it reads as metadata. When principal says a
label is junking up the design, REMOVE the label outright ("database
view" deleted; header reads exactly "Flow ledger") — do not re-style
what the principal asked to disappear.

## Pixel verification battery (principal correction: "you didn't screenshot
this to triple check your work")

STRUCTURE CHECKS ARE NOT VERIFICATION. grep + node --check prove the
strings exist and parse; they say nothing about rendering. After any
principal-visible surface change:
1. Playwright + system Chrome (chromium is NOT in the playwright cache;
  use executable_path='/Applications/Google Chrome.app/Contents/MacOS/
  Google Chrome'; playwright module importable from /<workspace>
  hermes-agent/venv/bin/python).
2. Screenshot full viewport AND zoom-crop the changed region (element
  locator screenshots or clip rects) — small regions audit reliably,
  full pages hallucinate.
3. Read the screenshot with vision, BUT never trust vision alone:
  it hallucinated a tab-strip overlap that bounding-box measurement
  disproved (measured gaps 7-8px uniform). Pair every visual claim with
  DOM measurement: getBoundingClientRect on the elements in question.
4. Vision provider format quirks: PNG at device_scale_factor=2 gets
  rejected; convert to JPEG (PIL convert('RGB'), quality~88) or shoot at
  1x. Intermittent duplicate/empty results — retry once.
5. Verify visible TEXT via DOM textContent of the served page, never
  curl|grep: grep counts JS comments too (a "database view" hit turned
  out to be a code comment while the visible header needed a separate
  check).

Design complaints route through the creative spine (the specialist engine pass)
  even when the fix is one word — "verified live" must mean pixels.

## Pattern: no dead-end drawers (calendar action row)

Symptom: a drawer ends with a note like use-the-Flow-view — a dead end;
  the principal cannot action from where they are.
Fix: every card drawer offers motion through EXISTING efferent limbs —
  never invent new write paths:
- respondTo(tid, source) (nonce-gated /api/respond, teach-the-OS modal)
  on EVERY item;
- a Full-detail button calling drill(kind=task) for ledger-backed items
  (T-*, mosaic_, cron_ prefixes) — that drawer already renders
  Approve/Reject/Defer for kind=decision tasks under the two-step
  confirm law.

Measured /api/calendar item types (2026-08-31): task, event, milestone,
  social, content — NO decision type arrives, so ruling buttons keyed on
  a decision type render only for future-typed items; today's decisions
  action via Full detail. Do not fake affordances: dormant limbs must be
  labeled dormant or they read as broken.

## Per-deploy verification battery

- node --check on served inline JS (syntax gate) — BEFORE kickstart
- structural asserts: ids present, id counts exactly 1, wiring strings
  present
- API shape check BEFORE keying UI on a field value (query the endpoint,
  list the actual types/states that arrive)
- pixel battery above for principal-visible changes
- confirm prior fixes still intact after any re-deploy (regression
  coupling: FLOW collapse, group-by, and calendar action row share one
  file/daemon)
