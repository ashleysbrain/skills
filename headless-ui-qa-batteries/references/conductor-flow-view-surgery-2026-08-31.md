# Conductor screen FLOW view surgery — 2026-08-31

Session detail for the FLOW (ledger) view edits on the conductor surface
(:port, `conductor_screen.py` + `conduction_daemon.py`). Three principal orders
in one day, all shipped + pixel-verified.

## Order 1 — filter-toolbar collapse (dropdown leak)

Symptom: "a long list of drop downs on the upper left that leak into the
other sections and create a large gap."

Root cause: `.ftools` flex-wrap row of 11 controls (search + 7 selects +
3 buttons + saved views) wrapping into a tall stack.

Fix shape (reusable for any toolbar pile):
- Split into: always-visible bar (search + two toggle buttons + row count)
  + collapsible panels (`.ftpanel`, display:none, class `open`).
- Gold active-count badge on the Filters toggle — count non-empty selects
  by id list, update in the same render function that rebuilds the table.
- KEEP select ids identical — zero render-logic churn, the collapse is
  purely presentational.
- DOM id collision trap: the Views PANEL wanted id `ft-views`, already
taken by the saved-views SELECT. Renamed panel to `ft-viewspanel`.
  Duplicate ids silently bind JS to whichever element parses first.

## Order 2 — de-clump: Group-by + header collision

Symptom: "this information. is all clumped together" + a smashed H2
("database viewevery row live…").

Two defects, two fixes:
1. H2 `float:right` subtitle collision → flex baseline layout
   (`display:flex;align-items:baseline;justify-content:space-between`),
   subtitle 11.5px dim.
2. 400 undifferentiated rows → **Group-by control** (stage/lane/state/
   kind/none, default stage) with sticky section headers (`tr.ftgroup`,
   `top:29px` to pin under the sticky column header, count badge pill).

The grouping surfaced the real bottleneck IN the UI: 323 of 400 rows at
tri:review. A flat 400-row table is an information desert — grouping IS
the deeper dive.

## Order 3 — timestamps ("I need times on these tasks")

Data limb (daemon): join per-task event timeline into the rows API —
  read-only ledger query, event filter list (minted/tri-stamp/claim/done/
  tri-close/blocked…), ORDER BY ts, LIMIT 40/row so chatty tasks can't
  balloon payloads.
Render limb: Age cell gains `title` = full timeline (one event per line,
  `event  MM-DD HH:MM  by actor`) + a dim `moved Xh ago` subline from the
  LAST timeline entry (only when >1 events). Task drawer already had the
  full step trail — the gap was LIST-LEVEL visibility, pre-click.

**Escaping trap:** the timeline joins with `'\n'` in JS. Authoring that
inside the Python-embedded HTML string produced `'\\n'` → tooltip
rendered literal `\n` text. Fix: single backslash in source. Symptom to
remember: `getAttribute('title')` containing `\n` as TWO chars.

## Verification loop that worked (per the vision-audit law)

1. Pre-deploy: `node --check` on extracted script blocks + structural
   greps (marker strings present, prior fixes intact).
2. Deploy: `launchctl kickstart -k gui/$(id -u)/com.your-org.
   conduction-daemon`.
3. Live: curl the API (timeline present on N/N rows) + DOM-read the
   rendered cells + screenshot + vision audit of the changed region.
4. "database view" grep hit that persisted post-fix was a JS COMMENT —
   visible-text claims need DOM reads, not grep (see
   vision-audit-reliability.md).

## Event-histogram diagnosis pattern (reusable)

"Nothing moved" complaints: bucket task_events for the window in
question (`SELECT event, COUNT(*) … WHERE ts > datetime('now','-60
minutes') GROUP BY event`). Live case: 45 done + 52 claimed + 27 advanced
in the hour — work WAS moving; but 1,290 tri-readmit events in the same
hour = churn diagnosis, and every principal-minted task sat at tri:review all
meeting. The histogram splits "system idle" from "system busy on the
wrong things" from "readmit churn" — three different diseases with the
same user-visible symptom.
