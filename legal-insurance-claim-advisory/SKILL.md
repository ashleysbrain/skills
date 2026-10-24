---
name: legal-insurance-claim-advisory
description: Advisory panel workflow for ANY insurance-related legal matter — personal injury, product liability, workers' comp fraud reporting, insurance fraud claims, anonymous tip filing. Covers insurance type identification, attorney/agency matching, evidence preservation, panel construction, character-limited statement drafting.
category: operations
version: "1.1.0"
---

# Legal Insurance Claim Advisory

## When to Use
User needs strategic advisory for ANY insurance legal matter. Two main branches:

1. **PI / Product Liability Claims** — personal injury claims involving vehicles, ADAS/Autopilot, product defects. Requires distinguishing between first-party (captive) and third-party carriers.
2. **Insurance Fraud Reporting** — filing fraud reports (workers' comp claimant fraud, provider fraud, employer fraud). Includes anonymous filing and character-limited statement drafting. See the dedicated section below.

## Core Workflow

### 1. Identify Insurance Type (CRITICAL FIRST STEP)
- **Tesla Insurance** = captive carrier, same parent as manufacturer
  - Incentive: PROTECT Tesla brand
  - Claims: bad faith focus, duty to defend
- **Progressive/State Farm/Geico/etc.** = third-party carrier
  - Incentive: PURSUE manufacturer via subrogation
  - Claims: product liability + PI, Made Whole Doctrine applies

**Never assume** — confirm the exact carrier from user. Wrong carrier = wrong attorney list = user frustration.

### 2. Match Attorney Type to Claim Structure
| Carrier Type | Primary Need | Secondary Need |
|--------------|--------------|----------------|
| Captive (Tesla Ins) | Insurance bad faith specialist | Product liability co-counsel |
| Third-party (Progressive) | Product liability + PI specialist | Bad faith specialist (if carrier stonewalls) |

### 3. Build Advisory Panel (5 Coaches)
1. **Insurance Claims Strategist** — coverage, bad faith, carrier tactics
2. **Automotive Systems Expert** — ADAS/Autopilot telemetry, sensor logs, failure modes
3. **Subrogation & Recovery Attorney** — manufacturer liability, third-party recovery
4. **Biomechanics & Injury Valuation** — injury causation, future care, pain and suffering
5. **Litigation Risk Analyst** — trial vs settlement, venue, jury dynamics

### 4. Stage Process
- **Stage 1**: Assessment questions (30-40 targeted questions)
- **Stage 2**: Red Team attack vectors (8 common defense strategies)
- **Stage 3**: Synthesis deliverables (strategy spec, expert plan, settlement framework, decision tree)

### 5. Evidence Preservation (TIME-SENSITIVE)
- Tesla data overwrites in 30-90 days — preservation letter URGENT
- Vehicle offline = data still on car
- Crash video, photos, medical records
- NHTSA complaint creates regulatory paper trail

## Key Precedents (as of 2026)
- **Benavides v. Tesla** (S.D. Fla., Aug 2025, upheld Feb 2026): $243M verdict, 33% fault to Tesla for Autopilot design defects
- **State Farm v. Tesla** (Nov 2025): Subrogation case, breach of implied warranties

## Wave Engine Panel Integration
When the user says "tap into the Wave Engine for a legal panel" or "one-off panel for a working session," they mean:
- Spin up an **advisory panel** using the Wave Coaching Engine (Kuramoto-based oscillator model)
- The session is a **working session**, not a final deliverable — focus on actionable answers, not documentation
- **Save session memory as a legal case file** — structured like a legal file (case number, parties, timeline, evidence index, strategy notes), not a general chat log
- Panel output should be immediately useful for the user's next action (attorney call, evidence request, filing deadline)

## Insurance Fraud Reporting (TX and other jurisdictions)

When the user asks to file an insurance fraud report (workers' comp fraud, claimant fraud, provider fraud, employer fraud), this is a DISTINCT workflow from PI/product liability claims.

### Fraud Report Panel (5 coaches)
1. **Legal Claims Strategist** — jurisdictional fraud statutes, reporting requirements
2. **Fraud Investigator** — fraud pattern identification (claimant/provider/employer), what constitutes reportable fraud vs. a dispute
3. **Statement Writer** — character-limited narrative drafting for official forms
4. **Evidence Curator** — documentation types that carry weight, how to reference without exposing identity
5. **Anonymity & OPSEC Advisor** — anonymous email setup, metadata scrubbing, traceback prevention

### Anonymous Reporting (fully legal in most jurisdictions)
- TX TDI explicitly states: "You may remain anonymous" and "All investigations are kept confidential"
- TX Insurance Code protects reporters from libel/slander suits for fraud reports
- Form FR029 (consumer) has an optional "Information About You" section — leave entirely blank for anonymous filing

### Character-Limited Statement Drafting
When the official form has a character-limited narrative field:
- Target 60-70% of the limit on first draft to leave room for revision
- Provide 3 draft variants: (1) comprehensive/detailed, (2) punchy/tight, (3) legal-formatted with jurisdictional buzzwords
- Use legal terms investigators look for: "material misrepresentation," "collecting benefits under false pretenses," "violating medical restrictions"
- Structure: who → when → what they did → how it contradicts their claim → evidence types → evidence contact
- Always verify phone numbers transcribed from audio — speech stutter produces invalid digit counts (e.g., "651-210-210-4713" is 13 digits; likely "651-210-4713")

### Reference
- `references/tx-insurance-fraud-reporting.md` — TX TDI FR029 form structure, submission channels, anonymous reporting protections

## Common User Corrections to Avoid
- Do NOT give general car accident attorneys — give Tesla Autopilot product liability attorneys
- Do NOT assume Tesla Insurance — ask "Which carrier?"
- Do NOT give general PI firms — give firms with Autopilot/ADAS product liability track record
- Do NOT produce verbose plans when the user wants a working session — give direct answers to their questions
- Do NOT save legal sessions as casual notes — use legal case file format (case number, parties, timeline, evidence, strategy)
- Do NOT set tight deadlines in legal documents that the ADHD user cannot reliably meet. Default to "seven (7) days" or "within a reasonable time" for records exchange and similar obligations. Never set 24-72 hour deadlines on the ADHD party — executive dysfunction could cause missed deadlines leading to sanctions or loss of possession. (User correction, 2026-08-01: "I still don't like this 72 hour timeline that still doesn't leave room for any error or mistake.")
- Do NOT produce one document alone when the user asked to "work these synergistically" across multiple documents. Hold both as drafts, gather all edits, build both in one operation, deliver simultaneously. (User correction, 2026-08-01: "This shouldn't even be done. This should only be partially done. You should not have already produced a document. That is lazy, that is generalist work.")

## References
- `references/tx-autopilot-firms.md` — Texas firms with Autopilot experience
- `references/claim-question-template.md` — 38-question intake template
- `references/tx-insurance-fraud-reporting.md` — TX TDI fraud reporting channels, FR029 form structure, anonymous filing protections