---
name: headless-ui-qa-batteries
description: 'Use when live-verifying UI changes via Playwright batteries. Pixel law (screenshot + DOM measurement + vision read, never one layer alone); beat-aware waits on polling pages.'
---

# Headless UI QA Batteries

Class-level skill: replayable Playwright batteries that verify UI changes the way users
actually hit them. Born from the Writing Studio session-fold passes (34 defects across
3 adversarial reviewers, all closed live).

## When to use

- Any frontend change that must be verified "live" (principal standard: offsetWidth > 0, never
  code-read or screenshot-only)
- Replaying an adversarial reviewer's defect list as a regression battery
- Verifying a multi-step user flow (collect → combine → act) end-to-end

## Setup (macOS host)

```js
const pw = require('/<workspace>');
const browser = await pw.chromium.launch({
  executablePath: '/<workspace>',
  headless: true,
});
```

- browser_exec blocks localhost — use node scripts, not the browser tool.
- Write batteries to /tmp/<name>.cjs; keep one battery per defect-family so failures isolate.
- **Battery file format (2026-08-26, 3 failed runs):** write .cjs with the whole body wrapped in
  `(async () => { ... })().catch(e => { console.error(e); process.exit(1); })` — top-level await in a
  .cjs is a SyntaxError and renaming to .mjs breaks the `require()`. Keep `require`, wrap in async.
- **Headless binary path rots:** the versioned path (mac-131…) may not exist; list
  `/<workspace>` and use the newest `mac-*/chrome-headless-shell-mac-x64/chrome-headless-shell`.
  A "binary doesn't exist" launch error with the file present on disk usually means the version dir is wrong.

## The five rules that catch real bugs

1. **Real clicks, not evaluate().** `element.click()` at coordinates — nested
   button-in-anchor layouts, overlay interception, and z-index traps only reproduce with
   real hit-testing. A battery that only calls functions misses them (this shipped a
   BLOCKER: buttons worked via evaluate, 422'd via real clicks).
2. **Auto-accept dialogs BEFORE the flow.** Playwright auto-DISMISSES confirm() by default —
   a graduate/delete behind a confirm() silently no-ops and the battery reports a false
   failure (or worse, false pass on the error path):
   `page.on('dialog', d => d.accept());`
3. **Intercept the POST, not the response.** When a click "doesn't work", wrap fetch and
   print the actual request body — a double-stringified JSON payload (`JSON.stringify(JSON.stringify(x))`)
   was invisible until the wire was inspected. Fix at the decode site: loop-parse until
   the payload is an object.
4. **Probe IDs rot; grep the source for real IDs first.** Batteries fail on stale element
   IDs (sessList vs sessBody, hubQuery vs unifiedSearchInput). Read the DOM block before
   writing the probe, and when a probe fails, classify: element missing = probe bug;
   element present but 0×0 or hidden ancestor = product bug.
5. **Visible = offsetWidth > 0 AND offsetHeight > 0.** Existence checks pass on
   display:none nodes. Paint proof requires nonzero geometry (principal standard).

## Probe-vs-product discipline (the biggest time sink)

When a battery check fails, run the split test before patching the product:
- Call the function directly via evaluate → works? The wiring/trigger is the bug (event
  delegation, hidden tab, overlay).
- Direct call also fails? The function/endpoint is the bug.
- Element exists but rect 0×0? Walk `getComputedStyle` up the ancestor chain for the
  hiding node — sub-tab panels (`display:none` until a tab activates) and duplicate
  inline `display` declarations are the usual culprits.

## Battery pitfalls with drawers, overlays, and case (2026-08-26, respond-limb session)

- **CSS `text-transform: uppercase` breaks label matching.** Buttons rendered
  `RESPOND` while the source said `Respond`; an exact-match battery reported
  "0 buttons" and nearly filed a false product defect. Always compare
  `innerText.toUpperCase()` in probes.
- **Set the viewport explicitly before testing right-side drawers.** Default
  1280×720 clips a drawer starting at x=1000 (drawer x1000+width 440 = 1440).
  Symptom: `element is outside of the viewport` retry loop on a perfectly
  visible button. `await page.setViewportSize({width: 1440, height: 900})` or
  read `getBoundingClientRect` first and size accordingly.
- **Modals injected INTO the drawer body die with the drawer.** Calling
  `closeDrawer()` to "clean up" between steps also hides any modal that lives
  inside it — sequence battery steps so the drawer stays open for the modal's
  whole lifecycle, and close only after asserting.
- **On pages with re-render pollers, prefer coordinate clicks with fresh
  geometry** over `locator.click()`:
  ```js
  const [x, y] = await page.evaluate(() => {
    const r = document.querySelector('#target').getBoundingClientRect();
    return [r.x + r.width/2, r.y + r.height/2];
  });
  await page.mouse.click(x, y);
  ```
  The geometry read and the click happen in the same tick, so a 5s innerHTML
  rebuild between "found" and "clicked" can't detach the handle.
- **`pkill -f <daemon>` can miss and lie.** After a pkill+restart, the served
  bytes may still come from the OLD pid (venv python path differs from the
  pattern you expect). Verify by pid: `ps aux | grep [d]aemon`, `kill <pid>`,
  restart, THEN `curl | grep` for a marker from the new code before running
  any battery. A "product bug" that is really a stale process wasted a full
  debug loop here.
- **An open drawer intercepts pointer events on the main view.** After opening
  a drawer (even via evaluate), clicks on underlying cards fail with "intercepts
  pointer events". `closeDrawer()` (the surface's own function, not just
  removing the modal) before returning to main-view clicks.

