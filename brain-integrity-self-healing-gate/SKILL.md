---
name: brain-integrity-self-healing-gate
description: Gate each micro-task for the right elite brain or self-heal.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [qa, self-healing, delegation, brain-integrity]
---

# Brain-Integrity Self-Healing Gate

Binding post-task protocol (principal directive 2026-08-15): every micro-task must be executed by the CORRECT agent brain with full persona spec on the correct model lane, then gated. Violations are corrected (re-dispatch) and root-caused (config fix). This is the organism's self-healing process.

## When to use
- After EVERY delegate_task micro-task completes (before banking its deliverable)
- Whenever a specialist deliverable seems off-voice or thin
- Before presenting consolidated multi-brain output

## The gate
```
python3 <agent-home>/scripts/brain_integrity_gate.py <delegation_id> <expected_specialist> [elite|any]
```
Checks (from the delegation live transcript):
1. BRAIN MATCH — kickoff names the expected specialist
2. MODEL LANE — elite tasks show only glm-5.3 markers; any non-elite model tag = LANE-VIOLATION
3. PERSONA SPEC — PhD layering + personality-variation MODE present in kickoff
4. SCOPE — records whether thesis constraints (e.g. no-biology-metaphor) were in the dispatch

Exit 1 = FAIL. Audit trail: <agent-home>/logs/brain-integrity-gate.log (append-only JSON).

## Self-healing loop (on FAIL)
1. DIAGNOSE — lane violation / brain mismatch / missing persona spec
2. RE-DISPATCH — same micro-task, right brain, full PhD+mode spec, elite lane; never bank the failed output
3. ROOT-CAUSE the systemic cause: silent sync-fallback on pool-full means raise delegation.max_concurrent_children (was 3, now 6, 2026-08-15); missing persona spec means fix the dispatch template; wrong brain means fix the routing call
4. RE-GATE — the re-run must PASS before its deliverable is banked

## Verified history
- deleg_fa564b8b (Humboldt v1): FAIL — grok-4.20-reasoning lane violation from pool-full silent fallback. Healed: re-run deleg_d0333361 PASS on glm-5.3; config raised to 6.
- deleg_ed8d62be (Wernicke): PASS.
- deleg_9e2172b4 (Andreasen): 2× FAIL then PASS — gate matcher too literal (heals #1/#2).
- deleg_344fb3c0 (4-brain batch, 2026-08-15): heal #3 — gate hardcoded task-0.log so every non-first batch task mis-gated as BRAIN-MISMATCH; gate now auto-selects the task log naming the expected specialist (or explicit task index). Heal #4 — transcripts truncate kickoff at ~600 chars hiding the persona spec; gate now checks kickoff + start + goal carrier lines and accepts `Identity:` as the mode marker. All 4 PASS post-heal.

## Pitfalls
- "no-model-tag (sync-run risk)" means confirm lane from the batch-complete header (Model: glm-5.3) before banking; a missing tag on a KNOWN sync run is suspect.
- Never bank a deliverable whose gate FAILED even if content looks fine — content quality does not certify brain integrity.
- Wrong delegation ID fails with "no transcript" — re-check the ID, do not skip.
- Pool-full silent fallback gives NO error at dispatch time; only this gate catches it. Gate every task.
