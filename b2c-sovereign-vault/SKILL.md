---
name: b2c-sovereign-vault
description: Use when principal private data needs a the operator agent-proof vault. Ops.
---

# B2C Sovereign Vault (persona data residency)

## Layout (fixed)

- `/<workspace>` — PERSONA zone, mode 700, raw personal data (health: apple_health.db 957MB, reports, ingest script). NEVER served, never leaves the vault.
- `/<workspace>` — PUBLIC zone: `server.py` (boundary) + `public/` (derived artifacts chosen for sharing).
- `/<workspace>` — append-only access audit (`access.jsonl`).

## Laws

1. Vault lives OUTSIDE `/<workspace>` (the operator agent engines roam that tree). Outside = no access.
2. persona/ is 700. Whitelist-only serving: report pdf/md/html + coverage.json, nothing else.
3. Other organisms (the operator agent) never get filesystem paths; they get `http://127.0.0.1:port/...` URLs to DERIVED artifacts only.
4. Boundary is read-only (POST 405), localhost-only, path-traversal 404, every request logged.
5. New shared fact = publish derived artifact to surface/public + add route in server.py ROUTES; never widen persona access.

## Operations

- Health check: `curl -s http://127.0.0.1:port/health` (expect organism b2c-sovereign).
- Negative test (should 404): `curl -o /dev/null -w '%{http_code}' http://127.0.0.1:port/persona/health/apple_health.db`.
- Server is launchd-seated via `~/Library/LaunchAgents/com.your-org.b2c-sovereign.plist` (RunAtLoad + KeepAlive). If it is running as a raw spawn, re-seat: `launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.your-org.b2c-sovereign.plist` from a NON-gateway shell (the the operator agent gateway blocks launchctl; that block is correct, do not bypass).
- New Apple Health export: `python3 /<workspace> /path/to/export_dir` (idempotent; re-runs insert 0 new rows).
- Audit cron jobs (AUDIT-ALGO/SMI/SYNTH) point at vault paths since 2026-09-28; keep path rewrites in sync if layout moves.

## Gotchas

- Inert historical text references to old `health-private` paths exist inside agent-organism memory transcripts (O'Keefe snapshot) — historical, not live; do not treat as leaks.
- The final firewall ORGAN (process-level egress control, consent keyed (issuer, data_type), fungal registration) is sibling-agent's lane per b2c-organism-spinup skill; bus row #62766 tracks it. The HTTP whitelist is the interim boundary.
- ls/cd into persona/ from an agent session works (same user) — filesystem perms are residency hygiene, not adversarial defense; the trust boundary for other organisms is network-only derived artifacts.