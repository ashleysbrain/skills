# Pipeline Data Flow Bugs — Pass 2 (2026-08-08 session 2)

After the original 14-bug fix, a second line-by-line trace found 8 MORE gaps.
Several were in the FIXES themselves (bugs introduced while fixing the original bugs).

## The KEY-NAME MISMATCH Pattern (3 CRITICAL bugs)

The #1 class of data flow bug: upstream stages store results under key X,
downstream stages read key Y. No error thrown — just silently returns the
`.get()` default (empty string/dict). Data never arrives.

### Bug 1: Stage 2 -> Stage 4 research keys
```
Stage 2 WRITES: result["arxiv_results"], result["openalex_results"], ...
Stage 4 READS:  s2.get("papers", s2.get("findings", {}))
Result: research_context = "{}" — Wernicke drafts from raw idea only.
```

### Bug 2: Stage 3.5 -> Stage 4 narrative keys
```
Stage 3.5 WRITES: result["narrative_structure"], result["section_outline"]
Stage 4 READS:    s35.get("narrative", s35.get("outline", ""))
Result: narrative = "" — narrative architecture never reaches drafting.
```

### Bug 3: Stage 3.5 -> Stage 4.6 same keys
```
Stage 4.6 READS: s35.get("narrative", "")
Same mismatch. Expansion prompt falls back to "Standard academic structure".
```

**Detection method:** For every stage-to-stage data handoff, grep the exact key
written and the exact key read. They MUST match. This is the single highest-value
audit step for multi-stage pipelines.

## Bugs Introduced BY Fixing Other Bugs

### Type-safety crash: dict passed where string expected
When fixing Bug 3, the narrative key was corrected but `narrative_structure` can be
a dict (not a string). The downstream code does `narrative[:500]` which throws
`TypeError: unhashable type: 'slice'` on a dict.

**Fix:** Always type-check before slicing:
```python
if not isinstance(narrative, str):
    narrative = json.dumps(narrative)
```

### Revision overwrite: short response replaces full draft
When fixing the orphaned revision bug (writing revised_draft back to current_draft),
the guard was `len(revised_text.split()) > 50`. But Wernicke receives `[:2000]` chars
and may return a 200-word revision snippet. That 200-word snippet REPLACES the 4000-word
draft. The pipeline then ships 200 words.

**Fix:** Length-relative guard:
```python
if revised_len > 50 and revised_len >= orig_len * 0.6:
    self.state.current_draft = revised_text
```

### F-string syntax error from patch tool
The patch tool double-escaped `\n` in f-strings (`\\n\\n` instead of `\n\n`). This
produced literal backslash-n in the string instead of newlines. Python's ast.parse()
passed but runtime execution failed.

**Fix:** After patching f-strings, read back the exact bytes and verify `\\n` is not
present when `\n` was intended.

## Output Truncation Bug

`_extract_draft_content()` truncated the final output to `[:port]` chars.
A 4000-word paper (~24000 chars) lost 66% of content in the API response.
User saw only 1/3 of the generated draft.

**Fix:** Increase to `[:50000]` or remove truncation entirely.

## The Redundant Cleanup Block

A prior session added a simple `.replace()` cleanup block AFTER the comprehensive
regex cleanup. It had a syntax error (`f"...{dict.get(\"key\")}..."` — double quotes
inside double quotes in an f-string). This syntax error crashed the entire pipeline
at runtime even though `ast.parse()` reported success.

**Lesson:** `ast.parse()` is necessary but not sufficient. The Python runtime f-string
parser is stricter in some versions. Always run the actual function, not just parse it.
