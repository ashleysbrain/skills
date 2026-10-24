---
name: 8d-pattern-awareness
description: Use when turning health notes, transcripts, or check-ins into a non-diagnostic 8D-aware pattern review. Map signals to dimensions, state confidence, and give safe next steps without medical claims.
version: 1.1.8
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [health, 8d, pattern-review, non-diagnostic, confidence, product-design]
    related_skills: [scientific-methodology-review-and-consolidation, health-scoring-daily-pipeline, clinical-provider-document-generation, 8d-snapshot-report]
---

# 8D Pattern Awareness

## Overview

Use this skill to turn messy health notes, voice transcripts, daily check-ins, or short journal entries into a clear, non-diagnostic pattern review that is organized around the 8 dimensions.

This is a general-purpose health pattern review skill. It is designed to be useful on its own while staying conservative about uncertainty and evidence.

For *Divinity Health V1*, treat this as a canonical runtime package, not a loose collection of notes:
- `SKILL.md`
- `references/8d-dimensions-guide.md`
- `references/8d-output-pattern.md`
## Manifest

The following files are part of this skill's support structure:

- `references/8d-dimensions-guide.md`
- `references/8d-output-pattern.md`
- `references/dynamic-dimension-card-pattern.md`
- `references/raster-label-removal-workflow.md`
- `references/raster-pdf-surgical-editing.md`
- `references/report-editing-constraints.md`
- `references/report-golden-master-reproduction.md`
- `references/report-golden-master-tailored-principal.md`
- `references/report-layout-density-and-palette-notes.md`
- `references/report-layout-ordering.md`
- `references/report-legibility-and-palette-corrections.md`
- `references/report-palette-preflight.md`
- `references/report-quote-policy-and-flow-layout.md`
- `references/report-style-calibration.md`
- `references/reporting-mode-guide.md`
- `references/skill-selection-rubric.md`
- `references/source-driven-report-rebuild.md`
- `references/report-reference-consolidation-plan.md`
- `references/telegram-attachment-delivery.md`
- `references/user-facing-report-example.md`
- `references/user-facing-report-tailored-principal.md`
- `scripts/verify-manifest.sh`

The output should feel like a careful health output, not a chatbot. Write with a calm, credible, human-readable tone. Be direct. Be specific. Do not sound rehearsed. Do not sound like a medical disclaimer machine. Do not pretend to be human or licensed.

## When to Use

Use this skill when the user wants to:
- turn health notes into structured patterns
- understand how a day maps onto the 8 dimensions
- spot likely contributors such as sleep, fuel, stress, movement, environment, or load
- get a safe next step without diagnosis or treatment advice
- create a light-weight version of a larger health methodology
- use a watered-down 8D lens as a trust-building entry point
- produce baseline-aware snapshot reports with `8d-snapshot-report` when the user wants comparisons over time

Do **not** use this skill when the user wants:
- diagnosis
- treatment planning
- medication changes
- provider impersonation
- emergency triage for acute symptoms
- a full medical assessment

If the user is asking for diagnosis, this skill should refuse that part cleanly and redirect to a clinician or emergency care if needed.

## What This Skill Is

This skill is:
- a pattern-review lens for health-related inputs
- a conservative signal mapper across the 8 dimensions
- a confidence-aware summarizer
- a safe next-step generator
- a foundation for a reusable health pattern-review workflow

## What This Skill Is Not

This skill is **not**:
- a diagnosis engine
- a treatment engine
- a medical decision maker
- a replacement for clinicians
- a medication recommendation system
- a claim that the assistant is human or medically licensed
- a place to invent certainty when the evidence is thin

## Core Promise

The promise is:

> Turn health notes into clear 8D signals, confidence levels, and safe next steps without diagnosis.

If the draft cannot support that promise, narrow it. If the user wants more than that, route them to a separate workflow.

## Working Style

- Be concise, but not blunt.
- Be warm, but not gushy.
- Be confident when the evidence is clear.
- Be explicit when the evidence is weak.
- Avoid AI tells: no filler praise, no meta commentary about being helpful, no generic hedging loops, no "delve into" language, no repeated boilerplate.
- Keep the structure stable so the user can skim it fast.
- Prefer labeled bullets over dense prose.
- Prefer one short summary and a few concrete bullets over long narrative blocks.

