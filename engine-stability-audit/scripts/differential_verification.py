#!/usr/bin/env python3
"""differential_verification.py — DIFFERENTIAL-VERIFICATION GATE (T-261021-0049)

Spynach pattern (Spinach MATLAB -> Python reimplementation, every stage
verified against the original) distilled into an executable engine-surgery
gate. GENOME (the specialist engine, immune): an agent-built reimplementation is
accepted ONLY when every stage is differentially verified against the
reference implementation. Verification is the immune system of automated
construction.

LAW (acceptance rule):
    accepted := (stages_run > 0) AND (all stages VERIFIED-PASS)
                AND (zero VERIFIED-FAIL / UNVERIFIED / SKIPPED stages)
A stage with no reference oracle, a stage never run, a stage whose cases
fail — all are ANTIGENS. Only zero-unverified shipping passes.

Exit codes:
    0  ACCEPTED          — every declared stage differentially verified + passed
    1  REJECTED          — >=1 stage VERIFIED-FAIL / UNVERIFIED / SKIPPED
    2  REFUSED           — manifest/adapter/reference unusable (never a pass)

Usage:
    differential_verification.py --manifest stages.json [--stage ID]*
                                  [--json] [--report-dir DIR]
    differential_verification.py --selftest

Manifest schema (JSON):
    {
      "reference": "refmodule",            # importable module (the oracle)
      "reimplementation": "reimplmodule",  # importable module (the rewrite)
      "stages": [
        {
          "id": "diffusion-weighting",
          "function": "diffusion_weight",   # same-named fn in both modules,
                                            # OR explicit: {"reference": "...",
                                            # "reimplementation": "..."}
          "cases": [ {"args": [0.5, 0.01], "kwargs": {}} , ... ],
          "compare": {"mode": "tolerance", "rtol": 1e-09, "atol": 1e-12},
          "skip": false                      # true => stage is UNVERIFIED,
                                             # acceptance impossible (teeth)
        }, ...
      ]
    }

Compare modes:
    exact        — Python == on results (discrete/categorical outputs)
    tolerance    — recursive numeric compare with rtol/atol (handles nested
                   lists/tuples/dicts; non-numeric leaves compared by ==)
    periodic     — numeric compare modulo `period` (PHASE-WRAPPED outputs:
                   -1 deg == 359 deg; naive tolerance FAILS on lawful wraps)
    keys         — structural parity: dict key sets must match exactly
                   (bare set/frozenset results compare by set equality)
    statistical  — stochastic stages: each case returns N samples; parity
                   via Welch t-statistic on the two sample sets (|m_e-m_a| /
                   sqrt(se_e^2+se_a^2) <= t_threshold, default 4.0).
                   Relative-to-mean tolerance is WRONG for zero-mean
                   signals (N(0,1) noise at n=500 has SE~0.045 — any
                   rtol on a mean near 0 misfires); the t-statistic is the
                   distributional oracle. Documented boundary: MATLAB-side
                   oracles cannot share Python seeds, so DISTRIBUTIONAL
                   parity — not trace parity — is what this verifies.

Falsification battery (selftest, written BEFORE the build per the
falsifiability gate):
    F1 detection     — reimpl with a sign error in ONE stage is caught
                       (VERIFIED-FAIL, exit 1) while sibling stages still pass
    F2 zero-unverified — a skipped stage blocks acceptance even when every
                       run stage passes
    F3 empty refusal — zero-stage manifest => exit 2, never vacuous pass
    F4 no-oracle     — unimportable reference => exit 2 REFUSED (cannot
                       verify == cannot accept)
    F5 missing fn    — reimpl missing a declared stage function => UNVERIFIED,
                       exit 1
    F6 periodicity   — phase-wrapped vs unwrapped outputs: periodic PASS where
                       naive tolerance FAILS (comparator-class proof, both
                       directions asserted)
    F7 relative tol  — 1e-12-scale outputs compared correctly by rtol where a
                       naive absolute compare misleads
    F8 statistical   — same-distribution stages pass; shifted-mean stage fails
    F9 keys-sets     — bare set/frozenset parity passes, drifted set fails
    F10 invalid spec — period=0 / n_samples=0 / atol=inf are UNVERIFIED
                       stages, never certificates (adversarial A1/C/E)
    F11 crash cont.  — comparator exceptions become named case failures,
                       no traceback (adversarial A2)
    F12 no partial   — --stage selection cannot mint ACCEPTED while
                       excluded stages are unverified (adversarial B)
    F13 no self-ref  — reference == reimplementation manifest => REFUSED
                       (adversarial D)
    F14 floor stays  — statistical n_samples<2 is rejected even with huge
                       t_threshold (adversarial C)
"""

from __future__ import annotations

import importlib
import json
import math
import os
import sys
import tempfile
import traceback
from dataclasses import dataclass, field

EXIT_ACCEPTED = 0
EXIT_REJECTED = 1
EXIT_REFUSED = 2

