# Cross-model critic seat — mechanics + rulings (proven 2026-08-21)

Session: TECH-TERRAFORM v1 QA pass 2 (deleg_5cc0ed45). First production use of a
genuinely cross-family critic seat; it fired and KILLED the protocol's free-energy
gate. Law origin: memory 2026-08-14+ (rotate elite brains; unanimous same-family
verdicts are suspect).

## Panel composition law

- Same-family unanimity (e.g. 6/6 LLM seats UPHELD) CONCEALS flaw classes — pass 1
  upheld the very gate pass 2's critic killed. Any high-stakes UPHELD needs at
  least one seat from a different model family before it counts as verified.
- Mechanism that worked: OpenRouter `openai/gpt-oss-20b:free`, temp 0, ONE call,
  prompt = target text verbatim + seat summaries (one-line each) + explicit kill
  instruction. Seats stay SEQUENTIAL in one child (concurrency law: max 1 elite).
- The critic sees only the one-line summaries of prior seats — independence is
  the point. If it re-derives a known wound blind, that is CROSS-FAMILY
  CONVERGENCE = confirmation of the wound, NOT novel damage: disposition stays
  "already bound for repair", possibly escalated (here: delta 4 escalated to
  FIX-NOW-FIRST, blocking the next stage-5 gate).

## Tool quirks (OpenRouter reasoning models via chat helper)

- `max_tokens` ≤ ~400 returns EMPTY content — the reasoning model spends the
  budget on reasoning tokens before any visible output. Budget ≥ 1600.
- Retry once at higher budget before switching models; keep temp 0.
- Verbatim-quote the critic's response into the review doc before any panel
  ruling — the ruling must cite the actual text, not a paraphrase.

## Ruling semantics (how to dispose of a cross-family kill)

1. KILL text is quoted verbatim + the kill line is logged (`critic: <model> KILLED — ...`).
2. Panel checks: is the flaw real? Is it ALREADY a delta from a family seat?
3. Real + already-bound → escalate the existing delta (don't mint a duplicate),
   record convergence explicitly, final verdict = SURVIVES CONDITIONAL.
4. Real + novel → treat as binding new delta.
5. The honest outcome shape is `N-upheld-with-deltas + 1-killed-on-known-flaw`,
   not unanimity. A pass that breaks unanimity is the system working.

## Records
- Full transcript: ~/your-workspace/technology-registry/REVIEW-TECH-TERRAFORM.md (QA PASS 2, Seat 5)
- Audit: ~/your-org/your-stack/audit/QA-PASS-TECH-TERRAFORM-v1-2026-08-21.md
