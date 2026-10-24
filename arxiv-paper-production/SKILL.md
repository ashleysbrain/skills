---
name: arxiv-paper-production
description: Class-level workflow for producing, verifying, and submitting compliant arXiv source packages.
tags: [arxiv, latex, verification, packaging, academic-submission]
---

# ArXiv Paper Production

**Goal:** Produce rigorous, compliant arXiv source packages that compile cleanly and meet platform constraints.

## Core Workflow

### 1. Drafting
- Standard LaTeX with `microtype`, `natbib`, `booktabs`
- Clear abstract (align with any dual-submission venue limits)
- Structure: Introduction, Related Work, Methodology, Results, Discussion

### 2. Local Verification
**Tool:** Use `tectonic` (portable, handles dependencies automatically)

```bash
tectonic -X compile main.tex --keep-logs
```

**Verification Checklist:**
- [ ] Compilation succeeds (no fatal errors)
- [ ] No missing (`undefined`) or unused citations
- [ ] AI-tell scan passes: `scan_ai_tells.py main.tex` → 0 telltales
- [ ] Figure PDFs render correctly (labels, legends)
- [ ] Page/word counts match expectations

### 3. Packaging for arXiv
arXiv will regenerate the PDF from source.

**Include in `arxiv-source.zip`:**
- `main.tex` (manuscript)
- `references.bib` (bibliography)
- `main.bbl` (precompiled bib for portability)
- `figures/*.pdf` (vector figures preferred)
- `ancillary/*` (data, scripts for reproducibility; optional)

**Exclude:**
- `main.pdf` (arXiv regenerates)
- `.aux`, `.log`, `.out`, `.fls`, `.blg` (intermediates)
- `.pyc`, `__pycache__`

**Command:**
```bash
zip -q arxiv-source.zip main.tex references.bib main.bbl figures/*.pdf ancillary/*.{py,json}
```

### 4. Pre-Submission VERITAS Review (for field-defining work)
For papers that claim to introduce a field, novel paradigm, or significant framework, run a three-part VERITAS hostile review before final packaging:

**Dispatch three parallel subagents:**
1. **Scientific novelty review** — Check prior art, overclaims, omitted closest work, citation quality
2. **Methods/statistics review** — Audit experimental design, controls, statistics, causal language, reproducibility
3. **arXiv moderation review** — Verify topicality, refereeability, category fit, moderation risks

**Integration pattern:**
- Address all MUST-FIX items before final compilation
- Apply executable fixes (add citations, clarify language, expand abbreviations)
- Note NON-BLOCKING items as future work in limitations section
- Re-compile and regenerate ZIP after all fixes applied

**Common MUST-FIX patterns to watch for:**
- **Abbreviations not expanded** (e.g., "the operator agent" → "For brevity in this manuscript, the system is referred to as the operator agent")
- **Control degeneracy not disclosed** (if random control baseline is degraded, state explicitly why)
- **Reproducibility statements overstating usability** (clarify if scripts require private modules)
- **Proxy values lacking denominators** (add "N of M" context for interpretability)
- **Closest prior art under-engaged** (cite explicitly and specify concrete differences)
- **Foundational citations missing** (e.g., Albert 2000 for network robustness, Rosen 1991 for relational biology)

**DO NOT:**
- Run VERITAS for routine incremental papers (wastes time)
- Ask user permission to apply VERITAS fixes (task execution discipline)
- Delay packaging while VERITAS runs (they run in background; continue other work)

### 4b. Section-Level Hostile Review (Five-Dimension Framework)
When the user asks for a hostile review of SPECIFIC revised sections (not the whole paper), use this structured framework instead of dispatching three full-paper subagents. Read the manuscript source (.tex) and .bib directly, then score each dimension independently:

**The five dimensions:**
1. **Substantive prose** — Does the section contain genuine argumentation, or is it a stub/table with no prose? Every numbered subsection must have at least one paragraph stating the distinction it establishes.
2. **Scientific discipline of terms** — Does each biological term (genotype, phenotype, development, epigenetics, reproduction, offspring, evolution) have an operational computational referent with a measurable criterion? No metaphor without a falsifiable test.
3. **Metaphor abuse avoidance** — Does every definition include an anti-metaphor clause stating what the term does NOT mean in this context?
4. **Citation appropriateness** — Are cited references real, accurately representing the claims, and standard for the field? Are there sections with zero citations that need back-references?
5. **Overreach vs existing literature** — Does the manuscript claim novelty or capability that overreaches existing artificial embryogeny (AE) or digital evolution (DE) work? Does it acknowledge what AE/DE already implements?

