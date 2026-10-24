# OpenAlex Bulk Enrichment Patterns

Learned from building the Otlet System TSC 2026 enrichment pipeline
(2026-08-07). The enrichment pipeline queries OpenAlex for each person
in a database, fetches their top works, creates citation/co-authorship
edges, and extracts concepts.

## The Script Architecture (proven pattern)

```
openalex_enrichment.py
├── Phase 1: Match persons to OpenAlex author IDs
│   ├── Search: GET /authors?search=NAME&mailto=X&per-page=1
│   ├── Store: UPDATE person SET openalex_id = ?
│   └── Skip already matched: WHERE openalex_id IS NULL OR openalex_id = ''
├── Phase 2: Fetch top works per matched author
│   ├── Fetch: GET /works?filter=author.id:ID&sort=cited_by_count:desc&per-page=5
│   ├── Reconstruct abstract from abstract_inverted_index
│   ├── Store paper node with DOI, year, abstract, venue
│   └── Buffer referenced_works for citation phase
├── Phase 3: Citation edges (cross-reference referenced_works)
│   └── Create cites edges where both papers exist in our DB
└── Phase 4: Co-authorship edges
    └── For each paper's authorship list, create collaborated_with edges
```

## Key Configuration Values

```python
SLEEP = 1.0              # NOT 0.15. IP-level throttle kicks in fast.
MAILTO = "you@example.com"  # Required for polite pool (100K/day vs 10K/day)
MAX_WORKS = 5            # Top cited works per author
CONCEPT_SCORE_THRESHOLD = 0.3  # Minimum concept relevance score
MAX_RETRIES = 7          # For 429 backoff
BACKOFF_CEILING = 15     # Max seconds per backoff step (not 30-60)
```

## 429 Retry Logic (proven)

```python
def api_get(url):
    for attempt in range(7):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": f"OtletSystem/1.0 (mailto:{MAILTO})"
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            time.sleep(SLEEP)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                # Linear backoff with low ceiling — NOT exponential
                wait = min(2.0 * (attempt + 1), 15)
                time.sleep(wait)
                continue
            if attempt < 2:
                time.sleep(SLEEP * (attempt + 1) * 3)
                continue
            return None
        except Exception:
            if attempt < 2:
                time.sleep(SLEEP * (attempt + 1) * 3)
                continue
            return None
    return None  # max retries exceeded
```

## SQLite Lock Prevention

```python
# In the enrichment writer:
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA synchronous=NORMAL")
conn.execute("PRAGMA busy_timeout=30000")  # wait up to 30s for locks

# CRITICAL: Kill any API server holding a read connection before
# running bulk writes. The server's connection persists between requests.
```

## Skipping Already-Enriched People

```python
def get_persons(conn):
    cur = conn.cursor()
    # Skip NULL AND 'NONE' (people confirmed to have no OpenAlex profile)
    cur.execute("""
        SELECT id, name, openalex_id FROM person
        WHERE openalex_id IS NULL OR openalex_id = ''
        ORDER BY name
    """)
    return cur.fetchall()

# After a full run, mark unmatched people:
# UPDATE person SET openalex_id = 'NONE' WHERE openalex_id IS NULL
```

## Abstract Reconstruction (REQUIRED)

OpenAlex does not return plain-text abstracts. Decode the inverted index:

```python
def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return None
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(w for _, w in word_positions) if word_positions else None
```

## Realistic Enrichment Expectations

| Conference type | Expected match rate | Reason |
|----------------|--------------------|---------|
| Neuroscience/CS conference | 90-95% | Academic researchers with publication records |
| Interdisciplinary (TSC consciousness) | 75-85% | Mix of academics + independent researchers |
| Alternative medicine / wellness | 40-60% | Many non-academic practitioners |
| Art / philosophy symposium | 30-50% | Many independent thinkers without indexed publications |

"NO MATCH" for independent researchers is correct data, not a pipeline failure.
Mark them as 'NONE' and move on. Their poster titles and concept tags from
title-based extraction are still valid graph nodes.
