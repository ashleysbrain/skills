# Otlet System Architecture Reference

## Context
The Otlet System is the evolution of the flat knowledge canon (canon.db) into a
living 3D heterogeneous knowledge graph of ALL science. Named after Paul Otlet
(1868-1944), Belgian visionary who proposed the Mundaneum in 1934 — a global
repository of all knowledge, indexed, cross-referenced, connected by links.
He described hyperlinks 50+ years before the internet.

Full spec: `/<workspace>`

## Research Findings (2026-08-07, 2 subagents)

### Existing Systems — NOBODY built what we're describing
- Eigenfactor/UCSD Map of Science: 2D, static, journal-level only (8K journals)
- OpenAlex: 250M papers, 2B citations, CC-0, API — but ZERO visualization
- Microsoft Academic Graph: DISCONTINUED 2021
- Semantic Scholar: 200M papers, proprietary, no 3D
- Scopus: paywall, no API

### Visualization Tools
- Obsidian graph: 5K-10K nodes, 2D canvas
- Three.js force-directed: 10K-50K nodes interactive in browser
- Gephi: 100K+ batch, desktop only, 2D
- Cytoscape: 1M+ desktop, 10K web
- Cosmograph.app: 1M+ WebGL/WebGPU, early stage

### The Gap
No solution combines: scientific data scale (100M+), 3D interactive exploration,
multi-type connection layers, real-time browser performance, domain-aware navigation.
WE ARE IN NOVEL TERRITORY.

## Mathematical Foundations

### Taxonomy Skeleton (free, CC-0)
OpenAlex topic hierarchy: 4 domains → ~26 fields → ~360 subfields → ~4,500 topics

### Embedding Pipeline (solved)
- SPECTER 2 (Allen AI): citation-aware paper embeddings, 768-dim. Title+abstract → SciBERT backbone.
- GraphSAGE: inductive graph embeddings, handles new papers without retraining.
- Fused: SPECTER 2 (semantic text) + GraphSAGE (citation graph structure)

### Layout Algorithm
- UMAP 3D (best for global+local structure preservation, ~1M nodes practical)
- LargeVis: O(n) for 10M+ scale
- d3-force-3d: client-side physics refinement after precomputed positions

### Scale Limits (what breaks at 1M+)
- O(n^2) adjacency matrices → must use sparse + approximate
- Browser WebGL collapses at ~50K-100K nodes → LOD/tiling mandatory
- No user navigates 1M nodes → hierarchical clustering + semantic zoom required

## Architecture: 7 Node Types, 14 Edge Types, 5 Layers

### Node Types
1. PAPER — title, abstract, year, doi, openalex_id, embedding, x/y/z
2. CONCEPT — label, domain, field, subfield, parent, embedding
3. PERSON — name, orcid, institutions, labs, tsc_role, embedding
4. INSTITUTION — name, country, type, labs, people
5. RESEARCH LAB — name, institution, head, members
6. EVENT — name, dates, location, host, presenters
7. VENUE — name, issn, publisher

### Edge Layers (toggleable in visualization)
- Citation: cites(Paper→Paper)
- Concept: discusses(Paper→Concept), subconcept_of(Concept→Concept)
- Social: authored, affiliated_with, member_of, collaborated_with, institution_collab
- Event: presented_at(Person→Event), presented_at_event(Paper→Event), hosted_event
- Organizational: hosts, lab_produced, published_in

### Zoom Hierarchy (Google Earth Model)
Z1 Universe (4-13 clusters) → Z2 Field (26-100) → Z3 Subfield (50-360) →
Z4 Topic (100-2000 papers) → Z5 Ground (individual papers, people, institutions)

## Tech Stack
- DB: SQLite+FTS5 (MVP) → DuckDB/Neo4j at scale
- Embedding: SPECTER 2 + GraphSAGE fused
- Layout: UMAP 3D + d3-force-3d
- Render: Three.js WebGL2
- API: FastAPI (:port)
- Data: OpenAlex API (free), arXiv (free), TSC website (scraped)

## Ownership Split
- the operator agent: schema, ingestion, embeddings, DB, API, Ebbinghaus gate, Goethe design, Luria QA
- Opencode: Three.js frontend, layout compute

## TSC 2026 Seed
- 483 presenters (papers + posters)
- Key figures: Stuart Hammeroff, Christof Koch, Anil Seth, Giulio Tononi
- ~3,000-7,000 nodes, ~15,000-50,000 edges
- Well within browser limits (~50K nodes)

## Build Plan (10 weeks: Aug 7 - Oct 11)
- Phase 1 (Wk 1-3): Foundation — schema + ingestion + OpenAlex (the operator agent)
- Phase 2 (Wk 3-5): Embeddings + layout (the operator agent + Opencode)
- Phase 3 (Wk 4-8): Visualization — Three.js + API (Opencode + the operator agent)
- Phase 4 (Wk 8-10): Polish + TSC demo (Joint)

## Opencode Bus Posts
- Bus 1513: Sherman model routing (per-task model selection)
- Bus 1523: Otlet Three.js frontend build request
