#!/usr/bin/env python3
"""
Ad-hoc verification template for AI health dimension physics correctness.

Run this after editing canonical_coupling_ai.py, real_sensors.py, or
self_healing_loop.py to verify the physics properties hold.

Usage (from anywhere, paths auto-resolve):
  python3 scripts/verify-ai-health-dimensions.py

Tests cover:
  1. canonical_coupling_ai: pair counts, TWC bounds, cascade amplification
  2. real_sensors: all 6 core sensors + INTER return telemetry dicts
  3. self_healing_loop: execute_cycle with operator param, all 8 stages
"""
import sys
import os

# Auto-resolve organism directory
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = [
    os.path.join(_SCRIPT_DIR, "..", "..", "your-workspace", "organism"),
    os.path.join(_SCRIPT_DIR, "..", "..", "..", "your-workspace", "organism"),
    "/<workspace>",
]
for _p in _CANDIDATES:
    if os.path.exists(_p):
        sys.path.insert(0, _p)
        break

from canonical_coupling_ai import (
    DIMS_CORE, twc, volatility_meta, verify, get_active_dims,
)
from real_sensors import sense_all, sense_cog, sense_pipe, sense_res, sense_know, sense_align, sense_adapt, sense_inter
from self_healing_loop import execute_cycle, sense, score, _neutral_defaults


def test_canonical_coupling_ai():
    """Verify the dimension system physics correctness."""
    print("TEST 1: canonical_coupling_ai physics correctness")
    print("-" * 60)

    assert verify(), "canonical_coupling_ai verify() failed"
    print("PASS: verify()")

    # TWC bounded [0, 10]
    for val in [0, 3, 5, 7, 8, 10]:
        scores = {d: float(val) for d in DIMS_CORE}
        twc_val = twc(scores)
        assert 0 <= twc_val <= 10, f"TWC out of bounds at {val}: {twc_val}"
    print("PASS: TWC bounded [0, 10]")

    # Cascade amplification: COG drops hardest
    base = {d: 8.0 for d in DIMS_CORE}
    degraded = dict(base)
    degraded["COG"] = 3.0
    degraded_twc = twc(degraded)
    linear_avg = sum(degraded.values()) / len(degraded)
    assert degraded_twc < linear_avg, \
        f"COG drop should amplify: TWC={degraded_twc:.2f} vs linear={linear_avg:.2f}"
    print(f"PASS: COG cascade amplification (TWC {degraded_twc:.2f} < linear {linear_avg:.2f})")

    # Volatility meta-signal
    vol = volatility_meta([
        {d: 8.0 + (0.3 if d != "COG" else -0.1 * i) for d in DIMS_CORE}
        for i in range(5)
    ])
    assert "COG" in vol
    print(f"PASS: Volatility meta-signal computed (COG vol: {vol['COG']:.3f})")

    # Fleet mode adds INTER
    fleet_dims = get_active_dims(fleet_mode=True)
    assert "INTER" in fleet_dims and len(fleet_dims) == 7
    print("PASS: Fleet mode: 7 dimensions")
    print()
    return True


def test_real_sensors():
    """Verify real sensor adapters return valid telemetry."""
    print("TEST 2: real_sensors telemetry collection")
    print("-" * 60)

    # Core mode: 6 dimensions
    telemetry = sense_all(operator="hermes", fleet_mode=False)
    assert len(telemetry) == 6, f"Expected 6 core dims, got {len(telemetry)}"
    for dim in DIMS_CORE:
        assert dim in telemetry, f"Missing {dim} in telemetry"
        assert isinstance(telemetry[dim], dict), f"{dim} telemetry not a dict"
    print("PASS: Core mode returns 6 dimensions with dict telemetry")

    # Fleet mode: 7 dimensions
    telemetry_fleet = sense_all(operator="hermes", fleet_mode=True)
    assert "INTER" in telemetry_fleet, "Fleet mode missing INTER"
    print("PASS: Fleet mode returns 7 dimensions including INTER")

    # Individual sensors return dicts (graceful degradation: never crash)
    for fn, name in [(sense_cog, "COG"), (sense_pipe, "PIPE"), (sense_res, "RES"),
                     (sense_know, "KNOW"), (sense_align, "ALIGN"), (sense_adapt, "ADAPT"),
                     (sense_inter, "INTER")]:
        result = fn()
        assert isinstance(result, dict), f"{name} sensor did not return dict"
    print("PASS: All individual sensors return dicts (graceful degradation works)")

    # sense() delegates to real_sensors
    via_loop = sense(operator="hermes", fleet_mode=False)
    assert "COG" in via_loop, "sense() did not return COG"
    print("PASS: self_healing_loop.sense() delegates to real_sensors")
    print()
    return True


