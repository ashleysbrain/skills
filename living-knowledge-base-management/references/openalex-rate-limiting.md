# OpenAlex API Rate Limiting — Patterns and Solutions

## Context

OpenAlex is a free CC-0 API (https://api.openalex.org) with 250M+ works,
2B+ citations. It is the primary data source for the Otlet System enrichment
pipeline. However, it enforces aggressive IP-level rate limiting that can
block an enrichment run for hours.

## Rate Limit Behavior (observed 2026-08-07)

### Polite Pool
- Add `mailto=you@example.com` to ALL API queries
- This enters the "polite pool" (higher rate limits, fewer 429s)
- Without mailto: 10 req/sec hard cap, frequent 429s
- With mailto: ~100K req/day, but still IP-throttled at scale

### Throttle Triggers
- ~300 API calls in rapid succession (even with 0.15s sleep) triggers 429
- Once throttled, ALL requests return 429 regardless of sleep or mailto
- Throttle resets in hours (observed: still blocked after 2+ hours)
- No documented reset interval — appears to be sliding window

### Rate Limit Headers (check these)
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 0
X-RateLimit-Reset: <unix-timestamp>
```

## Recommended Configuration

```python
SLEEP = 1.0              # minimum 1s between calls (not 0.15)
MAX_WORKS = 5            # top works per author
MAX_RETRIES = 7          # per-request retry limit
BACKOFF_BASE = 2.0       # seconds, linear (not exponential)
BACKOFF_CEILING = 15     # max backoff per retry
```

**Why linear not exponential**: exponential backoff (2^n) means retry 7
waits 128 seconds. With 33 unmatched people × 128s = 70 minutes wasted.
Linear backoff (2n) means max 15s, retrying faster when the throttle lifts.

## Enrichment Script Architecture

### Phase Separation (critical for resumability)

```
Phase 1: Author matching (search by name → get openalex_id)
  - 1 API call per person
  - Fast, stores openalex_id in person table
  - Rerun-safe: WHERE openalex_id IS NULL skips already matched

Phase 2: Works fetching (get top papers per author)
  - 1 API call per matched person
  - Slow (large responses with abstracts, concepts, references)
  - Rerun-safe: check if paper already exists before inserting

Phase 3: Citation edges (cross-reference referenced_works)
  - Zero API calls (uses stored data)
  - Buffer referenced_works in _openalex_refs temp table during Phase 2
  - Cross-reference after all papers ingested
```

### Handling "No Match" People

20% of TSC poster presenters have no OpenAlex profile (independent
researchers, artists, non-academics). Do NOT keep retrying them.

```python
# Mark unmatched people explicitly
db.execute("UPDATE person SET openalex_id = 'NONE' WHERE openalex_id IS NULL")

# Skip them in future runs
WHERE openalex_id IS NULL OR openalex_id = ''
# AND in Phase 2 map:
if existing_oa and existing_oa != 'NONE':
    oa_id_to_person[existing_oa] = pid
```

## Abstract Reconstruction

OpenAlex stores abstracts as inverted indexes (not plaintext). Reconstruct:

```python
def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return None
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(w for _, w in word_positions)
```

## SQLite Concurrency

When the API server and enrichment run simultaneously:

```python
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA synchronous=NORMAL")
conn.execute("PRAGMA busy_timeout=30000")  # wait up to 30s for locks
```

Without WAL + busy_timeout, the enrichment crashes with
`sqlite3.OperationalError: database is locked` when the API server holds
a read lock during a write operation.

## Overnight Cron Pattern

Set up a cron job that retries enrichment when rate limits reset:

```yaml
schedule: "0 1 * * *"     # 1am daily
repeat: 3                  # run 3 times (1am, 2am, 3am)
deliver: origin            # report results back
```

The cron prompt should:
1. Run the enrichment script
2. Restart the API server (to pick up new data)
3. Verify health + node/edge counts
4. Report whether new data was added

## Key URLs

- Author search: `https://api.openalex.org/authors?search=NAME&mailto=X&per-page=1`
- Works by author: `https://api.openalex.org/works?filter=author.id:ID&per-page=5&sort=cited_by_count:desc&mailto=X`
- Concept tags: `work.concepts[]` (scored 0.0-1.0)
- Primary topic: `work.primary_topic` (domain/field/subfield hierarchy)
- Abstract: `work.abstract_inverted_index` (inverted index format)
- Citations: `work.referenced_works[]` (list of OpenAlex work URIs)
