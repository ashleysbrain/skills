# Graph Perturbation Experiment Audit Patterns

Detection recipes for Checks 15-18 from the parent SKILL.md.
Derived from the Physiomorphic AI arXiv manuscript hostile review (2026-07-10).

---

## Check 15: Degenerate Control + Baseline Omission

### The Pattern

A perturbation experiment compares a structured (biologically organized, domain-informed) graph against a "randomized" control. The randomization method structurally cripples the control under the experiment's own functional rule, making the reported advantage partly or entirely tautological.

The key signal: the treatment-vs-control gap at minimal perturbation is already very large. This means the control is broken at rest, not that the treatment is robust under stress.

### How to Detect

1. Read the functional rule. (e.g., "component survives only if all transitive dependencies survive")
2. Read the control construction. (e.g., "edge-count-matched random rewiring of directed dependencies")
3. Ask: does the rewiring create spurious cycles, inflate path lengths, or generate long chains that the functional rule would mechanically punish?
4. Check whether the 0% removal baseline is reported.
5. Look for gap amplification: treatment-vs-control ratio at minimal perturbation (10% removal). If 3:1 or greater, the control is likely degenerate.

### Worked Example: Physiomorphic AI (2026-07-10)

**Setup:**
- Treatment: biologically organized dependency graph (100+ nodes)
- Control: edge-count-matched random rewiring of directed dependencies
- Functional rule: component is functional only if it survives AND all transitive dependencies survive
- Metric: normalized functional capacity under 10-50% random component removal
- 100 seeds x 100 trials per removal level = 10,000 trials per data point

**The signal:**

| Removal % | Isomorphic | Random Control | Ratio |
|-----------|-----------|----------------|-------|
| 10% | 0.623 | 0.180 | 3.46x |
| 20% | 0.443 | 0.121 | 3.66x |
| 30% | 0.337 | 0.095 | 3.55x |
| 40% | 0.244 | 0.072 | 3.39x |
| 50% | 0.173 | 0.057 | 3.04x |

At 10% removal (90% of nodes still present), the random control retains only 18% functional capacity. This is not a perturbation effect. The random rewiring itself has already destroyed 82% of functional capacity before any nodes are removed. Random directed edges create spurious dependency cycles, making most components non-functional even at full strength.

**What the paper did right:** Acknowledged that "random rewiring changed degree distribution, path structure, cycles, and dependency depth" and that "the functional rule also favors architectures with fewer or shallower dependencies." Explicitly stated: "It does not show that biological isomorphism caused the difference."

**What was missing:** No 0% removal baseline reported. The reader cannot quantify how much of the 0.259 mean advantage is control degeneracy vs genuine treatment resilience.

### Remediation Options

1. **Report 0% baseline:** Show functional capacity at zero removal for both conditions. If the control starts at, say, 0.25, the entire comparison is reframed.
2. **Better control:** Use a degree-sequence-preserving (configuration model) control or a depth-matched control instead of raw edge rewiring.
3. **Explicit acknowledgment:** State that the random control's baseline functional capacity is already degraded by the rewiring and the advantage partly reflects that.

### Severity Classification

- If the paper does NOT acknowledge the control weakness at all: severity-2 (major methodology flaw)
- If the paper acknowledges it qualitatively but omits the baseline: severity-3 (minor, transparency gap)
- If the paper reports the baseline or uses matched controls: no finding

---

## Check 16: Reproducibility-Statement vs Included-Code Mismatch

### The Pattern

A Data and Code statement says "aggregate results and the figure-generation script are included with the source package." But the included script imports a proprietary module not in the package, meaning it will fail if run. The statement implies reproducibility that does not exist.

### How to Detect

1. Open every included `.py` script.
2. Check the import block: does any import from a path or module not in the package?
3. Check for `os.environ.get(...)` pointing to external paths.
4. Check for hardcoded absolute paths (e.g., `/<workspace>`).
5. Run mentally: if you executed this script fresh, would it succeed?

### Worked Example: Physiomorphic AI (2026-07-10)

**The claim (manuscript line 228):**
> Aggregate results and the figure-generation script used for this manuscript are included with the source package.

**The code (`generate_results.py` lines 18-21):**
```python
GG_PATH = Path(os.environ.get("GG_ORGANISM_PATH", "/<workspace>"))
sys.path.insert(0, str(GG_PATH))
from cascade_failure_sim import run_cascade_experiment
```

The script imports `cascade_failure_sim` from a proprietary path not in the arXiv package. Running `generate_results.py` as distributed will fail with `ModuleNotFoundError`. The script also runs the full simulation (lines 27-29), not just plotting from the JSON.

