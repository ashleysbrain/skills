# VERITAS + CRUCIBLE Elite Writing Workflow Adversarial Review

**Date:** 2026-08-05
**Panel:** the specialist engine (lead) + 9 seats (Kahneman, Wernicke, Machiavelli, Bentham, Methodology Auditor, Editorial Proxy, Audience Proxy, Niche Expert x2)
**Standard:** Output must be publishable at top-tier venues (TSC, Nature Methods, IEEE, arXiv featured)

Full review on disk: `/<workspace>`

## Verdict: Both NEEDS WORK

The pipelines are competent research-validation engines but structurally incomplete
as writing workflows. They validate what a paper CLAIMS (physics gate, adversarial
panel) but do not craft how a paper READS.

## P0 Fixes (blocking elite output)

1. **No narrative/structure planning stage** — both jump from physics gate straight
   to drafting. Need Stage 3.5: thesis distillation, section outline, figure plan,
   abstract skeleton.

2. **No prose craft stage** — no dedicated sentence/paragraph-level revision. Revision
   only fires on claim failure. Need Stage 4.5: prose revision driven by voice-fidelity
   score, not claim validity. Runs unconditionally >=1 round.

3. **Panel reviews truncated JSON, not prose** — both pass `json.dumps(draft)[:2000]`
   to panel. Must pass actual prose text. Silent correctness bug.

4. **Wire scan_ai_tells.py as hard gate** — current AI-tell scan is a Wernicke compose
   call (LLM opinion), not the org's deterministic scanner. Replace with scan_ai_tells.py
   (already exists in ai-tell-removal-gate skill). FAIL = forced revision.

5. **No anti-formulaic diversity check** — nothing prevents every output from sounding
   the same. Need stylometric fingerprint comparison against prior outputs.

6. **Declare explicit niche** — VERITAS: active inference / comp-neuro for health.
   CRUCIBLE: AI-native infrastructure security. Hard-filter categories, add niche rules.

## P1 Fixes (high impact)

7. Voice profile not enforced in VERITAS (defined but never sent to engine)
8. PubMed missing from VERITAS (mandatory for neuroscience/health niche)
9. No editorial polish stage (Stage 7.5: final copy-edit by dedicated seat)
10. Prose revision coupled to claim revision (should be decoupled)
11. No academic-vs-scicomm register separation
12. Ground truth verification is lexical (bag-of-words), not semantic

## Silent Bug Found

The adversarial panel found that both pipelines pass `json.dumps(draft)[:2000]` to the
panel as the "content" to review. The panel is reviewing a truncated JSON serialization
artifact, not the actual prose. This is a critical correctness bug in both files.

VERITAS: line 947, `content = json.dumps(draft.get("wernicke_draft", self.state.idea))[:2000]`
CRUCIBLE: line 1068, same pattern.

## The Editorial Craft Chain (entirely missing)

Real elite writing goes through: developmental edit, line edit, copy edit, proofread,
voice consistency pass. Neither pipeline has any of these. They have claim validation
and packaging but no editorial craft.

## Elite Workflow Comparison

Real PI lab vs VERITAS: PI spends weeks on thesis distillation, outline, and
section-by-section drafting with role specialization. VERITAS does a single Wernicke
compose call and reviews truncated JSON.

Real CTO team vs CRUCIBLE: problem framing ("what decision will this drive?"),
competitive teardown, architecture diagrams as first-class artifacts. CRUCIBLE does
a single Wernicke call with regex vendor-neutrality checks.

## Niche Gap

VERITAS searches 9 arXiv categories spanning neuroscience, AI, statistics, HCI, NLP,
complex systems, and biophysics. That is "all of quantitative bioscience plus AI," not
a niche. CRUCIBLE is slightly better (4 categories) but still generic.

Recommended niches:
- VERITAS: active inference / computational neuroscience applied to health
- CRUCIBLE: AI-native infrastructure security
