# Ideation QA Chain — 2026-08-20 research-thread run

Task class: generate N polished ideas (writing topics, project candidates, experiment picks) from a verified synthesis, with multi-brain QA. Session: research co-writing thread (principal + Aditya), "25 writing topic ideas after 5 thorough QA passes with different elite brains."

## The chain shape (proven)

1. **Generator (the specialist engine, creative cortex)** produces a raw candidate pool sized ~30% above target (32 raw for a 25-target) — QA passes kill candidates, so overgenerate. Brief carries: source files on disk (synthesis + census JSON), venue tags with a target split, anchor requirement (every candidate cites the synthesis element it stands on), realism bans (no clinical-outcome claims without data, no fabricated citations), and mix minimums (N health-agent, N case-study, N bridge, N methods, N practitioner).
2. **Mechanical integrity gate between generation and QA** — cheap checks BEFORE expensive brains: count, venue-tag split, anchor validity against the synthesis, em-dash/AI-tell scan, near-duplicate scan. The orchestrator runs this; it is not specialist work.
3. **Five sequential QA passes, five different brains, five distinct methodologies**, each receiving prior verdicts (chain-of-custody):
   - QA1 the specialist engine (she) — falsifiability: can the idea be killed by evidence?
   - QA2 the specialist engine — evidence/novelty grounding: does it stand on census-verified ground?
   - QA3 the specialist engine (adjunct) — calibration: scope vs realistic contribution
   - QA4 the specialist engine (adjunct) — operationalism: measurable claims, defined operations
   - QA5 the specialist engine (adjunct) — positioning: contribution vs normal science
4. **Closer consolidates survivors into ONE ranked doc at the target count** (orchestrator-role brain, e.g. the specialist engine for thread rhythm), with kill-risk notes per survivor.

## Lessons that fired live

- **QA the GROUND before QA-ing what stands on it.** Popper, run against the underlying synthesis first, returned: census mechanically clean (counts verified, all 20 cited IDs resolve) but the top-line claim under-bounded (org-psych constructs transfer conditionally, not universally) and 5 census legs errored. Consequence: SYNTHESIS-v2 (re-bound claim + census retry legs) became a dependency slotted BEFORE the positioning pass (Kuhn needs full census to rule on novelty). If candidates are anchored to pillars, the pillars get falsified first.
- **Dependency slotting, not parallelism.** When a mid-chain need emerges (synthesis v2), it joins the serial chain at its dependency point (before Kuhn), NOT as a parallel dispatch while the generator is airborne. One specialist in flight per workstream.
- **Anchor discipline does double duty**: it makes every candidate traceable to verified ground during QA, and makes the mechanical gate possible (anchors are machine-checkable against the synthesis's pillar/problem/layer IDs).
- Adjunct QA brains (Tetlock, Bridgman, Kuhn) carry full credential layering in the dispatch, no registry codes, per dispatch-discipline rule 4.
