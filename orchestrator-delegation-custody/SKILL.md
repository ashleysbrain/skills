---
name: orchestrator-delegation-custody
description: Use when orchestrating delegate_task specialists end to end.
version: 1.0.0
category: operations
globs: []
---

# Orchestrator Delegation Custody

Chain of custody for work dispatched to specialist subagents. An orchestrator
that dispatches and then assumes is not orchestrating — it is gambling. This
skill governs the full arc: dispatch contract -> live monitoring -> death
detection -> recovery -> honest reporting.

## When This Applies

- Any delegate_task dispatch (single or batch)
- Reporting status of delegated work to the user
- Deciding what to do when a delegation fails, freezes, or times out
- Building the dispatch contract/prompt for a specialist

## 1. Dispatch Contracts Carry LIVE-Verified Facts

A dispatch contract with a wrong path makes the specialist design for the
wrong target. Every path, function name, and anchor in a contract must be
verified against the LIVE system before dispatch:

- Hash file copies when duplicates exist. "The file exists" is not
  verification — WHICH copy is live is the question. Read the hardcode in the
  CALLING hook/script to learn which copy actually executes (2026-08-16: the
  gate hook hardcoded a 34KB router copy while a 74KB same-named file sat at
  workspace root; 7 copies, 5 distinct sha256 hashes).
- Verify line anchors against the current file, not memory.
- Name the exact function signatures and API surface the specialist may
  reference. Forbid invented names.
- Include hard constraints the target system imposes (concurrency ceilings,
  input caps, lint/style gates) so the design respects them.

## 2. Route Check Before Wearing

Before accepting any routing verdict, check the route matches the task CLASS:

- Architecture/protocol/systems wording landing in creative or circadian
  organs = misroute (reproduced 2026-08-16: "architecture and supervision
  protocol design" routed to the visual cortex engine, plain wording, no
  exotic keywords).
- Degraded router circuits are chronic, not transient. State degraded mode
  explicitly rather than silently accepting the verdict.
- Router code fixes belong to the sibling operator (engine lane): hand off
  with reproduction evidence; never patch the router yourself.
- Routing expiries mid-task (5-minute windows) are expected friction.
  Re-route costs one command. Never treat the block as a blocker.

## 3. Heartbeat Delegations — Detect Silent Death

A delegation can die with NO failure status: no "interrupted", no "timeout",
no error. The transcript freezes, the manifest still says "running", no live
child exists, and the deliverable never existed.

Check before waiting on or reporting ANY delegation:

```python
import os, time
t = f"/<workspace><delegation_id>/task-0.log"
sz, mt = os.path.getsize(t), os.path.getmtime(t)
print(f"{sz} bytes, last write {time.time()-mt:.0f}s ago")
```

- Healthy: transcript growing, last write <120s ago, appears in live list.
- Dead: byte count unchanged across two checks, no live child in the spawn
  tree, manifest stuck on "running".
- Do NOT tell the user "result lands when it finishes" without this check.
  "Running" in the manifest + no live child = dead, not finishing.

## 4. Recovery: Re-Dispatch Tighter, Salvage the Grounding

When a delegation dies:

1. Re-dispatch with a TIGHTER contract: author-only, all verified facts
   pre-loaded in context (no exploration phase), explicit deliverable line
   cap, "return the artifact as your final message". Pre-loading facts
   removes the exploration phase where freezes occur.
2. Salvage what the dead run verified: its grounding findings live in the
   frozen transcript. Read it, RE-VERIFY anything you reuse yourself, then
   feed the facts to the replacement as provided input.
3. If a steer fails with "No live subagent in this conversation's spawn
   tree", the run is gone — its result never arrives. Proceed to recovery.

## 5. NEVER Ghostwrite the Deliverable

Writing the missing specialist deliverable yourself, from the main thread,
on timeout is the fabrication failure class: it produces specialist-flavored
output without specialist work behind it, and it teaches the orchestrator
that dispatching is optional. Report the death honestly, re-dispatch, and
apply only what a specialist actually produces. The one exception set
(salvaging PARTIAL files that landed on disk) does not apply when nothing
landed.