VALID_MODES = ("exact", "tolerance", "periodic", "keys", "statistical")


def _validate_spec(spec: dict) -> str | None:
    """Adversarial hardening (T-261021-0049 tri:adversarial battery A1/C/E):
    a comparator spec that cannot discriminate (period=0, atol=inf, sample
    floor disabled) minted false ACCEPTED certificates against a KNOWN-BROKEN
    reimplementation. Invalid spec => stage UNVERIFIED (antigen), never a
    pass. Returns None if the spec is sane, else the reason."""
    mode = spec.get("mode", "exact")
    if mode not in VALID_MODES:
        return f"invalid compare mode {mode!r}"
    if mode == "periodic":
        try:
            period = float(spec.get("period", 360.0))
        except (TypeError, ValueError):
            return "period is not a number"
        if not math.isfinite(period) or period <= 0:
            return f"period must be finite > 0 (got {period!r})"
    if mode == "statistical":
        n = spec.get("n_samples", 30)
        if isinstance(n, bool) or not isinstance(n, int) or n < 2:
            return (f"n_samples must be an int >= 2 (got {n!r}) — a "
                    f"disabled sample floor cannot verify a distribution")
        try:
            t = float(spec.get("t_threshold", 4.0))
        except (TypeError, ValueError):
            return "t_threshold is not a number"
        if not math.isfinite(t) or t <= 0:
            return f"t_threshold must be finite > 0 (got {t!r})"
        return None
    if mode in ("tolerance", "periodic"):
        defaults = {"rtol": 1e-9, "atol": 1e-12 if mode == "tolerance" else 1e-9}
        for key, dflt in defaults.items():
            try:
                v = float(spec.get(key, dflt))
            except (TypeError, ValueError):
                return f"{key} is not a number"
            if not math.isfinite(v) or v < 0:
                return f"{key} must be finite >= 0 (got {v!r})"
    return None


# --------------------------------------------------------------------------
# comparison core
# --------------------------------------------------------------------------

def _is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) \
        and not isinstance(v, str)


def _close(a: float, b: float, rtol: float, atol: float) -> bool:
    return abs(a - b) <= max(atol, rtol * max(abs(a), abs(b)))


def _numerate(v):
    """Complex numbers compare via (re, im) pairs — NMR/MRI outputs are
    complex-valued (transverse magnetization, k-space)."""
    if isinstance(v, complex):
        return [v.real, v.imag]
    return v


