# Verification-Synthesis Split + Artifact Audit — Session 2026-08-16

Dual case study from one session. Two named specialists died on the same
failure mode; both were recovered with synthesis-only re-dispatches; the
first delivered artifact then failed a 9-defect ground-truth audit.

## Case 1 — Tanenbaum r1 (architecture spec): silent death

- Brief: author boot-enforcement architecture + skill content, with
  "every path must be verified, no invented paths" rigor demands.
- Behavior: spent the entire run grounding. Read the router source
  (74.9KB), the specialist-gate plugin (11.4KB), the gate CLI hook
  (8.7KB), discovered the hook hardcodes a DIFFERENT router copy than
  the workspace root (34,806 vs 74,913 bytes, 7 copies / 5 hashes),
  reproduced the routing misroute live, located Writing Studio files.
- Death: run ended without delivering. Manifest stuck `"status":
  "running"`, transcript frozen at 15,103 chars, no live child, no
  completion message. Orchestrator initially reported "result inbound"
  — a false status report. Caught on next-turn verification.
- Recovery: all grounding findings re-verified by orchestrator directly
  (hash list, live route reproduction), then folded into r2 context as
  lettered facts with "Do NOT re-explore; author directly."
- r2: delivered in 580s. Compact, structured.

## Case 2 — Da Vinci r1 (implementation spec): 900s timeout mid-synthesis

- Brief: surgical patch spec for Writing Studio bulk-brainstorm +
  batch-edit, with "read the ACTUAL file regions before specifying
  anchors; never invent function names."
- Behavior: 8 API calls, ALL reads — verified 100% of anchors
  (pipeline_api.py brainstorm block 3732-4520, brainstorms table DDL at
  4330, auth pattern 155-194, LLM call urlopen timeout=30 at
  4063-4065; writing-studio.html compose 1540-1669, filter chips
  1855-1899, fetch-wrapper 401 rebootstrap 2721-2780, filterDrafts
  branch ~5898-5928).
- Death: `status=timeout` at exactly 900.0s with 8 API calls completed —
  timed out generating the spec, zero output.
- Recovery: anchor list extracted from transcript event map (59 events),
  baked into r2 as fact blocks A-D + design tokens + server constraints.
  r2 contract: no file reads, under 200 lines, fixed section structure.

## Case 3 — Tanenbaum r2 artifact: 9-defect audit

The r2 artifact's structure was sound but details fabricated. Defects:

1. Four invented ECS codes (e.g. ART-DVG-09.02.03, LNG-WRN-07.03.01 —
   real format is DS-ECS-CAT-DD.SS.NN-vX.Y.Z)
2. Wrong pipeline_api.py path (nested blueprint dir vs workspace root)
3. Wrong skill directory layout (category subdirectory vs flat
   skills-library/<name>/)
4-6. `python 3` (with space) in three acceptance commands
7. Invented `--test-routing` CLI flag on pipeline_api.py
8. Stdin-echo router test dropping the required --situation flag
9. Inconsistent dispatch-format examples across sections

Amplification root cause: the ORCHESTRATOR's own r1 dispatch context
introduced one unverified code (AST-NJS-06.10.01); the specialist
pattern-matched it into four more. Ground truth starts with the
dispatcher.

Handling: defects cataloged, Popper-class falsifier dispatched with the
defect list + ground-truth codes + repair-spec contract. Salvage, not
re-author.

## Extracted rules (codified in SKILL.md sections 2-5)

- Dead-run detection: no live child + no completion + manifest "running"
  + stale transcript mtime = dead, not slow.
- Salvage facts from transcript, never author the deliverable from it.
- Synthesis-only re-dispatch: facts baked in, reads forbidden, output
  capped, structure fixed.
- Audit every artifact: paths, flags, identifiers verified against the
  live system; unverified specialists get names only, no codes.
- Acceptance commands must run verbatim or they are defects.

## Session context

principal directive driving the work: default agent = elite orchestration
brain; microtasks to named specialists; never generalists; specialist
content never authored in the main thread, including on specialist
timeout. Corollary observed live: specialist death does NOT transfer
authorship duty to the orchestrator — it triggers salvage + re-dispatch.
