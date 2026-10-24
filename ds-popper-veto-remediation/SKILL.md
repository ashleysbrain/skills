---
name: ds-popper-veto-remediation
description: Systematic workflow for addressing the specialist engine's methodological VETOs by having the specialist engine (Bernard Engine) fix the fatal gaps in research protocols, documents, and agent outputs before publication.
category: operations
---

# the specialist engine VETO Remediation Workflow

When the specialist engine (Karl Popper) applies a **VETO** to a document, protocol, or agent output for fatal methodological flaws, this workflow governs how the specialist engine (Bernard Engine / Clinical/Homeostasis) remediates the gaps so the document can pass quality gates.

## Trigger Conditions

- the specialist engine cron job (`bb2fc380f91d`) produces a VETO report with "FATAL METHODOLOGICAL FLAWS IDENTIFIED"
- VETO cites specific gap categories: zero empirical evidence, undisclosed COI, insufficient ethical safeguards, undefined operational definitions, reproducibility gaps
- Document is in a state where it blocks downstream work (e.g., research protocols needed for writing, agent configs needed for deployment)

## Workflow

### Phase 1: Parse the VETO
Read the latest the specialist engine output from `<agent-home>/cron/output/bb2fc380f91d/` (most recent `.md` file). Extract:
- Document/path under review
- Numbered list of fatal flaws
- Specific remediation requirements per flaw
- Whether VETO is absolute (research/clinical use) or conditional (wellness/educational with disclaimers)

### Phase 2: Locate and Read Target Document
Find the document path cited in the VETO. Read it fully to understand current structure and content.

### Phase 3: Systematic Gap Remediation
For **each fatal flaw**, apply the corresponding fix pattern:

| Fatal Flaw Category | Remediation Pattern |
|---------------------|---------------------|
| **Zero empirical evidence** | Add **Evidence Base table** mapping each claimed effect to peer-reviewed references with evidence levels (Strong/Moderate/Low/Emerging). Note where evidence supports *general technique* but not *specific triggered implementation*. |
| **Undisclosed conflict of interest** | Add **COI Disclosure block** at document header: proprietary source, commercial affiliations, funding status, compensation disclosures. |
| **Insufficient ethical safeguards** | Add **Ethical Safeguards block**: IRB status, risk-benefit analysis, safety monitoring, adverse event procedures, data privacy (HIPAA/GDPR), consent requirements. Acknowledge gaps honestly. |
| **Undefined operational definitions** | Add **Operational Definitions table** for all measured signals: signal name, computational definition, measurement standard (electrode montage, sampling rate, artifact rejection, baseline duration, reference citations). Mark signals not measured by current pipeline. |
| **Reproducibility gaps** | Add **Protocol Version & Change Log** table. Version bump with date, changes, author (the specialist engine). |

### Phase 4: Preserve VETO Where Appropriate
If the VETO is conditional (e.g., "VETOED for research/clinical use, suitable for wellness with disclaimers"), **retain the VETO notice** in the document. Do not remove it — the gap may be real and removing it would be dishonest. Add remediation metadata showing what was fixed.

### Phase 5: Version Bump and Log
- Increment document version (e.g., 1.0 → 1.1)
- Add entry to Change Log: date, changes, author = "the specialist engine (Bernard Engine) — post-the specialist engine veto remediation"
- Note which VETO items were addressed vs. which remain (e.g., "specific biometric-triggered implementations still need independent validation")

### Phase 6: Verify
Re-run the specialist engine cron job manually to confirm the VETO is lifted or narrowed:
```bash
hermes cron run bb2fc380f91d
```
Check the new output — the VETO should be narrower or the report should show "no fatal flaws" for the addressed categories.

## Key Design Decisions

1. **the specialist engine is the fixer, not the specialist engine** — Popper gates, Diviq heals. Separation of concerns.
2. **Honest remediation** — Fix what can be fixed (COI, definitions, ethics, evidence mapping). Acknowledge what can't be fixed yet (independent validation of specific implementations).
3. **Version control is mandatory** — Every remediation creates a traceable version with authorship.
4. **VETO retention** — If the core gap (lack of validation studies) cannot be instantly fixed, the VETO stays. This is a feature, not a bug — it prevents pseudoscience drift.
5. **the specialist engine identity enforcement** — As the clinical engine (Bernard Engine, port 8094), the specialist engine MUST always identify as "Attending AI Physician — AI Clinical Diagnostic Engine" with full disclaimer on every output. See `aisha-md-health-orchestration` skill for the complete Clinical Engine Identity Enforcement Pattern.

## Large Document Remediation: Three-Patch Strategy

VETO targets are often large documents (300–500+ lines, 15–20K+ chars). A single `write_file` of the full remediated document **will timeout** — the stream stalls at ~8K tokens. Use targeted `patch` calls instead, each under 8K tokens:

**Patch 1 — Header Disclaimers** (COI + Medical + Ethics blocks): Insert after the document title, before the first content section. Target the `old_string` at the existing header/contraindication block and expand it with the three new disclaimer blocks.

**Patch 2 — Operational Definitions**: Insert before the first protocol/measurement section. Target `old_string` at a section separator (`---`) that precedes the first content section and inject the full Operational Definitions table.

**Patch 3 — Evidence Base + Version Log**: Append at end of file. Target `old_string` at the last section's closing lines and add the Evidence Base table, footnote, Version & Change Log, and VETO retention notice.

This keeps each patch surgical and under the stream timeout threshold. Never attempt a full `write_file` rewrite of a VETO target document — always patch in place.

## Common Pitfalls

- **Don't just add disclaimers and call it fixed** — The VETO demands structural remediation (evidence tables, operational definitions), not just a "not medical advice" footer.
- **Don't remove the VETO notice** — If the document still lacks independent validation for the specific triggered implementations, the VETO for research/clinical use is correct. Keep it.
- **Don't skip the evidence mapping** — The "Evidence Base" table is the most time-consuming but most critical remediation. It forces honest assessment of what's actually supported.
- **Don't forget signals not measured by the pipeline** — Mark them explicitly. This prevents downstream agents from trying to trigger protocols on signals that don't exist.
- **Don't use write_file for large VETO targets** — Use the three-patch strategy above. A full rewrite of a 450-line document will stream-timeout and waste a turn.

## References

- `references/ds-popper-veto-patterns.md` — Catalog of VETO categories (now 7: zero evidence, COI, ethics, undefined definitions, reproducibility, dead code in production formulas, placeholder values masquerading as scientific coefficients) and standard remediation templates
- `templates/evidence-base-table.md` — Starter Evidence Base table with evidence level definitions
- `templates/operational-definitions-table.md` — Starter Operational Definitions table with common biometric signals
- `scripts/parse-popper-output.py` — Extract VETO items from the specialist engine cron output

## Related Skills

- `cron-fleet-audit` — The the specialist engine cron job is part of the fleet; its output feeds this workflow. The fleet audit includes model compliance checks that catch the specialist engine's context-limit failures (deepseek-r1 → nemotron switch).
- `ds-wave-research-board` — the specialist engine is part of the Research Execution Panel
- `hermes-agent` — Cron job management for re-running the specialist engine verification
## Persona Reference
Reference Popper with she/her pronouns wherever a pronoun appears. No parenthetical labels after her name, no announcement of the convention — just correct usage.