def _compare_values(expected, actual, spec: dict) -> tuple[bool, str]:
    """Recursive differential compare of one oracle result vs one
    reimplementation result. Returns (ok, why-not) for failure diagnosis."""
    mode = spec.get("mode", "exact")

    expected = _numerate(expected)
    actual = _numerate(actual)

    if mode == "keys":
        # a bare set IS a pure key collection — set equality is the whole
        # contract (no leaves). E2E-caught (T-261021-0049 fresh-oracle run):
        # doc law says "key sets equal" but dicts-only handling false-rejected
        # legitimate set-of-keys stage outputs.
        if isinstance(expected, (set, frozenset)) and \
                isinstance(actual, (set, frozenset)):
            if expected == actual:
                return True, ""
            return False, (f"set contents differ: "
                           f"ref-only={sorted(expected - actual, key=repr)} "
                           f"reimpl-only={sorted(actual - expected, key=repr)}")
        if not isinstance(expected, dict) or not isinstance(actual, dict):
            return False, "keys-mode requires dict or set results"
        ek, ak = set(expected.keys()), set(actual.keys())
        if ek != ak:
            return False, f"key sets differ: ref-only={sorted(ek-ak)} reimpl-only={sorted(ak-ek)}"
        # leaf values still compared recursively in exact mode
        for k in sorted(ek):
            ok, why = _compare_values(expected[k], actual[k], {"mode": "exact"})
            if not ok:
                return False, f"key {k!r}: {why}"
        return True, ""

    if mode == "periodic":
        # periodic compare applies at NUMERIC LEAVES of structured results
        # (dicts with phase fields are the real stage-output shape); all
        # non-numeric leaves fall back to exact compare.
        period = float(spec.get("period", 360.0))
        rtol = float(spec.get("rtol", 1e-9))
        atol = float(spec.get("atol", 1e-9))
        if isinstance(expected, dict) and isinstance(actual, dict):
            if set(expected.keys()) != set(actual.keys()):
                return False, (f"key sets differ: {sorted(set(expected)^set(actual))}")
            for k in sorted(expected):
                ok, why = _compare_values(expected[k], actual[k], spec)
                if not ok:
                    return False, f"key {k!r}: {why}"
            return True, ""
        if isinstance(expected, (list, tuple)) and isinstance(actual, (list, tuple)):
            if len(expected) != len(actual):
                return False, f"length differs: ref={len(expected)} reimpl={len(actual)}"
            for i, (e, a) in enumerate(zip(expected, actual)):
                ok, why = _compare_values(e, a, spec)
                if not ok:
                    return False, f"[{i}]: {why}"
            return True, ""
        if _is_number(expected) and _is_number(actual):
            delta = (float(expected) - float(actual)) % period
            delta = min(delta, period - delta)  # shortest signed distance mod period
            if delta <= max(atol, rtol * period):
                return True, ""
            return False, f"phase delta {delta:.6g} mod {period:g} exceeds tolerance"
        return _compare_values(expected, actual, {"mode": "exact"})

    if mode == "statistical":
        n = int(spec.get("n_samples", 30))
        t_threshold = float(spec.get("t_threshold", 4.0))
        if not isinstance(expected, (list, tuple)) or not isinstance(actual, (list, tuple)):
            return False, "statistical-mode requires sample lists"
        if len(expected) < n or len(actual) < n:
            return False, f"need >= {n} samples (ref={len(expected)}, reimpl={len(actual)})"
        m_e = sum(expected) / len(expected)
        m_a = sum(actual) / len(actual)
        var_e = sum((x - m_e) ** 2 for x in expected) / max(len(expected) - 1, 1)
        var_a = sum((x - m_a) ** 2 for x in actual) / max(len(actual) - 1, 1)
        se = math.sqrt(var_e / len(expected) + var_a / len(actual))
        # RELATIVE-TO-MEAN tolerance is meaningless for zero-mean signals
        # (N(0,1) noise: SE=0.045 at n=500 dwarfs any rtol on a mean near
        # 0) — the correct differential oracle is the Welch t-statistic.
        if se == 0:
            ok = (m_e == m_a)
            return (ok, "" if ok else f"zero-variance samples, means {m_e!r} vs {m_a!r}")
        t_stat = abs(m_e - m_a) / se
        if t_stat <= t_threshold:
            return True, ""
        return False, (f"distributions differ: means {m_e:.6g} vs {m_a:.6g}, "
                       f"t={t_stat:.2f} > {t_threshold:g} (Welch)")

    if isinstance(expected, (list, tuple)) and isinstance(actual, (list, tuple)):
        if len(expected) != len(actual):
            return False, f"length differs: ref={len(expected)} reimpl={len(actual)}"
        for i, (e, a) in enumerate(zip(expected, actual)):
            ok, why = _compare_values(e, a, spec)
            if not ok:
                return False, f"[{i}]: {why}"
        return True, ""

    if _is_number(expected) and _is_number(actual):
        if mode == "exact":
            if expected == actual:
                return True, ""
            return False, f"{expected!r} != {actual!r} (exact)"
        rtol = float(spec.get("rtol", 1e-9))
        atol = float(spec.get("atol", 1e-12))
        if _close(float(expected), float(actual), rtol, atol):
            return True, ""
        return False, (f"{expected!r} vs {actual!r} outside "
                       f"rtol={rtol:g}/atol={atol:g} "
                       f"(delta={abs(float(expected)-float(actual)):.6g})")

    if type(expected) is not type(actual) and not (
        isinstance(expected, (list, tuple)) and isinstance(actual, (list, tuple))
    ):
        return False, f"type differs: ref={type(expected).__name__} reimpl={type(actual).__name__}"
    if expected != actual:
        return False, f"{expected!r} != {actual!r}"
    return True, ""


# --------------------------------------------------------------------------
# harness
# --------------------------------------------------------------------------

@dataclass
class StageResult:
    stage_id: str
    status: str            # VERIFIED-PASS | VERIFIED-FAIL | UNVERIFIED | SKIPPED
    cases_run: int = 0
    cases_passed: int = 0
    failures: list = field(default_factory=list)


def _import_side(module_name: str, side: str):
    try:
        return importlib.import_module(module_name)
    except Exception as e:  # noqa: BLE001 — refusal must name the cause
        raise RefusedError(
            f"{side} module {module_name!r} unimportable — no oracle, no "
            f"acceptance ({e.__class__.__name__}: {e})"
        ) from e


class RefusedError(Exception):
    pass


