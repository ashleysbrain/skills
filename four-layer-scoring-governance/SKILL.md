---
name: five-layer-scoring-governance
description: Five-layer autonomous scoring governance + VERITAS dogfooding system for Divinity Science. Layers 1-4 cover algorithm integrity, organizational health, scoring maturity, and builder-product correlation. Layer 5 adds strategic methodology evolution and horizon scanning. The VERITAS Dogfooding layer uses our own peer review product to QA our content and platform, serving as both quality assurance and product validation.
tags: [twc, 8d360, scoring, governance, algorithm-integrity, organizational-health, scoring-maturity, builder-product, methodology-evolution, veritas, dogfooding, your-org]
version: 2.0
---

# Five-Layer Scoring Governance + VERITAS Dogfooding System

## When to Use
- Managing or troubleshooting the autonomous scoring governance crons
- Understanding the five layers of scoring oversight plus VERITAS dogfooding
- Adding new checks, engines, or validation steps
- Explaining to the principal why a specific cycle exists and what it does
- Adjusting cadence, model, or prompt for any cycle
- Onboarding a new agent to the scoring governance architecture
- Understanding how VERITAS serves as both internal QA AND product development

## Architecture Overview

The system has TWO parallel missions:
1. **Scoring Governance** (Layers 1-5): Ensure the 8D/TWC scoring system is correct, improving, and strategically sound
2. **VERITAS Dogfooding** (Platform Layer): Use our own peer review product to QA all DS content, simultaneously improving content quality AND validating the VERITAS product

```
SCORING GOVERNANCE:
Layer 1: Algorithm Integrity (VERITAS-ALGO) — "Is the math right?"
    ↕ feeds into
Layer 2: Org Health (STRATEGOS) — "Is the company healthy?"
    ↕ depends on
Layer 3: Scoring Maturity (AXIOM) — "Is the product ready?"
    ↕ measured by
Layer 4: Builder-Product (SYNTHESIS) — "Is it helping the builder?"
    ↕ evolved by
Layer 5: Methodology Evolution (HORIZON) — "Is this the RIGHT approach?"

VERITAS PLATFORM LAYER (parallel):
VERITAS-DOGFOOD — "Does our peer review product work? Is our content excellent?"
```

Each layer has an independent AUDIT agent running on a different model (DeepSeek R1) to catch model-specific blind spots.

## The Five Scoring Cycles

### Cycle 1: TWC Algorithm Integrity (Every 12h)
- **Agent:** VERITAS-ALGO (PhD Computational Math MIT, PhD Psychometrics Stanford, Fellow ASA)
- **Cron ID:** `63f7dd22c96d`
- **Schedule:** Every 720 minutes (12h)
- **Model:** google/gemini-2.5-pro
- **What it checks:**
  1. Rescore engine test suite (7 tests must pass)
  2. Nutrition engine validation
  3. Sexual health engine validation
  4. Interaction matrix integrity (5 checks, 28 pairs)
  5. Scoring pipeline coverage (7-day gap detection)
  6. Drift detection (baseline comparison)
  7. Activity database integrity (dimension balance)
  8. Integrity report compilation and logging
- **Auto-fix:** Spawns fix agents immediately on any failure
- **Logs to:** ~/your-workspace/health-private/algorithm-integrity-log.md

### Cycle 2: the specialist engine 8D Improvement (Every 8h)
- **Agent:** STRATEGOS (PhD Org Behavior HBS, PhD Complex Systems Santa Fe, ex-McKinsey CSO)
- **Cron ID:** `0ad89e5ea49d`
- **Schedule:** 0 */8 * * *
- **Model:** google/gemini-2.5-pro
- **What it does:**
  1. Gathers evidence from 16 organizational data sources
  2. Scores all 8 dimensions using evidence-based methodology
  3. Computes TWC with proprietary formula (weighted sum + coupling)
  4. Root cause analysis for 3 weakest dimensions
  5. Cascade analysis (identifies feedback loops)
  6. ILS computation (intervention leverage scores)
  7. Spawns fix agents for highest-ROI interventions
  8. Verification pass and concise report
