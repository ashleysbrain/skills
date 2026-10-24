# Literature foundation pass: census-gated retrieval + relevance filter (2026-08-21)

Proven on the financial-domain foundation (F1 human financial wellbeing,
F2 business financial health, F3 startup runway science, F4 agent-fleet
compute economics; ledger T-260821-0088..0092; 122 live records, 90
on-topic after filtering, 0 fabricated). Applies when ANY new domain
enters the process flows and must satisfy the research-before-build law.

## Why the filter step exists
OpenAlex `search=` relevance returns ADJACENT mega-cited papers riding
every query: PRISMA (28k cites) inside a financial-wellbeing query,
bariatric-surgery trials inside a startup-survival query, USMLE/ChatGPT
papers inside an agent-economics query. Unfiltered retrieval produces a
foundation that looks rich and is mostly noise.

## Steps
1. Source gate BEFORE retrieval: only endpoints probed HTTP 200 within
   days. Carry a probe jsonl (id, endpoint, http_code, latency, sample
   title). Observed exclusions: Semantic Scholar 429s after 2-3 rapid
   calls; SSRN API 401 (auth-walled). OpenAlex + arXiv q-fin are the
   reliable free pair for cross-domain + quant work.
2. Per-foundation query sets (5 queries each worked well) -> raw JSONL
   recording EVERY query and error verbatim (zero-fabrication audit
   trail). OpenAlex: `mailto=` + `select=` params, ~0.35s sleep. arXiv:
   3.1s sleep (API asks 3s).
3. Keyword-containment relevance filter per foundation (lowercased title
   vs domain keyword list). Keep/drop counts go in the report — the
   dropped count is evidence of honesty, not failure.
4. Evidence grade A = live HTTP 200 + parsed metadata. Abstracts unread
   = pass-2 work: abstract reconstruction, then the Veritas gate via
   organism/openresearch_ingest.py with `--evidence literature_synthesis`
   (never consolidate ungated).
5. Report per foundation: kept/dropped counts, top-cited on-topic list,
   and the PENDING chain stated explicitly (never implied done).

## Reusable instrument
`/<workspace>` (stdlib only;
swap the OA/AX query dicts per domain; raw/ output beside it).

## Sequencing law (principal directive 2026-08-21, verbatim trigger:
"I need the research first.... don't short cut")
A new domain's foundation lands BEFORE any company/state instrumentation
in that domain; the principal later DIFFS company state against the
consolidated research. Company-side builds minted first get killed
before their first file write.