def run_manifest(manifest_path: str, only_stages: list[str] | None = None,
                 json_out: bool = False) -> int:
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"REFUSED: cannot read manifest {manifest_path!r}: {e}",
              file=sys.stderr)
        return EXIT_REFUSED

    if not isinstance(manifest, dict):
        print("REFUSED: manifest must be a JSON object", file=sys.stderr)
        return EXIT_REFUSED

    # Adversarial hardening (battery D): a self-referential manifest verifies
    # nothing — reference and reimplementation must be distinct modules.
    if manifest.get("reference") == manifest.get("reimplementation"):
        print("REFUSED: reference and reimplementation are the same module — "
              "a self-referential manifest cannot differentially verify "
              "anything (F13)", file=sys.stderr)
        return EXIT_REFUSED

    # make manifest-local modules importable (cold CLI runs: the manifest's
    # dir and cwd are the oracle/reimpl home — E2E-caught usability defect)
    for p in (os.path.dirname(os.path.abspath(manifest_path)), os.getcwd()):
        if p and p not in sys.path:
            sys.path.insert(0, p)

    try:
        ref_mod = _import_side(manifest["reference"], "reference")
        reim_mod = _import_side(manifest["reimplementation"], "reimplementation")
    except (KeyError, RefusedError) as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return EXIT_REFUSED

    stages = manifest.get("stages")
    if not isinstance(stages, list) or len(stages) == 0:
        print("REFUSED: zero-stage manifest — nothing verified is not "
              "accepted (F3: vacuous pass forbidden)", file=sys.stderr)
        return EXIT_REFUSED

    results: list[StageResult] = []
    for stage in stages:
        sid = stage.get("id") or "<unnamed>"
        if only_stages and sid not in only_stages:
            # Adversarial hardening (battery B): an excluded stage is
            # UNVERIFIED, not invisible — partial selection can never mint
            # an ACCEPTED certificate (zero-unverified law is manifest-wide).
            results.append(StageResult(sid, "UNVERIFIED",
                                       failures=["excluded by --stage "
                                                 "selection — acceptance "
                                                 "impossible"]))
            continue

        if stage.get("skip"):
            results.append(StageResult(sid, "SKIPPED",
                                        failures=["stage marked skip=true — "
                                                  "UNVERIFIED, acceptance blocked"]))
            continue

        fn_spec = stage.get("function", {})
        if isinstance(fn_spec, str):
            ref_fn_name = reim_fn_name = fn_spec
        else:
            ref_fn_name = fn_spec.get("reference", "")
            reim_fn_name = fn_spec.get("reimplementation", "")

        cases = stage.get("cases") or []
        spec = dict(stage.get("compare") or {})
        spec_error = _validate_spec(spec)
        if spec_error is not None:
            results.append(StageResult(sid, "UNVERIFIED",
                                        failures=[f"invalid compare spec: "
                                                  f"{spec_error}"]))
            continue

        ref_fn = getattr(ref_mod, ref_fn_name, None)
        reim_fn = getattr(reim_mod, reim_fn_name, None)
        if ref_fn is None or reim_fn is None or not callable(ref_fn) \
                or not callable(reim_fn):
            missing = []
            if ref_fn is None:
                missing.append(f"reference.{ref_fn_name}")
            if reim_fn is None:
                missing.append(f"reimplementation.{reim_fn_name}")
            results.append(StageResult(sid, "UNVERIFIED",
                                       failures=[f"missing callable(s): {', '.join(missing)}"]))
            continue
        if len(cases) == 0:
            results.append(StageResult(sid, "UNVERIFIED",
                                       failures=["zero cases declared — a stage with no "
                                                 "inputs is unverified, not passed"]))
            continue

        sr = StageResult(sid, "VERIFIED-PASS")
        for ci, case in enumerate(cases):
            args = case.get("args", [])
            kwargs = case.get("kwargs", {})
            sr.cases_run += 1
            try:
                expected = ref_fn(*args, **kwargs)
            except Exception as e:  # noqa: BLE001 — oracle crash = antigen
                sr.failures.append(f"case {ci}: REFERENCE raised "
                                   f"{e.__class__.__name__}: {e}")
                continue
            try:
                actual = reim_fn(*args, **kwargs)
            except Exception as e:  # noqa: BLE001
                sr.failures.append(f"case {ci}: REIMPL raised "
                                   f"{e.__class__.__name__}: {e}")
                continue
            try:
                ok, why = _compare_values(expected, actual, spec)
            except Exception as e:  # noqa: BLE001 — comparator crash = antigen
                # Adversarial hardening (battery A): a comparator exception
                # (period=0, non-numeric samples) must become a named case
                # failure — never an uncaught traceback, never a pass.
                sr.failures.append(f"case {ci}: COMPARATOR raised "
                                   f"{e.__class__.__name__}: {e}")
                continue
            if ok:
                sr.cases_passed += 1
            else:
                sr.failures.append(f"case {ci} args={args!r}: DIFFERS — {why}")
        if sr.cases_run == sr.cases_passed and not sr.failures:
            sr.status = "VERIFIED-PASS"
        else:
            sr.status = "VERIFIED-FAIL"
        results.append(sr)

    accepted = (len(results) > 0
                and all(r.status == "VERIFIED-PASS" for r in results))

    total = len(results)
    passed = sum(1 for r in results if r.status == "VERIFIED-PASS")
    failed = sum(1 for r in results if r.status == "VERIFIED-FAIL")
    unverified = sum(1 for r in results if r.status in ("UNVERIFIED", "SKIPPED"))
    cases_run = sum(r.cases_run for r in results)
    cases_passed = sum(r.cases_passed for r in results)

    if json_out:
        print(json.dumps({
            "verdict": "ACCEPTED" if accepted else "REJECTED",
            "stages": {"total": total, "passed": passed, "failed": failed,
                       "unverified": unverified},
            "cases": {"run": cases_run, "passed": cases_passed},
            "results": [vars(r) for r in results],
        }, indent=1))
    else:
        print(f"{'='*64}\nDIFFERENTIAL-VERIFICATION "
              f"({'ACCEPTED' if accepted else 'REJECTED'})\n{'='*64}")
        for r in results:
            line = f"  [{r.status:<14}] {r.stage_id}: {r.cases_passed}/{r.cases_run} cases"
            print(line)
            for f_ in r.failures[:5]:
                print(f"      - {f_}")
            if len(r.failures) > 5:
                print(f"      ... +{len(r.failures)-5} more")
        print("-" * 64)
        print(f"stages: {passed}/{total} VERIFIED-PASS | {failed} FAILED | "
              f"{unverified} UNVERIFIED/SKIPPED")
        print(f"cases:  {cases_passed}/{cases_run} passed")
        print(f"acceptance rule: zero-unverified shipping — "
              f"{'SATISFIED' if accepted else 'VIOLATED'}")

    return EXIT_ACCEPTED if accepted else EXIT_REJECTED


