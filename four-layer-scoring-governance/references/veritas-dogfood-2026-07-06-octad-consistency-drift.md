# VERITAS Dogfood Session — 2026-07-06 — OCTAD Cross-Doc Consistency Drift

**Cycle:** VERITAS Dogfood (weekly)
**Reviewer:** VERITAS-DOGFOOD
**Docs reviewed:** OCTAD-principal-BUSINESS-PLAN.md (4.3/10 REJECT-for-external), OCTAD-COMPANY-PROFILE.md (5.6/10 REVISE), open-source-showcase-research-2026-07-06.md (8.0/10 ACCEPT)

## The core finding

The OCTAD subsidiary ships as a family of independently-edited documents (principal plan, company profile, product roadmap). With no single source of truth, core specs and financial figures drifted apart across the docs. A customer or investor reading any two together would spot the contradictions immediately. This is a recurring class of error the VERITAS product should be built to catch.

## Contradictions found (cross-doc)

| Metric | principal Business Plan | Company Profile | Verdict |
|---|---|---|---|
| Category count | "10-category scoring system" (exec summary) | "8 rigorous categories" | Core spec disagrees |
| Reviewer count | "30-50 reviewers" (exec) vs "250 reviewers" (competitive moat, Phase 1) | "30-50 specialized reviewers" | Capability inflation in sales-facing copy |
| Year 1 revenue | Exec=$52K; Conservative table=$35K; Target table=$60K | $52K | Three sources, three numbers |
| Margin % | "58-63%" exec; "60/64/65%" detail table | "62/58/63%" | Three different sets |
| Breakeven Y3 volume | 14,000 papers stated | — | Arithmetically wrong: $280K fixed / ~$79 contribution = 3,544 papers (~4x error) |

## Legally/reputationally risky claims

1. **"90%+ acceptance rate" KPI** (principal plan) — a pre-submission review service cannot guarantee journal acceptance. Reframe to a metric we control: "review score >=9.0 achieved for X% of submissions."
2. **AI-detection "humanization guarantee"** — "money-back if flagged" implicitly sells detection evasion. Scope to "flagged erroneously."
3. **Fabricated market share** — "Journal peer review 90%+ market share" has no source. Fabricate-or-cite rule.

## Minor finding (W3 privacy spec, scored 8.0/10)

- Anonymeter GitHub link `statCel/Anonymeter` returns **404 (confirmed via curl)**. Broken citation in an otherwise publication-grade spec.
- Section 11's QI refinement (artifact's own dimension as quasi-identifier) not backported into section 4.1's QI list.

## VERITAS product signals (dogfood friction -> platform features)

These are the friction points VERITAS-DOGFOOD hit while reviewing. Each maps to a feature the VERITAS product should offer customers:

1. **Manual cross-doc consistency checking** -> Product feature: **automated cross-reference checker**. Reviewer had to open 4 large files and compare every numeric claim by hand. A platform feature that ingests a doc family and flags contradictions would catch all 5 issues in seconds.
2. **No version-control visibility** on which doc was edited when -> Product feature: **version diff highlighting** so the reviewer sees what changed since last review.
3. **No canonical-spec enforcement** -> Product feature: **canonical-spec registry**. Any doc referencing product specs (category count, pricing, reviewer count) must cite a versioned source-of-truth doc; platform flags docs that hardcode figures instead of importing by reference.
4. **Strong-tier/weak-tier gap is itself the finding** — DS produces excellent technical specs (W3 privacy = 8.0/10) but lets business/marketing docs drift (OCTAD = 4.3-5.6/10). The VERITAS product should offer a **doc-family QA tier** applying stricter consistency checks to business docs than to internal research specs.

## Process friction (VERITAS-as-product)

- (friction) Cross-document consistency required reading 4 files manually — no automated internal-contradiction detector exists in the VERITAS pipeline.
- (friction) No version-control visibility — could not determine if docs were edited independently or by different agents.
- (smooth) The W3 privacy spec demonstrates that when DS writes technical architecture docs, the quality is publication-grade. Marketing highlight: "our research specs are this rigorous."

## Content health

- Total DS content files: 1,000+
- Reviewed to date (cumulative): 7
- Average quality this cycle: 6.0/10
- Docs needing revision: 2 of 3 (both OCTAD business docs)

## Next queue

1. OCTAD-ACADEMIC-Mission.md (cross-check against principal plan for more drift)
2. SCORING-METHODOLOGY-UNIVERSAL.md (core methodology — highest-value target)
3. intel/products/FINAL-PRODUCT-LAUNCH-STATUS.md (claims verification)

## Cross-reference

The reusable QA technique (cross-document figure/spec consistency check) was encoded into the `external-content-qa-pipeline` skill (v1.1) as a mandatory check dimension + pitfall #11. This reference file captures the session-specific detail and the VERITAS product roadmap signals.
