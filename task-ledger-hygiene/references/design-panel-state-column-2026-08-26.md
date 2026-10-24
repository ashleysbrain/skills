# 10-Seat Design Panel → State Column Collapse (2026-08-26)

Session: adversarial design panel over the Conductor (:port) "Organism
State" column, then execution of the collapsed design. Companion to
`headless-ui-qa-batteries/references/conductor-respond-limb-2026-08-26.md`.

## Panel pattern that worked (10 seats, 2 waves + 3 re-runs)

Waves of 6 = delegation cap; API rate-limit (HTTP 429) killed 3 seats
mid-run — re-dispatch them with UPDATED context baked in (fixes shipped
since their first look), not their stale original prompt. Late/truncated
seats: read their partial transcript before re-dispatch.

Verdicts converged without conflict; the collapse inputs:
- **Seat 10 (fresh-eyes)**: default view was the machine's view —
  "the page leads with the organism's intestines instead of decisions."
  Highest leverage = Needs You default.
- **Seat 08 (attention economics)**: two layout candidates judged on
  decision-value per glance-second; 3-token header strip ≈ 95% of a 5-cell
  band's signal at ~5% attention cost. Verdict A (two-zone) + hybrid (keep
  cadence token).
- **Seat 09 (measurement validity)**: pokes/cycles and single-daemon
  uptime are VANITY (no denominator/baseline/discriminant validity —
  counterexample: daemon UP while 20/60 engines restart-loop). Valid
  proxies: events/day trend, closed:minted, needs-you age, fleet alive
  fraction, bus throughput, cursor-lag.
- **Seat 01**: hard precondition — counts must come from a live endpoint,
  never hardcoded.
- **Seat 05 (critical)**: `getJSON()` never checked `r.ok` — parsed 404
  bodies painted fabricated defaults. Fix: throw on `!r.ok || j.error`
  (whitelist real payload keys).
- **Seat 02**: metric law — every displayed value marked
  VERIFIED-REAL / FABRICATED / STALE; `ago()` Z-append bug on `+00:00`
  stamps; census served-but-never-rendered.

## Executed design (collapsed)

1. Needs You = default view (first toggle + `class="on"` section moved).
2. Two-zone flow grid (`1.6fr 1fr`), 340px plumbing column deleted.
3. 3-token live strip under the header: census counts (live read) +
   cadence token (`cycle Xs ago`) + "internals ›".
4. Internals drawer (click strip → drawer with System core / Executor
   cycle / pulse history) — demoted plumbing keeps drill depth.
5. `ago()` accepts trailing `Z` OR `+HH:MM` offsets.

## principal-law overrides of panel recommendations (on-record orders win)

Seat recommended filtering Needs You to `actor_class='human'` only; principal
standing order T-260826-0067 says EVERY awaiting-ruling decision renders.
Resolution: keep all rows, every card carries why_you instead. When a panel
verdict conflicts with a principal directive on record, the directive wins —
log the override in the task event.

## Battery verification of the rebuild

11 source checks (PASS all) + headless battery: default view paints 5
ruling cards; strip shows live census text; real-click on strip opens
drawer with d-health/d-cycle painted; flow grid two-zone with bus rows;
"Organism state" absent; zero page errors; JS syntax gate after every edit.
Cadence initially rendered "cycle" empty — the ago() fix had a second bug
(trailing-offset regex); fixed and re-proven (`cycle 18s ago`).
