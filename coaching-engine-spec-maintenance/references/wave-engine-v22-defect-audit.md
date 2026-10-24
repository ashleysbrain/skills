# Wave Engine v2.2 Defect Audit Catalog

Added 2026-07-23. The full catalog of 34 defects found in the v2.1 science-grounded diagnostic stack, with fixes applied in v2.2. Reusable as a checklist for any coaching engine build that uses diagnostic modules.

## The master defect: E16

**Diagnostics-after-generation.** The pipeline computed 9 diagnostic findings, attached them as metadata, but the LLM had already generated coaching text independently. Every diagnostic was decorative. The motivation type didn't change language. Efficacy didn't change step size. Nothing reached the user.

Detection: does the pipeline accept pre-generated coaching as INPUT, or build it WITH diagnostics in scope? `run_v2_pipeline(coaching_guidance=...)` encodes the bug in the function signature.

Fix: `pipeline_live.py` runs diagnostics first, builds a directives block, injects into system prompt, THEN calls LLM.

## Full defect catalog

### Complexity Gate (E1-E3)
- E1: word_count > 300 branch unreachable (elif cascade). Fixed: exclusive ranges.
- E2: double-counting strategy type + depth cue. Known limit (cosmetic).
- E3: non-English depth cues not detected. Known scope limit.

### Motivation Diagnosis (E4-E6)
- E4: "purpose" collision with PERMA. Fixed: removed from intrinsic markers.
- E5: distress + introjected vocabulary not coordinated. Known limit.
- E6: no density normalization. Fixed: confidence scaled by text length.

### Efficacy Calibration (E7-E9)
- E7: mixed signals scored LOW. Fixed: require net +/-2 to commit.
- E8: negation-colliding markers. Fixed: removed ambiguous phrases.
- E9: partial Bandura construct. Known limit (vicarious, physiological absent).

### Mindset Scoping (E10-E12)
- E10: dead bracket markers. Fixed: removed.
- E11: individual user labeled "high-risk." Fixed: calibrate intensity only.
- E12: jargon in LLM directive. Fixed: directives written in plain English.

### Multi-Perspective (E13-E15)
- E13: no actual advisor dispatch. Known limit.
- E14: voices are decorative metadata. Known limit.
- E15: structured default is wrong for neutral queries. Known limit.

### Pipeline (E16-E17)
- E16: MASTER FIX. Diagnostics flow INTO generation. Fixed in pipeline_live.py.
- E17: pipeline comment lied. Fixed: mechanism now matches.

### MAP Check (E18-E20)
- E18: external motivation always failed MAP. Fixed: external is valid start.
- E19: ability check ignored efficacy level. Fixed: tiered thresholds.
- E20: MAP result ignored. Fixed: steps revised before output.

### Habit Automaticity (E21-E23)
- E21: duplicate advice with efficacy. Known limit.
- E22: frequency detection matched stopwords. Fixed: content tokens only.
- E23: history not passed in production API. Known limit.

### If-Then Planner (E24-E26)
- E24: generic default action. Fixed: derived from user text.
- E25: generic default trigger. Fixed: specific anchor habits.
- E26: plans buried in science_trace. Fixed: surfaced to next_action.

### Progress Checkpoints (E27-E29)
- E27: never called with real milestones. Fixed: scans history for completions.
- E28: generic acknowledgment language. Known limit.
- E29: wrong milestone passed (step[0] is NEXT not DONE). Fixed.

### PERMA Scan (E30-E32)
- E30: weakest domain always positive_emotion. Fixed: stable priority.
- E31: "lonely" scores as positive. Known limit (needs polarity handling).
- E32: "purpose" cross-module collision. Known limit.

### Output Model (E33-E34)
- E33: jargon strip too aggressive. Fixed: multi-word phrases only.
- E34: LLM directive bleed. Mitigated (directives in plain English).

## Score: 19 fixed, 15 known limits documented

## Reusable checklist for any diagnostic-layer build

Before declaring a diagnostic-layer build complete, verify:

1. Does each diagnostic output reach the LLM prompt, or just metadata?
2. When MAP/gate finds gaps, do the steps actually change?
3. Run a sample coaching_response through the banned-jargon list.
4. Verify each conditional gate fires only under the right conditions.
5. Check for cross-module token collisions (grep all modules for shared words).
6. Check for negation-colliding markers (substring that matches its own negation).
7. Check for dead markers (literal brackets, domain-specific single words).
8. Verify the pipeline function signature doesn't encode the E16 bug.
9. Verify conversation history is actually passed through to diagnostics that need it.
10. Verify default values are specific, not generic ("brush teeth" not "tomorrow").