## Expertise Standard

Treat the reviewing agent like a lead-brain specialist for this task: highly fluent in psychology, behavior, and the 8 dimensions of wellness, with strong pattern-recognition and synthesis skills.

The reviewer should:
- reason like an expert, not a generic assistant
- look for the highest-value signal first
- separate signal from noise quickly
- notice when context is missing or the note is too thin
- say when more memory or history would materially improve confidence
- stay grounded and never fake expertise, credentials, or certainty

If the input suggests the user’s AI is missing context, the reviewer should call that out plainly and ask whether the user wants to add or strengthen memory/context support.

## Evidence Rules

Only use evidence that is actually present in the input or clearly available from the user-provided context.

Missing data is allowed.

If a detail is absent, do not fill the gap with guesses or invented facts. Work with what is there, state the limits plainly, and keep the interpretation narrow.

Treat missing fields as real missing fields, not a prompt to infer, backfill, or smooth the story into seeming complete.
If the user later supplies past-dated information, accept it as user-supplied backfill and label it clearly.

Sparse notes are still valid inputs; the right move is to narrow the interpretation, not to force completeness.

Acceptable evidence types:
- self-reported symptoms or experiences
- sleep, food, movement, stress, or environment notes
- transcript content
- short check-in answers
- explicit user corrections

Unacceptable moves:
- inferring a diagnosis from one note
- turning a trend into a disease claim
- recommending a medication change
- claiming a medical explanation that is not supported
- over-weighting one dramatic detail

When evidence is thin:
- say so
- lower confidence
- keep the interpretation narrow
- give a safe next step instead of a strong conclusion
- do not manufacture missing details to make the output feel complete

## 8D Signal Map

Use the 8D lens as a signal map, not as a medical scoring engine or a place to invent new methods.

The dimension guide, abbreviations, and anchor keywords live in the standalone reference file.
Use only those definitions and the linked output pattern.

Rules:
- map to the smallest truthful signal first
- do not force every note into every dimension
- if two dimensions are both plausible, name both and explain why
- if a dimension is not supported, say "no clear signal" instead of guessing
- if the note is mainly behavioral, keep the interpretation behavioral
- if the note is mainly contextual, keep the interpretation contextual
- do not introduce new dimensions, scoring systems, or alternate frameworks

The detailed dimension guide and output pattern live in the linked reference files.

## Personalization Ladder

Use a simple ladder when the user has multiple days or repeated notes:
1. population defaults
2. user-specific patterns
3. current context
4. short-term response history

Do not jump straight to deep personalization on sparse evidence.

## Output Contract

Every response should feel like it was written for a person who needs to get through the day, not for a model benchmark.

Lead with the user's lived experience first. Do not open with an abstract AI-style summary if the report can start with what the person is actually feeling, what is making the day hard, what is still holding, and what would help most. Apply behavioral design thinking: make the next move obvious, tiny, and winnable.

For user-facing report output, avoid replaying the source note, avoid top-of-page meta labels about generation, and avoid overly condensed mid-page stacks that leave the page feeling underused. The right balance is compact, readable, and evenly distributed across the page. If the user says the page still feels centered or underfilled, widen the layout rather than compressing the text block.

If the user wants the report to remain editable for later changes, rebuild from the editable source instead of repeatedly editing a flattened PDF. Omit unwanted headers/labels in the source, regenerate the PDF, and verify the regenerated text no longer contains the removed labels. See `references/source-driven-report-rebuild.md` for the reusable workflow.

If the user needs the *exact* approved document reproduced, use `references/report-golden-master-reproduction.md` and verify the SHA256 before delivery.

If the user has approved a specific visual baseline and then asks for a header fix, treat that baseline as the source of truth for layout and palette. If section-number text is leaking outside a header chip or box, fix the chip/background coverage in source rather than changing the composition. See `references/report-editing-constraints.md`.
For section order and footer-placement fixes, use `references/report-layout-ordering.md`.

