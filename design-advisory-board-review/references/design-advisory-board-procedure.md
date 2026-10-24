# Design Advisory Board Review Procedure

This document outlines the procedure for conducting a the specialist engine Advisory Board review.

## Mandatory First Step: Load Context
1. Read COACHING_CONTEXT.md in your workdir
2. Read all coach files in coaches/ directory
3. Check for any new design documents since last run

## Common Pitfalls to Avoid
- **Skipping the context check**: Always verify if there are new design documents since the last review (step 3). Missing updates can lead to outdated recommendations.
- **Premature synthesis**: Ensure each advisor review is truly independent before moving to synthesis. Discussing ideas too early can bias individual perspectives.
- **Rushing the feel specification**: The "Feeling Target" (what users should feel in first 5 seconds) is critical - don't treat it as an afterthought.
- **Ignoring the output format**: The specified format is mandatory for consistency. Deviating breaks the review process.
- **Overlooking brand consistency**: Remember to check how recommendations align across all touchpoints, not just the primary product.
- **PDF generation issues**: If the generate-pdf.py script fails, check that:
  - The markdown file exists and is properly formatted
  - You have permission to execute the script
  - The ds-wave-shared directory is accessible
  - The script is called with exactly 4 arguments: input.md output.pdf "Design Advisory Board" "AM"

## Verification Checklist
Before considering the review complete, verify that:
- [ ] All context files have been read
- [ ] Each advisor has provided an independent review
- [ ] The reviews have been synthesized into the required sections
- [ ] The output follows the exact format specified in the template
- [ ] A PDF has been successfully generated
- [ ] The final response includes the MEDIA: line pointing to the PDF

## Phase 1: Individual Advisor Reviews
For each advisor, write their independent review:
- What they see in the product's design landscape today
- Their lane-specific design assessment (human psychology, UX, visual, brand, tech-bridge)
- Their top design recommendation for Divinity Health
- Specific, actionable design direction

### Advisor Perspectives
- **Ian Spalter (Design Innovation Lead)**: Focus on design innovation, inevitable design, cognitive load reduction, and making technology feel invisible.
- **Don Norman (Human-Centered Design Psychology)**: Focus on affordances, signifiers, error prevention, and the three levels of emotional design (visceral, behavioral, reflective).
- **Julie Zhuo (Product Design at Scale)**: Focus on user outcomes, evidence-based design, prioritization, and shipping solutions that solve real problems.
- **John Maeda (Design × Technology Bridge)**: Focus on simplicity laws, design-technology convergence, progressive disclosure, and making complex technology feel simple.
- **Natasha Jen (Brand Design & Visual Identity)**: Focus on brand emotion, category differentiation, visual vocabulary, and provoking reactions.

## Phase 2: Board Synthesis
- Design priorities ranked by impact on human experience
- The "feeling target" — what should users feel in the first 5 seconds?
- Brand consistency check across touchpoints
- Design-system recommendations for implementation
- Outside-the-box thinking — what would nobody else think of?

## PDF Output (Critical)
After writing your review, you MUST generate a PDF:
1. Write the full report to /tmp/design-review-[YYYY-MM-DD].md (use today's date)
2. Run: python3 /<workspace> /tmp/design-review-[YYYY-MM-DD].md /tmp/design-review-[YYYY-MM-DD].pdf "Design Advisory Board" "AM"
3. Your final response MUST include: MEDIA:/tmp/design-review-[YYYY-MM-DD].pdf

## Output Format
---
## Design Advisory Board — Design Review
📅 Date

**Design State**: [Aligned / Needs Direction / Misaligned]

👥 **Advisor Notes:**
- 🎨 Ian Spalter: [2-3 sentence summary — design innovation angle]
- 🧠 Don Norman: [2-3 sentence summary — human psychology angle]
- 📐 Julie Zhuo: [2-3 sentence summary — product design angle]
- 🔄 John Maeda: [2-3 sentence summary — design × technology angle]
- 🖌️ Natasha Jen: [2-3 sentence summary — brand identity angle]

🎯 **Feeling Target**: [What users should feel in first 5 seconds]

📋 **Design Priorities:**
1. [PRIORITY] — why — for whom
2. [NEXT] — why — for whom

💡 **Outside-the-Box Idea**: [One thing nobody else would suggest]

## ⚡ ACTION ITEMS
**1. [ACTION]** — Impact: [why] — Source: [advisor]
→ Reply: ✅ 1 | ❌ 1 | 📝 1: your note

---
⚡ Quick reply: ✅ all, ✅ 1,3, ❌ 2, 📝 3: your idea