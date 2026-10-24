#!/usr/bin/env python3
"""
Degradation-graceful engine consumption pattern.

VERIFIED WORKING PATTERN for consuming Quartz lattice energies with tag-based
ID bridging. Replaces the old broken pattern that called a non-existent
/lattice/energy/{id} endpoint.

Confirmed end-to-end against Quartz v2.0.0 on 2026-06-20.
See references/quartz-integration-guide.md for full API quirks.
"""

import json
import math
from typing import Dict, List, Optional, Any
from urllib.request import Request, urlopen


def _engine_alive(url: str) -> bool:
    """Check if an engine is healthy. Checks JSON body, not just HTTP status."""
    try:
        with urlopen(f"{url}/health", timeout=2.0) as resp:
            data = json.loads(resp.read().decode())
            return data.get("status") in ("ok", "degraded")
    except Exception:
        return False


def _post(url: str, payload: dict, timeout: float = 5.0) -> bool:
    """POST JSON to an engine, returning True on success."""
    try:
        body = json.dumps(payload).encode("utf-8")
        req = Request(url, data=body, headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.getcode() == 200
    except Exception:
        return False


def feed_quartz_lattice(
    project_subtasks: List[Any],
    project_id: str,
    quartz_url: str = "http://127.0.0.1:port",
    energy_level: float = 0.7,
    cognitive_load: float = 0.4,
) -> bool:
    """
    Push subtasks INTO Quartz so it computes real lattice energies.

    CRITICAL: Call this BEFORE fetch_quartz_energies().

    Three gotchas handled here (see references/quartz-integration-guide.md):
    1. Priority sent as STRING "P0" not INT 0
    2. Capacity set BEFORE pushing tasks (auto-positioning requires it)
    3. PM spine ID embedded in tags for UUID bridging
    """
    if not _engine_alive(quartz_url):
        return False

    # 1. Set capacity FIRST — Quartz only auto-positions when capacity > 0
    _post(f"{quartz_url}/v1/lattice/capacity",
          {"energy_level": energy_level, "cognitive_load": cognitive_load})

    # 2. Push each subtask with PM ID in tags
    energy_map = {"setup": "low", "core": "high", "integration": "medium",
                  "validation": "medium", "ship": "low"}

    for st in project_subtasks:
        status = getattr(st.status, 'value', str(st.status))
        if status in ("approved", "rejected"):
            continue

        pri_val = getattr(st.priority, 'value', 'P2') if hasattr(st, 'priority') else "P2"

        payload = {
            "title": f"[{st.id}] {st.title}",
            "priority": pri_val,  # STRING, not int!
            "time_estimate_minutes": 60,
            "energy_required": energy_map.get(getattr(st, 'stage', ''), "medium"),
            "project": project_id,
            "tags": [getattr(st, 'stage', ''), st.id],  # PM ID in tags!
            "source": "pm-physics-layer",
        }
        _post(f"{quartz_url}/v1/tasks", payload)

    # 3. Trigger rebalance so energies are computed
    _post(f"{quartz_url}/v1/lattice/rebalance", {})
    return True


def fetch_quartz_energies(
    project_subtasks: List[Any],
    quartz_url: str = "http://127.0.0.1:port",
) -> Optional[Dict[str, float]]:
    """
    Fetch per-task lattice energies from Quartz.

    Bridges Quartz UUIDs back to PM spine IDs via the tags embedded during
    feed_quartz_lattice(). Converts stability scores to energies via
    Boltzmann transform: E = -ln(stability).

    Returns None if Quartz is down or has no positioned tasks (triggers
    local fallback in the calling physics layer).
    """
    if not _engine_alive(quartz_url):
        return None

    pm_ids = {st.id for st in project_subtasks}

    try:
        # Get lattice state (all positioned tasks + stability scores)
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
    except Exception:
        return None


def compute_local_task_energy(subtask: Any) -> float:
    """
    Local fallback for task energy when Quartz is unavailable.

    Uses priority weight * stage penalty — no lattice coupling, no
    spring energies, no stability scores. Less precise but always works.
    """
    pri_weights = {"P0": 3.0, "P1": 2.0, "P2": 1.0, "P3": 0.5}
    stage_penalties = {"setup": 0.5, "core": 1.5, "integration": 1.0,
                       "validation": 0.8, "ship": 0.6}

    status = getattr(subtask.status, 'value', str(subtask.status))
    if status in ("approved", "rejected"):
        return 0.0 if status == "approved" else 1.5

    pri = getattr(subtask, 'priority', None)
    pri_val = getattr(pri, 'value', 'P2') if pri else "P2"
    pw = pri_weights.get(pri_val, 1.0)
    sp = stage_penalties.get(getattr(subtask, 'stage', ''), 1.0)
    return pw * sp


# Example usage:
"""
# In your project physics compute function:

# 1. Feed Quartz (two-way bridge step 1)
feed_quartz_lattice(project.subtasks, project.id, QUARTZ_URL)

# 2. Fetch energies (two-way bridge step 2)
quartz_energies = fetch_quartz_energies(project.subtasks, QUARTZ_URL)

# 3. For each subtask, use Quartz energy if available, else local
for st in project.subtasks:
    if quartz_energies and st.id in quartz_energies:
        energy = quartz_energies[st.id]  # real Boltzmann energy from lattice
    else:
        energy = compute_local_task_energy(st)  # local fallback
"""