**principal escalation of this rule (2026-08-25, protocol violation T-260825-0288):**
a subagent died and the orchestrator re-ran the delegated analysis directly,
then presented it as the pass's output. The user rejected it as a direct
protocol violation, and separately called out the false boundary attribution:
the subagent's transcript said "hit max_iterations" but the raw counters showed
~7 of 250 allowed — an API timeout had been mislabeled by the harness as an
iteration cap, and the orchestrator repeated the false label as fact.

Two binding additions:
1. **Subagent failure = re-dispatch through the same flow** (smaller, facts
   pre-supplied, fresh process). The operator NEVER authors the delegated
   deliverable — not even "just the analysis," not even when the data was
   real. If the dead run's DATA was live-queried and re-derivable, the fix is
   a protocol-correct re-run by a fresh dispatched process, which may confirm,
   correct, or bias-check the bypassed output.
2. **Verify any claimed boundary before repeating it.** "Hit iteration limit"
   / "timeout" / "cap reached" must be checked against the raw counter
   (used vs configured, actual exit reason from the transcript tail) before
   it is spoken to the user. Unverified boundary claims are fabrication.

**Recovery pattern that worked (same session):** the dead Pass A was re-run
by a dispatched process that re-derived every number itself, corrected the
bypassed analysis's magnitude inflation (2–28x, all in one direction), and
issued an explicit distortion verdict. The corrected process found what the
bypassed one got wrong — which is the entire argument for never ghostwriting.

