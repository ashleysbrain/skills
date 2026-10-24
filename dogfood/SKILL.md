---
name: dogfood
description: "Exploratory QA of web apps: find bugs, evidence, reports."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [qa, testing, browser, web, dogfood]
    related_skills: []
---

# Dogfood: Systematic Exploratory QA and Content Review

## Overview

This skill guides you through systematic exploratory QA testing. Depending on the context, this may involve:
1. **Web Application QA** - Testing web applications using the browser toolset
2. **Content/Document Review** - Reviewing Divinity Science's own content using methodologies like VERITAS DOGFOOD

You will navigate/interact with the target, capture evidence of issues, and produce a structured report.

## VERITAS DOGFOOD Content Review

When reviewing Divinity Science's own content (scoring methodology documents, product specs, platform materials, etc.), use the VERITAS DOGFOOD methodology outlined below. This process serves three purposes simultaneously: Quality Assurance, Product Development, and Content Excellence.

### MANDATORY REVIEW SEQUENCE

#### Step 1: Inventory Content Requiring Review
Scan for all Divinity Science content files that should be reviewed using appropriate paths and the `search_files` tool. Focus on:
- Scoring methodology docs (`/<workspace>`)
- Scoring ecosystem (`/<workspace>`)
- Product specs (`/<workspace>`)
- Website content (`/<workspace>`)
- Agent methodology (`/<workspace>`)
- OpenClaw workspace docs (`/<workspace>`)

Filter for markdown files containing keywords like: `blueprint`, `methodology`, `spec`, `readme`, `about`, `product`, `calibrat`, `scoring`.

Identify newly or recently modified files (using `-mtime -14` with find) as highest priority.

#### Step 2: Select Review Targets
From the inventory, select 2-3 items for THIS review cycle. Prioritize:
1. Files modified since last review (new content = highest risk)
2. Files that are public-facing or customer-facing
3. Files that contain scoring math, claims, or methodology
4. Files that haven't been reviewed in the longest time

#### Step 3: Apply VERITAS Review Methodology
For EACH selected document, run the full VERITAS review pipeline:

**Stage 1: Evidence Level Gate**
Classify the content type (Original Data, Literature Synthesis, Theoretical, Mixed) to determine required review depth.

**Stage 2: Multi-Domain Review**
Evaluate each document across 6 dimensions (score 1-10 for each):

1. **Scientific Accuracy (20%)** — Are claims supported by evidence? Are citations real and accurately represented?
2. **Mathematical Rigor (15%)** — Are formulas correct? Are variables defined? Are assumptions stated?
3. **Methodological Soundness (15%)** — Is the approach valid? Are limitations acknowledged?
4. **Clinical Relevance (15%)** — Does this matter for real humans? Is it actionable?
5. **Ethical Considerations (15%)** — Bias, privacy, inclusivity, harm potential
6. **Communication Quality (20%)** — Is it clear? Would a customer understand it?

Use this review template for each document:
```
DOCUMENT: [filename]
REVIEW DATE: [date]
REVIEWER: VERITAS-DOGFOOD

SCORING:
  Scientific Accuracy: X/10 — [specific issue or "No issues found"]
  Mathematical Rigor: X/10 — [specific issue or "Formulas verified"]
  Methodological Soundness: X/10 — [specific issue or "Approach is sound"]
  Clinical Relevance: X/10 — [specific issue or "Clinically actionable"]
  Ethical Considerations: X/10 — [specific issue or "No ethical concerns"]
  Communication Quality: X/10 — [specific issue or "Clear and accessible"]

COMPOSITE SCORE: X/10

SPECIFIC FINDINGS:
  [Numbered list of specific issues found, with line references if possible]

VERDICT: ACCEPT / ACCEPT WITH REVISIONS / REJECT
```

**Stage 3: Cross-Model Validation**
For any document scoring below 7/10 on any dimension:
- Flag the specific claim
- Note what a customer/competitor/regulator would think when they see it
- Assess reputational risk

