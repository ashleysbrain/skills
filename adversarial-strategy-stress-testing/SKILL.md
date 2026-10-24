---
name: adversarial-strategy-stress-testing
description: For any business strategy, platform integration, or GTM plan, ALWAYS run adversarial red team BEFORE strategy board. Never build on fragile assumptions. The adversarial layer is non-negotiable for high-stakes strategic work.
version: 1.0
---

# Adversarial Strategy Stress Testing

Use this BEFORE running any strategic advisory board session for business strategy, platform integration, go-to-market plans, partnership strategy, or monetization models. The adversarial red team systematically breaks apart the strategy to find business-ending vulnerabilities before the strategy board builds on fragile assumptions.

## When to use

**MANDATORY for:**
- B2B platform wrapper strategies (Jira, Linear, Obsidian integrations)
- Go-to-market plans that depend on third-party partnerships
- Monetization models that rely on platform cooperation
- Partnership or alliance strategies
- Market entry strategies for competitive spaces
- ANY strategy where a single point of failure could destroy the business

**NOT needed for:**
- Tactical execution decisions (already validated)
- Operational process improvements (low-risk)
- Incremental feature additions to existing products
- Technical refactoring (no business model impact)

## Core principle

> **"If we don't find the weakness first, someone else will — and they won't be trying to help us fix it."**

The adversarial red team assumes the role of regulators, plaintiffs' attorneys, competitors, VCs, and customers who will attack the strategy. Every assumption is questioned. Every premise is stress-tested.

## Adversarial Red Team Composition (5 seats)

| Seat | Role | Attack Lens | Source Board |
|------|------|-------------|--------------|
| **AI The Adversary** | Legal/Regulatory Red Team | Finds every liability exposure FTC, FDA, state AGs, and plaintiffs' attorneys will exploit | Legal Advisory Board |
| **Ben Thompson** | Competitive Threat | Shows how incumbents will crush us with better positioning or faster execution | Research Advisory Board |
| **Dr. Andrew Ng (Attack Mode)** | Technical Failure Mode Engineer | Shows where the architecture breaks: multi-tenant scaling, per-customer data isolation, API rate limits, hot-deployment | CTO Advisory Board |
| **Reed Hastings** | Business Model Skeptic | Attacks the monetization model: why would customers/platforms pay? Why won't they just copy? What's the moat? | principal Advisory Board |
| **Elad Gil** | Market Timing Reality Check | Shows why this is the wrong market: timing, saturation, competing narratives, investor fatigue | CRO Advisory Board |

All 5 advisors exist in the specialist engine advisory board system. No new codenames needed.

## Attack Surface Audit

The adversarial team systematically reviews six attack vectors:

### 1. Platform Resistance Attack
**Questions:**
- Why would the platform let us wrap their product?
- What if they block APIs or change terms of service?
- What if they build the feature themselves?
- What if they demand 20-30% revenue share for partner access?

**Examples:**
- Atlassian blocking Jira API access
- Notion launching native AI scoring
- Linear announcing proprietary prioritization engine

### 2. Monetization Attack
**Questions:**
- Why would customers pay for this?
- What if they ask for free?
- What if competitors undercut?
- What if platforms pass costs to users and users revolt?

**Examples:**
- Enterprise procurement cycles (12-18 months)
- Security teams blocking external API access
- CFOs questioning why pay external vs build internal
- Users revolt on platform fees

### 3. Architecture Attack
**Questions:**
- What if we can't scale to 10 platforms?
- What if per-customer deployment costs kill margins?
- What if API changes break everything?
- What if hot-deployment fails?

**Examples:**
- Enterprise customers demanding dedicated instances ($10K/month infrastructure)
- API rate limits (Jira: 1000 requests/hour)
- Linear v2 API deprecation breaking 50+ integrations
- Multi-tenant vs per-customer tradeoffs

### 4. Legal/Regulatory Attack
**Questions:**
- What if FTC claims false advertising for scoring claims?
- What if GDPR blocks EU deployment?
- What if platforms claim IP infringement?
- What if state AGs investigate data practices?

**Examples:**
- Unsubstantiated "physics-informed scoring" claims
- FTC demanding peer-reviewed validation studies
- Data residency requirements for enterprise customers
- Platform IP claims on scoring algorithms

