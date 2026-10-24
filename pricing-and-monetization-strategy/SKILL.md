---
name: pricing-and-monetization-strategy
description: Produce pricing and revenue strategy recommendations for DS products. Covers competitor pricing benchmarking, freemium/open-core tier design, wedge feature analysis, B2B tiering, and revenue projections with conversion-rate math. Use when asked to analyze pricing, recommend a price point, design free vs premium boundaries, or project subscription revenue.
version: 1.1.0
metadata:
  hermes.tags: [pricing, monetization, freemium, open-core, subscription, b2c, b2b, revenue, strategy, saas]
  hermes.category: operations
---

# Pricing and Monetization Strategy

Produce evidence-based pricing recommendations for DS products and features. Combines competitor benchmarking, consumer psychology, freemium conversion economics, and B2B SaaS tiering into a structured recommendation document.

## When to Use

- User asks "what should we charge for X?" or "is $Y the right price?"
- Designing free vs premium feature boundaries (the "value cliff")
- Evaluating whether a specific feature (process flow saving, saved dashboards, etc.) is a good conversion wedge
- Structuring B2B/B2BU pricing tiers
- Projecting subscription revenue at various user scales
- Reviewing an open core monetization strategy

## Methodology (7 Steps)

### 1. Read the Case File / Product Context
- Understand what the product does, who the user is, and what pricing is being considered
- Identify constraints from the founder/user (e.g., "free tier must genuinely help", "not a crippled demo")
- Note existing revenue models that the new pricing must extend or complement

### 2. Competitor Pricing Benchmark (batch web searches)
Run parallel web searches for 5-7 comparable products. For health/wellness apps, the standard comparison set is:
- **Calm** — meditation/wellness anchor price
- **Headspace** — meditation competitor
- **MyFitnessPal** — health tracking freemium
- **Whoop** — hardware+software premium
- **Noom** — behavioral coaching premium

For B2B SaaS, search for per-seat pricing of comparable platforms (coaching platforms, health platforms, productivity tools).

**Key data points to capture per competitor:**
- Monthly price
- Annual price
- Effective monthly price if billed annually (annual discount %)
- Whether they offer a free tier or only a free trial

**Batch all competitor searches in one assistant turn** — they are independent queries.

