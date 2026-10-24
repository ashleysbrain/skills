# Missing Module Interface Recovery

Technique for when a consuming file imports from a module that was never built
(planned abstraction layer that was never implemented). Instead of stubbing or
disabling the import, reverse-engineer the expected interface from the consuming
code and build the real module.

## When to Use

- A file fails at import time: `ModuleNotFoundError: No module named 'X'`
- `git log -S "def function_name"` shows the module was never written (not deleted)
- The consuming code has clear usage patterns you can infer the contract from
- The missing module is an abstraction layer (adapters, bridges, fusion layers)

## The Recovery Process

### 1. Map All Import Sites

Find every place the missing module is imported and what symbols are pulled:

```python
# Using search_files for "from missing_module import" or "import missing_module"
# List every imported symbol — these are your required public API
```

### 2. Trace Every Call Site

For each imported symbol, find where it's called in the consuming code:

```
build_baseline_inputs()         → must return 8-tuple of Input dataclasses
build_baseline_confidence(tag)  → must return 8-tuple of floats
adapt_transcript(text)          → must return (inputs_tuple, confidence_tuple)
merge_inputs(base, bc, t, tc)   → must return (merged_tuple, merged_confidence_tuple)
```

Read the consuming code lines AFTER each call to see what attributes/methods
are accessed on the return value. This reveals the full object contract:

```
bundle.coverage                  → EvidenceBundle needs .coverage property (float)
bundle.overall_confidence        → needs .overall_confidence property (float)
bundle.to_summary()              → needs .to_summary() method returning dict
bundle.dimension_confidence(dim) → needs method taking dimension name string
bundle.low_confidence_fields()   → needs method with threshold= kwarg
```

### 3. Find Existing Building Blocks

Before writing new logic, check what already exists that can be wired together:

- Calibration files (JSON/YAML) that hold baseline values
- Existing extraction functions in the consuming file (regex/keyword patterns)
- Dataclass definitions in the core engine (Input types, Result types)
- Database tables that hold the data the module would query

### 4. Build the Module

Construct the module by wiring existing pieces:

```
input_adapters/__init__.py:
  - build_baseline_inputs() → instantiate Input dataclasses with calibration midpoints
  - merge_inputs() → confidence-weighted field blending using dataclasses.replace
  - EvidenceBundle class → implements .coverage/.overall_confidence/.to_summary()

input_adapters/transcript_adapter.py:
  - adapt_transcript() → keyword/regex extraction (reuse patterns from consuming file)
  - Returns (inputs, confidence) where confidence = evidence density per dimension
```

### 5. Verify End-to-End

Test the FULL consuming pipeline, not just the module in isolation:

```python
# Import the file that was broken
import score_from_evidence
# Call the function that uses all the missing imports
dims, baseline, bridge, pipeline = score_from_evidence.score_transcript_with_real_pipeline(text)
# Verify the expected fields are populated
assert pipeline["kappa_3d_sum"] is not None
```

## Key Insight

Missing modules are usually planned abstraction layers where the consuming code
was written first (top-down design) but the implementation never followed. The
consuming code IS the spec — read it carefully and the interface reveals itself.
The technique is read-the-consumer, not guess-the-design.

## Pitfall: Returning Dicts Instead of Objects

If the consuming code accesses attributes (`bundle.coverage`, not
`bundle["coverage"]`), you must return an object with those attributes, not a
dict. Check for dot-access vs bracket-access before choosing the return type.
When in doubt, build a lightweight class with the required properties/methods.

## Real Example (2026-06-29)

`health-private/score_from_evidence.py` imported `build_baseline_inputs`,
`adapt_transcript`, `merge_inputs`, `build_bundle_from_merged` from a
nonexistent `input_adapters` module, and `build_adhd_fusion` from a nonexistent
`adhd_fusion` module. Both modules were planned but never built.

Recovery: traced all import sites, found the consuming code expected an
`EvidenceBundle` object with `.coverage`/`.to_summary()`/`.dimension_confidence()`,
built both modules by wiring calibration.json + Input dataclasses + keyword
extraction patterns already present in the consuming file. Verified end-to-end:
transcript pipeline produced `engine=calculator_v4+support` with rank-3 triples
flowing. Took ~20 minutes vs. the alternative of disabling the import path.
