# Permutation-Null Coupling Calibration (executed 2026-08-16)

Trigger: principal asked "Do you actually use geometry for your qa reviews???" after a QA
pass that called a grep/diff checklist "the standard geometry." The correction
(memory, verbatim): "No prose decoration for wording. That is equivalent to
hallucinating behavior." The response was to actually RUN the geometry — the
shuffle-null calibration (gate-0B) on the live coupling engine. It failed, and the
failure was the most valuable output of the session.

## The claim under test

The organism scoring engine (`organism/canonical_coupling_ai.py`) carries coupling
matrices COUPLING_CORE (15 pairs) + COUPLING_FLEET (6 pairs). Downstream docs claimed
the coupling term measures structural "brilliant connections" / synergy / band
structure, and an admission test of the form "coupled composite > decoupled sum"
certified them.

## Executed test (reproduce verbatim)

```python
import sys; sys.path.insert(0, '/<workspace>')
import organism.canonical_coupling_ai as eng
from organism.canonical_coupling_ai import composite
import random, statistics

def delta(scores):
    r_with = composite(scores, fleet_mode=True)
    c_core, c_fleet = eng.COUPLING_CORE, eng.COUPLING_FLEET
    eng.COUPLING_CORE, eng.COUPLING_FLEET = {}, {}      # zero DATA, not functions
    r_without = composite(scores, fleet_mode=True)
    eng.COUPLING_CORE, eng.COUPLING_FLEET = c_core, c_fleet  # restore
    return r_with - r_without

random.seed(42)
DIMS = ['COG','ADAPT','KNOW','RES','INTER','PIPE']
vectors = []
for i in range(200):
    level = random.uniform(0.3, 0.95)
    vectors.append({k: min(1.0, max(0.0, level + random.gauss(0, 0.08))) for k in DIMS})

d_real = [delta(v) for v in vectors]
d_null = []
for v in vectors:                       # shuffle-label null: same marginals
    vals = list(v.values()); random.shuffle(vals)
    d_null.append(delta(dict(zip(DIMS, vals))))
```

## Results (live numbers)

| Probe | Result | Meaning |
|---|---|---|
| Real deltas (n=200) | mean +0.8385, sd 0.2269 | coupling contributes 83.9 pts of composite |
| Shuffle null (n=200) | mean +0.8386, sd 0.2268 | label order is irrelevant to the contribution |
| Welch z | -0.00 | NOT separable from label noise |
| Perm wiggle (50 shuffles) | max 6.17e-3 | structure worth <1% of the term |
| Per-dim variance (jitter sd 0.02) | 1.1-1.8e-5 (COG max) | offset dominates; dims weakly alive |
| Composite range | 0.000 (all-zero) -> 1.273 (all-one) | scale reference |

## Verdicts issued

- KILLED: entourage/field-effect claims for INTER/coupling (it measures a constant);
  "coupled > decoupled" admission test (fires identically on noise); any S0 model
  separation claim leaning on a coupling SIGNATURE.
- SURVIVED: engine as deterministic scorer; curvature/volatility on score histories
  (orthogonal computation); per-dimension signals (weak but real); event capture.
- REQUIRED REDESIGN: double-centered normalization (cancel the uniform offset) or
  construct-specific coupling matrices; acceptance test = re-run THIS null and see
  z > 3 with a non-trivial structure share.

## Trap hit on the first attempt (do not repeat)

Attempt 1 neutralized attributes by name-pattern (`attr if "COUPL" in attr.upper()`)
which caught FUNCTIONS (`get_coupling_matrix`, `get_kappa`) alongside the data dicts,
and setattr-{}-ing a function is a no-op that looks like success. The corrected probe
zeroes exactly the two DATA dicts. Lesson: neutralization must target data, verified
by type inspection, never name patterns.

## Standing rule born here

Every scoring/structure claim gets its shuffle-null before any verdict is banked, and
a method name (geometry, physics-informed, adversarial) may appear in a report ONLY
with its execution record attached. Naming a method without running it = fabricated
behavior claim.