# --------------------------------------------------------------------------
# selftest — the falsification battery (F1..F8), battery written first
# --------------------------------------------------------------------------

TOY_REFERENCE = '''\
"""Toy NMR/MRI-scale oracle (pure stdlib). Stages mirror the Spynach
reimplementation domain at toy scale: phase cycling, cogwheel modulation,
gradient coherence, diffusion weighting."""

import math
import random


def phase_cycle(amplitude, phase_deg):
    """Rotate a complex signal by phase_deg; result wrapped to (-180, 180]."""
    r = math.radians(phase_deg)
    rotated = amplitude * complex(math.cos(r), math.sin(r))
    ang = math.degrees(math.atan2(rotated.imag, rotated.real))
    if ang <= -180.0:
        ang += 360.0
    elif ang > 180.0:
        ang -= 360.0
    return {"amplitude": abs(rotated), "phase_deg": ang}


def cogwheel(states, steps):
    """Cogwheel modulation: state index advances by steps, mod len(states)."""
    return [states[(i + steps) % len(states)] for i in range(len(states))]


def gradient_coherence(components):
    """Coherence = |vector sum| / sum of magnitudes in [0, 1]."""
    sx = sum(c[0] for c in components)
    sy = sum(c[1] for c in components)
    mag_sum = sum(math.hypot(c[0], c[1]) for c in components)
    if mag_sum == 0:
        return 0.0
    return math.hypot(sx, sy) / mag_sum


def diffusion_weight(bvals, adc):
    """Signal decay S/S0 = exp(-b * adc) per b-value."""
    return [math.exp(-b * adc) for b in bvals]


def noise_samples(seed, n):
    r = random.Random(seed)
    return [r.gauss(0.0, 1.0) for _ in range(n)]
'''

TOY_REIMPL_GOOD = '''\
"""Faithful Python reimplementation of the toy oracle — deliberately written
with a DIFFERENT structure (class-based, different algorithms where lawful)
to prove structural difference does not break differential parity."""

import math
import random


class _Spin:
    @staticmethod
    def wrap(deg):
        # different wrap implementation: [0, 360) instead of (-180, 180]
        return deg % 360.0


class Stages:
    @staticmethod
    def phase_cycle(amplitude, phase_deg):
        r = math.radians(phase_deg)
        rot = amplitude * complex(math.cos(r), math.sin(r))
        return {"amplitude": math.sqrt(rot.real**2 + rot.imag**2),
                "phase_deg": _Spin.wrap(math.degrees(math.atan2(rot.imag, rot.real)))}

    @staticmethod
    def cogwheel(states, steps):
        n = len(states)
        out = []
        for i in range(n):
            out.append(states[(i + steps) % n])
        return out

    @staticmethod
    def gradient_coherence(components):
        sx = sy = mag = 0.0
        for x, y in components:
            sx += x
            sy += y
            mag += (x * x + y * y) ** 0.5
        if mag == 0.0:
            return 0.0
        return (sx * sx + sy * sy) ** 0.5 / mag

    @staticmethod
    def diffusion_weight(bvals, adc):
        return [math.exp(-(b * adc)) for b in bvals]

    @staticmethod
    def noise_samples(seed, n):
        # different RNG construction, same distribution contract
        r = random.Random(seed * 7919 + 13)
        return [r.gauss(0.0, 1.0) for _ in range(n)]


phase_cycle = Stages.phase_cycle
cogwheel = Stages.cogwheel
gradient_coherence = Stages.gradient_coherence
diffusion_weight = Stages.diffusion_weight
noise_samples = Stages.noise_samples
'''

