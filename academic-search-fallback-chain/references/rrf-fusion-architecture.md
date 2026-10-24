# RRF Fusion + Citation Graph Expansion Architecture

Implementation details for the optimized multi-source academic search system.
Proven in the VERITAS pipeline (2026-08-08). Reduced 9 API calls to 3-4 with
higher quality results via Reciprocal Rank Fusion.

## Problem with naive multi-source search

The default approach queries 5 APIs sequentially (arXiv, OpenAlex, Crossref,
PubMed, Semantic Scholar) then runs a duplicate verification function that
re-queries 4 of them. This results in:

- 9 API calls per pipeline run (44% waste from duplicates)
- ~20s total latency
- No ranking fusion (5 separate lists)
- PubMed queried for AI topics (zero relevant results)
- Crossref queried when OpenAlex covers the same DOI space

## Solution: RRF + Topic-Aware Selection + Citation Graph

### Step 1: Canonical paper key generation

```python
def _paper_key(paper: dict) -> str:
    """Generate a canonical dedup key from any paper dict across sources."""
    doi = (paper.get("doi") or "").lower().replace("https://doi.org/", "").strip()
    if doi:
        return f"doi:{doi}"
    arxiv_id = paper.get("arxiv_id") or ""
    if arxiv_id:
        return f"arxiv:{arxiv_id}"
    title = normalize_title(paper.get("title", ""))
    if title:
        return f"title:{title}"
    return ""
```

The same paper from OpenAlex (DOI: `10.1016/...`) and arXiv (arxiv_id: `2401.12345`)
gets different keys. Title-based merge in the RRF step catches these.

### Step 2: Reciprocal Rank Fusion

```python
def reciprocal_rank_fusion(ranked_lists: list, k: int = 60) -> list:
    """
    RRF_score(d) = Σ 1/(k + rank_i(d))
    Cormack, Clarke & Butt, SIGIR 2009.
    """
    scores = {}
    paper_map = {}

    for ranked in ranked_lists:
        for rank, paper in enumerate(ranked):
            key = _paper_key(paper)
            if not key:
                continue
            scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank + 1)
            if key not in paper_map:
                p = dict(paper)  # copy, don't mutate original
                p["_sources"] = []
                paper_map[key] = p
            src = paper.get("_source", "unknown")
            if src not in paper_map[key]["_sources"]:
                paper_map[key]["_sources"].append(src)

    # Title-based merge: same paper from different sources with different IDs
    # (e.g., arXiv preprint vs published version)
    title_groups = {}
    for key, p in paper_map.items():
        title = normalize_title(p.get("title", ""))
        if title:
            title_groups.setdefault(title, []).append(key)

    merged_keys = set()
    final_papers = {}
    for title, keys in title_groups.items():
        if len(keys) > 1:
            merged_score = sum(scores[k] for k in keys)
            merged_sources = set()
            for k in keys:
                merged_sources.update(paper_map[k].get("_sources", []))
            best_key = max(keys, key=lambda k: (bool(paper_map[k].get("doi")), scores[k]))
            merged_paper = dict(paper_map[best_key])
            merged_paper["_sources"] = sorted(merged_sources)
            merged_paper["_rrf_score"] = round(merged_score, 6)
            merged_paper["_source_count"] = len(merged_sources)
            final_papers[title] = merged_paper
            merged_keys.update(keys)

    # Add non-merged papers
    for key, score in sorted(scores.items(), key=lambda x: -x[1]):
        p = paper_map[key]
        title = normalize_title(p.get("title", ""))
        if title in final_papers or key in merged_keys:
            continue
        p["_rrf_score"] = round(score, 6)
        p["_source_count"] = len(p.get("_sources", []))
        final_papers[f"_key_{key}"] = dict(p)

    return sorted(final_papers.values(), key=lambda x: -x.get("_rrf_score", 0))
```

### Step 3: Citation graph expansion

