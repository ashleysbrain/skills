# Engine Registry Patterns (Morphogen)

## Overview
Morphogen Engine (port 8093) acts as the skeletal/registry system for the AI organism. All engines register themselves here for discovery and health monitoring.

## Registration Endpoint
```bash
POST http://127.0.0.1:port/genotypes/register
Content-Type: application/json
```

## Registration Payload Schema
```json
{
  "engine_id": "string",           // Unique identifier (e.g., "bernard", "wave")
  "name": "string",                // Display name (e.g., "Bernard Engine (Clinical Diagnostic)")
  "version": "string",             // Engine version (e.g., "1.0.0")
  "body_system": "string",         // Body system name (e.g., "clinical_diagnostic")
  "scientist": "string",           // Scientist namesake (e.g., "Claude_Bernard")
  "port": "integer",               // Engine port (e.g., 8094)
  "capabilities": [                // Array of capability objects
    {"name": "string", "version": "string"}
  ],
  "metadata": {                    // Optional metadata
    "agent_name": "string",
    "description": "string"
  }
}
```

## Example Registrations

### Bernard (Clinical Diagnostic)
```json
{
  "engine_id": "bernard",
  "name": "Bernard Engine (Clinical Diagnostic)",
  "version": "1.0.0",
  "body_system": "clinical_diagnostic",
  "scientist": "Claude_Bernard",
  "port": 8094,
  "capabilities": [
    {"name": "clinical_diagnosis", "version": "1.0"},
    {"name": "rounds", "version": "1.0"},
    {"name": "differential_diagnosis", "version": "1.0"},
    {"name": "vitals_monitoring", "version": "1.0"},
    {"name": "soap_notes", "version": "1.0"},
    {"name": "credential_management", "version": "1.0"}
  ],
  "metadata": {"agent_name": "the specialist engine", "description": "AI Organism Attending AI Physician"}
}
```

### Morphogen Self-Registration
```json
{
  "engine_id": "morphogen",
  "name": "Morphogen Engine (Skeletal/Registry)",
  "version": "1.0.0",
  "body_system": "skeletal_registry",
  "scientist": "Paxton",
  "port": 8093,
  "capabilities": [
    {"name": "genotype_registry", "version": "1.0"},
    {"name": "bmp_gradient", "version": "1.0"},
    {"name": "morphogen_field", "version": "1.0"}
  ],
  "metadata": {"agent_name": "the specialist engine", "description": "Skeletal structure & genotype registry"}
}
```

## Querying the Registry

### Organism Map
```bash
GET http://127.0.0.1:port/organism/map
```

Response:
```json
{
  "engines": {
    "wave": {
      "name": "Wave Engine",
      "body_system": "brain_cns",
      "scientist": "Kuramoto",
      "port": 8000,
      "capabilities": ["coaching", "mastermind", "resonance"],
      "status": "healthy",
      "last_heartbeat": "2026-06-13T20:09:30.058549"
    },
    ...
  },
  "total_engines": 7,
  "systems_covered": 7
}
```

## Health Check Pattern
```bash
# Check all engines
for port in 8000 8089 8090 8091 8092 8093 8094; do
  curl -s http://127.0.0.1:$port/health | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Port {port}: {d.get(\"engine\",d.get(\"name\"))} | {d.get(\"status\",\"ok\")}')"
done
```

## Re-registration After Restart
After Morphogen restarts, all engines must re-register. Use a script:
```bash
#!/bin/bash
# register_all_engines.sh
curl -s -X POST http://127.0.0.1:port/genotypes/register -H "Content-Type: application/json" -d '{"engine_id":"wave",...}'
curl -s -X POST http://127.0.0.1:port/genotypes/register -H "Content-Type: application/json" -d '{"engine_id":"quartz",...}'
# ... etc for all 7 engines
```

## Registry Status Codes
| Field | Values |
|-------|--------|
| `status` | "healthy", "unhealthy", "degraded" |
| `last_heartbeat` | ISO 8601 timestamp |
| `total_engines` | Integer count |
| `systems_covered` | Integer count |

## Best Practices
1. **Register immediately after engine starts** — use startup script
2. **Heartbeat updates automatically** — Morphogen polls engines
3. **Re-register on Morphogen restart** — engines must re-register
4. **Use consistent engine_id** — matches the operator agent profile names
4. **Monitor `last_heartbeat`** — stale = engine down