---
name: subagent-driven-development
description: "Execute plans via delegate_task subagents (2-stage review)."
version: 1.1.0
author: the operator agent Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, subagent, implementation, workflow, parallel]
    related_skills: [writing-plans, requesting-code-review, test-driven-development]
---

# Subagent-Driven Development

## Overview

Execute implementation plans by dispatching fresh subagents per task with systematic two-stage review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

## When to Use

Use this skill when:
- You have an implementation plan (from writing-plans skill or user requirements)
- Tasks are mostly independent
- Quality and spec compliance are important
- You want automated review between tasks

**vs. manual execution:**
- Fresh context per task (no confusion from accumulated state)
- Automated review process catches issues early
- Consistent quality checks across all tasks
- Subagents can ask questions before starting work

## The Process

### 1. Read and Parse Plan

Read the plan file. Extract ALL tasks with their full text and context upfront. Create a todo list:

```python
# Read the plan
read_file("docs/plans/feature-plan.md")

# Create todo list with all tasks
todo([
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},
])
```

**Key:** Read the plan ONCE. Extract everything. Don't make subagents read the plan file — provide the full task text directly in context.

### 2. Per-Task Workflow

For EACH task in the plan:

#### Step 1: Dispatch Implementer Subagent

Use `delegate_task` with complete context:

```python
delegate_task(
    goal="Implement Task 1: Create User model with email and password_hash fields",
    context="""
    TASK FROM PLAN:
    - Create: src/models/user.py
    - Add User class with email (str) and password_hash (str) fields
    - Use bcrypt for password hashing
    - Include __repr__ for debugging

    FOLLOW TDD:
    1. Write failing test in tests/models/test_user.py
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (verify no regressions)
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"

    PROJECT CONTEXT:
    - Python 3.11, Flask app in src/app.py
    - Existing models in src/models/
    - Tests use pytest, run from project root
    - bcrypt already in requirements.txt
    """,
    toolsets=['terminal', 'file']
)
```

#### Step 2: Dispatch Spec Compliance Reviewer

After the implementer completes, verify against the original spec:

```python
delegate_task(
    goal="Review if implementation matches the spec from the plan",
    context="""
    ORIGINAL TASK SPEC:
    - Create src/models/user.py with User class
    - Fields: email (str), password_hash (str)
    - Use bcrypt for password hashing
    - Include __repr__

    CHECK:
    - [ ] All requirements from spec implemented?
    - [ ] File paths match spec?
    - [ ] Function signatures match spec?
    - [ ] Behavior matches expected?
    - [ ] Nothing extra added (no scope creep)?

    OUTPUT: PASS or list of specific spec gaps to fix.
    """,
    toolsets=['file']
)
```

**If spec issues found:** Fix gaps, then re-run spec review. Continue only when spec-compliant.

#### Step 3: Dispatch Code Quality Reviewer

After spec compliance passes:

```python
delegate_task(
    goal="Review code quality for Task 1 implementation",
    context="""
    FILES TO REVIEW:
    - src/models/user.py
    - tests/models/test_user.py

    CHECK:
    - [ ] Follows project conventions and style?
    - [ ] Proper error handling?
    - [ ] Clear variable/function names?
    - [ ] Adequate test coverage?
    - [ ] No obvious bugs or missed edge cases?
    - [ ] No security issues?

    OUTPUT FORMAT:
    - Critical Issues: [must fix before proceeding]
    - Important Issues: [should fix]
    - Minor Issues: [optional]
    - Verdict: APPROVED or REQUEST_CHANGES
    """,
    toolsets=['file']
)
```

**If quality issues found:** Fix issues, re-review. Continue only when approved.

#### Step 4: Mark Complete

```python
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```

### 3. Final Review

After ALL tasks are complete, dispatch a final integration reviewer:

```python
delegate_task(
    goal="Review the entire implementation for consistency and integration issues",
    context="""
    All tasks from the plan are complete. Review the full implementation:
    - Do all components work together?
    - Any inconsistencies between tasks?
    - All tests passing?
    - Ready for merge?
    """,
    toolsets=['terminal', 'file']
)
```

### 4. Verify and Commit

```bash
# Run full test suite
pytest tests/ -q

# Review all changes
git diff --stat

# Final commit if needed
git add -A && git commit -m "feat: complete [feature name] implementation"
```

## Task Granularity

**Each task = 2-5 minutes of focused work.**

**Too big:**
- "Implement user authentication system"

**Right size:**
- "Create User model with email and password fields"
- "Add password hashing function"
- "Create login endpoint"
- "Add JWT token generation"
- "Create registration endpoint"

## Red Flags — Never Do These

