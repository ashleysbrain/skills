# Build-Direction Statement Pattern

## When to use
When a principal advisory board, CTO board, or product panel needs a formal build-direction / scope-cut document for principal approval before a build sprint begins.

## Document structure (tested June 2026)
1. **What We're Building** — one-paragraph plain-language product definition. No jargon. The user should read this and know exactly what the product does.
2. **What's In (Release 1 Scope)** — bullet list of features/modules in scope
3. **What's Out (Deferred to Release 2+)** — table of deferred items with WHY each is deferred. This prevents scope creep arguments later.
4. **Build Milestones** — week-by-week table with WHAT and WHY IT MATTERS columns
5. **What Needs to Be True (Assumptions)** — numbered list of assumptions that, if wrong, would change the plan
6. **Safety Rules (Non-Negotiable)** — numbered list of hard gates
7. **What the Builder Needs From the principal** — short bullet list of decisions/actions needed from the approver

## Framing
End with explicit approval framing: "Approve this and [builder] goes. Reply: ✅ approve | 📝 edits | ❌ reject"

## Source synthesis pattern
1. Delegate subagent to read ALL panel workspaces (CTO, Product, Marketing, Research, COO, Design)
2. Extract convergence: what do 3+ boards agree on? That's the core.
3. Extract divergence: where do boards disagree? Surface those as "decisions needed."
4. Check for existing drafts in the CTO or product workspace before writing from scratch.
5. Ground every "what's in" and "what's out" in at least one board's explicit recommendation.

## PDF generation
Use ReportLab with:
- Dark header row on milestone table (#1a1a2e)
- Alternating row backgrounds (#ffffff / #f8f9fa)
- Callout box for the product definition paragraph (backColor #f0f4f8)
- Keep to 1-2 pages maximum

## Session reference
- June 9, 2026: Rewrote Divinity Health build-direction statement from 4-board convergence (CTO, Product, Marketing, principal). Existing CTO draft existed from June 8 but was too technical. Rewritten in plain language with clear scope/defer structure. Delivered as markdown + PDF.
