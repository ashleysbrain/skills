# Physics Module API Reference

Exact field names and usage patterns for `project_physics.py` and
`quantum_project_layer.py`. Verified against live module source on 2026-06-20.

This exists because the result dataclasses use names that are NOT obvious
from the conceptual documentation. Guessing attribute names wastes time.

## Dynamic Import Gotcha (CRITICAL)

Both modules use `@dataclass` heavily. When loading them dynamically via
`importlib.util`, you MUST register the module in `sys.modules` BEFORE
calling `spec.loader.exec_module()`:

```python
import importlib.util, sys

def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # MUST do this BEFORE exec_module
    spec.loader.exec_module(mod)
    return mod

pp  = load_mod('project_physics', 'project_physics.py')
qpl = load_mod('quantum_project_layer', 'quantum_project_layer.py')
```

If you skip the `sys.modules[name] = mod` line, the `@dataclass` decorator
inside the module crashes with:

```
AttributeError: 'NoneType' object has no attribute '__dict__'
```

This happens because Python's dataclass machinery calls
`sys.modules.get(cls.__module__).__dict__` during class processing, and the
module isn't registered yet.

## Parameter Shapes (Common Confusion)

Both `analyze_project_physics()` and `analyze_quantum_project()` take a
**project object**, NOT a list of subtask dicts.

```python
# CORRECT — pass a project with .subtasks, .priority, .forks
report = pp.analyze_project_physics(project)
qrep  = qpl.analyze_quantum_project(project)

# WRONG — this crashes with AttributeError: 'list' object has no attribute 'subtasks'
report = pp.analyze_project_physics(list_of_subtask_dicts)
```

The project object must expose:
- `.subtasks` — list of subtask objects (each with `.id`, `.title`, `.stage`,
  `.status.value`, `.dependencies`, `.acceptance_criteria`, `.fork_question`)
- `.priority.value` — string like `"P0"`, `"P1"`, etc.
- `.forks` — list of fork objects (each with `.subtask_id`, `.question`, `.answered`)
- `.forks_history` — optional, list of dicts for critical-slowing analysis

## project_physics.py — Result Dataclasses

### FreeEnergyResult

| Field | Type | Description |
|-------|------|-------------|
| `internal_energy` | float | `<E>` = sum of remaining work energy across subtasks |
| `entropy` | float | Shannon entropy of status distribution |
| `temperature` | float | T = deadline pressure scalar (derived from priority) |
| `free_energy` | float | **`F = <E> - T*S`** (NOT `.F` — use `.free_energy`) |
| `normalized_entropy` | float | S normalized to [0, 1] |
| `interpretation` | str | Human-readable description |
| `body_analog` | str | Default: `"Cellular metabolism — ATP budget vs. entropy"` |

### CriticalPathResult

| Field | Type | Description |
|-------|------|-------------|
| `critical_path_length` | int | Longest dependency chain depth |
| `feasibility` | float | Largest connected component / total tasks |
| `parallelizable_count` | int | Tasks NOT on any critical chain |
| `bottleneck_task_id` | str / None | The task that is the chokepoint |

### StressStrainResult

| Field | Type | Description |
|-------|------|-------------|
| `stress` | float | Deadline force / available capacity |
| `strain` | float | `(planned_progress - actual_progress) / planned_progress` |
| `safety_factor` | float | Yield strength / stress (>1 = safe) |
| `verdict` | `StressVerdict` enum | `ELASTIC`, `PLASTIC`, or `FRACTURE` — access via `.verdict.name` |

### CriticalSlowingResult

| Field | Type | Description |
|-------|------|-------------|
| `early_warning` | bool | True if slowing trend detected |
| `recovery_time_trend` | str | `"increasing"`, `"stable"`, or `"decreasing"` |
| `variance_trend` | str | Variance direction |
| `autocorrelation` | float | Memory in the system |

### ProjectPhysicsReport (composite)

| Field | Type | Description |
|-------|------|-------------|
| `free_energy` | `FreeEnergyResult` | |
| `critical_path` | `CriticalPathResult` | |
| `stress_strain` | `StressStrainResult` | |
| `critical_slowing` | `CriticalSlowingResult` | |
| `composite_health` | float | Weighted blend: FE 35% + CP 25% + SS 40% - slowing penalty 15% |
| `verdict` | str | `"HEALTHY"` (>0.75), `"PROGRESSING"` (>0.5), `"AT_RISK"` (>0.3), `"CRITICAL"` (<0.3) |

## quantum_project_layer.py — Result Dataclasses

### QuantumProjectReport

| Field | Type | Description |
|-------|------|-------------|
| `superposition_forks` | `List[QuantumFork]` | NOT an object — it's a **list**. Use `len()` for count. |
| `entanglement_graph` | `EntanglementGraph` | Does NOT have `.entangled_pairs` — inspect via dataclass fields |
| `tunneling_events` | `List[TunnelingEvent]` | Barrier bypass events |
| `annealing_schedule` | `AnnealingSchedule` / None | Present when lattice optimization needed |
| `coherence` | `CoherenceState` | Has `.efficiency`, `.classical_message_cost`, `.quantum_propagations` |
| `quantum_speedup` | float | NOT `.estimated_speedup` — use `.quantum_speedup` |
| `interpretation` | str | Full human-readable summary |

### CoherenceState

| Field | Type | Description |
|-------|------|-------------|
| `engine_states` | Dict | Per-engine state dict |
| `last_sync` | Dict | Per-engine last sync timestamps |
| `coherence_time_hours` | float | Default 1.0 |
| `decoherence_rate` | float | Default 0.1 |
| `classical_message_cost` | int | O(N^2) message count |
| `quantum_propagations` | int | O(N) or O(1) propagation count |
| `efficiency` | float | `classical_cost / quantum_cost` |

### QuantumFork

| Field | Type | Description |
|-------|------|-------------|
| `subtask_id` | str | |
| `question` | str | |
| (amplitudes) | float | Named differently than `amplitude_A`/`amplitude_B` — check fields via `dataclasses.fields()` |

## Quantum Speedup Behavior

The quantum speedup is **context-dependent** — this is correct, not a bug:

- **0 forks, single engine**: `quantum_speedup = 0.00x` — no parallelism to exploit
- **3 forks, deep dependency chain**: `quantum_speedup = 2.00x` — verified
- **N coupled engines**: coherence efficiency scales as `N*(N-1) / quantum_propagations`

To demonstrate quantum advantage, construct a test project with:
1. At least 2-3 forks (unanswered questions with `.answered = False`)
2. A deep dependency chain (A -> B -> C -> D -> E)
3. Multiple parallelizable branches

A project with zero forks will always show 0.00x — the quantum layer
correctly reports no advantage when there's nothing to parallelize.

## Introspection Helper

When unsure of field names, use Python introspection:

```python
import dataclasses

obj = qrep.entanglement_graph  # or any result object
if dataclasses.is_dataclass(obj):
    for f in dataclasses.fields(obj):
        print(f"  {f.name}: {f.type}")
```
