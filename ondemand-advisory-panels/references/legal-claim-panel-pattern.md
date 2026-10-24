# Legal / Insurance Claim Panel Pattern

**Added**: 2026-06-12 (Tesla Autopilot claim session)
**Parent**: ondemand-advisory-panels

---

## When to Use This Variant

Any on-demand panel where the principal needs strategic advice for a legal claim, insurance dispute, or litigation matter. Signals:
- "insurance claim," "lawsuit," "attorney," "litigation," "settlement"
- Product liability (Autopilot, medical device, etc.)
- Personal injury with vehicle/technology involvement
- Any claim where the user is the plaintiff pursuing recovery

---

## Panel Composition (5 seats)

1. **Insurance Claims Strategist** — Coverage analysis, carrier-specific tactics, bad faith indicators, policy interpretation
2. **Domain Systems Expert** (vehicle tech, medical device, etc.) — Telemetry data, system logs, failure modes, product liability analysis
3. **Subrogation & Recovery Attorney** — Third-party liability, manufacturer liability path, Made Whole Doctrine, allocation of fault
4. **Biomechanics & Injury Valuation** — Injury causation mapping, future care projection, pain & suffering multipliers, economic damages
5. **Litigation Risk Analyst** — Trial vs. settlement calculus, venue selection, jury dynamics, cost-benefit, mediation timing

---

## Plaintiff's Attorney Perspective (Mattland Review)

Legal claim panels default to the **plaintiff's litigation attorney** perspective:
- Aggressive recovery focus — maximize the principal's net recovery
- Minimize the insurance carrier's leverage
- Preserve the direct manufacturer (Tesla, etc.) liability path
- Do NOT adopt defense counsel or claims adjuster framing

This contrasts with general advisory panels that adopt neutral/strategic perspectives.

---

## Insurance Carrier Correction Protocol

When the user corrects which carrier insures them (e.g., "it was Progressive, not Tesla Insurance"):

1. **Immediately rebuild the strategy** — carrier identity changes everything:
   - Duty to defend analysis
   - Bad faith dynamics (captive vs. third-party carrier)
   - Subrogation incentives (aligned vs. opposed to plaintiff)
   - Policy language and exclusions
   - Settlement behavior patterns

2. **Remove questions that no longer apply** — don't keep stale questions from the wrong carrier's context

3. **Add carrier-specific questions** — each carrier has different policy language, claims processes, and litigation behavior

---

## Question Framework (38 questions across 5 categories)

### Policy & Coverage (7 questions)
Policy number, coverages active, limits per coverage, ADAS/autonomous exclusions, vehicle ownership, gap insurance, effective dates

### The Incident (9 questions)
Date/time/location, technology engaged at impact, warnings issued, conditions, other parties, police report, witnesses, surveillance, driver state

### The Equipment & Data (7 questions)
Make/model/version, technology variant (basic vs. beta), software version, repair status, vehicle location, **PRESERVATION LETTER STATUS** (most urgent), manufacturer outreach

### Injuries & Treatment (8 questions)
Specific injuries, emergency treatment, current plan, ongoing treatment, pre-existing conditions, work missed, impact on principal/business role, quality of life

### Carrier Actions to Date (7 questions)
Claim acceptance, adjuster contact, settlement offers, recorded statement requests, medical authorization forms, subrogation mentions, damage estimates

---

## Urgency Tiers (Time-Sensitive)

### THIS WEEK (Data at risk)
1. **Manufacturer preservation letter** — Send BEFORE data is overwritten (many manufacturers overwrite telemetry in 30-90 days)
2. Request complete insurance policy documents
3. Start injury documentation (daily pain journal, photos, medical records)
4. **DO NOT give recorded statement without counsel**
5. **DO NOT sign medical authorizations without review**

### WITHIN 30 DAYS
6. Retain local counsel in incident jurisdiction
7. Calculate special damages (medical, lost wages, property)
8. File regulatory complaint (NHTSA, FDA, etc.) if applicable

### WITHIN 60 DAYS
9. Engage accident reconstruction expert
10. Engage domain systems expert
11. Decide: manufacturer direct claim vs. insurance-only
12. Evaluate no-fault vs. fault-based claim paths

---

## Landmark Case Research (Required)

Every legal claim panel MUST include web research for:
- Recent verdicts in the same domain (e.g., Autopilot product liability)
- Subrogation cases against the manufacturer by other insurers
- Regulatory investigations or recalls relevant to the technology
- Judge's rulings on similar motions

Example: Benavides v. Tesla (S.D. Fla., Aug 2025) — $243M verdict upheld Feb 2026, jury found Tesla 33% at fault for Autopilot defects. State Farm v. Tesla (Nov 2025) — subrogation case for $880K+. Both directly relevant to any Autopilot claim strategy.

---

## Key Legal Concepts to Research Per Case

- **Made Whole Doctrine** — Plaintiff must be fully compensated before carrier exercises subrogation
- **Comparative fault** — How the jurisdiction allocates fault percentages
- **Bad faith** — Carrier behaviors that support bad faith claims (delay, lowball, misrepresentation)
- **Product liability** — Design defect, failure to warn, manufacturing defect theories
- **Statutes of limitations** — Different clocks for contract, tort, and product liability
- **Subrogation coordination** — Aligning carrier's recovery with plaintiff's direct claim

---

## Workspace Structure

```
your-workspace/[case-slug]/
  advisory-board/
    PANEL_REGISTRY.md        # Panel roster, stage process, corrections log
    STAGE1_MATTLAND_REVIEW.md # Plaintiff's attorney Stage 1 assessment
    coaches/                  # 5 advisor profiles (generic, not real people)
    CASE_FILE.md              # Incident facts, timeline, evidence
    SESSION_LOG.md            # Running session history
    STRATEGY_BOARD.md         # Living strategy document
```

The case slug should be descriptive: `tesla-autopilot-claim`, not generic like `legal-panel-1`.

---

## DO NOT Capture in Primary Memory

Per the isolation rules in the parent skill:
- Case details, legal facts, insurance specifics → stay in panel workspace
- Panel workspace paths → ONE pointer line in MEMORY.md, nothing more
- Injury details, medical info, financial damages → NEVER in MEMORY.md or USER.md