**Stage 4: Process Friction Log**
While running the review, document every point where the VERITAS process was:
- Confusing or unclear → This is a UX issue for the product
- Missing a step → This is a product gap
- Overly tedious → This is a workflow optimization opportunity
- Surprisingly smooth → This is a feature to highlight in marketing

#### Step 4: Content Improvement Recommendations
For each reviewed document, produce specific, actionable revision notes:
- NOT "improve the introduction" (vague)
- YES "Line 23: The claim that '8 dimensions capture all wellness' needs a citation or a scope limitation. Suggested revision: '8 dimensions capture the primary wellness domains validated in meta-analytic research (cite: WHO 2024, Diener 2025).'"

#### Step 5: Product Development Signals
After reviewing content, translate findings into product features:
```
PRODUCT SIGNALS FROM DOGFOOD:
  Finding: "I had to manually check 3 different files to verify a formula" 
  → Product feature: Automated cross-reference checker in VERITAS UI

  Finding: "Evidence grading was subjective — I had to guess between MODERATE and STRONG"
  → Product feature: Evidence grading rubric with explicit criteria in the platform

  Finding: "I couldn't tell which version of the calibration file was current"
  → Product feature: Version control integration with diff highlighting
```

#### Step 6: Deliver Report
Produce a report following this format:
```
🐕 VERITAS DOGFOOD REPORT — [DATE] (Weekly)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DOCUMENTS REVIEWED: X
  [filename1]: X/10 — [verdict]
  [filename2]: X/10 — [verdict]

CRITICAL ISSUES FOUND: X
  1. [Issue] → [File:line] → [Recommended fix]
  2. ...

PROCESS QUALITY SCORE: X/10
  (How well did VERITAS methodology work for reviewing our own content?)

FRICTION POINTS: X
  ⚠️ [friction] → [product implication]
  ✅ [smooth point] → [marketing highlight]

PRODUCT SIGNALS:
  1. [Finding] → [Feature recommendation]
  2. ...

CONTENT HEALTH:
  📊 Total DS content files: X
  📊 Reviewed to date: X (X%)
  📊 Average quality score: X/10
  📊 Documents needing revision: X

NEXT WEEK'S REVIEW QUEUE:
  1. [file to review next]
  2. [file to review next]
```

#### Step 7: Update Dogfood Log
Append an entry to the dogfood log following this format:
```
## VERITAS Dogfood Cycle — [CURRENT DATE]
- Documents reviewed: X
- Average score: X/10
- Critical issues: X
- Process friction points: X
- Product signals generated: X
- Cumulative docs reviewed: X (running total)

---
```

**Important Note on File Operations**: When working with files in `/<workspace>`, you may encounter a "Baseline-first gate" that blocks new file writes. If this occurs, you must either:
1. Inspect and patch an existing baseline file first, or
2. Explicitly switch the canonical artifact in the session state before creating a new path
Always check for existing log/report files to append to rather than creating new ones when possible.

## Prerequisites

- Browser toolset must be available (`browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_vision`, `browser_console`, `browser_scroll`, `browser_back`, `browser_press`)
- A target URL and testing scope from the user

## Inputs

The user provides:
1. **Target URL** — the entry point for testing
2. **Scope** — what areas/features to focus on (or "full site" for comprehensive testing)
3. **Output directory** (optional) — where to save screenshots and the report (default: `./dogfood-output`)

## Workflow

Follow this 5-phase systematic workflow:

### Phase 1: Plan

1. Create the output directory structure:
   ```
   {output_dir}/
   ├── screenshots/       # Evidence screenshots
   └── report.md          # Final report (generated in Phase 5)
   ```
2. Identify the testing scope based on user input.
3. Build a rough sitemap by planning which pages and features to test:
   - Landing/home page
   - Navigation links (header, footer, sidebar)
   - Key user flows (sign up, login, search, checkout, etc.)
   - Forms and interactive elements
   - Edge cases (empty states, error pages, 404s)

