# #19 — Purge claims expire at the next run (caught 2026-08-19)

Belongs after failure mode #18 in SKILL.md (body edit blocked by curator read-gate
this session; foreground curator should fold in):

## Failure
- PASS-4 (2026-08-19) ended with "0 probe rows left" — true at that moment.
- The regression battery then ran again (post-restart verification), creating two
  new rows nobody purged.
- PASS-5's census found them and falsified the prior pass's "done" — the third
  consecutive QA pass where the previous pass's claim did not survive
  re-verification (PASS-2 gates bypassable → PASS-3; PASS-4 UPDATE-path re-open +
  hygiene leak → PASS-5).

## Root cause
"purged" is a claim about a PAST state. Any later run of the same battery —
regression, restart probe, another reviewer's pass — recreates the artifacts.

## Fix
- End every battery run with the count query and report its OUTPUT, never the
  memory of having purged.
- Fold purge+count into the battery script itself so skipping is structurally
  impossible.
- Generalizes: any "clean state" claim made before the last tool call that could
  have dirtied it is stale. Verify after the final mutating action, not before.

## Related
- Skill `headless-ui-qa-batteries` "Server-state hygiene" (same lesson, battery side)
- `references/write-path-census-pass4-pass5-2026-08-19.md` (companion session record)