### 5. Market Timing Attack
**Questions:**
- Is this too late? Too early?
- Is the market saturated?
- Are VCs burned on similar strategies?
- What competing narratives exist?

**Examples:**
- "AI wrappers" narrative peaked in 2024, VCs burned
- Incumbents launching native AI features
- VC fatigue on "wrapper" companies
- Market saturation in integration services

### 6. Incumbent Response Attack
**Questions:**
- What if the platform launches a competitive feature next week?
- How do we respond?
- What if they hire a better team than us?
- What if they have more data?

**Examples:**
- Atlassian launching "Jira Intelligence" with task scoring
- Notion launching "Notion AI" with prioritization
- Linear announcing "Linear Goals" with scoring

### 7. AI-Native Timeline Attack (CRITICAL — User Correction 2026-07-02)
**Questions:**
- Is this a 12-month human waterfall timeline or an AI-native timeline?
- AI development moves 5-10x faster (Autogen, Devin, Claude Code, Copilot) — does the timeline reflect this?
- Competitors with AI-native execution can launch in 3 months and iterate 4x before we ship — is this accounted for?
- Is "study then ship" (Month 6 study, Month 7 ship) a waterfall approach that delays launch?
- Can AI agents code adapters, run studies, and iterate concurrently instead of sequentially?

**Examples:**
- 12-month human timeline while competitor launches in 3 months
- Waterfall study-then-ship approach (Month 6 study → Month 7 ship) while competitor ships Month 3
- Sequential development (Q1 foundation → Q2 study → Q3 scale → Q4 enterprise) while competitor uses concurrent AI-native development

**Harm scenario:**
- DS starts 12-month human timeline
- Competitor (AI-native team of 3 people) launches in Month 3
- Competitor iterates 4x before DS ships
- DS launches Month 12 into saturated market
- VCs pass: "You're 9 months late. We're backing the faster team."

**Severity:** CRITICAL — Being slow in AI era is fatal

**Routed to:** Will Larson (CTO) for AI-native execution redesign

## Adversarial Output Format

For each vulnerability, the adversarial team delivers:

```
VULNERABILITY #N: [Name]
- Attack vector: [Who attacks and how]
- Legal/business theory: [What law or business principle is violated]
- Factual basis: [What the strategy actually does that creates exposure]
- Harm scenario: [What happens to the business if this attack lands]
- Discoverability: [How easily an adversary finds this]
- Severity: [CRITICAL | HIGH | Medium | Watch]
- Routed to: [Which domain coach should address this]
```

## Adversarial Workflow

1. **Attack first** — Adversarial team runs BEFORE strategy board
2. **Every assumption questioned** — No premise is safe
3. **No solutions offered** — The adversarial team finds holes, not fixes
4. **Severity-ranked vulnerabilities** — Critical attacks get priority attention
5. **Domain coach remediation** — Each vulnerability routed to relevant strategy advisor for fix

## Post-Adversarial Iteration Loop (Full Dialectic)

When the user explicitly requests "multiple iterations of reviews from writing panel to adversarial panel and back again until everyone agrees, then send another different model through it," use the full dialectic loop:

```
[ORIGINAL STRATEGY / DOCUMENT]
    ↓
[ROUND 1 ADVERSARIAL] ← 4+ seats attack from different vectors
    ↓
[SYNTHESIZE] ← Consolidate all findings into attack report
    ↓
[ROUND 2 WRITING PANEL] ← Each seat owns a cluster of findings, produces revisions
    ↓
[ROUND 2 ADVERSARIAL] ← Same seats re-attack, check RESOLVED / PARTIALLY / STILL OPEN
    ↓
[CONVERGENCE CHECK] ← New critical design failures → Round 3. Only execution failures → integrate.
    ↓
[ROUND 3 INTEGRATION] ← Build clean master document, resolve contradictions
    ↓
[CROSS-MODEL REVIEW] ← Different model, blind, no context about panels
    ↓
[FINAL STRATEGY] ← Survives full dialectic
    ↓
[EXECUTION]
```

