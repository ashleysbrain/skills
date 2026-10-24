# Adversarial Attack Framework — Six Attack Vectors

This reference details the six attack vectors the adversarial red team systematically reviews. Use this as a checklist when running adversarial attacks.

## Vector 1: Platform Resistance Attack

**Lens:** Legal/Regulatory (AI The Adversary) + Competitive (Ben Thompson)

**Questions to ask:**
- Why would the platform let us wrap their product?
- What if they block APIs or change terms of service?
- What if they build the feature themselves?
- What if they demand revenue share for partner access (20-30% is common)?
- What if they revoke API access overnight?

**Historical examples:**
- Twitter API pricing change (2023) killed 100+ third-party apps overnight
- Reddit API changes (2023) broke Apollo, Reddit is Fun, and dozens of clients
- Linear v2 API deprecation (2025) broke 50+ integrations

**Vulnerability indicators:**
- Strategy depends on platform APIs
- No commercial partnership mentioned
- Assumes platforms will play nice
- No "Plan B" if APIs are blocked

---

## Vector 2: Monetization Attack

**Lens:** Business Model Skeptic (Reed Hastings)

**Questions to ask:**
- Why would customers pay for this?
- What if they ask for free?
- What if competitors undercut by 50%?
- What if platforms pass costs to users and users revolt?
- What if enterprise procurement blocks deals for 18 months?

**Historical examples:**
- Enterprise SaaS sales cycles average 12-18 months (Gartner 2024)
- Security teams block external API access to 65% of enterprise data (McAfee 2025)
- CFO rejection is the #1 deal killer for new AI vendors (Salesforce 2025)

**Vulnerability indicators:**
- Strategy assumes customers will pay
- No pricing model details
- No procurement/sales cycle analysis
- Assumes friction-free adoption

---

## Vector 3: Architecture Attack

**Lens:** Technical Failure Mode Engineer (Dr. Andrew Ng Attack Mode)

**Questions to ask:**
- What if we can't scale to 10 platforms?
- What if per-customer deployment costs kill margins?
- What if API changes break everything?
- What if hot-deployment fails?
- What if rate limits restrict real-time scoring?

**Historical examples:**
- Jira API: 1000 requests/hour limit for enterprise (insufficient for 10,000-ticket workspaces)
- Multi-tenant to per-customer migration costs $50-100K per customer
- Hot-deployment failures caused 3-hour outages at major AI companies (2024-2025)

**Vulnerability indicators:**
- Strategy assumes multi-tenant works for all customers
- No per-customer cost analysis
- No API rate limit analysis
- No migration/deployment strategy

---

## Vector 4: Legal/Regulatory Attack

**Lens:** Legal/Regulatory (AI The Adversary)

**Questions to ask:**
- What if FTC claims false advertising for scoring claims?
- What if GDPR blocks EU deployment?
- What if platforms claim IP infringement?
- What if state AGs investigate data practices?
- What if FTC demands peer-reviewed validation studies?

**Historical examples:**
- FTC fined health apps $500K+ for unsubstantiated claims (2024-2025)
- GDPR blocked 30% of US health AI apps from EU (2024)
- State AGs investigated 15 AI companies for data practices (2025)

**Vulnerability indicators:**
- Marketing makes claims without validation studies
- No regulatory clearance mentioned
- No GDPR/data residency analysis
- No disclaimer strategy

---

## Vector 5: Market Timing Attack

**Lens:** Market Timing Reality Check (Elad Gil)

**Questions to ask:**
- Is this too late? Too early?
- Is the market saturated?
- Are VCs burned on similar strategies?
- What competing narratives exist?
- What if incumbents launch native features next week?

**Historical examples:**
- "AI wrappers" narrative peaked Q3 2024, 80% of funded startups failed or pivoted by 2026
- VCs raised $2B for wrapper companies in 2024, now say "no more wrappers"
- Incumbents launched native AI features (Salesforce Einstein, Atlassian Intelligence, Notion AI) starting 2024

**Vulnerability indicators:**
- Strategy assumes green field market
- No competitive landscape analysis
- No VC sentiment check
- No incumbent response analysis

---

## Vector 6: Incumbent Response Attack

**Lens:** Competitive Threat (Ben Thompson) + Market Timing (Elad Gil)

**Questions to ask:**
- What if the platform launches a competitive feature next week?
- How do we respond?
- What if they hire a better team than us?
- What if they have more data than us?
- What if they offer it for free (bundled)?

**Historical examples:**
- Notion AI launched in 2023, killed 5+ third-party Notion add-ons
- Atlassian Intelligence launched in 2024, bundled task scoring for free
- Linear Goals announced in 2025, made 3+ goal-tracking startups obsolete

**Vulnerability indicators:**
- Strategy assumes incumbents won't respond
- No moat analysis
- No response strategy
- Assumes first-mover advantage (rarely sustainable in platform markets)

---

## Using This Framework

When running an adversarial attack:

1. **For each vector, ask the questions**
2. **For each YES answer, construct a specific harm scenario** with numbered steps
3. **Rate severity:** CRITICAL (business-ending), HIGH (funding/credibility killer), Medium (serious problem), Watch (emerging risk)
4. **Route to domain coach:** legal attacks → legal advisor, technical → CTO, monetization → CRO, etc.

**Score severity based on:**
- **Probability of occurrence** (will this happen?)
- **Impact on business** (if it happens, does the business survive?)
- **Discoverability** (how easy is this to find?)

**CRITICAL** = high probability, high impact, high discoverability
**HIGH** = medium probability, high impact, OR high probability, medium impact
**Medium** = medium probability, medium impact
**Watch** = low probability, any impact

---

*Adversarial Red Team — 2026-07-02*