---
name: pipeline-dead-code-audit
description: Audit Python pipelines for dead functions and engine gaps.
---

# Pipeline Dead Code Audit

Multi-pass methodology for auditing large Python pipeline files (1000+ lines) for dead code, uncalled engines, and structural inconsistencies. Developed auditing VERITAS (3212 lines) and CRUCIBLE (3210 lines) research pipelines.

## When to Use
- Auditing a pipeline after adding many functions across multiple sessions
- Verifying that all engine calls resolve to defined engines
- Checking that stage lists match stage engine configs
- Pre-deployment dead code sweep

## The 6-Pass Audit

### Pass 1: Syntax + Import
```python
compile(code, filename, 'exec')
```
Run for every file. Catches indentation errors from patch operations.

### Pass 2: Engine Routing
Extract engine names from the ENGINES dict, compare against `engine_post("name", ...)` calls.
```python
defined = set(re.findall(r'^\s*"(\w+)":\s*\{', engines_dict_body, re.MULTILINE))
called = set(re.findall(r'engine_post\(["\'](\w+)["\']', code))
uncalled = defined - called
undefined = called - defined
```

### Pass 3: Dead Functions (CRITICAL PITFALL)
Stage methods are referenced in stages lists as `self.stage0_evidence_gate` WITHOUT parentheses. A naive `func(` search will flag them as dead.

**Wrong:** `re.findall(rf'{func}\(', code)` — misses method references in lists
**Right:** `re.findall(rf'\b{func}\b', code)` — word-boundary catches all references

Subtract 1 for the `def` line. Skip private methods (`_func`), `main`, `__init__`.

### Pass 4: Stage Consistency
```python
se_stages = set(re.findall(r'(\d+\.?\d*):', STAGE_ENGINES_body))
run_stages = set(re.findall(r'\((\d+\.?\d*),', stages_list_body))
mismatch = se_stages.symmetric_difference(run_stages)
```

### Pass 5: Cross-Pipeline Parity
If maintaining parallel pipelines (VERITAS/CRUCIBLE), verify both use identical engine sets.

## Wiring Dead Functions
When you find dead functions, they typically fall into these categories:

| Category | Example | Where to wire |
|---|---|---|
| Pre-submission generators | cover_letter, reviewer_template | Stage 7 output package |
| Tech validation checks | code_syntax, threat_model | Stage 7 tech_checks dict |
| LaTeX functions | generate_latex, compile, package | Stage 7 LaTeX pipeline |
| CircuitBreaker methods | is_open, record_success, record_failure | engine_post wrapper |
| SLA tracking | record_stage_time, get_sla_status | Run loop timing |
| Health check utilities | gate_single | gate_stage per-engine loop |
| Coherence checks | stage5_5_coherence_check | Add to stages list + STAGE_ENGINES |

### Pass 6: Data Flow Trace (CRITICAL — catches silent failures)

The dead code audit checks whether functions are CALLED. The data flow trace checks
whether stages actually RECEIVE data from the stages they depend on. A pipeline can
have zero dead code and still produce garbage because stage outputs are orphaned.

**The `str(dict)` / `json.dumps(dict)` bug pattern:** When an engine returns a nested
dict like `{"result": {"result": {"body": "actual prose..."}}}`, code that does
`str(response.get("result", ""))` or `json.dumps(stage_results[4])` passes the DICT
REPRESENTATION to quality checkers — not the prose. Every gate then "passes" because
it is scanning JSON keys, not written content. This is the #1 silent failure in DS
content pipelines.

**Trace method:**
```python
import re
# For each stage function, extract:
# 1. What stage_results it reads from
reads = re.findall(r'self\.state\.stage_results\.get\((\d+\.?\d*)', func_body)
# 2. What stage_results it writes to
writes = re.findall(r'self\.state\.stage_results\[(\d+\.?\d*)\]\s*=', func_body)
# 3. Whether it passes raw dicts (str/json.dumps) or extracted text to engines
dict_passes = re.findall(r'json\.dumps\(.*?stage_results', func_body)
str_passes = re.findall(r'str\(.*?\.get\(', func_body)
```

