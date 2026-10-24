# Synthetic Selftests vs Live Data — 4 Gate Defects Selftests Could Not See (2026-08-17)

Failure class: a gate with a green selftest was claimed working; live production
data broke it four ways in one probe.

## The defects (all found by ONE live probe, all missed by 5/5 synthetic selftest)

1. **Self-block** — the gate blocked an operator because of the operator's OWN
   active bus threads. Fix: `check(..., operator=<id>)` + `self_exempt` config;
   own `from_op` rows are never "sibling" work.
2. **Universal-token false positives** — operator names ("hermes", "sibling-agent")
   plus words like "work"/"complete" overlapped nearly every message, making
   the gate block on everything. Fix: operator names + high-frequency words
   into the stopword list; overlap requires SUBSTANTIVE shared tokens.
3. **No reading-list age decay** — 9-day-old done threads surfaced as
   must-read for a new task. Synergy duty covers current ground, not
   archaeology. Fix: `reading_list_max_age_days` (~7).
4. **Own done work listed as unread** — the reading list fed the operator
   their own completed threads and result-type rows. Fix: self-exempt +
   skip `result` message type in reading lists.

## Why synthetic fixtures missed all four

Fixtures are too clean: distinctive tokens ("kernel manifest schema"), fresh
timestamps, no self-authored rows, no on-disk config file. Every defect class
existed only in messy real data.

## Durable rules

- After ANY selftest passes, run ONE LIVE probe against production data before
  claiming the gate works. Assert the live verdict is sane (GO on clean ground,
  not BLOCK from your own posts).
- Selftests must include: (a) a self-authored active row (must not block),
  (b) near-universal tokens (must not overlap), (c) stale done rows (must age
  out), (d) an on-disk config older than DEFAULT_CONFIG.
- **On-disk config silently overrides code defaults on merge**
  (`{**DEFAULT_CONFIG, **json.load(cfg_file)}`): after changing DEFAULT_CONFIG,
  refresh the on-disk config file too, or the fix never applies live. This one
  hid defect #2's fix for an entire cycle until a live re-probe caught it.

## Artefacts

- Gate: `~/your-org/your-stack/gates/synergy_gate.py` (7/7
  selftest incl. both regression tests; live GO verified)
- Ledger: same package `audit/claim-audit-2026-08-17.py`