**The fix:** Change the statement to:
> "Aggregate results, the pre-generated figure, and the full simulation-plus-plotting script are included with the source package. The simulation script requires the proprietary cascade_failure_sim module, which is not distributed; only the aggregate JSON and figure PDF are directly usable from the package alone."

---

## Check 17: Proxy-Score Denominator Transparency

### The Pattern

A composite proxy score reports values like `1.0000` and `0.5000` to four decimal places. These are likely exact fractions (N/N, M/N) but are presented without numerator/denominator context. A reader cannot assess what the proxy measures or whether the precision is meaningful.

### How to Detect

1. Scan reported proxy values for suspiciously exact fractions at high precision.
2. Check whether the paper states the basis for each (e.g., "97 of 97 components registered").
3. If values like 1.0000 or 0.5000 appear without a fraction, flag as a transparency gap.

### Worked Example: Physiomorphic AI (2026-07-10)

The proxy isomorphism score was reported as:
```
I_hat = (1.0000 + 0.5000 + 0.9919 + 0.7143) / 4 = 0.8016
```

- `C_c = 1.0000` — likely "all N components registered" but N is not stated
- `C_f = 0.5000` — likely "M of N roles keyword-matched" but M and N are not stated
- `C_r = 0.9919` — appears to be a measured value, but denominator unknown
- `C_o = 0.7143` — likely "5 of 7 mechanisms present" (5/7 = 0.71428...) but not stated

**The fix:** Add one sentence: "The proxy values derive from N/N components registered, M/N roles keyword-matched, [reference integrity details], and 5/7 mechanisms present."

---

## Check 18: Construct Overlap Between Scoring Dimensions and Outcome Measures

### The Pattern

A composite score has a dimension measuring properties of the same artifact used as the outcome in a downstream experiment. The score and outcome share a data source, creating non-independence that inflates apparent validation.

### How to Detect

1. List each scoring dimension and what artifact/data it draws from.
2. List the outcome measure and what artifact/data it draws from.
3. Identify overlap: same graph? same registry? same metadata?
4. Flag if a dimension and the outcome share a data source.

### Worked Example: Physiomorphic AI (2026-07-10)

**Scoring dimension C_r (relational correspondence proxy):**
- Measures: dependency-reference integrity of the the operator agent registry
- Score: 0.9919
- Source: the dependency graph metadata in the the operator agent organism registry

**Outcome measure (perturbation experiment):**
- Measures: retained functional capacity under component removal
- Source: the dependency graph topology of the the operator agent organism

**The overlap:** Both C_r and the perturbation outcome draw from the same dependency graph artifact. A well-maintained registry (high C_r) likely correlates with a clean dependency topology (high resilience under the transitive-dependency survival rule). The perturbation result is therefore not fully independent of the C_r component of the isomorphism score.

**What the paper did right:** The anti-circularity section (4.2) correctly excludes robustness from C_o and requires blinded review. The C_r proxy measures metadata quality, not topology directly.

**What was missing:** The paper does not note that C_r and the perturbation outcome share a data source (the dependency graph), which is a form of construct overlap even if not direct circularity.

**Severity:** Low. The overlap is indirect (metadata quality vs topology resilience), and the paper's caveats about the proxy score being a "registry-completeness proxy" partially cover this. But explicit acknowledgment would strengthen the paper's anti-circularity argument.

---

## Cross-Check: Statistical Reporting for Perturbation Experiments

When auditing a graph perturbation experiment, verify these statistical items:

| Item | What to Check | Common Failure |
|------|---------------|----------------|
| Unit of analysis | Are SDs computed across runs (independent seeds) or across pooled trials? | Pooling trials from the same seed inflates N and deflates SD |
| Inferential test | Is any hypothesis test reported? | Many papers report only descriptives, which is fine if framed as illustrative |
| Pseudoreplication | Are "100 independent runs" truly independent systems or just randomization draws on one system? | 100 seeds on one architecture is not 100 independent architectures |
| Interval type | Is the reported interval a CI or a descriptive percentile range? | "Central 95% run interval" is descriptive, not inferential. Label must not say "CI" |
| Baseline reporting | Is the zero-perturbation condition reported for both treatment and control? | Omitting baseline hides control degeneracy (see Check 15) |

### Worked Example Scoring

The Physiomorphic AI manuscript scored well on statistical honesty:
- SDs computed across run means (correct unit)
- "Central 95% run interval" correctly labeled as non-inferential
- Pseudoreplication acknowledged ("No independent systems or deployment failures were tested")
- No inferential test reported, which is defensible for an illustrative case study

The only gap: baseline (0% removal) not reported, which is a Check 15 issue rather than a statistics issue per se.
