# Competitive Landscape Gaps (Round 3)

## Methodology

Researched 25+ real tools across 7 categories. For each tool: what it does, key
innovation, what it gets RIGHT, what it gets WRONG. Verified against primary
sources (OpenAlex, Crossref, arXiv, OSF, live product pages).

## Tools Studied

- **AI-Native Academic Writing:** Elicit (138M+ papers, 95% recall), Consensus,
  Scite (Smart Citations), SciSpace, Jenni AI (source-grounded writing),
  Writefull, Paperpal
- **Research Automation:** Covidence (#1 systematic review tool, Cochrane
  standard), Rayyan (AI screening), DistillerSR, Nested Knowledge
- **Collaborative Writing:** Overleaf (25M+ users, LaTeX standard), Authorea,
  Curvenote (Scientific CMS — modular components)
- **Literature Mapping:** Connected Papers (co-citation graphs), Litmaps
  (temporal maps), Inciteful, Research Rabbit
- **AI Research Agents:** Stanford STORM (arXiv:2402.14207, 30.9K GitHub stars),
  Co-STORM (EMNLP 2024), GPT-Researcher (28.9K stars, 8-agent architecture)
- **Reference Management:** Zotero (open source), Obsidian (networked thought),
  Roam Research, Logseq

## What We Already Do Better Than Every Tool

| Capability | Our Advantage |
|---|---|
| Toulmin argumentation | No tool structures arguments |
| Progressive drafting (Kellogg) | Multi-pass with cognitive science grounding |
| Leveled revision (Sommers) | Structured 3-level vs flat editing |
| Anti-homogenization (Doshi-Hauser) | No tool addresses AI convergence |
| Cognitive checkpoint (Bastani) | No tool verifies human knowledge construction |

## The 12 Gaps (3 CRITICAL, 7 MODERATE, 2 MINOR)

### C1: No Figure or Table Generation — CRITICAL
**Market:** Rougier et al. 2014 (102 cites), Weissgerber et al. 2015 (588 cites).
Curvenote embeds live computational figures.
**Fix:** Stage 6.5 Figure Generation. For each quantitative claim: generate
figure spec (Weissgerber "show raw data" + Rougier quality rules), execute via
matplotlib/Plotly, store figure+data+code as bound triple. Figure QA gate
(axes, colorblind-safe, no dual-axis, raw data shown).

### C2: No Computational Reproducibility — CRITICAL
**Market:** Curvenote modular SCMS, Jupyter (Kluyver 2016, 524 cites), Sandve
et al. 2013 (674 cites), Open Science Collaboration 2015 (5,454 cites).
**Fix:** Stage 6.5 Computational Artifact Bind. Every quantitative claim bound
to executable cell (notebook hash + dataset DOI + commit SHA). Stage 10 emits
computational appendix. Gate fails if cited number lacks provenance binding.

### C3: No Real Venue Peer Review Rubrics — CRITICAL
**Market:** RubricReviewer (arXiv 2608.00005), Nature reporting summary,
NeurIPS reproducibility checklist, ICML/NeurIPS soundness/significance grid.
**Fix:** Stage 5.1 Venue Rubric Overlay. Per-venue criteria grid applied as
deterministic pass over persona-panel findings. Selected at Stage 1 (adaptive
depth).

### C4: No Supplementary Materials — MODERATE
**Market:** Nature/Cell require SI. PLOS requires data availability. FAIR
guidelines (Wilkinson 2016, 14,670 cites).
**Fix:** Extend Stage 10 into Multi-Artifact Package Assembly (main text + SI +
code repo with DOI + data deposit + cover letter).

### C5: No Post-Submission Lifecycle — MODERATE
**Fix:** Stage 11 with REVISION (ingest reviewer comments, map to revision
findings, re-run stages), MONITORING (citation tracking), CORRECTION.

### C6: No Smart Citations — MODERATE
**Market:** Scite classifies citations as supporting/contrasting/mentioning.
**Fix:** Extend citation graph to classify citation context between gathered
papers. High contrasting-citation ratio = controversial evidence flag.

### C7: No Multi-Perspective Research — MODERATE
**Market:** Stanford STORM uses multi-perspective question asking.
**Fix:** Stage 2.1 Multi-Perspective Search Expansion. Generate 3-5 researcher
personas, run targeted searches from each vocabulary.

### C8: No Versioning / Revision Tracking — MODERATE
**Fix:** `paper_version` field. Structural diff between versions. Response-to-
reviewers document auto-mapping each comment to revised passage.

### C9: No External Write Integrations — MODERATE
**Fix:** Stage 10.5 Submission Connector Layer (Crossref DOI deposit, Zenodo
data+code deposit, ORCID work-add, bioRxiv metadata). arXiv = manual-assist
(no public auto-submit API — verified).

### C10: No Open Science Compliance — MODERATE
**Fix:** Stage 10 Open-Science Compliance Gate (FAIR datasets with DOI+license,
ORCID for all authors, CC-BY license, DOI'd code repo, TOP self-assessment).
HARD FAIL if funder-mandated items missing.

### C11: No Pre-Registration Support — MINOR (conditional)
**Fix:** Optional Stage 0.5 Pre-Registration (freeze analysis plan to OSF,
mark confirmatory vs exploratory claims).

### C12: No Multi-Lingual Support — MINOR (low priority)
**Fix:** Optional Stage 10b Translation Pass with target-language audience sim
and Bastani checkpoint in target language.

## Verified Papers Found During This Audit

- Wilkinson et al. 2016 FAIR (14,670 cites — most cited in entire analysis)
- Nosek et al. 2018 Preregistration Revolution (1,437 cites)
- Open Science Collaboration 2015 (5,454 cites)
- Sandve et al. 2013 Reproducible Research (674 cites)
- Kluyver et al. 2016 Jupyter (524 cites)
- Rougier et al. 2014 Better Figures (102 cites)
- Weissgerber et al. 2015 Beyond Bar Graphs (588 cites)
- STORM arXiv:2402.14207 (NAACL 2024, 30.9K GitHub stars)
- RubricReviewer arXiv:2608.00005
