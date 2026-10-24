# V3 Scoring Algorithm — A/B Tested Implementation

Tested 2026-08-11 against the baseline pipeline search across 3 queries.

## The A/B Test

Three test queries spanning science and tech:
1. "interoception prediction error computational psychiatry" (science)
2. "multi-agent reinforcement learning emergent cooperation" (tech)
3. "free energy principle artificial intelligence" (cross-disciplinary)

### Baseline metrics (current pipeline `optimized_research_search`)

| Query | Papers | Abstracts read | Tokens | Avg year |
|-------|--------|---------------|--------|----------|
| interoception | 15 | 2 | ~250 | ~2015 |
| multi-agent RL | 15 | 2 | ~250 | ~2016 |
| free energy + AI | 15 | 3 | ~225 | ~2018 |

### V3 metrics

| Query | Titles harvested | Selected for reading | Tokens | Avg year |
|-------|-----------------|---------------------|--------|----------|
| interoception | 23 | 5 | ~750 | ~2020 |
| multi-agent RL | 29 | 5 | ~600 | ~2023 |
| free energy + AI | 31 | 5 | ~750 | ~2024 |

### What the test proved

1. **Token savings claim was FALSE.** Baseline reads 2-3 abstracts (~250 tokens).
   V3 reads 5 (~600-750 tokens). The "25 abstracts at 6500 tokens" scenario
   that motivated four brainstorming passes was never the actual behavior.

2. **Recency is the real value.** V3 surfaces 2024-2026 papers that citation
   ranking buries. Baseline returns 2010-2017 papers.

3. **Quality floor works.** Removed noise like book chapter numbers
   ("17.3 ASSOCIATIONS BETWEEN...") that scored high on keyword overlap.

4. **IDF weighting works.** Prevents generic terms ("artificial intelligence")
   from dominating rare discriminating terms ("free energy principle").

5. **Clustering does NOT work** with title keywords. Most "clusters" had 1
   paper. Needs citation-graph data from sibling-agent's lane to work properly.

## Implementation: `_metadata_score_v3()`

### Quality Floor (`_passes_quality_floor`)

```python
# Reject: book chapter numbers, very short titles
if re.match(r"^\d+\.\d+", title) or len(title) < 15:
    return False

# Pass if ANY of:
if citations > 5: return True
if year >= 2024 and title_relevance > 0.5: return True
if venue in QUALITY_VENUES: return True
return False
```

### IDF Table

Hand-tuned for DS research domains. Needs recalibration for other fields.

```python
_IDF_WEIGHTS = {
    # Common (low signal): 0.2-0.4
    "system": 0.2, "model": 0.2, "artificial": 0.3, "intelligence": 0.3,
    "learning": 0.3, "review": 0.2, "survey": 0.2, "theory": 0.3,
    # Moderate: 0.5-0.6
    "prediction": 0.5, "computational": 0.5, "reinforcement": 0.5,
    "cooperation": 0.6, "emergent": 0.6, "consciousness": 0.7,
    # Rare (high signal): 0.8-0.9
    "interoception": 0.9, "morphogenesis": 0.9, "allostasis": 0.9,
    "percolation": 0.9, "psychiatry": 0.7,
    # Default for unknown: 0.5
}
```

### N-gram Phrase Matching

```python
# For each n-gram in the query (trigrams checked first, then bigrams):
# If the phrase appears in the title, add word_count * 0.10
# trigram match = 0.30, bigram match = 0.20
```

This is what prevents "Artificial Intelligence Theory Combining Buddhism"
from outranking "Artificial Consciousness and the Free Energy Principle" —
the FEP paper gets the trigram bonus for "free energy principle."

### Score Composition

```
raw = title_idf * 0.35
    + phrase_bonus        # additive, not multiplied
    + citation_log * 0.20
    + recency * 0.25
    + concept_overlap * 0.10
    + venue_boost * 0.05
    - dedup_penalty
```

### Operator Lane Split

- **the operator agent (this skill):** API endpoint, scoring function, Studio UI
- **Opencode:** Integrate `_metadata_score_v3()` as post-RRF re-ranking step
  in `optimized_research_search()` (veritas_process.py). After RRF fuses
  results from all sources, apply quality floor → IDF scoring → recency boost.
- **Opencode (future):** Citation-graph clustering (Phase 3). Title keywords
  don't work for clustering. Needs real co-citation data.

## Commits

- `3afb2ec` — v3 search methodology: IDF + phrase + quality floor + recency
- `ce19e2c` — Two physics-informed research engines + 5 API endpoints
