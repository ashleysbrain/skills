# Session 2 — 2026-08-16 (later): gap-audit pass + custody lessons

Continuation of the founding session. Live-verified facts; re-verify before
reuse.

## Rollout state (supersedes founding-session notes)

- Skill `elite-orchestration-default` NOW EXISTS:
  skills-library/protocol/elite-orchestration-default/SKILL.md v1.1.0.
  Created after Tanenbaum r2 delivered + orchestrator applied fact-dictated
  repairs (the founding note "does not exist yet" is obsolete).
- Popper r1 (deleg_79b976cc) timed out at exactly 900.0s on API call 7 —
  BUT her verification phase completed and produced three facts, all
  re-verified by the orchestrator and folded into the skill:
  1. workspace-root sherman_router.py is a SYMLINK to
     organism/config/sherman_router.py (so those two "copies" are one).
  2. The gate hook's hardcoded your-org/the operator agent copy (34806 bytes) is
     genuinely divergent from canonical (74913) — every gate call runs the
     stale router.
  3. Tanenbaum and Lamport are ABSENT from the ECS registry; Popper IS
     present. Unregistered specialists must be cited by name only.
- Popper ALSO violated her no-write contract: wrote the UNREPAIRED
  defective artifact to the skill path mid-run. Caught by post-run
  filesystem check; overwritten with the repaired version. This birthed
  custody rule 5c (below).
- Router defects (misroute + stale hook copy) handed to the sibling
  operator via bus #1949 with exact file refs. Still their lane.

## The three 900s deaths and the fix

Tanenbaum r1, Da Vinci r1, Popper r1 all died at exactly 900.0s. All three
transcripts showed the same shape: thorough verification (7-8 API calls of
reads/probes, all successful) and death before synthesis. Both
synthesis-only re-dispatches with facts baked in completed (423s, 580s).
Do not re-dispatch a combined verify+author brief after this failure mode;
split the phases: Phase 1 verifies and reports, Phase 2 authors from
baked-in facts with an output cap and no-exploration instruction.

## Delivered-artifact defect audit

Tanenbaum r2's delivered artifact, grounded correctly, still contained:
4 invented ECS codes (ART-DVG-09.02.03, LNG-WRN-07.03.01,
ART-DVN-09.02.04, SCI-POP-08.04.01) + unverified AST-NJS-06.10.01 (which
the ORCHESTRATOR originated in its own dispatch context and the specialist
amplified — audit your own dispatch context as a contamination source),
wrong pipeline_api path, wrong skill path, `python 3` broken commands x3,
invented --test-routing flag, stdin-echo router test dropping --situation.
Grounding layer clean, synthesis layer hallucinated. Always audit the
ARTIFACT, not just the findings: extract every path/command/code and check
each against the live system before applying anything.

## Writing Studio bulk brainstorm: shipped, then gap-audited

Shipped: backend (commit 7be8285) + UI (860b839) + gap pass (e378f64,
1e435e5). principal: "I don't believe you did solid work do another pass and
find your gaps." The audit proved the skepticism correct — 6 real gaps:

1. CRITICAL: batch worker marked seeds "saved" without persisting anything
   (single-seed UI auto-saves via _autoSaveBrainstorm; the batch path had
   no equivalent). A 25-seed run (~30 min) would produce ZERO sessions.
   Fixed: worker calls save_brainstorm server-side per seed; bs_id returned
   in status. Verified: sessions 11 -> 12 after a live batch.
2. Save-failure still showed "saved". Fixed: honest failed status +
   save_error surfaced.
3. Retry scraped the rendered row, which truncates seeds at 80 chars ->
   would retry a TRUNCATED seed. Fixed: _batchSeeds array.
4. Server restart mid-batch = infinite silent polling. Fixed: stop on 404
   with honest message.
5. Bulk Set Status=archived did not remove sessions from the default list.
   Fixed: list excludes archived unless ?status=archived (parity with
   drafts stage filter). Round-trip verified live.
6. No path from completed batch to results. Fixed: View-in-Workshop link.

Transferable lesson: acceptance-test the DATA after batch operations
(row counts before/after), not just status fields and HTTP codes. The
original acceptance sweep passed completely while the core value
proposition was broken. The status-chip UI can say "saved" while nothing
persisted — UI state is not persistence evidence.

## FastAPI route shadowing (hit live)

DELETE /api/brainstorm/saved/batch registered after
/api/brainstorm/saved/{bs_id} was unreachable — the parameterized route
captured the literal "batch" as bs_id. Probe signature: the live endpoint
returns the SINGLE-delete response shape ({"id":"batch",...}) instead of
the batch shape. Fix: register static routes BEFORE parameterized
siblings. py_compile passes; only live probing catches this.

## Sibling co-editing on shared files

The sibling operator landed hubAddToBatch (research finding -> batch
pipeline, commit 71d91ab) in writing-studio.html MID-SESSION. Detection:
patch tool warned "modified by sibling subagent ... after this agent's last
read". Correct handling: git diff HEAD to attribute every uncommitted line
(mine vs theirs), verify both features coexist, commit immediately after
each step. Never re-read-and-rewrite the whole file over a sibling's
in-flight changes.

## Endpoints shipped (for future QA passes)

- POST /api/brainstorm/batch {seeds[1..25], shared{}} -> {batch_id, total,
  poll, note}; daemon thread, sequential seeds (~105s each live-measured),
  _BATCH_REGISTRY with 1h TTL + pruning.
- GET /api/brainstorm/batch/{batch_id} -> {status, done, seeds[{seed,
  status, error, bs_id, save_error}]}; 404 unknown/expired.
- POST /api/brainstorm/saved/batch-update {ids[], patch{notes?, tags?,
  status?, starred?, tags_mode? merge|replace}} -> {updated, failed[]}.
  tags_mode is popped from patch BEFORE the unknown-field check (order
  matters — the original strip-after-check rejected it as unknown).
- DELETE /api/brainstorm/saved/batch {ids[]} -> {deleted, failed[]};
  registered before the {bs_id} route.
- Bulk bar UI: checkboxes .bs-sel + shift-range + select-all chip, floating
  #bsBulkBar (Bulk Tag merge / Set Status / Star / Delete w/ confirm /
  Export JSON), toast on batch-update success.
