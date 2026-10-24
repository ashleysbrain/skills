---
name: academic-search-fallback-chain
description: Find academic papers across ALL disciplines (not just STEM). Covers the API escalation chain (OpenAlex → arXiv → Semantic Scholar → Crossref → Google Scholar), with working code for each, failure modes, and the inverted-index abstract decoder OpenAlex requires. Use when searching biomedical, neuroscience, consciousness, social-science, or any non-CS literature.
version: 1.0.0
metadata:
  hermes:
    tags: [research, academic, search, openalex, arxiv, semantic-scholar, crossref, literature]
    related_skills: [arxiv, openresearch, duckduckgo-search]
---

# Academic Search Fallback Chain

Reliable cross-disciplinary academic paper search. The core problem this
solves: every academic search API has a failure mode, and no single source
covers all disciplines. You need a chain that degrades gracefully.

## The chain (try in order)

| Priority | Source | Best for | Failure mode | Key needed? |
|----------|--------|----------|--------------|-------------|
| 1 | **OpenAlex** | Cross-disciplinary, biomedical, neuroscience, social science | Inverted-index abstracts (must decode) | No |
| 2 | **arXiv** | CS, physics, math, quantitative biology | Narrow corpus, no biomedical/clinical | No |
| 3 | **Semantic Scholar** | Citations, recommendations, JSON clean | HTTP 429 after a few calls | No (rate-limited) |
| 4 | **Crossref** | DOI metadata lookup | Frequent timeouts | No |
| 5 | **Google Scholar** | Broadest human-facing coverage | IP-blocks ALL automated access | N/A (scrape-only, unreliable) |

**Rule of thumb:** Start with OpenAlex for any non-pure-CS topic. Only drop
to arXiv when you know the paper is a CS/physics/math preprint. Use Semantic
Scholar for citation graph traversal AFTER you already have a paper ID.

## OpenAlex (primary, most reliable)

No API key. No aggressive rate limiting. Broadest discipline coverage.
Returns JSON. Stores abstracts as an inverted index (see decoder below).

### CRITICAL: concepts.id filter is DEPRECATED (verified 2026-08-14)

**OpenAlex retired the concepts taxonomy.** `filter=concepts.id:C71688214`
now returns HTTP 200 with **ZERO results** (the concept endpoint itself
404s). This is the worst failure mode — silent success with empty data. A
production research pipeline ran dead for days on 2026-08-13/14 because of
this: every "high-precision" concept-filtered query returned nothing, and
`if not data` failovers never fired because the API "succeeded".

**Current correct pattern — plain search + relevance sort + dynamic year window:**
```
https://api.openalex.org/works?search=SLEEP+NEUROSCIENCE
  &filter=publication_year:2020|2021|2022|2023|2024|2025|2026
  &sort=relevance_score:desc&per-page=15
```

