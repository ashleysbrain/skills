#!/usr/bin/env python3
"""
End-to-end physics + quantum verification script.

Runs the full physics suite (classical + quantum) against all projects in
the work-spine state file. This is the verification probe — run it after
any change to the physics modules or project state to confirm everything
still computes correctly.

Usage:
    cd ~/your-workspace
    python3 skills-library/project-management/physics-informed-project-management/scripts/verify_physics_on_projects.py

Exit codes:
    0 — all projects computed successfully
    1 — one or more projects failed (error details printed)
    2 — modules or state file not found
"""
import importlib.util
import sys
import json
import dataclasses
from pathlib import Path

WORKSPACE = Path.home() / "your-workspace"
PHYSICS_PATH = WORKSPACE / "project_physics.py"
QUANTUM_PATH = WORKSPACE / "quantum_project_layer.py"
STATE_PATH = WORKSPACE / "kanban" / "work-spine-state.json"


def load_mod(name: str, path: Path):
    """Load a Python module by path, handling the dataclass/sys.modules gotcha."""
    if not path.exists():
        print(f"ERROR: {path} not found")
        sys.exit(2)
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # CRITICAL: register before exec_module
    spec.loader.exec_module(mod)
    return mod


class _Fork:
    def __init__(self, d):
        self.subtask_id = d.get("subtask_id", "")
        self.question = d.get("question", "")
        self.answered = d.get("answered", False)


class _Subtask:
    def __init__(self, d):
        self.id = d.get("id", "")
        self.title = d.get("title", "")
        self.stage = d.get("stage", "core")
        self.status = type("S", (), {"value": d.get("status", "todo")})()
        self.dependencies = d.get("dependencies", [])
        self.fork_question = d.get("fork_question", "")


class _Project:
    """Minimal wrapper that satisfies the physics/quantum module interfaces."""
    def __init__(self, d):
        self.id = d.get("id", "unknown")
        self.name = d.get("name", "unnamed")
        self.subtasks = [_Subtask(s) for s in d.get("subtasks", [])]
        self.priority = type("P", (), {"value": d.get("priority", "P1")})()
        self.forks = [_Fork(f) for f in d.get("forks", [])]
        self.forks_history = d.get("forks", [])


def main():
    pp = load_mod("project_physics", PHYSICS_PATH)
    qpl = load_mod("quantum_project_layer", QUANTUM_PATH)

    if not STATE_PATH.exists():
        print(f"ERROR: state file {STATE_PATH} not found")
        sys.exit(2)

    with open(STATE_PATH) as f:
        state = json.load(f)

    projects = [_Project(p) for p in state.get("projects", [])]
    quartz_alive = pp._engine_alive(pp.QUARTZ_URL)
    print(f"{len(projects)} projects | Quartz alive: {quartz_alive}")
    print("=" * 70)

    failures = 0
    for proj in projects:
        try:
            # CLASSICAL
            report = pp.analyze_project_physics(proj)
            fe = report.free_energy
            cp = report.critical_path
            ss = report.stress_strain

            print(f"\nPROJECT: {proj.name} ({len(proj.subtasks)} subtasks)")
            print(f"  CLASSICAL:")
            print(f"    Free Energy:    F = {fe.free_energy:.2f}  (E={fe.internal_energy:.1f})")
            print(f"    Critical Path:  chain={cp.critical_path_length}, feasibility={cp.feasibility:.2f}")
            print(f"    Stress/Strain:  {ss.verdict.name}, safety={ss.safety_factor:.2f}")
            print(f"    COMPOSITE:      {report.composite_health:.3f} -> {report.verdict}")

            # QUANTUM
            qrep = qpl.analyze_quantum_project(proj)
            print(f"  QUANTUM:")
            print(f"    Speedup:        {qrep.quantum_speedup:.2f}x")
            print(f"    Superposition:  {len(qrep.superposition_forks)} forks")
            coh = qrep.coherence
            print(f"    Coherence:      {coh.efficiency:.1f}x propagation efficiency")

        except Exception as e:
            print(f"\nFAIL: {proj.name} -> {e}")
            failures += 1

    print(f"\n{'=' * 70}")
    if failures:
        print(f"RESULT: {failures}/{len(projects)} projects FAILED")
        sys.exit(1)
    else:
        print(f"RESULT: Physics + quantum verified on all {len(projects)} projects")
        sys.exit(0)


if __name__ == "__main__":
    main()
