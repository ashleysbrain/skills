# Veritas Stage-6 Convergence Loop: Operating Notes

The paper pipeline's revision loop (`veritas_process.py`, stage 6) enforces the
convergence law. Constants (env-overridable): `VERITAS_REVIEW_FLOOR=10`,
`VERITAS_CONSECUTIVE_CLEAN=3`, `VERITAS_MAX_REVISION_ROUNDS=12`, unified event
budget = 4x rounds.

## Semantics that are easy to get wrong

- **A "clean" panel** = `panel_verdict == "PASS"` AND zero seats carrying
  REVISE/FAIL. SKIP seats do not break cleanliness.
- **Review events** count every panel execution one-to-one (the stage-5 panel
  is event 1). PASS-class re-panels on identical bytes rotate a distinct
  interrogation `probe_angle` so the streak must survive different questions.
- **FAIL-class verdicts force a revision round** (their critiques feed the
  revision prompt exactly like REVISE) and the original FAIL stays on the
  seat record — history is never rewritten.
- **Every re-panel consumes the unified event budget** — nothing loops free,
  including persistent FAILs.
- **Fail-closed** sets `status = "convergence_unmet_fail_closed"`, parks stage 6
  in `state.parked_stages`, and `run()` ABORTS immediately: stages 6.5/7/7.5
  must not execute afterward. A resume into a parked stage is refused.
- `_classify_seat` maps pass/accept -> PASS, revise/warning/degraded -> REVISE,
  fail/reject -> FAIL, and unparseable -> REVISE (never a silent PASS).

## Verification recipe (mocked-engine prover)

Prove loop behavior without touching engines or the LLM:

1. `sys.path.insert(0, '/<workspace>')`; stub `httpx.Client` to
   raise (kills the direct-LLM revision call so rounds fail honestly).
2. Monkeypatch module-level `engine_post`, `sherman_route`, `engine_health`.
   Engine seat responses use `{"ok": true, "result": {"verdict": "pass"|"revise"}}`.
3. Instantiate `VeritasPipeline.__new__` (skip `__init__`) and set a fake
   `state` carrying AT MINIMUM: `stage_results`, `current_draft` (300+ words),
   `revision_count`, `status`, `idea`, `evidence_level`, `citations`,
   `output_formats`, `process_id`, `finished_at`, `parked_stages`,
   `stages_completed`, `health_snapshots`, and a `checkpoint()` method —
   missing attrs surface as AttributeError mid-stage.
4. Scenarios: (A) all seats pass -> converges at event 10, zero revisions;
   (B) one seat always revise -> 12 revision rounds then fail-closed,
   `parked_stages == [6]`; run the run()-seam with 6.5/7/7.5 stubbed as
   counters -> all counters must be ZERO after fail-close; (C) 9 dirty then
   clean -> converges at event 12 with streak 3.

## Defect classes the adversarial panel caught (do not reintroduce)

- A stage returning `{'status': ...}` that its CALLER ignores — a fail-closed
  return must abort the caller's loop, not just exit the method.
- A budget keyed only on the counter one branch increments — persistent FAIL
  could loop forever. Every event must consume budget.
- Consecutive-clean streaks over identical inputs with ~6/11 seats that never
  see the artifact (they review the idea or earlier-stage angles) — rotate
  probe angles; know which seats are draft-aware.
- A verdict classifier with no PASS branch — engine "pass" mapping to REVISE
  makes convergence unreachable in production while mocked tests pass.
- Resume paths that re-enter a parked stage and clobber the parked ledger.
- Docker copies of the studio that bake `veritas_process.py` at image build
  (no bind mount) — a host patch is invisible to them; rebuild or retire the
  shadow lane.
