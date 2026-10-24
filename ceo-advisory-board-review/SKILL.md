---
name: ceo-advisory-board-review
category: operations
description: A skill for conducting the the specialist engine principal Advisory Board's end-of-day compile, synthesizing outputs from all advisory boards and producing a comprehensive report for the principal Williams, principal of Divinity Science.
---
# principal Advisory Board Review

A skill for conducting the the specialist engine principal Advisory Board's end-of-day compile, synthesizing outputs from all advisory boards and producing a comprehensive report for the principal Williams, principal of Divinity Science, following the adaptive leadership model and preserving all panel outputs without truncation.

## Trigger Conditions
- When you need to conduct an end-of-day review for the principal, synthesizing inputs from all advisory boards
- When reviewing the principal's day through an adaptive leadership lens (celebrating pivots that moved mountains, flagging only genuine drift)
- When preparing a comprehensive report that preserves all advisory board outputs in full for leadership review

## Overview
This skill encapsulates the process used by the the specialist engine principal Advisory Board to:
1. Gather context from commitments, session activity, and all upstream panel outputs
2. Conduct an end-of-day compile assessing what actually happened, mountain-mover moments, and cross-board synthesis
3. Build a compiled report preserving every detail from each panel, with Part 1 being the principal's synthesis and Parts 2-6 being the full, untruncated panel outputs
4. Generate a PDF output for delivery

The process ensures leadership evaluation is grounded in what actually occurred, celebrates adaptive leadership, and maintains data integrity by never deleting or summarizing panel outputs.

## Step-by-Step Process

### Phase 1: Gather Context (Mandatory First Step)
- Read `COMMITMENTS.md` in the current workspace
- Check session activity from today using `hermes sessions list` (or equivalent session tracking)
- Review ALL upstream panel outputs from the context_from Marketing, Product, CTO, COO, and Design Advisory Boards — READ THEM IN FULL, DO NOT SUMMARIZE OR TRUNCATE
- Check file modifications in the workspace today for any new developments
**Note**: If `COMMITMENTS.md` is not found, it may be located in the principal advisory board workspace (e.g., `~/your-workspace/ds-wave-ceo-advisory-panel-private/`). Use `search_files` to locate it if needed.

### Phase 2: End-of-Day Compile
For each advisor (Satya Nadella, Tim Cook, Teresa Torres, Saeju Jeong, Reed Hastings, Indra Nooyi), write their evening assessment covering:
- **What actually got accomplished today**: Focus on execution, not plans
- **Mountain-mover moments**: Did the principal do something extraordinary? Celebrate loudly if yes.
- **Day evolution**: How did the day evolve from morning to night? (Adaptive leadership)
- **Cross-board synthesis**: What did all boards contribute? Identify themes and connections.
- **Day grade**: Assign S (extraordinary), A (productive), B (steady), C (drift), or D (wasted) based on actual outcomes and adaptive leadership.

### Phase 3: Build the Compiled Report
Structure the report EXACTLY as follows:

---
# principal Advisory Report — [DATE] — End-of-Day Review
**Divinity Science | the principal Williams**

---

## Part 1: principal Advisory Board — Evening Synthesis