**What to flag:**
- Writing stages (4, 4.5, 4.6, 6) whose output is never READ by a later stage
- Reading stages (5, 7, 7.5) that read stage 4 instead of the latest written version
- **Key-name mismatches between writer and reader stages** — the #1 silent data loss
  pattern. Stage X writes `result["arxiv_results"]`, stage Y reads `s2.get("papers")`.
  No error — just empty data. Grep the EXACT key written vs the EXACT key read.
- Any `json.dumps(stage_results[N])` or `str(response.get("result", ""))` passed to
  an engine endpoint as `"text"` or `"idea"` — these pass dicts, not prose
- Any `[:500]` or `[:2000]` truncation on draft text before it reaches a quality gate
- Any `json.dumps()` wrapping when the target engine expects plain text
- **Type mismatches after key fixes** — correcting a key name may now return a dict
  where downstream expects a string. Add `isinstance(x, str)` guards before slicing.

**The shared-state fix:** Multi-stage content pipelines need a `current_draft` field
that every writing stage UPDATES and every reading stage READS. Without it, each stage
works on its own isolated copy and improvements are lost.

See: `references/pipeline-data-flow-bugs.md` for the 14-bug case study from VERITAS.
See: `references/pipeline-data-flow-bugs-pass2.md` for 8 more gaps found in the fix-pass,
including key-name mismatches, type-safety crashes, and bugs introduced by fixing other bugs.

### Pass 6b: Citation Filter Starvation (caught 2026-08-12)

A pipeline can gather 15 relevant papers in stage 2 but only pass 3 to the
writer in stage 4.6 because a relevance filter silently rejects the rest.
The `_progressive_draft()` function filters `self.state.citations[:12]` by
keyword overlap with the idea text. Two bugs starved non-DS topics:

1. **Keyword extraction threshold** — `len(word) > 4` drops short critical
   terms: "Bach" (4 chars), "DNA", "RNA", "fMRI", "T-cell". Lower to `>= 3`
   with alphanumeric cleaning (`"".join(c for c in word if c.isalnum())`).

2. **Match threshold too high + domain-specific bypass** — `matches >= 2`
   rejects papers matching only 1 keyword. A paper titled "FUGUE EXPOSITION"
   matches only "fugue" (1 match) and gets filtered out. Combined with a
   DS-only bypass list (`["interocept", "predict", "psychiatr", ...]`),
   non-DS topics lose 75% of their evidence base. Fix: `matches >= 1`,
   remove domain-specific bypass lists entirely.

**Detection method:** Load the checkpoint state JSON and simulate the
filter against the stored citations. If <40% of gathered papers pass,
the writer is evidence-starved and the draft will have thin citations.

```python
import json
state = json.load(open(state_path))
citations = state.get("citations", [])
keywords = {w.lower() for w in idea.split() if len(w) > 3}
passed = [c for c in citations[:12]
          if sum(1 for kw in keywords
                 if kw in (c.get("title","")+c.get("abstract","")).lower()) >= 2]
print(f"Passed: {len(passed)}/{len(citations[:12])} — {'STARVED' if len(passed) < 4 else 'OK'}")
```

## Verification After Wiring
1. Re-run dead function audit (should show 0 dead)
2. Run data flow trace (Pass 6 — should show 0 orphaned stages)
3. Syntax check both files
4. Health check: `python3 pipeline.py --health-check`
5. Push to GitHub

## Pitfall: Premature Optimization Destabilizes Working Code (learned 2026-08-08)

After fixing data flow bugs, I immediately added ThreadPoolExecutor
parallelization to stage 2 research gathering to "optimize." This caused
the server process to crash silently during API calls — no traceback, no
error, just a dead process. The parallelization was reverted to sequential.

**Rule:** Do NOT optimize while fixing bugs. Get the pipeline working
correctly FIRST. Run an end-to-end test. THEN consider optimizations one
at a time, testing after each. Parallelization in particular can cause
silent process crashes in long-running servers that are extremely hard
to debug because the process is gone before you can inspect it.

**Rule:** `ast.parse()` passing does NOT mean the code will run. Always
execute the actual function. F-string quoting errors (`f"...{x.get("k")}..."`)
parse fine syntactically in some Python versions but fail at runtime.

**Rule:** The patch tool can double-escape `\n` to `\\n` in f-strings.
After patching any f-string, read back the exact line to verify newlines
are single-escaped.
