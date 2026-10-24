# Toulmin Skeleton Builder: Runtime Wiring Debug Log

Session: 2026-08-10
Commit: 903efa4 (initial) + runtime fixes

## What Was Built

`stage3_argument_architecture()` in `veritas_process.py` — replaces the old
`stage3_physics_gate` as the primary Stage 3. The physics gate is now
Stage 3.1 (sub-check).

The method:
1. Extracts citation context from Stage 2 gathered papers (flat dicts)
2. Builds a Toulmin skeleton prompt with available evidence
3. Calls LLM-5.2 three times with different variant prompts (strong, qualified, contrarian)
4. Parses JSON from each response (handles ```json fences)
5. Validates each skeleton: missing warrant = BLOCKING, missing Walton scheme = warning
6. Auto-selects the strongest non-blocking skeleton
7. Stores result at `stage_results[3]` with all candidates

## Bugs Found at Runtime (3 bugs, all fixed)

### Bug 1: Citations Structure Mismatch
**Symptom:** `'str' object has no attribute 'get'` at the citations loop
**Root cause:** Code expected nested structure `c.get("arxiv", [])` returning
a list of paper dicts. Actual structure from Stage 2 is FLAT:
```json
{"source": "crossref", "doi": "10.31234/osf.io/daf5n", "title": "...", "authors": [...], "year": 2024}
```
**Fix:** Access flat keys directly:
```python
citations_context.append({
    "ref_id": f"S{len(citations_context)+1:03d}",
    "title": (c.get("title", "") or "")[:120],
    "abstract": (c.get("abstract", "") or "")[:200],
    "year": c.get("year", ""),
})
```

### Bug 2: Non-Dict Skeleton Items Crash Validation
**Symptom:** `'str' object has no attribute 'get'` in the validation loop
**Root cause:** LLM sometimes returns non-JSON text. When `_json_mod.loads(raw)`
succeeds but returns a string or list (not a dict), or when the JSON parse
fails and an error string gets appended to `skeletons` list, the validation
loop's `skel.get("error")` crashes.
**Fix:** Guard every iteration:
```python
for skel in skeletons:
    if not isinstance(skel, dict):
        validated.append({"variant": "error", "error": f"non-dict skeleton: {str(skel)[:80]}"})
        continue
```

### Bug 3: Stage Key Collision (3 -> 3.1)
**Symptom:** Stage 3 result shows "physics_gate" instead of "argument_architecture"
**Root cause:** Both `stage3_argument_architecture` and `stage3_physics_gate`
saved to `self.state.stage_results[3]`. Physics gate ran second (as Stage 3.1
in the run loop) and overwrote the argument architecture result.
**Fix:** Changed ALL three places in `stage3_physics_gate` that write to key 3:
- Error handler: `stage_results[3.1]` + `_complete_stage(3.1)`
- Success path: `stage_results[3.1]` + `_complete_stage(3.1)`
- Also update the `stage` field in the result dict to `3.1`

## Verified Runtime Output

Input: "Active inference and the computational architecture of consciousness"

Stage 3 output (93.9s):
- 3 skeletons generated (strong, qualified, contrarian)
- Central claim: "Active inference constitutes the computational architecture of consciousness: phenomenal experience emerges from precision-weighted generative modeling..."
- Qualifier: "probably, under conditions where (i) precision-weighting is empirically decodable..."
- 4 sub-claims, each with explicit warrant + Walton scheme:
  - C1: abductive_reasoning
  - C2: argument_from_correlation
  - C3: argument_from_analogy
  - C4: abductive_reasoning
- Blocking: False (all warrants present)
- Full pipeline completed: 3,423 words, 0 phantom citations

## Stage Order in Run Loop

```python
stages = [
    (0, self.stage0_evidence_gate),
    (1, self.stage1_topic_refinement),
    (2, self.stage2_research_gathering),
    (2.5, self.stage2_5_human_checkpoint),
    (3, self.stage3_argument_architecture),  # NEW: Toulmin skeleton
    (3.1, self.stage3_physics_gate),          # MOVED: sub-check
    (3.5, self.stage3_5_narrative_architecture),
    (4, self.stage4_drafting),
    (4.5, self.stage4_5_prose_craft),
    (4.6, self.stage4_6_full_draft_expansion),
    (5, self.stage5_adversarial_panel),
    (5.5, self.stage5_5_coherence_check),
    (6, self.stage6_revision_loop),
    (7, self.stage7_qa_output),
]
```

## Next Steps

Wire the methods that exist but aren't in the run loop:
1. Replace `stage4_6_full_draft_expansion` with 3-pass progressive drafting
2. Add concurrent reader model inside Pass 3
3. Replace `stage6_revision_loop` with leveled revision (L1 discourse, L2 paragraph, L3 sentence)
4. Add Stage 9A cognitive checkpoint before output
