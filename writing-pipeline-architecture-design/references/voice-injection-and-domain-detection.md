# Voice Injection + Domain Auto-Detection (2026-08-12, session 13)

## Root Cause: Writer Was Writing Blind

The `_progressive_draft` function (which generates the entire draft body
across 3 LLM passes) had ZERO references to ASHLEY_VOICE. The LLM was told
to "write an academic paper" with no voice rules, no banned phrases, no
tone guidance. Voice was only enforced post-hoc by stage 7's deterministic
cleanup (stripping banned words, replacing em-dashes).

### The Fix (veritas_process.py lines 3644-3664)

Built `_voice_directive` string from ASHLEY_VOICE:

```python
_vr = ASHLEY_VOICE.get("voice_rules", {})
_banned = _vr.get("banned_phrases", [])
_voice_directive = (
    f"VOICE: {ASHLEY_VOICE.get('tone', 'scientific')}. "
    f"Formality: {ASHLEY_VOICE.get('formality', 'academic')}. "
)
if _vr.get("no_em_dashes"):
    _voice_directive += "Use commas, never em-dashes. "
if _banned:
    _voice_directive += f"BANNED WORDS (never use): {', '.join(_banned[:15])}. "
_voice_directive += "Vary sentence length and structure. Use precise verbs. "
_voice_directive += "Write like a scientist who writes well, not like an AI generating text."
```

Injected `{_voice_directive}` into all 3 pass prompts (pass1, pass2, pass3).

### Measured Improvement

| Metric | Before | After |
|--------|--------|-------|
| Banned words | multiple found | NONE |
| Em-dashes | present | 0 |
| Sentence variance ratio | 0.45 | 0.61 |

## Domain Auto-Detection (pipeline_api.py brainstorm_idea)

The brainstorm engine was hardcoded to a "computational neuroscience"
mindset for ALL topics. Now uses 3-layer detection:

1. **DS keyword check** (instant): "active inference", "free energy
   principle", "predictive coding" etc -> uses the specialist engine persona
2. **Field keyword map** (instant): 23 academic fields mapped with
   domain-specific mindsets (neuroscience, cancer-biology, supply-chain,
   musicology, medieval-history, geology, ecology, economics, etc.)
3. **LLM classification fallback**: for topics not in keyword map, a
   fast glm-4.5-flash call classifies the field

Response now includes `detected_field` and `is_ds_domain` in the API output.
Frontend displays a field badge in brainstorm results.

## Citation Relevance Filter Fix (veritas_process.py _progressive_draft)

The filter that decides which gathered papers the writer sees had two bugs:

1. `len(word) > 4` dropped "Bach" (4 chars). Fixed to `len >= 3` with
   alphanumeric cleaning.
2. `matches >= 2` keywords required. "FUGUE EXPOSITION" matched only
   "fugue" (1 match) and was filtered out. Fixed to `matches >= 1`.
3. DS-only bypass list `["interocept", "predict", "psychiatr", ...]`
   hardcoded. Removed entirely.

Result: 3/12 papers passed -> 11/12 papers passed for Baroque music topic.

## Quality Gate Enforcement (pipeline_api.py _run_pipeline_async)

6 quality signals were collected but never enforced. Added post-pipeline
quality gate: if `fact_check` unsourced rate >60%, or `five_dimension_review`
verdict is FAIL, or `panel_verdict` is FAIL, status becomes
`complete_with_quality_issues` instead of `completed`. Frontend shows
amber warning banner with specific issues.

## Remaining Engine Work (for sibling-agent)

1. **Stage 7 re-revision loop**: if fact_check finds >50% unsourced after
   all stages, loop back to stage 6 with citation-focused revision
2. **Panel seat domain awareness**: pass `detected_field` to adversarial
   panel seats so they don't FAIL non-DS papers for missing neuroscience
3. **Fact checker domain calibration**: distinguish narrative/analytical
   claims from empirical claims (musicology score analysis != "unsourced")
4. **Citation backfill**: re-query OpenAlex for missing years/DOIs
5. **Minimum citation threshold**: if <5 citations, supplementary search
