# Session Detail: owner-exit with HETEROGENEOUS seat outcomes (2026-08-21)

Backing detail for sections 2 and 4 of the parent SKILL.md. Extends
`dead-seat-salvage-2026-08-18.md` (which covered uniform deaths: never-
started vs full-budget-timeout). This case adds the mixed batch: SOME seats
delivered before the owner died.

Case: 4-seat memory gap panel (Squire/Buzsaki/Marr/Tonegawa), dispatch
deleg_eed9a67e, salvage child deleg_c2e34e5b, both glm-5.3.

## Signature

Batch error: "Delegation owner exited before recording a terminal result;
outcome unknown." Per-seat logs show a MIX:
- task-0 and task-2: `final | status=completed` (106s, 168s) — verdicts ARE
  in the logs.
- task-1 and task-3: end mid-tool-call, zero think/final lines — died with
  no analytical output.

## What made this salvage different from 2026-08-18

1. DELIVERED seats must NOT be re-dispatched. Their verdicts live in the
   task logs (grep `final | status=`). The batch-level loss does not mean
   seat-level loss.
2. CHECK FOR PARALLEL-TURN SALVAGE FIRST. In this case an earlier turn had
   already recovered the delivered seats' verdicts to files (verdict-file
   mtimes 09:26, inside the dispatch window) and acked on the bus
   (manifest.json mtime 10:30, `"status": "done"` + ack notes). Re-running
   delivered seats would have clobbered that work. Signals: verdict/spec
   file mtimes after the kill; manifest ack notes naming the artifacts.
3. DEAD seats (no think/final) re-dispatch SEQUENTIALLY IN ONE CHILD:
   "run seat X brief, then seat Y brief; return both verdicts". One child,
   two briefs: 397s, 27 tool calls, every claim re-verified against live
   source, verdicts written to disk by the child itself. The single-child
   sequential pattern is also the standing 429 countermeasure (concurrent
   same-model children die together).
4. Bake the delivered seats' findings into the replacement's context and
   say explicitly "seats A/C already delivered — do NOT redo their work."
5. Salvage-run verdict files SUPERSEDE operator drafts: the seat-authored
   artifact is canonical over an earlier operator summary of the same seat.
6. Consolidate recovered + re-run seats in ONE pass; the run-record cites
   BOTH dispatch ids (original + salvage).

## Gates encountered while consolidating (chair-side)

Three sequential write gates fired on the chair's own writes, in order:
integrity gate (required [source: ...] markers) → specialist gate (Sherman
route expiry >5 min; re-route via specialist_gate.py --route) → baseline-
first gate (blocked NEW canonical report path; append to the existing
RUN-RECORD via patch instead of minting a new file). Lesson: when a new-file
write is gate-blocked, the sanctioned move is to append the synthesis to the
existing canonical artifact, not to fight the gate.

## Patch-payload corruption on the large append (durable failure mode)

Two corruptions in one session, both on LARGE patch new_string payloads to
canonical files, both tools REPORTED SUCCESS:
- RUN-RECORD append: "2,-143", "lulence"→lability, "MoccClelland",
  "Newdergaard", duplicated M3/M6 lines.
- MISSING-ANATOMY-QUEUE append: wrong dates (2026-08-18/25, 2026-06-21,
  202A), `confirmed_anEalog`, "fMRIrippl", duplicated garbage ANA-012.

Repair protocol (worked twice):
1. Detect by grep sweep of the written region for corruption markers.
2. Repair via deterministic python heredoc with hard anchors (last legit
   line + next section marker), regex block extraction, well-formedness
   filter (correct date, required fields, no corruption tokens), dedupe by
   id, rewrite the tail. NOT a second model-authored patch — it draws from
   the same corrupted context.
3. Verify by readback: expected id count, zero corruption-marker hits.
4. Regex pitfall: tolerate variable newlines between anchor and first new
   block — use find()+slice, not one rigid pattern.

## Outcome

All 4 verdicts canonical on disk; consolidated chair report appended to
RUN-RECORD.md (corruption repaired, swept clean); 6 mint specs registered in
MISSING-ANATOMY-QUEUE.md as ANA-007..012 (ledger verified: 12 ANA ids, zero
corruption markers). Salvage cost: one sequential child, zero lost seats.
