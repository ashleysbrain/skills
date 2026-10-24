# Quartz Engine Integration Guide

Verified integration patterns for consuming the the specialist engine lattice engine
from a project-management physics layer. All patterns confirmed end-to-end
on 2026-06-20 against Quartz v2.0.0 on port 8089.

## Engine Endpoints (Verified)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check. Returns JSON with `status: "ok"` or `"degraded"`. Check body, not just status code. |
| `/v1/sessions` | POST | Create a session (optional — default_user lattice works without) |
| `/v1/tasks` | POST | Create a task. **Priority must be STRING `"P0"`, not INT `0`** |
| `/v1/tasks` | GET | List all tasks. Returns `{"tasks": [...], "count": N}` |
| `/v1/lattice/capacity` | POST | Set energy_level and cognitive_load. **Must be called before tasks will auto-position** |
| `/v1/lattice/state` | GET | Full lattice state: positions, stability scores, coupling, capacity |
| `/v1/lattice/rebalance` | POST | Trigger lattice rebalance (recomputes all stability scores) |

## Three Critical API Quirks

### Quirk 1: Priority Type Mismatch (Silent 422)

**Bug**: Sending `priority: 0` (integer) to `/v1/tasks` returns HTTP 422
Validation Error. Pydantic rejects it silently — the task is never created.

**Root cause**: Quartz's `TaskCreate(BaseModel)` declares:
```python
priority: str = "P2"  # expects STRING
```
But the PM spine was mapping `{"P0": 0, "P1": 1, ...}` and sending the int.

**Fix**: Send the priority STRING directly:
```python
payload["priority"] = st.priority.value  # "P0", "P1", "P2", "P3"
```

**Detection**: POST to `/v1/tasks`, then GET `/v1/tasks` — if count
didn't increase, tasks were rejected. Read response body for 422 detail.

### Quirk 2: Capacity Pre-Condition

**Bug**: Tasks POST successfully but `/v1/lattice/state` shows 0 positioned
tasks, meaning no stability scores or energies are computed.

**Root cause**: Quartz's `create_task` endpoint only calls
`add_task_to_lattice()` when:
```python
if lattice_engine.capacity["energy_level"] > 0 or lattice_engine.capacity["cognitive_load"] > 0:
    lattice_engine.add_task_to_lattice(...)
```
Default capacity is 0.0 for both, so tasks are added to the engine but
never positioned in the lattice.

**Fix**: POST to `/v1/lattice/capacity` BEFORE pushing any tasks:
```python
_post(f"{quartz_url}/v1/lattice/capacity",
      {"energy_level": 0.7, "cognitive_load": 0.4})
```

### Quirk 3: UUID Mismatch (ID Bridging)

**Bug**: Quartz generates its own UUID per task. Your PM spine subtask IDs
will NOT appear in `/v1/lattice/state`. Energy lookups by `st.id` return
nothing.

**Fix**: Embed the PM spine ID in the task's `tags` during POST:
```python
payload["tags"] = [st.stage, st.id]  # PM ID in tags
```
Then read `/v1/tasks` to build a `{quartz_uuid: pm_spine_id}` mapping.

## Energy Conversion (Boltzmann Transform)

Quartz stores `stability_score` per positioned task (0.0–1.0, higher =
more stable). To convert to energy for physics calculations:

```python
energy = -math.log(stability_score) if stability_score > 0 else 5.0
```

This is a Boltzmann transform: stable tasks (stability→1) have energy→0
(ground state), unstable tasks (stability→0) have high energy.

## Reproduction Recipe

1. Verify Quartz is alive: `GET http://127.0.0.1:port/health`
2. Set capacity: `POST /v1/lattice/capacity {"energy_level": 0.7, "cognitive_load": 0.4}`
3. Push tasks: `POST /v1/tasks` with priority as STRING and PM ID in tags
4. Trigger rebalance: `POST /v1/lattice/rebalance {}`
5. Read energies: `GET /v1/lattice/state` → positions → stability_score → E = -ln(S)
6. Bridge IDs: `GET /v1/tasks` → match tags to PM spine IDs

## Degradation-Graceful Pattern

```python
def _engine_alive(url):
    try:
        with urlopen(f"{url}/health", timeout=2.0) as resp:
            import json
            return json.loads(resp.read().decode()).get("status") in ("ok", "degraded")
    except Exception:
        return False

# When Quartz is down, physics layer falls back to local energy estimates:
# E_local = priority_weight * stage_penalty (no lattice coupling)
# When Quartz is up, uses real Boltzmann energies from stability scores
```

## File Locations

- Quartz engine source: `~/your-workspace/ds-quartz-engine/src/`
  - Lattice core: `src/lattice/core.py` (spring-coupled Hamiltonian)
  - Free energy: `src/healing/free_energy.py` (Friston FEP, variational Bayes)
  - Shannon entropy: `src/entropy/shannon.py` (clarity index)
  - Percolation: `src/entropy/percolation.py` (feasibility prediction)
  - API server: `src/api/server.py` (FastAPI endpoints)
- PM physics layer: `~/your-workspace/project_physics.py`
- Quantum layer: `~/your-workspace/quantum_project_layer.py`
- Work spine: `~/your-workspace/the operator agent-work-spine.py`