### Convergence criteria
The loop stops when:
1. Adversarial panel cannot find NEW critical DESIGN failures
2. All remaining issues are EXECUTION failures (revisions not applied to master doc)
3. Recurring issues are acknowledged tradeoffs, not unresolved failures

### Cross-model review
Dispatch final version to a different model entirely (DeepSeek, Gemini, Grok). Model gets it blind. If multi-model infrastructure (MoA, external delegates) is credits-blocked, use `web_search` competitive intelligence + structural assessment as fallback.

### The #1 process failure
Writing panel produces revisions as SEPARATE DOCUMENTS that never get integrated into the master. All adversarial seats will independently find this. Fix: rebuild the master document from scratch in Round 3, do NOT patch line-by-line.

## The Single Question

Every adversarial report must end with the strategic question:

> *"If [platform/competitor/regulator] does [adversarial action], and VCs say [competitive response] — what's our business?"*

If the answer is "we'd be screwed," the strategy needs fundamental redesign.

## Relationship to multi-agent-panel-blueprinting

This skill is the adversarial **pre-requisite** to multi-agent-panel-blueprinting. The workflow is:

1. **This skill** — adversarial attack on the strategy
2. **multi-agent-panel-blueprinting** — design the strategy advisory board
3. Run the strategy board — advisors propose fixes to adversarial vulnerabilities
4. Second adversarial attack — stress-test the proposed fixes
5. Final strategy approval

## The Funding/Structure Gauntlet (5-Round Sequential Pattern, validated 2026-08-15)

For plans where the deliverable is a DECISION + EXECUTION ROADMAP (funding strategy, company structure, GTM sequencing), run a five-round gauntlet instead of a single panel attack. Each round = ONE named elite brain, dispatched SEQUENTIALLY (never parallel — principal correction 2026-08-15: "Not in parallel"), each attacking the SURVIVING plan from the previous round, each gated on landing (brain-integrity check):

1. **Falsification (Popper-mode, she):** kill-level gaps ranked by lethality. Verdict: survives / does not survive / survives with structural changes.
2. **Calibration (Tetlock-mode):** probabilities on every instrument (p × size × speed-to-cash), honest CIs, calibrated replacements for certainty claims ("will REQUIRE" → p-stated / conditional / base-rate-with-falsifier), kill-shot indicator with a falsification window and a pre-planned pivot.
3. **First-principles deletion (Musk-mode):** delete ceremony (registrations before needed, cap tables with no equity event, data rooms with no counterparty, outbound LOIs faking inbound). Derive structure from constraints, not options menus. Replace structure debates with trigger-events.
4. **Money-side reality (Program-Officer composite):** ACCEPT / MODIFY / REJECT per line item against how funders actually triage. Eligibility kills (UK-only funds for a US lab, 501c3 sponsors that cannot hold SBIR) surface HERE, not at submission.
5. **Decision layer (Kozyrkov-mode):** portfolio cut by EV-per-principal-hour (park the only resumable lane, don't kill it), principal-only irreversibles vs delegables, pre-commitments locked while calm (tie-breaks, auto-park rules, client cutoffs), weekly ≤15-min hour-gate ("deliverables lie; calendars don't").

Then ONE consolidation brain fuses surviving rounds into an executable build doc: decided structure, week-by-week roadmap with microsteps + brain assignments + principal hours caps, binding operating rules, and a 5-line emergency card.

**Discipline rules:** the principal reads nothing until all rounds land ("I'm not even reading this until we go through this a couple of times"); every round gated; every forward claim carries a number, a conditional, or a falsifier; more rounds on demand ("There should be more adversarial rounds") — the gauntlet extends, it doesn't shortcut.

## New-input evaluation: the two-brain pattern (validated 2026-08-16, LittleLearner session)

When a NEW external model/tech/tool enters mid-plan ("can we use it? what for? how?"), do NOT run a generalist assessment or a single-brain review. Run two brains SEQUENTIALLY with deliberately opposite postures, then consolidate:

1. **Technical-legs brain first (Karpathy-mode):** empiricist's judgment. Sanity-check the design (where's the catch — data leakage, boundary fuzz, scale limits?). Spec the ONE experiment if it were used (data, measurement, baseline, expected figure, cost in days). Name the hard preconditions and the explicit NO conditions. Read the actual source of what would consume it BEFORE judging (in the LittleLearner case he read the scoring engine's code to check whether it consumes weights or telemetry — that single fact drove every downstream ruling).
2. **Falsification brain second (Popper-mode, she):** attacks the PREMISE, not the tech. The binding-constraint reframe: the right question is never "can we use it?" but **"what does this displace, and does it out-earn it?"** Kill vectors: construct validity (does the instrument fit the substrate, or is it "an ECG on a rock"), statistical emptiness (an N=2 ablation proves nothing a reviewer won't puncture), frame capture (our method becomes a dependent variable of their methodology), bandwidth theft (which milestone's principal-hour this steals), legibility (does this make the lab clearer or muddier to funders).
3. **Consolidate with disjunctive re-entry conditions.** When the brains split (use-it-later vs park-it-now): park-now wins on timing while pre-money; BANK the experiment spec so re-entry costs zero design time; define re-entry as EITHER demand-pull (a qualified inbound asks for it) OR a scheduled slot opening (post-milestone). Allow exactly one free touch (a related-work citation) if it plants a flag in the relevant community.

This pattern caught a seductive distraction before it cost a milestone. The consolidated LittleLearner ruling: parked, spec banked, citation allowed, re-entry defined — and the plan's own park rule (from the gauntlet's round 5) did exactly what it was designed to do.

