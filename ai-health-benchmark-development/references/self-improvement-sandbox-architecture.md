# Self-Improvement & Sandbox Architecture for the AI Health Benchmark

**Session:** the specialist engine (Kyoto University)
**Date:** 2026-08-13
**Context:** principal requirement — benchmark must track rapid capability evolution while staying accurate, with a sandbox for any edits.

This is benchmark ENGINEERING (versioning, contamination, evolution), distinct from the physics scoring covered in SKILL.md and `references/advanced-physics-frameworks-2026-08-13.md`.

---

## 1. Three-Tier Test Architecture (resolves frozen-vs-evolving tension)

| Tier | Purpose | Mutability | Comparability role |
|------|---------|-----------|-------------------|
| **F (Frozen)** | Longitudinal tracking. Never changes after lock. | Immutable per epoch | The ruler. All historical scores stay comparable. |
| **C (Contamination-resistant)** | Same skills as Tier F, but with **parameterized variants** — different inputs/contexts testing same capability. Rotated quarterly. | Variant rotation | Detects memorization (score on variant << score on original = contamination). |
| **E (Exploratory)** | New capabilities not yet in frozen suite. | Freely added/removed | No longitudinal weight. Promotes to Tier F at epoch boundary. |

**Key mechanism:** Epoch-based freezing. Tier E tests that prove stable + discriminative over a full epoch (6 months) graduate to Tier F at next epoch boundary. Frozen tier never changes mid-epoch → within-epoch comparisons always valid.

**Bridging set (~20% of Tier F):** carried forward verbatim into next epoch's frozen set. Establishes calibration link for cross-epoch comparison. This is how MMLU/ImageNet *should* have evolved but didn't.

## 2. Shadow-Score Sandbox

```
LIVE INDEX (production)
  └── canonical_coupling_ai.py (frozen, tagged version)
  └── scores/{agent}/latest.json (what users see)

SANDBOX (staging)
  └── canonical_coupling_ai.py (proposed edit)
  └── replay/ — full historical score histories, replayable
  └── scores_shadow/{agent}/ — recomputed scores with proposed formula

VALIDATION GATE (automated, blocks promotion)
  ├── monotonicity: score ordering preserved on 1000 historical vectors
  ├── bounds: all scores stay [0,10], TWC stays [0,10]
  ├── sensitivity: formula change shifts <15% of scores by >1 point
  ├── physics-consistency: cascade still amplifies (TWC < linear when dims drop)
  ├── unit tests: verify() passes + new tests for changed behavior
  └── regression: shadow scores correlate >0.85 with live scores on bridging set
```

**Critical rule:** Sandbox NEVER touches live index. Live index only changes via promotion through the gate (git branch + replay engine + physics-consistency validator).

## 3. Framework Swappability (how new physics plug in)

The dimension is the interface, not the framework:
```
COG dimension (stable interface: returns score 0-10 + degradation signature)
  ├── v1: KL divergence (current)
  ├── v2: KL + entropy rate + Lyapunov λ_max
  └── v3: + recurrence determinism
```
Promotion path: implement in sandbox → validate against historical data → optional sub-signal → shadow-score one epoch → promote to default. Old framework stays as `--legacy` for one epoch.

## 4. Versioning (semantic + epoch hybrid)

```
v2.3.1
│ │ └─ patch: bug fix (no score change)
│ └─── minor: new sub-signal/telemetry (e.g., adding Lyapunov)
└────── major/epoch: frozen-set rotation + dimension add/remove
```
- **Patches:** bug/telemetry fixes, no semantic change. Ship anytime.
- **Minor (quarterly):** new sub-signals, new frameworks behind existing dims. Shadow-scored first. Additive.
- **Major/Epoch (6 months):** Tier E→F graduation, dimension restructuring, formula changes. Migration table + bridging calibration.

Every score: `{"epoch": "2026.2", "version": "2.3.1"}`. Cross-epoch comparison needs bridging-set calibration factor.

## 5. Contamination Strategy

**The private-frozen-set rule is critical.** Public benchmarks (MMLU, HumanEval) are contaminated because downloadable. Tier F must NEVER be published as a dataset — only scores published. Agents tested via orchestrated API calls against private test harnesses.

Tier C (variants) detects contamination: if model scores 9.0 on Tier F but 5.0 on Tier C variant of same skill → memorized → flag.

## 6. Update Cadence & Autonomous Learning

- **Continuous (per score event):** κ refined via LEARN stage. (NOTE: `twc_coupling_physics.py` MI layer is referenced in docs but MISSING from repo — the LEARN stage has no implementation.)
- **Weekly:** Tier E exploratory tests run; candidates flagged for promotion.
- **Quarterly:** Minor version. Shadow-scored sub-signal promotions. Contamination report.
- **Semi-annually (epoch boundary):** Major version. Tier E→F graduation. Frozen-set rotation + bridging.

**Self-learning (no human):** κ self-calibrates; thresholds set at 95th percentile of observed healthy-agent values (NOT hardcoded constants); Tier C variants auto-generate from Tier F templates; anomaly-driven test generation (novel failure → new Tier E test).

**Human-gated:** frozen set (Tier F), dimension definitions, scoring formula. Change only at epoch boundary with review. Benchmark learns its *parameters* autonomously; its *structure* evolves on the epoch clock.
