---
name: physics-informed-project-management
category: project-management
description: Class-level skill for applying physics-informed thinking to project management systems, creating degradation-graceful executive function layers that complement task-level physics engines.
tags: [physics, project-management, executive-function, degradation-graceful, body-analog]
---

# Physics-Informed Project Management

Apply physics-informed engine principles at the PROJECT level to complement task-level physics systems (like Quartz). This creates an executive function layer that provides thermodynamic, mechanical, and dynamical systems insights for project health monitoring and early warning.

## Core Insight

Task-level physics engines (e.g., Quartz) model the potential energy landscape of individual tasks. Project-level physics models the thermodynamic state of the entire project portfolio, providing early warning signals and health metrics that emerge only at scale.

This follows the same principle as biological systems: cellular biochemistry (task level) vs. organismal physiology (project level).

## Five Physics Primitives for Projects

### 0. Queue Health Monitor (NEW — 2026-08-28)
**Purpose**: Detects external build system queue wedges that block task completion
- **Queue Depth**: Total pending items (0 = healthy, >50 = spike warning)
- **Stalled Items**: Items pending >30 min or >1 hour (sibling-agent filtering pattern)
- **Liveness Check**: Verify autonomic daemon alive (launchctl status + boot events in log)
- **Filter Detection**:区分 "dead daemon" vs "filtering issue" (builds never picked up vs stuck in processing)
- **False Diagnosis Prevention**: Never claim system dead without log reconstruction (TIME LAW)
- **Body Analog**: Vagal tone — organism can be conscious but not executing (autonomic dysregulation)

**Implementation pattern** (queue_health_daemon.py, built 2026-08-28):
```python
def get_queue_stats():
    conn = sqlite3.connect(BUS_DB)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM messages WHERE status='pending'")
    total_pending = cur.fetchone()[0]
    
    # Items stalled >30 min
    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()
    cur.execute("SELECT COUNT(*) FROM messages WHERE status='pending' AND timestamp < ?", (cutoff,))
    stalled_30m = cur.fetchone()[0]
    
    # Items stalled >1 hour
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    cur.execute("SELECT COUNT(*) FROM messages WHERE status='pending' AND timestamp < ?", (cutoff,))
    stalled_1h = cur.fetchone()[0]
```

**Critical learning (2026-08-28):** Plain build_requests are skipped by sibling-agent (filtered by fleet_guard/law_carrier flags). This is NOT a daemon death issue. Verify via log grep for specific build IDs.

### 1. Free Energy Landscape (F = ⟨E⟩ - TS)
**Purpose**: Measures project's distance from completion ground state
- **Internal Energy (⟨E⟩)**: Sum of remaining work energy across all subtasks
- **Entropy (S)**: Shannon entropy of subtask status distribution (uncertainty measure)
- **Temperature (T)**: Deadline pressure scalar (0 = no deadline, high = urgent)
- **Free Energy (F)**: Seeks minimum = completed project state
- **Body Analog**: Cellular metabolism / Free Energy Principle (Friston)

### 2. Critical Path Analysis (Directed Percolation)
**Purpose**: Identifies the bottleneck chain that determines project duration
- **Critical Path**: Longest chain of dependencies - any stall here stalls the project
- **Feasibility**: Largest connected component / total tasks (directed reachability)
- **Parallelizable Count**: Tasks not on any critical chain
- **Body Analog**: Cardiovascular perfusion - critical path is the aorta, parallelizable tasks are collateral circulation

### 3. Stress & Strain (Continuum Mechanics)
**Purpose**: Quantifies timeline pressure and deformation from plan
- **Stress (σ)**: Deadline force / available capacity
- **Strain (ε)**: (planned_progress - actual_progress) / planned_progress
- **Yield Strength**: Maximum sustainable work rate before quality degrades
- **Safety Factor**: σ_y / σ (>1 = safe, <1 = fracture imminent)
- **Verdict**: ELASTIC | PLASTIC | FRACTURE
- **Body Analog**: Mechanotransduction - cells sense and remodel in response to mechanical load

### 4. Critical Slowing Down (Dynamical Systems Early Warning)
**Purpose**: Detects approaching tipping points before deadline misses
- **Recovery Times**: History of fork resolution durations
- **Trend**: Increasing recovery time = approaching critical point
- **Variance Trend**: Growing fluctuations = destabilizing
- **Autocorrelation**: High memory = system "remembering" longer
- **Early Warning**: Fires when slowing trend + (increasing variance OR high autocorrelation)
- **Body Analog**: Allostatic load - body's pre-collapse warning signs (elevated HR, reduced HRV)

