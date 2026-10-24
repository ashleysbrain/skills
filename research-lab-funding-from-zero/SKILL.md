---
name: research-lab-funding-from-zero
description: Fund a small AI research lab from zero. Grant-first plan.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [funding, strategy, research-lab, grants, investors]
---

# Research Lab Funding From Zero

The falsification-hardened playbook for getting a tiny AI-native research lab its first external money. Consolidated from the 2026-08-15 strategy session (Popper falsification round + Andreasen consolidation + Bridgman asset grading).

## When to use
- The lab has zero external funding and needs its first grant/investment
- A founder wants to sell equity in a sub-entity without touching parent ownership
- Building a funding strategy, pitch artifact, or research-hub structure

## The five hard rules (each one killed a real plan)

1. **GRANT-FIRST, NOT EQUITY-FIRST.** Named doors (ARC Prize, Schmidt Sciences, ARIA, NIH SBIR/STTR) are all NON-DILUTIVE. Equity investors for a pre-revenue hub with zero publications, zero signed advisors, ~1 FTE effectively do not exist. Optimize the entity for the instrument the first dollar actually arrives through.
2. **NO SHELL ENTITIES.** Before any structure forms: IP assignment (engines/code from founder to the entity), license boundary (parent and hub), cap table stub, data room skeleton. Every diligence path — grant or equity — dead-ends at "prove you own it."
3. **EVIDENCE BEFORE ENTITIES.** First money follows evidence artifacts: a signed advisor letter (zero cost, highest leverage — do it FIRST), a preprint/technical report of the lead asset. Letters before structure, structure before pitch.
4. **LEAD WITH THE VERIFIABLE ASSET.** Grade every asset REAL/THEORETICAL/ASPIRATIONAL (operationalism: real = a funder can run the operation themselves and reproduce your number). The REAL asset is the funding identity; the impressive-but-theoretical flagship is the DILIGENCE TRAP — present as roadmap, never headline. First diligence question is always a live demo of the flagship claim; if it fails, every adjacent claim regrades downward.
5. **FIREWALL THE TWO NARRATIVES.** Funding docs and public essays can carry different emphases, but omission becomes concealment when an investor reads both: the funding memo needs a one-line acknowledgment of the public vision (roadmap framing). Certainty claims ("the market will REQUIRE X") fail evidence gates — grade every forward claim (probability + timeline + what would change my mind).

## Sequencing (the dependency chain)
1. Advisor engagement letters (the willing expert, moved to signed)
2. Grant mechanics with lead time (SAM.gov registration takes weeks — start immediately)
3. IP conveyance + data room
4. Structure decision via the instrument gate: fiscal sponsorship (grant-first, fastest, 5-10% overhead) vs subsidiary/standalone LLC (equity track) — SPV is an investment vehicle, not a lab; category error
5. Economics/runway model
6. Pitch artifact (only after 1-5)
7. Standing falsification: the plan goes through minimum 2 adversarial rounds by different brains before anyone with money sees it

## Verified asset-grading pattern (Bridgman, 2026-08-15)
| Asset type | Grade | Door |
|---|---|---|
| Physics-informed scoring engine (funder-runnable, reproducible number) | REAL | ARC-adjacent + ARIA |
| Fleet + QA gates (live crontab, watchdogs, journals) | REAL | Schmidt agents |
| Writing pipeline with enforced gates | REAL | credibility layer |
| Scoring code without external validation cohort | REAL-code/THEORETICAL-instrument | NIH-style once cohort exists |
| Products with zero external users | THEORETICAL commercially | validation-dependent |
| Impressive partially-built runtime | THEORETICAL = trap | roadmap only |

## People verification (before strategy depends on them)
Verify named experts via Crossref (`api.crossref.org/works?query.author=<Surname>`) and arXiv before treating them as assets. Record verified publications in the strategy doc. "Willing" is not "recruited" until a letter is signed.

## Pitfalls
- Building investor-grade structure for grant money (instrument inversion)
- Forming the entity before the IP conveyance exists (shell)
- Scheduling prose and structure while no microtask produces proof
- Parallel projects when serial is faster to first money (context-switching tax on a solo founder)
- Publishing certainty claims that the lab's own evidence gates would reject

## References
- `references/2026-08-15-falsification-verdict.md` — Popper's full dual-track kill verdict with the rebuilt microtask sequence