## Event delegation over inline onclick

Inline onclick + JSON payloads breaks on apostrophes in titles and double-encoding.
Convert to `data-*` attributes + one delegated listener:
```js
document.addEventListener('click', e => {
  const btn = e.target.closest('.sess-collect');
  if (!btn) return;
  const payload = btn.dataset.sessItem;  // single-encoded, apostrophe-safe
});
```

## Write-path batteries: verify the persistent side effect, not the HTTP 200

A POST that returns `{ok: true}` has proven nothing. When a click creates a
decision/record, read back EVERY durable effect the click claims to produce:

1. The store row itself (state transition, if any).
2. The append-only event/audit record (actor + kind + payload).
3. Every downstream carrier the write fans out to (message-bus message,
   webhook, queue entry) — read the actual target store, not the writer's
   return value.

Live pattern (the OS Task Console, 2026-08-26): `curl POST /api/decide
approve` → assert `tasks.state='done'` AND `task_events` has the
`ceo-approve` row (actor `ceo/human`) AND `message-bus.db messages`
contains the `ceo-ruling` row. Three assertions, one battery. The bus leg
is the one a silent except-block eats most easily — wrap carrier posts so
carrier-down degrades (returns `bus_msg: null`) without blocking the ruling,
then surface the null in the response JSON.

## Vacuous-verification trap: an empty result is not a pass (2026-08-27, review-2 panel catch)

The most dangerous false positive of the session: "verifying" a store write
with a query that matched nothing and echoed OK anyway — `sqlite ... SELECT
event FROM task_events WHERE ...` printed no rows, exited 0, and the check
said `ledger leg OK`. An adversarial panel then proved the write had NEVER
worked (4/4 failures, 100% broken since first build). Rules:

- Assert on the DATA ROW, never on the exit code: the check must print or
  count the actual returned row and fail loudly when it is absent.
- `bash -c 'cmd && echo OK'` where cmd outputs nothing is a vacuous pass —
  pipe through a row-count assert (`| grep -c <expected>` and compare to N).
- A `try/except: field = False` in the writer that the checker never reads
  means the writer can fail forever while the UI shows success. Surface the
  error (return `ledger_error`/`store_error` in the API response) so the
  next verification can see it.
- The same session's root cause: an ID-format regex (`T-\d{8}-`) that never
  matched the store's legacy 6-digit generation — the gate silently skipped
  286 rows. Grep the REAL store for actual ID shapes
  (`SELECT DISTINCT substr(id,1,12)`) before writing any ID validator, and
  when a gated write reports zero successes, suspect the gate before the
  writer.

Hardening patterns from the same review pass (CSRF Origin gate,
X-Frame-Options/CSP headers, flock+atomic-rename for jsonl stores under
threaded servers, honest multi-store response reporting):
`references/review2-hardening-2026-08-27.md`

## Server-state hygiene

