---
name: federal-grant-application-production
description: Use when producing NIH SBIR or NSF grant applications.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [grants, sbir, nih, nsf, funding, non-dilutive, grant-writing]
---

# Federal Grant Application Production

Class-level workflow for converting a company's locked strategic verdicts and technical architecture into federal grant application packages (NIH SBIR/STTR Phase I, NSF Seed Fund / America's Seed Fund, and similar non-dilutive instruments).

## When to Use

Use when the task involves: NIH SBIR/STTR applications, NSF SBIR/STTR Project Pitches or full proposals, specific aims drafting, institute/center targeting, non-dilutive vs. dilutive sequencing, Phase I budgets, or investor-facing explanations of a grants-only first raise.

## Inputs (gather before drafting)

1. **Locked verdicts / decision memo** — instrument ranking, vehicle choice (SBIR vs STTR vs NSF), budget ceiling, dilution stance, credibility-asset ranking. These are the constitution; the application serves them, never the reverse.
2. **Technical architecture doc** — the physics/engineering core that becomes the Innovation section. For DS: the 6+1 physics engines (COG/PIPE/RES/KNOW/ALIGN/ADAPT/INTER) with Fisher-Rao unification, Bloch-sphere composite, participation-ratio dimensionality.
3. **Live source pack on the programs themselves** — fetched program pages (sbir.gov, seedfund.nsf.gov, sbir.nih.gov). Program caps and rules change; cite the fetched date. Phase I cap as of the 2026-04 policy update: **$323,090** (verified 2026-08-15 fetch).

## Phase I NIH SBIR skeleton (proven structure)

Per-deliverable section map — each with its content source:

| Section | Content source |
|---|---|
| Project title (3 candidates) | Locked instrument name + physics claim; title must name the deliverable, not the science |
| Specific Aims (3, each with month ranges) | Architecture doc aims: parameterization → prospective validation → composite-score validation |
| Significance | Gap statement from architecture doc: every existing instrument returns static scalar snapshots; none measure trajectory/predict degradation |
| Innovation | The physics core verbatim from architecture: named frameworks per engine, unification metric, why each named framework (JS distance not KL, geometric mean not arithmetic) |
| Approach | Aims as milestones + GO/NO-GO gates at engine-lock and cohort-enrollment thresholds; shadow-scoring sandbox with 30-day promotion rule as de-risking |
| Human subjects | Minimal-risk observational cohort; IRB through the academic partner institution (not the company) |
| Researchers | PD/PI = principal/architect; key personnel = named academic bench (physics reviewer + biomedical-informatics advisor); subaward = sister lab for pipeline hardening + cohort data security |

**Rules:** funding request at the cap, not below. Bench names open doors — the biomedical-informatics advisor at a Harvard affiliate is the NIH door. Institute choice is a cohort-recruitment choice, not a science choice.

## Institute targeting logic (NIH, 24 institutes fund SBIR)

- **NIBIB** — default primary for any measurement/quantitative instrument: bioengineering instrumentation is its mandate, and named physics reads native there.
- **NIMH** — measurement-based care priorities; strong when ALIGN/ADAPT-style behavioral trajectory dims are salient.
- **NINDS** — credible if the cohort oversamples neurodegenerative decline; critical-slowing-down is literally tipping-point detection.
- **NIDA** — viable for trajectory-based relapse-precursor monitoring.
- Pattern: when the science is disease-agnostic, target the institute whose *recruitment population* matches the cohort you can actually enroll.

## NSF Seed Fund skeleton (two-gate)

**Gate 1 — Project Pitch** (three parts): (a) innovation — the engines as universal state estimators; (b) market — measurement/certification layer; (c) societal impact — earlier decline detection. **Gate 2 — Full Proposal** tech paragraph structure: fundamental-science basis (one engine, one physics, one equation) → delta on state of the art → technical objectives = cohort validation milestones → commercialization (API, certification, private instances). Frame the work as **deep tech: fundamental-science-based and internally validated, not exploratory**. NSF takes zero equity; up to $2M across phases.

## THE COHORT AS FEDERAL ASSET (the converting milestone)

One validation cohort, cited in BOTH applications, serving three functions: NIH feasibility data (Phase II competitiveness), NSF technical-risk reduction, and the company's #1 credibility asset — peer-reviewed validation with an academic partner. Design rules: **design once, cite twice** — pre-register, power for the primary endpoint, lock the analysis plan before enrollment. In both applications the cohort is THE milestone converting *theoretical → in-validation*: engines and instrument exist; the human cohort is what remains.

## The principal's 3-sentence investor answer (grants-only raise)

Template derived from the locked-facts version (structure, not verbatim):

1. What exists and is validated now (internally validated engines + instrument entering human validation with an academic partner this cycle).
2. The raise structure (grants-only first raise; named federal amounts; non-dilutive) — federal reviewers validate the science before anyone prices the equity.
3. The post-cohort position (the only validated physics-based instrument of its kind; that peer-reviewed result is the asset an investor gets before anyone else can).

## Pitfalls

- **Stale dispatch paths.** A parent-provided source path may not exist (see `tool-output-verification-discipline` item 18). Search by filename substring across the workspace root; verify via `os.walk` before reporting "not found."
- **Inventing program numbers.** Phase I/II caps and solicitation windows are fetched-live facts, not memory facts. If the source pack is missing, fetch sbir.gov/about before quoting any cap.
- **One cohort, many claims.** If both applications (and any academic paper) rest on the same cohort, the pre-registration and analysis lock must exist BEFORE either application is submitted — reviewers see overlap and non-pre-registered analyses taint both.
- **Do not oversell the conditional dimension.** The 7th engine is conditional; applications should present 6 core + 1 conditional, not 7 co-equal aims.

## Support files

- `references/nih-sbir-phase1-8d360-skeleton-2026-08-15.md` — full worked example: title candidates, 3 aims with month ranges, institute rationale, NSF pitch, cohort framing, and the 3-sentence investor answer, produced from locked verdicts + AI-Health-Benchmark architecture v3.0.0.
