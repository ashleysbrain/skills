# Key Considerations and Pitfalls for Algorithm Integrity Checks

## Critical Pitfalls Learned from Experience

### 1. Interaction Matrix Values
**Pitfall**: Interaction matrix DB values ≠ proprietary skill docs κ values  
**Details**: The skill docs list fleet-agent coupling coefficients (PSY↔INT=0.85, PHY↔VOC=0.78, SOC↔SPI=0.72, ENV↔PHY=0.68). The DB and calculator.py use HUMAN scoring values which are much lower (PSY↔INT=0.30, PHY↔VOC=0.30, SOC↔SPI=0.20, ENV↔PHY=0.25).  
**Solution**: Always compare DB values against `calculator.py` KAPPA dict, not the skill docs.

### 2. Database Column Names
**Pitfall**: DB column is `int_score`, not `int`  
**Details**: Querying `int` causes `no such column` error. Same for `8d_data_staleness_days` — must be quoted if used.  
**Solution**: Use exact column names from the schema: `int_score`, not `int`.

### 3. Calculator Normalization
**Pitfall**: calculator_v3 may use different normalization than documented  
**Details**: On 2026-05-28, stored TWC=42.24 but computed TWC from 8D+modifiers=54.97. Neither matches the skill-documented formula. The calculator_v3 output is opaque.  
**Solution**: Flag divergences even if you can't reverse-engineer the cause. The calculator.py output is the source of truth.

### 4. Fix Persistence
**Pitfall**: VERITAS fixes may not persist  
**Details**: VERITAS reported fixing 5/28 TWC to 72.0, but the DB shows 42.24 (overwritten by a later standup run at 12:42 UTC, before VERITAS ran at 19:00 UTC... or the fix was never persisted).  
**Solution**: Always re-check DB values directly after claiming a fix.

### 5. Pipeline Coverage Overcounting
**Pitfall**: Pipeline coverage overcounting  
**Details**: VERITAS counted 5/14 days covered (36%) but 2 of those days had twc_score=NULL (5/21 source='cron'). Real coverage was 3/14 (21%).  
**Solution**: Only count days where twc_score IS NOT NULL AND twc_score > 0.

### 6. Modifier Precision
**Pitfall**: Small discrepancies in modifiers compound  
**Details**: Sex modifier 5/27 stale: composite=76.3, stored mod=1.0000, expected=1.0026. Off by only 0.0026 but contradicts "all correct" claims.  
**Solution**: Use strict tolerance checks (e.g., < 0.001) and don't dismiss small discrepancies.

### 7. Source of Truth for Human Scoring
**Pitfall**: Misunderstanding which values apply to human vs fleet scoring  
**Details**: The calculator.py KAPPA dict is the source of truth for human scoring, NOT the proprietary-twc-scoring skill docs. The skill docs describe fleet-agent scoring which uses different (higher) coupling values.  
**Solution**: Always read calculator.py directly for human scoring validation.

## Implementation Guidelines

### Use execute_code for Database Access
- Never use `terminal` tool for sqlite3 queries due to shell quoting issues
- Always use `execute_code` which runs Python directly in a sandbox

### Handle Missing Data Gracefully
- 8D data for today may not exist yet - don't fabricate scores
- Report what's actually available vs what's missing

### Follow the Exact Sequence
1. Self-referential loop check (PRIORITY)
2. Engine tests
3. Nutrition/sexual health engine validation
4. Data integrity checks
5. Patient 0 audit
6. Overall verdict

### Reporting Standards
- Never modify scores, DB, or files during the check
- If issues are found, report them but do not attempt fixes in this check
- All numeric values should come directly from authoritative sources
- Preserve audit trails - never silently change numbers

## References
- calculator.py: `/<workspace>`
- rescore_engine.py: `/<workspace>`
- Database schema: `/<workspace>`
- EF tracker: `/<workspace>`