# Adversarial Attack Workflow — Step-by-Step

This reference details the exact adversarial attack workflow used in the B2B wrapper strategy session on 2026-07-02. Use this as a template for future adversarial attacks.

## Phase 1: Attack Surface Identification

Load each adversarial advisor's voice patterns and attack framework from their source files:

1. **AI The Adversary** (`adversarial_red_team.md`) — Legal/regulatory attack surface
2. **Ben Thompson** (`ben-thompson.md`) — Competitive intelligence attack surface
3. **Dr. Andrew Ng** (`andrew-ng.md`) — Technical failure mode attack surface
4. **Reed Hastings** (`reed-hastings.md`) — Business model skeptic attack surface
5. **Elad Gil** (`elad-gil.md`) — Market timing attack surface

**Run advisors consecutively, not concurrently.** Each advisor attacks from their specific lens without seeing others' attacks. This prevents consensus bias and surface more independent vulnerabilities.

## Phase 2: Attack Execution

For each advisor, generate attacks following this structure:

```
VULNERABILITY #[n]: [Name]
- Attack vector: [Who attacks and how]
- Legal/business theory: [What law or business principle is violated]
- Factual basis: [What the strategy actually does that creates exposure]
- Harm scenario: [What happens to the user/business if this attack lands]
- Discoverability: [How easily an adversary finds this]
- Severity: [CRITICAL | HIGH | Medium | Watch]
- Routed to: [Which domain coach should address this]
```

**Voice requirements:**
- Adversarial advisors speak cold, clinically, without softening
- No "on the other hand" balancing
- Attack the premise, not the person
- Specific, plausible harm scenarios with numbered steps

## Phase 3: Severity Ranking and Consolidation

After all 5 advisors have attacked, consolidate into one report:

1. **Sort by severity** — CRITICAL first, then HIGH, Medium, Watch
2. **Consolidate duplicates** — if multiple advisors attacked the same vulnerability, merge into one entry with multiple attack vectors
3. **Identify patterns** — look for recurring themes (e.g., "platform control across 4 vulnerabilities")
4. **Count distribution** — how many CRITICAL? how many HIGH?

**Pattern recognition:**
- **3+ CRITICAL vulnerabilities** = strategy needs fundamental redesign
- **1-2 CRITICAL** = may be salvageable with specific fixes
- **0 CRITICAL but 3+ HIGH** = serious but survivable
- **Only Medium/Watch** = proceed with caution

## Phase 4: The Strategic Question

Every adversarial report MUST end with:

> *"If [platform/competitor/regulator] does [adversarial action], and VCs say [competitive response] — what's our business?"*

Example from B2B wrapper session:
> *"If Atlassian blocks our API access, launches native scoring, and VCs say 'they'll just copy you' — what's your business?"*

If the answer is "we'd be screwed," the strategy needs fundamental redesign.

## Phase 5: Remediation Prioritization

Create a prioritization table:

| Priority | Vulnerability | What to Fix | Who Owns Fix |
|----------|--------------|-------------|--------------|
| **P0** | #1 Platform API resistance | Switch from API integration to user-side processing (browser extension, local data export) | Andrew Ng (CTO) |
| **P0** | #2 Zero moat | Build data moat: longitudinal user data, personalization, multi-platform correlation | Satya Nadella (principal) |
| **P0** | #3 Monetization failure | Pivot from platform-paid to user-paid (direct subscription) or enterprise consulting | Madhavan Ramanujam (CRO) |
| **P1** | #4 Architecture collapse | Design hybrid architecture: core scoring (multi-tenant) + customer-specific adapters (per-customer) | Andrew Ng + Will Larson (CTO) |
| **P1** | #5 Legal exposure | Run peer-reviewed validation study BEFORE any claims; disclose methodology clearly | Teresa Torres (Product) |
| **P1** | #6 Market timing | Reposition: Not "AI wrapper" but "personal wellness intelligence layer" across platforms | Elad Gil (CRO) |

**P0 = CRITICAL vulnerabilities.** If you cannot address ALL P0s, stop and redesign. Do not proceed with only P1 fixes.

## Phase 6: Post-Adversarial Iteration Plan

Generate a handoff document that:

1. Summarizes adversarial findings (not raw output, synthesized)
2. Answers the strategic question or admits defeat
3. Identifies what must be fixed before strategy board can proceed
4. Offers the user: run strategy board NOW, discuss adversarial findings first, or something else

**User options presented in B2B wrapper session:**
- Option A: Run Strategy Board NOW (advisors propose fixes to adversarial vulnerabilities)
- Option B: Discuss Adversarial Findings First (walk through each vulnerability before bringing in board)
- Option C: Something Else (user's choice)

## Phase 7: Strategy Board Review (NOT in this skill)

Strategy board receives adversarial findings and proposes fixes. Then:

```
[REVISED STRATEGY]
    ↓
[SECOND ADVERSARIAL ATTACK] ← Stress-test the fixes
    ↓
[FINAL STRATEGY] ← Survives adversarial review
    ↓
[EXECUTION]
```

## Timing

Typical adversarial attack session: **30-45 minutes**

- Phase 1 (load advisors): 5 minutes
- Phase 2 (attack execution): 20-25 minutes
- Phase 3 (consolidation): 5-10 minutes
- Phase 4-6 (prioritization + handoff): 5-10 minutes

**Second adversarial attack** (after strategy board proposes fixes): 15-20 minutes

## Files Generated

In B2B wrapper session, adversarial attack generated:

1. `/tmp/adversarial-attack-report-001.md` — Raw adversarial output (11.7K bytes)
2. `/tmp/adversarial-attack-report-001.pdf` — PDF deliverable (92K bytes)
3. `/tmp/post-adversarial-iteration-plan.md` — Handoff document (4.8K bytes)
4. `/tmp/b2b-wrapper-strategy-panel-brief.md` — Updated panel brief with adversarial layer (updated via patch)

All files timestamped, versioned (001, 002, etc.) for iteration tracking.

## Common Pitfalls

- **Do NOT soften adversarial findings.** If something is CRITICAL, call it CRITICAL. Don't downgrade to make it palatable.
- **Do NOT let adversarial advisors propose solutions.** Their job is to find holes. Remediation is the strategy board's job.
- **Do NOT run advisors concurrently.** Run consecutively to preserve independence and avoid consensus bias.
- **Do NOT skip the second adversarial attack.** The strategy board's fixes must survive adversarial review too.
- **Do NOT route vulnerabilities to the wrong domain coaches.** Legal → legal advisor, technical → CTO, monetization → CRO, etc.
- **Do NOT proceed with strategy board if 3+ CRITICAL vulnerabilities are found.** First address P0s or redesign.

---

*Adversarial Red Team — 2026-07-02*