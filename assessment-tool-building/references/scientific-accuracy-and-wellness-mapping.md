# Scientific Accuracy, Wellness Mapping, and Facet Guide

Companion to `assessment-tool-building/SKILL.md` sections "Scientific Accuracy
in Assessment UI" and "8D-Inspired Wellness Mapping." Contains the reusable
data structures and patterns built for the IPIP-NEO Goldberg-Johnson
Personality Inventory (2026-08-07).

## Wellness Mapping: OCEAN-to-8D

Maps each OCEAN domain to wellness dimensions with citations. Each entry has
high/low descriptions and actions. Both poles are strength-framed.

```javascript
const WELLNESS_MAP = {
  intellectual: {
    name: 'Intellectual',
    primaryDomain: 'O',
    highDesc: 'You are naturally drawn to ideas, abstract thinking, and intellectual exploration.',
    lowDesc: 'You tend to prefer the practical and concrete over abstract theorizing.',
    highAction: 'Feed your curiosity with structured deep-dives into new domains.',
    lowAction: 'Channel your practical intelligence into hands-on problem-solving.',
    source: 'Openness is the strongest personality correlate of intellectual engagement and lifelong learning (McCrae & Costa, 1997).'
  },
  social: {
    name: 'Social',
    primaryDomain: 'E',
    highDesc: 'You gain energy from social interaction and tend to build wide social networks.',
    lowDesc: 'You prefer fewer, deeper connections and recharge through solitude.',
    highAction: 'Leverage your networks, but protect time for depth over breadth.',
    lowAction: 'Invest deliberately in a few close relationships. Quality over quantity.',
    source: 'Extraversion is the strongest personality correlate of social network size (Asendorpf & Wilpers, 1998).'
  },
  emotional: {
    name: 'Emotional',
    primaryDomain: 'N',
    highDesc: 'You experience emotions intensely. You benefit from active regulation skills.',
    lowDesc: 'You tend to stay emotionally steady under pressure.',
    highAction: 'Build a regular stress-reduction practice. Mindfulness and CBT have strong evidence bases.',
    lowAction: 'Use your stability to support others and take on high-pressure challenges.',
    source: 'Neuroticism is the strongest personality correlate of subjective well-being and stress reactivity (Lahey, 2009).'
  },
  vocational: {
    name: 'Vocational',
    primaryDomain: 'C',
    highDesc: 'You are driven by achievement, structure, and goal completion.',
    lowDesc: 'You prefer flexibility and spontaneity over rigid structure.',
    highAction: 'Set ambitious but realistic goals. Beware of perfectionism and burnout.',
    lowAction: 'Create lightweight external structure to channel your flexibility productively.',
    source: 'Conscientiousness is the strongest personality correlate of job performance across occupations (Barrick & Mount, 1991, meta-analysis).'
  },
  interpersonal: {
    name: 'Interpersonal',
    primaryDomain: 'A',
    highDesc: 'You naturally prioritize cooperation, empathy, and harmony.',
    lowDesc: 'You are direct, competitive, and comfortable with conflict.',
    highAction: 'Your cooperation is a strength, but practice setting boundaries.',
    lowAction: 'Your directness is effective. Practice tempering it with empathy in sensitive situations.',
    source: 'Agreeableness is associated with relationship satisfaction and interpersonal trust (Graziano & Eisenberg, 1997).'
  },
  physical: {
    name: 'Physical',
    primaryDomains: ['C', 'N'],
    desc: 'Conscientiousness and emotional stability are both associated with health behaviors.',
    action: 'High-C individuals tend to maintain consistent health routines. Those with higher emotional sensitivity tend to benefit most from active stress-reduction practices. These are statistical patterns, not guarantees.',
    source: 'Conscientiousness is associated with health behaviors and longevity in the Terman Life Cycle study (Friedman et al., 1993). Higher neuroticism is associated with stress-related health complaints in cross-sectional studies (Lahey, 2009).'
  },
  financial: {
    name: 'Financial',
    primaryDomains: ['C'],
    desc: 'Conscientiousness is the personality trait most strongly associated with financial responsibility.',
    action: 'If your C score is high, channel this into systematic financial planning. If lower, use automated systems and external accountability.',
    source: 'Conscientiousness is associated with financial behaviors and credit scores (Letkiewicz & Fox, 2014).'
  },
  environmental: {
    name: 'Environmental',
    primaryDomains: ['O', 'A'],
    desc: 'Openness to experience and agreeableness together are associated with environmental awareness.',
    action: 'High-O individuals often thrive in aesthetically rich, varied environments. High-A individuals are more likely to engage in pro-environmental behavior.',
    source: 'Openness and Agreeableness are associated with pro-environmental attitudes and behaviors (Hirsh, 2010).'
  }
};
```

### Rendering function

