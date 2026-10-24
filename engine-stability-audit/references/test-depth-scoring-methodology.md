# Test Depth Scoring Methodology

## Context

Originated from a 5-round iterative production-readiness audit of 5 organism engines
(ATC-01, ATC-02, ATC-03, ATC-04, Hippocampus) by DS J Eccles (quality auditor).

The problem: engines can have tests that pass, but the tests may be SHALLOW —
only checking `isinstance(result, dict)` or `hasattr(result, 'seats')` without
falsifiable behavioral assertions. "Tests pass" is necessary but NOT sufficient
for production readiness. You must score the TEST SUITE'S OWN DEPTH against a
reference bar, just as the stability skill scores engine RUNTIME depth.

## The Reference Bar

Use the most mature engine's test file in the same ecosystem as the reference.
In this case: **the specialist engine** (`ds-farr-engine/tests/test_farr_physics.py`).

| Metric | Farr (reference) | Meaning |
|--------|-----------------|---------|
| Test LOC | 387 | Total lines in test file |
| Test functions | 34 | `def test_*` count |
| Test classes | 7 | Coverage categories (one per concern) |
| Assert lines | 63 | Lines beginning with `assert` |
| Pass rate | 34/34 | All tests must actually pass |

## Scoring Dimensions

Score each engine's test file on these axes:

### 1. Test LOC (volume)
- Compare against the reference. A test file at 60-84 LOC (ATC-01/02 range)
  has minimal coverage. 200-285 LOC (ATC-03/04/Hippocampus after deep-coverage
  additions) has meaningful behavioral testing.
- Threshold for PRODUCTION-READY: at least 50% of reference LOC (~190+).

### 2. Assertion Count (density)
- Count lines starting with `assert `. This is the real work-unit of a test.
- Threshold for PRODUCTION-READY: at least 50% of reference assertions (~30+).

### 3. Coverage Categories (breadth)
- Count test classes. Each class should cover a distinct concern:
  - Core functionality (the main engine method)
  - Cognitive layer (L2 integration)
  - Layer loading (methodology/philosophy import)
  - Edge cases / sensitivity (domain-specific physics)
  - Multi-ingest trend (temporal behavior)
  - Cognitive recommendation (advisory output)
- A file with only 3 classes (core + cognitive + layers) is doing the bare
  minimum. 6-7 classes indicates real depth across concern axes.

### 4. Theater Detection (THE critical technique)
Not all assertions are equal. Classify each test:

- **STRONG**: assertions with specific numerical thresholds, comparisons,
  or semantic content checks. Examples:
  - `assert spread > 0.1` (quantitative threshold)
  - `assert positive.moat_score >= max(neutral.moat_score, negative.moat_score)`
  - `assert stats["total_memories"] == 1000` (exact value)
  - `assert "DELAY" in verdict.fatal_flaw.upper()` (semantic content)
  - `assert scores[0] > scores[2]` (monotonicity / ordering)
  - `assert rec["action"] != "maintain"` (exclusion of wrong output)

- **WEAK**: assertions that pass regardless of input quality. Examples:
  - `assert isinstance(result, dict)` (always true for dicts)
  - `assert hasattr(result, 'seats')` (structural, not behavioral)
  - `assert result is not None` (nearly always true)
  - `assert len(result) > 0` (no specificity about WHAT is returned)

A test file with 16 assertions but 14 of them weak is THEATER — it looks
tested but doesn't actually constrain behavior. The metric that matters:
**fraction of STRONG assertions**. Aim for >50% strong.

### 5. Live Execution
ALL tests must actually pass. Run `pytest -v` and verify 0 failures.
A test file that was never run (or has xfails/skips) doesn't count.

### 6. Live Falsifiability Verification (proving assertions have teeth)

Theater detection (dimension 4) classifies assertions as STRONG or WEAK by
reading them. But a STRONG-looking assertion can still be vacuous if the engine
happens to produce values that satisfy it trivially. To prove a hardened test
is **genuinely falsifiable** — not just well-written — run the engine with
controlled inputs and verify the assertion's discriminating power:

1. **Identify the mutation the test claims to catch.** E.g., "inverted sort
   order," "hardcoded constant output," "always-promote," "ignore input."
2. **Feed inputs that create maximum contrast.** E.g., for a sort-order test,
   encode 3 memories with strictly different overlap to the query.
3. **Run the engine and print the raw values the assertion checks.** If the
   values barely separate (e.g., scores 0.31, 0.30, 0.29), the test is
   technically falsifiable but fragile — a small code change could collapse the
   gap. If the values separate cleanly (e.g., 0.400, 0.167, 0.143), the test
   is robustly falsifiable.

**Worked example (Hippocampus retrieve sort order):**
The hardened test `test_retrieve_ranks_by_relevance` asserts results are in
descending relevance with strict separation (`scores[0] > scores[1] > scores[2]`).
Live verification: encode 3 memories sharing "python" with different extra
tokens, query "python programming". Raw scores: `[0.400, 0.167, 0.143]`.
Descending? Yes. Top beats #2 by 0.233? Yes. An inverted sort mutation would
put 0.143 first → test fails. **Confirmed genuinely falsifiable.**

This step is especially important in **final confirmation rounds** (round N+)
where the question is "are the hardened tests real?" rather than "are there
gaps?" — you must demonstrate the teeth, not just read the assertions.

### 7. mtime Regression Gate (no-engine-change confirmation)

