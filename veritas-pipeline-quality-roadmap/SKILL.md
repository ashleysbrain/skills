---
name: veritas-pipeline-quality-roadmap
description: "Make VERITAS produce peer-review-survivable academic output."
version: 1.0.0
---

# VERITAS Pipeline Quality Roadmap

After 13 structural fixes (all resolved), 5 microtasks remain. Bus msg 1738.

## M1: Semantic Citation Verification (P0)
`verify_ground_truth` (L1265) uses keyword overlap. Extract [N] markers from
draft, match to papers, compute claim-abstract overlap. Flag <20%.

## M2: Panel Deliberation (P1)
Stage 5 seats independent. After all verdicts, ONE LLM call with draft +
anonymized dissent for synthesized rebuttal.

## M3: Human Checkpoint (P1)
Pause after stage 2 as awaiting_human_review. POST /api/veritas/resume/{id}.

## M4: Gap Analysis (P2)
Check each DS core domain has >=1 paper. Flag missing. Do not block.

## M5: Revision Tracking (P2)
Extract actionable items before/after revision. Per-concern status.

## NOT to build
No embeddings, no per-seat rounds, no gap blocking, no truth replacement.