- **Key principle:** NEVER scores from vibes. Plans that haven't shipped = 0 VOC credit.

### Cycle 3: Scoring Maturity Index (Weekly Sunday 9AM CT)
- **Agent:** AXIOM (PhD Software Engineering CMU, PhD Measurement Science UvA, ex-FDA Digital Health)
- **Cron ID:** `58d2ec241296`
- **Schedule:** 0 9 * * 0
- **Model:** google/gemini-2.5-pro
- **What it measures (SMI 0-100):**
  - Engine Completeness (25 pts): Which engines exist and work
  - Test Coverage (20 pts): Automated test pass rates
  - Validation Coverage (20 pts): Independent panel review status
  - Data Quality (20 pts): 30-day coverage, evidence richness
  - Production Readiness (15 pts): Multi-user, API, documentation
- **Classifications:** 85-100 Production Ready | 70-84 Beta | 50-69 Alpha | 30-49 Lab | <30 Pre-Product
- **Logs to:** ~/your-workspace/health-private/scoring-maturity-log.md

### Cycle 4: Builder-Product Correlation (Weekly Saturday 8PM CT)
- **Agent:** SYNTHESIS (PhD Systems Biology MIT, PhD Behavioral Econ Chicago, PhD Complex Adaptive Systems Santa Fe, ex-WHO)
- **Cron ID:** `cd5e641428d0`
- **Schedule:** 0 20 * * 6
- **Model:** google/gemini-2.5-pro
- **What it measures:**
  1. Dogfooding Integrity Score (0-100): Is the system helping its builder?
  2. Cross-layer status: Snapshots from all 4 layers in one view
  3. Flywheel direction: Virtuous / Stalled / Vicious
  4. Trust Readiness (1-10): Could a customer trust this product?
  5. ADHD Paralysis Signature detection
- **Logs to:** ~/your-workspace/health-private/builder-product-correlation-log.md

