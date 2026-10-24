# Healthy-run telemetry anomaly monitor — build record (2026-08-20)

Session record for the T-260820-0115 build (the specialist engine), minted from the
arxiv 2608.02464 digest (T-260820-0065). Method transfer: failure
detection from observable step telemetry only, monitors trained ONLY on
healthy runs, no second-LLM judge, microsecond checks.

## What was built

`organism/telemetry/telemetry_anomaly_monitor.py` (OS-core canonical;
workspace path is a bridge symlink):

- **Baselines**: P1/P99 per (sensor, key) fitted from the observation
  history in `organism/telemetry/telemetry.db` (34k+ rows, 6 sensors:
  dim_sensors, bus_monitor, engine_heartbeat, cost_tracker,
  volatility_daily, task_log). 44 bands fitted on first run.
- **Evaluate**: trailing 1h window vs bands; fires when a value sits
  outside band + 25% of band span (per-side). Each finding carries a
  signature `anomaly:<ident>:<side>`.
- **Cooldown**: per-signature 6h lock in `anomaly_baselines.state.json`
  (anti-spam law; one signal per drift event, not per observation).
- **Exit codes**: 0 = healthy/silent, 2 = anomaly (failure-only cron
  alerting surfaces it). Baselines refit via `--fit`; `--selftest`
  injects a synthetic spike and asserts it fires.
- **Composition**: called from the existing
  `<agent-home>/scripts/telemetry_engine_heartbeat_cron.py` wrapper AFTER
  the 5-min sensor sweep — no new cron (principal no-new-crons law).

## Verification chain (all executed, none asserted)

1. `--selftest` -> injected spike 90 vs band [18,32] FIRES (PASS)
2. `--fit` -> 40 bands from raw history
3. First live evaluate -> 2 REAL anomalies: engine_heartbeat/alive=79
   (band 67-71) + degraded=3 (band 0-1)
4. Root-cause per finding -> both were sensor defects (see below), fixed
5. Post-fix sweep: alive=80, degraded=1, exit=0 silent
6. Refit on corrected data -> 44 bands

## The pattern worth keeping: monitor catches the SENSOR, not just the system

A healthy-run monitor flags distribution shifts with no opinion about
cause. Both first-day findings were upstream sensor rot:
- vocabulary false-positives (UP / empty status counted degraded)
- a silently-dead sensor (broken ecs.py shim path, ImportError since
  13:37 — the monitor fired on the GAP the dead sensor left)

**Protocol when an anomaly fires:** hand-classify a sample of the flagged
entities FIRST (curl each /health, read the self-report), THEN decide
whether the fix belongs in the sensor (vocabulary, import path) or the
system. Do not relay an anomaly to the bus until this classification is
done — a false-positive alert train erodes the alert channel.

## arxiv method -> organism mapping

| Paper (2608.02464) | Organism implementation |
|---|---|
| Observable step telemetry | telemetry.db observations table (sensor/key/value) |
| Monitors trained on healthy runs only | P1/P99 bands from history; flagged epochs excluded on refit |
| Microsecond per-step monitors | SQL percentile check, no model inference |
| No second-LLM judge | zero LLM calls anywhere in the monitor |

Limits (disclosed, not hidden): band method assumes roughly-stationary
healthy distribution; slow legitimate growth (fleet expanding 67->80
engines) permanently sits near the band edge until refit — refit cadence
(weekly + after known fleet changes) is the mitigation, and the refit
excludes epochs flagged since the last fit.
