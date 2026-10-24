# Intelligent Search — Co-occurrence Discovery Design

Session: 2026-08-11. The hardcoded concept list (even with 20 verified fields)
was still siloed. User: "this search is still too narrow with only 20 fields
and isn't intelligent searching."

## Problem

The `_generate_dynamic_topics()` function in pipeline_api.py hardcoded 20
OpenAlex concept IDs. Even after verifying all 20 against the API and expanding
from 8 DS-specific fields to cover physics, biology, medicine, environmental
science, social sciences, and materials, it was still a fixed menu. A new
research field publishing 2,000+ papers daily would never appear until someone
manually added its concept ID to the list.

## Solution: Co-occurrence Discovery

`intelligent_search.py` implements self-expanding discovery:

### Phase 1: Discover (0 LLM tokens)

Search OpenAlex for recent papers matching DS seed concepts. Extract concept
tags from each paper. Concepts that appear across multiple seeds have high
bridge potential.

```python
seeds = [
    "free energy principle active inference",
    "interoception prediction error computational",
    "predictive coding Bayesian brain",
]

for seed in seeds:
    data = _fetch_json(
        "https://api.openalex.org/works"
        "?search=%s&filter=publication_year:2024|2025"
        "&per-page=5&select=id,title,concepts" % seed
    )
    for paper in data["results"]:
        for concept in paper["concepts"]:
            if concept["score"] > 0.4:  # filter noise
                discovered[concept_name] = {
                    "concept_id": concept["id"].split("/")[-1],
                    "seed_count": count of seeds that found this concept,
                    "frequency": how often it appeared,
                }
```

### Phase 2: Rank and Select

Sort discovered concepts by bridge potential (seed_count desc, then frequency).
Take top 15: 5 by bridge potential, 5 by frequency within single seed,
5 by avg relevance score. This ensures both cross-field bridges and deep
single-field discoveries.

### Phase 3: Fetch Trending Papers

For each selected concept, fetch top-cited papers from 2024-2025.

```python
url = (
    "https://api.openalex.org/works"
    "?filter=concepts.id:%s,publication_year:2024|2025"
    "&sort=cited_by_count:desc&per-page=3"
) % concept_id
```

### Phase 4: Global Trending

Add most-cited papers from the last 30 days across ALL fields (no concept
filter) as a wildcard discovery channel.

## Results

From 3 seeds, discovered 70+ unique concepts including:
- Cognitive science (3-seed bridge)
- Psychology (2-seed bridge)
- Inference (2-seed bridge)
- Computer science (2-seed bridge)
- Bayesian probability (single seed, high score)
- Allostasis (single seed)
- N400 (single seed — discovered from predictive coding papers)
- Philosophy of language, clinical psychology, autism research, etc.

Nobody hardcoded any of these. They emerged from what researchers actually
publish.

## Rate Limiting

OpenAlex returns HTTP 429 after ~10 requests/second. Required mitigations:
1. `_fetch_json()` has 3-retry exponential backoff (1s, 2s, 3s delays)
2. `time.sleep(0.3)` between concept fetches in Phase 2
3. Results should be cached (current API endpoint doesn't cache yet)

## Cache Versioning

The hardcoded topics endpoint uses `_TOPICS_VERSION` in the cache file to
invalidate when field_queries change. The intelligent endpoint does NOT
cache yet — every call hits OpenAlex fresh. This is intentional for now
(always discovers new connections) but should add a short TTL (15-30 min)
to avoid rate limits.

## API Response Shape

```json
{
  "topics": [
    {
      "id": "intel_C188147891",
      "title": "Cognitive science",
      "summary": "110010 papers in 2024-2025. Top: ...",
      "pipeline_fit": "veritas",
      "trend_score": 9.8,
      "industry": "Cognitive science",
      "trending_papers": [...],
      "total_field_papers": 110010,
      "source": "intelligent",
      "discovery_method": "concept_co_occurrence",
      "bridge_potential": 3
    }
  ],
  "count": 12,
  "source": "intelligent",
  "method": "co_occurrence_discovery"
}
```

Note: `bridge_potential` > 1 means the concept was found from multiple seeds.
These are the cross-field bridges the user cares about.
