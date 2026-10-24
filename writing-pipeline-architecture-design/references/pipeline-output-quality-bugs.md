# Pipeline Output Quality Bugs — Runtime Debugging (Aug 2026)

## The 3 Output Quality Bugs (All Fixed)

### Bug 1: Truncation
**Symptom:** Drafts were 634 words instead of 3000+.
**Root cause:** `max_tokens=8000` in the LLM-5.2 expansion call. LLM-5.2 is a
reasoning model that spends tokens thinking before generating. 8000 left only
1000-2000 for actual output.
**Fix:** Changed to `max_tokens=16000`. Verified: drafts now 3600-4400 words.
**File:** `veritas_process.py` stage 4.6 expansion call.

### Bug 2: Fabricated Citations
**Symptom:** Drafts contained `(Smith et al., 2024)` citations that didn't exist
in the gathered literature.
**Root cause (3 layers):**
1. **Prompt:** No constraint against inventing citations.
2. **Phantom check regex:** Only matched `[N]` format, missed `(Author, Year)`.
3. **Data flow bug:** Stage 2 stored papers in `stage_results[2]["fused_results"]`
   but NOT in `self.state.citations`. Stage 4.6 read `self.state.citations` →
   got empty list → LLM had no literature to cite from → invented citations.
   This was a **flat-list-vs-nested-by-source** bug: old code did
   `for c in self.state.citations: for src in ("arxiv","openalex",...): ...`
   but after the fix, citations are a flat list of paper dicts.

**Fix:**
1. Added prompt constraint: "Only cite from supporting literature. Use [N] format."
2. Added author-year regex to `_verify_citation_support()`.
3. Changed Stage 2 to store papers directly:
   `self.state.citations = fused_papers; self.state.current_citations = fused_papers`
4. Changed Stage 7 to use flat list: `all_citations = list(self.state.citations)`

**Verified:** 12 unique [N] citations, 0 phantom, all 12 in References section.

### Bug 3: Hallucinated Metrics
**Symptom:** Drafts contained unverified percentage claims ("34%", "50%") with
no source.
**Root cause:** No metric detection anywhere in the 4592-line pipeline.
**Fix:** Added `_verify_metric_grounding()` function. Extracts percentages,
p-values, ML metrics from draft. Flags any metric not grounded in a citation
abstract as `fabricated_metric`. Wired into Stage 7 QA output.
**Verified:** 0 fabricated metrics after fix.

## Key Debugging Pattern

When the pipeline produces output that LOOKS right but has quality defects:

1. **Run the pipeline** and save checkpoint JSON
2. **Read the checkpoint** — don't trust the `.run()` return value; read
   `state["current_draft"]`, `state["citations"]`, `state["final_output"]`
3. **Check data flow between stages** — the most common bug is a stage producing
   data in one structure and the next stage reading it from a different structure
4. **Verify prompt constraints** — LLMs will invent data if not explicitly told
   not to, and will avoid ALL citations if over-constrained
5. **Check the regex/verification functions** — phantom detection only works if
   it matches the ACTUAL citation format in the draft

## PipelineConfig Signature (verified Aug 2026)

```python
PipelineConfig(
    idea="topic here",           # NOT "topic"
    evidence_level="theoretical",
    author_name="principal"
)
```

The parameter is `idea`, not `topic`.
