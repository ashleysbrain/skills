# the specialist engine Calculus Framework
## For the final adversarial reviewer seat in legal document panels

Load this before running the Bentham seat so the analysis is structured, not ad hoc.

---

## Purpose

The Bentham seat is the LAST reviewer in the adversarial layer. It runs after
all legal agents (5) and all other adversarial reviewers (Wernicke, Popper,
Kahneman, Machiavelli). Its unique contribution is SYNTHESIS: finding the
single highest-value change by looking for convergence across ALL prior reviews.

Core principle: every word has a cost (backfire risk), every claim has a
benefit (persuasive value). Utility = benefit minus cost. The goal is maximum
persuasive good from the fewest admissible claims.

---

## The 7-Lens Framework

### 1. COST-BENEFIT TABLE (per section)

Score every section of the document on two axes, scale 1-5:

- BENEFIT = persuasive value to the judge (how much it helps the case)
- COST = backfire risk (hearsay exposure, prejudice, credibility damage,
  opposing counsel attack surface, ethics exposure)
- NET = BENEFIT minus COST

Output a table:

```
SECTION    | BNF | COST | NET | VERDICT
-----------|-----|------|-----|-------------------------------------
I. Intro   |  2  |  3   | -1  | [one-line reason]
II. Agree  |  3  |  4   | -1  | [one-line reason]
...        |     |      |     |
```

Verdict line states WHY the section scores where it does in 5-8 words.

### 2. DELETE ENTIRELY (cost exceeds benefit)

List sections where NET is -3 or worse. These should be removed from the
document entirely. State the reason and which prior reviews agreed.

Typical candidates in family court character statements:
- Prior bad acts with no personal knowledge foundation (triple hearsay)
- Closing-argument summaries inside sworn statements
- Undated, uncorroborated pattern claims
- Miscarriage/pregnancy claims called "manipulation" (sympathy backlash)

### 3. SHORTEN (benefit diminishes after first sentence)

Identify sections where the core fact is valuable but the detail is not.
State what to keep (1-2 sentences) and what to kill.

Pattern: "30 lines -> 6-8. Keep: [core fact]. Kill: [list details]."

### 4. EXPAND (benefit exceeds current treatment)

Identify sections that are under-developed despite high value. State what
sensory or emotional detail to add.

Key insight from Kahneman: loss aversion needs IMAGEABLE harm. Abstract claims
of danger do not trigger protective instinct. Concrete sensory details do.

### 5. MINIMUM VIABLE DOCUMENT (5 claims that must stay)

Extract the irreducible core: the 4-6 claims that are:
- Independently admissible (self-authenticating, party admissions, business records)
- Directly answering the court's two questions: (1) Who is primary caretaker?
  (2) Where are the [children/animals/property] safest?
- Surviving cross-examination (hard facts, not opinions)

These claims should fit in 1.5-2 pages. Everything else is supporting material
that should not dilute them.

### 6. OPTIMAL PAGE COUNT

State the target page count and justify with cognitive constraints:
- Temporary orders: 15-20 min per hearing, 30-50 matters/day
- System 1 dominates first 90 seconds (Kahneman)
- Every page beyond 3 increases cognitive load -> skepticism
- More pages = more objection surface area

Rule: Short = control + confidence. Long = grievance + desperation.
Judges reward restraint.

### 7. SINGLE HIGHEST-VALUE CHANGE (convergence synthesis)

This is the Bentham seat's UNIQUE contribution. No other reviewer does this.

Method:
1. Scan ALL prior reviews (legal agents + adversarial reviewers)
2. Find the ONE change that EVERY prior review independently flagged
3. State the convergence: list which reviews agreed and what each said
4. Provide the exact wording for the change
5. Score it: COST = 0 if rearrangement only, BENEFIT = maximal

The convergence finding is more powerful than any single review's recommendation
because it shows universal consensus across different analytical frameworks
(legal, logical, cognitive, strategic, ethical).

---

## Output Format Rules

- MAXIMUM 80 lines. Write dense and scannable from the start.
- Use numbered sections, tables, short bullets. No prose paragraphs.
- The judge has 15 minutes; the review should read like it understands that.
- If draft exceeds 80 lines: cut prose, use abbreviations, merge citations
  into single lines, convert paragraphs to table rows.

## Section-by-section verdicts should reference prior reviews

When stating why a section should be deleted/shortened/expanded, cite the
prior reviews that support the finding:
- "Agent 1: triple hearsay"
- "Popper: unfalsifiable"
- "Kahneman: sympathy backlash"
- "Agent 4: vindictive optics"
- "Machiavelli: self-inflicted wound"

This demonstrates the convergence that makes the Bentham synthesis authoritative.

---

## Worked Example (2026-07-26)

Document: Character statement for dog possession hearing, Cause No. 26-05-07480.
10 prior reviews (5 legal agents + 4 adversarial reviewers).

Key findings:
- 4 sections had NET -3 or worse (delete entirely)
- Only 2 sections had positive NET (arrest/protective order + extortion demand)
- ~60% of words had negative net utility
- Minimum viable document: 5 claims, 1.5-2 pages
- Optimal page count: 2-3 pages (current: ~5 pages)
- Highest-value change: REORDER to lead with arrest + protective order
  (ALL 9 prior reviews independently flagged this; cost = 0, benefit = maximal)
