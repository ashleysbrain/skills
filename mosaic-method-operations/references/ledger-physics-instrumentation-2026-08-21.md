# Ledger Physics Instrumentation — 2026-08-21

principal directive: when research lands, do not stop at the verdict — ask "can we
take this science and apply it to our processes to improve organism health and
performance, in ANY way? Build on the science." Research → instrumentation →
minted build tasks. Mosaic methodology always.

## The mapping (crossing science → ledger observables)

The task ledger already records the physics; it just was never measured as
physics. No schema change needed:

| Science | Ledger observable | Live measurement (804 tasks, 2026-08-21) |
|---|---|---|
| Crooks fluctuation theorem (forward/reverse asymmetry) | reopened task = non-commuting crossing | 2/804 = 0.2% (near-reversible = healthy) |
| Kibble-Zurek (quench rate → defect density) | claim-lag cohort vs reopen rate | <1min: 0%, 1-60min: 2.3% (N=87), >=12h: 0% |
| Critical slowing down | per-kind claim-lag quantiles | question p50=79h vs build p50=9.4m |
| Free energy (F = cost - T*info_gain) | est_cost discipline at mint | 785/804 carry DEFAULT 1.0 — gate is decorative until fixed |

Instrument: `gates/physics_probe.py` (built + executed live; --json mode for
telemetry absorption). Minted T-260821-0178 (improvement/immune) and
T-260821-0179 (question/scheduler).

## Research→build protocol (generalizes)

1. Route the verdict pass through the specialist engine (falsification) — grade claims
   against live literature before applying.
2. Ask "which infrastructure already records this quantity?" The answer is
   usually a store (ledger, bus, cadence_state), not a new schema.
3. Compute the observable with a read-only probe first — prove signal exists
   BEFORE proposing gates (adiabatic: measure first, gate later).
4. Variance law: N>=3 probe runs before closing any improvement minted from
   a probe result.
5. Mint follow-ups as typed tasks (improvement/question) with the probe
   output as evidence in `detail`.

## Ledger timestamp pitfalls (bit me 3x this session)

- Microtasks close within the SAME SECOND (claimed+done at identical
  timestamps) — a `duration > 0` filter silently discards the entire
  population. Use `>= 0`.
- `tasks.created_at` mixes tz-aware and tz-naive ISO strings vs
  `task_events.ts`; always normalize with `d.replace(tzinfo=UTC)` on naive
  values before subtracting, else TypeError.
- Event vocabulary is richer than states: `minted/claimed/done/cancelled/
  briefed/stage/reopened/...` — take FIRST occurrence per event name per
  task; `reopened` is the defect/rework signal, not state='blocked'.
- sqlite3.Row has no `.get()`; guard `created_at` fetch explicitly.
- Check est_cost distribution before trusting act/est ratios: 785/804
  default-1.0 means ratio medians of 0.0x are artifacts, not findings.

## Related theory (verdicts logged in Research Library canon.db 190/191)

- Crooks FT: P_F(W)/P_R(-W) = exp(beta(W - dF)) — A->B vs B->A asymmetry.
- KZM limits: universal breakdown in fast quenches (Zeng PRL 2023);
  first-order-transition scaling contested (Fan 2025).
- Fenichel GSPT derives crossing (inner) dynamics from bulk (outer) —
  the "generate the crossing" answer.
- PSP linkages (materials AM): formation history → property classes, local
  practice, no universal criterion — open DS hypothesis: relaxation-time
  divergence as the class-split criterion.
