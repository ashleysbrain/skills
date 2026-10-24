# Research Hub Extraction Pipeline — Gap Analysis

Session: 2026-08-11. Comprehensive inventory of what the academic paper
extraction pipeline is missing, discovered through iterative review with
the user. 25 gaps total, prioritized by severity.

## Pipeline Architecture

The pipeline at `/<workspace>` consists of:
- GROBID (Docker :port) for PDF to TEI XML structural parsing
- Passage extraction (41+ structured passages per paper)
- Constrained LLM extraction via Instructor + LLM (Pydantic schema enforcement)
- String-match quote verification (anti-hallucination gate)
- NLI semantic verification via DeBERTa-v3-large (replaces keyword overlap)
- Deterministic modality classification (TCM/Ayurveda/Kampo lookup tables)
- Golden set benchmark framework (precision, recall, hallucination rate)
- Metadata enrichment via Crossref, Semantic Scholar, OpenAlex, Unpaywall, PubMed

## Gap Inventory

### Input Layer
1. **Paywall strategy** (CRITICAL) — Most medical papers are not OA. Abstract-only
   mode + PDF upload + Unpaywall OA lookup needed. Without this, pipeline only
   works on OA papers.
2. **PDF parsing quality** (CRITICAL, SOLVED) — PyMuPDF produces garbage on academic
   PDFs (0 tables, 0 figures, 0 reference sections). GROBID solves this.
3. **Non-English papers** (HIGH for holistic/medical) — TCM, Ayurvedic, Kampo
   research published in Chinese, Japanese, Korean. Need translation or
   multilingual models.

### Extraction Layer
4. **Quantitative data extraction** (HIGH) — Effect sizes, p-values, CIs, sample
   sizes must be extracted as structured fields, not lost in prose.
5. **Methodology extraction for evidence tier** (HIGH) — PICO extraction from
   Methods section drives evidence classification. Separate from finding extraction.
6. **Table data extraction** (HIGH) — Many medical findings reported only in tables.
   GROBID extracts table structure but cells need a separate extraction pass.
7. **Negative/null result extraction** (MEDIUM) — Models biased toward positive claims.
   Must explicitly extract null findings to prevent publication bias.
8. **Cross-passage findings** (MEDIUM) — Findings requiring synthesis across sections
   (Methods design + Results outcome) need multi-passage extraction pass.
9. **Manual addition path** (LOW) — Researcher should be able to add a finding the
   system missed, with system doing the verification.

### Classification Layer
10. **Modality classification** (MEDIUM, SOLVED) — TCM/Ayurveda/conventional/
    integrative/functional/lifestyle classification built with deterministic
    lookup tables.
11. **Multi-domain assignment** (MEDIUM) — Findings should map to 1-N domains with
    relevance weights, not a single domain_id.
12. **Evidence tier classification** (MEDIUM, SOLVED) — Study design keywords map
    to tiers. Universal hierarchy replaces per-field pipelines.

### Verification Layer
13. **Library-level contradiction detection** (HIGH) — NLI checks passage vs finding,
    but does not check if new finding contradicts existing library findings.
14. **Completeness check** (HIGH) — No mechanism to detect if extraction missed
    findings. Count results-section paragraphs that produced no findings; flag
    if >30%.
15. **Corroboration scoring** (MEDIUM) — `sources.corroboration_count` field exists
    but is never computed. Independent studies supporting same finding should
    increment it.

### Library Integrity Layer
16. **Retraction detection** (HIGH) — Check Retraction Watch Database at ingestion
    and periodically. Flag findings from retracted sources.
17. **Preprint/published version tracking** (HIGH) — Same study as arXiv preprint
    and published journal version. Crossref indexes version relationships.
18. **Copyright-safe storage** (MEDIUM) — Store only extracted findings + passage
    quotes (fair use), never full PDF text. Discard uploaded PDFs after extraction.
19. **Author disambiguation** (MEDIUM) — "J. Smith" in cardiology and neuroscience
    may be different people. Use ORCID from Crossref for disambiguation.
20. **Replication tracking** (MEDIUM) — When new finding enters library, check for
    equivalent findings from different source groups. Link as replications.
21. **Erratum propagation** (MEDIUM) — Crossref indexes errata. Check for
    `type: erratum` relationships. Apply corrected values.
22. **Confidence temporal recalibration** (LOW) — Batch job finds findings with
    3+ studies on same question, recalculates confidence based on aggregate.
23. **Supplementary materials** (MEDIUM) — Extended methods, full data tables in
    supplementary PDFs. Download and process through same pipeline.
24. **Figure data extraction** (HARD, Phase 2) — Kaplan-Meier curves, forest plots
    contain critical data. Figure caption + OCR/image analysis needed.
25. **Persistence layer** (MEDIUM) — Pipeline output vanishes after function returns.
    Needs database writer: passages table, findings table, provenance table.

## Verified Tools

| Tool | Status | Install/Endpoint |
|------|--------|-----------------|
| GROBID Docker 0.8.1 | Running | `docker run --rm -d -p 8070:port lfoppiano/grobid:0.8.1` |
| Crossref API | Working | `https://api.crossref.org/works/{doi}` |
| OpenAlex API | Working | `https://api.openalex.org/works/doi:{doi}` |
| Semantic Scholar API | Working | `https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}` |
| PubMed E-utilities | Working | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` |
| Unpaywall API | Working | `https://api.unpaywall.org/v2/{doi}?email=X` |
| NLI DeBERTa-v3-large | Loaded | `cross-encoder/nli-deberta-v3-large` on HuggingFace |
| Instructor | Installed | `pip install instructor` — constrains LLM to Pydantic schema |
| Biopython | Installable | `pip install biopython` — full PubMed Entrez client |
| Pyzotero | Installable | `pip install pyzotero` — Zotero bibliography sync |

## Python Environment

- System python3 (3.14.6): API calls, GROBID client, modality classification.
  Run with `PYTHONPATH=""` prefix to avoid the operator agent venv site-packages conflict.
- the operator agent venv python3 (3.11.15): `/<workspace>`
  for torch + sentence-transformers (NLI model). Install typing_extensions in venv.
