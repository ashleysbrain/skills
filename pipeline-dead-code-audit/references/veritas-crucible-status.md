# VERITAS + CRUCIBLE Pipeline Status (2026-08-06)

## File Inventory
- `veritas_process.py` (~3,212 lines) — 12-stage academic pipeline
- `crucible_process.py` (~3,210 lines) — 12-stage technology pipeline
- `pipeline_api.py` (266 lines) — FastAPI wrapper on :port
- `research_discovery.py` (304 lines) — Stage -1 discovery engine
- `field_evolution_tracker.py` (311 lines) — Weekly YAML updater
- `veritas_field_knowledge.yaml` / `crucible_field_knowledge.yaml` — Externalized configs
- `pipeline_user_profile_schema.json` — JSON schema for user profiles

## Key Patterns
- YAML config loading: `_fk.get("key", hardcoded_fallback)` pattern
- API compatibility: alias classes (VeritasPipeline extends VeritasProcess)
- CircuitBreaker: wired into engine_post (is_open before, record after)
- SLA tracking: record_stage_time in run loop, printed with each stage
- User fine-tuning: _update_user_profile() writes persistent JSON after each run

## Engine Set (14, identical in both pipelines)
andreasen, bell, friston, gazzaniga, goethe, harvey, humboldt, ito, kuramoto, luria, okeefe, popper, sherrington, wernicke

## API Endpoints (:port)
- POST /api/veritas/run, /api/crucible/run
- GET /api/veritas/status/{id}, /api/crucible/status/{id}
- GET /api/veritas/profile, /api/crucible/profile
- GET /api/veritas/field-evolution, /api/crucible/field-evolution
- GET /api/discover/{pipeline}?top=10
- GET /api/pipelines/health, /api/pipelines/runs

## CRITICAL
- System python3 has broken pydantic_core. Use `/<workspace>`
- Operator bus DB is at workspace root `message-bus.db`, NOT `organism/config/operator_bus.db`
- Semantic Scholar returns 429 frequently. Retry with 3+5*n second backoff.