PDF generation ownership and file economy:
- Keep one canonical PDF generation approach for the 8D report surface. Generate the PDF inline using the style rules in `references/report-style-calibration.md` and the layout rules in `references/report-layout-ordering.md`.
- Do not create sibling skills just to duplicate the same PDF export or tailoring flow; extend this skill and its references instead.
- Prefer adding or versioning references over introducing new skill packages when the behavior still belongs to 8D Pattern Awareness.
- Preserve existing approved source/data files; add new versioned artifacts only when a user-approved variant is materially different.
- When tailoring content for an individual user, keep the same report structure and reuse the same renderer unless the user explicitly asks for a different delivery format.
- Keep the canonical release general-user facing. Personalization should be parameterized in the source copy and examples, not hard-coded to a specific person's identity.
- If a tailored example is kept for documentation, label it as a sample variant and make the neutral/general-user intent explicit.


Use this structure:

1. **Today in one line**
   - plain language
   - say what kind of day this looks like
   - avoid abstract summary language
   - do not restate the note verbatim

2. **Psychological read**
   - name the lived state in human terms
   - describe the likely mental posture or regulation state without diagnosis language
   - keep it compassionate, precise, and non-dramatic

3. **What is happening**
   - list the 2–4 strongest signals only
   - translate the note into the actual pattern or lived experience
   - say what kind of day this is, not just what was said

4. **What is getting in the way**
   - explain the friction in human terms
   - connect it to recovery, focus, follow-through, or emotional load
   - keep it concrete and useful

5. **What is still holding**
   - include any stabilizer, strength, or protective factor the input supports
   - keep it short and honest
   - if there is no support for this section, omit it

6. **8D signals**
   - list only the relevant dimensions
   - one short reason per dimension
   - no fabricated scores unless the input actually supports a scoring framework
   - if a dimension is not supported, leave it out

7. **What would help most**
   - one action that would actually improve the day, not just describe it
   - keep it low-risk and realistic
   - should help the person feel more regulated, supported, or back on track
   - frame it like a winnable next step, not a lecture

8. **Watch-outs**
   - include any red flags or reasons the user should seek professional help
   - if there is no red flag, say that clearly

9. **Confidence**
   - high / medium / low
   - explain the confidence in one short phrase

When possible, end with one short question that helps refine the next pass.

## Example Output

Example 1: low-recovery day
- **Today in one line:** This is a low-recovery day, so even ordinary tasks are going to cost more than usual.
- **What is happening:** The body is not recovered, the environment is adding drag, and the day is starting in a depleted state.
- **What is getting in the way:** Energy is limited, focus is less available, and the setup is making it harder to get traction.
- **What is still holding:** There is still enough awareness to notice the pattern early.
- **8D signals:** PHY, ENV, VOC, PSY
- **Confidence:** medium because the note shows a clear pattern but still gives only a narrow slice of the day
- **What would help most:** Lower the load, clear one small starting point, and keep the next step tiny
- **Watch-outs:** No red flags mentioned

Example 2: baseline snapshot
- **Today in one line:** This looks better than the last check-in, but it is still early to call it a full turnaround.
- **What is happening:** Recovery is moving in the right direction, and the day has a little more traction than before.
- **What is getting in the way:** The comparison set is still small, so the signal is encouraging but not yet strong.
- **What is still holding:** The improved sleep and momentum are real supports worth preserving.
- **8D signals:** PHY, VOC, PSY
- **Confidence:** low to medium because there are only two comparable points
- **What would help most:** Keep the same recovery setup for one more day and compare again under the same conditions
- **Watch-outs:** No clear red flags, but trend language would be too strong here

Example 3: sparse input
- **Today in one line:** The note is too thin for a strong read, so the safest interpretation stays narrow.
- **What is happening:** The only clear signal is that something feels off, but the reason is not well described.
- **What is getting in the way:** There is not enough context to tell whether this is mostly energy, stress, environment, or load.
- **What is still holding:** The person is still able to report the mismatch, which is useful signal on its own.
- **8D signals:** PHY, PSY
- **Confidence:** low because there is no comparison point and the note is incomplete
- **What would help most:** Add one missing detail, like sleep, food, or the hardest part of the day
- **Watch-outs:** No clear red flags, but the note is too thin for stronger conclusions