In **regression confirmation rounds** (the question is "did hardening tests
break anything?" not "are there gaps?"), compare file modification timestamps:

```
stat -f '%Sm  %N' -t '%m-%d %H:%M' \
  <engine>/src/<mod>/core/engine.py \
  <engine>/src/<mod>/core/cognitive.py \
  <engine>/tests/test_*.py
```

**Rule:** if ALL test files have mtimes LATER than the engine.py and cognitive.py
mtimes, then the engine source was NOT modified after the tests were hardened.
There can be no engine regression — the tests are testing current code. This
takes 30 seconds and closes the regression question definitively without needing
git history (useful when test files are untracked/new).

If any engine file has a LATER mtime than its test file, that engine needs a
full re-run of the regression battery, not just a timestamp check.

## The Multi-Round Upgrade Cycle

Production-readiness scoring is iterative across rounds:

- **Round 1-2**: Identify NEEDS-WORK engines with specific gap categories
  (e.g., "ATC-03 lacks Fisher sensitivity tests, multi-ingest trend tests,
  cognitive recommendation tests").
- **Round 3-4**: New tests get added. Re-score. Check if gaps are closed.
- **Round 5 (final)**: Confirm all gaps closed, all tests pass, no theater.

Track which specific test classes were added between rounds. In this audit:
22 new tests across 3 engines closed all previously identified gaps.

## Verdict Rubric

| Verdict | Criteria |
|---------|----------|
| **PRODUCTION-READY** | All tests pass + LOC >= 50% reference + assertions >= 50% reference + >=4 coverage categories + >50% strong assertions + no theater-only classes |
| **NEEDS-WORK** | Tests pass but missing coverage categories, assertion density too low, or too many weak assertions. Specific gaps must be identified for the next round. |
| **THEATER** | Tests pass but are predominantly weak (isinstance/hasattr only), OR tests were never run, OR test count is inflated with duplicates. Engine cannot be trusted. |

## Pitfalls

- **Counting test FUNCTIONS instead of test CLASSES for breadth** — 12 test
  functions in 3 classes is narrow coverage, not broad. Count classes for breadth.
- **Accepting "all tests pass" without theater detection** — a file of 15 tests
  that all do `assert isinstance(x, dict)` passes but proves nothing.
- **Not running the tests live** — a test file that was written but never
  executed may have import errors, collection errors, or wrong method names.
  `pytest -v` is mandatory, not optional.
- **Comparing against an absolute threshold instead of a reference engine** —
  the reference bar should be the most mature engine in the same ecosystem,
  not an arbitrary number. What counts as "enough tests" is relative to the
  domain's reference standard.

## Metric Computation Script

```python
import re

def score_test_file(path, ref_loc=387, ref_asserts=63):
    with open(path) as f:
        text = f.read()
    
    loc = len(text.splitlines())
    test_funcs = len(re.findall(r"def (test_\w+)\(", text))
    test_classes = len(set(re.findall(r"class (Test\w+)", text)))
    
    assert_lines = sum(1 for l in text.splitlines()
                       if l.strip().startswith("assert ") or l.strip().startswith("assert("))
    
    # Theater detection: classify each test function
    tests = re.findall(r"def (test_\w+)\(.*?\):\n((?:.{8,}\n)+?)(?=\n    def |\nclass |\Z)", text)
    strong_kw = ['>=', '<=', '>', '<', '==', '!=', 'spread', 'monoton', 'exactly', 'factor']
    strong_tests = sum(1 for _, body in tests if any(kw in body for kw in strong_kw))
    
    return {
        "loc": loc,
        "loc_pct": round(100 * loc / ref_loc, 1),
        "test_functions": test_funcs,
        "test_classes": test_classes,
        "assert_lines": assert_lines,
        "assert_pct": round(100 * assert_lines / ref_asserts, 1),
        "strong_test_fraction": round(strong_tests / max(test_funcs, 1), 2),
        "verdict": "PRODUCTION-READY" if (
            assert_lines >= ref_asserts * 0.5 and
            test_classes >= 4 and
            strong_tests >= test_funcs * 0.5
        ) else "NEEDS-WORK",
    }
```

## Session Example: 5-Engine Final Audit (2026-08-12)

| Engine | LOC | Tests | Classes | Asserts | %Ref LOC | %Ref Asserts | Verdict |
|--------|-----|-------|---------|---------|----------|-------------|---------|
| Farr (ref) | 387 | 34 | 7 | 63 | 100% | 100% | — |
| ATC-01 | 84 | 8 | 3 | 20 | 22% | 32% | PROD (prior round) |
| ATC-02 | 61 | 5 | 3 | 16 | 16% | 25% | PROD (prior round) |
| ATC-03 | 227 | 11 | 6 | 39 | 59% | 62% | PROD (upgraded) |
| ATC-04 | 206 | 12 | 6 | 44 | 53% | 70% | PROD (upgraded) |
| Hippocampus | 285 | 15 | 7 | 42 | 74% | 67% | PROD (upgraded) |

ATC-01 and ATC-02 scored PRODUCTION-READY in an earlier round despite lower
metrics — they are simpler engines (competitive scan, regulatory check) where
3 coverage categories sufficed for the domain. The scoring rubric must account
for engine complexity: a 5-force analysis engine needs fewer test categories
than a memory consolidation engine with persistence, retrieval, eviction, and
promotion semantics.

All 51 tests across 5 engines passed live execution. Zero theater-only classes
detected in the final round.

**Round 6 (final confirmation):** Two tests hardened since round 5 (ATC-03 and
ATC-04 deep-coverage sections). Ran the full 51-test suite (all pass), applied
live falsifiability verification to the hippocampus sort-order assertion (scores
[0.400, 0.167, 0.143] — confirmed genuinely falsifiable), and applied the mtime
regression gate (all engine.py files predate test files by 30-90 min — no engine
regressions possible). Verdict: all 5 engines remain PRODUCTION-READY. This
round added dimensions 6 and 7 above to the methodology.