**Scoring rules:**
- Score each dimension 0-10 independently with a one-paragraph justification.
- The PASS threshold is 8.5/10 weighted average AND no individual dimension below 8.0.
- Return exact must-fix text for any MEDIUM or higher issue. Minor items are noted but non-blocking.
- Use sequential thinking to work through each dimension systematically before committing the score.
- Output format: dimension table (5 rows with scores and findings), must-fix items with exact text and severity, minor polish items, final score, and PASS/FAIL verdict.

**Session evidence (2026-07-11):** Five-dimension review of revised Sections 3.2-3.3 scored 8.7/10. Identified one MEDIUM must-fix (AE developmental encodings already implement stage-dependent expression; manuscript must acknowledge this) and three MINOR items. All dimensions passed.

### 5. Submission
- **Category:** `cs.AI` for architecture/theory; verify fit against `cs.MA`, `cs.NE`
- **Metadata:** Copy title/abstract from `.tex` (strip LaTeX commands)
- **License:** `CC BY 4.0` (max reuse) or arXiv default (conservative)
- **Endorsement:** Complete if requested; distinct from peer review

## Critical Pitfalls

### Micro-Task Execution Discipline
When upgrading pipeline code, NEVER delegate large multi-fix batches to subagents. Subagents writing 2000+ lines of code consistently time out after 600s. Instead: apply fixes one by one in the main session, running `py_compile` after each patch. This was learned from repeated subagent timeouts during VERITAS/CRUCIBLE elite gate mirroring.

