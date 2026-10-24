# CDP census batteries (raw CDP, no Playwright)

Born from the Research Studio adversarial-review prep (2026-08-19): a 17-view census
sweep over a 783KB single-file app. Runnable script: `scripts/cdp-census-battery.cjs`
(configurable via APP_URL / VIEWS / OUT env vars).

## Why raw CDP

`browser_exec` blocks localhost and playwright-core may not be installed; raw
chrome-headless + chrome-remote-interface via NODE_PATH is a two-minute setup that
survives any environment.

## The three probe traps that faked defects (all verified live)

1. **`window[name]` false-positive dead buttons.** A wiring probe using
   `typeof window[fnName]` reported 36/54 dashboard buttons dead. Cause: functions
   defined as `const fn = ...` / `fn = async function` in a script are not window
   properties. Real clicks proved ZERO dead buttons. Correct check:
   `eval('typeof ' + name)` in page scope. Dead-wiring claims are only reportable
   after real clicks with effect measurement.
2. **Multi-statement onclick parsing.** `event.stopPropagation();realFn('id')` —
   `onclick.split('(')[0]` yields `event.stopPropagation`, inflating dead counts.
   Split on ';' first, take the LAST segment, then extract the name.
3. **Nav labels are not view ids.** "Brainstorm" nav button routes to `view-compose`;
   "Workshop" routes to `view-drafts`. A view-id census must map nav labels to actual
   view ids before declaring a view missing. Also caught: a section with content but
   zero inbound nav items (orphaned surface — a real defect class).

## Click-effect measurement (three signals)

View-switching clicks can show DOM-delta 0 if measured too soon. Settle 1200-1500ms,
then record together: (a) DOM length delta, (b) visible view ids
(`[id^=view-]` filtered by offsetWidth>0), (c) network calls fired
(Network.requestWillBeSent filtered to `/api/`). Interpretation: changes nothing in
all three = dead; network only = silent-action bug; navigation only = no-op-action bug.

## Runtime.evaluate gotchas

- Async IIFEs need `awaitPromise: true` or they return `{}`.
- Wrap every in-page probe in try/catch returning `{probeErr}` — one throwing view
  must not kill a multi-view sweep.
- Never embed `${var}` in JS strings written from Python raw strings; the template
  never substitutes (killed a 53-second battery at output-write time).

## Frontend↔API cross-reference (orphan-route detection)

Route-to-UI matching by literal string fails on apps that build URLs dynamically
(template literals + concatenation). Three-stage refinement, most-recent first:
1. Literal match of UI endpoint strings against declared routes (~50% coverage).
2. Template-literal-aware wildcard match (`${id}` → `*`).
3. Fragment test: for each route, grep the frontend for its DISTINCTIVE segments
   (skip generic words like status/list/run/next). A route whose distinctive segment
   appears nowhere in frontend source is truly orphaned. Result on the studio: 186
   routes → 123 "uncalled" by stage 2 → **4 truly orphaned** by stage 3. Report stage-3
   numbers only; earlier stages are probe artifacts.

## Parallel reviewer lane separation

Multiple subagent reviewers probing one app concurrently must get exclusive resource
lanes in their dispatch context: one owns the chrome CDP port; others are static-file
+ curl-API only. Shared browser profiles produce phantom defects from interleaved
probes.

## Verified working setup (macOS)

```bash
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  --headless=new --remote-debugging-port=9333 \
  --user-data-dir=/tmp/rs-qa-profile --disable-gpu about:blank &
npm install --prefix /tmp/rs-qa chrome-remote-interface
NODE_PATH=/tmp/rs-qa/node_modules node cdp-census-battery.cjs
```

Auth token: read from the app's .env (never print it), inject via localStorage
best-effort before the sweep. One cosmetic 401 (favicon behind auth) is expected noise.
