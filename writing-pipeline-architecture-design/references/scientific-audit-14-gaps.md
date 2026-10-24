# Scientific Audit: 14 Gaps Found Against the Literature (Round 2)

## Methodology

Each of the 14 verified papers was checked against the architecture for actual
implementation, not just citation. The question: "Does the architecture
implement what the paper says, or does it only cite the paper without
implementing its findings?"

## The 5 CRITICAL Gaps

### S1: False Recursion — Feedback loops are not parallel cognitive processes
**Paper:** Flower & Hayes (1981) — 3,512 cites
**Architecture says:** Every stage has backward feedback loops.
**Paper requires:** Planning, translating, reviewing happen IN PARALLEL. A writer
drafts paragraph 4 while re-planning the thesis while reviewing paragraph 1.
**Gap:** Feedback loops are sequential (A finishes → loops to B). That is
iteration, not recursion.
**Fix:** Stage 6 (drafting) and Stage 7 (reader model) run CONCURRENTLY via a
shared live document buffer. Drafter writes a section; reader model evaluates
at section boundaries (not mid-paragraph — paragraph atomicity prevents race
conditions). Drafter revises Section N based on reader feedback before starting
Section N+1.

### S2: No Thesis Mutation — Revision cannot change the central claim
**Paper:** Sommers (1980) — 753 cites
**Architecture says:** Stage 8 revision operates at multiple levels. Feedback
loops can return to Stage 3.
**Paper requires:** Expert revision discovers that the real argument is different
from what was planned. Revision is discovery, not editing.
**Gap:** The skeleton is treated as a fixed artifact. No mechanism for the
pipeline to discover mid-revision that the central claim has shifted.
**Fix:** Add a **Reverse Outline** sub-step to Stage 8 Level 1. Engine extracts
what each section actually argues, compares to the Stage 3 skeleton. Divergences
surfaced as findings. Human decides: revise draft back to intent OR accept the
discovered thesis and UPDATE THE SKELETON. Skeleton is versioned.

### S3: Audience Sim is Post-Hoc, Not Parallel
**Paper:** Kellogg (2008) — 839 cites
**Architecture says:** Stage 7 runs after Stage 6. Sequential.
**Paper requires:** Knowledge-crafting requires SIMULTANEOUSLY manipulating
author content, text, AND reader interpretation.
**Fix:** Merge Stage 7 into Stage 6 Pass 3. Reader model runs AS prose is
generated, section by section. Standalone Stage 7 remains as final validation.

### S6: Warrants Required in Skeleton But Not Enforced in Prose
**Paper:** Toulmin (1958) — 5,618 cites
**Gap:** Skeleton enforces warrants structurally. But drafting and revision do
not verify warrants appear in PROSE. LLM writes claims+evidence without the
connecting inference.
**Fix:** Stage 8 Level 2 Detection includes **Warrant Extraction Check**: for
each paragraph with a claim+evidence, can the engine extract the explicit warrant
sentence? Missing = blocking at Level 2.

### S7: Walton Scheme Classification is Optional
**Paper:** Walton et al. (2008) — 1,351 cites
**Gap:** Scheme classification is offered but not mandated. Unclassified claims
can proceed through the pipeline.
**Fix:** Stage 3 makes Walton scheme classification MANDATORY for every claim.
No scheme = skeleton is BLOCKING. Critical questions auto-generated per scheme.

## The 7 MODERATE Gaps

### S4: Undiagnosed Findings Have No Workflow
**Paper:** Flower et al. (1986) — 376 cites
**Gap:** Schema allows diagnosis: null but workflow doesn't. No "detected but
undiagnosed" state.
**Fix:** Add `detected_undiagnosed` status. Non-blocking. Can persist across
revision rounds. Can be escalated to co-authors.

### S5: Research Problem and Practical Problem Are Conflated
**Paper:** Booth et al. (1995) — 458 cites
**Gap:** Architecture collapses Booth's two problem levels (research = conceptual
gap, practical = real-world cost) into one "stakes" question.
**Fix:** Stage 1 produces TWO outputs. Skeleton includes `problem_connection`
field linking research problem to practical problem. Empty = BLOCKING.

### S8: Rebuttals Not Weighted Equally With Claims
**Paper:** Osborne et al. (2004) — 1,540 cites
**Gap:** Evidence coverage map tracks claim support but not rebuttal quality.
Osborne found argument quality correlates with REBUTTAL quality more than claim
quality.
**Fix:** Coverage map gains `rebuttal_coverage`: anticipated/unaddressed/missing.
Panel includes dedicated counter-argument check, weighted equally with claim
support.

### S9: No Risk of Bias Assessment Per Source
**Paper:** Liberati et al. (2009) — 28,000 cites
**Gap:** Single quality_score field does not constitute a bias assessment.
**Fix:** Add `risk_of_bias` with structured domains (selection, performance,
detection, attrition, reporting) + funding_source/conflicts_declared. Sources
with high bias risk can be grounds but NOT backing.

### S11: Bastani Gate Tests Explanation, Not Construction
**Paper:** Bastani et al. (2025) — 119 cites
**Gap:** "Can you explain?" is gameable. Memorize and recite = recall, not
construction.
**Fix:** Change to PREDICTION. "Given a NEW scenario, what would this warrant
predict?" Forces reasoning, not recitation.

### S12: No Acceptance vs Provocation Ratio Tracking
**Paper:** Lee et al. (2022) — 334 cites
**Gap:** No telemetry tracking whether selective acceptance is actually
happening.
**Fix:** Decision Provenance telemetry. Acceptance Ratio: if >0.80 = rubber-
stamping warning, if <0.20 = rejecting all assistance warning. Advisory.

### S13: Stage 3 Generates One Skeleton, Not Alternatives
**Paper:** Boussioux et al. (2024) — 256 cites
**Gap:** Edit-one-proposal, not select-among-alternatives.
**Fix:** Stage 3 generates THREE candidate skeletons (strong, qualified,
contrarian). Human selects or combines. Unselected preserved as alternatives.

## The 2 MINOR Gaps

### S10: Homogenization Audit Ignores Author Creativity Level
**Paper:** Doshi & Hauser (2024) — 599 cites
**Fix:** Calibrate thresholds per author based on prior corpus after 3+ papers.

### S14: Melumad Protocol Does Not Adapt to Prior Knowledge
**Paper:** Melumad & Yun (2025) — 27 cites
**Fix:** Add `prior_knowledge_level` (expert/familiar/novice). Experts get
navigation aids; non-experts get primary sources only.
