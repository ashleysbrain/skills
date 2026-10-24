# Adversarial Execution Pattern

## Overview

Execute adversarial attacks using built adversarial engines with specialist brains, NOT generalist drift.

## Pre-Execution Checklist

Before executing adversarial attacks:

1. ✅ Adversarial engines built (at least 1, preferably 3-5)
2. ✅ Engines registered in ENGINE_REGISTRY.yaml
3. ✅ Engines can be invoked via Python directly
4. ✅ Target strategy clearly defined
5. ✅ Attack situation description ready

## Execution Modes

### Mode 1: Single Engine Attack

Execute one adversarial engine against a target strategy.

**Command:**
```bash
cd /<workspace><name>-engine
python3 -c "
import sys
import json
sys.path.insert(0, 'src')
from atcXX.core.methodology import get_engine_info, select_methodology

# Get engine info
print('=== Engine Info ===')
info = get_engine_info()
print(json.dumps(info, indent=2))

# Select methodology for attack
print('\n=== Attack Execution ===')
result = select_methodology(
    '<Attack situation description>',
    'adversarial_attack'
)
print(json.dumps(result, indent=2))
"
```

**Use when:**
- Testing single dimension (competitive, regulatory, moat, timeline)
- Deep dive into specific vulnerability
- Target strategy is narrow

---

### Mode 2: Parallel Multi-Engine Attack

Execute multiple adversarial engines in parallel using delegate_task.

**Code:**
```python
from hermes_tools import delegate_task

delegate_task(
    tasks=[
        {
            "goal": "Execute DS ATC-01 Competitive Analysis adversarial attack on the specialist engine strategy. Target: Find competitive vulnerabilities in positioning, moat strength, and differentiation.",
            "toolsets": ["terminal"],
        },
        {
            "goal": "Execute DS ATC-02 Regulatory Attack adversarial attack on the specialist engine strategy. Target: Find regulatory vulnerabilities in health claims, medical device classification, and HIPAA compliance.",
            "toolsets": ["terminal"],
        },
        {
            "goal": "Execute DS ATC-03 Moat Stress-Test adversarial attack on the specialist engine strategy. Target: Find moat vulnerabilities in brand, switching costs, network effects, and regulatory barriers.",
            "toolsets": ["terminal"],
        },
        {
            "goal": "Execute DS ATC-04 Timeline Hack adversarial attack on the specialist engine strategy. Target: Find timeline vulnerabilities in feasibility, estimation error, and complexity growth.",
            "toolsets": ["terminal"],
        },
    ]
)
```

**Use when:**
- Comprehensive adversarial coverage
- Target strategy is broad
- Time-sensitive (parallel execution faster)

---

### Mode 3: Sequential Multi-Engine Attack

Execute multiple adversarial engines sequentially, using results from previous engines.

**Workflow:**
1. Execute ATC-01 (Competitive Analysis)
2. Analyze vulnerabilities found
3. Execute ATC-02 (Regulatory Attack) focusing on competitive vulnerabilities
4. Execute ATC-03 (Moat Stress-Test) focusing on regulatory vulnerabilities
5. Execute ATC-04 (Timeline Hack) focusing on moat vulnerabilities
6. Consolidate findings across all engines

**Use when:**
- Deep adversarial coverage
- Find cross-vulnerability patterns
- Each engine builds on previous findings

---

## Output Format

Each adversarial engine produces:

### 1. Engine Metadata (get_engine_info())
```json
{
  "engine_name": "DS ATC-01 Competitive Analysis",
  "ds_ecs_code": "DS-ECS-ATK-01-01-v1.0.0",
  "port": 8201,
  "body_system": "adversarial",
  "eight_d_dimension": "intellectual",
  "role": "Competitive intelligence adversarial engine",
  "scientist": "Michael Porter + Richard Rumelt"
}
```

### 2. Selected Methodology and Personality (select_methodology())
```json
{
  "engine": "DS ATC-01 Competitive Analysis",
  "body_system": "adversarial",
  "eight_d_dimension": "intellectual",
  "situation": "<Attack situation description>",
  "task_type": "adversarial_attack",
  "selected_methodology": {
    "code": "ATC-M01",
    "name": "Five Forces Analysis",
    "institution": "Harvard Business School",
    "description": "Analyze industry structure using Porter's Five Forces",
    "parameters": {
      "threat_of_new_entrants": "high|medium|low",
      "bargaining_power_of_suppliers": "high|medium|low",
      "bargaining_power_of_buyers": "high|medium|low",
      "threat_of_substitutes": "high|medium|low",
      "competitive_rivalry": "high|medium|low"
    }
  },
  "active_personality": {
    "name": "The Porter Analyst",
    "archetype": "Strategic analyst",
    "traits": ["systematic", "analytical", "ruthless", "evidence-driven"],
    "decision_speed": "deliberate",
    "risk_tolerance": "calculated",
    "communication_style": "Frames every argument in Porter's Five Forces; asks: 'What's the competitive advantage? Is it sustainable?'"
  },
  "model_routing": {
    "model": "glm-4.6",
    "provider": "llm-vendor",
    "reason": "High-quality adversarial thinking and strategic critique"
  },
  "sub_agents_for_task": [],
  "can_delegate": false,
  "version": "1.0.0",
  "adversarial_context": {
    "attack_type": "competitive_analysis",
    "seat_count": 5,
    "primary_frame": "porter_five_forces",
    "secondary_frame": "rumelt_strategy_kernel"
  }
}
```

