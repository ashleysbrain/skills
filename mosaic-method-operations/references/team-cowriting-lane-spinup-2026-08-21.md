# Team-Member Co-Writing Lane Spin-Up (Parag / finance session, 2026-08-21)

Pattern source: Parag finance session (ledger T-260821-0080..0084). Same
model as the Aditya health lane: principal writes, team member works alongside
in a dedicated thread until their own organism spins up (B2BU for Parag).
Reusable for the next member lane.

## Sequence (verified live, in order)

1. CONTEXT: session_search the member's name first (meetings, prior
   deliverables, standing directives) before minting anything.
2. PEOPLE: mint P-<NAME> in stores/people.json ONLY with a principal
   attestation quote in notes (provenance rule lives in people.json).
   Put lane semantics in notes: co-writing until organism spin-up,
   workspace path, known history.
3. WORKSPACE: <domain>-thread/ dir with briefs ON DISK before any child
   dispatch (chat context does not survive; children read briefs from
   disk): CENSUS-BRIEF.md (side-thread mission + live-probe law +
   per-source JSON schema), TOPICS-BRIEF.md (pool mission + QA chain),
   <MEMBER>-WALKTHROUGH.md (session map, live-stamped after step 6).
4. LEDGER MINT SET for a lane kickoff (kind/lane vocabulary that EXISTS
   in task-taxonomy): BRAINSTORM pool (kind=gap, lane=report), QA PANEL
   (verify/report), WALKTHROUGH (decision/report), CENSUS
   (gap/connectivity), census QA (verify/report). There is NO 'research'
   lane — census/ingest work goes under lane=connectivity.
5. SHELL DISCIPLINE: mint one task per line (assign the interpreter and
   gate path to shell vars, one invocation per row). This session a long
   inline multi-mint string corrupted mid-compose; bash failed CLOSED on
   the mangled segments (ledger untouched), but only a ledger readback
   proved which rows actually landed — the same readback also
   distinguished sibling rows (sibling-agent minted 0085/0086 the same
   minute) from corruption. Always read back id/state/created_by after a
   multi-mint before claiming the set is complete.
6. READINESS STAMPS before declaring the process ready (no stamp = not
   ready): conduction :port /health; Studio :port novelty-scan with a
   REAL domain claim — the finance probe "financial wellbeing scoring
   for households" returned TAKEN, top overlap 0.75, proving the gate
   discriminates in the new domain AND handing the panel its first
   crowding signal; ledger readback; child transcript tail
   (<agent-home>/cache/delegation/live/<deleg_id>/task-0.log) to watch
   census progress WITHOUT polling the child.
7. CHILD SHAPE: ONE child, sequential seats inside it (Otlet census ->
   Popper cross-exam; concurrent elite subagents = 429 death). The
   orchestrator builds the walkthrough doc in the main thread while the
   child runs — never idle on a running child.

## Brainstorm-phase clarify rule (principal correction 2026-08-21)

During an EXPLORATORY brainstorm kickoff, do NOT ask the principal to pre-pick
scope, sublane, or member role: "this is why we are going through the
brainstorming... don't ask silly questions." Generate the pool across
ALL lanes; the elite panel connects dots and ranks; the principal collapses.
Logistics questions (when is the session) are fine; scope questions are
not. Encoded as pitfall 6 in the elite-orchestration-default skill.

## Second lane spin-up (a teammate / design, 2026-08-21) — new pitfalls

8. DISPATCH SHAPE: delegate_task with a `tasks[]` array spawns N PARALLEL
   children even when told "sequential seats inside one child" — the array
   IS the parallelism. For sequential-seat children pass ONE goal string
   with the seat order spelled out inside it. (3-way parallel split
   caught and stopped 2026-08-21; 429 law would have killed them anyway.)
9. ORPHANED CLAIMS: killed/stopped children may have already CLAIMED the
   ledger rows before the stop lands. The re-dispatched child then sees
   "already claimed" and can stall or abort. Fix: check task_events for
   the claim actor, and if it matches (same harness actor identity), STEER
   the new child with "rows already claimed by your identity, skip the
   claim, go straight to work, --complete works because state=claimed".
10. QA-CHAIN TIMING: on an EXPLORATORY lane kickoff, do NOT pre-run the
    Andreasen + QA chain before the live session. Superposition law: the
    principal + member reaction IS the first measurement; run the chain after
    the session collapses the pool. (Contrast: Parag lane ran the chain
    pre-session because principal seeds were given; a teammate lane had none.)

## Files (reusable as the next lane's templates)

- /<workspace>
- /<workspace>
- /<workspace>
- /<workspace> (same four shapes, design lane)
