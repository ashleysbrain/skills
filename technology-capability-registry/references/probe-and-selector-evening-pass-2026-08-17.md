# Probe + Substrate Selector Evening Pass (2026-08-17) — session detail

Context: principal directive (evening volley) — build toward the internet-of-models
future: models free or pennies, OS chooses per MICROTASK from many
interchangeable models via measured capability. Zero hard-wired lanes.
Artifacts live in `~/your-workspace/technology-registry/`:
`probe_runner.py`, `registry.py`, `cost_ledger.py`, `prices.json`,
`substrate_selector.py`, `selector_profiles.json`.

## Found defects (Popper self-falsification pass)

1. **Selector dark**: `select()` ranked only `status=="probed"` entries;
   registry had 38 entries, ZERO probed. Selection layer existed but could
   never fire. (Architecture was all claimed, no measured.)
2. **`--model` probe evaporation**: CLI path printed results, never wrote
   the registry. Measurements lost on exit; spend still recorded. Fixed by
   routing single-model probes through the same canonical write as batch.
3. **Writer/reader schema fork**: probe wrote legacy `probe_results`;
   selector read v2 `status`/`measured`/`substrate`. 38 entries, 0
   selectable. Fixed via canonical write + dual-schema backfill of the 4
   legacy-probed llm-vendor models.
4. **Reasoning-model artifact**: nemotron returns `content: None`,
   `finish_reason: length`, answer in `reasoning_content`. Probes scored
   silence as 0.0. Fix trio: content->reasoning-tail fallback, terse-answer
   system prompt + max_tokens 1024 + timeout 180s, tail-120 scoring.
   Verification: same model 0.0 -> 100 on all axes.
5. **Cross-provider slug 404**: openrouter id `nvidia/nemotron-3.5-lightning:free`
   not valid on nvidia-nim (`nvidia/llama-3.3-nemotron-super-49b-v1.5` is).
   Slug map stored per-entry (`access.slug`), verified against live
   `/models` listing. Zero-score garbage from failed-slug probes was reset
   before re-probing (all-null measured = never measured).
6. **Cost gate holes (found by the gate falsifying its author)**: monthly
   cap declared in prices.json but never enforced (decoration);
   unpriced-model est $0 = budget bypass by omission. Gate now enforces
   monthly cap and refuses unpriced models until priced as data. Price
   shape must be `{prompt, completion}` dicts (flat floats crash usd()).

## Substrate selector design (the directive's core artifact)

`utility = fitness - λ · cost_normalized`
- fitness: weighted measured-axis score (registry ranker, measured only)
- cost_normalized: est USD / max est in pool (scale-free)
- λ: per-profile JSON data. elite=0.0, balanced=0.3, bulk=0.8, scarce=0.1.
- Empty pool REFUSES (fail-stop). Cross-substrate axes raise. 6/6 selftest:
  elite pick, bulk cost-weighting, cheaper-at-equal-fitness, unknown-profile
  refuse, cross-substrate refuse, cost sanity.

Live proof after fixes: 5 measured models (glm-5.3/5.2/4.7/4.5-flash +
external nemotron-lightning via NIM). Per-task selection live; the free
external model tops all profiles at fitness 100, est $0.00. Cost ledger:
nvidia $0.00, $4.99 of $5 daily budget remaining.

## Reusable moves

- Probe a new provider lane end-to-end BEFORE trusting scores: raw
  completion call -> inspect message shape -> map slugs -> THEN run axes.
- An all-zero probe result is a probe defect until proven otherwise
  (silence != incapability). Check the raw response shape first.
- Wire budget gate into chat() at the single call site so no path skips it;
  then the gate catching YOUR OWN unpriced slug is the system working.
- Tasks minted in the ledger: T-0026 (closed, build), T-0027 (wire WHO +
  WHICH MODEL into one dispatch record — open next beat).