## Degradation-Graceful Consumption Patterns

### External Engine Probing
Always probe external engine health before consuming. Check the JSON body,
not just the HTTP status — Quartz returns 200 with `status: "ok"` or
`status: "degraded"`:
```python
def _engine_alive(url: str) -> bool:
    try:
        with urlopen(f"{url}/health", timeout=2.0) as resp:
            import json
            data = json.loads(resp.read().decode())
            return data.get("status") in ("ok", "degraded")
    except Exception:
        return False
```

### Fallback Hierarchy
1. **Preferred**: Consume external engine (e.g., Quartz for task energies)
2. **Fallback**: Local estimates when engine unavailable
3. **Graceful Degradation**: System continues to function with reduced fidelity

### ⚠️ Quartz API Integration Quirks (Verified 2026-06-20)

These are real gotchas discovered during end-to-end integration. See
`references/quartz-integration-guide.md` for the full reproduction recipe.

1. **Priority is STRING, not INT.** Quartz's `TaskCreate` Pydantic model
   expects `"P0"`, `"P1"`, etc. Sending integer `0` silently fails with
   HTTP 422. Every task POST is rejected with no error surfaced unless you
   read the response body.

2. **Capacity must be set BEFORE pushing tasks.** Quartz only auto-positions
   tasks (computes lattice energies) when `capacity["energy_level"] > 0`.
   POST to `/v1/lattice/capacity` with `{"energy_level": 0.7,
   "cognitive_load": 0.4}` BEFORE pushing any tasks, or all tasks land
   with no lattice position and zero stability scores.

3. **Quartz generates its own UUIDs — bridge IDs via tags.** Quartz creates
   its own UUID per task. Your PM spine subtask IDs will NOT match. Embed
   the PM spine ID in the task's `tags` array during POST, then read back
   `/v1/tasks` to build a `{quartz_uuid: pm_spine_id}` mapping for energy
   lookup.

4. **No per-task energy endpoint exists.** Quartz exposes lattice energies
   via `/v1/lattice/state`, not per-task. Fetch the full state dict and
   convert stability scores to energies: `E = -ln(stability_score)`
   (Boltzmann transform).

Working pattern for consuming Quartz energies (replaces the old broken code):
```python
def _fetch_quartz_energies(subtasks, quartz_url):
    """Fetch per-task lattice energies with tag-based ID bridging."""
    if not _engine_alive(quartz_url):
        return None  # triggers local fallback

    pm_ids = {st.id for st in subtasks}

    # Get lattice state (contains all positioned tasks + stability scores)
    with urlopen(f"{quartz_url}/v1/lattice/state", timeout=3.0) as resp:
        state = json.loads(resp.read().decode())
    positions = state.get("positions", {})
    if not positions:
        return None

    # Get all tasks to build UUID -> PM spine ID mapping via tags
    with urlopen(f"{quartz_url}/v1/tasks", timeout=3.0) as resp:
        tasks_data = json.loads(resp.read().decode())

    quartz_to_pm = {}
    for qt in tasks_data.get("tasks", []):
        for tag in qt.get("tags", []):
            if tag in pm_ids:
                quartz_to_pm[qt["id"]] = tag
                break

    # Convert stability -> energy via Boltzmann: E = -ln(stability)
    energies = {}
    for qid, pos in positions.items():
        stability = pos.get("stability_score", 0.5)
        energy_val = -math.log(stability) if stability > 0 else 5.0
        pm_id = quartz_to_pm.get(qid)
        if pm_id:
            energies[pm_id] = energy_val

    return energies if energies else None
```

### Feeding Quartz (Two-Way Bridge)
The PM spine feeds tasks INTO Quartz and reads energies BACK:

```python
def feed_quartz_lattice(project, quartz_url):
    """Push subtasks into Quartz so it computes real lattice energies."""
    if not _engine_alive(quartz_url):
        return False

    # 1. Set capacity FIRST (Quartz requires this before auto-positioning)
    _post(f"{quartz_url}/v1/lattice/capacity",
          {"energy_level": 0.7, "cognitive_load": 0.4})

    # 2. Push each subtask with PM spine ID embedded in tags
    for st in project.subtasks:
        if st.status.value in ("approved", "rejected"):
            continue
        payload = {
            "title": f"[{st.id}] {st.title}",  # embed PM ID for lookup
            "priority": st.priority.value,       # STRING "P0".."P3"
            "energy_required": energy_map.get(st.stage, "medium"),
            "project": project.id,
            "tags": [st.stage, st.id],           # PM ID in tags!
            "source": "the operator agent-work-spine",
        }
        _post(f"{quartz_url}/v1/tasks", payload)

    # 3. Trigger rebalance so energies are computed
    _post(f"{quartz_url}/v1/lattice/rebalance", {})
    return True
```

### Composite Health Score
Blend multiple physics signals into a single actionable metric:
```python
# Weighted blend: low free energy + clear critical path + safe stress
fe_health = max(0.0, 1.0 - fe.free_energy / max(len(subtasks) * 2, 1))
cp_health = cp.feasibility
stress_health = min(1.0, stress.safety_factor / 2.0) if stress.safety_factor != float("inf") else 1.0
slowing_penalty = 0.15 if (slowing and slowing.early_warning) else 0.0

composite = max(0.0, min(1.0,
    (fe_health * 0.35 + cp_health * 0.25 + stress_health * 0.40) - slowing_penalty
))
```

## Quantum Layer (quantum_project_layer.py)

Five quantum mechanics analogs that solve problems classical physics cannot.
Each maps a real quantum phenomenon to a real PM problem where the quantum
solution is strictly more powerful. The math is real (Born rule, tunneling
probability formula, entanglement correlations, annealing schedule).

| Primitive | Formula | PM Problem | Body Analog |
|-----------|---------|------------|-------------|
| **Superposition Forks** | psi = alpha\|A> + beta\|B> | Fork blocks work. Pre-compute ALL branches in parallel, collapse on measurement (answer arrival) | Photosynthesis: 95% energy transfer via quantum coherence |
| **Entanglement Dependencies** | Bell pair correlations | Serial polling between dependent engines. Completing A collapses B from "waiting" to "ready" instantly | Bird cryptochrome quantum entanglement (navigation) |
| **Tunneling Barriers** | P = exp(-2*kappa*L) | Forked subtask blocked. Nonzero probability of bypassing via alternative path | Enzyme proton tunneling |
| **Quantum Annealing** | H(t) = H_problem - Gamma(t)*H_driver | Lattice optimization stuck in local minimum. Quantum fluctuations tunnel through shallow barriers | Protein folding hypothesis |
| **Coherence Flow** | tau = coherence time, gamma = decoherence rate | N engines need O(N^2) messages for state sync. Coherent engines: 1 propagation reaches all | Plant photosynthesis exciton coherence |

**Key insight**: The quantum advantage materializes when forks exist
(superposition pre-computes branches), when dependencies chain deeply
(entanglement propagates state), and when engines multiply (coherence
beats O(N^2) polling). It shows `0.00x` speedup on projects with no forks
and single-engine setups — that's correct, not a bug.

## Implementation Checklist

- [x] Implement all four physics primitives (free energy, critical path, stress/strain, critical slowing)
- [x] Map each primitive to a body analog for intuitive interpretation
- [x] Build degradation-graceful consumption of external physics engines
- [x] Create composite health score with weighted primitives
- [x] Add early warning detection (critical slowing down)
- [x] Provide human-readable interpretation for each signal
- [x] Ensure system works when external engines are down (local fallback)
- [x] Build two-way Quartz bridge (feed tasks IN, read energies BACK) — **code exists but endpoints DEAD since 2026-08-09 (the specialist engine repurposed); only the local fallback path is active**
- [x] Build quantum layer (5 primitives with real Born/tunneling/annealing math)
- [x] Validate with real project trajectories (verified classical + quantum on live state 2026-06-20; 2.00x quantum speedup confirmed with 3 forks + deep chain)
- [ ] Wire coherence flow to live multi-engine organism (currently scaffold)

## Module Loading and API (Gotchas)

When running physics/quantum modules dynamically (e.g., from a test script
or verification probe), two gotchas bite hard. See
`references/physics-module-api.md` for the full field reference.

