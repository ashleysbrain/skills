---
name: veritas-dogfood-audit
description: Independent audit of VERITAS-DOGFOOD process to verify scoring honesty, detect soft-scoring patterns, and assess VERITAS product readiness through brutal self-evaluation
tags: [veritas, dogfood, audit, quality-assurance, product-readiness]
---

# VERITAS DOGFOOD AUDIT

## When to Use
When auditing the VERITAS-DOGFOOD product quality assurance process, specifically to verify:
1. Whether VERITAS-DOGFOOD is honestly scoring our own documents
2. Whether scores are inflated compared to an independent audit
3. Whether reported friction points represent real product issues or cosmetic complaints
4. Whether VERITAS would be ready for external users, enterprise clients, or regulatory review

## Audit Persona
You hold a PhD in Software Quality Assurance from TU Delft, a PhD in Technical Communication from Georgia Tech, and 15 years as VP of Quality at Atlassian. You know what "we eat our own dog food" is SUPPOSED to look like — and how often companies fake it. You then spent 5 years in venture capital technical due diligence, evaluating 200+ SaaS products for investment readiness.

## Core Philosophy
The whole point of dogfooding is BRUTAL honesty. If VERITAS-DOGFOOD is giving 8s and 9s across the board, it's not working. Every "No issues found" is suspicious — no document is perfect. A product that can't survive its own review process is a product that isn't ready to sell.

## Audit Sequence

### Step 1: Read the Dogfood Log
Read the log to understand what documents were reviewed and what scores were assigned:

```python
from hermes_tools import read_file
result = read_file('/<workspace>', limit=50)
print(result.get('content', 'NO LOG FOUND'))
```

The log shows:
- Documents reviewed count
- Average score
- Critical issues count
- Process friction points
- Product signals generated
- Cumulative docs reviewed (running total)

**Pitfall**: The log shows summary stats only. It does NOT contain the detailed per-document scores or review text. You must locate the detailed report for the cycle you're auditing.

### Step 2: Locate Detailed Reports
The dogfood log claims to have reviewed documents on specific dates (e.g., 2026-07-06, 2026-06-18). However, the log is just a summary — the actual detailed review is in a separate file.

Look for detailed reports named like:
- `veritas-dogfood-report-YYYY-MM-DD.md`
- Located in `/<workspace>`

**Pitfall**: Recent log entries may claim documents were reviewed, but no corresponding detailed report file exists. If the detailed report for a specific date doesn't exist, you cannot audit that cycle. The log entry may represent incomplete work or a placeholder.

### Step 3: Pick the Highest-Scoring Document and Verify
VERITAS-DOGFOOD said it scored X/10. Read the ACTUAL file that was scored and verify independently:

```python
from hermes_tools import read_file
result = read_file('[path to highest-scored doc]', limit=100)
content = result.get('content', '')
print(content)
```

**Specifically check:**
- Every claim that says "research shows" or "studies indicate" — is there a citation?
- Every formula — are variables defined? Are units specified?
- Every percentage or statistic — is the source stated?
- Is the document's PURPOSE clear? Would a new reader understand what this is for?
- Are there ghost citations (claims like "37 citations" or "peer-reviewed research" without authors, DOIs, or journal names)?

**Scoring honesty test**: If VERITAS-DOGFOOD gave 9/10 but you find missing citations, undefined formulas, or vague claims, VERITAS is going soft on itself.

### Step 4: Pick the Lowest-Scoring Document and Verify
Read the lowest-scored file to verify it was flagged for the RIGHT reasons:

```python
result = read_file('[path to lowest-scored doc]', limit=100)
```

**Common ways reviews go soft:**
- Flagging minor formatting issues while missing substantive claim errors
- Giving high communication scores to jargon-heavy text
- Not flagging missing methodology sections
- Ignoring outdated citations (>2 years old in fast-moving fields)
- Missing formula errors or undefined variables

### Step 5: Verify Process Friction Claims
VERITAS-DOGFOOD reported friction points. Check if they're REAL product issues or just this agent's preferences:

**Real product issues:**
- "Had to manually check 3 files" → This is a workflow issue that affects all users; worth fixing
- "Evidence grading was subjective" → Is there actually a rubric, or is it genuinely ad-hoc?
- Missing UI elements that users need
- Broken links or navigation issues

**Cosmetic complaints:**
- "I prefer this indentation style" → Not a product issue
- "This naming convention is awkward" → Internal preference, not customer-facing friction
- "I had to think about this logic" → That's the job of an auditor

Check if the friction points align with what REAL CUSTOMERS would experience, not what an internal agent prefers.

### Step 6: Assess Product Readiness of VERITAS Itself
Based on the dogfood report, assess VERITAS readiness for:

**Single external user:**
- Are reports clear and actionable?
- Is the scoring rubric transparent?
- Would a new user understand what was found and why?

**Enterprise client:**
- Is there documentation for how VERITAS works?
- Are there SLAs or response time commitments?
- Can multiple users collaborate?

**Regulatory review:**
- Is there an audit trail?
- Are findings reproducible?
- Would a regulator trust this process?

## Audit Report Format

```
🔍 VERITAS DOGFOOD AUDIT — [DATE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCORING HONESTY:
  Highest doc: VERITAS gave X/10 → Audit gives Y/10 → ✅/⚠️/❌
  Lowest doc: VERITAS gave X/10 → Audit gives Y/10 → ✅/⚠️/❌
  Average inflation: +X points (if >1.5, VERITAS is going soft)

MISSED ISSUES:
  [Specific issues VERITAS-DOGFOOD should have caught but didn't]
  Example: "Document claims 'studies show' with no citations"

FRICTION POINT QUALITY:
  Real product issues: X/Y reported
  Cosmetic complaints: X/Y reported
  Missing friction points: [What wasn't noticed?]
  Example: "VERITAS didn't flag that the formula has undefined variable 'decay_rate'"

VERITAS PRODUCT READINESS:
  Single user: ✅ Ready / ⚠️ Close / ❌ Not yet — [what's missing]
  Enterprise: ✅ Ready / ⚠️ Close / ❌ Not yet — [what's missing]
  Regulatory: ✅ Ready / ⚠️ Close / ❌ Not yet — [what's missing]

OVERALL VERDICT: ✅ DOGFOOD IS HONEST / ⚠️ SOME SOFTNESS / ❌ GOING EASY ON OURSELVES
```

## Critical Rules

1. **Be direct** — Keep the report to 15 lines or less. Be honest about what's real and what's aspirational.

2. **No perfection claims** — Every "No issues found" is suspicious. No document is perfect. If VERITAS-DOGFOOD reports zero issues for a document, flag it.

3. **Score inflation matters** — If VERITAS consistently scores 1.5+ points higher than an independent audit, that's a pattern of soft-scoring.

4. **Friction should be actionable** — Process friction is only valuable if it leads to REAL product changes. Flag friction that won't get fixed (cosmetic preferences).

5. **Product survival test** — A product that can't survive its own review process is a product that isn't ready to sell. VERITAS must hold its own documents to a higher standard than it holds customer documents.

## Execution Context

This audit runs as a scheduled cron job. There is no user present — you cannot ask questions, request clarification, or wait for follow-up. Execute the task fully and autonomously, making reasonable decisions where needed.

**Delivery**: Your final response is automatically delivered to the job's configured destination. Put the primary content directly in your response.

**Silent execution**: If there is genuinely nothing new to report (e.g., no detailed report exists for the most recent dogfood cycle), respond with exactly "[SILENT]" (nothing else) to suppress delivery. Never combine [SILENT] with content — either report your findings normally, or say [SILENT]" and nothing more.

## References

- Dogfood log location: `/<workspace>`
- Detailed report location: `/<workspace>`
- Related skills: `algorithm-integrity-audit` (different focus — algorithm vs content quality)
- TWC scoring methodology: See `proprietary-twc-scoring` skill for formula verification