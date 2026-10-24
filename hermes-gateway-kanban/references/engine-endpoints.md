# Standard Engine Endpoints (from Divinity Science session)

## Engine Fleet Endpoint Map

| Engine ID | Port | Body System | Agent | Health Endpoint | Key Capabilities |
|---|---|---|---|---|---|
| **morphogen** | 8093 | Skeletal/Registry | the specialist engine | `/health` | `/genotypes`, `/organism/map`, `/gradients` |
| **wave** | 8000 | Brain/CNS | the specialist engine | `/health` | `/coach`, `/resonance`, `/mastermind` |
| **quartz** | 8089 | Autonomic NS | the specialist engine | `/health` | `/tasks`, `/lattice`, `/pid`, `/healing` |
| **seed** | 8090 | Endocrine/Growth | the specialist engine | `/health` | `/projects`, `/growth`, `/avrami`, `/critical-path` |
| **allostasis** | 8091 | Immune/Homeostatic | the specialist engine | `/health` | `/organism`, `/surveillance`, `/allostatic-load` |
| **harvey** | 8092 | Cardiovascular | the specialist engine | `/health` | `/fabric/vitals`, `/circulation`, `/comms` |
| **bernard** | 8094 | Clinical Diagnostic | the specialist engine | `/health` | `/rounds`, `/patient/vitals`, `/patient/summary`, `/scan`, `/health-systems` |

## Python Constant (for profile skills)

```python
ENGINE_ENDPOINTS = {
    "wave": "http://127.0.0.1:port",
    "quartz": "http://127.0.0.1:port",
    "seed": "http://127.0.0.1:port",
    "allostasis": "http://127.0.0.1:port",
    "harvey": "http://127.0.0.1:port",
    "morphogen": "http://127.0.0.1:port",
    "bernard": "http://127.0.0.1:port",
}
```

## Morphogen Registry Registration (for each engine)

```bash
# Wave
curl -X POST http://127.0.0.1:port/genotypes/register \
  -H "Content-Type: application/json" \
  -d '{"engine_id":"wave","name":"Wave Engine (Coaching)","version":"2.0.0","body_system":"neurological","scientist":"Yoshiki_Kuramoto","port":port,"capabilities":[{"name":"coaching","version":"2.0"},{"name":"resonance","version":"2.0"},{"name":"mastermind","version":"2.0"}],"metadata":{"agent_name":"the specialist engine","description":"Brain/CNS - Coaching & Resonance"}}'

# Quartz
curl -X POST http://127.0.0.1:port/genotypes/register \
  -H "Content-Type: application/json" \
  -d '{"engine_id":"quartz","name":"Quartz Engine (Crystal Lattice)","version":"2.0.0","body_system":"autonomic","scientist":"Peter_Sterling","port":port,"capabilities":[{"name":"lattice","version":"2.0"},{"name":"pid_control","version":"2.0"},{"name":"task_management","version":"2.0"},{"name":"self_healing","version":"2.0"}],"metadata":{"agent_name":"the specialist engine","description":"Autonomic NS - PID Control & Tasks"}}'

# Seed
curl -X POST http://127.0.0.1:port/genotypes/register \
  -H "Content-Type: application/json" \
  -d '{"engine_id":"seed","name":"Seed Engine (Product Development)","version":"2.0.0","body_system":"endocrine","scientist":"Conrad_Waddington","port":port,"capabilities":[{"name":"product_development","version":"2.0"},{"name":"avrami_jmak","version":"2.0"},{"name":"landau_theory","version":"2.0"},{"name":"critical_path","version":"2.0"}],"metadata":{"agent_name":"the specialist engine","description":"Endocrine/Growth - Product Dev"}}'

# Harvey
curl -X POST http://127.0.0.1:port/genotypes/register \
  -H "Content-Type: application/json" \
  -d '{"engine_id":"harvey","name":"Harvey Engine (Circulation)","version":"1.0.0","body_system":"cardiovascular","scientist":"William_Harvey","port":port,"capabilities":[{"name":"circulation","version":"1.0"},{"name":"message_fabric","version":"1.0"},{"name":"inter_engine_comms","version":"1.0"}],"metadata":{"agent_name":"the specialist engine","description":"Cardiovascular - Circulation & Comms"}}'

# Bernard (Clinical Diagnostic)
curl -X POST http://127.0.0.1:port/genotypes/register \
  -H "Content-Type: application/json" \
  -d '{"engine_id":"bernard","name":"Bernard Engine (Clinical Diagnostic)","version":"1.0.0","body_system":"clinical_diagnostic","scientist":"Claude_Bernard","port":port,"capabilities":[{"name":"clinical_diagnosis","version":"1.0"},{"name":"rounds","version":"1.0"},{"name":"differential_diagnosis","version":"1.0"},{"name":"vitals_monitoring","version":"1.0"},{"name":"soap_notes","version":"1.0"},{"name":"credential_management","version":"1.0"},{"name":"evidence_synthesis","version":"1.0"},{"name":"health_system_modeling","version":"1.0"}],"metadata":{"agent_name":"the specialist engine","description":"Clinical Diagnostic - AI Organism Attending Physician"}}'
```

## Health Check Verification

```bash
# Check all engines
for port in 8000 8089 8090 8091 8092 8093 8094; do
  echo "=== Port $port ==="
  curl -s http://127.0.0.1:$port/health | jq '.engine // .status'
done

# Verify Morphogen registry
curl -s http://127.0.0.1:port/organism/map | jq '.engines | keys'
```