# ECS Prefix Corrections Reference

**Session:** 2026-06-25 — Operator bus R2 processing
**Issue:** Messages used invalid ECS v4.0 category prefixes (REP, ALS, HRV, MRG, BEA, BRI, UNN)
**Correction:** All engines must use valid DS-ECS v4.0 prefixes (SYS/ORG/SUB/CEL/NPR/PTH/APP/GEN) with proper scientist names from registry.

---

## Invalid → Valid Mapping

| Invalid Prefix | Invalid Code Example | Correct Engine Name | Correct DS-ECS Code | Scientist | Domain |
|----------------|---------------------|---------------------|------------------------|--------|
| REP | DS-ECS-REP-01.00.00-v1.0.0 | **the specialist engine** | DS-ECS-ORG-11.01.01-v1.1.0 | Reproductive |
| ALS | DS-ECS-ALS-01.00.00-v1.0.0 | **the specialist engine** | DS-ECS-SUB-04.02.01-v1.0.0 | Nervous (Homeostasis) |
| HRV | DS-ECS-HRV-01.00.00-v1.0.0 | **the specialist engine** | DS-ECS-ORG-06.01.01-v1.1.0 | Cardiovascular |
| MRG | DS-ECS-MRG-01.00.00-v1.0.0 | **the specialist engine** | DS-ECS-ORG-11.01.02-v1.1.0 | Reproductive (Morphogen) |
| BEA | DS-ECS-BEA-01.00.00-v1.0.0 | **the specialist engine** | DS-ECS-ORG-09.01.01-v1.0.0 | Digestive |
| BRI | DS-ECS-BRI-01.00.00-v1.0.0 | **the specialist engine** | DS-ECS-ORG-10.01.01-v1.1.0 | Urinary |
| UNN | DS-ECS-UNN-01.00.00-v1.0.0 | **the specialist engine** | DS-ECS-SYS-01.01.01-v1.1.0 | Integumentary |

---

## Additional Corrections from Same Session

| Incorrect Reference | Correct Engine | Correct Code |
|---------------------|----------------|--------------|
| DS-ECS-SUB-04.15.02 (O'Keefe afferent) | **DS O'Keefe** | DS-ECS-SUB-04.09.01-v1.1.0 |
| "the specialist engine" (deprecated) | **the specialist engine** | DS-ECS-PTH-04.01.01-v1.1.0 |
| "the specialist engine" (proposed as PTH-04.01.02) | **the specialist engine** | DS-ECS-SUB-04.11.01-v1.0.0 (already correct) |

---

## Valid ECS v4.0 Category Prefixes (ONLY THESE 8)

| Prefix | Category | Definition |
|--------|----------|------------|
| **SYS** | Organ System | Complete body system spanning the organism |
| **ORG** | Organ | Discrete macroscopic anatomical organ |
| **SUB** | Substructure | Named region within an organ |
| **CEL** | Cell System | Population of cells with shared function |
| **NPR** | Neural Process | Functional mechanism across cell populations |
| **PTH** | Pathway | Signal or mechanical route through tissue |
| **APP** | Apparatus | Composite functional unit (not a single organ) |
| **GEN** | Genetic | DNA/genome/chromatin level entity |

---

## Protocol: When You See Invalid Prefixes

1. **STOP** — do not proceed with invalid codes
2. **LOOKUP** — check `agent-organism/REGISTRY.yaml` or `ecs.py` for correct scientist name and code
3. **CORRECT** — use DS <Scientist Name> (DS-ECS-<VALID_PREFIX>-DD.SS.NN-vX.Y.Z)
4. **POST CORRECTED R2** — if processing operator bus messages, post corrected response
5. **NEVER** use ad-hoc prefixes like REP/ALS/HRV/MRG/BEA/BRI/UNN — they don't exist in ECS v4.0

---

## Source of Truth

- Canonical registry: `/<workspace>`
- Python source: `/<workspace>` (FLEET_REGISTRY)
- Domain map: 11 Gray's Anatomy systems + Diagnostic (01-12)