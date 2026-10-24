# Differential-Verification Protocol for Agent-Built Reimplementations

**Origin:** T-261021-0049 (BUILD 261021, ceo-referral g-ZNB4Fi, research line
sr-751617c4e7 `st-verified-reimplementation-agents`). Harness:
`scripts/differential_verification.py` (this directory). Executable selftest:
9/9 falsification checks (F1–F8 + golden path).

**GENOME (the specialist engine, immune):** an agent-built reimplementation is accepted
only when every stage is differentially verified against the reference
implementation. Verification is the immune system of automated construction.
Metric: differential-verification checklist on every agent-built engine
rewrite; per-stage verify/pass counts reported; zero unverified stages
shipped.

## The Pattern (Spynach)

Spinach is a MATLAB magnetic-resonance simulation library. The Spynach
project reimplemented it in Python with an AI coding agent — motive: no
license barrier, runs in a browser and via pip, no MATLAB seat required.
The physics is NMR/MRI-grade: phase cycling, cogwheel modulation, gradient
coherence, diffusion weighting. The operative discovery was NOT "an AI can
rewrite MATLAB in Python" — it was the acceptance discipline:

> Every stage of the reimplementation was verified against the original
> before being counted as done. The rewrite shipped with per-stage parity
> evidence, not vibes.

Distilled: **the reference implementation is the oracle; the reimplementation
is accepted stage-by-stage; acceptance requires zero unverified stages.**
This protocol makes that discipline executable for ANY agent-built engine
rewrite in this organism (Python→Python ports, MATLAB/engine refactor
escapes, cross-language reimplementations through adapters).

## Why differential (and not just "tests pass")

A reimplementation's own test suite proves nothing about fidelity — the
agent that misread the reference also writes the tests. The ONLY trustworthy
oracle is the reference implementation itself, executed on identical inputs.
"Differential" = both sides run, outputs compare, per stage:

```
for stage in reference_stages:
    for case in stage.cases:
        expected = reference.invoke(case)
        actual   = reimplementation.invoke(case)
        verdict  = compare(expected, actual, stage.compare_mode)
accepted := all stages VERIFIED-PASS AND stages_run > 0
```

## Protocol Steps (binding order)

1. **Oracle establishment.** The reference must be executable through an
   adapter (importable module, subprocess wrapper, MATLAB-via-python shim).
   No runnable oracle → NO ACCEPTANCE IS POSSIBLE, by construction
   (harness exits REFUSED). "The paper describes it" is not an oracle.
2. **Stage inventory.** Decompose the reference into stages = units whose
   outputs are independently observable (a function, an API endpoint, a
   pipeline phase). Each stage gets an ID recorded in the manifest.
3. **Case design per stage.** Minimum: typical inputs, boundary inputs
   (zero, empty list, max expected size), and domain edge inputs (for
   NMR-class physics: b=0, 180° phase wrap, empty gradient table, negative
   ADC). A stage with zero cases is UNVERIFIED, not passed.
4. **Comparator-class assignment.** Each stage declares its compare mode
   from the taxonomy below. Wrong comparator class = false FAIL on lawful
   behavior (phase wrap) or false PASS on real drift (zero-mean noise).
5. **Differential execution.** Run the harness. Both sides crash-loud:
   a reference exception is as much an antigen as a reimplementation one.
6. **Verdict + immune memory.** Report per-stage verify/pass counts. Every
   VERIFIED-FAIL caught becomes a regression case in the manifest (the
   antibody) — manifests grow monotonically like the immune-memory test
   suite.

## Comparator-Class Taxonomy (the non-obvious core)

| Mode | Use on | Law |
|---|---|---|
| `exact` | Discrete/categorical outputs (cogwheel state tables, flags, key sets) | `==` |
| `tolerance` | Floating accumulation outputs (signal intensities, decay curves) | recursive `rtol`/`atol`; rtol is MANDATORY for magnitudes spanning decades — absolute-only compare at 1e-12 scale misfires |
| `periodic` | Phase-wrapped outputs (phase cycling, cogwheel angle maps) | compare modulo `period` at numeric leaves; `-1° == 359°`. Naive tolerance FALSE-FAILS lawful wraps — this class exists because the domain demands it |
| `keys` | Structured results where shape parity is the contract | dict: key sets equal + leaf-exact; bare `set`/`frozenset` result: set equality (F9, E2E-caught 261022) |
| `statistical` | Stochastic stages (noise, Monte-Carlo) | Welch t-statistic `|m_e−m_a|/√(se_e²+se_a²) ≤ t_threshold` (default 4.0). NEVER relative-to-mean tolerance: zero-mean signals (N(0,1) noise, SE≈0.045 at n=500) make rtol-on-mean meaningless — this defect was caught by this protocol's own falsification battery (F8) |

Complex-valued outputs (transverse magnetization, k-space) compare via
(real, imag) pair decomposition — handled by the harness's `_numerate`.

## Acceptance Law (the teeth)

```
accepted := stages_run > 0
        AND every stage ∈ {VERIFIED-PASS}
```

- `VERIFIED-FAIL` — differential mismatch on ≥1 case → REJECT (exit 1)
- `UNVERIFIED` — missing callable, zero cases, invalid comparator → REJECT (exit 1)
- `SKIPPED` — `skip:true` is a confession of unverified scope → REJECT (exit 1)
- Empty manifest / no runnable oracle → REFUSE (exit 2, never a pass)

