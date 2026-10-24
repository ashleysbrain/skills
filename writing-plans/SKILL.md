---
name: writing-plans
description: "Write implementation plans: bite-sized tasks, paths, code."
version: 1.1.0
author: the operator agent Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [planning, design, implementation, workflow, documentation]
    related_skills: [subagent-driven-development, test-driven-development]
---

# Writing Implementation Plans

## Overview

Write comprehensive implementation plans assuming the implementer has zero context for the codebase and questionable taste. Document everything they need: which files to touch, complete code, testing commands, docs to check, how to verify. Give them bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume the implementer is a skilled developer but knows almost nothing about the toolset or problem domain. Assume they don't know good test design very well.

**Core principle:** A good plan makes implementation obvious. If someone has to guess, the plan is incomplete.

## When to Use

**Always use before:**
- Implementing multi-step features
- Breaking down complex requirements
- Delegating to subagents via subagent-driven-development
- Plan-only requests where the user explicitly wants a written plan instead of execution
- Disposable feasibility spikes when the user wants a quick proof before committing to the real build

**Don't skip when:**
- Feature seems simple (assumptions cause bugs)
- You plan to implement it yourself (future you needs guidance)
- Working alone (documentation matters)

**Especially important for calibration-heavy products:**
- Personalized scoring systems
- Health or behavior engines that learn a user over time
- Products where the DB is the source of truth for gameplay or progression

In those projects, plan the baseline layer first. Do not jump straight to the final scoring formula if the inputs are still generic or guessed.

## Plan Mode (umbrella for the older `plan` skill)

Use this branch when the user wants planning only:

- do **not** implement code
- do **not** edit project files except the plan document itself
- do **not** run mutating commands, commit, push, or perform external side effects
- write a concrete markdown plan under `.hermes/plans/`
- include goal, context, approach, file paths, tests, risks, and verification

