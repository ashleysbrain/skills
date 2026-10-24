# Social Content Batch Template

Use this structure when generating a content batch. Each batch produces a markdown file + PDF.

## Markdown Structure

```markdown
# [Brand] Content Batch [N]
# Generated: [DATE]
# Based on: [source docs used]
# Company: [company structure]

## POST 1 — [Post Type]
[Full copy-paste text of the post]

---

## POST 2 — [Post Type]
[Full text]

---

(repeat for 8-10 posts)

---

## IMAGE CONCEPTS
1. **[Concept Name]** — [Description]. Pairs with Posts [X, Y].
2. (repeat)

---

## POSTING CADENCE
- Monday: [which post type]
- Tuesday: [which post type]
- Wednesday: [which post type]
- Thursday: [which post type]
- Friday: [which post type]
```

## Post Type Checklist

Ensure the batch covers at least 6 of these 9 types:

| Type | Purpose | Key Hook Pattern |
|------|---------|-----------------|
| Curiosity Hook | Stop the scroll | "X and Y are the same problem." |
| Data Insight | Science credibility | "[Study] found [stat]." |
| Personal Story | Vulnerability + proof | "I built X. It told me Y. I ignored it." |
| Category Break | Define by negation | "Most [competitors] do X. We do Y." |
| Founder Origin | Why you built it | "I built the first version for myself." |
| Build Progress | Building in public | "Week N: [accomplishment]." |
| Competitive Reframe | Handle comparisons | "So you're like X? No. X does Y. We do Z." |
| Community Question | Engagement | "What's the one thing that..." |
| Worldview | Philosophy | "[Value statement]. That's not a mission. That's the product." |

## Character Limits

- Twitter/X posts: 280 chars hard limit. Target 250-275 for safety.
- LinkedIn posts: 3,000 chars max. Target 1,200-1,500 for readability.
- Twitter bio: 160 chars.
- LinkedIn headline: 120 chars.

## Image Concept Spec Format

For each image concept, provide:

```
**[N]. [Name]** — [One-line description of what it shows].
- Visual type: [network graph / heatmap / cascade flow / comparison split / infographic]
- Tool: [D3 / matplotlib / Figma / other]
- Pairs with: Posts [X, Y, Z]
- Key elements: [specific data points, colors, labels to include]
```

## PDF Generation

1. Write styled HTML to `/tmp/<brand>-content-batch-N.html`
2. Use branded styling: `.post` boxes with type labels, character counts, tag badges
3. Image concepts in yellow callout boxes (`.img-box`)
4. Cadence in blue callout box (`.cadence`)
5. Render: `weasyprint /tmp/<brand>-content-batch-N.html /tmp/<Brand>-Batch-N-<DATE>.pdf`
6. Deliver: `MEDIA:/tmp/<Brand>-Batch-N-<DATE>.pdf`
```

## File Locations

Save batch markdown to the brand's marketing workspace:
- DS: `/<workspace>`
- Other brands: corresponding `02-social-posts/` directory

PDF goes to `/tmp/` for delivery.