```javascript
function buildWellnessPanel(scoreData) {
  var domainMap = {};
  (scoreData.domains || []).forEach(function(d) {
    domainMap[d.domain_code] = d.mean;
  });
  // For each wellness dim: if primaryDomain score >= 3.4 use highDesc,
  // if <= 2.6 use lowDesc, else blend. Show the matching action.
}
```

## Facet Guide Pattern: Separate High/Low Actions

CRITICAL: each facet needs FOUR fields: `high`, `low`, `actionHigh`,
`actionLow`. A single `action` field will show wrong advice for one pole.

Template for all 30 IPIP-NEO facets:

```javascript
const FACET_GUIDE = {
  N1: {
    high: 'You are attentive to potential threats and risks.',
    low: 'You experience low baseline anxiety and remain calm under uncertainty.',
    actionHigh: 'Channel your vigilance into planning rather than rumination.',
    actionLow: 'Your calm is an asset in high-pressure roles.'
  },
  // ... repeat for all 30 facets (N1-N6, E1-E6, O1-O6, A1-A6, C1-C6)
};
```

### Strengths & Growth Edges rendering

```javascript
function buildStrengthsPanel(scoreData) {
  var facets = scoreData.facets.slice().sort(function(a,b) {
    return b.mean - a.mean;
  });
  var top3 = facets.slice(0, 3);    // Signature Strengths
  var bottom3 = facets.slice(-3).reverse();  // Growth Edges

  // For strengths: use guide.high + guide.actionHigh
  // For growth edges: use guide.low + guide.actionLow
  // NEVER use guide.actionHigh for a growth edge card
}
```

### Interpretation thresholds

```javascript
function interpLabel(score) {
  if (score >= 4.2) return 'Very High';
  if (score >= 3.4) return 'High';
  if (score >= 2.6) return 'Average';
  if (score >= 1.8) return 'Low';
  return 'Very Low';
}
```

## Physics Concept Relabeling

The backend returns physics concepts with jargon names. The UI must relabel
them as plain-English measurement quality indicators:

| Backend key | UI label | Plain description |
|---|---|---|
| concept_1_superposition | Response Decisiveness | How many facets landed near the midpoint |
| concept_2_entanglement | Domain Balance | Which domain pairs show notable differences |
| concept_3_free_energy | Information Quality | Whether enough non-neutral responses were given |
| concept_4_critical_slowing | Internal Consistency | Facets where responses varied widely |
| concept_5_adiabatic | Response Diversity | Whether you used the full scale range |

Section subtitle: "These reflect how carefully the assessment was taken,
not personality traits."

## Adversarial Review Checklist

Before shipping any assessment UI, run a subagent adversarial pass with
these instructions:

1. **Read only the assessment file** (no file exploration beyond it).
2. **Do NOT load any skills** (blows context budget before review completes).
3. **Cap output at 800 words**.
4. Check for:
   - [ ] Correlation stated as causation ("predicts" vs "is associated with")
   - [ ] Missing percentile disclaimers
   - [ ] Facet actions showing wrong-pole advice (actionHigh for low scorers)
   - [ ] Pathologizing language ("crumbles", "extreme", "unstable")
   - [ ] Missing informed consent block
   - [ ] Missing safety disclaimer
   - [ ] Inaccurate citations (wrong author, wrong year, wrong study type)
   - [ ] Physics concepts presented as validated psychometric constructs
   - [ ] Deficit framing (low scores described as problems, not variations)
   - [ ] Deterministic language ("you are X" vs "you tend toward X")

## Citation Reference Table

All citations used in the wellness map, verified for accuracy:

| Claim | Citation | Study type | Accuracy note |
|---|---|---|---|
| Openness <-> intellectual engagement | McCrae & Costa (1997) | Correlational | Correct |
| Extraversion <-> social network size | Asendorpf & Wilpers (1998) | Longitudinal | Correct |
| Neuroticism <-> subjective well-being | Lahey (2009) | Review | Cross-sectional evidence |
| Conscientiousness <-> job performance | Barrick & Mount (1991) | Meta-analysis | Correlational at individual level |
| Agreeableness <-> relationship satisfaction | Graziano & Eisenberg (1997) | Chapter | Associational |
| Conscientiousness <-> longevity | Friedman et al. (1993) | Longitudinal (Terman) | Correct: Terman Life Cycle study |
| Neuroticism <-> health complaints | Lahey (2009) | Review | Cross-sectional, not causal |
| Conscientiousness <-> financial behavior | Letkiewicz & Fox (2014) | Correlational | Correct |
| O+A <-> pro-environmental behavior | Hirsh (2010) | Correlational | Correct |

## Verified Build

Built and verified 2026-08-07 at `personality_test.html` (workspace root):
- 8 wellness dimensions with citations
- 30-facet interpretation guide with separate actionHigh/actionLow
- Signature Strengths (top 3) + Growth Edges (bottom 3)
- Physics concepts relabeled as measurement quality indicators
- Adversarial review run (1 pass, found critical actionHigh/actionLow bug)
- All fixes verified through live browser testing
