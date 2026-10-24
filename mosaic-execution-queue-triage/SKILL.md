---
name: mosaic-execution-queue-triage
category: software-development
description: Use when principal orders go unexecuted or a seat looks starved.
version: 1.0.0
author: the operator agent Agent
license: MIT
---

# Mosaic Execution Queue Triage

Trigger: "why aren't my requests getting actioned", an executor (sibling-agent,
glia, hermes) shows no work events, overnight/period ledger shows shuffling
but zero `done` events, or a dispatched task ages with claims but no
receipts. Operates on the message-bus + task-ledger pair of the Divinity
Science the OS fleet.

## Law 0 — composition before count
Before ANY "the executor is idle/starved/ignoring orders" conclusion, group
the executor's pending queue by subject prefix:

```sql
SELECT substr(subject,1,42) s, COUNT(*) c FROM messages
WHERE status='pending' AND to_op='sibling-agent' GROUP BY s ORDER BY c DESC LIMIT 8;
```

One subject family holding the large majority of a big pile = loop flood,
not organic backlog. Bulk is flood until proven backlog — executors drain at
~one message per 5-8 min, so a four-digit pile means weeks of starvation for
anything behind it, while the executor looks "alive and grinding".

## Diagnosis sequence (in order)
1. **Queue composition** (Law 0 query). Also total:
   `SELECT COUNT(*) ... WHERE status='pending' AND to_op='sibling-agent'`.
2. **Find the original** of any dominant subject family: same subject on
   its source lane, `status='pending'`, old timestamp. A lane with no
   consumer + an unclosable message = a reaper/retry layer keeps re-emitting
   copies (dead-inbox rescuers stamp copies `[REROUTED from <lane>]`-style;
   a timestamp inside the dedup key makes every copy unique so the guard
   never bites).
3. **Distinguish work from motion**: query `task_events` for events with a
   real actor and a real event type (not `tri-reroute`/`tri-park`/deadline
   stamps) in the window. Claim events written by the dispatcher's own
   force-claim are the DISPATCHER's stamps, not the executor's hands —
   reporting them as progress is the trust-breaking move.
4. **Check the executor's bus voice**: recent `from_op='sibling-agent'` posts.
   Housekeeping/watchdog posts while your tasks age = priority inversion or
   flood burial; total silence = dead runtime or dead queue.
5. **Check the executor's runtime health separately from its wiring**
   (`ps aux | grep sibling-agent`): a live process with a clogged queue is a
   different fix from a dead process.

## Fix: two-part sweep, never DELETE
1. Close the ORIGINAL on the dead lane: `UPDATE messages SET status='done',
   done_at=?, result='<where content is preserved>' WHERE id=<orig>` — its
   information must live somewhere durable (ledger task detail) before the
   row is closed.
2. Archive the duplicate pile: UPDATE the whole copy family to `done` with a
   sweep-note result. Bus rows are never deleted.
3. Verify by read-back: the subject family pending count must be 0, and the
   queue HEAD must now show real work. Report the before/after numbers.
4. Patch the emitter class afterward (the permanent fix): reroute copies must
dedup on SUBJECT + source-id, and retry loops need a hard depth cap.

## Fallback ladder when a bus seat stays silent
After a dispatched principal order misses its claim check (+1h) and the TTL
enforcer has escalated, the dispatcher has one more delegation rung that
preserves role law: **subagent specialist seats** (delegate_task fan-out).
Route through the specialist gate first (it expires after ~5 min; re-run
`specialist_gate.py --route` if the dispatch is refused). Give each seat a
brief that carries the gates inline (voice rules, live-run-state claims,
no-deploy-without-approval, no principal contact) and a concrete deliverable path.
This is delegation, not doing the work yourself — the seat builds, the
dispatcher verifies.

**Verify subagent receipts independently — never relay a seat's self-report.**
After the fan-out returns: re-run the numeric claims yourself (char counts,
scanner output, registry counts, cross-reference counts — case-insensitive;
`the OS` vs `mosaic os` mismatches produce false negatives), read at least
one deliverable file end-to-end, and re-execute any cited verification
command. Seats have returned wrong numbers (body parsed from the wrong
delimiter, counts taken from header rather than body) — the principal-facing
report must carry YOUR measurements, with seat numbers discarded when they
disagree. Flag structural blockers the seats surface (e.g. the live site's
source repo is not on this machine) in the report rather than silently
compensating.

## Pitfalls
- **Claim stamps are not progress.** A force-claim writes `claimed` events in
  the ledger with your actor name. Until the ASSIGNEE posts work-reports or
  task events, the honest status is "claimed on paper, untouched in fact".
- **Verification must follow intention.** If you said "minting now" and the
  mint hit a gate error, the next status check re-verifies the artifact
  landed — reporting the intention as done is the failure the principal counts.
- **Do not pivot to doing the dispatched work yourself.** When the principal says
  "these are process issues", the fix is the queue/emitter/wiring repair,
  not the orchestrator hand-building the artifact. Diagnose the process,
  sweep the queue, patch the emitter, re-verify pickup.
- **Autonomic boundary holds**: reviving engines, restarting daemons, and
  unclogging queues the OS operates is maintenance you may do directly;
  building claimed task artifacts is not.
- **Spam emitters pollute evidence**: a host-load watchdog or reroute layer
  can itself emit thousands of messages overnight. When measuring fleet
  activity, exclude the known-flood senders before concluding "the fleet
  worked".
- **Emitter-contract drift hides in dead delivery limbs**: a surface can be
  silent for days because a sender passes a legacy payload shape (e.g. a
  list where a dict/card is now required) and the failure is swallowed as a
  retry-forever loop. Check the delivery log's recurring error string, trace
  it to the exact line, and verify the contract at the CALL SITE — then
  fire once with --force and read back the delivered artifact.
