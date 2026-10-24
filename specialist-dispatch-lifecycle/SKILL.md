---
name: specialist-dispatch-lifecycle
description: "Run subagents end to end: dispatch, monitor, salvage, audit."
version: 1.0.0
category: operations
---

# Specialist Dispatch Lifecycle

Full lifecycle for dispatching specialist subagents in an
orchestrator/specialist system: dispatch contracts, liveness monitoring,
salvage of dead runs, and falsification-grade audit of specialist artifacts
BEFORE applying them.

Overlap note: `subagent-anti-timeout-patterns` covers timeout causes and
prevention; this skill covers the surrounding lifecycle (monitoring, salvage,
artifact audit). `agent-delegation-discipline` covers WHETHER to delegate.
Use all three together.

## When to Use
- Any delegate_task dispatch of named specialist work (one specialist, one
  microtask)
- While specialists run in background
- When a delegation dies, times out, or returns an artifact you must apply
- Before applying any specialist-authored spec/code/skill content

## 1. Dispatch Contract Rules
- ONE named elite specialist per microtask. Sequential build-on when there
  are dependencies; parallel only when genuinely independent.
- Never combine "verify/read/ground everything yourself" with "author a large
  deliverable" in ONE brief (see section 3).
- Cap the deliverable size in the contract ("under 200 lines") so synthesis
  fits the budget.
- Bake verified facts (paths, line anchors, sizes, ground-truth identifiers)
  into the context when they exist. Facts cross the dispatch boundary in the
  prompt; replacements must not rediscover them.

## 2. Monitor: Heartbeats and Silent Death
While children run, check liveness by transcript heartbeat:
`<agent-home>/cache/delegation/live/<deleg_id>/task-0.log` — size growth and
mtime age.

A run is DEAD, not slow, when ALL of these hold:
- `delegate_task action='list'` shows no live child
- No completion message arrived
- The run's `manifest.json` still says `"status": "running"`
- Transcript mtime is many minutes stale

Never tell the user "result inbound" for a run in that state — that is a
false status report. Diagnose, salvage, re-dispatch.

## 3. Verification-Synthesis Split

**UPDATED 2026-08-28 — the composition-death ladder.** When a harness bug
(`name 'max_iterations' is not defined`) kills seats AT COMPOSITION (after
4-11 min of successful exploration, before the write), apply the escalation
ladder in order — do NOT skip to self-build, ever:

1. **Salvage-retry** (first death): re-dispatch with the dead seat's
   transcript path + "READ IT (tail ~80 lines) to recover findings instead
   of re-deriving; WRITE THE SECTION FIRST after salvage." Works when the
   seat's exploration was the time sink.
2. **Write-only shape** (second death): pre-measure ALL facts yourself
   (mechanical extraction — schema PRAGMAs, row counts, thresholds, paths)
   and inline them in the dispatch. Hard rules in the brief: "your very
   first tool call must be the append; NO exploration; do not run queries;
   do not read other files; if a fact seems wrong tag it [UNVERIFIED]."
   Observed: 664s exploration-death → 89s write-only completion. CAUTION:
   verify the write actually completed — one write-only seat wrote a
   191-char fragment then died; check section size, not just header
   presence, and when extracting "the section after the last ## header"
   remember a final section extends to EOF.
3. **Cross-lane route** (limb itself failing repeatedly): post the build
   request on the operator bus to the sibling operator with the salvage
   briefing attached as a file. A dead dispatch limb is a routing problem,
   not a promotion to self-build. (principal correction 2026-08-28: "you do NOT
   BUILD YOURSELF" — logging the violation does not undo it.)

Rigor-demanding briefs ("verify the actual anchors, never invent paths")
make the specialist spend its whole budget grounding. It then dies before
synthesis. Split into two dispatches:

1. Grounding run: reads and verifies. If it dies after grounding, salvage
   the verified facts from its transcript (every read result is in the log).
2. Synthesis-only re-dispatch: "Do NOT re-read files; author directly from
   these VERIFIED facts" + lettered fact list + hard output cap + fixed
   section structure.

Re-dispatching the SAME combined brief reproduces the death; the replacement
re-verifies because the brief tells it to.

## 4. Transcript Salvage Procedure
For a dead/timeout run, before re-dispatching:
1. Read the full live transcript log.
2. Extract verified facts: file contents read, line anchors, sizes, live
   reproductions, hashes.
3. Fold them into the synthesis-only re-dispatch context.
4. Do NOT author the deliverable yourself from the transcript — that is
   main-thread specialist work (generalist drift). Only mechanical
   extraction is yours.

## 5. Artifact Audit Before Applying
Specialist-authored artifacts routinely contain confident fabrications.
Audit EVERY artifact against ground truth before applying ANY of it. Defect
classes observed (9 in one 103-line artifact):
- Invented identifier codes (wrong registry format, plausible-looking IDs)
- Wrong file paths (blueprint vs runtime, nested vs flat)
- Broken command syntax ("python 3" with a space)
- Invented CLI flags that the target binary does not have
- Test commands that drop required arguments
- Internally inconsistent format examples
- Wrong skill-directory layout

Audit rule: every path, flag, and identifier in the artifact must be
verified against the live system or cited as unregistered. Names only, no
codes, for unverified specialists.

Orchestrator-originated errors propagate: if YOUR dispatch context carries
an unverified identifier, the specialist will amplify it into more invented
ones. Ground truth starts with you.

## 6. Chain of Custody Format
Track the chain visibly for the user:

| Microtask | Specialist | State |
|---|---|---|

Applicator steps (applying a surviving artifact) are mechanically yours;
falsification review belongs to a Popper-class specialist; router/engine
changes cross to the sibling operator via the bus (post -> poll -> ACK ->
integrate, never fire-and-forget).

## 7. Falsifiability Gate
A dispatched artifact is not done until its own acceptance tests have been
RUN live and their outputs inspected. Commands that cannot run verbatim are
defects (see section 5). Report DONE only with executed-test evidence.

## Pitfalls
- Waiting on a dead delegation because a completion message "should" arrive.
- Re-dispatching a combined verify+author brief unchanged.
- Applying a specialist artifact because its structure looks right. Structure
  survives; details fabricate.
- Trusting your own dispatch context as ground truth without re-verification.
- Saying "specialist X is authoring" while you write the same deliverable in
  the main thread (parallel duplication).

## Support files
- `references/verification-synthesis-split-2026-08-16.md` — dual case study:
  two specialist deaths, salvage + synthesis-only re-dispatches, and the
  9-defect artifact audit that followed.