Batteries create rows. Purge probe artifacts after each pass (identifiable prefixes like
"QA process", "empty", "R 3") — keep only real user data. A drawer full of test sessions
is itself a defect a reviewer will file.

## Related skills

- `dogfood` — exploratory QA (this skill is the battery/replay side)
- `ai-tell-removal-gate` — pre-presentation cleanup after QA passes
- Triangle-offense tri-group volley + pass-count stop law (SHIP = 2
  consecutive rotated cleans; findings reset the streak; fixer never
  confirms its own fix): `references/triangle-offense-pass-count-law-2026-08-27.md`
- Adversarial Fleet v2 engine-first review (Ravine/Ring-1/Nullius — use the
  organism's QA organs before dispatching ad-hoc panels):
  `references/adversarial-fleet-v2-engine-first-2026-08-27.md`
- Session detail for the conductor-screen scenario lens, visibility law,
  and drill rebuild: `references/conductor-screen-lens-and-drill-2026-08-26.md`
- FLOW view surgery 2026-08-31 (toolbar collapse + group-by de-clump +
  list-level task timelines, event-histogram "nothing moved" diagnosis,
  escaping traps): `references/conductor-flow-view-surgery-2026-08-31.md`
- Live/history view split + header-law surgery 2026-09-01/02 (archive mode,
  truly-done receipt audit, state-boundary battery, live-count header):
  `references/flow-live-history-split-2026-09-02.md`
- the OS Console session (escaping collapse, census truncation bug,
  kickstart→bootout escalation, three-assertion write-path battery):
  `references/console-census-escaping-2026-08-26.md`
- UI design laws from the 2026-08-26 corrections — drawers over tabs,
  census-then-extend, surface marriage, direction-on-record:
  `references/ui-design-laws-conductor-2026-08-26.md`
- Pixel-law verification stack (screenshot + measurement + vision,
  vision hallucination arbitration, provider quirks, polling-page beat
  races, title-tooltip DOM-read law, schedule display for periodic
  processes): `references/vision-audit-reliability.md`
- principal respond limb (teaching channel beyond ruling): `/api/respond`
  four-store write pattern, ADHD modal, verification battery:
  `references/conductor-respond-limb-2026-08-26.md`

## Live-preview pane as verification channel (2026-08-26)

When no headless browser is available (browser_exec blocks localhost,
puppeteer MCP down), the in-app preview pane (`open_preview` + `drive_preview`)
IS a real browser and verifies live behavior:

- `drive_preview action=click` with returned element refs = real clicks.
- Read state via `read_preview` (visible text) — the URL/title/hash fields
  confirm navigation and JS-driven state changes.
- CAUTION: pages with a fast re-render loop (5-30s pollers rebuilding
  innerHTML) constantly invalidate element refs — re-snapshot `elements`
  immediately before each click, and treat "ref removed" as a re-render
  race, not a dead element.

## Daemon-served HTML: verify the SERVED bytes, not the source file

Python daemons that serve embedded HTML strings (e.g. conductor_screen.py's
CONDUCTOR_SCREEN_HTML) cache the module at process start. After editing the
source, `curl the page | grep` for a marker from your NEW code — if absent,
restart the daemon (`launchctl kickstart -k gui/$(id -u)/<label>`) before
concluding the JS is broken. Two full debug loops in one session were caused
by testing edits against a stale in-memory page. If `launchctl kickstart -k`
still serves stale bytes (err log shows old line numbers), escalate to a full
`launchctl bootout gui/$(id -u)/<label>` + `bootstrap` — kickstart alone
re-execed the old module in one 2026-08-26 case.

## JS syntax gate for embedded HTML (one command)

```bash
curl -s http://127.0.0.1:PORT/page > /tmp/s.html && node -e "
const s = require('fs').readFileSync('/tmp/s.html','utf8');
const js = s.split('<script>')[1].split('</script>')[0];
try { new Function(js); console.log('JS SYNTAX OK'); } catch(e){
  console.log('JS SYNTAX ERROR:', e.message); }"
```

Catch this BEFORE browser testing. Recurring bug class when patching
embedded JS: ternary strings losing a quote (`'</div> : ''` instead of
`'</div>' : ''`) — check copied `dl = (k,v) =>` helper lines first. When
bisecting for the bad byte, do it LINE-wise, not byte-wise: naive byte
bisection splits multibyte UTF-8 (em dashes) and reports false errors.

## Multi-layer escaping in daemon-embedded HTML (2026-08-26)

When a Python string holds a JS string that holds HTML that holds prose, an
apostrophe in the prose (`organism's`) collapsed `\\'` to `'` across the
Python layer and broke the WHOLE page with `Unexpected identifier 's'` —
while the source file looked fine on read. Rules:

- Prefer apostrophe-free copy in embedded JS strings; cheaper than a
  triple-escaping audit.
- The served-bytes JS gate above catches this class in one command — run it
  after EVERY edit to an embedded page, before any browser testing.
- Fastest localization: extract the script block from SOURCE and from SERVED
  and byte-compare (`src == served` in python3); the first differing byte IS
  the bug, no bisection needed. A line-wise `new Function` prefix scan gives
  false positives mid-function — do not trust it as a locator.

## Probe payloads: parse full JSON, truncate only the display

A fleet /health census reported 19/21 engines "down" because the probe read
`.decode()[:400]` BEFORE `json.loads` — engines with longer health payloads
failed to parse and scored as dead (real state: 21/21 alive). Truncate what
you SHOW, never what you PARSE.

## Debug crumbs in served pages (install deliberately, remove after)

For click paths that silently fail: `window.onerror` writing to
`location.hash` (`#JSERR:...`) survives re-render loops and is visible in
the pane URL, unlike document.title (not surfaced) or DOM text nodes
(clobbered by pollers). Persist interactive state to the hash too
(`#scen=b2c`) so a reload restores and proves the handler ran.

## Pre-build design gate: is a canonical surface already the answer? (2026-08-26)

principal correction after a fresh tab-based console shipped: "you just erased
our hard work." Before building ANY new UI surface: (1) census existing
surfaces (ports, daemons, sibling sessions) for the capability; (2) if a
canonical surface covers it, EXTEND it (new view + daemon query patch +
restart) rather than shipping a parallel page; (3) the house interaction
model is dense interactive lists + slide-out drill drawers + in-drawer
actions — top-tabs with plain panes reads as a regression even when
feature-equivalent; (4) when a secondary surface wins praise for one token
(font scale, color), port the token INTO the canonical surface. Full laws
+ verbatim corrections: `references/ui-design-laws-conductor-2026-08-26.md`.

## Daemon API queries go stale like served bytes do (2026-08-26)

After ledger semantics change (new claimed_by conventions, state usage,
grammar folds), grep every API consumer query, not just the page HTML. The
Conductor daemon's rulings query still surfaced fleet-claimed decisions and
missed a human-only task after autonomous triage — page JS was fine, the
SQL was the defect. Fix pattern: patch the query, `python3 -m py_compile`,
kickstart the daemon, re-curl the API, THEN reload the pane.

## Ledger detail JSON + trailing archive = parse-hardened reader required (2026-08-26)

The relabel surgery appends a verbatim markdown archive AFTER the JSON
object in `tasks.detail` (`{"ceo_brief": ...}\n#### ORIGINAL TITLE...`).
Every strict `json.loads(detail)` in a consumer FAILS on the trailing data
and silently rendered empty decision briefs — the archive law and the
consumers were in conflict. Fix pattern (read-side only, archive untouched):

```python
def _parse_detail(raw):
    if not raw: return {}
    try:
        obj, end = json.JSONDecoder().raw_decode(raw.lstrip())
        if isinstance(obj, dict):
            tail = raw.lstrip()[end:].strip()
            if tail: obj.setdefault("archive", tail)
            return obj
    except (ValueError, TypeError):
        return {}
    return {}
```

Grep every `json.loads` that touches a stored `detail` field when the
archive law is in force. Honest-fallback law for human queues: when no
brief exists, derive `what` from the record itself (archive text stripped
of `^#+` headers, or the title) and SAY "no brief was written at mint" —
never fabricate a plausible one.

## Nested-quote JS in Python-embedded HTML: quote-free wiring (2026-08-26)

Building `onclick="fn('arg')"` inside a JS string inside a Python string
collapsed to broken quadruple-backslash escapes — served JS was syntactically
dead while the source looked plausible. The JS syntax gate caught it, but the
robust fix is to AVOID nested quotes entirely: emit `<button data-topic="x">`
and attach one `addEventListener` that reads `ev.target.getAttribute(...)`.
Same pattern as the event-delegation rule above; apply it at AUTHOR time for
any dynamically-built control, not just apostrophe repair.

## Glyph batteries (2026-08-26)

When a surface ships inline-SVG button glyphs, assert three layers, not one:
(1) `svg` presence inside each labeled button; (2) geometry (13×13 by CSS);
(3) `getComputedStyle(svg).color` equals the button's token color —
`stroke="currentColor"` means the icon inherits the button color, and this is
the assertion that catches a glyph wired to the wrong class. Static-HTML
buttons cannot use JS `g()` interpolation — the interpolation renders as
literal text in HTML context (raw inline SVG required there); a battery
checking `header button svg` count catches that class instantly.

## Route shadowing in prefix-matched HTTP handlers (2026-08-27)

DoGET/DoPOST handlers that dispatch on `self.path.startswith("/api/metrics")`
SHADOW any longer sibling route (`/api/metrics/series`) added BELOW them —
the new endpoint returns the parent's payload and every consumer sees subtly
wrong data with HTTP 200. Three defenses:
- Order matters: put LONGEST paths first (`/api/metrics/series` ABOVE
  `/api/metrics`), or match exact-prefix with a separator
  (`path == "/api/metrics" or path.startswith("/api/metrics/")`).
- Battery: after adding any route, curl the NEW path and assert a KEY that
  only the new payload has (`'events' in resp` for series, absent in the
  metrics rollup) — a 200 with wrong shape is the failure signature.
- Grep for sibling `startswith` on the shared prefix before inserting;
  the shadowing is invisible in a syntax check and a py_compile pass.

## Date drill-down battery: DOM numbers must match the API (2026-08-27)

For time-series surfaces (time-span chips 7d/14d/30d/90d, day/week/month
buckets, per-flow small multiples): fetch `/api/metrics/series?days=N` in the
battery, compute expected totals in JS, and assert the DOM-rendered bar
count/total equals the API JSON bucket count. Research-derived layouts
(Instana/Kibana simultaneous zoom, Tufte small multiples shared scales,
period-over-period delta rows) each need their own assertion: chip click
refetches with new `days` param, bucket toggle regroups, and the delta row
compares span N vs previous span N (fetch both, assert the sign matches).

## Brand-voice engine scans: split rendered copy from source (2026-08-27)

the specialist engine's `/v1/review` (POST the served HTML) flagged 25 em-dashes, 37
exclamations, and a banned dimension name — but it scans the FULL source
including JS comments and code. Before rewriting anything, re-run the scan
against RENDERED text only (headless: walk every view, collect
`document.querySelector('main').innerText`, count violations there). In the
live pass: all 37 exclamations were comment noise (0 rendered), "emotional"
rode in from ledger DATA rows (task titles written by other agents — not UI
copy to silently rewrite), and only the ~6 authored em-dash strings were
real fixes. Engine verdict + rendered-copy split = accurate brand lint;
engine verdict alone = over-correction.

## Time-series bucketing: ISO weeks, user-local "today", midnight boundary (2026-08-27)

Date-grouped analytics surfaces (found by a rotated pass AFTER two clean
passes missed it):

- **Week buckets: use `isocalendar()`, never `strftime('%W')/('%U')`.**
  `%W` (W34) contradicts ISO week numbers (W35 for the same date) —
  internally consistent, wrong to the world. Label `f"{iso[0]}-W{iso[1]}"`.
- **Bucket in the USER's timezone, not UTC.** With UTC days, the principal's
  "today" bar froze at 18:00 America/Chicago. Convert each stamp via
  `astimezone(ZoneInfo('<user-tz>'))` (naive stamps = UTC assumed), make
  cutoffs local too, and add a plain-words note in the UI
  ("times in your timezone").
- **Battery: the midnight-boundary test.** UTC-early-hours stamps
  (`2026-08-27T02:00+00:00` = Aug 26 21:00 Chicago) MUST land on the
  previous local day. Query raw rows in the UTC-early window, recount by
  local date in SQL/Python, and assert the API bucket equals the recount
  exactly (live proof: 1539 == 1539).
- **Delta rows: guard div-by-zero.** Previous span = 0 → render `n/a`,
  never NaN or a fabricated percent.

## Status-strip metrics: measure motion, not state (2026-08-31)

principal order after "20 moving" sat frozen on a shared screen all meeting: the
strip's `moving` counted raw `state='claimed'` — 9 of 20 were zombie seats
claimed 3–13 days earlier with zero progress events. A metric that counts
STATE (a claim, an assignment) instead of MOTION (events in a window) always
lies during stalls, and it lies in the direction that flatters the system.
Rules:

- **Define every live metric over events, not state fields.** moving =
  claimed tasks WITH a progress-class event in 24h — not the claim count.
- **Surface the excluded rot, don't silently drop it.** The 9 zombie seats
  became a visible kv note ("stale seats 9 claimed 3+ days, no progress")
  instead of vanishing from the surface.
- **Fix EVERY producer of the metric, not just the visible one.** The strip
  had three census producers (daemon inline SQL, compose_header.ledger_census
  for Telegram/status, render_hints composer); grep all of them or the lie
  persists on a surface you aren't watching.
- **Honest fallback law:** producers that can't measure events fall back to
  the coarser count — never fabricate the finer one.
- **Audit each number against the raw store before trusting it.** "45 done
  today" survived the audit; "20 moving" didn't. Verify with one SQL query
  per chip before rebuilding definitions.
- Stock counters that CANNOT visibly move (a 561-task tri:review pile) read
  as broken even when accurate — pair them with a flow metric or split them
  (actionable vs review-pile) so the principal sees motion somewhere true.

Session detail (SQL definitions, producer patches, ledger mint→claim→complete
proof-gate mechanics incl. the P1 substance gate and flow-registry validation):
`references/strip-metric-honesty-2026-08-31.md`

## Live-view vs history split: state-scoped list queries (principal order 2026-09-01/02)

principal: "why are there done items in the flow ledger? done items should be
archived… but you must be sure and I don't trust you rn." The live work
list was `SELECT … ORDER BY created_at DESC LIMIT 400` with NO state
filter — 149 of 400 rows were done/cancelled, polluting the active view.
Laws:

- **Live lists scope to active states** (`state IN ('open','claimed',
  'blocked')`); terminal states (done/cancelled) live behind an explicit
  history/archive mode — same table, `archive=1` query param. Birth-
  certificate no-delete law is untouched: this is VIEW discipline, rows
  never move or delete.
- **Verify "truly done" against receipts before archiving** — audit for
  post-done events (rework signals: repair/amend/corrected/re-claim). 39
done tasks carried post-done events; ALL were bookkeeping stamps (taxonomy
  migrations, future-fit amends, notes), zero reopens. Event-kind split is
  the discriminator: bookkeeping (note/ceo_note/minted/ts-normalize/
  verified/deadline-*) vs real rework (repair/amend/corrected/claimed).
- **Battery for view splits: assert BOTH modes + the boundary.** API probe:
live rows ⊆ {open,claimed,blocked} and archive rows ⊆ {done,cancelalled}
(zero pollution both ways); DOM probe: `FLOWTASKS[0..3].state` flips
open→done after the history toggle — the first screenshot pass caught a
banner toggle with NO table re-render because the check looked at the
wrong column (state cell vs lane cell indexing).
- **Header = live measured count + policy + control, never prose summary.**
Same session, same principal: "your headers are also still not fixed… they are
just a summary." `every row live from the task ledger · click a title…`
was rejected; `<N> active · done archived, in history · [history]` with N
wired to the data (re-read on load AND on every mode toggle) is the shape.
A static descriptive sentence on a live surface reads as a stub.

## Patch-tool anchor loss: re-grep symbol counts after structural patches (2026-08-26)

Using a function declaration line (`function popOut(kind, id){`) as the
old_string anchor for an INSERTION, the patch consumed the declaration
itself — the function silently vanished from the served page. The JS syntax
gate passed (the remaining code was still valid) and only a grep for the
symbol found it. REFLEX: after any patch anchored on a declaration, grep the
symbol count before AND after (`grep -c "function popOut"`). When anchoring
insertions, include the anchor line in both old_string and new_string.