```python
def expand_via_citations(seed_papers: list, max_expand: int = 5) -> list:
    """
    Uses OpenAlex filter=cites:W123456789 to find papers citing the seed.
    Bibliographic coupling (Kessler 1963).
    """
    # Extract OpenAlex IDs from seed papers
    seed_ids = []
    for p in seed_papers[:3]:
        oa_id = p.get("openalex_id") or ""
        if oa_id:
            seed_ids.append(oa_id)
    if not seed_ids:
        # Fallback: DOI lookup
        for p in seed_papers[:3]:
            doi = (p.get("doi") or "").replace("https://doi.org/", "")
            if doi:
                lookup = f"https://api.openalex.org/works/doi:{doi}?select=id"
                # ... fetch and extract id
        if not seed_ids:
            return []

    # Query: papers citing the top seed, sorted by citation count
    seed_filter = f"cites:{seed_ids[0].split('/')[-1]}"
    params = urllib.parse.urlencode({
        "filter": seed_filter,
        "per_page": max_expand,
        "sort": "cited_by_count:desc",
        "select": "id,doi,title,publication_year,cited_by_count,authorships,abstract_inverted_index",
    })
    # ... fetch and parse
```

### Step 4: Topic-aware source selection

```python
_BIOMEDICAL_KW = frozenset({
    "clinical", "patient", "disease", "drug", "therapy", "health", "medical",
    "biological", "neural", "brain", "cancer", "treatment", "diagnosis",
    "symptom", "physiological", "disorder", "infection", "immune",
})

def is_biomedical_topic(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in _BIOMEDICAL_KW)
```

### Step 5: Fair RRF contribution guard

Semantic Scholar frequently returns 429 (rate limited). When it returns only
1-2 results, that single paper gets an unfair RRF boost. Guard:

```python
s2_results = search_semantic_scholar(query, max_results=5)
if s2_results and len(s2_results) >= 3:
    ranked_lists.append(s2_results)  # include in RRF
else:
    # log but don't fuse — unfair contribution
    pass
```

### Step 6: Zero-cost verification

The old pipeline made 4 duplicate API calls for "citation verification"
(re-querying arXiv, OpenAlex, Crossref, PubMed). The RRF dedup step already
knows which papers appear in multiple sources. Verification = count papers
with `_source_count >= 2`. Zero additional API calls.

## Offline verification test

Test with 3 simulated source lists, 7 raw papers, 2 overlapping titles:

| Rank | RRF Score | Sources | Paper |
|------|-----------|---------|-------|
| 1 | 0.0328 | openalex + arxiv | Active Inference: A Process Theory |
| 2 | 0.0323 | openalex + semantic_scholar | Free Energy Principle for Biological Systems |
| 3 | 0.0161 | openalex | The Markov Blankets of Life |
| 4 | 0.0161 | arxiv | A Novel Approach to Neural Computing |
| 5 | 0.0161 | semantic_scholar | Consciousness and Predictive Processing |

7 raw inputs fused to 5 unique papers. Multi-source papers rank highest.
Dedup working. Error dicts (HTTP 429 responses with no title/doi) correctly
filtered out by `_paper_key` returning empty string.

## API profiling data (2026-08-08)

| API | Latency | Rate Limit | Unique Yield | Citation Graph | Abstract |
|-----|---------|------------|--------------|----------------|----------|
| OpenAlex | 0.81s | Daily budget (resets midnight UTC) | HIGH | YES (refs + cited_by) | Inverted index |
| arXiv | 0.18s | Generous | HIGH (preprints) | NO | Summary field |
| Crossref | 0.51s | Generous | MEDIUM (DOI metadata) | NO | Sometimes |
| PubMed | 0.32s | Generous | ZERO for AI topics | NO | NO |
| Semantic Scholar | 0.39s | 100 req/5min free tier | HIGH but 429 frequent | YES (best) | YES |
