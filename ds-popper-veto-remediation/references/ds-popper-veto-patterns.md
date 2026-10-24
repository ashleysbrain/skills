# the specialist engine VETO Patterns & Remediation Templates

Catalog of VETO categories observed in the specialist engine reviews, with standard remediation templates for the specialist engine.

## VETO Category 1: Zero Empirical Evidence for Claimed Effects

**Typical language**: "The document contains no citations, validation studies, effect sizes, or references to peer-reviewed research supporting the claimed effects for the specific protocols as described."

**Remediation**: Add **Evidence Base Table** with columns:
- Protocol / Effect
- Evidence Level (Strong / Moderate / Low / Emerging)
- Key References (APA style: Author (Year) *Journal*)

**Evidence Level Definitions**:
- **Strong**: Multiple RCTs + meta-analyses supporting the *general technique*
- **Moderate**: Some RCTs + mechanistic studies supporting the *general technique*
- **Low**: Pilot studies, case series, theoretical rationale only
- **Emerging**: Very recent, limited replication, preprint or popularization-driven

**Critical Note**: Always add a footnote: "Evidence supports the *general technique*, not the *specific biometric-triggered implementation* in this document. This remains a gap for scientific use."

---

## VETO Category 2: Undisclosed Conflict of Interest

**Typical language**: "The document does not disclose any financial, institutional, or proprietary ties between the protocol authors and [Commercial Entity]."

**Remediation**: Add **COI Disclosure Block** at document header (after title, before content):

```markdown
> **⚠️ Conflict of Interest Disclosure**: These [protocols/methods/analyses] are derived from [Source]'s [repertoire/approach] (commercial [product/service], [package/repo identifier]). The authors have not received independent validation funding. No financial compensation was received from [Source] for this document. Users should be aware of the proprietary origin when evaluating claimed effects.
```

Customize for the specific source (NeuroLoop, specific vendor, etc.).

---

## VETO Category 3: Insufficient Ethical Safeguards

**Typical language**: "No IRB/ethics committee approval mentioned. No risk-benefit analysis for general use. No safety monitoring or adverse event reporting procedures. No data privacy guidance for biometric signals."

**Remediation**: Add **Ethical Safeguards Block** at document header (after COI disclosure):

```markdown
> **⚠️ Ethical Safeguards**: No IRB/ethics committee approval has been obtained for this [protocol set/analysis/document]. No formal risk-benefit analysis, safety monitoring, or adverse event reporting procedures exist. [Biometric data types] should be treated as sensitive health data. Users must provide informed consent before [data collection]. Data privacy: signals should not be stored, transmitted, or shared without explicit user consent per applicable regulations (HIPAA, GDPR, etc.).
```

Add protocol-specific contraindications inline where they exist (e.g., Wim Hof for epilepsy_risk).

---

## VETO Category 4: Undefined Operational Definitions

**Typical language**: "Trigger thresholds lack operational definitions: How is 'Focus' measured? What device/signal processing pipeline is assumed? No standardization... no calibration or quality-check steps included."

**Remediation**: Add **Operational Definitions Table** with columns:
| Signal | Operational Definition | Measurement Standard |

**Standard measurement fields to specify**:
- Electrode montage / sensor placement
- Sampling rate
- Bandpass filter ranges
- Artifact rejection thresholds
- Baseline duration and conditions
- Reference citations for computation methods (e.g., "Modulation index (Tort et al. 2010)")

**For signals NOT measured by current pipeline**: Add a row with "NOT measured by current pipeline" in Measurement Standard and a note: "Retained for protocol completeness but cannot be triggered. Implementing requires additional validated sensors."

---

## VETO Category 5: Reproducibility Gaps

**Typical language**: "No version control or protocol ID: Users cannot track which exact protocol version they followed."

**Remediation**: Add **Protocol Version & Change Log** table:
| Version | Date | Changes | Author |

