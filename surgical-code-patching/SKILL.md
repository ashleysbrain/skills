---
name: surgical-code-patching
description: "Use when applying numbered surgical patches to code files."
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [editing, code, patching, verification, precision]
---

# Surgical Code Patching (Multi-Patch Missions)

## When to Use
- A delegated task or review-chain verdict hands you a numbered patch list
  (e.g. "apply these 6 surgical patches") with hazard descriptions and
  approximate line numbers in production code.
- The instruction says "surgical, minimal, no refactors" — verify and report
  old→new per patch, not a rewrite.
- You must make live production code safe for an imminent downstream use
  (a deadline the patches de-risk) without a full test cycle.

## Workflow (proven 2026-08-15, VERITAS 6-patch mission)

1. **Batch-read ALL target regions before ANY edit.** 2–4 parallel `read_file`
   calls, ~50–130 lines around each cited line number. Cited line numbers from
   prior audits are approximate, never exact — confirm against live code.
   Do not patch against an assumed context.
2. **If a named symbol isn't in the named file, search the workspace.**
   Task specs frequently attribute wrapper-level concerns (DB persistence,
   status mapping, run identity) to the wrong file. Example: run persistence
   was specified "in veritas_process.py L28-70" but lives in `pipeline_api.py`
   (`_RUNS_DB`, `_persist_run`, table `runs(run_id, data, updated)`).
   Never invent a DB schema — read the real `CREATE TABLE` and column list.
3. **Patch with unique context anchors** — 3–6 surrounding lines, not bare
   one-liners. Large files repeat patterns; bare strings match twice.
4. **Leave `# PATCH N: <reason>` comment markers** in the edited code. Makes
   post-hoc verification a single `PATCH [1-6]` grep. Cheap, permanent
   greppability for future audits.
5. **After ALL patches, run the syntax check yourself:**
   `python3 -c "import ast; ast.parse(open('<file>').read())"` for every
   touched file. The patch tool's lint status is NOT your own verification.
   Then grep the patch markers to confirm every patch landed where expected.
   If a fix carries executable semantics (SQL, sort keys, dict contracts),
   ALSO prove it behaviorally: e.g. a 10-line `sqlite3.connect(":memory:")`
   test — write the sibling column, run the new SQL twice, assert the
   column survives. In-memory only: no temp files, safe under disk pressure.
6. **Report old→new per patch**: exact old code, exact new code, location.
   An auditable diff without needing git.

## Cross-file hazard pattern

When a pipeline/engine module is driven by an API wrapper: run persistence,
status mapping, and run-id identity often live in the WRAPPER. A
pipeline-side persistence hook is useless unless the wrapper attaches the
run id (`config.run_id = run_id`) and the wrapper's status mapping honors
new statuses you add (e.g. `blocked_phantom_citations` must not be
overwritten to "completed"). Adding statuses or persistence usually spans
BOTH files — check before declaring done.

## Defect classes to recognize on sight

- **Unbound-variable branch crash**: variable assigned only inside `if not X:`
  but read unconditionally later. Fix: initialize safe defaults BEFORE the
  branch; never `dir()` checks at the read site.
- **Filter drops the severe case**: forwarding filtered `verdict == "REVISE"`
  while `FAIL` seats vanished. Severity gradients: forward the top too.
- **Truncation before the consumer**: per-item `[:100]` + total `[:800]`
  starves the downstream LLM. Apply caps once, at final assembly, sized to
  the consumer's real budget.
- **Exact-match verdict checks**: `== "FAIL"` misses `FAIL_DEGRADED`. Use
  `str(verdict).startswith("FAIL")` for verdict families.
- **Unconditional success status**: `run()` returning `"complete"` regardless
  of tracked state. Return the tracked state; early-exit paths must RETURN,
  not `break` into a success return.
- **Wrong metric under a scary name**: `phantom_count = support.get("weak")`.
  Fabricated (phantom) vs thin (weak) are different severities: fabricated
  hard-blocks, thin surfaces for human decision.
- **REPLACE-wipe of sibling columns**: `INSERT OR REPLACE INTO t (a, b)`
  deletes+reinserts the row, NULLing every column not in the insert list —
  so a later full-row persist silently wipes columns an earlier partial
  UPDATE wrote (`draft_content` vs `data`/`updated` in `runs`). Fix:
  `INSERT … ON CONFLICT(pk) DO UPDATE SET` naming only the columns you own.
- **Severity-blind slicing**: widening a filter to include FAIL is useless
  if the downstream `[:5]` slice keeps list order — five REVISE seats crowd
  out a FAIL. Sort severity-first, then slice:
  `sorted(seats, key=lambda s: 0 if s.get("verdict") == "FAIL" else 1)[:5]`.
- **Guard without emitter**: fixing the consumer guard
  (`str(verdict).startswith("FAIL")`) is dead code if the producer dict
  never emits `verdict` — and a
  `result.get("verdict") or result.get("panel_verdict") or result.get("name")`
  fallback chain masks the gap silently (verdict becomes the stage name).
  Check BOTH sides: does every stage the guard covers actually emit the key?

## Pitfalls

- Patching against stale line numbers without reading live code.
- Trusting the patch tool's lint result instead of running `ast.parse`.
- Editing only the pipeline module when the wrapper owns status/persistence.
- One transient write failure ("No space left on device" under macOS
  purgeable-space pressure) does not mean the strategy is broken — retry
  the identical op once before switching approaches.

## Support files

- `references/veritas-6-patch-mission-2026-08-15.md` — full case study: exact
  old→new for all 6 patches, cross-file hooks, defect taxonomy.
- `references/veritas-third-pass-residuals-2026-08-15.md` — second-order
  residuals of that patch set (REPLACE-wipe, severity-blind slicing,
  guard-without-emitter), plus the review-chain meta-lesson.

## Verification checklist

- [ ] Read every target region before editing?
- [ ] Located every named symbol in its real file (searched if missing)?
- [ ] Unique context anchors on every patch?
- [ ] `# PATCH N:` markers left in code?
- [ ] `ast.parse` run on every touched file after ALL patches?
- [ ] Behavioral test run for executable semantics (SQL/sort/contracts)?
- [ ] Checked second-order effects: does any pre-existing code path
      (older full-row persist, list-order slice, fallback chain) clobber
      or mask what each patch produces?
- [ ] Marker grep confirms every patch landed?
- [ ] Report shows old→new + location per patch?
