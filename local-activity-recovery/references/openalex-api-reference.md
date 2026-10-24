# OpenAlex API — Academic Paper Search (no-auth fallback)

## When to use

When history recovery fails (Chrome still running, tab closed, not flushed)
but the user CAN describe the content of what they were reading. Pivot from
disk-based recovery to content-based academic search.

Also the cleanest first-try for ANY academic paper identification task,
regardless of whether local-activity-recovery was the trigger.

## Why OpenAlex over the alternatives

| Source | Failure mode |
|--------|-------------|
| Google Scholar | Bot detection — redirects to `google.com/sorry` CAPTCHA wall |
| Semantic Scholar API | 405 on web search, 429 rate-limit on API |
| DuckDuckGo HTML | Returns empty / cookie-wall page |
| Crossref | Often empty for niche/interdisciplinary queries |

OpenAlex (`api.openalex.org`) is free, requires no API key, returns
structured JSON, and has full-text search across 250M+ works.

## The search query

```bash
curl -s --max-time 10 \
  "https://api.openalex.org/works?search=<SPACE-separated+keywords>&per-page=10" \
  -o /tmp/oalex.json
```

The `search` param does full-text search across titles + abstracts + full text.
Results ranked by relevance. No filters needed for a keyword sweep.

## Reconstructing abstracts (inverted index)

OpenAlex stores abstracts as position-inverted indexes, not plain text:

```python
import json

data = json.load(open('/tmp/oalex.json'))
for w in data.get('results', [])[:10]:
    title = w.get('title', '')
    year = w.get('publication_year', '')
    doi = w.get('doi', '')
    idx = w.get('abstract_inverted_index', {})
    abstract = ''
    if idx:
        max_pos = max(pos for lst in idx.values() for pos in lst)
        words = [''] * (max_pos + 1)
        for word, positions in idx.items():
            for p in positions:
                if p < len(words):
                    words[p] = word
        abstract = ' '.join(words)
    authors = ', '.join(
        [a['author']['display_name'] for a in w.get('authorships', [])][:3]
    )
    print(f'{year} | {title}')
    print(f'  Authors: {authors}')
    print(f'  DOI: {doi}')
    print(f'  Abstract: {abstract[:400]}')
    print()
```

## Fetching a single paper by DOI

```bash
curl -s --max-time 10 \
  "https://api.openalex.org/works/https://doi.org/10.1093/nc/niaf047" \
  -o /tmp/paper.json
```

Returns full metadata: title, all authors, venue, abstract, concepts,
referenced works, cited-by count.

## Iterative narrowing pattern

When the first search returns too-broad results (count > 500):

1. First query: broad keywords (`meditation MEG connectivity efficiency`)
2. Review titles — identify which subfield the target paper lives in
3. Second query: add subfield-specific terms
   (`meditation magnetoencephalography graph theory small-world topology`)
4. The target paper usually surfaces in the top 10 of the refined query

The `meta.count` field tells you how many total results matched.

## Proven case (2026-07-06)

User vaguely recalled "a meditation article about MEG and efficiency using
small model networks." History recovery failed (Chrome still running, tab
not flushed). Pivoted to OpenAlex:

1. Broad search (`meditation MEG connectivity efficiency`) returned 603
   results including tangential papers
2. Refined to `meditation MEG whole brain network small-world efficiency
   experienced meditators` (63 results)
3. Target paper surfaced at rank 7:

> Pascarella et al. (2025). "Meditation induces shifts in neural
> oscillations, brain complexity, and critical dynamics: novel insights
> from MEG." Neuroscience of Consciousness. DOI: 10.1093/nc/niaf047

The "small model networks" in the user's memory was a compression of the
paper's critical-dynamics findings (deviation from criticality coefficient,
1/f slope, neural complexity).

## Selecting fields to reduce payload

For large result sets, add `&select=` to trim the response:

```
&select=id,title,abstract_inverted_index,doi,publication_year,authorships
```

Without `select`, each result is ~35KB. With it, ~5KB. Matters when paginating.