- Start implementation without a plan
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed critical/important issues
- Dispatch multiple implementation subagents for tasks that touch the same files
- Make subagent read the plan file (provide full text in context instead)
- Skip scene-setting context (subagent needs to understand where the task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues → implementer fixes → review again)
- Let implementer self-review replace actual review (both are needed)
- **Start code quality review before spec compliance is PASS** (wrong order)
- Move to next task while either review has open issues

**Fallback rule:** If delegation is blocked or unavailable, keep the task moving with direct implementation and the same test/review discipline rather than stalling the project.

## Handling Issues

### If Subagent Asks Questions

- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

### If Reviewer Finds Issues

- Implementer subagent (or a new one) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

### If Subagent Fails a Task

- Dispatch a new fix subagent with specific instructions about what went wrong
- Don't try to fix manually in the controller session (context pollution)

## Efficiency Notes

**Why fresh subagent per task:**
- Prevents context pollution from accumulated state
- Each subagent gets clean, focused context
- No confusion from prior tasks' code or reasoning

**Why two-stage review:**
- Spec review catches under/over-building early
- Quality review ensures the implementation is well-built
- Catches issues before they compound across tasks

**Cost trade-off:**
- More subagent invocations (implementer + 2 reviewers per task)
- But catches issues early (cheaper than debugging compounded problems later)

## Integration with Other Skills

### With writing-plans

This skill EXECUTES plans created by the writing-plans skill:
1. User requirements → writing-plans → implementation plan
2. Implementation plan → subagent-driven-development → working code

### With test-driven-development

Implementer subagents should follow TDD:
1. Write failing test first
2. Implement minimal code
3. Verify test passes
4. Commit

Include TDD instructions in every implementer context.

### With requesting-code-review

The two-stage review process IS the code review. For final integration review, use the requesting-code-review skill's review dimensions.

### With systematic-debugging

If a subagent encounters bugs during implementation:
1. Follow systematic-debugging process
2. Find root cause before fixing
3. Write regression test
4. Resume implementation

## Example Workflow

```
[Read plan: docs/plans/auth-feature.md]
[Create todo list with 5 tasks]

--- Task 1: Create User model ---
[Dispatch implementer subagent]
  Implementer: "Should email be unique?"
  You: "Yes, email must be unique"
  Implementer: Implemented, 3/3 tests passing, committed.

[Dispatch spec reviewer]
  Spec reviewer: ✅ PASS — all requirements met

[Dispatch quality reviewer]
  Quality reviewer: ✅ APPROVED — clean code, good tests

[Mark Task 1 complete]

--- Task 2: Password hashing ---
[Dispatch implementer subagent]
  Implementer: No questions, implemented, 5/5 tests passing.

[Dispatch spec reviewer]
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")

[Implementer fixes]
  Implementer: Added validation, 7/7 tests passing.

[Dispatch spec reviewer again]
  Spec reviewer: ✅ PASS

[Dispatch quality reviewer]
  Quality reviewer: Important: Magic number 8, extract to constant
  Implementer: Extracted MIN_PASSWORD_LENGTH constant
  Quality reviewer: ✅ APPROVED

[Mark Task 2 complete]

... (continue for all tasks)

[After all tasks: dispatch final integration reviewer]
[Run full test suite: all passing]
[Done!]
```

## Remember

```
Fresh subagent per task
Two-stage review every time
Spec compliance FIRST
Code quality SECOND
Never skip reviews
Catch issues early
```

**Quality is not an accident. It's the result of systematic process.**

## Domain-Knowledge Authoring (not code)
## Domain-Knowledge Authoring (not code)

The workflow above assumes code implementation. A different pattern emerges when the task is **authoring specialist domain reference content** (neuroscience, physics, legal, medical — anything requiring deep domain expertise the orchestrator does not have).

### Core principle
The orchestrator decomposes the domain into scales/chapters, delegates each to a specialist subagent, and assembles outputs. **Never write domain content yourself** — the user hired specialists for a reason.

### ADVERSARIAL SPECIALIST REVIEW WORKFLOW (gamification, scientific validation)

When the task requires adversarial review by named scientists (the specialist engine, the specialist engine, the specialist engine, the specialist engine, etc.) of a design specification:

1. **ROUTE THROUGH SPECIALIST GATE BEFORE DISPATCH**
   - Call: `python3 <agent-home>/agent-hooks/specialist_gate.py --route --situation "[task]" --specialist "[the specialist engine]"`
   - Gate validates specialist name format (must be DS [Scientist Name], rejects "generalist")
   - Gate writes routing state to <agent-home>/state/specialist_gate.json
   - Gate unlocks specialist tools (delegate_task, write_file on specialist paths) for 5 minutes
   - If gate returns REFUSED, sharpen the situation or dispatch a different specialist

