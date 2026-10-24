# Case Study: Constellation/Otlet Stage 0 & Stage 1 Adversarial Review

**Context:** Research discovery platform (3D knowledge graph). Two staged-design
specs had survived a first pass that claimed "verified against live OpenAlex API."
The adversarial review found 3 design-breaking flaws by testing failure modes
the first pass never touched.

## Lesson 1: "Verified against live API" often means happy-path-only

The first pass made real API calls but only tested the happy path. It claimed:
- "2 OpenAlex calls for signup" — TRUE for <200-paper authors, FALSE for prolific ones
- "10-second budget" — TRUE for 1 paginated call, FALSE for the 10 pages a 2000-paper author needs
- "per-page=200 covers 95% of researchers" — the 95% was fabricated, no source

**Technique:** For every quantitative claim in the spec, hit the live API at the
claimed boundary AND beyond it. The spec said "per-page=200" → test per-page=201
and confirm it errors. The spec said "10 seconds" → compute the actual call count
for a 2000-paper author and multiply by the code's SLEEP constant.

## Lesson 2: Cross-design contradiction is a high-yield vector

Two specs written in the same session contradicted each other:
- Stage 0: "SPECTER 2 embeddings" (768-dim, local GPU)
- Stage 1: "text-embedding-3-small" (1536-dim, OpenAI API)

These cannot be cosine-compared. The core "see how your work connects" feature
silently produces no valid similarity edges. **Always review multiple specs from
the same project together** and cross-check that assumptions are consistent.

## Lesson 3: Constraint verification, not just code logic

The spec described a Postgres `SELECT ... FOR UPDATE SKIP LOCKED` worker. The
actual DB was SQLite — which has no row-level locking. The spec assumed a
UNIQUE constraint on `openalex_id`; the actual schema had a non-unique INDEX.

**Technique:** `.schema <table>` and `.indices <table>` reveal what the DB
actually enforces. A non-unique index is not a constraint — it's a performance
hint. Two concurrent writers can insert the same key.

## Lesson 4: Dedup-key mismatch between data shape and design

The stub design deduped via `citation_fingerprint = sha1(title|year|first_author)`.
But at signup, `referenced_works` from OpenAlex is a bare list of OpenAlex IDs —
no title, no year, no author. The dedup key cannot be computed from the available
data. The design also set `openalex_id: null` on stubs, discarding the one field
that WAS available.

**Technique:** Trace the actual data payload shape (curl the API, inspect the
JSON keys) and verify the design's fields can be populated from it. A dedup key
that requires fields not present in the input is a silent failure.

## The 9 findings (summary)

| # | Flaw | Severity | How found |
|---|------|----------|-----------|
| 1 | 10s budget breaks at >200 papers | CRITICAL | Live API: per-page max=200, pagination math |
| 2 | SPECTER2 vs OpenAI incompatible embeddings | CRITICAL | Cross-design contradiction |
| 3 | Stub dedup fails (bare IDs, fingerprint unusable) | CRITICAL | API payload shape inspection |
| 4 | No UNIQUE constraint on openalex_id | HIGH | `.indices` schema check |
| 5 | Rate-limit math wrong; backoff cascades | HIGH | Live headers + code analysis |
| 6 | 0.7x confidence unjustified | MEDIUM | No calibration data |
| 7 | Abstract-missing rate drops user papers | MEDIUM | Live API sampling (96% recent, 76% older) |
| 8 | ORCID disambiguation fragile | MEDIUM | Live 69-record response analysis |
| 9 | Postgres SKIP LOCKED on SQLite DB | MEDIUM | Schema-vs-design mismatch |

## What the first pass got right (to calibrate)

- 69-authors-per-ORCID: verified, real
- 2-call happy path: correct for simple case
- Inline concepts + referenced_works: eliminates extra graph calls
- Stub-as-status-flag architecture: sound (immortal node_id, free referential integrity)
