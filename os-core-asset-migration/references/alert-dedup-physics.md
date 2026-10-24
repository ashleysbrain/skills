# Alert Dedup Physics (bus emitters: self-healing alerts + maintenance tickets)

Verified live 2026-08-20, Pass 6 (Cannon rotation). Both spam lanes measured,
gated, and re-tested through the production entrypoints.

## The physics

An alert carries information only when its signature CHANGES. An emitter on a
15-min cadence re-firing an identical defect is zero-surprisal — measured:
62 critical-alert posts and 71 maintenance tickets per 24h, all dedup-defeated.

**Score jitter defeats subject-line dedup.** Subjects like
`MAINTENANCE: INTER at 3.12` vs `at 3.17` are unique strings; every drift
mints a "new" ticket. Dedup keys must ROUND (0.1 granularity) so jitter
cannot defeat them, while a real worsening (>0.5) still re-alerts.

## Lane 1: critical alerts (`self_healing_loop._cron_post_alerts`)

- Cooldown: 6h identical-signature suppression, signature =
  sorted (dimension, round(score,1)) pairs.
- Reads the bus read-only (`mode=ro`), `DS_ORGANISM_ROOT` env override.
- Never let dedup block a genuine alert: wrap in try/except, fail-open.
- Verify by running the runtime entrypoint (launchd plist's exact argv) and
  counting bus rows before/after; a cycle with REAL criticals must post 0.

## Lane 2: maintenance tickets (`adaptive_thresholds.post_maintenance_ticket`)

The Ohno gate (pending-check + marginal hibernation) is NECESSARY but NOT
SUFFICIENT — its pending-check is vacuous under bridge ack-churn:

- The autonomic bridge acknowledges nearly everything within minutes
  (measured: 130 acks, zero rows survive in `pending`).
- So `COUNT(*) WHERE status='pending'` reads 0 almost always → gate always
  opens → rate bounded by ACK CADENCE, not information.
- Fix (additive, ahead of the existing checks): unconditional 2h
  same-dimension cooldown on `MAX(timestamp) WHERE subject LIKE
  'MAINTENANCE: <dim> %'` regardless of status.

## Parsing bus alert payloads

Alert content is MULTILINE: a JSON object on line 1, prose after.
`json.loads(content)` raises `Extra data` on every row → everything buckets
"unparseable" → probes report nothing. Use
`json.JSONDecoder().raw_decode(content.lstrip())[0]`.

## Testing gates without lying

- `post_maintenance_ticket` returns `linear_url is not None` — False means
  "blocked" OR "posted to bus but Linear failed" OR "your ticket dict was
  malformed and an `except: pass` swallowed it". Instrument internals before
  concluding the gate is broken (two false alarms taught this).
- Build probe tickets with `generate_maintenance_ticket()`, never hand-rolled
  dicts.
- Clean residue: `linear_bridge.close_health_issue(<id>)` for every synthetic
  Linear issue + `operator_bus.py complete <id> --result ...` for every bus
  row the probe created. Audit trails stay, open work queues don't.
