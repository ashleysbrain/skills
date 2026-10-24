# VERITAS Third-Pass Residual Fixes (2026-08-15, later session)

Context: the specialist engine (DS-ECS-SUB-04.07.03) fixing 3 residuals falsified by a
Popper review pass against the earlier 6-patch mission (see
`veritas-6-patch-mission-2026-08-15.md`). Same files, same workspace:
`/<workspace>` + `pipeline_api.py`.

Key structural fact: fixes 2 and 3 landed in `veritas_process.py`, but
fix 1's quoted code (`INSERT OR REPLACE INTO runs`, "_persist_run L46",
"final persist L330") lives in `pipeline_api.py` — second consecutive
mission where the spec attributed wrapper-level persistence to the
pipeline file. Both files share `pipeline_runs.db`; `veritas_process`
writes `draft_content` via UPDATE, the wrapper's full-row REPLACE then
wiped it on every completed run.

## RESIDUAL 1 — REPLACE-wipe of draft_content (pipeline_api.py L46)

- OLD: `INSERT OR REPLACE INTO runs (run_id, data, updated) VALUES (?, ?, ?)`
- NEW: `INSERT INTO runs (run_id, data, updated) VALUES (?, ?, ?)
  ON CONFLICT(run_id) DO UPDATE SET data=excluded.data, updated=excluded.updated`
- Why: REPLACE = delete+reinsert → NULLs every column not in the insert
  list. ON CONFLICT DO UPDATE touches only the named columns.
- Verified behaviorally with `sqlite3.connect(":memory:")`: sibling
  column written via UPDATE, then two full persists with the new SQL —
  draft_content survived. (Disk pressure noted in task → in-memory only.)

## RESIDUAL 2 — FAIL-first ordering (veritas_process.py ~L4544)

- OLD: `for seat in revise_seats[:5]:`
- NEW: `for seat in sorted(revise_seats, key=lambda s: 0 if s.get("verdict") == "FAIL" else 1)[:5]:`
- Why: the earlier mission widened the seat filter to include FAIL, but
  the [:5] slice kept list order, so 5 REVISE seats could crowd out a
  FAIL seat. First-pass fix was incomplete on its own — the fix had a
  residual. Review-chain lesson: a fix's consumer path must be checked,
  not just its producer path.

## RESIDUAL 3 — stage 0 / stage 3 verdict keys (veritas_process.py)

- Stage 0 result dict (~L2965): added `"verdict": "PASS" if passed else "FAIL"`.
- Stage 3 result dict (~L3374): hoisted `blocking = selected.get("blocking",
  False) if isinstance(selected, dict) else True` to a local, then added
  `"verdict": "FAIL" if blocking or selected.get("error") else "PASS"`.
- Why: the fixed run-loop guard
  `if stage_num in (0, 3, 3.1) and str(verdict).startswith("FAIL")`
  was dead code for stages 0 and 3 — those dicts never emitted `verdict`,
  and the run loop's `result.get("verdict") or result.get("panel_verdict")
  or result.get("name", "done")` fallback silently substituted the stage
  NAME as the verdict, masking the gap. Stage 3.1 already emitted verdict.
- Note: hoisting `blocking` to a local before the dict avoided computing
  the isinstance-guarded expression twice and kept the dict readable.

## Verification performed

1. `ast.parse` on both files → OK.
2. In-memory SQLite behavioral test of the new ON CONFLICT SQL →
   draft_content survives repeated full persists.
3. `# PATCH` comment markers left at all four edit sites.

## Meta-lesson for review chains

Third-pass residuals were all SECOND-ORDER effects of the first-pass
fixes: (a) a fix that widened a data path left the slice consumer wrong,
(b) a guard fix assumed producers emitted the key, (c) a persistence
helper added in pass one was being wiped by pre-existing wrapper SQL.
When auditing a patch set, ask: what does each patch's output feed into,
and does any pre-existing code path now clobber it?