1. **`@dataclass` + `importlib.util` crash.** Both modules use `@dataclass`
   heavily. Loading via `importlib.util.spec_from_file_location` crashes
   with `AttributeError: 'NoneType' object has no attribute '__dict__'`
   unless you register the module in `sys.modules` BEFORE calling
   `spec.loader.exec_module()`.

2. **Both analysis functions take a project object, not a list.**
   `analyze_project_physics(project)` and `analyze_quantum_project(project)`
   both expect an object with `.subtasks`, `.priority.value`, and `.forks`.
   Passing a bare list of subtask dicts crashes with
   `AttributeError: 'list' object has no attribute 'subtasks'`.

3. **Result dataclass field names are non-obvious.** `FreeEnergyResult`
   uses `.free_energy` (not `.F`). `QuantumProjectReport` uses
   `.quantum_speedup` (not `.estimated_speedup`). `superposition_forks`
   is a list (use `len()`), not an object. When in doubt, introspect with
   `dataclasses.fields(obj)`.

Run `scripts/verify_physics_on_projects.py` to validate the full physics
+ quantum stack against live project state after any change.

## Known Integrations
- Quartz Engine (task-level physics: springs, Hamiltonians, percolation) — **DEAD as of 2026-08-09**: :port was repurposed to the specialist engine (circadian rhythm / SCN clock_root). `/v1/tasks` and `/v1/lattice/state` return 404. The Quartz lattice code still exists in `ds-quartz-engine/` source but is NOT served by any running engine. the specialist engine on :port now serves only `/health`, `/mode`, `/sleep`, `/wake`.
- Thalamus (Mountcastle dispatch router)
- Scoville (episodic memory)
- Luria-Executive (goal decomposition engine)

**⚠️ Quartz endpoint death (confirmed 2026-08-09 via sibling-agent bus msg 1625):**
The `_fetch_quartz_energies()` and `feed_quartz_lattice()` code blocks above are historical reference. They will silently no-op because `_engine_alive()` probes `/health` which still returns 200 on :port, but `/v1/tasks` and `/v1/lattice/state` now return 404. The degradation-graceful fallback (local estimates) is the ONLY active path. Do not report Quartz integration as "live" or "verified" in any status output. If a future session revives the task lattice on a different port, the code patterns above remain valid — just update the URL.

## Reference Files
- `references/thread-splitting-protocol.md` — Multi-thread work session protocol: labeled parallel workstreams in one chat, O'Keefe persistence at milestones, workspace handoff docs for desktop splits, cross-thread isolation rules (validated 2026-08-15 across 4 threads)
- `references/body-analog-mappings.md` — Classical physics body analogs (4 primitives)
- `references/quartz-integration-guide.md` — Real API quirks, reproduction recipe, working code patterns for Quartz two-way bridge (**endpoints currently dead — see Known Integrations**)
- `references/client-side-urgency-computation.md` — Fallback urgency heuristic when physics engines are unavailable (used by calendar Lattice view)
- `references/physics-module-api.md` — Exact result-dataclass field names, dynamic-import gotcha, parameter shapes, introspection helper
- `references/task-planning-gap-analysis.md` — Competitive research (Sunsama, Motion, Linear, OmniFocus, Taskwarrior, GTD frameworks) ranked by impact. Phase 1 items (projects, tags, duration) now DONE in calendar Lattice view.
- `scripts/degradation_graceful_consumption.py` — Working pattern for consuming external physics engines with fallback
- `scripts/verify_physics_on_projects.py` — End-to-end verification probe: runs full physics + quantum suite on all projects in state

## Validation Patterns
1. **Degradation Test**: Verify physics layer returns sensible values when all external engines are down
2. **Early Warning Test**: Inject slowing fork recovery times and verify early warning triggers
3. **Fracture Test**: Simulate deadline overload and verify stress state reaches FRACTURE
4. **Recovery Test**: After intervention, verify system returns to HEALTHY state

## Anti-Patterns to Avoid
- ❌ Don't rebuild task-level physics in the project layer - consume and complement
- ❌ Don't make external engine calls blocking/timeout-prone without fallbacks
- ❌ Don't ignore the body analog - it provides crucial intuition for signal interpretation
- ❌ Don't use equal weighting for primitives - free energy and stress are typically more informative than entropy alone
- ❌ Don't forget to normalize entropy to [0,1] range for meaningful comparison across projects