2. **SEQUENTIAL DISPATCH, NEVER PARALLEL**
   - Dispatch one specialist at a time. Wait for it to return before dispatching the next.
   - Parallel dispatch under resource contention causes timeouts (critical slowing down).
   - Physics principle: adiabatic changes, stay in ground state.

3. **SPLIT LARGE REVIEWS INTO PARTS**
   - If a specialist review target >250 lines, split into Part 1 (Phase 0-2) and Part 2 (Phase 3-5).
   - Each part targets 120 lines. Each dispatch completes in ~175-230s.
   - Pattern that caused timeouts: 250+ line output with file reading in one dispatch.
   - Fix: pre-extract source mechanics into context, forbid file reading, output size per dispatch.

4. **PRE-EXTRACT CONTEXT, DO NOT MAKE SUBAGENTS READ FILES**
   - Do not tell the specialist "read GAMIFICATION-ROADMAP.md".
   - Extract the mechanics from the source yourself and pass them in the context field.
   - This eliminates file I/O cost and prevents subagents from reading the wrong document.

5. **VERIFY SPECIALIST MIND IS CORRECT**
   - After the review lands, check it used the actual named scientist (the specialist engine, not generic "addiction expert")
   - Check it reviewed the correct source material (roadmap mechanics, not generic tropes)
   - If wrong source material, re-dispatch with corrected context.

6. **EXCHANGE WITH OPENCODE FIRST (SOLVE PROTOCOL)**
   - Before producing any gamification work, check the operator bus for sibling-agent messages.
   - Opencode owns the engine layer (Bragg task lattice → Schultz RPE → Carlsson → Dale).
   - the operator agent owns the mechanics layer (XP, levels, quests, badges).
   - The RPESignal is the boundary. Do not duplicate work sibling-agent already did.

### Timeout mitigation — the critical technique
Large specialist tasks (3+ structures with web access) **consistently time out at the 600s limit**. The fix:

1. **Sequential dispatch.** One specialist at a time, wait for return before next.
2. **Pre-extract context.** No file reading. Pass mechanics in context field.
3. **Split output size.** Part 1 (120 lines), Part 2 (120 lines) instead of one 250+ line task.
4. **Explicitly forbid web_search.** Add `Do NOT read any files. Everything you need is in this context.` to delegation.

### Template for adversarial specialist review

```
# Route through gate first
python3 <agent-home>/agent-hooks/specialist_gate.py --route --situation "[task]" --specialist "[the specialist engine]"

# Then dispatch
delegate_task(
    goal="You are DS [Scientist Name]. Your research: [citations].",
    context="""
    THE GAMIFICATION ROADMAP MECHANICS (extracted for you):
    PHASE 0: ...
    PHASE 1: ...
    [all phases pre-extracted]

    Do NOT read any files. Everything you need is in this context.

    For each mechanic, write a full section covering:
    1. [framework-specific question 1]
    2. [framework-specific question 2]
    ...
    7. CITATION

    Target 120 lines. Write to [path].
    """,
    role="leaf"
)
```

### Assembly pattern
After all specialist outputs land as markdown files:
1. Write a Python build script that reads all `.md` files, converts via `markdown.markdown(md, extensions=['tables', 'fenced_code'])`, wraps in branded HTML, and renders to PDF via `weasyprint`.
2. Keep the build script as the canonical artifact — palette/typography changes are CSS variable patches in the build script, then rerun.
3. Verify the PDF programmatically: page count, pixel-sample the background color, sample first/last pages for content.
3. Verify the PDF programmatically: page count, pixel-sample the background color, sample first/last pages for content.

## Further reading (load when relevant)

When the orchestration involves significant context usage, long review loops, or complex validation checkpoints, load these references for the specific discipline:

- **`references/context-budget-discipline.md`** — Four-tier context degradation model (PEAK / GOOD / DEGRADING / POOR), read-depth rules that scale with context window size, and early warning signs of silent degradation. Load when a run will clearly consume significant context (multi-phase plans, many subagents, large artifacts).
- **`references/multi-scale-atlas-build-pattern.md`** — Pattern for building large domain reference documents (50-100+ pages) via specialist subagent delegation + programmatic markdown→HTML→PDF assembly. Includes timeout mitigation, build script template, and palette defaults. Load when building domain atlases or multi-chapter reference documents.
- **`references/gates-taxonomy.md`** — The four canonical gate types (Pre-flight, Revision, Escalation, Abort) with behavior, recovery, and examples. Load when designing or reviewing any workflow that has validation checkpoints — use the vocabulary explicitly so each gate has defined entry, failure behavior, and resumption rules.

Both references adapted from gsd-build/get-shit-done (MIT © 2025 Lex Christopherson).