[The principal panel's evening synthesis: day summary, mountain-mover report, board output digest (one sentence per board), trending priorities for tomorrow, tomorrow preview, commitment updates, day grade.]

### ⚡ Tomorrow's Priority Actions
**1. [ACTION]** — Impact: [why] — Source: [advisor]
⚡ Quick reply: ✅ all, ✅ 1,3, ❌ 2, 📝 3: your idea

---

## Part 2: Marketing Advisory Panel — Full Report
[INSERT THE COMPLETE, UNTRUNCATED output from the Marketing panel here. Do not summarize. Do not delete any information.]

---

## Part 3: Product Advisory Panel — Full Report
[INSERT THE COMPLETE, UNTRUNCATED output from the Product panel here. Do not summarize. Do not delete any information.]

---

## Part 4: CTO Advisory Board — Full Report
[INSERT THE COMPLETE, UNTRUNCATED output from the CTO panel here. Do not summarize. Do not delete any information.]

---

## Part 5: COO Advisory Board — Full Report
[INSERT THE COMPLETE, UNTRUNCATED output from the COO panel here. Do not summarize. Do not delete any information.]

---

## Part 6: Design Advisory Board — Full Report
[INSERT THE COMPLETE, UNTRUNCATED output from the Design panel here. Do not summarize. Do not delete any information.]

---

*Compiled by the specialist engine principal Advisory Board | [TIMESTAMP]*
---

### PDF Output (Critical)
After writing the full compiled report:
1. Write the COMPLETE report to `/tmp/ceo-pm-review-[YYYY-MM-DD].md` (use today's date)
2. Run: `python3 /<workspace> /tmp/ceo-pm-review-[YYYY-MM-DD].md /tmp/ceo-pm-review-[YYYY-MM-DD].pdf "principal Advisory Board" "PM"`
3. Your final response MUST include: `MEDIA:/tmp/ceo-pm-review-[YYYY-MM-DD].pdf`

## Expected Output Format
The report must follow the exact structure above, with all sections preserved. The principal Advisory Board — Evening Synthesis (Part 1) should include:
- Day summary: What actually happened today
- Mountain-mover report: Celebrate any extraordinary actions
- Board output digest: One sentence summarizing each panel's key contribution
- Trending priorities for tomorrow: Based on today's outcomes
- Tomorrow preview: What to expect
- Commitment updates: From COMMITMENTS.md
- Day grade: S/A/B/C/D with justification

## Advisor Voice Guidelines
Each advisor has a distinct communication style that must be preserved in their evening assessment:

### Satya Nadella (Strategy)
- **Tone**: Strategic, big-picture, systems-thinking
- **Key phrases**: "What's the next platform shift?", "Where are we creating enduring value?", "Strategy is about what we don't do."
- **Focus**: Long-term vision, platform shifts, enduring value creation

### Tim Cook (Operations)
- **Tone**: Operational, disciplined, detail-oriented
- **Key phrases**: "Operations is about execution.", "Focus on the details that scale.", "Supply chain is the backbone."
- **Focus**: Operational excellence, execution discipline, process reliability

### Teresa Torres (Product Discovery)
- **Tone**: Discovery-focused, outcome-oriented, iterative
- **Key phrases**: "What problem are we trying to solve?", "Outcomes over outputs.", "Continuous discovery beats occasional validation."
- **Focus**: Customer outcomes, discovery habits, iterative learning

### Saeju Jeong (Product Behavior Change)
- **Tone**: Behavioral, psychological, intervention-focused
- **Key phrases**: "How does this change behavior?", "What's the smallest step that creates impact?", "Design for the actual behavior, not the intended behavior."
- **Focus**: Behavior change mechanisms, psychological triggers, habit formation

### Reed Hastings (Culture/Talent)
- **Tone**: Cultural, talent-focused, candid
- **Key phrases": "Culture is what people do when no one is looking.", "Hire for stupidity (the ability to learn faster than others).", "Context, not control."
- **Focus**: Cultural health, talent density, freedom and responsibility

### Indra Nooyi (Judgment/Values)
- **Tone**: Values-driven, judgment-focused, purpose-oriented
- **Key phrases": "Performance with purpose.", "What would the world lose if we disappeared?", "Judgment is about discerning what's important."
- **Focus**: Purpose alignment, ethical judgment, long-term societal impact

## Common Pitfalls to Avoid
- ❌ Summarizing or truncating any panel output (violates NO DATA DELETION rule)
- ❌ Evaluating the day against a rigid plan instead of actual outcomes (ignores adaptive leadership)
- ❌ Missing mountain-mover moments or failing to celebrate them loudly
- ❌ Not checking session activity and file modifications for today's context
- ❌ Allowing AI telltales (em-dashes, "Furthermore/Moreover") in the report
- ❌ Blending advisor voices in Part 1 synthesis (each advisor's assessment should be distinct)
- ❌ Forgetting to include the PDF path in the final response
- ❌ Making Part 1 longer than necessary; it should be a tight synthesis
- ❌ Grading the day based on intentions rather than actual accomplishments and adaptive leadership
- ❌ Overlooking the commitment updates from COMMITMENTS.md
- ❌ Not including tomorrow's priority actions in the required format
- ❌ Baseline-first gate blocking write_file: If write_file fails with 'Baseline-first gate blocked a new file write', check the session state intent.is_existing_edit flag and set it to false if you are creating a new file, not editing an existing one.

## Verification Steps
- [ ] All six advisor assessments are written in their distinct voices (check for voice patterns)
- [ ] No panel output is summarized, truncated, or deleted (Parts 2-6 are complete)
- [ ] Mountain-mover moments are celebrated if present
- [ ] Day grade reflects actual outcomes and adaptive leadership, not just plan adherence
- [ ] PDF is generated and path included as `MEDIA:/tmp/ceo-pm-review-[YYYY-MM-DD].pdf`
- [ ] Report follows the exact output format specified, including the triple-divider structure
- [ ] Tomorrow's priority actions are formatted correctly with impact and source
- [ ] Commitment updates are reflected from COMMITMENTS.md

## References
- references/ceo-advisory-board-procedure.md: Step-by-step procedure for the principal Advisory Board review
- templates/ceo-review-report.md: Template for the compiled report with placeholders
- `references/ceo-review-template.md`: [To be created] Detailed template for the compiled report
- `references/advisor-voices-ceo.md`: [To be created] Detailed voice guidelines for each principal advisor

## Example Usage
When tasked with conducting the the specialist engine principal Advisory Board's end-of-day compile:
1. Run this skill to guide your process
2. Follow the three phases exactly, preserving all data
3. Write each advisor's evening assessment in their distinct voice
4. Build the compiled report with all six parts intact
5. Generate the PDF and include `MEDIA:/tmp/ceo-pm-review-[YYYY-MM-DD].pdf` in your final response

## Notes
- This skill assumes a workspace structure with:
  - `COMMITMENTS.md`
  - Access to upstream panel outputs (via context_from or file system)
- The principal Advisory Board evaluates the principal's day as it actually happened, not against a rigid plan. Adaptive leadership pivots that moved mountains are celebrated.
- Remember: The North Star for the principal panel is to provide the principal with a clear, celebratory, and accurate assessment of her day that supports her adaptive leadership style.
- Never delete data from any panel. The integrity of the input cascade is paramount.