### Cycle 5: Methodology Evolution & Horizon Scan (Biweekly Wednesday 10AM CT)
- **Agent:** HORIZON (PhD Complex Systems Santa Fe, PhD Health Informatics Stanford, PhD Innovation Management MIT Sloan, ex-Rock Health CRO)
- **Cron ID:** `1628b3bed348`
- **Schedule:** 0 10 1,15 * * (1st and 15th of each month)
- **Model:** google/gemini-2.5-pro
- **What it does:**
  1. Assesses internal methodology state (activities, dimensions, matrix)
  2. Horizon scans scientific literature across 7 domains
  3. Competitive landscape analysis (WHO-5, Oura, Whoop, Noom, etc.)
  4. Framework structural analysis (right # of dimensions? right formula? right evidence system?)
  5. Opportunity identification (ranked by impact/effort/timing)
  6. Threat detection (regulatory, technical, market)
  7. Product roadmap implications
- **Key principle:** Strategic, not tactical. Asks "Is this the RIGHT approach?" not "Is the math correct?"
- **Logs to:** ~/your-workspace/health-private/methodology-evolution-log.md
- **Feeds into:** health-scoring-improvement-cycle for tactical execution of discoveries

## VERITAS Dogfooding Layer (Platform + Content QA)

### What This Is
VERITAS is Divinity Science's peer review and quality assurance platform — a multi-agent review panel system with evidence-level gates, cross-model validation, and 6-dimension scoring rubrics. Instead of only using it for external research, we USE IT ON OURSELVES.

This serves three simultaneous purposes:
1. **Quality Assurance** — Catch errors in DS content before anyone else does
2. **Product Development** — Every review session is a live test of the VERITAS product
3. **Content Excellence** — Every public document meets the standard we'd impose on others

### VERITAS Dogfood Cycle (Weekly Thursday 10AM CT)
- **Agent:** VERITAS-DOGFOOD (PhD Publishing Science Oxford, PhD Digital Product Management Stanford, ex-Nature Digital Medicine, ex-VP Product PLOS)
- **Cron ID:** `a6ae3f18aebc`
- **Schedule:** 0 10 * * 4
- **Model:** google/gemini-2.5-pro
- **What it does:**
  1. Inventories all DS content files (methodology docs, product specs, scoring docs)
  2. Selects 2-3 files for review (prioritizes recently modified and public-facing)
  3. Applies full VERITAS review pipeline:
     - Evidence Level Gate (Original Data / Literature Synthesis / Theoretical / Mixed)
     - 6-dimension scoring (Scientific Accuracy 20%, Math Rigor 15%, Methodology 15%, Clinical Relevance 15%, Ethics 15%, Communication 20%)
     - Cross-model validation for low-scoring claims
  4. Logs process friction points (UX issues with VERITAS itself)
  5. Translates findings into product features
  6. Updates cumulative review log
- **Logs to:** ~/your-workspace/health-private/veritas-dogfood-log.md
- **Session references:** `references/veritas-dogfood-*.md` — per-cycle detail (contradictions found, VERITAS product signals, friction points). See `veritas-dogfood-2026-07-06-octad-consistency-drift.md` for the cross-document consistency drift pattern that fed the `external-content-qa-pipeline` cross-doc check.

### VERITAS Infrastructure (pre-existing)
- **VERITAS Audit Panel:** 4 agents on non-Anthropic models
  - VERITAS-MATH (Gemini), VERITAS-PHYS (Gemini), VERITAS-STAT (Qwen), VERITAS-ETHICS (DeepSeek)
- **14 specialist agents** across 4 panels: 8D Core, Kink/BDSM, EF COMPASS, VERITAS Audit
- **5-stage review pipeline:** Evidence Level Gate → Research Agent → Panel Review → Regulatory → QA
- **250-agent panel capacity** (scaled up after ICBN v5 failure)
- **Review database:** review_panels + panel_reviewers tables in agents.db

## Audit Layer (Independent Verification)

Each cycle has an independent AUDIT agent running AFTER the doer on DeepSeek R1 (different model = catches Gemini-specific blind spots).

| Cycle | Doer (Gemini) | Auditor (DeepSeek R1) | Offset |
|-------|---------------|----------------------|--------|
| Algorithm Integrity | VERITAS-ALGO | AUDIT-ALGO (`8ca403ce6f36`) | +30min |
| Org 8D Health | STRATEGOS | AUDIT-ORG (`139345b251b3`) | +1hr |
| Scoring Maturity | AXIOM | AUDIT-SMI (`7a432feca269`) | +2hr |
| Builder-Product | SYNTHESIS | AUDIT-SYNTH (`a70b610f3c08`) | +2hr |
| Methodology Evolution | HORIZON | AUDIT-HORIZON (`84fd46b1773c`) | +2hr |
| VERITAS Dogfood | VERITAS-DOGFOOD | AUDIT-DOGFOOD (`3a881594a562`) | +2hr |

Auditors are READ-ONLY. They verify, dispute, and escalate — never modify or fix.

## Data Flow

```
VERITAS-ALGO (12h) → integrity results → STRATEGOS's PHY/ENV scores
STRATEGOS (8h)     → org TWC → SYNTHESIS's cross-layer analysis
AXIOM (weekly)     → SMI score → SYNTHESIS's product maturity layer
SYNTHESIS (weekly) → flywheel → informs where STRATEGOS intervenes next
HORIZON (biweekly) → strategic opportunities → feeds health-scoring-improvement-cycle
VERITAS-DOGFOOD (weekly) → content quality + process friction → VERITAS product roadmap
```

## Full Schedule (12 Cycles)

| Time | Job | Agent | Role |
|------|-----|-------|------|
| Every 8h (0,8,16) | the specialist engine 8D Improvement | STRATEGOS | Doer |
| Every 8h (1,9,17) | Org Health Audit | AUDIT-ORG | Auditor |
| Every 12h (:00) | Algorithm Integrity | VERITAS-ALGO | Doer |
| Every 12h (:30) | Algorithm Integrity Audit | AUDIT-ALGO | Auditor |
| Thu 10AM | VERITAS Dogfood QA | VERITAS-DOGFOOD | Doer |
| Thu 12PM | VERITAS Dogfood Audit | AUDIT-DOGFOOD | Auditor |
| Sat 7PM | GENESIS Sprint | AISHA | Sprint |
| Sat 8PM | Builder-Product Correlation | SYNTHESIS | Doer |
| Sat 10PM | Builder-Product Audit | AUDIT-SYNTH | Auditor |
| Sun 9AM | Scoring Maturity Index | AXIOM | Doer |
| Sun 11AM | Scoring Maturity Audit | AUDIT-SMI | Auditor |
| 1st & 15th 10AM | Methodology Evolution | HORIZON | Doer |
| 1st & 15th 12PM | Methodology Evolution Audit | AUDIT-HORIZON | Auditor |

## Audit Escalation Path

```
Doer produces report → Auditor verifies → 
  ✅ CLEAN: system healthy
  ⚠️ MINOR: logged, doer self-corrects next cycle
  ❌ MATERIAL: flagged → next doer cycle MUST address
    → If missed AGAIN → escalation compounds
```

## Model Diversity Strategy

- **Doers:** google/gemini-2.5-pro via openrouter — best reasoning depth
- **Auditors:** deepseek/deepseek-r1-0528 via openrouter — different architecture catches Gemini blind spots
- **VERITAS specialist panels:** Gemini, Qwen, DeepSeek (never single-provider)
- NO Anthropic models in cron jobs (the operator agent cannot use Claude)

## Log Files
- Algorithm integrity: ~/your-workspace/health-private/algorithm-integrity-log.md
- Algorithm baseline: ~/your-workspace/health-private/algorithm-integrity-baseline.json
- Scoring maturity: ~/your-workspace/health-private/scoring-maturity-log.md
- Builder-product: ~/your-workspace/health-private/builder-product-correlation-log.md
- Methodology evolution: ~/your-workspace/health-private/methodology-evolution-log.md
- VERITAS dogfood: ~/your-workspace/health-private/veritas-dogfood-log.md

## Pitfalls
1. STRATEGOS and the existing the specialist engine TWC Scorecard (c34176850670) overlap but differ in depth — daily is a snapshot, 8h is active improvement
2. SYNTHESIS reads personal health data — PHI, handle per health-private security rules
3. If VERITAS-ALGO detects a broken pipeline, STRATEGOS will also see degraded PHY/ENV — fix should come from VERITAS's fix agent, not duplicate
4. SMI trajectory needs 4+ weeks before meaningful — don't over-interpret early deltas
5. HORIZON's findings are STRATEGIC — they need to be translated into tactical work via health-scoring-improvement-cycle
6. VERITAS dogfood scores should NOT all be 8-9/10 — if they are, the review is too soft
7. All execute_code blocks in cron prompts must be self-contained (no imports carry over)
8. Carry-forward contamination (source='cron') must be filtered from all trend analysis
9. HORIZON search queries must be broad enough to catch disruptive approaches, not just incremental improvements
10. VERITAS dogfood logs must include per-document scores and verification details to enable honest auditing; summary-only logs prevent independent verification.

## Verification
After any change to this system, verify:
- All 12 cron jobs (6 doers + 6 auditors) are enabled and scheduled correctly
- Auditor schedules offset from doer schedules by 30min-2hr
- Auditors run on DeepSeek R1, doers on Gemini 2.5 Pro
- Log file directories exist
- No schedule conflicts with GENESIS or other existing crons
- No Anthropic models assigned (model compliance)
- Auditors have no write permissions
- VERITAS dogfood is actually reviewing new content weekly, not re-reviewing the same files