# Writing Studio Full-Surface Audit (Passes 16-17, 2026-08-18)

Session detail backing `subtractive-design-review`. Single-file UI (~750KB
`writing-studio.html`, served by pipeline_api.py on :port).

## Scope discovered
- 16 views defined, 13 exposed in nav, 243 buttons total. The subtractive audit
  extended beyond the dashboard to the entire surface — the same failure classes
  lived everywhere.

## Dead shells found (nav cut 13 -> 9)
- Argument Skeleton, Adversarial Panel, Revision Dashboard, Authorship Dashboard:
  nav entries whose stat elements had ZERO JS writers. Detection: for each stat id,
  grep `getElementById('id')` — no writer means hardcoded zeros render forever.
  The same "surface pretending to be real" class as a freshness metric reading a
  dead database. Sections left in-file for future wiring; nav entries removed.

## Progressive disclosure
- Writing Audit / Publication Readiness / Sentence Rewrite Engine — always-visible
  analysis walls stacked under every draft — collapsed behind Show/Hide toggles
  (`display:none` default). Firepower preserved, surface cleaned.

## Splice damage found by fresh-brain QA (Popper seat)
- The panel-collapse string-splice produced malformed attributes:
  `id="panelWritingAudit" style="display:nonestyle="margin-top:20px"`
  (missing space + duplicated style attr). Invisible to regex tag-counting; caught
  by an HTMLParser pass. Lesson: PARSE, don't grep, after splice edits.

## Watchdog restore collision
- `organism/writing_studio_guardian.py` (JS-validate + restore-from-backup,
  10-min idle grace) restored a pre-edit `ws-good-*` backup after a mid-edit
- validation failure; previously cut dashboard cards resurrected while newer
  edits survived. Recovery: re-apply cuts on the restored baseline, then
  immediately `validate` + `backup` so known-good equals intent.
  Full pattern documented in `baseline-first-surgical-precision`.

## Latent defect found during audit
- Unguarded `document.getElementById('recPipeline').value` on an element that
  never exists in HTML or JS — TypeError the moment the "Scored Recommendations"
  tab is clicked. Predated the edit campaign. Fix pattern:
  `const el = document.getElementById('x'); const v = el ? el.value : '';`

## Verification that earned trust
- `node --check` on extracted `<script>` bodies (the guardian's own validator).
- `html.parser` full pass: 0 duplicate element ids, style attrs parse clean.
- Served page byte-compared to disk after service restart.
