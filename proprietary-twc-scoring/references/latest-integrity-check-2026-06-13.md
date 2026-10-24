# Algorithm Integrity Check Findings - 2026-06-13

## Key Findings from integrity-check-findings-2026-06-13.md

### SELF-REFERENTIAL LOOP CHECK:
- Observations scanned: 390
- Self-referential found: 0 ❌
- Deleted: 0
- Score corrections: [none] → [none]

### ENGINE TESTS:
- Rescore engine: ✅ 7/7 / ❌ 0 failures
- Nutrition engine: ⚠️ LABEL MISMATCH (composite 79.0 labeled "strong" should be "adequate")
- Sexual health engine: ⚠️ LABEL MISMATCH (composite 76.3 labeled "healthy" should be "strong")

### DATA INTEGRITY:
- Pipeline coverage: 4/31 days (13%) - MAJOR GAP
- Drift from baseline: -33.84 (baseline 62.2 on 2026-05-28 vs latest 28.36 on 2026-05-29)
- Interaction matrix: ❌ VALUES MISMATCH (PSY↔INT: 0.2 vs 0.85 spec, PHY↔VOC: 0.15 vs 0.78, etc.)

### PATIENT 0 AUDIT:
- Activation observations reviewed: 5 (algorithm work properly credited as activation)
- Under-scored work detected: N
- GitHub-only lens detected: N

### VERDICT: ❌ MATERIAL ISSUES