TOY_REIMPL_BROKEN = '''\
"""Reimplementation with a SINGLE sign error in diffusion_weight —
the detection battery (F1) must catch exactly this stage and no other."""
import math
import random


def phase_cycle(amplitude, phase_deg):
    r = math.radians(phase_deg)
    rot = amplitude * complex(math.cos(r), math.sin(r))
    ang = math.degrees(math.atan2(rot.imag, rot.real))
    if ang <= -180.0:
        ang += 360.0
    elif ang > 180.0:
        ang -= 360.0
    return {"amplitude": abs(rot), "phase_deg": ang}


def cogwheel(states, steps):
    return [states[(i + steps) % len(states)] for i in range(len(states))]


def gradient_coherence(components):
    sx = sum(c[0] for c in components)
    sy = sum(c[1] for c in components)
    mag_sum = sum(math.hypot(c[0], c[1]) for c in components)
    return math.hypot(sx, sy) / mag_sum if mag_sum else 0.0


def diffusion_weight(bvals, adc):
    # SIGN ERROR (antigen): decay implemented as growth
    return [math.exp(b * adc) for b in bvals]
'''

TOY_REIMPL_SHIFTED = TOY_REIMPL_GOOD.replace(
    "r.gauss(0.0, 1.0)", "r.gauss(0.4, 1.0)")


def _write(tmp, name, text):
    p = os.path.join(tmp, name)
    with open(p, "w") as f:
        f.write(text)
    return p


def _manifest(tmp, ref="toy_reference", reim="toy_reimpl", stages=None):
    return os.path.join(tmp, f"manifest_{ref}_{reim}.json")


