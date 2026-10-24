# Interaction Matrix Findings - 2026-06-13
## VERITAS-ALGO Integrity Check

## Summary
The interaction_matrix table in ashley_unified_health.db contains values that significantly deviate from the proprietary TWC specification coupling coefficients.

## Findings
Proprietary specification vs. actual database values:

| Coupling Pair | Spec Value | Actual Value | Difference |
|---------------|------------|--------------|------------|
| PSY↔INT       | 0.85       | 0.20         | -0.65      |
| PHY↔VOC       | 0.78       | 0.15         | -0.63      |
| SOC↔SPI       | 0.72       | 0.20         | -0.52      |
| ENV↔PHY       | 0.68       | 0.25         | -0.43      |

All actual values are approximately 70-75% lower than specification values.

## Query Used
```sql
SELECT dim1, dim2, value 
FROM interaction_matrix 
WHERE (dim1='PSY' AND dim2='INT') OR (dim1='INT' AND dim2='PSY')
   OR (dim1='PHY' AND dim2='VOC') OR (dim1='VOC' AND dim2='PHY')
   OR (dim1='SOC' AND dim2='SPI') OR (dim1='SPI' AND dim2='SOC')
   OR (dim1='ENV' AND dim2='PHY') OR (dim1='PHY' AND dim2='ENV');
```

## Actual Results
```
INT|PSY|0.2|Cognitive reserve and mental health: intellectual engagement protects against cognitive decline and depression|Valenzuela & Sachdev 2006 Psychol Med cognitive reserve meta-analysis; Stern 2009 Neuron|STRONG|2026-05-27T02:07:53Z|2026-05-27T02:07:53Z
PHY|VOC|0.15|Physical health-work performance: fitness predicts productivity, reduced absenteeism|Pronk 2009 ACSM workplace health; Rongen et al. 2013 Occupational Environmental Medicine meta-analysis|MODERATE|2026-05-27T02:07:53Z|2026-05-27T02:07:53Z
SOC|SPI|0.2|Community-spiritual belonging: congregational participation, shared rituals, spiritual community|Lim & Putnam 2010 American Sociological Review religion social capital; Ellison & George 1994 J Scientific Study Religion|MODERATE|2026-05-27T02:07:53Z|2026-05-27T02:07:53Z
ENV|PHY|0.25|Nature-based physical activity synergy: outdoor exercise amplifies both physical and environmental wellbeing benefits|Bratman et al. 2019 Sci Advances nature experience meta-analysis; Twohig-Bennett & Jones 2018 Environmental Research|STRONG|2026-05-27T02:07:53Z|2026-05-27T02:07:53Z
```

## Root Cause Analysis
The interaction_matrix values appear to be populated with default or placeholder values rather than the scientifically-derived coupling coefficients specified in the proprietary TWC formula. This suggests either:
1. The population script for interaction_matrix is not functioning correctly
2. The values were set during initial development and never updated to reflect the proprietary specification
3. There is a mismatch between the specification documentation and the implementation

## Impact
Since the interaction_matrix values are used in TWC recomputation verifications (as noted in qubit-gr-8d360-scoring-pipeline skill), this discrepancy means:
- Integrity checks using the specification values will show false mismatches
- The actual coupling effect in scores may be significantly understated
- Intervention Leverage Score (ILS) calculations may be inaccurate

## Recommended Actions
1. Investigate the source of interaction_matrix population
2. Either:
   a. Update interaction_matrix values to match proprietary specification (0.85, 0.78, 0.72, 0.68)
   b. Update proprietary specification to match empirically validated values (after proper validation)
3. Document the decision and update all relevant skills and verification procedures
4. Re-run integrity checks with corrected values