### 3. Vulnerability List (Manual Analysis Required)

After receiving methodology and personality selection, the engine (or operator) must:

1. Apply the methodology to the target strategy
2. Use the selected personality's communication style
3. Identify vulnerabilities with severity ratings
4. List fixes required for each vulnerability

**Vulnerability Format:**
```markdown
## ENGINE #X: DS ATC-XX <Engine Name>

### Methodology Applied
<Methodology code + name>

### Personality Invoked
<Personality name>

### Vulnerability #<N>: <Title>
**Severity:** CRITICAL | HIGH | MEDIUM | LOW
**Description:** <What's wrong>
**Fix Required:** <How to fix>

### Final Verdict
<Overall assessment of the target strategy>
```

---

## Example: ATC-01 Attack Execution (2026-07-02)

**Command Executed:**
```bash
cd /<workspace>
python3 -c "
import sys
import json
sys.path.insert(0, 'src')
from atc01.core.methodology import get_engine_info, select_methodology

info = get_engine_info()
print(json.dumps(info, indent=2))

result = select_methodology(
    'Attack DS information layer strategy: Proprietary moat is 8D physics-informed scoring + 4D coupling matrix + TWC calculation. Find competitive vulnerabilities.',
    'adversarial_attack'
)
print(json.dumps(result, indent=2))
"
```

**Results:**
- Engine selected: DS ATC-01 Competitive Analysis
- Methodology selected: Five Forces Analysis (ATC-M01)
- Personality invoked: The Porter Analyst
- Model routed: glm-4.6 (llm-vendor)
- Adversarial context: Competitive analysis, 5-seat panel, Porter's Five Forces + Rumelt's Strategy Kernel

**Vulnerabilities Found:**
| # | Vulnerability | Severity |
|---|---------------|----------|
| V1 | Substitute threat is VERY HIGH (free AI scoring) | CRITICAL |
| V2 | Competitive rivalry is VERY HIGH (building ON competitors) | CRITICAL |
| V3 | "Proprietary scoring" moat is weak (12-18 month replication) | HIGH |
| V4 | Buyer power is HIGH (low switching costs) | HIGH |
| V5 | No coherent guiding policy | MEDIUM |

**Porter's Final Verdict:** "This strategy has no moat. Industry Attractiveness Score: 2/10."

---

## Post-Execution Workflow

After executing adversarial attacks:

1. **Consolidate Findings**
   - Aggregate vulnerabilities across all engines
   - Identify cross-vulnerability patterns
   - Rank by severity (CRITICAL > HIGH > MEDIUM > LOW)

2. **Strategy Board Response**
   - Route each vulnerability to appropriate specialist via the specialist engine
   - Generate fixes for each vulnerability
   - Update target strategy

3. **Deliverable Generation**
   - Adversarial attack report (Markdown + PDF)
   - Strategy brief (Markdown + PDF)
   - Vulnerability prioritization list

4. **Documentation**
   - Log execution in adversarial engine catalog
   - Update skill with new learnings
   - Save deliverables for future reference

---

## Troubleshooting

**Issue:** Engine cannot be invoked via Python

**Fix:** Check:
- Engine directory structure (src/atcXX/core/methodology.py)
- Python path (sys.path.insert)
- Import statement (from atcXX.core.methodology)
- Method signatures (get_engine_info, select_methodology)

**Issue:** select_methodology() returns empty methodology

**Fix:** Check:
- MethodologyProfile has best_for list
- Situation description includes keywords from best_for
- PersonalityVariant has preferred_methodology

**Issue:** Baseline-first gate blocking writes

**Fix:** Inspect baseline artifact first, then patch. This is a safety mechanism.

---

## Integration with Strategy Board

After adversarial execution, route findings to strategy board:

```python
# For each vulnerability found:
python3 /<workspace> \
    --gate \
    --situation "Address competitive vulnerability V#<N>: <vulnerability title>. Target strategy: the specialist engine. Fix required: <fix description>" \
    --operator hermes
```

This routes to the appropriate specialist (e.g., the specialist engine for positioning, the specialist engine for brand, etc.).

---

## See Also

- Adversarial engine template: `references/adversarial-engine-template.md`
- Engine catalog: `references/adversarial-engines-catalog.md`
- Skill main: `SKILL.md`