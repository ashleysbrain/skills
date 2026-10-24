# Self-Healing OS 4-Brain QA Panel — 2026-08-15 (deleg_344fb3c0)

Session detail for the elite-panel QA of the organism self-healing OS.
Method: live probes only (sqlite reads, HTTP health checks, launchctl/plist
inspection, source reads, read-only stage replay). Every claim measured.

## Panel composition + dispatch pattern

Four specialists in ONE batch delegation (tasks[] parallel), each with full
persona spec in the dispatch context: Tanenbaum (OS supervision), Lamport
(TLA+ state machine), Scheffer (critical transitions — the theorist whose
work the organism's detector claims to implement), Bridgman (operationalism
grading). Panel design principle proven here: **seat the originator of the
theory when auditing an implementation of it** — Scheffer found the detector
blind spot nobody else could, because he wrote the theory it half-implements.

## Evidence-pack-first dispatch

Each brain got the SAME verified evidence pack (exact numbers, ports, paths,
timestamps from the main thread's live probes) plus permission to re-verify.
This kept 4 parallel brains from diverging on facts and let them go straight
to verdicts. All four independently re-probed (7-33 api_calls each) and
confirmed the pack — R2 discipline by construction.

## Verdict formats that worked

- Tanenbaum: text supervision tree + subsystem grades (4 FAIL, 1 PASS)
- Lamport: stage-walk table (EXECUTES/DEGRADED/DEAD per stage) + property
  violations stated formally + numbered minimal repairs
- Scheffer: mechanism → why detector missed it → design law (quotable) →
  prescription with thresholds AND the date each alarm WOULD have fired
- Bridgman: component ledger table (grade + one-line live evidence each) +
  delete/archive list governed by a stated rule

## Batch-mode result recovery (the transport lesson)

Live transcripts truncate: kickoff lines at ~600 chars, final summaries at
~413 chars with `(+N)` markers. The FULL deliverables are NOT in the .log
files. Recovery chain that worked:
1. Batch-complete message names the files: `<agent-home>/cache/delegation/
   subagent-summary-<task>-<timestamp>.txt` — these are COMPLETE.
2. Read them directly; they contain the full verdict + a "Summary for parent"
   footer (what I did / key findings / grades / files touched / issues).
3. The live task-N.log remains useful for watching tool calls mid-run and
   for gate evidence (kickoff/start/goal lines), never for the deliverable.

## Gate interaction (batch mode)

The brain-integrity gate pre-fix mis-gated 3 of 4 tasks (hardcoded task-0.log).
Post-fix (auto-select by specialist name) it gated 4/4 PASS. For batch
delegations, gate each specialist by name; the gate now resolves the task
log itself. Lane check note: batch runs show "no-model-tag" in transcripts —
verify the lane from the batch-complete header (`Model: glm-5.3`) instead.

## Handoff pattern (QA -> sibling-agent)

Post the remediation order to the operator bus with EXACT refs per item
(engine, port, registry code vs live code, file paths, the specific repair).
Done-in-my-lane items listed separately from handed-off items. Verdict doc
at one canonical path (organism/QA-SELF-HEALING-OS-2026-08-15.md) + bus msg
number referenced from O'Keefe so future sessions can trace it.

## Crossover test (definition of healed)

(a) one Virchow finding closes end-to-end, (b) interventions column non-empty
once, (c) a stale operator flips dead without human action, (d) TWC variance
nonzero 7 consecutive days.
