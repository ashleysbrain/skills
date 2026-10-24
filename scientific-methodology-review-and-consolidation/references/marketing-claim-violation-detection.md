# Marketing Claim Violation Detection — Detection Recipes with Worked Examples

Reference for Check 9 of the ML/AI Claim Validation quality gate in the parent SKILL.md.
Captures reusable detection patterns from the the specialist engine marketing sprint audit (2026-06-13).

---

## Detection Recipe 9: Marketing Gate Bypass

### The Pattern

While methodology flaws persist unfixed (0% fix rate across audit cycles), the organism produces marketing materials that package those exact flaws as selling points. The quality gate traditionally covers manuscripts, protocols, and code — but marketing materials bypass the gate entirely unless explicitly scanned.

### How to Detect

1. **Scan for new external-facing documents** since the last audit cycle:
   ```bash
   find ~/your-workspace -maxdepth 6 -type f -newermt "<LAST_CYCLE_TIME>" \
     \( -name "*one-pager*" -o -name "*positioning*" -o -name "*social-media*" \
        -o -name "*marketing*" -o -name "*brief*" -o -name "*investor*" \
        -o -name "*deck*" -o -name "*branding*" \) | grep -viE "node_modules|\.git/"
   ```

2. **Extract every factual claim** from each document. A factual claim is any sentence containing:
   - Quantitative performance claims ("4-12x improvement")
   - Capability claims ("cannot suggest impossible outcomes")
   - Technical-naming claims ("Langevin stochastic equations")
   - Precision claims ("exactly how each one pulls on the others")
   - IP/proprietary claims ("The physics equations are proprietary")

3. **Map each claim to applicable checks:**

   | Claim Type | Applicable Check |
   |-----------|-----------------|
   | Performance improvement ratio | Check 2 (cherry-picked metrics) + Check 1 (circularity) |
   | "Cannot hallucinate/impossible" | Check 8 (bounded ≠ safe) |
   | Named technique (Langevin, Landau-Ginzburg) | Check 3 (marketing-vs-code) |
   | "We were doing X before it had a name" | Check 4 (HARKing) |
   | "Measured in our prototype" | Check 1 (circular benchmarking) |
   | Coupling matrix precision claims | Check 8 / interaction matrix audit |
   | "Proprietary equations/IP" | N=1 calibration cross-check |

4. **Build the violation catalog:**
   ```
   document_path:line_number | claim_text | violated_check | evidence_from_audit_register
   ```

5. **Check for "no hedging" voice instructions:**
   Search for instructions that explicitly remove scientific uncertainty language:
   ```bash
   grep -i "no hedging\|no 'we believe'\|say what the science does\|no 'studies suggest'" <marketing_docs>
   ```
   These compound every other violation — they instruct removing the very language that would honestly qualify unvalidated claims.

### Worked Example: the specialist engine Sprint (2026-06-13, 17:38 Cycle)

**Documents audited:**
- `DIVINITY-SCIENCE-ONE-PAGER.md` (investor/partner/press, 4,869 bytes)
- `VANITY-SCIENCE-POSITIONING.md` (brand strategy, 9,251 bytes)
- `SOCIAL-MEDIA-CALENDAR.md` (4-week Twitter/LinkedIn schedule, 29,173 bytes)

**12 violations catalogued** across these documents. Key entries:

| # | Doc & Line | Claim | Check | Evidence |
|---|-----------|-------|-------|----------|
| 9a | ONE-PAGER L32 | "cannot suggest impossible outcomes because physics will not let it" | Check 8 | Scalar scores bounded [0,100]; LLM text unconstrained. Regulatory liability. |
| 9b | ONE-PAGER L33 | "4 to 12 times better predictions" | Check 2 | Primary metric: 1.06x (6%). Range picks only two extrapolation endpoints from circular data. |
| 9c | ONE-PAGER L32 | "coupling matrices that map how dimensions influence each other" | Finding 8 | Coupling_sum = constant 6.775 (dead). Interaction matrix max = 0.35 vs spec 0.85. Never functioned. |
| 9d | ONE-PAGER L32 | "Langevin stochastic equations. Landau-Ginzburg phase transition models" | Check 3 | Terms in API docstrings only, not computation code. PIML prototype does not implement them. |
| 9e | ONE-PAGER L42 | "recently discovered the academic term... PIML" | Check 4 | Framework labeled retroactively (HARKing). |
| 9f | ONE-PAGER L34 | "Not theoretical. Measured in our prototype." | Check 1 | Prototype tested against self-generated data (circular). |
| 9g | ONE-PAGER L62 | "The coupling matrix defines exactly how each one pulls on the others" | Finding 8 | Placeholder values 63-81% off spec. "Exactly" is false precision for broken code. |
| 9h | ONE-PAGER L68 | "The physics equations are proprietary... the specialist engine IP" | N=1 | Coefficients from single-individual calibration. No population derivation. |
| 9i | VANITY L60 | "shows you the coupling matrix... exactly how your sleep coefficient pulls" | Finding 8 | Cannot show "exactly" with placeholder coefficients and dead coupling_sum. |
| 9j | VANITY L91 | "No hedging. No 'we believe'... Say what the science does." | Falsifiability | Explicitly removes scientific hedging from unvalidated claims. |
| 9k | VANITY L157 | "we were doing PIML before it had a name" | Check 4 | Historical revisionism — retroactive framing. |
| 9l | SOCIAL L34, L52 | "I built the math to map it. One coupled system." | Finding 8 | Math is broken — coupling is decorative metadata. |

### Regulatory Risk Assessment

Claims that "the system cannot suggest impossible outcomes" or "cannot hallucinate" in health/wellness contexts imply clinical reliability. Under FDA scrutiny, such claims could:
1. Trigger medical device classification (contradicting wellness-coaching regulatory posture)
2. Create a false sense of safety that discourages appropriate clinical consultation
3. Expose the company to liability if the system (LLM text) produces harmful advice

**Always flag** "cannot X" claims in health/wellness marketing as regulatory risk, regardless of the underlying scoring engine's properties.

### The "No Hedging" Problem

Marketing voice guides that instruct removing scientific uncertainty language are not neutral brand decisions — they are methodology violations. For unvalidated claims, hedging IS the scientifically correct posture.

An instruction like "No hedging. No 'we believe' or 'studies suggest.' Say what the science does." applied to claims that haven't been validated:
- Removes the very qualifiers that make the claims honest
- Creates a systematic overclaim bias across all content produced under that voice guide
- Should itself be flagged as a finding, not just the claims it generates

### Remediation Protocol

1. **Categorical hold:** Issue a VETO on the entire marketing document set until remediated
2. **Claim-by-claim triage:** For each violation, either (a) substantiate with evidence, (b) remove, or (c) hedge with documented limitations
3. **Voice guide revision:** Remove "no hedging" instructions; replace with "hedge unvalidated claims honestly; assert validated claims directly"
4. **Gate integration:** All future marketing materials must pass through the quality gate before external release
5. **Pre-registration check:** Verify that marketing claims are not more specific than what was pre-registered

### Key Files for Marketing Claim Audits

- Investor one-pagers: `~/your-workspace/marketing-sprint/`
- Brand positioning: `~/your-workspace/ds-wave-cto-advisory-panel-private/PIML-MARKETING-BRANDING-BRIEF.md`
- Codebase for cross-reference: `~/your-workspace/ds-wave-coaching-engine/src/`, `~/your-workspace/divinity-health/piml-prototype/`
- Audit findings register: Previous cycle output in `<agent-home>/cron/output/bb2fc380f91d/`