def selftest() -> int:
    tmp = tempfile.mkdtemp(prefix="diffverify-")
    _write(tmp, "toy_reference.py", TOY_REFERENCE)
    _write(tmp, "toy_reimpl.py", TOY_REIMPL_GOOD)
    _write(tmp, "toy_reimpl_broken.py", TOY_REIMPL_BROKEN)
    _write(tmp, "toy_reimpl_shifted.py", TOY_REIMPL_SHIFTED)
    sys.path.insert(0, tmp)

    def m(name, doc):
        p = os.path.join(tmp, name)
        with open(p, "w") as f:
            json.dump(doc, f)
        return p

    core_stages = [
        {"id": "phase-cycling",
         "function": "phase_cycle",
         "cases": [{"args": [2.0, 45.0]}, {"args": [1.5, 350.0]},
                   {"args": [1.0, -90.0]}, {"args": [0.0, 17.0]}],
         "compare": {"mode": "periodic", "period": 360.0, "rtol": 1e-9,
                     "atol": 1e-9}},
        {"id": "cogwheel",
         "function": "cogwheel",
         "cases": [{"args": [[1, 2, 3, 4], 1]}, {"args": [["a", "b"], 3]},
                   {"args": [[True, False, True], 2]}],
         "compare": {"mode": "exact"}},
        {"id": "gradient-coherence",
         "function": "gradient_coherence",
         "cases": [{"args": [[[1.0, 0.0], [1.0, 0.0]]]},
                   {"args": [[[1.0, 0.0], [-1.0, 0.0]]]},
                   {"args": [[]]}],
         "compare": {"mode": "tolerance", "rtol": 1e-12, "atol": 1e-15}},
        {"id": "diffusion-weighting",
         "function": "diffusion_weight",
         "cases": [{"args": [[0.0, 100.0, 1000.0], 0.001]},
                   {"args": [[500.0], 0.002]}],
         "compare": {"mode": "tolerance", "rtol": 1e-12, "atol": 1e-15}},
    ]
    tiny_stage = [{"id": "tiny-scale",
                   "function": "diffusion_weight",
                   "cases": [{"args": [[1e-12, 2e-12], 1e-12]}],
                   "compare": {"mode": "tolerance", "rtol": 1e-9, "atol": 1e-30}}]
    noise_stage = [{"id": "noise-distribution",
                    "function": "noise_samples",
                    "cases": [{"args": [42, 500]}],
                    "compare": {"mode": "statistical", "n_samples": 500,
                                "t_threshold": 4.0}}]

    battery = []

    def run(name, path, want_exit, want_verdict, assertions=None):
        rc = run_manifest(path, json_out=False)
        ok = rc == want_exit
        detail = f"exit={rc} want={want_exit}"
        if assertions:
            with open(os.devnull, "w") as devnull:
                saved = sys.stdout
                sys.stdout = devnull
                try:
                    # re-run capturing via a tiny shim: reuse results by
                    # calling internals instead (cheap: compare funcs)
                    pass
                finally:
                    sys.stdout = saved
        battery.append((name, ok, detail))

    # F1 detection: broken reimpl -> REJECTED exit 1, sibling stages intact
    p_broken = m("m_broken.json",
                 {"reference": "toy_reference",
                  "reimplementation": "toy_reimpl_broken",
                  "stages": core_stages})
    run("F1 detection (broken stage caught)", p_broken, EXIT_REJECTED, "REJECTED")

    # F2 zero-unverified: skip=true blocks acceptance
    p_skip = m("m_skip.json",
               {"reference": "toy_reference", "reimplementation": "toy_reimpl",
                "stages": core_stages[:2] + [
                    {"id": "diffusion-weighting",
                     "function": "diffusion_weight",
                     "skip": True,
                     "cases": [{"args": [[100.0], 0.001]}],
                     "compare": {"mode": "tolerance", "rtol": 1e-12}}]})
    run("F2 zero-unverified (skip blocks)", p_skip, EXIT_REJECTED, "REJECTED")

    # F3 empty manifest refused
    p_empty = m("m_empty.json",
                {"reference": "toy_reference", "reimplementation": "toy_reimpl",
                 "stages": []})
    run("F3 empty manifest refused", p_empty, EXIT_REFUSED, "REFUSED")

    # F4 no oracle refused
    p_nooracle = m("m_nooracle.json",
                   {"reference": "does_not_exist_anywhere",
                    "reimplementation": "toy_reimpl",
                    "stages": core_stages[:1]})
    run("F4 no-oracle refused", p_nooracle, EXIT_REFUSED, "REFUSED")

    # F5 missing reimpl function -> UNVERIFIED -> exit 1
    p_missing = m("m_missing.json",
                  {"reference": "toy_reference",
                   "reimplementation": "toy_reimpl_broken",  # lacks noise_samples
                   "stages": core_stages[:2] + [{
                       "id": "noise-distribution",
                       "function": "noise_samples",
                       "cases": [{"args": [1, 50]}],
                       "compare": {"mode": "statistical", "n_samples": 30}}]})
    run("F5 missing fn -> UNVERIFIED", p_missing, EXIT_REJECTED, "REJECTED")

    # F6 periodic comparator class: unwrapped-vs-wrapped phase
    ok_f6_pass, why = _compare_values(-10.0, 350.0,
                                      {"mode": "periodic", "period": 360.0,
                                       "atol": 1e-9})
    ok_f6_fail, _ = _compare_values(-10.0, 350.0,
                                    {"mode": "tolerance", "rtol": 1e-9,
                                     "atol": 1e-9})
    battery.append(("F6 periodic PASS where tolerance FAILS",
                    ok_f6_pass and not ok_f6_fail,
                    f"periodic={ok_f6_pass} tolerance={ok_f6_fail}"))

    # F7 relative tolerance at 1e-12 scale
    ok_f7_pass, _ = _compare_values(1e-12, 1.0000000005e-12,
                                    {"mode": "tolerance", "rtol": 1e-9,
                                     "atol": 1e-30})
    ok_f7_fail, _ = _compare_values(1e-12, 2e-12,
                                    {"mode": "tolerance", "rtol": 1e-9,
                                     "atol": 1e-30})
    battery.append(("F7 rtol tiny-scale (pass + reject both directions)",
                    ok_f7_pass and not ok_f7_fail,
                    f"near={ok_f7_pass} far={ok_f7_fail}"))

    # F8 statistical: same-distribution passes, shifted mean fails
    import toy_reference, toy_reimpl, toy_reimpl_shifted  # noqa: E402
    e = toy_reference.noise_samples(7, 500)
    a_good = toy_reimpl.noise_samples(7, 500)
    a_shift = toy_reimpl_shifted.noise_samples(7, 500)
    ok_f8_pass, _ = _compare_values(e, a_good,
                                    {"mode": "statistical", "n_samples": 500,
                                     "t_threshold": 4.0})
    ok_f8_fail, _ = _compare_values(e, a_shift,
                                    {"mode": "statistical", "n_samples": 500,
                                     "t_threshold": 4.0})
    battery.append(("F8 statistical (same passes, shift fails)",
                    ok_f8_pass and not ok_f8_fail,
                    f"same={ok_f8_pass} shifted={ok_f8_fail}"))

    # F9 keys-mode on bare sets: parity passes, drifted set fails
    # (E2E-caught T-261021-0049: doc law "key sets equal" vs dicts-only code)
    ok_f9_pass, _ = _compare_values({(0, 0), (1, -1), (-1, 1)},
                                    frozenset({(1, -1), (-1, 1), (0, 0)}),
                                    {"mode": "keys"})
    ok_f9_fail, _ = _compare_values({(0, 0), (1, -1), (-1, 1)},
                                    {(1, -1), (-1, 1), (0, 1)},
                                    {"mode": "keys"})
    battery.append(("F9 keys-mode set parity (pass + drift reject)",
                    ok_f9_pass and not ok_f9_fail,
                    f"parity={ok_f9_pass} drift={ok_f9_fail}"))

    # ------------------------------------------------------------------
    # Adversarial battery (tri:adversarial, T-261021-0049): each check below
    # was a CONFIRMED false-accept or crash in the red-team run before the
    # corresponding hardening landed. They stay here so the holes cannot
    # silently reopen.
    # ------------------------------------------------------------------

    # F10 invalid-spec (battery A1/C/E): period=0 / n_samples=0 / atol=inf
    # => stage UNVERIFIED => REJECTED, even with a GOOD reimplementation
    p_badspec = m("m_badspec.json",
                  {"reference": "toy_reference", "reimplementation": "toy_reimpl",
                   "stages": core_stages[:1] + [
                       {"id": "phase-zero-period",
                        "function": "phase_cycle",
                        "cases": [{"args": [1.0, 45.0]}],
                        "compare": {"mode": "periodic", "period": 0.0}},
                       {"id": "noise-floor-off",
                        "function": "noise_samples",
                        "cases": [{"args": [7, 500]}],
                        "compare": {"mode": "statistical", "n_samples": 0,
                                    "t_threshold": 1e9}},
                       {"id": "diff-inf-atol",
                        "function": "diffusion_weight",
                        "cases": [{"args": [[100.0], 0.001]}],
                        "compare": {"mode": "tolerance", "rtol": 0.0,
                                    "atol": float("inf")}}]})
    run("F10 invalid spec (period=0, n=0, atol=inf) -> REJECT",
        p_badspec, EXIT_REJECTED, "REJECTED")

    # F11 comparator crash contained (battery A2): string samples in
    # statistical mode -> named case failure, no traceback, exit 1
    _write(tmp, "toy_str.py",
           "def noise_samples(seed, n):\n    return ['x'] * n\n")
    p_strstats = m("m_strstats.json",
                   {"reference": "toy_reference", "reimplementation": "toy_str",
                    "stages": [{"id": "noise", "function": "noise_samples",
                                "cases": [{"args": [1, 30]}],
                                "compare": {"mode": "statistical",
                                            "n_samples": 30}}]})
    run("F11 comparator-crash contained (no traceback)", p_strstats,
        EXIT_REJECTED, "REJECTED")

    # F12 partial selection cannot ACCEPT (battery B): --stage over a
    # manifest whose OTHER stage is broken must NOT mint a certificate
    p_partial = m("m_partial.json",
                  {"reference": "toy_reference",
                   "reimplementation": "toy_reimpl_broken",
                   "stages": [{"id": "cogwheel", "function": "cogwheel",
                               "cases": [{"args": [[1, 2, 3, 4], 1]}],
                               "compare": {"mode": "exact"}},
                              {"id": "diffusion-weighting",
                               "function": "diffusion_weight",
                               "cases": [{"args": [[100.0], 0.001]}],
                               "compare": {"mode": "tolerance", "rtol": 1e-12}}]})
    rc = run_manifest(p_partial, only_stages=["cogwheel"], json_out=False)
    battery.append(("F12 partial-selection cannot ACCEPT",
                    rc == EXIT_REJECTED, f"exit={rc} want={EXIT_REJECTED}"))

    # F13 self-referential manifest refused (battery D)
    p_selfref = m("m_selfref.json",
                  {"reference": "toy_reference", "reimplementation": "toy_reference",
                   "stages": core_stages[:1]})
    run("F13 self-referential manifest REFUSED", p_selfref,
        EXIT_REFUSED, "REFUSED")

    # F14 statistical bypass closed (battery C): shifted-mean reimpl with
    # n_samples=0 + t_threshold=1e9 must be REJECTED, not accepted
    p_bypass = m("m_bypass.json",
                 {"reference": "toy_reference",
                  "reimplementation": "toy_reimpl_shifted",
                  "stages": [{"id": "noise", "function": "noise_samples",
                              "cases": [{"args": [7, 500]}],
                              "compare": {"mode": "statistical", "n_samples": 0,
                                          "t_threshold": 1e9}}]})
    run("F14 statistical floor bypass REJECTED", p_bypass,
        EXIT_REJECTED, "REJECTED")

    # GOLDEN PATH: good reimpl, full manifest incl statistical stage -> ACCEPT
    p_good = m("m_good.json",
               {"reference": "toy_reference", "reimplementation": "toy_reimpl",
                "stages": core_stages + tiny_stage + noise_stage})
    run("GOLDEN full-fidelity acceptance", p_good, EXIT_ACCEPTED, "ACCEPTED")

    failed = [b for b in battery if not b[1]]
    print("=" * 64)
    for name, ok, detail in battery:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}  ({detail})")
    print("=" * 64)
    print(f"selftest: {len(battery) - len(failed)}/{len(battery)} "
          f"falsification checks hold")
    return 0 if not failed else 1


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return selftest()
    manifest = None
    only: list[str] = []
    json_out = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--manifest":
            i += 1
            manifest = argv[i] if i < len(argv) else None
        elif a == "--stage":
            i += 1
            only.append(argv[i])
        elif a == "--json":
            json_out = True
        else:
            print(f"REFUSED: unknown arg {a!r}", file=sys.stderr)
            return EXIT_REFUSED
        i += 1
    if manifest is None:
        print(__doc__)
        return EXIT_REFUSED
    return run_manifest(manifest, only_stages=only or None,
                        json_out=json_out)


if __name__ == "__main__":
    sys.exit(main())
