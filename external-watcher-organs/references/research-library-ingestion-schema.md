# Research Library Ingestion Schema + Publisher Bot-Wall Recovery

Session-derived reference (2026-08-20) for absorbing external findings into
the the specialist engine (`research-library/research-library.db`).

## The live schema (read before INSERT — columns drift)

Do NOT guess column names. The first ingestion attempt of 2026-08-20 died
with `sqlite3.OperationalError: table sources has no column named added_at`.
The real columns:

```sql
-- sources
INSERT INTO sources (title, authors, venue, year, url, arxiv_id, doi,
                     source_type, credibility_weight)
VALUES (...);
-- credibility_weight: 1.0 primary paper/lab page, 0.8 science journalism,
--   0.5 default. created_at auto-fills (datetime('now')).

-- findings
INSERT INTO findings (domain_id, title, body, action_text, source_id,
                      tags, confidence)
VALUES (...);
-- confidence defaults 'high'; tags comma-separated.
-- date_observed/created_at/updated_at auto-fill. principle_id nullable.
```

Domains (verify live, these were current 2026-08-20): ai-tell-detection,
arts-design, behavioral-science, brand-philosophy, creative-systems,
data-science-ml, health-science, human-perception, neuroscience-cognition,
preference-learning, product-methodology, systems-architecture.

## Absorption pattern that worked (Media Lab + Quanta sessions)

1. Fetch the PRIMARY source (lab group page / arXiv paper), not just the
   news excerpt. Dissect it fully before writing.
2. One `sources` row per provenance tier: primary paper (1.0) AND
   journalism feature (0.8) both get rows; the finding links to the
   primary, the body references both.
3. `action_text` = the expansion uses, split near-term vs watch-track,
   named explicitly ("NOT near-term integration" is a valid classification).
4. Cross-stream discoveries (e.g. neuro2.ai author also in the Media Lab
   group) go IN the body — that is how future scans connect the streams.
5. Mint the ledger follow-on task for decision-grade questions at the same
   time; close the watcher-origin task with a run-record citing finding IDs.
6. Verify with a read-back join (finding id + domain name + source id)
   before reporting anything ingested.

## Publisher bot-walls → arXiv title recovery (verified twice 2026-08-20)

AIP (`pubs.aip.org`) served a ~6KB Cloudflare "Just a moment..." page to
curl. Recovery chain:

1. Distinctive title fragment from the URL slug:
   `.../3401363/Beyond-the-quantum-regression-theorem-in` →
   "quantum regression theorem".
2. arXiv title search:
   `curl -sL "http://export.arxiv.org/api/query?search_query=ti:%22quantum+regression+theorem%22&sortBy=submittedDate&sortOrder=descending&max_results=6"`
3. Match on title + recency — publisher dates postdate arXiv by 6-18
   months (JCP 2026-08 article ↔ arXiv 2604.13541 posted 2026-04,
   identical title, authors Bundgaard-Nielsen & Iles-Smith).
4. Fallback if arXiv misses: OpenAlex `filter=title.search:...` carries
   publisher metadata + DOI behind the wall.
5. Index 5-6 topical siblings from the same search (concurrent
   competitors of a "beyond the X theorem" paper are always adjacent).

Same pattern resolved an Annals of Mathematics 2025 paper (Cohen,
"Fractal uncertainty in higher dimensions", arXiv 2305.05022) that was
referenced only in Quanta journalism.
