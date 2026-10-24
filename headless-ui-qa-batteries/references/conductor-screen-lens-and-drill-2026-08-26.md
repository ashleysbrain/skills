# Conductor screen scenario lens + visibility law + drill rebuild — 2026-08-26

Session detail for the SKILL.md section "Conductor Screen (:port)".
Source files: `~/your-org/organism/conductor_screen.py` (embedded
HTML/JS, ~1080 lines) and `conduction_daemon.py` (:port).

## The triggering corrections (verbatim principal intent)

1. "the buttons are just decoration" — the scenario toggle set `SCEN` and
   NOTHING read it. grep confirmed zero consumers. This is the L11
   claims-honesty violation class: declared behavior code does not run.
2. "the change in scenario does nothing to the thought history" — first
   fix only wired Calendar; the Flow view (bus + pulse) the principal actually
   watches was untouched. LESSON: a global control must be verified against
   EVERY view it claims to govern, in the view the user looks at.
3. "I like how the rows of events are kind of darkened... useful when
   distinguishing human from ai tasks quickly... while still allowing the
   human to drill into the ai work" — dimming promoted from side effect to
   deliberate visibility language.
4. "I should be able to have access to all information even if it isn't
   generated in the page... go down rabbit holes... layer by layer but
   only if needed. this is data architecture done brilliantly."

## What shipped (all live-verified in the preview pane)

- `/mesh` proxy on :port -> :port `/api/calendar/mesh` (read-only, 8s
  timeout, 502 with detail on failure). Screen went from ~12 thin items to
  184 across 10 sources.
- `scenOf/scenKeep/updateScenCounts` + counts printed on the toggle buttons
  themselves (B2B2C · 184 / B2B · 0 / B2C · 6, live-moving).
- `dimFor(route, scen)`: human=1.0, ai=0.72, shared-under-lens=×0.45
  (0.32 for shared+ai under lens). Human never route-dimmed. Legend line
  at top of bus and pulse lists.
- Bus rows infer route by subject regex (/ceo|APPROV|AWAITING|RULING|
  DECISION/i -> human).
- Drill: universal id resolver, linkify T-IDs and #bus-ids inside drawer
  text, depends_on chain clickable, `/api/crondetail` proxy for cron rows,
  calendar rows route by id prefix (cron_/mosaic_/bus_).

## Debugging sequence that worked (reuse this order)

1. `curl served page | node syntax gate` — catch embedded-JS syntax errors
   before the browser.
2. Check the SERVED bytes for your new marker (`grep` for a string only
   present in the edit) — daemon module caching serves stale pages until
   `launchctl kickstart -k`.
3. Preview pane: reload -> `elements` -> click immediately (re-render loop
   invalidates refs fast).
4. `read_preview` at multiple char offsets to find the panel you care
   about; the URL field carries the hash = JS state proof.
5. window.onerror -> location.hash crumb for silent click failures.

## Failure patterns hit (fixed, do not repeat)

- Ternary helper copy losing a quote: `'</div> : ''` — happened TWICE in
  copied `dl = (k,v) =>` lines. The odd-quote-count line scan finds them:
  `node -e` counting `'` per line, flag odd counts containing `esc(`.
- CSS patch landing inside an open rule block (patch anchored on the first
  line of a multi-line CSS rule). Anchor CSS patches on the COMPLETE rule
  or insert after a closing brace.
- CSS was patched fine but style was invisible: verify with grep on served
  HTML after daemon restart, then pane reload.
- Byte-wise JS bisection false-errors on multibyte chars — bisect by lines.
- `document.title` instrumentation is NOT visible in read_preview; DOM text
  nodes get clobbered by 5s pollers. location.hash survives both.

## Still open at session end (honest ledger)

- The drill drawer chain (click bus row -> drawer -> click linkified T-ID
  -> task drill) is wired and syntax-clean but NOT yet visually confirmed
  end-to-end in the pane; the re-render loop kept eating refs mid-click.
  Next session: verify the drawer chain live, then remove the
  window.onerror->hash debug crumb.
- B2B lens shows 0 because no B2B organism exists in the mesh yet — honest
  signal, toggle ready for when one does.
- Dynamics-per-interaction (T-260826-0128) awaiting principal ruling — the
  calendar-harmony layer that tags mastermind/synergy/symbiosis/entourage
  per engine join.
