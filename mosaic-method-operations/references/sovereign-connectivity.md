# Sovereign connectivity layer (census + security falsification, 2026-08-18)

Session evidence: the OS QA panel MR1 (the specialist engine, 8D sensors) + MR5 (DS
Gilchrist, sovereignty falsification), both glm-5.3. Canonical artifacts:
stores/connectivity.store.json, audit/QA-MICRO-REVIEW-1-8D-SENSOR-LAYER-2026-08-18.md,
audit/QA-MICRO-REVIEW-5-SOVEREIGNTY-SECURITY-2026-08-18.md,
sovereign-user/health-webhook/sovereign_health_webhook.py (T-260818-0104,
built + live-verified).

## Two-layer connectivity architecture (principal directive 2026-08-18)
- ORGANISM_B2B layer: upstream-capable bridges (github gh CLI, Linear
  LINEAR_API_KEY GraphQL, notion ntn, telegram gateway, operator bus, apple
  notes/reminders bridges, obsidian vaults). Dead bridges with fixes:
  gws 401 (gws auth setup), himalaya unconfigured, xurl re-auth, imsg Full
  Disk Access, airtable key.
- SOVEREIGN_USER layer: user-organism connection hub; data NEVER flows to
  the operator agent or any B2B organism (verbatim directive). Governed by
  sovereignty_law_v2 below.

## sovereignty_law_v2 (falsified v1, do not reuse v1 wording)
v1 claimed "deny-by-default ACL + separate data plane" — neither existed in
code. v2 guarantees, each marked true/false against live state:
- G1 8D scoring/coupling/token custody local-only; src/engine zero network
  calls (TRUE for 8d-sleep-pwa).
- G2 OAuth tokens encrypted at rest, key from device keychain or PBKDF2,
  never server (FALSE: storage.ts:174 admits plaintext).
- G3 cloud-model inference gated per-dimension consent default-OFF +
  redaction + zero-retention endpoints + local audit log (NOT BUILT).
- G4 egress allow-list: provider domains only via single typed module,
  lint blocks fetch elsewhere (NOT BUILT).
- G5 explicit export is UI on top of G1-G4, not the enforcement layer.
- G6 hub process isolated from B2B engine plane (engines share 0.0.0.0
  open HTTP today).
THE INFERENCE LEAK: any cloud-model call whose prompt contains user data
(or derivable summaries) IS data egress. A coach calling glm-5.x with a
daily bundle is exfiltration-by-scoring. There is no laundering this.

## Substrate facts (MR5 corrections)
- Two repos diverge: 8d-sleep-pwa = sovereign core (zero fetch/https in
  src, IndexedDB only); 8d-sleep-web = OAuth chassis with plaintext
  localStorage tokens (connectionManager.ts:159-173). providers.ts lives in
  -web, NOT -pwa.
- T-0104 webhook receiver pattern (built, launchd KeepAlive :port,
  isolated from B2B port ranges): HMAC-SHA256 constant-time, 5-min
  timestamp window + nonce LRU, 10 MB bound, malformed-payload quarantine
  table (never auto-ingested), no CORS (preflight 405), 60/hr rate limit,
  raw-store-first ingestion. Test battery: signed POST 200 / replay 409 /
  bad-sig 401 / malformed 422 / preflight 405.
- Hub interface (T-0107) bound to constraints C1-C10 in MR5 section 6:
  egress allow-list module, per-dimension consent registry, encrypted
  token store, process isolation, CSP header, egress audit log, no
  localStorage, in-product data-flows table, SW rules, CI egress test.

## 8D sensor truth at census time (for calibration of future claims)
One live sensor (EF self-report 71d); PHY nearly dead (nutrition stale 83d,
activity 2 days); ENV/SOC/FIN literal zero; SOC emits 0.03 on baseline-filled
fields (false precision — empty dimensions must not emit numbers);
dimension_trends 0 rows; TWC dead 84 days; overall_confidence 0.336.
Build order: health webhook (DONE) -> ENV APIs -> Oura OAuth -> calendar/
comms aggregates -> FIN CSV (Plaid only on client demand).