### 3. Price Point Recommendation
- Identify the "anchor price" — the price the market leader charges. This sets consumer expectations.
- For health/wellness B2C: Calm's $14.99/mo is the proven anchor. Headspace at $12.99/mo is the secondary anchor.
- Recommend BOTH a monthly and an annual price. Annual should be 40-55% cheaper than monthly (effective rate) — this is industry standard and drives retention.
- Explain why NOT the lower price (revenue left on table, no conversion benefit in the $10-15 range due to price inelasticity)
- Explain why NOT a higher price (unless there's hardware, human coaching, or medication to justify it)

### 4. Free vs Premium Boundary Design
Define the free tier, the value cliff(s), and the premium tier.

**Free tier principles:**
- Must deliver genuine value (not a crippled demo)
- Should solve ONE complete use case end-to-end
- Creates the "I want more" moment naturally

**Value cliff patterns (the moment a user needs to upgrade):**
- **Save/reuse** — "I want to save this and use it again" (primary wedge)
- **Concurrency** — "I want to run multiple things at once" (power user trigger)
- **Depth** — "I want the deeper/more advanced engines" (curiosity trigger)
- **Volume** — "I've hit the limit and need more" (consumption trigger)

**Premium tier = the system builder tier.** Free = "get one good answer." Premium = "build a system over time."

### Anti-Churn Design for Saved Artifacts (Critical for Retention)

When the premium value proposition includes saving/reusing artifacts (process flows, dashboards, templates), the #1 churn risk is **internalization**: users save a flow, run it 3-5 times, internalize the process, then cancel. The saved artifact becomes a finite-value template, not an ongoing subscription.

**The fix: saved artifacts must be LIVING, not static.** Design premium saved features so they:

1. **Auto-update when underlying engines improve** — New capabilities propagate to saved flows automatically. The user's saved flow gets better over time without effort.
2. **Pull in live/new data** — Wearables, journals, changing goals re-contextualize the flow each time it runs. If the flow can ingest fresh data, it stays relevant.
3. **Show progress tracking over time** — "You've run this 12 times, trending up." Visible evolution gives the user a reason to keep the subscription.
4. **Offer seasonal/dynamic adjustments** — Winter vs summer optimization, life-stage shifts, changing priorities. The flow adapts to context.

**Test:** If a saved flow in month 3 is identical to month 1, the user cancels. If it has evolved with new insights and data, they stay. Design for evolution, not preservation.

**When this applies:** Any product where the premium tier includes saved/reusable artifacts AND the product has access to changing input data (health data, behavioral data, performance metrics). If inputs are static, saved artifacts have finite shelf life and churn is inevitable.

### 5. Wedge Feature Evaluation
When asked whether a specific feature drives paid conversion, evaluate against:
- **Sunk cost / investment:** Does the user invest time/effort in the feature before hitting the paywall? (Yes = good wedge)
- **Contextual paywall moment:** Is the upgrade prompt triggered at peak value/Intent? (Yes = good wedge)
- **Stickiness / return visits:** Does saving create a reason to come back? (Needs reinforcement via notifications/reminders)
- **Comparison to competitors' wedges:** Is this stronger or weaker than how comparable apps gate their premium?

**Verdict format:** "Yes/no — this is/isn't a good wedge because..." + specific reinforcement recommendations.

### 6. B2B / B2BU Tier Structure
Design 3 tiers using per-seat pricing (the dominant B2B SaaS model):

| Tier | Price Range | Target | Key Differentiators |
|------|-------------|--------|---------------------|
| Team / Starter | $20-35/seat/mo | Small orgs (2-10 seats) | All B2C premium + shared resources + basic analytics |
| Professional / Business | $40-60/seat/mo | Mid-size (10-50 seats) | Custom features + white-label + advanced analytics + priority support |
| Enterprise | Custom ($30K-100K+/yr) | Large orgs (50+ seats) | Custom development + dedicated success + SSO/security + SLA |

**B2BU rule:** Professionals within a B2B org inherit their org's tier. No separate individual billing.

## Revenue Projection
Use these standard assumptions (cite sources):
- **50% of paying users choose annual** (industry standard for health/consumer apps)
- **Freemium conversion rate for Health/MedTech: 2-5%** (First Page Sage 2026: 3.9% Healthcare/MedTech average; RevenueCat 2025: 2.18% for pure freemium, 12.11% for trial-based)
- **Blended ARPU calculation:** If monthly is $M and annual is $A/yr ($A/12 per month effective), then blended monthly ARPU = (0.5 × M) + (0.5 × A/12)

**Revenue table format:**
| Total Free Users | Conversion % | Paying Users | Annual Revenue |
|---|---|---|---|
| 10K / 50K / 100K | 2% / 3% / 5% | computed | computed |

Always show the range (conservative 2%, realistic 3%, optimistic 5%).

## Unit Economics for AI-Powered Freemium (Cost Analysis)

Revenue projections mean nothing without per-user cost analysis. For AI-powered products, **LLM costs can consume 30-50% of subscription revenue**. Run this cost model alongside every revenue projection.

### Cost Categories Per User/Month

| Cost | Range | Notes |
|------|-------|-------|
| LLM API calls | $2-5/mo | Depends on engine count, model tier, call frequency. Multi-engine stacking (3+ engines per request) pushes to the high end. |
| Payment processing | ~$0.73 | Stripe (~2.9% + $0.30) on $14.99/mo |
| Infrastructure | $0.50-1.50/mo | Compute, storage, bandwidth per user |
| Support allocation | $0.50-1.00/mo | Amortized CS cost |

**Total: $3.73-$8.23/user/month.**

### Margin Analysis

At $14.99/mo: **Best case margin** = $11.26 (75%). **Worst case margin** = $6.76 (45%).

**Power user risk:** Users running flows daily (30+ requests/mo) with multi-engine stacking can burn $5-8/mo in API costs alone. At worst case, **power users go net-negative** — they cost more to serve than they pay.

### Cost Mitigation Strategies

1. **Aggressive caching** — Cache common query patterns and reuse results without fresh LLM calls. If 2 users ask similar questions, serve the cached engine output.
2. **Model tiering** — Route simple categorization/routing tasks to cheap models ($0.25-1/M tokens). Reserve expensive models for complex analysis requiring deep reasoning.
3. **Flow reuse** — When a saved flow re-runs, check if inputs changed. If not, serve cached results. If only one dimension changed, re-run only the affected engine.
4. **Usage caps on free tier** — Limit free users to N requests/month to control API cost exposure. This is separate from feature gating.

### When Unit Economics Don't Work

If projected per-user costs exceed 60% of subscription price, the pricing model needs adjustment BEFORE launch:
- Raise price
- Reduce engine depth in the default flow
- Add a usage-based overage component for power users
- Require annual (locks in revenue before API costs accrue)

## Document Format

Structure the output document with these sections:
1. **B2C Pricing** — comparison table + recommendation with rationale
2. **Free vs Premium Line** — free tier features, value cliff(s), premium features
3. **Wedge Feature Analysis** — if a specific feature was proposed as the conversion driver
4. **B2B Tier Structure** — 3-tier table with per-seat pricing
5. **Revenue Projection** — table with conversion scenarios
6. **Summary Recommendations** — bullet list of the specific calls
7. **Glossary** — define all jargon (ARPU, ARR, churn, freemium, open core, per-seat, value cliff, wedge feature)

## Word Count Management

Many pricing analysis requests come with a word limit (commonly 1500 words). To manage this:

1. **Write the full document first** — completeness over brevity on first pass
2. **Check word count** with `wc -w <file>`
3. **Trim iteratively** using `patch` (mode='replace') — target the most verbose sections:
   - Collapse multi-paragraph explanations into single dense paragraphs
   - Remove transitional phrases ("Here's why:", "Let me explain")
   - Shorten table headers (e.g., "Monthly Price" → "Monthly")
   - Merge adjacent sentences with the same subject
4. **Re-check** after each trim pass until under the limit

**Pitfall:** Tables with long column headers eat word count fast. Use abbreviated headers and put full descriptions in surrounding text.

## Pitfalls & How to Avoid Them

- **Don't recommend a price without competitor data** — Always benchmark against at least 4-5 comparable products. Consumer pricing is anchored by what users already pay for similar tools.
- **Don't forget the annual plan** — Monthly-only pricing leaves 40-55% of revenue on the table and inflates churn. Always propose both.
- **Don't overstate freemium conversion** — 2-5% is the honest range for Health/MedTech. Don't project revenue at 10%+ conversion unless there's a specific reason (free trial model, strong viral loop).
- **Don't make the free tier useless** — A crippled demo converts worse than a genuinely useful free tier. The free tier must solve one complete use case.
- **Don't confuse B2C and B2B pricing** — B2C is per-user subscription. B2B is per-seat with org-level features (analytics, SSO, admin controls). Don't apply B2C pricing to B2B prospects.
- **Don't forget B2BU inheritance** — Professionals within a B2B org don't get separately billed. The org pays; the professional inherits.
- **Don't skip unit economics** — LLM costs for AI-powered products can consume 30-50% of revenue. Power users can go net-negative. Always model per-user costs alongside revenue projections (see Unit Economics section above).
- **Don't design saved artifacts as static templates** — If the premium tier includes saved/reusable artifacts (flows, dashboards, templates), they MUST be living (auto-updating, data-integrating). Static saved artifacts lead to churn after month 3 when users internalize the process. See Anti-Churn Design section above.
- **Don't over-engineer B2B tiers early** — Full 3-tier B2B pricing is premature until 10+ organic B2B signups validate demand. Start with a flat Teams plan and let the market tell you what to build.
- **Don't confuse "what the feature does" with "why users pay"** — Saving workflows is a feature. Proven health outcomes is the moat. ChatGPT and Notion AI already have saved workflows. Market the outcomes, not the features.
- **Always define jargon** — Pricing documents may be read by non-technical stakeholders (investors, partners, board members). Include a glossary.

## Extended Competitive Landscape

Beyond consumer health apps, DS pricing must be benchmarked against AI productivity tools and open core SaaS. See `references/extended-competitive-pricing.md` for full data tables.

**AI Productivity Tools (the $20/mo standard):**
- ChatGPT Plus, Claude Pro, Notion AI, Perplexity all charge $20/mo for consumer
- $200/mo emerging as power-user tier (ChatGPT Pro, Claude Max)
- Free tier conversion driver: message caps and rate limits (NOT feature gating)

**Open Core SaaS (the team-boundary conversion model):**
- GitLab: free solo, paid at team/admin/security boundary ($29/user/mo)
- n8n: closest analog to DS -- free self-hosted unlimited, paid cloud ($20-60/mo), enterprise ($800+/mo)
- Conversion lesson: free tier must be genuinely useful solo but frictionful for teams

**Workflow/Automation Tools (the saved-workflow pricing model):**
- Zapier: task-based pricing (100 free tasks/mo, $19.99/mo entry)
- n8n: execution-based (free self-hosted, paid cloud per execution)
- DS process flow saving maps most closely to n8n's model

## Dispatch Pattern for Panel Analysis

When running a pricing analysis via advisory panel subagents, DO NOT use a single orchestrator with 6+ advisors -- it will timeout at 600s. Instead, split into 3 parallel leaf subagents:

1. **Pricing Analysis** -- B2C price validation, free/premium line, wedge analysis, B2B tiers, revenue projections
2. **Red Team Attack** -- cannibalization, churn, competitive undercut, unit economics, complexity risks
3. **Competitive Research** -- web search for real pricing data across health apps, AI tools, open core SaaS, automation tools

Each completes in 50-165 seconds. Then synthesize the 3 outputs into one brief in the parent session. See `subagent-anti-timeout-patterns` Pattern 29.

## Founder Decision Logging (Post-Analysis)

When presenting a pricing/monetization analysis with open questions for the founder:

1. **Present with numbered questions** — Q1, Q2, etc. Each question tagged with urgency: "MUST ANSWER NOW", "NEED WITHIN 48 HOURS", "CAN WAIT".
2. **Log answers immediately to the case file** — When the founder responds, append a DECISIONS LOG section to the original case file with a table: Question, Answer, Status (Confirmed / Deferred / Rejected).
3. **Update the synthesis document** — Add a decisions table at the top of the synthesis doc so future readers see the resolution without hunting.
4. **State implications** — For each confirmed decision, state what it unlocks architecturally (e.g., "Q2=YES means living-flows anti-churn strategy is technically viable").
5. **Track deferred decisions** — Deferred items must note what blocks launch and when they must be resolved.

**Pattern:** Confirmed answers close risks. Deferred answers keep risks open. The case file is the single source of truth for which risks are closed and which remain.

## References

- `references/consumer-health-app-pricing-benchmarks.md` — Current pricing data for Calm, Headspace, MyFitnessPal, Whoop, Noom, and freemium conversion rate benchmarks. Refresh periodically as competitors change pricing.
- `references/extended-competitive-pricing.md` — AI productivity tools (ChatGPT, Claude, Notion AI), open core SaaS (GitLab, n8n, Zoom), workflow automation (Zapier, Make, n8n), and B2B health-tech pricing models. Includes B2B conversion benchmarks and PMPM trend data.

## Related Skills
- `partnership-strategy-and-platform-architecture` — Partnership/revenue-share deals (Costco, Strava), B2B organism partnerships, demand-driven adoption loop. This skill handles PRODUCT pricing; that skill handles PARTNERSHIP pricing.
- `product-advisory-panel-review` — CPO Board daily review (may surface pricing questions)
- `marketing-advisory-panel-review` — CMO Board daily review (positioning affects price perception)

## Change Log
- v1.1.0 (2026-07-16): Added Anti-Churn Design for saved artifacts (living vs static flows), Unit Economics for AI-powered freemium (per-user cost model with margin analysis), Founder Decision Logging pattern, and 4 new pitfalls (unit economics, static templates, B2B over-engineering, feature-vs-moat confusion). Bumped from v1.0.0.
- v1.0.0 (2026-07-16): Initial version. Captured from the specialist engine + Genius Engine open core monetization analysis session. Includes competitor pricing data for consumer health apps, freemium conversion benchmarks, and the 7-step methodology for producing pricing recommendation documents.