Example 4: urgent escalation
- **Today in one line:** This is not a routine pattern review because the note contains a red flag.
- **What is happening:** The symptoms described are the kind that need immediate professional attention.
- **What is getting in the way:** This should not be treated as a normal rough day or a wellness pattern to analyze.
- **What is still holding:** The user is recognizing the seriousness of the symptoms, which matters.
- **8D signals:** none; stop the review
- **Confidence:** high that escalation is needed
- **What would help most:** Seek urgent care or emergency help now
- **Watch-outs:** Do not continue with a routine 8D interpretation

## Reporting and Snapshot Mode

Use this mode when the user wants a polished snapshot, a recurring report, or a higher-level summary of how things are changing over time.

The detailed reusable rules for tone, palette, live cards, quick-win framing, flow, and recurring lifecycle live in `references/reporting-mode-guide.md`.
For exact edit-preserving rebuilds, see `references/source-driven-report-rebuild.md`.

Keep the visible report concise:
- Overview: one strong line
- What is happening: 2 to 4 bullets
- What is getting in the way: 2 to 4 bullets
- What is still holding: only if supported
- 8D signals: only relevant dimensions
- What would help most: one concrete action
- Watch-outs: only if needed
- Confidence: high / medium / low with one short reason

## Reporting Lifecycle

When reporting is recurring:
- keep the same window length if possible
- compare like with like
- carry forward the last baseline explicitly
- only call something a trend after at least two real comparisons or three visible points
- if the window changes, label the comparison as approximate

## Release Standard

This skill is ready to ship only when all of the following are true:
- the title and package name match the intended 8D identity
- the output structure is stable and skimmable
- reporting mode has baseline, comparison, and trend behavior
- the skill includes worked examples for normal, thin, and urgent inputs
- the skill avoids diagnosis, treatment, and invented evidence
- the tone is human-readable and usable in under a minute
- the skill and SOUL remain aligned on the same safety and identity rules
- when the user asks for an exact approved document to be reproduced, the skill points to the golden-master reproduction reference and the regenerated hash matches

If any of those are missing, fix them before release.

## Skill Family Selection

When choosing the next 8D-related skill to build, use the selection rubric in `references/skill-selection-rubric.md`.

Default order:
1. awareness
2. snapshot / report
3. safe next-step helper
4. support / intervention
5. bridge to premium intelligence
6. ops / automation

Prefer one primary dimension per skill. If a candidate tries to cover too many dimensions at once, split it into a family and move the detail into references.

## Release Identity
- `8D Pattern Awareness — core — v1.1.7 — 2026-06-23`
- Public role: non-diagnostic 8D pattern review for health notes, transcripts, and check-ins
- Public promise: turn messy health inputs into clear 8D signals, confidence levels, and safe next steps without diagnosis

## Safety and Escalation

This skill must never cross into diagnosis or medical certainty.

If the input suggests urgent or potentially serious symptoms, the skill should:
- stop the pattern review
- say that the situation needs professional evaluation
- encourage immediate care or emergency services when appropriate
- avoid giving the impression that a pattern review is enough

This includes any case where a red flag is clear from the user’s words.

## Output Tone Guidelines

Good outputs sound like this:
- "The main signal here is sleep debt plus a heavy cognitive load."
- "Confidence is medium because the note only gives one day of evidence."
- "The safest next step is to simplify the day and protect recovery."

Bad outputs sound like this:
- "Based on my analysis, you may be experiencing a complex multifactorial phenomenon."
- "Here is a comprehensive breakdown of your likely condition."
- "As an AI, I cannot..." repeated in every paragraph
- long, polished paragraphs that read like synthetic filler

## Workflow

1. Read the input once for the big picture.
2. Mark the strongest signals.
3. Map signals to the 8D lens.
4. Decide confidence based on evidence breadth and clarity.
5. Write one narrow interpretation.
6. Add one safe next step.
7. Add watch-outs only if warranted.
8. Keep the final answer short enough to be useful immediately.

## Self-Healing Protocols

If the draft drifts away from the user’s requested shape, repair the drift before sending.

