# Progressive Drafting Runtime Bugs (2026-08-10 session 10)

Three bugs found by running the pipeline and inspecting actual output after
the 3-pass progressive drafting (MT2) was wired into the run loop.

## Bug 1: Pass 3 Shrinks the Draft

**Symptom:** Pass 1 produces 3,313 words, Pass 2 produces 3,140 words, Pass 3
produces 944 words. The final draft is less than a third of Pass 2's output.

**Root cause:** Pass 3 prompt said "Tighten prose — remove filler, redundancy,
meta-commentary." The LLM interpreted this as aggressive deletion, cutting
entire paragraphs and sections. No length guard existed.

**Fix (3 layers):**
1. Changed Pass 3 prompt: removed "tighten/remove filler," added "Do NOT
   shorten the draft. Output must be at least as long as input. Polish
   sentence-by-sentence. Do NOT delete paragraphs or sections."
2. Added explicit word-count target: `Target: {len(pass2_text.split())}+ words.`
3. Added post-Pass-3 guard: if Pass 3 output < 70% of Pass 2 word count,
   discard Pass 3 and return Pass 2 instead. Log the decision.

```python
p2_words = len(pass2_text.split())
p3_words = len(pass3_text.split())
if p2_words > 500 and p3_words < p2_words * 0.7:
    print(f"Pass 3 shrunk draft ({p2_words} -> {p3_words}). Using Pass 2.")
    return pass2_text
```

## Bug 2: Citation Structure Mismatch in _progressive_draft

**Symptom:** Pass 1 draft has 0 citation markers despite 10+ papers gathered.

**Root cause:** Same flat-list-vs-nested-by-source bug as Stage 3 Toulmin
builder. `_progressive_draft` iterated `self.state.citations` expecting nested
`c.get("arxiv", [])` but citations are flat dicts: `{"source": "crossref",
"title": "...", "year": ..., "abstract": "..."}`. The inner loop found nothing,
produced an empty cite_context, and the LLM had no evidence to cite from.

**Fix:** Changed to flat-key access:
```python
for c in self.state.citations[:8]:
    if isinstance(c, dict):
        title = (c.get("title", "") or "")[:80]
        abstract = (c.get("abstract", "") or "")[:150]
        year = c.get("year", "")
        cite_context.append(f"[{len(cite_context)+1}] {title} ({year}) — {abstract}")
```

This is the SAME bug pattern as the Toulmin builder citations fix and the
Stage 4.6 fallback expansion citations fix. The flat-list-vs-nested-by-source
data structure mismatch recurs in every new method that reads
`self.state.citations`.

**General rule:** `self.state.citations` is a flat list of dicts with keys:
`source`, `doi`, `title`, `authors` (list), `year`, `abstract`. NEVER iterate
by source key. Always access flat keys directly.

## Bug 3: Stage 6 Revision Overwrites Draft with Dict Stringification

**Symptom:** After Stage 4.6 progressive drafting produces clean prose
(2,000+ words), the final `current_draft` in the checkpoint file is a
stringified dict: `{'status': 'ok', 'organ': "Temporal Lobe / Wernicke's
Area", 'result': {'headline': '...', 'body': 'REVISE t...'}}`

**Root cause:** Stage 6 revision_loop calls the specialist engine engine for revision.
Wernicke returns a nested dict response. Line 4104 did
`revised_text = str(wern_res.get("result", ""))`. `str()` on a dict produces
the dict's repr, not the body text. Then the length check
`revised_len >= orig_len * 0.6` passed because the dict-stringified text was
long enough. `current_draft` was overwritten with dict garbage.

**Fix:** Extract actual prose from the Wernicke response before comparison:
```python
wern_result = wern_res.get("result", "")
if isinstance(wern_result, dict):
    inner = wern_result.get("result", wern_result)
    if isinstance(inner, dict):
        revised_text = inner.get("body", "") or str(inner.get("body", ""))
    else:
        revised_text = str(inner)
else:
    revised_text = str(wern_result)
# Guard against dict-stringification
if revised_text.startswith("{") and "'status'" in revised_text[:50]:
    revised_text = ""
```

**General rule:** the specialist engine engine returns nested dict responses. ALWAYS
extract `.get("body", "")` from the innermost dict. NEVER `str()` a Wernicke
response directly. This applies to every stage that reads Wernicke revision
output (Stage 4, 4.5, 6).

## Bug 4: Pass 1 Prompt Missing Section Structure

**Symptom:** Draft has 0 `##` markdown headers despite Pass 1 prompt requesting
"content sections."

**Root cause:** Pass 1 prompt said "Write the content sections (Introduction,
each claim as a section, Discussion)" but didn't explicitly require `##` markdown
headers or specify the section structure.

**Fix:** Explicitly specified the section structure with markdown headers in the
prompt:
```
Write a FULL academic paper with these sections, each starting with ## markdown headers:
## Abstract
## 1. Introduction
## 2. [First sub-claim topic]
## 3. [Second sub-claim topic]
...
```

**General rule:** LLM prompts for structured academic output must explicitly
list the expected section headers in markdown format. "Write sections" is
insufficient; "Write these sections: ## Abstract, ## Introduction, ..." works.

## The Recurring Pattern: Reading state.citations

This is the THIRD time the flat-list-vs-nested-by-source bug has been found
and fixed in a different pipeline method. The pattern:

1. Old code (pre-Aug 2026) stored citations nested by source:
   `{"arxiv": [...], "openalex": [...]}`
2. After the citation flow fix (Aug 2026), citations are flat dicts
3. Every NEW method written after the fix still uses the old nested pattern
4. The method silently produces empty citation context → LLM fabricates

**Prevention:** Any new method that reads `self.state.citations` must use:
```python
for c in self.state.citations[:N]:
    if isinstance(c, dict):
        title = c.get("title", "")
        abstract = c.get("abstract", "")
        year = c.get("year", "")
        # ... use directly, do NOT iterate by source key
```

## Verification Protocol

After fixing progressive drafting bugs, verify by:
1. Run pipeline end-to-end
2. Read checkpoint JSON
3. Check: word count > 2000
4. Check: citation markers present (`re.findall(r'\[\d+\]', draft)`)
5. Check: sections present (`[l for l in draft.split("\n") if l.startswith("##")]`)
6. Check: `current_draft` is prose, not dict-stringified (`draft.startswith("#") or draft.startswith("Abstract")`)
