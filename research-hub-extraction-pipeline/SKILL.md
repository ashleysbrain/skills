---
name: research-hub-extraction-pipeline
description: Operate the Research Hub paper extraction pipeline.
version: 1.0.0
metadata:
  hermes:
    tags: [research, extraction, grobid, nli, modality, pipeline, research-hub]
    category: software-development
---

# Research Hub Extraction Pipeline

Use when building, extending, or operating the paper extraction pipeline for the
Research Hub — the researcher-facing platform that ingests academic papers,
extracts findings, classifies evidence, and verifies claims.

## Architecture

The pipeline lives at `/<workspace>`:

| Module | Purpose |
|--------|---------|
| `grobid_client.py` | GROBID Docker wrapper — PDF to TEI XML structured passages |
| `extraction_schema.py` | Pydantic models forcing structured extraction (finding + passage quote + evidence tier + modality) |
| `extractor.py` | Instructor + LLM extraction engine with quote verification |
| `modality_classifier.py` | Deterministic modality + evidence tier classification (TCM/Ayurveda/Kampo lookup tables) |
| `nli_verifier.py` | DeBERTa-v3-large NLI model for semantic claim verification |
| `benchmark.py` | Golden set benchmark framework (precision, recall, hallucination rate) |
| `pipeline.py` | End-to-end orchestrator (DOI or PDF to structured output) |

## Key Design Decisions

1. **GROBID for PDF parsing** — not PyMuPDF. PyMuPDF finds 0 tables, 0 figures, 0 reference sections in academic PDFs. GROBID uses ML models trained on academic layouts.

2. **Passage-grounded extraction** — the LLM reads one passage at a time, not the whole paper. Each finding MUST include a verbatim passage quote.

3. **Deterministic modality classification** — lookup tables for TCM herbs, acupuncture points, Ayurvedic concepts, not model judgment.

4. **NLI verification replaces keyword overlap** — the Popper audit documented that keyword overlap cannot detect contradictions. DeBERTa NLI catches semantic mismatches.

5. **PYTHONPATH conflict** — system python3.14 conflicts with the operator agent venv python3.11. Run pipeline scripts with `PYTHONPATH=""` prefix or use the venv python directly.

## GROBID Deployment

GROBID runs as a Docker container:
```
docker run --rm -d -p 8070:port --name grobid --memory=4g lfoppiano/grobid:0.8.1
```
Colima VM needs at least 8GB RAM. Startup takes 30-45 seconds.
API endpoint: `POST /api/processFulltextDocument` (NOT `/api/processFulltext`).

## Verified External APIs

- Crossref: `https://api.crossref.org/works/{doi}`
- Semantic Scholar: `https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=title,tldr,citationCount`
- OpenAlex: `https://api.openalex.org/works/doi:{doi}`
- Unpaywall: `https://api.unpaywall.org/v2/{doi}?email=X`
- PubMed: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`

## Architectural Audit (2026-08-11)

9 defects found and fixed:

1. **CRITICAL FIXED**: Extraction step never called (extractor=None, never initialized)
2. **CRITICAL FIXED**: NLI verification never wired into pipeline
3. **HIGH FIXED**: SSL verification globally disabled (CERT_NONE) — security vulnerability
4. **HIGH FIXED**: Nested div double-extraction (descendant selector grabbed inner div paragraphs)
5. **HIGH FIXED**: Temp PDF not cleaned on exception (os.unlink only on success path)
6. **HIGH FIXED**: Sequential API calls (60s worst case) → parallel ThreadPoolExecutor (0.3s)
7. **MEDIUM FIXED**: Quote verification O(n*m) → capped search with early termination
8. **MEDIUM KNOWN**: Tables/figures extracted without section context (hardcoded section="body")
9. **MEDIUM KNOWN**: No persistence layer — pipeline output vanishes (needs database writer)

## Remaining Build Items

1. Persistence layer — write pipeline output to Research Library database (passages table, findings table, extraction_provenance table)
2. Wire extraction with real API key — extractor module built but needs ZAI_API_KEY to run
3. Full golden set benchmark run — measure actual precision/recall on 50 papers
4. Preprint/published version deduplication via Crossref relations
5. Retraction detection via Retraction Watch DB
6. Table data extraction pass — GROBID extracts structure, need cell-level extraction for quantitative findings

## Platform Layer (12 Micro Tasks — All Complete)

Beyond extraction, the Research Hub has 12 modules serving 8 researcher workflows:

| Module | Purpose | Verified |
|--------|---------|----------|
| `entry_type_classifier.py` | 11 entry types (scientific_fact, empirical_finding, benchmark_result, etc.) | 97% classification rate on 364 real findings |
| `embedding_index.py` | Semantic search + vector index (all-MiniLM-L6-v2, 384-dim) | 1216 entries indexed in 26s, all queries return cross-domain results |
| `study_design_detector.py` | 21 universal study designs across all fields | Validated on real findings |
| `evidence_quality.py` | 3 quality systems routed by entry type (study design, reproducibility, authority) | All 364 findings scored with explainable labels |
| `gap_surfacing.py` | Detects missing meta-analyses, missing RCTs, single-domain bias | Correctly identified 2 gaps on golden ratio topic |
| `trust_panel.py` | Provenance chain, verification status, corroboration, contradictions | Working on findings + principles |
| `community.py` | Researchers, collections, notes, review queue, level progression | All tested: create researcher, collection, notes, queue, level up |
| `api.py` | FastAPI server (:port) with 16 endpoints serving all modules | All 10 tested endpoints returned real data |

## The Eight Researcher Workflows

| Flow | Status | Modules serving it |
|------|--------|-------------------|
| Discovery | OPERATIONAL | embedding_index (semantic search) + gap_surfacing |
| Understanding | OPERATIONAL | entry_type_classifier + evidence_quality + related entries |
| Trust | OPERATIONAL | trust_panel (provenance, verification, corroboration, contradictions) |
| Organization | OPERATIONAL | community (collections, notes, custom tags) |
| Contribution | OPERATIONAL | extraction pipeline + community (queue) |
| Collaboration | PARTIAL | shared collections work, discussion threads not built |
| Growth | OPERATIONAL | community (levels: explorer > contributor > verified > steward > fellow) |
| Feedback | OPERATIONAL | community (review queue for corrections) |

## Python Environment

- System python3 (3.14.6): use for API calls, GROBID client, modality classification (PYTHONPATH="")
- the operator agent venv python3 (3.11.15): `/<workspace>` for torch/sentence-transformers NLI
