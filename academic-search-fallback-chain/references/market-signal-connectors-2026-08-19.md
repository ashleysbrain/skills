# Market-Signal Connectors — free-tier live sources beyond the academic chain

Verified live 2026-08-19 while building the Research->Coursework pipeline
(Workstream 2). Module: `/<workspace>`.

## The honest-status envelope pattern

Every connector returns the same envelope and NEVER fabricates:

    {source, status: live|blocked|error, count, items: [...], notes}

- `live` — proven this run, real items returned
- `blocked` — known missing prerequisite (e.g. API key), with the exact env
  var to set; spending decisions belong to the user, not the agent
- `error` — attempted and failed THIS run (HTTP code in notes)

Aggregate callers sum `status == "live"`. Downstream scoring treats
missing/throttled sources as 0 signal, not as "no market exists".

## Sources and their real behavior (2026-08-19)

| Source | Endpoint | Behavior |
|---|---|---|
| HN Algolia | `hn.algolia.com/api/v1/search?query=Q&tags=story&hitsPerPage=N` | Reliable, no key, points/comments per story |
| Semantic Scholar | `api.semanticscholar.org/graph/v1/paper/search` | Works, but shared public pool 429s under burst; retry with growing backoff (5s, 10s); proved live then throttled within the same hour |
| GDELT 2.0 DOC | `api.gdeltproject.org/api/v2/doc/doc?query="Q"&mode=ArtList&maxrecords=N&sort=DateDesc&format=json` | Implemented with retry; IP-level 429 persisted a full working day — record as unproven, do not claim live without a successful run |
| PatentsView | `search.patentsview.org/api/v1/query_patent/` (POST, `X-Api-Key`) | Free tier REQUIRES API key (`PATENTSVIEW_API_KEY`); report blocked, do not fabricate patent counts |
| EconPapers/RePEc | `api.econpapers.repec.org` | Endpoint DNS-dead from this network; use labeled fallback |
| RePEc fallback | OpenAlex `filter=concepts.id:C162324750` (Economics concept) | Verified live, 5 works; label the fallback honestly in `notes` |

## Network-layer fixes required in any connector

1. Catch `urllib.error.URLError` AND `OSError` in the fetch helper — DNS
   failure ("nodename nor servname provided") raises before HTTP status
   exists; return code 0 with the message instead of crashing the batch.
2. Retries with GROWING backoff only on 429; never retry other codes blind.
3. `User-Agent` with contact mailto improves OpenAlex treatment.

## OpenAlex query construction (cross-ref to main skill)

- `title_and_abstract.search:` beats plain `search=` (plain matches journal
  names — "Chinese Optics Letters" for a quantum query).
- NEVER `sort=cited_by_count:desc` with a search filter: it overrides
  relevance ranking and returns mega-cited fuzzy matches (COVID/GBD medical
  papers for "active inference"). Fetch relevance-ranked (omit sort),
  over-fetch per-page=25, filter locally by concept-token overlap, then sort
  locally by citations.
- Concept IDs: verify live via `api.openalex.org/concepts/<id>` before
  trusting a zero — a one-digit typo (C162324850 vs C162324750) looks
  identical to deprecation.

## Scoring integration pattern (Synergy Composer)

When market signals feed a score, compute per-source normalized parts ONLY
from `status=="live"` sources and divide by the number of contributing
parts — absent sources contribute nothing and dilute nothing. Example:
HN top-points -> `log10(1+pts)/2.5`; S2 presence -> 0.5 base heat.