Always include the remediation as a version bump with author = "the specialist engine (Bernard Engine) — post-the specialist engine veto remediation".

---

## VETO Outcome Patterns

### Pattern A: Absolute VETO (Research/Clinical)
**Language**: "I **VETO** this document's use in any research, clinical, or validation context until..."
**Remediation**: Full structural fixes (all 5 categories). VETO notice **retained** in document. Version bump.

### Pattern B: Conditional VETO (Wellness/Educational)
**Language**: "If used strictly for non-clinical, self-guided well-being suggestions (with clear disclaimers)... it may pose lower risk."
**Remediation**: Full structural fixes + Medical Disclaimer block. VETO notice **retained but narrowed** ("VETOED for research/clinical use; suitable for wellness with disclaimers"). Version bump.

---

## VETO Category 6: Dead Code in Production Formulas

**Typical language**: "The TWC formula stores `coupling_sum = 6.775` across ALL scored days — it is a constant, never varies, never enters the actual TWC computation."

**Root cause**: A formula component was coded as a hardcoded constant rather than being computed from live data. It appears in the database and documentation as if active, but has no mathematical effect.

**Remediation**: Either (a) implement the computation so the value varies with actual cross-dimensional state, or (b) formally remove it from the documented formula and stop claiming it as a feature. **Do NOT leave it as a decorative metadata field** — this creates a false impression that the formula is more complex than its actual implementation.

**Remediation check**: Run the diagnostic query from `recurring-cycle-audit-methodology.md` (coupling_sum constancy check). If `COUNT(DISTINCT coupling_sum) > 1`, the fix is confirmed.

**Integrity note**: If the dead code is retained without fix for 5+ audit cycles, this constitutes a persistent process failure. The VETO should escalate and the finding should be flagged to the research director as a process breakdown.

---

## VETO Category 7: Placeholder Values Masquerading as Scientifically-Derived Coefficients

**Typical language**: "The interaction_matrix values are approximately 70-75% lower than specification values. The highest value in the matrix is 0.35; the spec says the strongest coupling should be 0.85."

**Root cause**: A database table intended to hold scientifically-derived proprietary coefficients was populated with default/placeholder values during development and never updated.

**Remediation**: Either (a) update the DB values to match the scientifically-derived specification, or (b) acknowledge the spec values are aspirational and the current values are empirical defaults pending validation. **Either path must be documented** — a 4+ cycle contradiction between spec and implementation is unacceptable.

**Integrity note**: Any publication, investor deck, or external claim citing the interaction matrix as a methodological innovation is VETOED while placeholder values are in production. The feature as implemented does not match the feature as documented.

---

## the specialist engine Job Details

- **Job ID**: `bb2fc380f91d`
- **Schedule**: Every 4 hours (was hourly, reduced after audit)
- **Output Dir**: `<agent-home>/cron/output/bb2fc380f91d/`
- **Model**: `deepseek/deepseek-r1:free` (rigorous reasoning model)
- **Workdir**: Varies per review (e.g., `ds-wave-research-execution-final` workspace)
- **Prompt**: Standing orders to review the specialist engine, Pearl, Simon, Asimov outputs; apply falsifiability, bias checklists, CONSORT/STROBE/PRISMA/TRIPOD; statistical audit, code review, FAIR compliance

---

## Quick Reference: VETO → Fix Checklist

When a new VETO arrives:

- [ ] Parse VETO: document path, fatal flaw list, remediation requirements
- [ ] Read target document
- [ ] For each fatal flaw, apply corresponding remediation pattern
- [ ] Add COI Disclosure block
- [ ] Add Medical Disclaimer block
- [ ] Add Ethical Safeguards block
- [ ] Add Operational Definitions table (all signals)
- [ ] Add Evidence Base table (all claimed effects)
- [ ] Add Protocol Version & Change Log
- [ ] Bump version number
- [ ] Re-run the specialist engine cron to verify
- [ ] Log SOAP note in `ds-clinical-engine/rounds/`