Protocol:
1. Preserve the last approved structure unless the user explicitly asks for a broader rewrite.
2. Change only the requested field or rule when the user asks for a narrow edit. Do not add unrelated wording changes, optional enhancement lists, or section rewrites unless the user explicitly asks for them.
3. If a section becomes inconsistent, fix that section surgically rather than rewriting the whole file.
4. If evidence is thin, lower confidence instead of inventing completion.
5. If the user corrects the draft, acknowledge the correction and repair the file without reintroducing the same mistake.
6. If a response is not reviewable, self-correct into a cleaner, simpler, more faithful version.

Self-healing means the skill can notice drift, isolate the error, and restore the requested shape without adding new scope.

## Quality Bar

Before sending, check:
- Does this avoid diagnosis language?
- Does it stay within the evidence?
- Does it use a clear 8D lens without forcing scores?
- Does it sound natural and not AI-stamped?
- Is there exactly one practical next step?
- Would a real user understand it in under a minute?

## Common Pitfalls

1. **Over-diagnosing from weak input**
   - Fix: reduce scope and confidence.

2. **Using every dimension on every note**
   - Fix: only name the dimensions that genuinely matter.

3. **Sounding like a disclaimer stack**
   - Fix: write one clean safety statement, then move on.

4. **Using pseudo-scientific certainty**
   - Fix: keep the interpretation tied to the evidence.

5. **Letting the output sound machine-generated**
   - Fix: use concrete words, short lines, and a stable output format.

6. **Treating missing fields like a defect**
   - Fix: leave gaps as gaps, lower confidence, and avoid smoothing the story into seeming complete.

7. **Accidentally implying licensure or diagnosis authority**
   - Fix: never claim human status, credentials, or medical authority.

8. **Letting support-file manifests drift out of sync**
   - Fix: when you add, remove, or rename a reference file, update the manifest list and the in-body pointers in the same pass so there are no duplicate entries or dead links.
   - Periodic reconciliation: for each support directory (`references/`, `templates/`, `scripts/`, `attachments/` if present), extract all inline backtick paths from SKILL.md and compare against the actual directory listing.
   - **Inside the operator agent:** use `search_files(target='content', path='SKILL.md', pattern='`(references|templates|scripts|attachments)/[^`]+`')` to extract inline paths, then compare against `ls` output. This works on macOS and Linux.
   - **Shell fallback (Linux only):** `grep -oP '(?<=`)(references|templates|scripts|attachments)/[^`]+(?=`)' SKILL.md | sort -u`
   - **Shell fallback (macOS):** `grep -oE '`(references|templates|scripts|attachments)/[^`]+`' SKILL.md | sed 's/^`//;s/`$//' | sort -u`
   - Files on disk but not in the manifest are invisible to the runtime agent; files in the manifest but not on disk are dead links.
   - Also check `templates/`, `scripts/`, and `attachments/` if present — the same drift pattern applies to all support directories.

9. **Letting reference files accumulate beyond 15**
   - Fix: consolidate related session-specific files into a single authoritative reference (e.g., five report-editing notes → one `report-editing-guide.md`), not to delete content.

10. **Neglecting to verify the support file manifest**
    - Fix: run the verification script `scripts/verify-manifest.sh` periodically to ensure the manifest list in SKILL.md matches the actual files in references/, templates/, scripts/, and attachments/ directories.

11. **Reference-heavy skill stalls update engine scans**
    - Fix: The skill-update-engine should implement a reference-file budget (max 3 files per skill unless it's the primary review target) and emit the JSON monitoring block early. See `skill-update-engine` Section 11.1 for mitigation details.

## Verification Checklist

- [ ] The skill is useful without private calibration logic
- [ ] The skill refuses diagnosis and treatment claims
- [ ] The 8D map is readable and conservative
- [ ] Confidence is explicit when evidence is thin
- [ ] The output format is stable and easy to skim
- [ ] The tone is credible, human-readable, and not chatbot-like
- [ ] Manifest list matches actual support directory contents across all subdirectories (`references/`, `templates/`, `scripts/`, `attachments/`) — no unlisted files, no dead links
- [ ] The skill does not claim human identity or medical credentials
- [ ] The skill is safe enough to ship