Rules:
1. Use `search=` + `sort=relevance_score:desc`. Never sort concept-filtered
   results by `cited_by_count:desc` — that returns the most-cited papers IN
   THE FIELD, not relevant to the query (the original 2026-08-12 bug:
   "sleep neuroscience" sorted by citations returned "Gammarus species from
   Xinjiang").
2. Build the year list dynamically:
   `"|".join(str(y) for y in range(date.today().year - 5, date.today().year + 1))`
   A hardcoded year list silently excludes current-year publications —
   the second half of the 2026-08-14 bug.
3. `concepts` still EXISTS in work records for tagging/display — only the
   `concepts.id` FILTER is dead. `topics.id` is the successor filter if you
   can resolve topic IDs, but plain search + relevance sort is the robust path.
4. **Empty-results guard:** treat HTTP 200 with zero results as a failure
   worth failing over from (to the next source in the chain), not as "no
   literature exists".

**General lesson: when a scraper dies silently with HTTP 200, suspect
upstream API deprecation before debugging your own code.** Probe the exact
URL the code builds, then probe the resource endpoint directly
(`api.openalex.org/concepts/<id>` → 404 was the smoking gun).

### Search by topic

```bash
curl -s --max-time 15 \
  "https://api.openalex.org/works?search=meditation+MEG+neural+efficiency&per-page=10" \
  -o /tmp/oalex.json
```

The `meta.count` field in the response tells you total results for the
query — use it to judge whether you're broadening or narrowing effectively.
Iteratively add terms to narrow:

```bash
# 603 results (broad)
curl -s "https://api.openalex.org/works?search=meditation+MEG+connectivity+efficiency"

# Fewer, more targeted (narrow)
curl -s "https://api.openalex.org/works?search=meditation+magnetoencephalography+graph+theory+small-world+topology"
```

### Fetch a single paper by DOI

```bash
curl -s --max-time 15 \
  "https://api.openalex.org/works/https://doi.org/10.1093/nc/niaf047" \
  -o /tmp/paper.json
```

### Decode the inverted-index abstract (REQUIRED)

OpenAlex does NOT return plain-text abstracts. It returns a map of
`word → [positions]`. You MUST reconstruct the abstract yourself. This
trips up every agent the first time:

```python
import json
data = json.load(open('/tmp/paper.json'))
idx = data.get('abstract_inverted_index', {})
if idx:
    max_pos = max(pos for lst in idx.values() for pos in lst)
    words = [''] * (max_pos + 1)
    for word, positions in idx.items():
        for p in positions:
            if p < len(words):
                words[p] = word
    abstract = ' '.join(words)
else:
    abstract = '(no abstract)'
```

### Useful fields

`id`, `title`, `publication_year`, `doi`, `abstract_inverted_index`,
`authorships` (list, each with `author.display_name`),
`primary_location.source.display_name` (venue/journal), `concepts`,
`cited_by_count`, `open_access`

## Wikipedia REST API (structured knowledge extraction)

The Wikipedia **REST API** returns clean, structured JSON — no HTML
stripping needed. Far better than the old MediaWiki action API
(`api.php`) for extracting readable content. Use it for encyclopedic,
conceptual, or biographical research when you need definitions,
overviews, or context on scientific/artistic topics.

### Page summary (most useful endpoint)

```bash
curl -sL --max-time 10 "https://en.wikipedia.org/api/rest_v1/page/summary/Kuramoto_model" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('extract',''))"
```

Returns JSON with: `title`, `extract` (plain text, 300–800 chars),
`thumbnail` (image URL), `content_urls.desktop.page`.

**Batch multiple topics** by looping with a short sleep:

```bash
for topic in "Connectomics" "Free_energy_principle" "Reaction-diffusion_system"; do
  echo "=== $topic ==="
  curl -sL --max-time 10 "https://en.wikipedia.org/api/rest_v1/page/summary/$topic" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('extract','NO DATA')[:600])"
  sleep 0.5
done
```

### Rate-limiting pitfall

Rapid batched requests (8+ calls with no delay) start returning **empty
responses** (not errors — just empty extracts). This looks like the topic
doesn't exist when it actually does. Fix: add `sleep 0.5` between calls.
If you see a sudden run of `NO DATA` after successful earlier calls, it's
rate-limiting — slow down and retry, don't assume the pages are missing.

### When to use which Wikipedia endpoint

| Endpoint | Best for |
|----------|----------|
| `/api/rest_v1/page/summary/{topic}` | Clean extract, one topic at a time |
| `/w/api.php?action=query&list=search` | Full-text search across Wikipedia |
| `/w/api.php?action=parse&page={topic}&prop=wikitext` | Full raw article text |

## arXiv (CS/physics/math preprints)

See the bundled `arxiv` skill for full details. Quick version:

```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:transformer+attention&max_results=5"
```

Returns Atom XML — parse with Python's `xml.etree.ElementTree`. Good for
CS, physics, math, quantitative biology. NO coverage of clinical medicine,
neuroscience experimental work, consciousness studies, or social science.

### Field-specific search prefixes

arXiv supports field qualifiers for more precise searches. Use these
when `all:` returns too many false matches:

| Prefix | Searches | Example |
|--------|----------|---------|
| `all:` | All fields (default) | `all:connectome+visualization` |
| `ti:` | Title only | `ti:brain+AND+ti:visualization` |
| `au:` | Author only | `au:friston` |
| `abs:` | Abstract only | `abs:free+energy+principle` |
| `cat:` | Category | `cat:q-bio.NC` (neuroscience) |

Combine with `AND`/`OR`: `ti:brain+AND+ti:visualization+AND+all:art`

## Semantic Scholar (citation graphs)

Best used AFTER you have a paper ID, for finding what cited it or what it
cites. Fragile for search without an API key (429 after a few calls).

```bash
# Search (works, but rate-limited)
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=GRPO+reinforcement+learning&limit=5&fields=title,authors,year,citationCount"

# Citations OF a paper
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/citations?fields=title,authors,year&limit=10"

# References FROM a paper
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/references?fields=title,authors,year&limit=10"
```

## Crossref (DOI metadata)

Reliable for looking up a known DOI, but search is slow and frequently
times out. Use only when you have a DOI and OpenAlex doesn't have the
paper.

```bash
curl -s "https://api.crossref.org/works?query=meditation+MEG&rows=5&select=title,DOI,URL,author" \
  -H "User-Agent: YourApp/1.0 (mailto:you@example.com)"
```

## Working workflow: find a paper from a vague description

When the user describes a paper vaguely ("meditation, MEG, something about
small-world network efficiency"), the sequence that works:

1. Start with a broad OpenAlex search using the keywords they gave you.
2. Read `meta.count` — if it's in the hundreds, you're in the right
   neighborhood. Scan titles.
3. If nothing matches, iteratively add specificity (author field, method
   terms, journal terms).
4. When you find the likely paper, fetch it by DOI and decode the full
   abstract.
5. Confirm against the user's description before asserting you found it.
6. Be honest if you cannot find it — never fabricate a paper or abstract.

## Prior-art and competitive term sweeps

When the user asks whether a term, concept, or neologism already exists in
any field (e.g. "is anyone using 'physiomorphic' in AI?"), the academic
API chain above is necessary but NOT sufficient. You need broader coverage.

### Additional databases for term sweeps

| Source | What it covers | How to query |
|--------|---------------|--------------|
| **Google Patents** | Patents worldwide | `curl -sL "https://patents.google.com/xhr/query?url=q%3D%2522TERMA%2522%26num%3D10&exp=" -H "User-Agent: Mozilla/5.0"` — returns JSON, check `results.total_num_results` |
| **Datamuse API** | Lexical database, word associations, etymology neighbors | `curl -sL "https://api.datamuse.com/words?sp=TERMA"` (spelling match) or `?ml=TERMA` (meaning). Returns `[]` if the word has no lexical foothold |
| **USPTO Trademarks** | Registered trademarks (US) | `web_search` for `site:uspto.report TERMA` — uspto.report renders JSON cleanly |
| **Collins Dictionary submissions** | Crowdsourced new-word proposals (user-submitted, not accepted) | `web_search` for `site:collinsdictionary.com TERMA "new word suggestion"` |
| **Wikipedia** | Encyclopedia entries | `curl -sL "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=TERMA&format=json"` |

### Methodology

1. Run the term through ALL databases in parallel (batch `curl` calls in
   one `execute_code` block — each `curl` takes ~2s, 10 in parallel < 5s).
2. For each hit, check the DOMAIN. Is it in the user's field, or a
   different field that happens to use the same word? (e.g. "physiomorphic"
   exists in psychology, agriculture, and sunglasses but NOT in AI).
3. Read the actual definition at each hit. Same word + different meaning =
   no collision. Same word + same meaning = prior art.
4. Check for near-variants: `-morphic` vs `-mimetic`, `bio-` vs `physio-`,
   plural forms, hyphenated vs unhyphenated.
5. Compile a table: database / total hits / any in target domain?
6. When the user challenges findings ("I found it on Google"), re-verify
   with EXACT-PHRASE quoted searches and compare what Google actually
   returns vs what the user thinks they saw. Users frequently conflate
   visually-similar terms (e.g. "Physical AI" vs "Physiomorphic AI").
   Hold your ground with evidence. Show the actual search result titles and
   explain the collision clearly.

## Pitfalls

- **DEPRECATED concepts.id filter (2026-08-14)**: returns HTTP 200 with zero results — silent pipeline death. See the CRITICAL section above for the replacement pattern (plain search + relevance sort + dynamic year window).
- **Inverted index surprise**: OpenAlex abstracts look empty/garbled until
  you run the decoder. If the abstract field is a dict of `{word: [ints]}`,
  that's the inverted index — decode it.
- **Semantic Scholar 429**: Hits after 3-5 calls without an API key. The
  fix is to space out calls or apply for a key — not to abandon the API.
- **OpenAlex bulk enrichment 429 (IP-level throttle)**: When enriching
  100+ authors in sequence (search + fetch works per person), OpenAlex
  starts returning HTTP 429 on EVERY request after ~50-100 API calls in
  rapid succession. This is NOT a per-request rate limit — it is an
  IP-level throttle that persists for 1-6 hours. Even `curl` from the
  terminal returns 429 during the ban window.
  - **Fix: Use 1.0s base sleep** (not 0.15s). The polite pool
    (`mailto=` parameter) raises the daily cap from 10K to 100K requests
    but does NOT prevent the per-IP burst throttle.
  - **Fix: Mark unmatched people as 'NONE'** so re-runs skip them.
    `UPDATE person SET openalex_id = 'NONE' WHERE openalex_id IS NULL`
    and `WHERE openalex_id IS NULL OR openalex_id = ''` in the query.
    Without this, every re-run re-processes all unmatched people (each
    costing 7 retries × 15s backoff = 2 min per person for a guaranteed
    "NO MATCH").
  - **Fix: Do NOT run enrichment via subagent** — delegate_task has a
    600s timeout. A 150-person enrichment at 1s/call × 2 calls/person
    = 300s just for author matching, leaving no time for works
    fetching. Run as `terminal(background=true, notify_on_complete=true)`
    instead.
  - **Fix: Kill API server before bulk writes** — a FastAPI server
    holding a read connection causes `sqlite3.OperationalError: database
    is locked` when the enrichment script tries to commit. Set
    `PRAGMA busy_timeout=30000` in the writer as a belt-and-suspenders
    defense, but killing the server is the clean fix.
  - **Legitimate "NO MATCH" expectation**: At a consciousness conference
    (TSC 2026), ~20% of poster presenters have no OpenAlex profile.
    These are independent researchers, artists, alternative medicine
    practitioners. "NO MATCH" is correct data, not a failure.
- **OpenAlex abstract reconstruction pitfall (already covered above but
  critical for enrichment)**: The `abstract_inverted_index` field is a
  dict of `{word: [positions]}`. The decode function MUST sort by
  position and join. Missing this means every enriched paper has a NULL
  abstract even though the data was fetched.
- **Google Scholar blocking**: It IP-blocks all automated access and serves
  a CAPTCHA/error page. Do NOT rely on it for programmatic search.
- **Browser search-engine CAPTCHA trap**: Do NOT use `browser_navigate`
  to Google, Bing, or DuckDuckGo search URLs. All three serve CAPTCHAs to
  automated browsers within 1-3 queries. This wasted multiple full turns
  in a real session (2026-07). Use `web_search` (native tool, routes
  through a backend API with no CAPTCHAs) for general web search. Use
  `curl` via `execute_code` for academic APIs. Reserve the browser for
  reading specific known URLs, not for search.
- **Crossref timeouts**: `curl` calls to `api.crossref.org` frequently
  exceed default timeouts. Always set `--max-time 15`.
- **Wikipedia REST API rate-limiting**: Rapid batched `curl` calls to
  `/api/rest_v1/page/summary/` (8+ with no delay) return **empty
  responses** — not errors, just empty extracts. Looks like the page
  doesn't exist when it actually does. Fix: add `sleep 0.5` between
  calls. If you see a sudden run of `NO DATA` after successful earlier
  calls, it's rate-limiting — slow down and retry, don't assume the
  pages are missing.
- **arXiv corpus gap**: arXiv has no clinical, biomedical, or social-science
  papers. Searching "meditation MEG" on arXiv returns almost nothing useful.
  Use OpenAlex for those topics.
- **Term collision vs prior art**: Finding the same word in a different
  field with a different meaning is NOT prior art. Always read the
  definition at each hit before claiming the term exists. A word used in
  agriculture (meaning "physiological + morphological") does not invalidate
  a coinage in AI architecture (meaning "mimicking the whole organism").
- **User conflation of similar terms**: When a user insists "I found it on
  Google," run the EXACT-PHRASE quoted search and show them the actual
  result titles. Visually-similar terms ("Physical AI" vs "Physiomorphic
  AI") flood search results and create false impressions. Do not
  capitulate to a vague claim — verify and present evidence.
- **Premature "zero results"**: If a broad term search returns 0 hits in
  the target field, that does NOT mean the term is absent. Before declaring
  novelty, run INTERSECTION searches that combine the term with adjacent
  fields the user might be thinking of. Example (2026-07): searching
  "physiomorphic" broadly returned agriculture + psychology hits, and I
  declared "zero in AI." But searching `"physiomorphic" digital twin human
  physiology medical` immediately surfaced two active research lines
  (Denison/NPBH neuromodulation workshop, Manimaran cardiology) that the
  user already knew about. The user had to steer me there — that is a
  methodology failure. Always run at least 3 intersection searches
  pairing the term with plausible adjacent domains BEFORE claiming zero.
  See `references/prior-art-term-sweep.md` for the intersection-search
  protocol.
- **Full-text PDF mining for terms inside papers**: Academic APIs search
  titles and abstracts, not full paper bodies. A term used deep in a
  workshop report or methods section will be invisible to OpenAlex/arXiv
  metadata search. When you suspect the term exists but can't find it via
  API, download likely PDFs and grep the full text:
  `curl -sL "https://arxiv.org/pdf/XXXX.XXXXX" -o /tmp/paper.pdf && pdftotext /tmp/paper.pdf /tmp/paper.txt && grep -n -i "TERM" /tmp/paper.txt`
  This technique found 6 uses of "physiomorphic" inside a 56-page arXiv
  workshop report that the arXiv search API did not surface for the term.

## When ALL managed web tools are down (Firecrawl billing/402 errors)

Sometimes `web_search` AND `web_extract` BOTH fail with billing errors
(Firecrawl 402 Payment Required, insufficient balance). Academic API
sources (OpenAlex, arXiv, Semantic Scholar) are unaffected — they use
their own endpoints via curl, not Firecrawl. But if you need general web
search or page content extraction alongside academic APIs, use this chain:

1. **Brave Search via curl** — `search.brave.com/search?q=...` — best
   tolerance of any search engine for curl-based requests, no CAPTCHAs
   observed across many queries in a real session.
2. **DuckDuckGo Lite via curl** — `lite.duckduckgo.com/lite/?q=...` —
   works but CAPTCHAs after ~3 rapid requests.
3. **Page content via curl + regex HTML strip** — fetch any URL, strip
   tags with a Python one-liner (see pattern below).
4. **Bot-protected sites** (DataDome, Cloudflare) — use `browser_navigate`
   which has stealth features curl lacks.
5. **Pivot strategy** — if one source is blocked, search for the same
   facts on alternative domains. Wikipedia, niche blogs, and database
   sites often carry the same information without bot protection.

```bash
curl -sL --max-time 15 -A "Mozilla/5.0" "URL" | python3 -c "
import sys,re
t=sys.stdin.read()
t=re.sub(r'<script.*?</script>','',t,flags=re.S)
t=re.sub(r'<style.*?</style>','',t,flags=re.S)
t=re.sub(r'<[^>]+>',' ',t)
t=re.sub(r'\s+',' ',t)
print(t[:N])
"
```

**Key insight**: The academic API chain (OpenAlex → arXiv → Semantic
Scholar → Crossref) is completely independent of Firecrawl and keeps
working even when managed web tools are down. Always try academic APIs
first for paper/literature searches; fall back to the web chain above
only for non-academic sources (blogs, news, company pages).

See `references/web-research-fallback-chain.md` for the full worked chain
from a real research session where all Firecrawl tools were down.

- `references/cognitive-science-of-writing-verified-papers.md` — 14 verified
  papers on the cognitive science of writing (Flower & Hayes, Sommers, Kellogg,
  Doshi & Hauser, Bastani, Lee CoAuthor, Toulmin, Osborne, PRISMA, Walton,
  Booth Craft of Research) with real abstracts and citation counts. Retrieved
  live via OpenAlex 2026-08-10.
- `references/science-graph-3d-foundations.md` — condensed knowledge bank
  on representing all science as a connected 3D graph: taxonomy hierarchy
  (OpenAlex/MeSH/ACM CCS/UCSD/DDC), graph embedding methods (node2vec,
  GraphSAGE, SPECTER, PyTorch-BigGraph), 3D layout algorithms (UMAP,
  t-SNE, LargeVis, force-directed), what breaks at 1M+ nodes, **cross-
  disciplinary bridge detection** (betweenness centrality × embedding
  distance × degree), **7-factor credibility scoring** model, and the
  **proven Otlet heterogeneous graph schema** (7 node types / 14 edge
  types / 5 layers).

## Multi-source fusion: Reciprocal Rank Fusion + citation graph expansion

When searching multiple academic APIs for the same query, fuse results using
Reciprocal Rank Fusion (Cormack, Clarke & Butt, SIGIR 2009) instead of
presenting separate lists or naive concatenation:

    RRF_score(d) = Σ 1/(k + rank_i(d)), where k=60

This provably outperforms any single source. Each source contributes a
ranking; papers high in multiple lists get the highest fused score.

### Cross-source dedup (CRITICAL)

The same paper appears under different identifiers across sources:
- OpenAlex: `doi` field (e.g. `10.1016/j.neubiorev.2017.01.001`) + `openalex_id`
- arXiv: `arxiv_id` field (e.g. `2401.12345`), often NO DOI
- Semantic Scholar: `paper_id` field, often NO DOI
- PubMed: `pmid` field, NO DOI

Without canonical key generation, the same arXiv preprint in OpenAlex (DOI)
and arXiv (arxiv_id) gets TWO entries instead of fusing into one. Generate
keys via: DOI first, then arxiv_id, then normalized title. Also merge by
normalized title to catch preprint-vs-published duplicates.

### Topic-aware source selection

Not all sources are useful for all topics:
- arXiv has ZERO biomedical/clinical/social-science coverage
- PubMed has ZERO AI/CS/physics coverage
- Querying PubMed for AI topics wastes an API call returning irrelevant results
- Use a deterministic keyword set ("brain", "neural", "clinical", "patient",
  "disease", "drug", "therapy") to decide whether to include PubMed — no LLM needed
- Crossref adds low marginal yield over OpenAlex (same DOI registry space)

### Citation graph expansion (bibliographic coupling)

Instead of more keyword searches, traverse the citation graph after initial
fusion. Take the top-ranked seed paper's OpenAlex ID and query
`filter=cites:W123456789` to find papers citing it. This is bibliographic
coupling (Kessler 1963) — papers citing the same seeds are topically related.
One API call finds work that keyword search misses.

### Fair RRF contribution guard

If Semantic Scholar returns only 1-2 results (rate limited), that single
paper gets an unfair RRF boost (it gets S2 contribution while no other paper
does). Skip S2 from RRF fusion when it returns <3 results. Log it but don't
fuse it.

### Optimized pipeline measured results (2026-08-08)

| Metric | Old (5-source + duplicate verification) | Optimized (RRF + citation graph) |
|--------|----------------------------------------|----------------------------------|
| API calls | 9 | 3-4 |
| Latency | ~20s | ~2.5s |
| Duplicate calls | 4 | 0 |
| Ranking | None (5 separate lists) | RRF fusion |
| Citation graph | Not used | 1 expansion call |

## Presenting literature: actual papers, not generalizations

**User preference (verified 2026-08-10, signal strength: 9x repeated):**
When the user asks for literature or research, they want the ACTUAL papers
with real abstracts, real citation counts, real DOIs, and real venues —
NOT your synthesized generalization of what the papers say.

**The protocol:**
1. Search by DOI lookup when you know the specific paper — generic keyword
   search returns irrelevant high-citation papers from other fields.
2. Present each paper with: authors, year, full title, venue, citation count,
   DOI, and the ACTUAL ABSTRACT (decoded from OpenAlex inverted index).
3. Let the user read the primary source text. Do NOT paraphrase findings into
   your own bullet points and present those as the deliverable.
4. Only AFTER presenting the actual papers, offer your synthesis — clearly
   labeled as interpretation, not as the literature itself.

**DOI lookup pattern (most reliable for known papers):**
```python
# When you know the paper title/author but generic search returns noise,
# look it up by DOI directly:
url = f"https://api.openalex.org/works/https://doi.org/{doi}"
# This bypasses the keyword matching that returns irrelevant results.
```

**Common failure:** Generic `search=` query for "Flower & Hayes cognitive process"
returns marketing AI papers, not the foundational 1981 CCC paper. The `title.search:`
filter is more precise:
```python
url = f"https://api.openalex.org/works?filter=title.search:{quote(query)}&sort=cited_by_count:desc"
```

## See also

- `references/rrf-fusion-architecture.md` — full implementation of RRF + dedup +
  citation graph expansion + topic-aware source selection with measured results
- `references/openalex-working-script.md` — a complete Python script for
  OpenAlex search + abstract decoding + clean output formatting
- `references/openalex-bulk-enrichment-patterns.md` — proven patterns for
  bulk-enriching 100+ people from OpenAlex (rate-limit handling, retry
  logic, SQLite lock prevention, skip-already-enriched, realistic match
  rate expectations by conference type)
- `references/prior-art-term-sweep.md` — full methodology for competitive
  term sweeps across academic, patent, trademark, and lexical databases
- `references/web-research-fallback-chain.md` — the curl + Brave Search +
  browser fallback chain when Firecrawl/managed web tools are down
- `arxiv` skill — bundled, covers CS/physics/math search in depth
- `openresearch` skill — the gate research findings pass through before
  entering the organism knowledge base (VERITAS)
