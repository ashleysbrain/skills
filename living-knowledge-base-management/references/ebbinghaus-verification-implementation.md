# the specialist engine Gate — Implementation Details

Built: 2026-08-05. Location: `gg3-blueprint/organism/engines/ds-ebbinghaus-engine/`.

## Engine Spec

- **Name:** the specialist engine (Hermann Ebbinghaus, 1850-1909, forgetting curve)
- **DS-ECS Code:** DS-ECS-IMM-06.01.02-v1.0.0
- **Port:** :port (NOT 8150 — taken by the specialist engine)
- **Body system:** Immune System + Prefrontal Cortex
- **Role:** knowledge_verification_gate
- **Canon DB:** `/<workspace>`

## File Structure

```
ds-ebbinghaus-engine/
├── src/
│   ├── ebbinghaus/
│   │   ├── __init__.py        # exports
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── engine.py       # 480 lines — verification engine core
│   │       ├── cognitive.py    # 226 lines — credibility weighting
│   │       ├── methodology.py  # 243 lines — verdict methodology
│   │       ├── philosophy.py   # 144 lines — engine philosophy
│   │       └── validation.py   # 327 lines — physics validation
│   └── api/
│       ├── __init__.py
│       └── server.py           # FastAPI server, 7 endpoints
└── run_server.py               # entrypoint
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Engine identity + full canon stats |
| POST | /verify | Submit draft text, get per-claim verdicts |
| POST | /query | Search canon for a specific claim |
| GET | /canon/stats | Principle/finding/source counts + credibility distribution |
| GET | /canon/domains | All 12 knowledge domains |
| POST | /canon/reinforce | Mark principle as accessed (boost accessibility) |
| POST | /canon/decay | Apply Ebbinghaus forgetting curve to stale entries |

## FTS5 Query Tokenization

The `query_canon()` method does NOT pass the raw claim string to FTS5 MATCH.
Raw multi-word strings are treated as exact-phrase queries, killing recall.
Instead, the method:

1. Splits the claim into lowercase tokens (>2 chars)
2. Removes stop words (the, and, for, are, but, this, that, with, from...)
3. Joins remaining tokens with ` OR ` (FTS5 OR query for max recall)
4. Limits to 12 tokens max
5. Passes the tokenized query to `WHERE canon_search MATCH ?`

This is the same pattern documented in `references/fts5-retrieval-pitfalls.md`
for canon_query.py, applied to the verification engine.

## Credibility Weighting

Canon DB `sources` table has `credibility_weight REAL` and `corroboration_count
INTEGER` columns (added 2026-08-05, backfilled for all 140 sources).

Weighted score = `similarity * credibility_weight * (1.0 + corroboration_count * 0.1)`

The query joins FTS5 results back to the `sources` table to get credibility:

```sql
SELECT s.credibility_weight, s.corroboration_count
FROM sources s
JOIN principles t ON t.source_id = s.id
WHERE t.id = ?
```

## Known Issues

### 1. Contradaction Detection False Positives
The naive contradiction detection checks for negation keywords (not, never,
refuses, marginalizing, false, incorrect, wrong, unlike, contrary, opposite)
in matched text. This produces false CONTRADICTED verdicts because these words
appear in canon entries that AGREE with the claim. Example: a claim about
"aesthetic bias" matched a principle about "AI models refuse to depict realistic
individuals" — "refuse" triggered false contradiction.

**Workaround:** Use /query endpoint for claim lookup (no contradiction detection).
Use /verify for full draft verification but treat CONTRADICTED verdicts as
"needs human review," not automatic rejection.

**Fix path:** Replace keyword-based detection with semantic negation comparison.

### 2. Similarity Score Uses FTS5 Rank
The similarity metric is `1.0 / (1.0 + abs(rank))`. FTS5 rank is a BM25-based
score where lower = better match. This produces very low similarity scores
(0.02-0.25 range) because BM25 ranks are typically large negative numbers.
The weighted_score (similarity * credibility_weight) ends up below the
CONFIDENCE_HIGH threshold (0.8) for most queries, so most matches produce
UNVERIFIED verdicts instead of VERIFIED. The threshold needs calibration
against real query/result pairs.

## Canon DB Schema Changes (Task 1)

Added to `sources` table:
- `credibility_weight REAL DEFAULT 0.5` (backfilled from source_type map)
- `corroboration_count INTEGER DEFAULT 0`

Added to `principles` and `findings` tables:
- `last_accessed TEXT` (timestamp of last access, null = never accessed)
- `accessibility REAL DEFAULT 1.0` (Ebbinghaus retention score, 0.0-1.0)

## Remaining Build Tasks

5. Wire into Veritas pipeline (Stage 5 -> Ebbinghaus gate -> Stage 6)
6. Wire into Crucible pipeline
7. Corroboration bonus system (tune contradiction detection)
8. Ebbinghaus decay scheduler (cron job applying forgetting curve)
9. Unify canon.db with DS O'Keefe MemoryTraces
10. Ingestion cron for continuous absorption
