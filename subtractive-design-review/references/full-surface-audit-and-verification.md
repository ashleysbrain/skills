# Full-Surface Extension + Verification Protocol (Passes 16-17)

Additions to the core workflow — the dashboard-only subtractive pass is incomplete.
Pending SKILL.md integration (curator read-guard); content authoritative here.

## Step 6: Extend the Audit to the WHOLE Surface (not just the dashboard)

The same disease lives in nav, views, and panels. Full-surface census:

1. **Enumerate every view/section and every nav entry pointing at it.**
   For a single-file UI: `re.findall(r'data-view="(\w+)"', src)` for nav; section ids for views.
   Compare: views defined vs. views reachable. Hidden/unreachable views are suspects.

2. **Dead-shell detection.** For each view's stat/value elements, grep the JS for a
   WRITER (`getElementById('<id>')` assignments). **Zero writers = dead shell**: the
   view renders hardcoded zeros forever. This is the same "surface pretending to be
   real" failure class as a freshness metric reading a dead database.
   Action: cut dead shells from nav (keep the section in-file for future wiring).
   Observed: 4 of 13 nav entries were dead shells (Argument Skeleton, Adversarial
   Panel, Revision Dashboard, Authorship Dashboard). Nav went 13 -> 9.

3. **Button-density triage.** Count buttons per view. A 51-button drafts surface is
   a working toolbar (keep); always-visible analysis walls are not. Collapse heavy
   analysis panels (readability scoring, venue analysis, rewrite engines) behind
   Show/Hide toggles, collapsed by default — progressive disclosure, not deletion,
   for genuinely useful firepower.

4. **Deref safety sweep.** For every `document.getElementById(...)` deref in
   reachable code paths, confirm the element exists in HTML or is dynamically
   created. Guard pattern:
   `const el = document.getElementById('x'); const v = el ? el.value : '';`
   (Found live: unguarded `recPipeline.value` -> TypeError on tab click.)

## Step 7: Verify with a Parser and the SERVED Artifact

- After ANY string-splice edit, run a real HTML parse (python `html.parser.HTMLParser`),
  not regex counts. Assert: zero duplicate element ids; style attributes parse clean.
  Observed splice damage invisible to grep: `style="display:nonestyle="margin-top:20px"`
  (missing space + duplicated style attr) — caught only by HTMLParser.
- Run `node --check` on extracted `<script>` bodies after every edit batch.
- Compare the SERVED artifact byte-for-byte to disk after service restart. Mismatch
  means a watchdog restored a backup (see below) or the service wasn't restarted.

## Pitfall 8: Self-healing watchdog restoring the baseline underneath you

Files guarded by a known-good-backup watchdog (JS-validate + restore, ~10-min idle
grace) will silently resurrect pre-edit content:
mid-edit state fails validation -> grace window passes -> watchdog restores a
pre-edit backup -> later edits land on the STALE baseline -> cut elements reappear
while newer edits survive. Rules:
1. Keep edit batches short; validate JS after every batch.
2. At session end on a watched file, run the watchdog's `validate` then `backup`
   so known-good equals your INTENT, not a pre-edit snapshot.
3. Never trust a cut claim without re-grepping the SERVED artifact after the grace
   window — byte-compare served vs disk catches the restore.

## Trust-earning verification sequence (what made pass 17 stick)

1. `node --check` on extracted script bodies (the guardian's own validator).
2. HTMLParser full pass: 0 duplicate ids, style attrs clean.
3. `validate` + `backup` via the guardian CLI.
4. Service restart; served == disk byte-compare.
5. Commit.
