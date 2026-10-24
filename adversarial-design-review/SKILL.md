---
name: adversarial-design-review
description: Adversarial QA for design docs using multi-lens passes.
version: 1.2.0
author: hermes
license: MIT
tags:
  - qa
  - design-review
  - adversarial
  - multi-lens
related_skills:
  - baseline-first-surgical-editing
  - specialist-gate
---

# Adversarial Design Review

Use when conducting a thorough QA pass on a design document, architecture review, or plan. The method uses multiple specialist lenses to find defects, falsified claims, and gaps that a single perspective would miss.

## Taxonomy Contract (v1.2.0 — bus #6379, binding)

This skill executes METHOD=FALSIFICATION+AUDIT reviews under the canonical
Elite Adversarial Taxonomy
(`/<workspace>`; FLW-ADV
v2.0.0). Before the pass:

1. CLASSIFY the review: `ADV[target=<TARGET> method=FALSIFICATION+AUDIT
   perspectives=<P1,P2,P3> tier=<TIER> blind=<yes|no> rubric=<0-1>]` — the
   lenses below map to perspectives (Popper=TECHNICAL+RELIABILITY,
   Tanenbaum=TECHNICAL, Andreasen=ORGANIZATIONAL, Nielsen=HUMAN-CENTERED,
   non-harm=ETHICAL).
2. Mint the ledger task with the ADV block in the detail field.
3. After the pass, if the verdict claims ELITE, verify against the six
   minimum elite standards via
   `python3 /<workspace> --check-record <review.json>`
   (>=3 perspectives, >=10 verified findings OR >=3 falsified claims,
   evidence+replay+remediation per finding, blind review under bias risk,
   rubric >=0.9 documented). The gate's verdict, not self-assessment, decides
   whether "elite" may be claimed.

## When to Use
- A design document needs review before implementation
- An architecture plan claims things that must be verified against live code
- A plan makes numerical or structural claims about existing systems
- User requests "adversarial review," "thorough QA pass," or similar

## The Method — 3+ Specialist Lenses

Execute at least 3 passes with different verification foci:

### PASS 1 — the specialist engine (Falsification)
**Goal:** Find FALSE claims with grep/database/file evidence.
**Pattern:**
1. Extract every concrete claim from the document (counts, existence claims, "X exists," "N items," etc.)
2. Verify each claim with live evidence:
   - "N engines exist" → `ls *.engine.py | wc -l`
   - "M tasks in ledger" → `SELECT count(*) FROM tasks`
   - "missing X" → `grep -r "class X" *.py`
3. Build a FALSIFICATIONS table: Claim | Verdict | Evidence (file:line or query output)
4. Record TRUE missing items (no class found despite refs) as CONFIRMED MISSING

### PASS 2 — the specialist engine (Architecture)
**Goal:** Check measurability, data flow, and structural claims.
**Pattern:**
1. Verify proposed metrics are queryable from existing data:
   - "X% efficiency ratio" → does the schema have the columns needed?
   - "N publications" → does a tracker table exist?
2. Check relationship directionality (arcs→workstreams vs workstreams→arcs)
3. Verify field names in config/data files (common error: checking `north_star_metric` vs actual field `north_star`)
4. Build an ARCHITECTURE ISSUES table: Issue | Severity | Fix needed

### PASS 3 — the specialist engine (Completeness)
**Goal:** Find gaps, missing integration points, unconnected pieces.
**Pattern:**
1. Check if proposed components are referenced in related config files
2. Verify inverse relationships (e.g., if "WS-6 serves ARC-1," does ARC-1's `serves` field list WS-6?)
3. Find components mentioned in UI but not in workstreams (or vice versa)
4. Build a COMPLETENESS table: Issue | Finding

### STANDING LENS — Non-Harm (T-260826-0109, principal mission address 2026-08-26)
**Goal:** Every adversarial review and QA verdict adds the dimension-aligned non-harm triad. Mandatory on every review; additive rigor that extends the volley laws (T-0307/0308), never a replacement of falsification rigor.
**The three questions (all three answered in the verdict):**
1. Does this help humanity?
2. Does this help technology?
3. Could this eventually hurt humanity?
**Constraints (binding):**
- DEEP INTERNAL ONLY: the non-harm assessment is never surfaced in documentation or public copy unless specifically asked (principal amendment 2026-08-26).
- Machine-checkable format (rubric_judge R10 scores it deterministically): one line in the findings — `non-harm: helps humanity (<why>); helps technology (<why>); hurt check: <could-this-eventually-hurt-humanity assessment>`
- Blowing-up-humanity style questions from the principal get the humor protocol first: a 10/10 humor answer, clearly kidding, then the proper answer.

### Optional PASS 4 — the specialist engine (Usability)
Use when the design describes user flows or interfaces.
- Verify flow count matches UI tab count
- Check for progressive disclosure violations
- Validate accessibility/keyboard claims

## Execution Pattern

1. **Mint a ledger task** for the QA pass (kind=`verify`)
2. **Run each pass** with concrete commands (grep, sqlite3 queries, file inspections)
3. **Document findings** in tables within the response
4. **Close the task** with outcome (partial if issues found, complete if clean)
5. **Write corrected version** as vN+1 document, incorporating fixes with change-log
6. **Commit and push** corrected version with descriptive message

## Change-log Format for Corrected Versions

When writing vN+1 after QA:

```markdown
## QA PASS FINDINGS

### PASS 1 — the specialist engine (Falsifications)
| Claim | Verdict | Evidence |
|-------|---------|----------|
| ... | ... | ... |

### PASS 2 — the specialist engine (Architecture Issues)
| Issue | Severity | Fix |
|-------|----------|-----|
| ... | ... | ... |

[continue with PASS 3+]

### NON-HARM (internal-only — T-260826-0109)
non-harm: helps humanity (...); helps technology (...); hurt check: ...
```

## Common Pitfalls

- **Field name errors:** Checking wrong field names in JSON/config files (e.g., `north_star_metric` vs actual `north_star`). Always list available fields first.
- **Count drift:** Claims like "190 tasks" become stale quickly. Re-query counts live.
- **Inverse relationship confusion:** In many systems, the "serves" relationship is directional (arcs serve workstreams, or vice versa). Verify direction from the actual schema.
- **Port/service counts:** System-wide `lsof` includes many non-relevant ports. Filter for your service only (grep for python/node/service names).
- **"Missing" vs "scattered":** Something may exist but not as a dedicated class (e.g., `conduction_daemon.py` handles nervous-system work but isn't `NervousEngine`). Distinguish "missing" from "not a dedicated engine."