## Pitfalls

- **CRITICAL: Never run strategy board BEFORE adversarial attack.** Building strategy on fragile assumptions wastes everyone's time.
- **CRITICAL: Never use human waterfall timelines for AI-native strategies.** 12-month human timelines are fatal in AI era where competitors launch in 3 months. AI development moves 5-10x faster. Always stress-test whether timeline reflects AI-native execution velocity or human waterfall assumptions.
- Do not skip the second adversarial attack. The strategy board's fixes must survive adversarial review too.
- Do not route adversarial findings to the wrong domain coaches. Legal attacks → legal advisor, technical attacks → CTO, etc.
- Do not let the adversarial team propose solutions. Their job is to find holes. Remediation is the strategy board's job.
- Do not let adversarial findings be "softened" or "balanced." The adversarial role is to show the worst-case scenario in specific, plausible detail.

## References

- `references/adversarial-attack-framework.md` — detailed six-vector attack framework with checklists and vulnerability indicators
- `references/adversarial-critical-vulnerabilities.md` — business-ending vulnerabilities from B2B wrapper strategy case study (2026-07-02)
- `references/adversarial-iteration-workflow.md` — step-by-step adversarial attack workflow with timing, file generation, and handoff process
- `references/new-input-two-brain-evaluation.md` — worked LittleLearner case for the two-brain new-input pattern: OCR extraction pipeline, both dispatch verdicts, the consolidated park/bank/re-entry ruling

## Session Archive

- **2026-07-02 — B2B Platform Wrapper Strategy (First Adversarial Attack):** Found 6 vulnerabilities (3 CRITICAL, 3 HIGH). Original strategy fundamentally flawed. Critical vulnerabilities: platform API resistance, zero moat, monetization failure. Strategy board review pending to propose fixes. See `references/adversarial-critical-vulnerabilities.md` for full case study.

- **2026-07-02 — B2B Platform Wrapper Strategy (Second Adversarial Attack on REVISED Strategy):** Found 5 NEW vulnerabilities (2 CRITICAL, 3 HIGH) in the revised strategy. Original 6 vulnerabilities were FIXED by strategy board, but fixes created new vulnerabilities. Critical NEW vulnerabilities: AI-native timeline failure (12-month human timeline), data moat illusion (browser extensions collect same data). High NEW vulnerabilities: pricing delusion (20% conversion fantasy), study design flaw (underpowered study), Obsidian platform trap (too niche for scale). See `references/adversarial-critical-vulnerabilities.md` for full case study and iteration pattern.

## Success criteria

- All six attack vectors are systematically reviewed
- Vulnerabilities are severity-ranked (CRITICAL/HIGH/Medium/Watch)
- Each vulnerability has a specific remediation path routed to correct domain coach
- The single strategic question is answered or the strategy is redesigned
- No strategy proceeds to board review without adversarial clearance

---