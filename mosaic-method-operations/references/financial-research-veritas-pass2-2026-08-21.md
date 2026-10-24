# Financial research pass 2 — anchor verification + Veritas gating (2026-08-21)

Session: financial-research thread (this skill's pitfalls section, items
7-10). Ledger: T-260821-0088..0091 -> stage=verified. All five anchor
claims Veritas PASS + consolidated to DS O'Keefe (:port), count 92->97
verified via /health endpoint.

## What ran (all live, zero fabricated records)

1. **OpenAlex 429 wall.** Verification bursts (3 queries, 0.35-10s
   apart, mailto param) still 429'd ~50% of queries. Retry ladder with
   exponential backoff (8s/16s/24s) recovered some, not all.
2. **Crossref polite pool = reliable fallback.**
   `https://api.crossref.org/works?query.bibliographic=<q>&rows=4&select=title,author,published,DOI,is-referenced-by-count,container-title&mailto=census@divinity.science`
   — zero failures across 8 queries, 4s spacing. Select only needed
   fields to keep payloads small.
3. **consumerfinance.gov 403s bots.** The CFPB FWB Scale primary page
   cannot be fetched directly. Correct pattern: verify the instrument
   through its PUBLISHED validation records (Crossref: "Validation and
   psychometric properties of the [CFPB scale]" 2025; "Translation,
   cross-cultural adaptation..." 2021). Never fabricate snippet text
   from a blocked fetch.
4. **Gate-path defect (sibling-agent lane, bus 2884).**
   `your-org/organism/openresearch_ingest.py` computes
   `WORKSPACE = dirname(dirname(__file__))` then joins
   `veritas_engine.py` — which does NOT exist at your-org root
   (engine lives at your-workspace root). Result: rc=2 "can't open
   file .../your-org/veritas_engine.py" for EVERY claim.
   **Canonical working entry point (placed this session):**
   `/<workspace>`
   (invocation copy of the gate CLI in canonical layout; gate logic
   byte-identical, zero edits to the sibling's file).
   Proposed real fix for sibling-agent: make engine path env-overridable
   (VERITAS_ENGINE) or vendor the engine into your-org.
5. **Smoke-then-gate pattern.** First call after any path change:
   `--claim 'smoke test...' --source self-test --evidence theoretical
   --no-consolidate --quiet` -> expect `{"verdict":"PASS",
   "consolidated":false}`. Only then gate real claims WITHOUT
   --no-consolidate so PASS routes to O'Keefe.
6. **Claim construction.** One Veritas claim per anchor; claim sentence
   carries the finding + dates, source string carries the live citation
   (title, year, citations, raw-file pointer). evidence=
   literature_synthesis. Emitted JSON includes `okeefe_memory_count`
   and `consolidated:true` — verify the COUNT DELTA and /health, never
   rc=0 alone (anti-decoration law).

## Gated anchors (5/5 PASS, O'Keefe 92->97)

- F1: CFPB Financial Well-Being Scale = validated psychometric
  instrument (validation studies 2021-2025).
- F1: Lusardi-Mitchell "Big Three" financial literacy instrument.
- F2: Ohlson 1980 probabilistic bankruptcy (6,098c) + working-capital/
  profitability cluster (Belgian 2003 1,817c; SME 2007 1,007c).
- F3: cash-burn/runway survival = active research area (downturn
  studies 2024).
- F4: cost-efficient LLM inference serving = active systems-economics
  area (LOIS 2026; PACO 2025).

## Execution mechanics (pitfall 9 proven live)

- Inline `python3 - <<'EOF'` heredocs arrived CORRUPTED twice this
  session (garbled tokens: `splitl ines`, ` LIVEwrite_text`, garbled
  claim text) — llm-vendor glm-5.3 payload corruption, known class. The
  corrupted batch produced SyntaxError at write time (caught); the
  danger is a batch that half-executes.
- **Compile-gate pattern:** `cat > /tmp/script.py <<'PYEOF' ... PYEOF &&
  python3 -m py_compile /tmp/script.py && python3 /tmp/script.py` —
  py_compile rejects corrupted payloads before execution.
- Foreground terminal max = 600s (a 900s attempt is rejected outright).
  Gate batches of 4+ claims (each up to 240s subprocess timeout) go
  background=true + notify_on_complete=true, then process wait.

## Artifacts

- Report: your-workspace/financial-research/RESEARCH-FOUNDATION-FINANCIAL-2026-08-21.md
- Raw: financial-research/raw/{verify-anchors*.json, gate-results-pass2.json}
- Bus: msg 2884 (gate defect, sibling-agent lane); msg 2868 (reroute notice).
- Ledger: F1..F4 stage=verified with outcome run-records.
