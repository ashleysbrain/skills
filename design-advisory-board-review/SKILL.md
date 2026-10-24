---
name: design-advisory-board-review
category: creative
description: A skill for conducting a structured design advisory board review, particularly for health AI products, following the the specialist engine Advisory Board methodology.
---
# Design Advisory Board Review

A skill for conducting a structured design advisory board review, particularly for health AI products, following the the specialist engine Advisory Board methodology.

## Trigger Conditions
- When you need to conduct a design review with multiple advisors, each bringing a distinct design philosophy
- When reviewing health AI products where psychological safety and human-centered design are paramount
- When preparing for a recurring design review (e.g., daily, weekly) for a product line

## Overview
This skill encapsulates the process used by the the specialist engine Advisory Board to:
1. Read coaching context and advisor profiles
2. Generate independent advisor reviews in their distinct voices
3. Synthesize into board-level design priorities and recommendations
4. Produce a formatted report and PDF output

The process ensures design decisions are grounded in human psychology, not engineering constraints, and follows the North Star: "Psychologically sound for humans."

## Step-by-Step Process

### 1. Load Context (Mandatory First Step)
- Read `COACHING_CONTEXT.md` in the current workspace
- Read all advisor files in the `coaches/` directory (each `.md` file represents one advisor)
- Check for any new design documents since the last review
**Note**: If `COACHING_CONTEXT.md` and/or the `coaches/` directory are not found in the current workspace, they may be located in a board-specific workspace (e.g., `~/your-workspace/[board-name]-private/`). Use `search_files` to locate them if needed.

### 2. Generate Independent Advisor Reviews
For each advisor, write their review covering:
- **What they see**: Their assessment of the current design landscape
- **Lane-specific assessment**: Evaluation through their specialty lens (e.g., human psychology, brand identity, design innovation)
- **Top recommendation**: Their most important design suggestion
- **Actionable direction**: Specific, concrete steps to implement

Each advisor must speak in their distinct voice (see advisor profiles for voice patterns, decision-making style, and red lines).

### 3. Board Synthesis
After collecting individual reviews, synthesize:
- **Design priorities**: Ranked by impact on human experience (not technical feasibility)
- **Feeling target**: What users should feel in the first 5 seconds (visceral level)
- **Brand consistency**: Check across all touchpoints
- **Design-system recommendations**: For implementation teams
- **Outside-the-box idea**: One unconventional suggestion nobody else would think of

### 4. Produce Output
- Write the full report to a markdown file following the required format
- Generate a PDF using the provided script or standard markdown-to-PDF tools, then apply the Da Vinci Creative Organ branding (colors, typography, layout) to ensure brand consistency.
- Include the PDF path in the final response as `MEDIA:/path/to/report.pdf`

## Expected Output Format
```
---
## Design Advisory Board — Design Review
📅 Date

**Design State**: [Aligned / Needs Direction / Misaligned]

👥 **Advisor Notes:**
- 🎨 [Advisor 1]: [2-3 sentence summary — their angle]
- 🧠 [Advisor 2]: [2-3 sentence summary — their angle]
- 📐 [Advisor 3]: [2-3 sentence summary — their angle]
- 🔄 [Advisor 4]: [2-3 sentence summary — their angle]
- 🖌️ [Advisor 5]: [2-3 sentence summary — their angle]

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
```

## Advisor Voice Guidelines
Each advisor has a distinct communication style that must be preserved:

### Ian Spalter (Design Innovation Lead)
- **Tone**: Calm, direct, slightly understated
- **Key phrases**: "If people notice the design, we've already lost.", "Show me the Tuesday morning version.", "The feel IS the feature."
- **Focus**: Cognitive load, inevitable design, motion and feel

### Don Norman (Human-Centered Design Psychology)
- **Tone**: Professorial but warm, authoritative through knowledge
- **Key phrases**: "It's not the user's fault. It's never the user's fault.", "Affordances exist. Signifiers reveal them.", "Visceral. Behavioral. Reflective."
- **Focus**: Error prevention, affordances, three levels of emotional design

### Julie Zhuo (Product Design at Scale)
- **Tone**: Pragmatic, warm, direct
- **Key phrases**: "Who is this for and what do they need?", "What's the job to be done?", "Ship the thing that solves the problem."
- **Focus**: User outcomes, evidence-based prioritization, ship-learn-iterate

### John Maeda (Design × Technology Bridge)
- **Tone**: Thoughtful, intellectual but accessible, playful edge
- **Key phrases**: "Simplicity is about subtracting the obvious and adding the meaningful.", "Design + technology isn't two things. It's one thing with a hyphen."
- **Focus**: Simplicity laws, progressive disclosure, AI-human interaction

### Natasha Jen (Brand Design & Visual Identity)
- **Tone**: Bold, provocative, confident
- **Key phrases**: "Does this provoke a reaction? If not, it's not decoration.", "Stop blanding.", "A brand is not a logo. A brand is a living system."
- **Focus**: Emotional core, category differentiation, visual vocabulary as brand expression

## Common Pitfalls to Avoid
- ❌ Skipping the coaching context and jumping straight to advisor reviews
- ❌ Not writing each advisor's review independently (causes voice crossover)
- ❌ Using a generic tone instead of each advisor's distinct voice
- ❌ Forgetting to check for new design documents since the last run
- ❌ Synthesizing before completing all independent reviews
- ❌ Focusing on technical feasibility over human experience
- ❌ Missing the feeling target (visceral reaction is critical for health AI)
- ❌ Making design decisions based on engagement metrics rather than human outcomes in health contexts
- ❌ Overlooking error prevention and recovery design (Don Norman's red line)
- ❌ Defaulting to safe health AI conventions instead of expressing brand tension (Natasha Jen's red line)
- ❌ Adding features without a coherent design system (Ian Spalter's strong pushback)
- ❌ Defaulting to safe health AI conventions instead of expressing brand tension (Natasha Jen's red line)
- ❌ Generating PDFs without applying Da Vinci Creative branding (colors, typography, layout) – all PDFs must go through the Da Vinci creative organ system.

## Verification Steps
- [ ] Each advisor review is written in their distinct voice (check for voice patterns)
- [ ] Feeling target addresses the visceral level (first 500ms reaction)
- [ ] Design priorities are ranked by human impact, not technical effort
- [ ] At least one actionable item per advisor is included
- [ ] Outside-the-box idea is genuinely unconventional
- [ ] PDF is generated and path included in final response
- [ ] Report follows the exact output format specified

## References
- references/design-advisory-board-procedure.md
- templates/design-review-report.md
- `references/design-review-template.md`: Template for the markdown report
- `references/advisor-voices.md`: Detailed voice guidelines for each advisor

## Example Usage
When tasked with conducting the the specialist engine Advisory Board's daily design review:
1. Run this skill to guide your process
2. Follow the steps exactly, pausing to write each advisor's review
3. Synthesize after all individual reviews are complete
4. Generate the PDF and include `MEDIA:/path/to/report.pdf` in your final response

## Notes
- This skill assumes a workspace structure with:
  - `COACHING_CONTEXT.md`
  - `coaches/` directory containing `.md` files for each advisor
- Adapt the advisor list and voices as needed for different advisory boards
- For health AI products, always prioritize the three emotions: Safe → Understood → Empowered
- Remember: "Design should feel invisible" (Ian Spalter) and "Good design is actually invisible" (Don Norman)