"Zero unverified stages shipped" means exactly that: a skipped stage is not
a concession, it is a rejection. Partial acceptance does not exist; stages
that matter get oracles, stages that don't get deleted from the manifest.

## Report Format (per GENOME metric)

```
DIFFERENTIAL-VERIFICATION (ACCEPTED|REJECTED)
  [VERIFIED-PASS] stage-id: n/n cases
  [VERIFIED-FAIL] stage-id: k/n cases — first divergence + delta
  [SKIPPED     ] stage-id: unverified scope, acceptance blocked
stages: P/T VERIFIED-PASS | F FAILED | U UNVERIFIED/SKIPPED
cases:  C/N passed
acceptance rule: zero-unverified shipping — SATISFIED|VIOLATED
```

Attach this report to any "reimplementation done" claim. A claim without
per-stage counts is DECORATIVE (SOUND vs DECORATIVE, the specialist engine).

## Integration Points

- **engine-stability-audit** (this skill): differential verification runs
  BEFORE the 8-standard-tests stability battery when the audited change is
  a reimplementation/rewrite. Fidelity first (are the physics right?),
  then stability (does it hold under load?). A rewrite that is stable but
  not differentially verified is STILL BROKEN — wrong physics that never
  crashes is the worst failure class.
- **product-immune-system**: a reimplementation "birth" requires the
  differential-verification certificate as a `passive_immunity` milestone
  (see SKILL.md wiring). Caught divergences become manifest regression
  cases = antibody production.

## Falsification Battery (what was tried to break it)

F1 single-stage sign error caught while siblings pass · F2 skip=true blocks
acceptance even with all-run-stages green · F3 zero-stage manifest refused
(vacuous pass forbidden) · F4 unimportable oracle refused · F5 missing
reimpl callable → UNVERIFIED → reject · F6 periodic PASS where tolerance
FALSE-FAILS (-1° vs 359°, both directions asserted) · F7 rtol correct at
1e-12 scale (near passes, 2× fails) · F8 same-distribution passes /
shifted-mean fails via Welch t · F9 bare-set outputs accepted in keys mode
(parity passes, drifted set named) — caught live by the 261022 fresh-oracle
E2E run, fixed and battery-locked same day. Development itself falsified
four defects
(traceback escape on refusal, non-recursive periodic compare,
rtol-on-zero-mean statistical compare) — all fixed, all now battery-locked.

### Adversarial station hardening (261023, tri:adversarial F10-F14)

Five MORE holes confirmed by cold red-team execution against the built gate
— four minted false ACCEPTED certificates on KNOWN-BROKEN reimplementations,
two crashed with uncaught tracebacks. All repaired same pass, all
battery-locked (selftest F10-F14):

- **A1/E — absurd comparator specs** (`period=0`, `atol=inf`): a spec that
  cannot discriminate verifies nothing. Now: invalid spec → stage UNVERIFIED
  → reject (F10). Validated: period finite>0; rtol/atol finite≥0;
  t_threshold finite>0.
- **A2 — comparator crash escape**: exceptions inside the comparator
  (ZeroDivisionError, TypeError on non-numeric samples) escaped as
  tracebacks. Now: contained as named case failures (`COMPARATOR raised …`)
  → VERIFIED-FAIL → reject, clean report, no traceback (F11).
- **B — partial-selection bypass**: `--stage good` over a manifest with a
  BROKEN sibling minted exit-0 ACCEPTED — the zero-unverified law was
  selection-scoped, not manifest-scoped. Now: excluded stages are reported
  UNVERIFIED; acceptance is impossible under any partial selection (F12).
- **C — statistical floor bypass**: `n_samples=0` + `t_threshold=1e9`
  accepted a shifted-mean (broken) reimplementation. Now: `n_samples` must
  be an int ≥ 2 — a disabled sample floor cannot verify a distribution
  (F10/F14).
- **D — self-referential manifests**: `reference == reimplementation`
  trivially passed (it verifies nothing). Now: REFUSED at intake (F13).

Re-verified after hardening: selftest 15/15 (exit 0), GOLDEN acceptance
intact (6/6 stages, 14/14 cases), external cold battery 6/6 attacks closed
(0 false-accepts, 0 crashes).

**Could not falsify / known boundaries:** MATLAB-native oracles require a
python adapter (octave-engine/matlab.engine wrapper; protocol takes any
importable callable, adapter construction is out of scope); GUI-only
reference behavior has no callable oracle and cannot be differentially
verified (must be excluded from acceptance claims explicitly); statistical
mode verifies distributional parity, not trace parity (cross-RNG streams
can never match trace-for-trace — by design, not defect).

## Worked Example

The harness selftest IS the worked example: a toy NMR-scale oracle (phase
cycling, cogwheel, gradient coherence, diffusion weighting, noise) with a
faithful structural-different reimplementation (class-based, different wrap
convention [0,360) vs (-180,180], different RNG construction) accepted at
exit 0; a single-sign-error variant rejected with the exact stage and delta
named. Run: `python3 scripts/differential_verification.py --selftest`
