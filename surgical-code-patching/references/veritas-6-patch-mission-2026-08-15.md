# VERITAS 6-Patch Mission — Full Case Study (2026-08-15)

Context: the specialist engine subagent (production engineering) delegated a 6-patch
surgical set from an 8-brain review chain. Target:
`/<workspace>` (~5.9k lines) + discovered
companion `pipeline_api.py` (~7k lines). All patches applied, `ast.parse`
clean on both files, marker grep confirmed 11 landing sites.

## Key discovery: the spec named the wrong file

The task said "pipeline_runs.db persistence (L28-70 area: _persist_run /
sqlite writes)" in veritas_process.py. A workspace-wide search for
`pipeline_runs` found it in `pipeline_api.py` only: `_RUNS_DB`,
`_persist_run(run_id)`, schema `runs(run_id TEXT PRIMARY KEY, data TEXT,
updated TEXT)`. The patch therefore spanned two files — helper + hooks in
the pipeline, run-id attachment + status propagation in the wrapper.

## Exact old→new per patch

### PATCH 1 — Draft persistence (hazard: crash loses draft)
- NEW `_persist_draft_content(source)` helper: guarded `ALTER TABLE runs ADD
  COLUMN draft_content TEXT` (try/except pass), then
  `UPDATE runs SET draft_content=?, updated=? WHERE run_id=?`. No-ops when
  `config.run_id` absent (CLI runs — checkpoint file already holds draft).
- Hooked at 3 sites: stage 4.6 progressive path, stage 4.6 fallback path,
  stage-6 accepted-revision swap.
- Wrapper: `config.run_id = run_id` after PipelineConfig construction.

### PATCH 2 — S6 critique visibility (hazard: FAIL critiques invisible)
- OLD: `revise_seats = [s for s in seats if s["verdict"] == "REVISE"]`;
  `raw = str(seat.get("raw",""))[:100]`; `feedback = "\n".join(...)[:800]`.
- NEW: filter `in ("REVISE","FAIL")`; full `raw`; each line tagged
  `[VERDICT]`; final cap `[:4000]`.

### PATCH 3 — Abort guard (hazard: no gate can fire)
- OLD: `if stage_num in (0, 3) and verdict == "FAIL":`
- NEW: `if stage_num in (0, 3, 3.1) and str(verdict).startswith("FAIL"):`

### PATCH 4 — Truthful status (hazard: UI lies)
- Final return: OLD `"status": "complete"` → NEW `"status": self.state.status or "complete"`.
- Stage-7 exception path: OLD `break` (fell through to "complete") → NEW
  early `return` with `"complete_with_errors"` + reason.

### PATCH 5 — Phantom gate (hazard: fabricated citations ship)
- OLD: `phantom_count = citation_support.get("weak", 0)` — mislabeled.
- NEW: read `phantom` and `weak` separately; `phantom_count = phantom + weak`.
  If `phantom > 0`: `quality_status = "blocked_phantom_citations"`, gate
  verdict "BLOCKED", human-review message. Wrapper propagates the block
  (never maps it to "completed"). Weak-only stays surfaced for humans.

### PATCH 6 — Unbound crash guard (hazard: brainstorm handoff crashes)
- OLD: `search_result` bound only inside `if not pre_evidence:`; read
  unconditionally later (`["api_log"]`) → NameError on pre-evidence path.
- NEW: `search_result = {"api_log": [], "total_api_calls": 0}` initialized
  BEFORE the branch; overwritten by the normal-search branch.

## Verification performed
1. `python3 -c "import ast; ast.parse(open('veritas_process.py').read())"` → OK
2. Same for `pipeline_api.py` → OK
3. `search_files` for `PATCH [1-6]` → 11 matches, all at expected sites.

## Transient issue
One patch write failed with "No space left on device" (disk at 100%,
1.2GB purgeable). Identical retry succeeded immediately. Retry-once before
strategy-switching under macOS purgeable-space pressure.
