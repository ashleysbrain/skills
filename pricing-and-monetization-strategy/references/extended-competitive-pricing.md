# Extended Competitive Pricing: AI Tools, Open Core SaaS, Automation, B2B Health-Tech

**Last verified:** 2026-07-16
**Source:** Competitive research subagent (12 web searches, official pricing pages, Bain & Co., ChartMogul)

## AI Productivity Tools

| Tool | Free Tier | Pro/Plus | Max/Premium | Enterprise/Team |
|------|-----------|----------|-------------|-----------------|
| ChatGPT | Yes (limited GPT, message caps) | Plus: $20/mo | Pro: $200/mo; Team: $30/user/mo | Enterprise: custom |
| Claude | Yes (limited messages) | Pro: $20/mo ($17/mo annual) | Max 5x: $100/mo; Max 20x: $200/mo | Team: $30/user/mo |
| Notion AI | Free workspace (limited blocks); AI add-on $10/1K credits | Plus: $10/user/mo; Business: $20/user/mo | AI add-on per seat | Enterprise: custom |
| Perplexity | Yes (limited Pro searches/day) | Pro: $20/mo ($17/mo annual) | Max: $200/mo | Enterprise Pro: $40/seat/mo |

**Key pattern:** Universal $20/mo consumer "sweet spot." $200/mo emerging power-user tier. Annual billing ~15% discount. Free tier is aggressively gated -- message caps and rate limits are the primary conversion driver, NOT feature gating. Notion uses a hybrid per-seat + usage-based AI credits model.

## Open Core SaaS

| Platform | Free Tier | Entry Paid | Mid-Tier | Enterprise |
|----------|-----------|------------|----------|------------|
| GitLab | Free (SaaS or self-hosted): unlimited users, 400 CI min/mo | Premium: $29/user/mo (+$19 for Duo AI) | Ultimate: $99/user/mo | Enterprise: custom |
| Notion | Free: unlimited blocks for individuals, limited for teams | Plus: $10/user/mo | Business: $18/user/mo | Enterprise: custom |
| Zoom | Basic: 40-min meetings (restricted for businesses) | Pro: $13.33/user/mo | Business: $18.33/user/mo | Enterprise: custom |

**Conversion drivers:**
- GitLab: CI/CD compute minutes, security scanning, compliance. Self-hosted free then managed cloud.
- Notion: Collaborative features, file upload limits, admin controls. Free to paid at team boundary.
- Zoom: Meeting duration limits + recording + admin. Zoom tightened free tier deliberately.

**Open-core lesson:** Free tier must be genuinely useful solo but frictionful for teams. Conversion happens at the team/admin/security boundary, not the individual feature boundary.

## Workflow / Automation Platforms

| Platform | Free Tier | Entry Paid | Pro | Enterprise |
|----------|-----------|------------|-----|------------|
| Zapier | 100 tasks/mo, 2-step Zaps | Professional: $19.99/mo (750 tasks) | Team/Company: scales to $100s/mo | Custom |
| Make | 1,000 credits/mo, 2 active scenarios | Core: $9-12/mo (10K credits) | Pro: $16-21/mo (10K credits) | Enterprise: custom |
| n8n | Self-hosted free forever (Community) | Cloud Starter: $20-24/mo (2.5K execs) | Cloud Pro: $50-60/mo (10K execs) | Self-hosted Business: $800/mo |

**Pricing model differences:**
- Zapier: Task-based (each step = 1 task). Gets expensive at scale.
- Make: Credit-based (operations consume credits). Generally cheaper.
- n8n: Execution-based (each full workflow run = 1 execution). True open core.

**Key insight for DS:** n8n is the strongest analog -- genuinely free self-hosted with unlimited workflows, paid cloud for convenience. Conversion driver is operational burden (hosting, updates, reliability), not feature gating.

## B2B Health-Tech SaaS Pricing Models

| Model | How It Works | Who Uses It | Pros/Cons |
|-------|-------------|-------------|-----------|
| Per-seat | Charge per user/month | Teladoc, most health-tech | Aligns cost with growth; breaks when AI reduces headcount |
| Per-organization / flat | Fixed monthly/annual org fee | Smaller platforms, clinic software | Predictable; doesn't scale with value |
| Usage / per-session | Pay per consultation | Telehealth, API-based services | Aligns with value; unpredictable budgets |
| Hybrid (seat + usage) | Base fee + per-interaction overage | Growing trend; AI platforms | Captures both adoption and value |

**Emerging trend (Bain 2025):** Per-seat losing ground. Subscription models projected to drop from 60% to 30% of SaaS over next decade as outcome-based and usage-based pricing grows. Health-tech moving toward per-member-per-month (PMPM) for B2B2C employer/health-plan deals.

**Conversion benchmarks (SaaS, 2025-2026):**
- Freemium free-to-paid median: 3-5% (consumer); 8% (B2B SaaS)
- Opt-in free trial (no CC): ~18% conversion
- Opt-out free trial (CC required): ~49% conversion
- "Great" freemium conversion: 15-20%; "good": 6-8%

## Key Takeaways for the specialist engine

1. $20/mo consumer price point is proven across every AI tool category. Health apps cluster at $5-15/mo annual equivalent.
2. Annual billing is non-negotiable -- every successful app offers 40-60% discount.
3. Open core conversion happens at the team boundary, not the individual feature boundary.
4. Hybrid pricing (seat + usage) is the future for AI-heavy platforms.
5. PMPM is the health-tech B2B standard for employer/payer deals.
6. n8n's open-core model is the strongest analog for DS.
7. Requiring a credit card for trials roughly triples conversion rates (18% to 49%).
