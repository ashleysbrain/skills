# Behavioral Physics Engine Spec Corpus

Last audited: 2026-06-03

## Purpose

The Divinity Science behavioral physics engine (internally "Diviq") is a layered equation engine that replaces flat single-score tracking with a full trajectory engine: observation, latent state estimation, past-behavior analytics, spacetime geometry, distribution geometry, dynamics, regime detection, and decision policy.

This reference documents the spec file corpus, the dedicated specialist, and the cross-document coherence check pattern used by the nightly self-healing operator.

## Specialist

- **PULSAR** (`INTP-5w4-PHYS-01`) owns the behavioral-physics translation lane
- Keeps math honest for curvature, trajectories, momentum, drift, barriers
- Only escalate to PULSAR when the lane needs that expertise (not for routine spec coherence checks)

## Spec File Inventory

| File | Role | Lines | Last modified |
|---|---|---|---|
| `docs/your-org-behavioral-physics-engine.md` | Canonical 8-layer engine specification with full math | 590 | 2026-06-01 |
| `docs/your-org-behavioral-physics-layers.html` | Presentation version (navy/gold themed, print-ready) | 388 | 2026-06-03 |
| `docs/plans/divinitygr-adaptive-baseline-engine-implementation-plan.md` | 8-task TDD implementation plan | 353 | unknown |
| `intel/products/DIVINITY-GR-ADAPTIVE-BASELINE-ENGINE.md` | Product architecture spec (Draft), 5-layer adaptive baseline | 797 | unknown |
| `processes/culture/SELF-HEALING-ORG.md` | Org-level self-healing philosophy (4 feedback loops) | 106 | 2026-03-23 |

All paths are relative to `~/your-workspace/hydra-os/`.

## Cross-Document Coherence Check Pattern

When running a nightly self-healing pass on the behavioral physics engine, follow this checklist:

### 1. Structural element count check
Extract countable structural elements from each file and verify they match:
- **Layer count**: MD spec lists 8 layers. HTML cards should be 8. Implementation plan tasks should map 1:1.
- **Pill/tag counts in HTML**: The hero summary pill row must show all 8 layers (Observation, Latent State, History, Geometry, Distribution, Dynamics, Regime, Policy). Easy to drift when one is omitted.
- **Dimension order**: PHY, PSY, SOC, INT, SPI, VOC, ENV, FIN must be consistent across schemas and specs.

### 2. Equation correspondence
Each layer in the MD spec has specific equations. The HTML presentation renders them in a simplified form. Check that:
- Every equation in the MD has a corresponding rendering in the HTML
- No layer in the HTML is missing its equations

### 3. Phase/ordering consistency
The engine's layer ordering is load-bearing:
1. Observation → 2. Latent State → 3. History → 4. Geometry → 5. Distribution → 6. Dynamics → 7. Regime → 8. Policy

Verify this ordering is identical in:
- MD spec ("How the layers stack" section)
- HTML presentation ("How the layers stack" section)
- Implementation plan (task order)
- Product architecture spec (rollout phases)

### 4. Implementation gap check
The implementation plan references these files. None exist yet (as of 2026-06-03):
- `products/principal-8d-tracker/baseline_store.py`
- `products/principal-8d-tracker/normalization.py`
- `products/principal-8d-tracker/calibration_engine.py`
- `products/principal-8d-tracker/activity_score_store.py`
- `products/principal-8d-tracker/quest_engine.py`
- `intel/products/schemas/user_baselines.schema.json`
- `intel/products/schemas/baseline_snapshot.schema.json`
- `intel/products/schemas/activity_score.schema.json`
- `intel/products/schemas/quest.schema.json`
- `products/principal-8d-tracker/tests/`

The schemas ARE defined inline in the product architecture spec (lines 236-416 of DIVINITY-GR-ADAPTIVE-BASELINE-ENGINE.md) and can be extracted directly when implementation begins.

### 5. HTML presentation drift detection
HTML files are最容易 to drift from their MD source because they are manually maintained presentations. Specifically check:
- Pill/tag counts in hero sections match the number of items in the spec
- Card sections match layer sections in the spec
- Equation rendering in HTML matches LaTeX in MD

## Known Mismatch (Fixed 2026-06-03)

The HTML file was missing a "Distribution" pill in the hero section. It showed 7 pills (missing Layer 5: Distribution Geometry) while having all 8 layer cards further down. Fixed by adding `<span class="pill">Distribution</span>` between Geometry and Dynamics pills.

## Relationship to Adaptive Baseline Engine

The behavioral physics engine spec and the adaptive baseline engine spec serve different layers:
- **Behavioral physics engine** = the math stack (8 layers from observation to policy)
- **Adaptive baseline engine** = the personalization layer that sits between evidence collection and the scoring math

The adaptive baseline engine is Layer 2 (latent state estimation) made user-specific. The product architecture spec (DIVINITY-GR-ADAPTIVE-BASELINE-ENGINE.md) defines a 5-layer sub-system for this personalization.

## No "Diviq" Branded Files

The name "Diviq" does not appear in any filename in the workspace. The behavioral-physics engine is identified by its full file paths. Do not search for "diviq" expecting to find dedicated files.
