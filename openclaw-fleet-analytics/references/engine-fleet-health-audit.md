# Engine Fleet Health Audit Procedure

This reference outlines the steps to verify that the Divinity Science (DS) engine fleet is up, running, operational, and fully connected with all four layers (physics layers 1‑3 and methodology layer 4).

## Overview

- **Goal**: Confirm each engine responds with `{"status":"ok"}` on `/health` and exposes a live `/v1/layers` endpoint (Layer 4 mounted).
- **Tools**: `curl` (or HTTP client), optional JSON parsing.
- **Workspace**: Assumes `ENGINE_REGISTRY.yaml` at `/<workspace>` (or equivalent) mapping engine names to ports.

## Procedure

### 1. Load Engine Registry
Read the YAML registry to obtain a list of engines and their assigned ports.

```bash
# Example using Python (can be adapted to shell)
python3 -c "
import yaml, sys
with open('/<workspace>') as f:
    data = yaml.safe_load(f)
for entry in data:
    port = entry.get('port')
    name = entry.get('engine_name', 'unknown')
    if port:
        print(f'{name}:{port}')
"
```

### 2. Verify Basic Health (`/health`)
For each engine, query `http://127.0.0.1:<port>/health` and expect JSON with `"status":"ok"` (or equivalent healthy indicator).

```bash
curl -s -m 3 http://127.0.0.1:<port>/health
```

- If the response is not valid JSON or does not indicate health, mark the engine as **DOWN**.
- Record status for reporting.

### 3. Verify Layer 4 Endpoint (`/v1/layers`)
Query `http://127.0.0.1:<port>/v1/layers` and ensure a JSON response is returned (any valid JSON indicates the endpoint is live).

```bash
curl -s -m 3 http://127.0.0.1:<port>/v1/layers
```

- If the endpoint fails to respond or returns non‑JSON, Layer 4 is **not mounted**.
- If responding, inspect the JSON for Layer 4 status:
  - `"status": "not_configured"` indicates a stub (Layer 4 file present but not active).
  - Any other status (or rich data like `"institutions"`, `"personalities"`, `"model_routes"`) indicates a **live, configured** Layer 4.

### 4. Assess Layer 4 Quality (Optional)
To differentiate between a minimal live Layer 4 and a richly configured one, check for depth fields:

```bash
curl -s -m 3 http://127.0.0.1:<port>/v1/layers | python3 -m json.tool
```

Look for keys such as `institutions`, `personalities`, `model_routes`, `sub_agent_pools`. Presence of these with non‑zero values indicates a fully instantiated methodology layer.

### 5. Reporting
Compile results into a summary:

- **Total engines**: count from registry.
- **UP engines**: those with healthy `/health`.
- **Layer 4 live**: those with valid JSON on `/v1/layers`.
- **Layer 4 configured**: those where Layer 4 JSON indicates active methodology (not `not_configured`).
- **Layer 4 rich**: those with depth fields.

### Example Output (Markdown)

```markdown
## Engine Fleet Health Audit

- **Total engines**: 38
- **UP (`/health=ok`)**: 38 (100%)
- **Layer 4 live (`/v1/layers` JSON)**: 38 (100%)
- **Layer 4 configured (not stub)**: 38 (100%)
- **Layer 4 rich (institutions+personalities)**: 20+ (varies per engine)
```

## Notes

- The `/health` endpoint implicitly confirms Layers 1‑3 (physics) are functional because the engine must be running to serve it.
- The `/v1/layers` endpoint is mounted by the shared `methodology_api.py`; a live response proves Layer 4 is integrated.
- Engines sharing a port (e.g., legacy Seed and Reproductive on 8090) are counted separately by name but share the same health/Layer 4 status.
- This procedure can be automated via a script (see `scripts/engine_fleet_audit.py` if available) or executed ad‑hoc for troubleshooting.

## Related References

- `ENGINE_REGISTRY.yaml` – source of engine‑to‑port mapping.
- `ds-engine-shared/methodology_api.py` – Layer 4 mounting logic.
- Individual engine methodology implementations (e.g., `ds-*-engine/src/*/core/methodology.py`).