def test_self_healing_loop():
    """Verify the self-healing loop end-to-end with operator parameter."""
    print("TEST 3: self_healing_loop end-to-end")
    print("-" * 60)

    # execute_cycle with operator parameter
    cycle = execute_cycle(operator="hermes", fleet_mode=False, dry_run=True)
    assert isinstance(cycle, dict), "execute_cycle did not return dict"
    print("PASS: execute_cycle with operator param completed")

    # All 8 stages present
    required_keys = ["timestamp", "scores", "twc", "fleet_mode", "alerts",
                     "diagnoses", "interventions", "validation", "kappa_updates"]
    for key in required_keys:
        assert key in cycle, f"Missing key in cycle: {key}"
    print("PASS: All 8 stages present")

    # TWC bounded and consistent
    twc_val = cycle["twc"]
    assert 0 <= twc_val <= 10, f"TWC out of bounds: {twc_val}"
    print(f"PASS: TWC bounded [0,10]: {twc_val:.2f}")

    # All 6 core dims present in scores
    for dim in DIMS_CORE:
        assert dim in cycle["scores"], f"Missing {dim} in cycle scores"
    print(f"PASS: All 6 core dimensions scored")

    # score() uses real telemetry field names
    test_telemetry = {
        "COG": {"reentry_loop_count": 2.0, "reentry_severity": 2.0, "escalation_rate": 0.1},
        "PIPE": {"api_latency_p95": 3.0, "tool_failure_rate": 0.1, "stalled_count": 1.0},
        "RES": {"budget_adherence": 0.85, "cost_trajectory_slope": 0.02},
        "KNOW": {"source_age_median_days": 45.0, "learning_rate": 0.6},
        "ALIGN": {"compliance_rate": 0.90, "boundary_violations": 1.0},
        "ADAPT": {"recovery_time_avg": 300.0, "novel_input_success": 0.65,
                  "critical_slowing_verdict": "SLOWING"},
    }
    scores = score(test_telemetry, fleet_mode=False)
    assert len(scores) == 6
    for dim, s in scores.items():
        assert 0.0 <= s <= 10.0, f"{dim} score out of bounds: {s}"
    print("PASS: score() handles real telemetry fields")

    # ADAPT critical slowing penalty gradient
    base_adapt = {"recovery_time_avg": 120.0, "novel_input_success": 0.9}
    s_stable = score({**{d: {} for d in DIMS_CORE if d != "ADAPT"},
                      "ADAPT": {**base_adapt, "critical_slowing_verdict": "STABLE"}})["ADAPT"]
    s_slowing = score({**{d: {} for d in DIMS_CORE if d != "ADAPT"},
                       "ADAPT": {**base_adapt, "critical_slowing_verdict": "SLOWING"}})["ADAPT"]
    s_tipping = score({**{d: {} for d in DIMS_CORE if d != "ADAPT"},
                       "ADAPT": {**base_adapt, "critical_slowing_verdict": "NEAR_TIPPING"}})["ADAPT"]
    assert s_stable > s_slowing > s_tipping, \
        f"ADAPT penalty gradient wrong: {s_stable} vs {s_slowing} vs {s_tipping}"
    print(f"PASS: ADAPT critical slowing gradient (STABLE {s_stable:.1f} > SLOWING {s_slowing:.1f} > TIPPING {s_tipping:.1f})")

    # TWC matches coupling engine
    from canonical_coupling_ai import twc as coupling_twc
    expected = coupling_twc(cycle["scores"], fleet_mode=False)
    assert abs(cycle["twc"] - expected) < 0.1, \
        f"TWC mismatch: loop={cycle['twc']}, coupling={expected:.2f}"
    print(f"PASS: TWC matches coupling engine ({cycle['twc']:.2f})")
    print()
    return True


def main():
    try:
        test_canonical_coupling_ai()
        test_real_sensors()
        test_self_healing_loop()
        print("=" * 60)
        print("RESULT: ALL TESTS PASSED")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"FAIL: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
