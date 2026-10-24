# Wellness-Budget Coupling (2026-08-17, second principal directive) — session detail

Directive (verbatim essence): "the cost of a model can ultimately be tied
into the financial wellness of either the user or the business because we
are scoring the financial wellness of each of those... so that we have the
appropriate budget for systems... it will all tie back to the stuff we've
already built."

Artifacts in `~/your-workspace/technology-registry/`:
`wellness_budgets.py` (reservoir engine, 6/6 selftest),
`wellness_budgets.json` (all constants as data), `wellness_feed.py`
(evidence feed). Ledger task T-260817-0028 (closed with run-record).

## The physics (reservoir model — same laws as the 8D scoring engine)

- **Reservoir = budget envelope.** `daily_cap = base_daily_usd * factor`.
- **Sigmoid factor**: wellness 0-1 → multiplier in [floor 0.1, ceiling 1.5].
  Floor > 0 is a DESIGN LAW: sick throttles hard but the organism keeps
  breathing (monitoring/heartbeats never lose funding). Ceiling releases
  headroom when wellness is strong.
- **Lagrangian drain step-down**: as the reservoir drains, the substrate
  selector's λ_cost RISES through profiles elite → balanced → bulk →
  scarce (thresholds green 0.5 / amber 0.8 as data). The system gets
  progressively cheaper per microtask BEFORE the hard cost gate stops it.
  No cliff — the step-down happens ahead of the wall.
- **Replenish = income events.** `record_replenish(entity, usd, reason)`
  raises the level and logs an append-only row.
- **Separate reservoirs per entity**: `user:principal` and
  `org:your-org`. An unhealthy business throttles its own compute
  before it throttles the user's.

## The evidence feed (never hand-set wellness)

`wellness_feed.py --sync` pulls the REAL financial dimension from
`ashley_unified_health.db` → `daily_scorecard.fin` (scale /10 → 0-1) and
calls `set_wellness()` with `source: "8d-fi:<evidence-date>"`. Unscored
entities REFUSE to guess — they hold bootstrap values, flagged
`wellness_source: "bootstrap"` in every budget resolution. No evidence →
no silent default (same fail-stop law as routing health).

Live proof: latest Fi evidence 2026-08-06 = 1.39/10 → wellness 0.139 →
factor 0.174 → user:principal cap throttled to **$1.39/day**, automatically.
When the score improves, the envelope opens with zero config edits.

## The full closed loop (every arrow executable)

8D scoring engine → Fi evidence → reservoir cap → drain profile →
substrate_selector λ → per-microtask model pick → cost_ledger spend →
back into the reservoir balance.

## Pitfalls found

- `dimension_trends` table existed but was EMPTY — read
  `daily_scorecard` directly (it carries `fin` + `fin_base` columns).
- Sigmoid steepness 8.0 at midpoint 0.5: wellness 0.15 → factor ~0.18,
  wellness 0.9 → ~1.45. Verify monotonicity + floor>0 in selftest, not
  just happy-path caps.
- The coupler imports cost_ledger for spend lookup — keep both in the
  same directory so `resolve_budget` reflects same-day spend, not a
  parallel ledger (one fact, one place — Codd).

## Reusable moves

- Register BOTH user and org reservoirs up front; org stays bootstrap
  until an org scorecard publishes a financial dimension.
- `resolve_profile()` returns a PROFILE NAME (data in
  selector_profiles.json), never an inline λ — one fact, one place.
- Demo sequence that proves the loop in one minute:
  register → set-wellness high → budget → set-wellness low → budget →
  feed --sync (real evidence overrides) → profile → selector pick.