### Phase 2: Explore

For each page or feature in your plan:

1. **Navigate** to the page:
   ```
   browser_navigate(url="https://example.com/page")
   ```

2. **Take a snapshot** to understand the DOM structure:
   ```
   browser_snapshot()
   ```

3. **Check the console** for JavaScript errors:
   ```
   browser_console(clear=true)
   ```
   Do this after every navigation and after every significant interaction. Silent JS errors are high-value findings.

4. **Take an annotated screenshot** to visually assess the page and identify interactive elements:
   ```
   browser_vision(question="Describe the page layout, identify any visual issues, broken elements, or accessibility concerns", annotate=true)
   ```
   The `annotate=true` flag overlays numbered `[N]` labels on interactive elements. Each `[N]` maps to ref `@eN` for subsequent browser commands.

5. **Test interactive elements** systematically:
   - Click buttons and links: `browser_click(ref="@eN")`
   - Fill forms: `browser_type(ref="@eN", text="test input")`
   - Test keyboard navigation: `browser_press(key="Tab")`, `browser_press(key="Enter")`
   - Scroll through content: `browser_scroll(direction="down")`
   - Test form validation with invalid inputs
   - Test empty submissions

6. **After each interaction**, check for:
   - Console errors: `browser_console()`
   - Visual changes: `browser_vision(question="What changed after the interaction?")`
   - Expected vs actual behavior

### Phase 3: Collect Evidence

For every issue found:

1. **Take a screenshot** showing the issue:
   ```
   browser_vision(question="Capture and describe the issue visible on this page", annotate=false)
   ```
   Save the `screenshot_path` from the response — you will reference it in the report.

2. **Record the details**:
   - URL where the issue occurs
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Console errors (if any)
   - Screenshot path

3. **Classify the issue** using the issue taxonomy (see `references/issue-taxonomy.md`):
   - Severity: Critical / High / Medium / Low
   - Category: Functional / Visual / Accessibility / Console / UX / Content

### Phase 4: Categorize

1. Review all collected issues.
2. De-duplicate — merge issues that are the same bug manifesting in different places.
3. Assign final severity and category to each issue.
4. Sort by severity (Critical first, then High, Medium, Low).
5. Count issues by severity and category for the executive summary.

### Phase 5: Report

Generate the final report using the template at `templates/dogfood-report-template.md`.

The report must include:
1. **Executive summary** with total issue count, breakdown by severity, and testing scope
2. **Per-issue sections** with:
   - Issue number and title
   - Severity and category badges
   - URL where observed
   - Description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshot references (use `MEDIA:<screenshot_path>` for inline images)
   - Console errors if relevant
3. **Summary table** of all issues
4. **Testing notes** — what was tested, what was not, any blockers

Save the report to `{output_dir}/report.md`.

## Tools Reference

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to a URL |
| `browser_snapshot` | Get DOM text snapshot (accessibility tree) |
| `browser_click` | Click an element by ref (`@eN`) or text |
| `browser_type` | Type into an input field |
| `browser_scroll` | Scroll up/down on the page |
| `browser_back` | Go back in browser history |
| `browser_press` | Press a keyboard key |
| `browser_vision` | Screenshot + AI analysis; use `annotate=true` for element labels |
| `browser_console` | Get JS console output and errors |

## Tips

- **Always check `browser_console()` after navigating and after significant interactions.** Silent JS errors are among the most valuable findings.
- **Use `annotate=true` with `browser_vision`** when you need to reason about interactive element positions or when the snapshot refs are unclear.
- **Test with both valid and invalid inputs** — form validation bugs are common.
- **Scroll through long pages** — content below the fold may have rendering issues.
- **Test navigation flows** — click through multi-step processes end-to-end.
- **Check responsive behavior** by noting any layout issues visible in screenshots.
- **Don't forget edge cases**: empty states, very long text, special characters, rapid clicking.
- When reporting screenshots to the user, include `MEDIA:<screenshot_path>` so they can see the evidence inline.