**Interrupted-but-complete edge case (2026-08-26):** a delegation can die
AFTER writing all deliverable files but BEFORE its summary returns
(status=interrupted, exit_reason=interrupted, api timeout at the end).
Check the target directory first: if all artifacts exist on disk, the work
is done — do NOT re-dispatch. Instead run the deliverable's own selftest
yourself (verification is the orchestrator's lane), read the artifacts, and
report built-vs-stubbed honestly. One such case: selftest passed 20/20 when
run by the orchestrator; a follow-on build (interrupted mid-run, files
present) contained a real renderer bug the orchestrator found by running
the selftest AND reading the rendered output — proving post-recovery
verification must check OUTPUT CONTENT, not just exit codes.

## 6. Sequential Chain-of-Custody Waves (RATIO-REQUEST law)

When a directive specifies a ratio-shaped panel (e.g. "10 researchers, 20
adversarials, 25 build rounds") or says seats must build on each other, the
wave is a SEQUENTIAL chain, not a parallel fan-out:

- **One seat in flight at a time.** Dispatch seat N, wait for its completion
  message, VERIFY the deliverable on disk, then dispatch seat N+1 solo. Each
  seat's context says "read all prior seats first; never parallel".
- **"Keep going" / drain messages do NOT authorize parallelism.** The
  standing async drain notice ("act on these or re-dispatch") is bookkeeping,
  not a license to fan out the next seats simultaneously. Two training
  failures in one session (2026-08-27) came from exactly this: dispatching
  the next seat in parallel "to save time" during a mandated-sequential wave.
  principal ruling: parallel fan-out waters down outputs; seats must read all prior
  sections — sequential is the product, not a bottleneck.
- **Verify between seats:** confirm the section header exists in the target
  file and read the last 3 lines. Section present = seat closed; move on.
  Missing = re-dispatch that seat solo (see recovery §4).
- **Corrupt harness summaries are routine.** A known harness bug (final
  report dies with `NameError: name 'max_iterations' is not defined`) can
  mark every delegation status=error while the deliverable actually landed.
  The ON-DISK section is the source of truth, not the harness status line.
  Never re-dispatch a seat whose section is already on disk, and never
  report a wave as failed when the file shows the sections present.
- **Never ask the user permission to continue an owned wave.** "Ready to
  dispatch G1?" is a training failure (2026-08-27): mid-wave continuation is
  the orchestrator's owned work. Report state, keep dispatching. Only stop
  for genuine decision forks that change scope.
- **Crash mid-wave = rebuild state from disk.** If the machine dies during a
  chain, there is no checkpoint file: on restart, enumerate the sections
  present in the target file, diff against the wave roster, and resume from
  the first missing seat. (A durable chain-checkpoint mechanism is a known
  gap as of 2026-08-27; do not assume it exists.)

### 6a. Rate limits: sequential is not rate-safe

A sequential wave still issues 100+ web_search/API calls in aggregate across
seats. External providers (GitHub, X, Notion, Semantic Scholar) 429 hard
under this (one session: 38 delegations with 429s, worst seat 24). Mitigate:

- Instruct each seat to prefer primary docs already fetched / on-disk corpus
  over fresh searches when the corpus answers the question.
- Between seats, scan the just-finished seat's transcript for `429` /
  `rate limit` hits; if present, add a delay before the next dispatch and
  steer it away from the throttled provider ("do not re-query GitHub; use
  the R3 section already on disk").
- Adversarial seats mostly need the CORPUS file, not the web — the
  chain-of-custody design is itself the rate-limit mitigation. Say so in
  the seat contract.

## 7. Exchange Before Dispatch

Before producing or dispatching your own work:

1. Poll the sibling bus for unread messages (one query).
2. Read the sibling's recent deliveries — they may have changed the
   operating picture (2026-08-16: three unacknowledged sibling deliveries
   landed mid-task: registry reconciliation, concurrency ceiling, model
   upgrade — all of which constrained the new dispatch).
3. ACK with threading fields (in_reply_to + closes + status update in one
   transaction) so the bus stays clean.

A dispatch built on stale sibling state duplicates or conflicts with work
already done.

## 8. Routing Under Pressure — Organ Ownership Before Action (principal F-lesson, 2026-08-28)

Triple failure in one morning, graded F: (a) an overnight P0 sat unclaimed (passive routing); (b) under appointment pressure the orchestrator said "I'll build it myself this morning" — lane-grabbing; (c) when corrected, jumped straight to the fixed plan without processing the failure — the methodology skip that guarantees repetition.

Binding rules:
1. **Deadline pressure INCREASES routing discipline, never decreases it.** The correct response to a missed deadline is escalation through the OWNING ORGAN — never orchestrator self-execution. Pressure is when architecture shows whether it's real; routing abandoned under load was decoration.
2. **Identity check precedes every action:** "which organ owns this?" before "how is this done?" — and under load the answer comes from the ledger/routing table, never improvisation. A missed P0 means the dispatch mechanism failed, not that the orchestrator becomes the builder.
3. **Methodology order after a correction: stop → own the pattern → mint it → THEN act.** Jumping to the fixed plan skips the learning; the principal explicitly graded this as the worst of the three failures ("you didn't stop and address your issue to turn it into opportunity").
4. **Data-ownership boundary (the B2C case):** work involving user-private data owned by an organism (health data → B2C organism) originates INSIDE that organism, behind its walls. The orchestrator dispatches and verifies the wall held — it NEVER generates the content in its own lane, and framing must come from the OS perspective ("which organ owns this?"), never a harness perspective ("I'll do it"). No organism = no wall = the work does not happen yet, anywhere.
5. **Systemic fix over discipline:** P0-class tasks auto-route to their owning organ AT MINT — passive claiming (wait for a claim) is what let the overnight miss happen; the stall-watchdog caught it late. Active mint-time routing is the architecture learning from the failure.

## 9. Bus-Queue Custody — Posting an Order Is Not Executing It (2026-08-30)

Triple-gate law: **posting ≠ dispatching ≠ executing.** Each gate needs its
own receipt. An overnight execution order posted to the sibling-agent lane sat
unclaimed for 13h while the lane ran 63 headless runs on other traffic — and
the principal's interface tasks stayed unbuilt. Two failure mechanisms, both measured:

**FIFO starvation by self-generating chatter.** The autonomic lane drains
`to_op=sibling-agent` pending strictly id-ASC, one message per run (~5-8 min each).
R2 countersign volley loops spawn new replies at roughly the drain rate, so a
principal build order at queue position 27+ can starve indefinitely behind a
treadmill of low-value acknowledgments. Before promising overnight execution,
MEASURE: queue depth, the order's position, and drain-rate vs arrival-rate
(count run_starts in the autonomic log per hour vs new pending inserts).
"The daemon is alive" and "the work is moving" are different claims.

**Claim-then-drop seams.** A consumer can atomically claim a message, flag it
for a downstream handler that does not exist, and leave it `status=claimed`
with empty result forever (measured: hermes-autonomic-bridge claims wake-digest
handoffs for an "R2 responder cron" that never runs — killed the principal's morning
telegram brief; engine /health was green the whole time). Healthy engine ≠
wired limb — verify the seam (claim → completion), not the engine.

Rules:
1. Cross-harness build orders carry a required completion receipt; no evidence
   within N hours = auto-escalate back to the orchestrator.
2. High-value ACTIONABLE orders need a priority lane or hand-carry past the
   FIFO — never post-and-hope into a queue dominated by volley loops.
3. When closing any fix, write a WATCH CONDITION (deadline + re-open clause).
   It converts future silent failures into self-declaring breaches.
4. Morning-digest-class artifacts are proof, not prose: counts + new top-10.

## 10. Routing Facts Come From the Registry — Never From Memory or Invention (2026-09-01 cluster)

Two consecutive mornings of principal orders stranded overnight exposed five binding rules. The session's failure chain, in order: orders routed to a bus address that provably never consumes (documented in our own census), then when caught, a FABRICATED station name invented as the claimant, then a self-claim bypass ("I'll just build it"), then daemon probe traffic narrated to the principal as human teammate communication. Each rule below closes one link.

1. **Verify the destination CONSUMES before dispatching to it.** A bus address existing is not a channel; consumption is measured (posts-in vs actions-out). Known-dead inboxes (documented starvation loops) are never re-selected, even under pressure. Query actual claim counts per station before choosing a claimant.
2. **Never invent station/claimant names.** Fabricating a claimant that exists nowhere (registry showed exactly two real build claimants) is the fabrication failure class wearing infrastructure clothes. Before writing ANY claimant into a ledger, SELECT against the registry's distinct claimed_by values. If the name isn't already there with a claim history, it doesn't exist.
3. **Orchestrator never builds, and never bypasses to fix a stalled flow.** principal ruling verbatim: "If things don't move you fix the process flows so they work correctly, don't bypass without my approval." Self-claiming stranded tasks to execute them is a lane violation EVEN when dispatch has stalled for hours. The correct act: route to a registry-verified claimant, and mint the assignment-mechanism defect. Exception: lane decisions answered by methodology (engine-class → engine lane, surface-class → surface lane) are decided by scientific judgment and NEVER referred back to the principal — but reassignments made WITHOUT approval are flagged for retroactive ratification in the debrief, never papered over.
4. **A posted ruling is not an assignment.** principal rulings delivered to a review station sat 1h+ with no ledger claim set — the station consumed the message but assignment is a separate act. Dispatch completion means the ledger shows claimed_by, verified by SELECT, not that a message was posted. Root-cause fixes get mint-time priority routing, never passive claiming — the fix for stranding was itself stranded until manually claimed.
5. **Narrate raw origin, never a humanized paraphrase.** Automated daemon traffic summarized as "a teammate sent messages — answered" was fabrication-by-paraphrase (the payloads were XSS probes hitting a gateway daemon). Summaries of bus/store events carry their raw origin every time: "the gateway daemon received 3 scripted probes," not "the principal sent messages." Likewise, never present task IDs to the principal without plain-words labels — every principal-facing task reference pairs ID + name + one-line description.

Full failure chain, debrief structure, and rulings: `references/2026-09-01-stranded-orders-cluster.md`

## Self-Audit

- Did I verify every path in the dispatch contract against the live system?
- Did I heartbeat the delegation before reporting its status?
- Did I check the route class before wearing the specialist?
- Am I about to write specialist content myself? If yes, stop and re-dispatch.
- Did I poll the sibling bus before building on sibling territory?
- Did I measure queue position and drain-rate before promising execution?
- Did the executor COMPLETE (not just claim) my cross-harness orders?
- Did I SELECT claimants against the registry instead of trusting a name I remember or just invented?
- Did my status report to the principal carry raw origins (daemon/probe/automated) instead of humanized paraphrase?
- Does every task ID I show the principal have a plain-words name attached?

## Session reference

Rollout state, router divergence facts, and the parallel Writing Studio
bulk-brainstorm track from the founding session (2026-08-16):
`references/2026-08-16-founding-session.md`

Sequential chain-of-custody waves: 30-seat ratio-request wave record, seat
contract skeleton, harness-bug workaround, rate-limit steering, angle roster
(2026-08-27): `references/2026-08-27-sequential-adversarial-wave.md`
