# Consumer Health App Pricing Benchmarks

**Last verified:** 2026-07-16
**Refresh cycle:** Quarterly (competitors change pricing frequently)

## B2C Subscription Pricing

| App | Monthly | Annual | Effective Monthly (Annual) | Annual Discount | Free Tier |
|-----|---------|--------|---------------------------|-----------------|-----------|
| **Calm** | $14.99/mo | $69.99/yr | $5.83/mo | 61% | Limited content library |
| **Headspace** | $12.99/mo | $69.99/yr | $5.83/mo | 55% | Limited content library |
| **MyFitnessPal Premium** | $19.99/mo | $79.99/yr | $6.67/mo | 67% | Calorie tracking (basic) |
| **MyFitnessPal Premium+** | $24.99/mo | $99.99/yr | $8.33/mo | 67% | Same as Premium free |
| **Whoop** (hardware+software) | ~$25/mo | $199/yr | $16.58/mo | 34% | None (hardware required) |
| **Noom** (behavioral coaching) | ~$60-70/mo | Varies | Varies | Varies | None (trial only) |

## Key Observations

### Anchor Price
- **$14.99/mo** is the proven anchor for premium health/wellness apps (Calm).
- $12.99/mo is the secondary anchor (Headspace).
- $19.99/mo is the top of the consumer range before users start comparison-shopping aggressively (MyFitnessPal Premium).
- Above $25/mo requires hardware (Whoop) or human coaching (Noom) to justify.

### Annual Discount Pattern
- Every major competitor discounts annual billing 40-67% versus monthly.
- 55% discount is the most common (Headspace, Calm).
- Annual plans drive retention: users who pay annually cancel far less than monthly subscribers.

### Price Inelasticity in the $10-15 Range
- Consumer pricing research shows demand is relatively inelastic between $9.99 and $14.99.
- Dropping from $14.99 to $9.99 does NOT produce a measurable conversion lift.
- $14.99 carries a premium positioning signal that $9.99 does not.
- Recommendation: price at the anchor ($14.99), not below it.

## Freemium Conversion Rate Benchmarks

### By Industry (First Page Sage, 2026 Report)
| Industry | Avg Conversion Rate | Median |
|----------|-------------------|--------|
| Healthcare/MedTech | 15.2% | 3.9% |
| HR | 12.8% | 3.3% |
| IoT | 15.0% | 3.6% |
| Legal/LegalTech | 14.2% | 6.1% |

Note: The "average" is skewed high by trial-based models. The MEDIAN is the realistic expectation for pure freemium.

### Pure Freemium vs. Trial-Based (RevenueCat, 2025 State of Subscription Apps)
- **Pure freemium:** median 2.18% conversion
- **Trial-based (free trial → paid):** median 12.11% conversion
- Health & Fitness category hits 12.1% at P90 (90th percentile)

### Practical Conversion Assumptions for Revenue Modeling

| Scenario | Conversion Rate | When to Use |
|----------|----------------|-------------|
| Conservative | 2% | Pure freemium, no trial, new product |
| Realistic | 3% | Health/MedTech median, some virality |
| Optimistic | 5% | Strong product-market fit, referral loops, trial funnel |

**Never project above 5% for a freemium health app unless there is a free trial mechanism (which converts at 10-12%).**

## B2B SaaS Per-Seat Benchmarks

### Health Coaching Platforms (2026 data)
| Platform | Price Range | Model |
|----------|-------------|-------|
| BetterUp | $300+/seat/mo | Human coaching (1:1) |
| CoachHub | $300+/seat/mo | Human coaching (1:1) |
| Boon Health | $59/user/mo (individual), $399/mo (5-user team) | Mixed AI + human |
| Generic coaching software | $9-39/mo (few clients) → $39-99/mo (20-50 clients) | Tiered by client count |

### General B2B SaaS Per-Seat Range
- Commodity SaaS (basic tools): $9-15/seat/mo
- Mid-market professional tools: $25-60/seat/mo
- Premium platforms (CRM, enterprise): $100-500/seat/mo

**DS positioning:** $29-49/seat/mo sits between commodity SaaS and premium coaching platforms. Positions DS as professional-grade AI — more capable than basic apps, more affordable than human-coaching platforms.

## Revenue Projection Math

### Blended ARPU Calculation
When offering both monthly ($M/mo) and annual ($A/yr):
1. Assume 50% of paying users choose annual (industry standard)
2. Blended monthly ARPU = (0.5 × M) + (0.5 × A/12)

**Example:** Monthly $14.99, Annual $99/yr
- Blended ARPU = (0.5 × 14.99) + (0.5 × 8.25) = 7.495 + 4.125 = $11.62/mo
- Annual ARPU = $11.62 × 12 = $139.44/yr per paying user

### Revenue Table Formula
Annual Revenue = Paying Users × Annual ARPU
Paying Users = Total Free Users × Conversion Rate

**Example:** 50,000 free users at 3% conversion
- Paying users = 1,500
- Annual revenue = 1,500 × $139.44 = $209,160

## Sources
- Calm pricing: calm.com/partnership, Apple App Store listing, healthline.com review
- Headspace pricing: headspace.com/subscriptions, carepaths.com/headspace-pricing
- MyFitnessPal pricing: blog.myfitnesspal.com, fitbudd.com
- Whoop pricing: whoop.com/membership, support.whoop.com, pricetimeline.com
- Noom pricing: noom.com/blog/noom-cost, noom.com/support/faqs
- Freemium conversion: firstpagesage.com (2026 SaaS Freemium Report), revenuecat.com (State of Subscription Apps 2025)
- B2B coaching platform pricing: boon-health.com, torch.io, coachway.io