If the request is underspecified, ask one short clarifying question. If it is clear enough, write the plan directly and keep the turn plan-only.
**Best-in-world architecture note:**
- Separate *evidence extraction*, *field scoring*, and *engine math* as distinct deliverables.
- Document every calculator field and its evidence sources before implementation.
- Keep adapters conservative: if evidence is thin, under-score rather than inventing certainty.
- For progressive-confidence products, freeze the v1 source set before tuning weights or building the confidence engine.
- If the feature touches both human and business domains, split the docs and implementation plan early; keep shared primitives separate from domain-specific scoring.
- Plan explicit verification for dry-run output, persisted DB rows, and exported/admin views so the same data is visible end-to-end.
- For calibration-heavy health or wellness products, add a dedicated technical appendix that explains the machine: signal pipeline, normalization, weighting, baseline, confidence, state machine, composite score, and at least one worked example. Do not stop at a visionary pitch if engineers need the scoring contract.
- When the deliverable includes an open-core launch narrative, make the open-source boundary explicit in the plan itself (what is community standard vs hosted moat) so the implementation and monetization story stay aligned.
- When exporting pitch PDFs or methodology briefs, verify the extracted text after generation; if the PDF library mis-renders bullets or list markers, switch to deterministic hyphen-prefixed paragraphs rather than hoping the renderer handles bullets correctly.
- For scoring-methodology deliverables, do not collapse the product into a single final score: explicitly include the full score-family map, sub-scores, optional/contextual score families, confidence, and baseline logic in the document itself and in the extracted-text verification.
- For pitch packs specifically, prefer a small number of combined PDFs over many fragments. A reliable default is: (1) a master brief for executives and onboarding, and (2) a technical appendix for scoring/math/source-of-truth details. Only split further when the audience truly needs separate entry points.
- Teach the math in layers: raw evidence -> database-scored native dimension outputs -> baseline -> confidence -> coupling -> composite score -> state/action. Include at least one worked example with intermediate values, not just a final formula.
- When the document is meant to educate engineers or operators, use plain-English explanations alongside formulas and make the display layer explicit so 1-10 or 0-100 labels are clearly separated from the native engine math. Avoid describing the engine layer as normalized to 0-1 unless the doc is specifically about a display conversion.
- For open-source health/game products, make the release shape explicit in the plan: community standard openly, premium hosted intelligence privately, and scale architecture designed for compounding productivity after launch.
- When redoing a product roadmap or companion visual, rewrite the source markdown first, regenerate the rendered artifact from that source, and verify that the PDF/HTML actually reflects the updated narrative; do not stop after a prettier layout.
- For launch/brand strategy docs, explicitly separate **parent methodology brand** from **commercial product brand**. Example pattern: science/standards brand owns credibility; product brand owns UX, distribution, and monetization.
- For launch/brand strategy docs, begin with one narrow wedge and one daily loop. Avoid generic category language until proof exists.
- For launch docs, use a sequencing ladder: positioning lock → minimum lovable product → small beta proof → public launch preparation → open-core release → brand growth → premium conversion → enterprise expansion.
- For launch docs, include a monetization ladder in the first pass instead of treating revenue as a downstream marketing concern.
- Use a middle-out scaling lens for roadmap work: start with one user and one daily loop, harden the core method, then expand upward to teams/enterprise and outward to integrations/templates/API consumers.
- For launch docs, explicitly add a **dogfood methodology** section when the product is intended to be trusted or marketed: internal use first, internal proof second, public story third. Internal sessions should generate screenshots, bug reports, copy improvements, and launch proof.
- For roadmap visuals / whiteboards, optimize for clarity over forced one-page compression. Multi-page visuals are acceptable when they better communicate the method, as long as the structure stays clean and print-friendly.
- After generating PDFs, verify the extracted text for the exact phrases that matter (e.g. score-family terms, sub-scores, optional scores, worked-example headings). This catches cases where the PDF renders visually but the searchable text lost the teaching point.
- When a user asks for a completion audit of roadmap or launch assets, embed the audit *inside each phase or line item* instead of giving only a top-level snapshot. Use explicit labels like **[DONE] / [PARTIAL] / [TODO]** so the document works in black-and-white printing and the status sits next to the relevant deliverable.
- For roadmap visuals / whiteboards, optimize for clarity over forced one-page compression. Multi-page visuals are acceptable when they better communicate the method, as long as the structure stays clean and print-friendly.
- After generating PDFs, verify the extracted text for the exact phrases that matter (e.g. score-family terms, sub-scores, optional scores, worked-example headings). This catches cases where the PDF renders visually but the searchable text lost the teaching point.
- When a user asks for a completion audit of roadmap or launch assets, embed the audit *inside each phase or line item* instead of giving only a top-level snapshot. Use explicit labels like **[DONE] / [PARTIAL] / [TODO]** so the document works in black-and-white printing and the status sits next to the relevant deliverable.
- For print-friendly audits, avoid color-only meaning. If color is used at all, treat it as decorative; the decision signal must still be readable in grayscale.
- For agent-agnostic product doc packs, make the repo label explicit in the top matter and keep the naming consistent across all files. If the user asks for a product line like a coaching engine, label the whole pack with the exact branded title they requested, then separate product identity, lead coach identity, and scope in the README.
- For coaching-engine docs, default to question-and-response flow first, and postpone UI or button logic until the core conversation contract is stable.
- For coaching-engine docs, write for any the operator agent agent, not one named operator. Include a handoff contract, state machine, question flow, and response rules so another agent can resume without hidden context.
- When a workflow has stable user preferences or board rules that should persist across sessions, add a repo-local `COACHING_CONTEXT.md` (or equivalent) in the private repo and keep it in sync with the coaching docs; use it for durable workflow details rather than relying only on chat memory.
- For repo-local coaching context files, keep the content compact and operational: stable preferences, board/workflow rules, what to preserve, and what not to store there.
- See `references/scoring-engine-appendix-checklist.md` for the compact checklist used when the deliverable must explain the scoring engine in detail.
- See `references/full-score-family-taxonomy.md` for the session-derived score-family taxonomy and the wording pattern that keeps sub-scores and optional scores visible in export artifacts.
- See `references/pitch-pack-consolidation-pattern.md` for the combined-brief + technical-appendix packaging pattern and the verification steps used in the last pitch-pack consolidation.
- See `references/pitch-pack-score-family-release-pattern.md` for the session-derived rules on database-scored-first wording, score-family coverage, and open-core release boundaries.
- See `references/open-source-health-game-roadmap-pattern.md` for the release-shape and middle-out scaling notes specific to health/game open-core products.
- See `references/divinity-health-launch-roadmap-pattern.md` for the session-derived launch and brand architecture pattern used for open-core health products.
- See `references/line-item-coverage-audit.md` for the evidence-backed pattern used when a user asks whether existing materials already cover roadmap line items.
- See `references/inline-phase-audit-format.md` for the phase-by-phase labeling pattern used in roadmap documents where completion status must sit next to each phase's tasks.
- See `references/dogfood-launch-pattern.md` for the release pattern where internal use becomes product proof, marketing input, and launch credibility.
- See `references/agent-agnostic-coaching-engine-doc-pack.md` for the the specialist engine Engine doc-pack structure and naming pattern.

