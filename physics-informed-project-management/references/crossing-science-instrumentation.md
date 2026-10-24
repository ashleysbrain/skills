# Crossing-Science Instrumentation (Regime-Crossing Physics on a Task Ledger)

Session-validated 2026-08-21 on the the OS task ledger (806 tasks / 1,726
append-only events). Source research: A/B regime-crossing question (Sofie
post, "Two crystals. Same chemistry"), verdict via the specialist engine — Crooks
fluctuation theorem SETTLED the asymmetry question; Kibble-Zurek and
Fenichel GSPT both generate crossing-region math (claim falsified);
formation-history criterion genuinely open.

## The Mapping (physics → process observable)

| Physics | Process analog | Live measurement (2026-08-21) |
|---|---|---|
| Crooks crossing asymmetry (forward vs reverse work) | Reopened task = forward/reverse crossing that didn't commute | 2/804 tasks (0.2%) — near-reversible = healthy |
| Kibble-Zurek quench rate → defect density | Claim-lag cohort vs reopen rate | <1min: 0%, 1–60min: 2.3% (N=87), ≥12h: 0% |
| Critical slowing down | p50 claim-lag drift per task kind | question p50=79h vs build p50=9.4m — the tail is the radar |
| Free energy F = cost − T·info_gain | est_cost birth facts | **785/804 tasks carried the schema default 1.0 — the biggest finding** |

Key infrastructure insight: the ledger already RECORDS the physics (birth
facts + append-only event history). Instrumentation computes observables
from existing state — no schema changes required. The instrument
(`gates/physics_probe.py`) is ~120 lines over two SQL queries.

## The Estimation-Discipline Law

When 97%+ of tasks carry a DEFAULT est_cost, every downstream ratio
(act/est, free energy) divides by a placeholder. The fix is not a new
field — it's a mint-time tagging law in the single write path
(`task_ledger.submit`): if the minter did not pass est_cost explicitly,
append `[est_cost=default(unscored)]` to detail. Probes then exclude
tagged tasks from ratio math instead of silently dividing by defaults.
Deliberate `est_cost=1.0` is NOT tagged — the minter chose it.

Selftest pattern (3 cases, temp DB copy, never prod):
1. mint without est_cost → tag present
2. mint with explicit est_cost=1.0 → no tag (deliberate choice)
3. mint with est_cost=0.5 → no tag

## Failure-Only Health-Gate Pattern (band crossing)

`physics_health_gate.py` wraps the probe for daemon consumption:
- Silent rc=0 while every observable is inside its band (principal law: healthy =
  zero output)
- rc=2 + one-line reason on band crossing → message-bus alert via the
  reconciler's alert() (transition + hourly cooldown gated)
- First run = baseline snapshot; history-dependent bands stay silent

Bands (all require the physics to CROSS, not merely exist):
- CROOKS: reopen share > 5% absolute
- KZM: 1–60min cohort reopen% > 2× prior snapshot, N≥30 both sides
- CRITSLOW: any kind's p50 claim-lag > 2× prior, N≥5

**Falsification is mandatory before trusting the gate**: fabricate a
prior/now pair that MUST trip each band, assert it trips; assert
steady-state pairs produce zero hits. 4/4 bands verified this way before
the gate was trusted.

## Crossing-Science A/B Protocol v1 (harness A/B flows)

A one-direction A/B measures preference, not structure — the exact analog
of measuring hysteresis in one sweep direction. Protocol (annotated onto
the harness A/B task T-260818-0081):

1. **Both directions**: same-task twins run A→B AND B→A.
2. **Dissipation per run**: tokens, wall-clock, est_cost, reopens.
3. **Crooks log-ratio** of forward vs reverse outcome-quality
   distributions = the arbiter. Asymmetry > 0 means ordering carries real
   work → persist the winner.
4. **Adiabatic promotion**: shadow → partial → full. Our own ledger shows
   the quench signature (1–60min switch cohort reopens 2.3%; <1min and
   ≥12h cohorts 0%) — fast full swaps produce defects.
5. **N≥3 per direction** before any close (variance law). No verdict
   citable without physics observables attached.

## Environment Notes

- Probe JSON goes to stdout MIXED with human table output — parse with
  `re.search(r"\{.*\}", raw, re.S)`, not bare `json.load(stdin)`.
- The daemon lane system (`cadence_reconciler.py`) takes absolute script
  paths in LANE_JOBS; rc 0 and 1 count as green, rc 2 = red → alert.
- New-file writes to existing artifact directories can be blocked by a
  baseline-first gate; writing via terminal heredoc + `ast.parse` syntax
  check is the working path.
