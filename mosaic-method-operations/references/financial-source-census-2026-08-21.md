# Financial Data Source Census (2026-08-21, finance-thread / Parag lane)

Knowledge bank: 36 external financial sources, every one live-probed
(HTTP code + sample title + latency recorded; no fabrication). Graded
A=16 / B=8 / C=12. Ledger: T-260821-0083 (census) + T-260821-0084
(Popper cross-exam), both closed rubric 1.0. Full machine-readable data:
/<workspace>
(42 KB; top-level keys: census_id, task, minted_by, date,
studio_baseline, sources, grade_counts, popper_cross_exam).

## Wire-now A-grades (key-free)
- Regulator: SEC EDGAR full-text search (1,332 live hits on probe;
  submissions JSON; XBRL frames), Treasury yield curve CSV (/all paths
  only), FOMC, World Bank, FINRA, CFTC
- Academic: arXiv q-fin, OpenAlex, Crossref JF/JFE/RFS by ISSN
- Market: Yahoo v8 chart (v10 is crumb-gated — use v8 ONLY),
  CoinGecko
- News/alt: Google News RSS, Seeking Alpha RSS, Wikimedia core REST

## Kills / downgrades (with causes)
- Dead: SSRN (401, API closed), IEX Cloud (timeout, paid), SEC tick
  pilot (static), Yahoo earnings calendar (404), IMF datamapper (403)
- Egress-blocked (host-side, not source death): FRED (4 timeouts),
  Stooq (JS wall), Reddit JSON (403, OAuth), Google Trends (429)
- Conditional B: GDELT (429x3, needs backoff), Crossref extras

## Studio wiring recommendation (child's consolidated verdict)
1. novelty-scan += Crossref finance journals + EDGAR FTS + GDELT
   (backoff-gated)
2. FLW-RESEARCH ingest tier-1 = all key-free A-grades
3. writing_evidence whitelist = journals + arXiv + OpenAlex + EDGAR x3
   + FOMC + Treasury + WorldBank; news/social NEVER evidence
4. Registry as data: stores/source-registry.store.json (id/endpoint/
   auth/grade/studio_targets/probe freshness); re-probe A monthly,
   B weekly

## Baseline gap (proven live)
Studio :port novelty-scan checks ONLY openalex + arxiv today — zero
financial wiring. Probe: "financial wellbeing scoring for households"
-> 200, CROWDED, 2.25s. This census closes that gap for finance;
other domains need their own census before wiring.

## Reusable probe tooling
/<workspace> (probe helpers)
+ probe-raw.jsonl (49 raw rows) + popper-reprobe.json (21 adversarial
re-probes). Pattern: probe everything, record verbatim, grade on
evidence, cross-exam with adversarial re-probes.
