# Owner-exit batch salvage + patch-payload corruption (2026-08-21)

Case: 4-seat memory gap panel (Squire/Buzsaki/Marr/Tonegawa), dispatch
deleg_eed9a67e, salvage deleg_c2e34e5b.

## Owner-exit kill: seats are heterogeneous

Batch error: "Delegation owner exited before recording a terminal result;
outcome unknown." The seats did NOT die uniformly:

- Seat A (task-0.log): `final | status=completed` at 106s — verdict IS in
  the log; batch loss does not mean seat loss.
- Seat C (task-2.log): `final | status=completed` at 168s.
- Seats B/D (task-1/3.log): end mid-tool-call, zero think/final lines —
  died with no analytical output; nothing to salvage.

Triage rules learned:
1. grep each task log for `final | status=completed` BEFORE re-dispatching
   anything. Completed seats' verdicts live in the logs even when the batch
   result is lost.
2. Check for parallel-turn salvage BEFORE re-dispatching: verdict files with
   mtimes inside/after the dispatch window, and manifest.json with a LATER
   mtime carrying `"status": "done"` + ack notes. In this case an earlier
   R2 turn had already recovered seats A/C to verdict files and acked on the
   bus. Redoing them would have wasted an hour and clobbered that work.
3. Re-dispatch ONLY the dead seats, SEQUENTIALLY IN ONE CHILD: "run seat X
   brief, then seat Y brief; return both verdicts". One child, two briefs,
   397s, 27 tool calls, all claims re-verified against live source. This is
   also the 429-storm countermeasure (concurrent same-model children die).
4. Tell the replacement which seats already delivered and bake their
   findings into its context ("do NOT redo their work").
5. Salvage-run verdict files SUPERSEDE operator drafts written by an earlier
   turn; the seat-authored artifact is canonical.
6. Consolidate all seats (recovered + re-run) in ONE pass, citing BOTH
   dispatch ids in the run-record.

## Model-authored patch payloads corrupt on large appends

Two separate corruptions observed in one session, both on large patch/
new_string payloads to canonical files, both REPORTED SUCCESS by the tool:

- RUN-RECORD.md append: "2,-143" for "2,143", "lulence" for "lability",
  "MoccClelland" for "McClelland", "Newdergaard", duplicated M3/M6 lines.
- MISSING-ANATOMY-QUEUE.md append: wrong dates (2026-08-18/25, 2026-06-21,
  202A), `confirmed_anEalog`, "fMRIrippl", a whole duplicated garbage
  ANA-012 block.

Repair protocol (worked twice, deterministic):
1. Detect: sweep the written region with grep for corruption markers
   (duplicated ids, malformed field names, impossible dates, doubled words).
2. Repair with a python heredoc, NOT another model-authored patch: anchor on
   the last legitimate pre-existing line + the next section marker, regex
   out the new blocks, filter for well-formedness (correct date line,
   required fields present, no corruption tokens), dedupe by id, rewrite.
3. Verify by readback: id count matches expectation, corruption-marker grep
   returns nothing.
4. Pitfall that cost one retry: the regex must tolerate the variable number
   of newlines between the anchor and the first new block — use
   `src.find(anchor_line)` then slice, not a single rigid pattern.

Why python heredoc and not patch: the second model patch is drawn from the
same corrupted context that produced the first corruption; it can remove the
old damage while inserting new damage. Deterministic string surgery cannot
hallucinate tokens.