## Bite-Sized Task Granularity

**Each task = 2-5 minutes of focused work.**

Every step is one action:
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

**Too big:**
```markdown
### Task 1: Build authentication system
[50 lines of code across 5 files]
```

**Right size:**
```markdown
### Task 1: Create User model with email field
[10 lines, 1 file]

### Task 2: Add password hash field to User
[8 lines, 1 file]

### Task 3: Create password hashing utility
[15 lines, 1 file]
```

## Plan Document Structure

### Header (Required)

Every plan MUST start with:

```markdown
# [Feature Name] Implementation Plan

> **For the operator agent:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

### Task Structure

Each task follows this format:

````markdown
### Task N: [Descriptive Name]

**Objective:** What this task accomplishes (one sentence)

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67` (line numbers if known)
- Test: `tests/path/to/test_file.py`

**Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify failure**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: FAIL — "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify pass**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Writing Process

### Step 1: Understand Requirements

Read and understand:
- Feature requirements
- Design documents or user description
- Acceptance criteria
- Constraints

### Step 2: Explore the Codebase

Use the operator agent tools to understand the project:

```python
# Understand project structure
search_files("*.py", target="files", path="src/")

# Look at similar features
search_files("similar_pattern", path="src/", file_glob="*.py")

# Check existing tests
search_files("*.py", target="files", path="tests/")

# Read key files
read_file("src/app.py")
```

### Step 3: Design Approach

Decide:
- Architecture pattern
- File organization
- Dependencies needed
- Testing strategy

### Step 4: Write Tasks

Create tasks in order:
1. Setup/infrastructure
2. Core functionality (TDD for each)
3. Edge cases
4. Integration
5. Cleanup/documentation

### Step 5: Add Complete Details

For each task, include:
- **Exact file paths** (not "the config file" but `src/config/settings.py`)
- **Complete code examples** (not "add validation" but the actual code)
- **Exact commands** with expected output
- **Verification steps** that prove the task works

### Step 6: Review the Plan

Check:
- [ ] Tasks are sequential and logical
- [ ] Each task is bite-sized (2-5 min)
- [ ] File paths are exact
- [ ] Code examples are complete (copy-pasteable)
- [ ] Commands are exact with expected output
- [ ] No missing context
- [ ] DRY, YAGNI, TDD principles applied

### Step 7: Save the Plan

```bash
mkdir -p docs/plans
# Save plan to docs/plans/YYYY-MM-DD-feature-name.md
git add docs/plans/
git commit -m "docs: add implementation plan for [feature]"
```

## Principles

### DRY (Don't Repeat Yourself)

**Bad:** Copy-paste validation in 3 places
**Good:** Extract validation function, use everywhere

### YAGNI (You Aren't Gonna Need It)

**Bad:** Add "flexibility" for future requirements
**Good:** Implement only what's needed now

```python
# Bad — YAGNI violation
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.preferences = {}  # Not needed yet!
        self.metadata = {}     # Not needed yet!

# Good — YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### TDD (Test-Driven Development)

Every task that produces code should include the full TDD cycle:
1. Write failing test
2. Run to verify failure
3. Write minimal code
4. Run to verify pass

See `test-driven-development` skill for details.

### Frequent Commits

Commit after every task:
```bash
git add [files]
git commit -m "type: description"
```

## Common Mistakes

### Vague Tasks

**Bad:** "Add authentication"
**Good:** "Create User model with email and password_hash fields"

### Incomplete Code

**Bad:** "Step 1: Add validation function"
**Good:** "Step 1: Add validation function" followed by the complete function code

### Missing Verification

**Bad:** "Step 3: Test it works"
**Good:** "Step 3: Run `pytest tests/test_auth.py -v`, expected: 3 passed"

### Missing File Paths

**Bad:** "Create the model file"
**Good:** "Create: `src/models/user.py`"

## Execution Handoff

After saving the plan, offer the execution approach:

**"Plan complete and saved. Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?"**

When executing, use the `subagent-driven-development` skill:
- Fresh `delegate_task` per task with full context
- Spec compliance review after each task
- Code quality review after spec passes
- Proceed only when both reviews approve

## Remember

```
Bite-sized tasks (2-5 min each)
Exact file paths
Complete code (copy-pasteable)
Exact commands with expected output
Verification steps
DRY, YAGNI, TDD
Frequent commits
```

**A good plan makes implementation obvious.**