### Engine Routing Audit Pattern
When auditing a pipeline that calls specialist engines via `engine_post()`, verify:
1. Every engine in the ENGINES dict is actually called (defined but never called = dead weight)
2. No `engine_post()` call references an engine NOT in the dict (typo or hallucinated engine name)
3. Panel seats use engines whose biological role matches the seat function (e.g., Popper for falsifiability, not Gazzaniga's interpreter module)
4. Both pipelines have engine name parity (same 14 engines, different port blocks)
Run this as a Python script using `re.findall` on the source, not manual inspection.

### Whitespace-Only Lines Cause IndentationError
Python files edited with `patch` can accumulate lines containing only spaces (not empty strings). These cause `IndentationError: unindent does not match any outer indentation level`. Fix by normalizing: replace any line where `line.strip() == ''` with empty string. Run `py_compile` after every patch to catch this early.

### Cross-Disciplinary Term Sweep
When introducing novel terminology, you must acknowledge ALL prior uses of the word, even outside your discipline.

- **Wrong:** Only citing ML/AI uses of "physiomorphic"
- **Right:** Searching psychology, biology, medical domains (e.g., Richards 1989, Manimaran 2024) and citing them explicitly
- **Why:** Hostile reviewers will find uses outside your domain. Failing to cite them looks like ignorance or suppression

### Source Exclusion
Uploading `main.pdf` or log files can cause arXiv build failures. Verify ZIP contents.

### Table Overflows
arXiv's TeX Live differs from Tectonic. Avoid overflows:
- Use `booktabs` + `array` package
- Fixed column widths: `\newcolumntype{P}[1]{>{\raggedright\arraybackslash}p{#1}}`
- Reduce font size (`\footnotesize`) before reducing margin

### Table and Section Integrity
A table does not substitute for prose. Every numbered subsection must contain at least one paragraph that states:
- what distinction the subsection establishes,
- how the table/figure supports that distinction,
- what inference the reader should and should not draw.

After compilation, inspect the table of contents or extracted page text for headings followed immediately by floats or page breaks. A visually populated page can still be semantically empty.

### User Review Artifact Discipline
When the user asks to review "all pages":
- Deliver the compiled multi-page PDF as one document by default.
- Do not paste the manuscript into chat unless explicitly requested.
- Do not substitute separate PNG page files when the user asked for one document.
- If the user explicitly requests a single PNG, stitch all rendered pages vertically into one scrollable PNG and verify its dimensions before delivery.
- Regenerate review artifacts after every manuscript revision; never show stale page renders.

### Biological Lifecycle Terminology
For papers discussing DNA, inheritance, development, reproduction, offspring, or evolution in artificial systems, keep architecture and lifecycle orthogonal. Physiomorphic architecture does not require reproduction, and digital reproduction does not imply organism-level mapping.

Use operational terms:
- **digital genotype:** versioned heritable generative specification;
- **phenotype:** instantiated architecture and observable behavior in a stated environment;
- **development:** stage-dependent genotype-to-phenotype expression with measurable commitment or differentiation;
- **epigenetic state:** persistent expression control without changing the genotype;
- **offspring:** independently addressable derived system with inherited specification, distinct state, lineage, and capacity for divergence;
- **evolution:** population-level heritable variation plus differential retention across generations.

Ordinary source code is not automatically DNA, configuration is not automatically epigenetic, a deployment sequence is not automatically development, a generated product is not automatically offspring, and update distribution is not evolution. See `references/artificial-lifecycle-claims.md` for the full claim gate and literature anchors.

**AE prior art acknowledgment requirement:** When defining "development" with criteria like "measurable stage-dependent expression, commitment, or differentiation," the manuscript MUST acknowledge that artificial embryogeny (Stanley & Miikkulainen 2003 and successors) already implements stage-dependent gene expression in developmental encodings (CPPN-NEAT etc.). Physiomorphic AI's contribution is the additional requirement that developmental stages map to organism-level organizational constraints, not the concept of staged expression itself. Omitting this acknowledgment risks implying originality for developmental computation, which would be overreach.

### Biological Isomorphism Terminology
When using "biological isomorphism" as a graded architectural correspondence score, add a footnote or paragraph clarifying this is NOT strict mathematical graph isomorphism (binary, requires bijection). Future work may determine "biological homomorphism" is more accurate. This prevents overclaim and mathematical criticism.

### Engage Closest Prior Art Explicitly
For architecture frameworks that reference organism-level organization, you MUST engage Arbib's schema theory directly. Arbib's work on mapping functional schemas to brain regions as "dynamic systems for perception, action and cognition" within a "systems of systems" integration framework is the closest prior art. Distinguish your formulation by:
- Requiring explicit organism-level anatomical reference beyond neural structures
- Separating component, functional, relational, and organizational correspondence
- Committing to matched-control falsifiability rather than comparative model evaluation alone

Failing to engage Arbib appears as ignorance or suppression of the most relevant precedent. Acknowledge it and specify the concrete differences.

## Strategy

### Announcement Sequence
For high-stakes field introductions:
1. **arXiv Live** — establishes public, citable, timestamped priority
2. **LinkedIn** — same-day announcement linking to arXiv paper
3. **Wikipedia** — do not rush; requires independent secondary sources and strict COI policies

### Novelty Language
- arXiv establishes priority, NOT peer validation
- Use "proposed as a research program," not "validated field"
- Explicitly state limitations of preliminary results

### Score Threshold Discipline
**RULE:** A field-defining paper may be presented as a working draft, but it MUST NOT be labeled ready, packaged as final, or passed to the user as a completed deliverable when any hostile VERITAS dimension is below **8.5/10** or carries `REVISE`/`REJECT`. The weakest dimension controls the gate; averaging scores is forbidden.

Required sequence:
1. Identify every MUST-FIX item.
2. Apply all executable fixes without asking permission.
3. Recompile and rerun mechanical verification.
4. Run a new hostile review on the revised manuscript. Applying fixes does not itself convert a failed review into a pass.
5. Deliver as final only when every required review is `PASS` and scores at least 8.5/10.

If the user asks for an interim artifact, mark it visibly as `WORKING DRAFT — FAILED QUALITY GATE` and state the unresolved blocker before the file link.

**Why:** A 5/10 scientific-novelty score indicates that the work still under-engages prior art or lacks evidentiary value. Reporting the score alongside a supposedly final package does not cure the failure. The user expects the specialist to absorb the review, repair the work, and withhold the final-delivery claim until re-review passes.

**This session's evidence:**
- VERITAS scientific-novelty review scored 5/10 with REVISE verdict
- User feedback: "this should never be only 5/10 to pass to me... this should not have made it to me"
- Corrective action: Applied all executable fixes, addressed MF1 (Arbib), MF3 (Albert 2000), MF5 (bibliography), recompiled, delivered updated package

**Pattern to avoid:**
- Running VERITAS reviews then reporting scores neutrally
- Presenting REVISE/REJECT verdicts as "information only"
- Asking user "should I fix these?" for clearly missing prior art or control disclosures

**Correct pattern:**
- For field-defining work: Dispatch VERITAS → Integrate fixes silently → Re-verify → Deliver fixed product
- For routine work: Skip VERITAS; standard compile + scan suffices

## Pipeline Integration (VERITAS 16-Stage Pipeline)

Both research pipelines now produce arXiv-ready output through the elite quality gate system. The five-dimension hostile review framework described above is wired into Stage 7 of both pipelines as `five_dimension_review()`, with weakest-controls-gate scoring (threshold 8.0 weakest + 8.5 average).

### Domain Auto-Detection (added 2026-08-12)
The pipeline now detects the academic field from the seed idea using a 26-field keyword map (multi-word phrase priority) before brainstorming. This ensures the LLM uses the right researcher persona. Fields include: distributed-systems, psychiatry, neuroscience, cancer-biology, genetics, musicology, classical-history, geology, ecology, climate-science, economics, psychology, philosophy, law, linguistics, chemistry, physics, biology, education-research, sociology, machine-learning, public-health, supply-chain-logistics, art-history, medieval-history, and LLM fallback for unknown fields.

### Voice Injection (added 2026-08-12)
ASHLEY_VOICE profile (tone, 30+ banned phrases, em-dash prohibition, sentence variety directive) is injected into all 3 progressive draft passes (knowledge-telling, knowledge-transforming, knowledge-crafting). Prose is voice-compliant from the FIRST draft, not stripped post-hoc.

### Fact Checker Domain Awareness (added 2026-08-12)
The fact checker now distinguishes:
- **Empirical claims** ("found that", "p <", "data show") — always need citation
- **Analytical claims** ("proves", "demonstrates") — need citation ONLY if they reference external work
- **Primary-source observations** about the paper's own subject — NOT flagged as unsourced
Also recognizes author-name citations ("McGahie's comparison confirms...") not just [N] markers.

### Revision Loop (added 2026-08-12)
Stage 6 revision now uses direct LLM calls (httpx + Z.ai API) instead of the degraded Wernicke engine. Includes voice directive and citation preservation instructions.

### Quality Gate Status Surfacing (added 2026-08-12)
Stage 7 computes a quality_gate verdict (PASS vs QUALITY_ISSUES) based on fact_check unsourced ratio, 5-dimension score, panel verdict, and citation count. Status flows to API as "completed" vs "complete_with_quality_issues" with specific warnings.

### Quality Gates Wired Into Pipeline Stage 7
- `generate_latex_document()` + `package_arxiv_source()` + `compile_latex_check()` produce the arXiv package automatically
- `generate_completeness_statements()` produces reproducibility, data availability, author contributions, competing interests, ethics, acknowledgments
- `cross_disciplinary_term_sweep()` flags terms with prior uses outside target domain (the same check described in the Cross-Disciplinary Term Sweep pitfall above)
- `prior_art_engagement_check()` verifies Arbib, Stanley, Tononi, Friston etc. are cited (VERITAS) or Shamir, NIST, BeyondCorp etc. (CRUCIBLE)
- `metaphor_abuse_check()` flags metaphors without operational definitions
- `validate_venue_compliance()` checks abstract word count and page limits per venue
- `fact_check_pass()` ensures every factual claim has a citation marker
- `citation_completeness_audit()` checks DOI/year/author completeness, foundational vs recent mix
- `run_all_citation_quality_checks()` runs self-citation rate, recency distribution, diversity, predatory journal detection, retraction check
- `generate_cover_letter()`, `generate_reviewer_response_template()`, `generate_supplementary_materials()` produce pre-submission materials

### Voice Fidelity and User Fine-Tuning
Both pipelines track voice fidelity per run and maintain persistent user profiles. See `dual-process-research-pipeline` skill for the full architecture. The arXiv paper production workflow is now a STAGE of the pipeline, not a separate manual process.

## References

Session-tested workflows from Physiomorphic AI paper production (2026-07-10). Elite pipeline integration added 2026-08-06.

### Writing Science Literature Base (2026-08-10)

The pipeline redesign is grounded in 14 verified papers from cognitive
science, AI-assisted writing, argumentation theory, and peer review. See
`references/writing-science-literature-base.md` for the full base with
citation counts, DOIs, and key findings. See
`references/writing-pipeline-architecture.md` for the 11-stage architecture
spec (progressive drafting, multi-pass revision, audience simulation,
anti-homogenization).

**Key principle from literature:** Single-shot LLM drafting reproduces the
novice "knowledge-telling" pattern (Kellogg 2008). Expert writing is recursive
(Flower & Hayes 1981) and requires pre-writing synthesis (Booth 1995),
progressive drafting (3 passes: telling → transforming → crafting), and
multi-pass revision at discourse level before sentence level (Sommers 1980).