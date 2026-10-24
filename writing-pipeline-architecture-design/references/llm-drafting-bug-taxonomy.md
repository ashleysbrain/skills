# LLM Progressive Drafting Bug Taxonomy

Complete debugging log from 8 pipeline passes (2026-08-10 sessions 10-11).
Each pass found real bugs by running the pipeline and reading actual output.

## The 3-pass progressive drafting architecture

```
Pass 1 (knowledge-telling): Flash/fast model. Externalize content from
       Toulmin skeleton into prose. One section per claim.
Pass 2 (knowledge-transforming): Reasoning model. Reshape argument, detect
       contradictions, strengthen warrants, add transitions.
Pass 3 (knowledge-crafting): Reasoning model. Polish prose, vary sentence
       openers, check academic tone, ensure citation markers in context.
```

## Bug catalogue

### BUG: Citation fabrication (CRITICAL)

**Detection method:** Read the actual draft prose. Check if [N] markers in the
draft match gathered citations. Check if the References section contains papers
from the evidence pool or from LLM training memory.

**Observed failure:** Draft had 8 citation markers [1]-[5] referencing Barrett
2015, Khalsa 2018, Friston 2010, Pezzulo 2018, Paulus 2006. These are real
papers from the LLM's training data, NOT from the 5 relevant papers gathered in
Stage 2. The Toulmin skeleton's grounds used abstract ref_ids (S002, S008) that
connected to NOTHING in the draft.

**Root cause:** Three disconnected citation systems:
1. Stage 2 gathers papers as flat dicts: `{source, doi, title, authors, year, abstract}`
2. Toulmin skeleton (Stage 3) grounds use `ref_id: "S002"` format
3. Draft uses `[N]` markers from LLM training memory
The progressive draft prompt passes abstract ref_ids that the LLM cannot resolve
to actual papers, so it invents real-sounding citations from training data.

**Fix (6 parts):**
1. Filter gathered citations by keyword relevance (remove arxiv physics spam)
2. Build cite_context with full metadata: `[1] Author (Year). Title. DOI: xxx`
3. Prompt instruction: "ONLY cite papers from EVIDENCE list. Do NOT invent references."
4. Post-draft (programmatic): strip `[N]` markers where N > len(evidence)
5. Post-draft (programmatic): inject References section from actual evidence
6. Pass 2 instruction: "do NOT add new citations not in original draft"

### BUG: Pass 3 shrinkage (HIGH)

**Detection method:** Compare word counts across passes. Pass 3 consistently
produces 0-70% of Pass 2 output.

**Observed failure across multiple runs:**
- Run A: Pass 1=1431, Pass 2=2257, Pass 3=944 (42% of Pass 2)
- Run B: Pass 1=2397, Pass 2=2763, Pass 3=1921 (70%)
- Run C: Pass 1=3385, Pass 2=334 (10%!), Pass 3=462
- Run D: Pass 1=3051, Pass 2=2851, Pass 3=49 (2%!)

**Root causes:**
1. Input truncation: Pass 2 receives `pass1_text[:6000]` — only 6,000 chars of
   a 20,000+ char draft. LLM sees 30% of the draft and summarizes what it saw.
2. max_tokens=8000 insufficient for outputting a 3,000-word draft.
3. Pass 3 prompt says "tighten prose — remove filler, redundancy" which the LLM
   interprets as "delete entire paragraphs."
4. No anti-summary instruction in system prompt.

**Fix:**
- Input limit: `pass1_text[:12000]` (doubled)
- max_tokens: 16,000 (doubled)
- System prompt: "You ALWAYS output the complete full-length draft, never a summary"
- Pass 3 prompt: removed "tighten" and "remove redundancy", added explicit
  "Do NOT shorten. Output must be at least {N} words."
- Shrinkage guard: if p3_words < p2_words * 0.7, return pass2_text
- Shrinkage guard: if p2_words < p1_words * 0.5, return pass1_text

### BUG: Stage 6 dict-stringification (CRITICAL)

**Detection method:** Check if `current_draft` starts with `{` and contains
`'status': 'ok'`. If so, it's a stringified dict, not prose.

**Observed failure:** After Stage 6 revision, `current_draft` contained:
```
{'status': 'ok', 'organ': "Wernicke's Area", 'result': {'headline': '...', 'body': '...'}}
```
Instead of the actual prose body text.

**Root cause:** Wernicke engine returns a nested dict. Stage 6 does:
```python
revised_text = str(wern_res.get("result", ""))
```
`str()` on a dict produces its repr, which passes the length check because
the dict repr is long enough.

**Fix:** Extract body text from nested structure before comparison:
```python
wern_result = wern_res.get("result", "")
if isinstance(wern_result, dict):
    inner = wern_result.get("result", wern_result)
    if isinstance(inner, dict):
        revised_text = inner.get("body", "")
    else:
        revised_text = str(inner)
else:
    revised_text = str(wern_result)
if revised_text.startswith("{") and "'status'" in revised_text[:50]:
    revised_text = ""  # dict dump, not prose
```

### BUG: Pass 1 rate-limit failure (MODERATE)

**Detection method:** Pass 1 returns 0 words (empty string).

**Root cause:** Three back-to-back API calls to LLM-5.2 (90s + 120s + 120s =
330s total). Rate limiting or timeout on the first call.

**Fix:** timeout=90s for Pass 1. If Pass 1 fails, Pass 2 can generate from
the skeleton alone (it has enough context). Pipeline does not abort.

### BUG: Citation flat-list vs nested-by-source (RECURRING)

**Detection method:** Check `cite_context` array length. If 0 despite having
gathered citations, the parsing is broken.

**Root cause:** Code expects `c.get("arxiv", [])` but actual citations are
flat dicts with a `source` key: `{"source": "crossref", "title": "...", ...}`.

**This bug recurred 3 times** in different methods (Stage 3, Stage 4.6 Pass 1,
Stage 4.6 fallback). Every method that iterates citations independently
implements the same parsing logic and makes the same mistake.

**Fix pattern:** Use flat-key access everywhere:
```python
for c in self.state.citations[:8]:
    if isinstance(c, dict):
        title = (c.get("title", "") or "")[:100]
        abstract = (c.get("abstract", "") or "")[:200]
```

**General rule:** Extract a `_build_citation_context()` helper to eliminate
the recurring copy-paste bug.
