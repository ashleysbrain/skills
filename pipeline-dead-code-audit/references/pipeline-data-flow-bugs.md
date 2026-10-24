# Pipeline Data Flow Bugs — VERITAS Case Study (2026-08-08)

14 structural bugs found across 3 adversarial passes on `veritas_process.py`.
The pipeline ran all stages and reported "complete" but produced 87-113 word stubs
with AI telltales, zero citations, and all quality gates false-passing.

## Root Cause: No Shared Draft State

Every writing stage (4, 4.5, 4.6, 6) stored its result in an isolated
`stage_results[N]` slot. Every reading stage (5, 7, 7.5) read from `stage_results[4]`
— the ORIGINAL Wernicke response. Improvements from prose craft, expansion, and
revision were orphaned and invisible to QA.

## The 14 Bugs

### CRITICAL (6)
1. **Bell renders at stage 4, not the end** — `sections: [{"heading": "Abstract", "body": str(wern_res.get("result", ""))[:500]}]` produces a 500-char stub as the file on disk. Stages 4.5-7.5 improve text but never re-render.
2. **Research not fed into drafting** — Stage 4 reads `self.state.idea` only. Does not pass `stage_results[2]` (gathered papers) or `self.state.citations` to Wernicke. Draft written from raw idea, not research.
3. **Stage 4 truncates Wernicke output to 500 chars** — `[:500]` on the body passed to Bell.
4. **Revision loop sends feedback string, not draft** — Stage 6 passes `"idea": f"REVISE based on feedback: {feedback}"` to Wernicke. No draft text included.
5. **Panel reviews json.dumps of dict, not prose** — `json.dumps(draft.get("wernicke_draft", self.state.idea))[:2000]`. Panel sees JSON structure.
6. **Stage 4.6 truncates expanded draft to 5000 chars** — `"full_draft": full_draft[:5000]` cuts 75% of a 4000-word paper.

### HIGH (6)
7. **Stage 4.6 expansion orphaned** — result goes to `stage_results[4.6]`, not read by stages 5 or 7.
8. **QA reads stage 4, not latest** — Stage 7 reads `stage_results[4]["wernicke_draft"]`, not the expanded/revised version.
9. **Prose craft (4.5) orphaned** — `_get_draft_text()` checks 4.6 then 4, skips 4.5.
10. **Luria quality check reviews JSON** — `json.dumps(self.state.stage_results.get(4, {}))[:2000]` passed as `"text"`.
11. **Bell section hardcoded to abstract only** — Even with data flow fixed, render template only accepts one "Abstract" section.
12. **Narrative architecture (3.5) not fed into drafting** — Stage 4 ignores `stage_results[3.5]`.

### MEDIUM (2)
13. **Revision re-runs full panel on wrong input** — Stage 6 calls `stage5_adversarial_panel()` which reads stage 4, not revised text.
14. **Gate enforcement incomplete** — Panel FAIL and 5-dim FAIL verdicts ignored. Content ships with status="complete".

## The Fix: Shared current_draft

```
self.state.current_draft (string):
  Stage 2: SET current_citations from research
  Stage 4: SET current_draft from Wernicke (passing research + architecture)
  Stage 4.5: UPDATE current_draft with prose-crafted version
  Stage 4.6: UPDATE current_draft with expanded version (NO TRUNCATION)
  Stage 5: READ current_draft (not stage_results[4])
  Stage 6: UPDATE current_draft with revised version
  Stage 7: READ current_draft for all QA checks
  Stage 7.5: UPDATE current_draft with polished version
  NEW Stage 8: Bell RENDERS current_draft to HTML/PDF
```

## Detection Pattern

```python
# Red flag: passing dict representation to a text-expecting endpoint
json.dumps(stage_results[N])  # passes JSON, not prose
str(response.get("result", ""))  # passes dict repr string

# Red flag: truncating draft text before quality gates
text[:500], text[:2000], text[:5000]

# Red flag: reading from stage 4 when stages 4.5/4.6/6 exist
stage_results.get(4, {}).get("wernicke_draft")  # original, not improved
```

## Bus Messages
- 1565: Wernicke response nesting mismatch (content extraction thin)
- 1571: Quality gates scanning wrong text + FAIL verdicts ignored
- 1576: 7 structural flow problems found
- 1578: 7 more problems (14 total)
