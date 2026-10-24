# Adversarial Engine Template — Copy-Paste-Ready

## File Structure

```
ds-atk-XX-<name>-engine/
├── src/
│   └── atcXX/
│       └── core/
│           ├── __init__.py
│           ├── methodology.py  ← LAYER 4 (REQUIRED)
│           ├── engine.py       ← LAYERS 1, 3, 5, 6 (required for full organism)
│           ├── philosophy.py   ← LAYER 2 (required for full organism)
│           └── cognitive.py    ← LAYER 5 (required for full organism)
└── requirements.txt
```

## methodology.py Template (REQUIRED)

```python
"""DS ATC-XX — <Engine Name> — Layer 4: Methodology

==========================================================================
ENGINE IDENTITY
==========================================================================
Engine name ......... DS ATC-XX <Engine Name>
DS-ECS code .......... DS-ECS-ATK-XX-01-v1.0.0  (Port 82XX)
Body system .......... adversarial  (<Domain>)
Eight-D dimension .... <intellectual|physical|emotional>
Role ................. <Role description>

SCIENTIST NAMESAKE
------------------
<Scientist> (years), <credentials>.
<Why this scientist is relevant>.

THE 5-SEAT ADVERSARIAL PANEL
-----------------------------
DS ATC-XX's method is realised as a 5-seat adversarial panel. Each seat
specializes in a <domain> attack dimension:

  1. <SCIENTIST> SEAT — <Methodology 1>
  2. <SCIENTIST> SEAT — <Methodology 2>
  3. <SCIENTIST> SEAT — <Methodology 3>
  4. <SCIENTIST> SEAT — <Methodology 4>
  5. <SCIENTIST> SEAT — <Methodology 5>

Together the five seats <describe what they do together>.
==========================================================================
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "ds-engine-shared"))

from methodology_base import (
    MethodologyLayerBase,
    Institution,
    MethodologyProfile,
    PersonalityVariant,
    ModelRoute,
    SubAgentSpec,
)

# ---------------------------------------------------------------------------
# INSTITUTIONS — elite institutions tied to the scientist's lineage
# ---------------------------------------------------------------------------
INSTITUTIONS = [
    Institution(
        name="<Institution 1>",
        short_code="<CODE1>",
        location="<City, Country>",
        methodology="<Methodology>",
        methodology_code="<CODE>-<YEAR>",
        relevance="<Why this institution matters>",
        key_papers=[
            "<Paper 1>",
            "<Paper 2>",
            "<Paper 3>",
        ],
        ranking_year=2025,
    ),
    Institution(
        name="<Institution 2>",
        short_code="<CODE2>",
        location="<City, Country>",
        methodology="<Methodology>",
        methodology_code="<CODE>-<YEAR>",
        relevance="<Why this institution matters>",
        key_papers=[
            "<Paper 1>",
            "<Paper 2>",
        ],
        ranking_year=2025,
    ),
]

# ---------------------------------------------------------------------------
# PERSONALITY VARIANTS — adversarial behavioral profiles
# ---------------------------------------------------------------------------
PERSONALITIES = [
    PersonalityVariant(
        name="The <Personality 1>",
        archetype="<Archetype>",
        traits=["trait1", "trait2", "trait3", "trait4"],
        communication_style="<How they speak>",
        decision_speed="<deliberate|rapid|medium|slow>",
        risk_tolerance="<high|low|calculated|very_low>",
        preferred_model="<model-name>",
        preferred_methodology="<METHODOLOGY-CODE>",
    ),
    PersonalityVariant(
        name="The <Personality 2>",
        archetype="<Archetype>",
        traits=["trait1", "trait2", "trait3", "trait4"],
        communication_style="<How they speak>",
        decision_speed="<deliberate|rapid|medium|slow>",
        risk_tolerance="<high|low|calculated|very_low>",
        preferred_model="<model-name>",
        preferred_methodology="<METHODOLOGY-CODE>",
    ),
    # Add more personalities
]

# ---------------------------------------------------------------------------
# SUB-AGENTS — specialized adversarial tools
# ---------------------------------------------------------------------------
SUB_AGENTS = [
    SubAgentSpec(
        role="<Sub-agent 1>",
        purpose="<What it does>",
        required_expertise=["expertise1", "expertise2", "expertise3"],
        personality="<Personality name>",
        task_type="adversarial_attack",
        can_spawn_further=True,
    ),
    SubAgentSpec(
        role="<Sub-agent 2>",
        purpose="<What it does>",
        required_expertise=["expertise1", "expertise2"],
        personality="<Personality name>",
        task_type="adversarial_attack",
        can_spawn_further=True,
    ),
    # Add more sub-agents
]

# ---------------------------------------------------------------------------
# METHODOLOGIES — analytical frameworks
# ---------------------------------------------------------------------------
METHODOLOGIES = [
    MethodologyProfile(
        code="ATC-M<XX>1",
        name="<Methodology 1>",
        institution="<Institution>",
        description="<Description>",
        best_for=["expertise1", "expertise2"],
        parameters={
            "param1": "value1|value2|value3",
            "param2": "type",
        },
    ),
    MethodologyProfile(
        code="ATC-M<XX>2",
        name="<Methodology 2>",
        institution="<Institution>",
        description="<Description>",
        best_for=["expertise1", "expertise3"],
        parameters={
            "param1": "type",
            "param2": "list",
        },
    ),
    # Add more methodologies
]

# ---------------------------------------------------------------------------
# MODEL ROUTING — task-specific model routing
# ---------------------------------------------------------------------------
MODEL_ROUTES = [
    ModelRoute(
        task_type="adversarial_attack",
        model="<model-name>",
        provider="<anthropic|openai|llm-vendor>",
        reason="<Why this model>",
    ),
    ModelRoute(
        task_type="adversarial_attack",
        model="<model-name>",
        provider="<anthropic|openai|llm-vendor>",
        reason="<Why this model>",
    ),
]

# ---------------------------------------------------------------------------
# METHODOLOGY LAYER CLASS
# ---------------------------------------------------------------------------
class <EngineName>Methodology(MethodologyLayerBase):
    """<Scientist>'s <framework>"""

    def __init__(self):
        super().__init__(
            engine_name="DS ATC-XX <Engine Name>",
            body_system="adversarial",
            eight_d_dimension="<intellectual|physical|emotional>",
            institutions=INSTITUTIONS,
            methodologies=METHODOLOGIES,
            personalities=PERSONALITIES,
            model_routes=MODEL_ROUTES,
            version="1.0.0",
        )

    DEFAULT_PERSONALITY = PERSONALITIES[0]
    DEFAULT_INSTITUTION = INSTITUTIONS[0]
    DEFAULT_METHODOLOGY = METHODOLOGIES[0]

# ---------------------------------------------------------------------------
# Export for the specialist engine
# ---------------------------------------------------------------------------
def select_methodology(situation: str, task_type: str = None) -> dict:
    """the specialist engine entry point: select appropriate methodology"""
    methodology = <EngineName>Methodology()
    result = methodology.select_all(situation, task_type or "adversarial_attack")

    result["adversarial_context"] = {
        "attack_type": "<attack_type>",
        "seat_count": 5,
        "primary_frame": "<primary_frame>",
        "secondary_frame": "<secondary_frame>",
    }

    return result

def get_engine_info() -> dict:
    """Return engine metadata for the specialist engine"""
    return {
        "engine_name": "DS ATC-XX <Engine Name>",
        "ds_ecs_code": "DS-ECS-ATK-XX-01-v1.0.0",
        "port": 82XX,
        "body_system": "adversarial",
        "eight_d_dimension": "<intellectual|physical|emotional>",
        "role": "<Role>",
        "scientist": "<Scientist>",
    }
```

## ENGINE_REGISTRY.yaml Entry

```yaml
- directory: ds-atk-XX-<name>-engine
  engine_name: DS ATC-XX <Engine Name>
  port: 82XX
  scientist: <Scientist>
  body_system: adversarial
  ds_ecs_code: DS-ECS-ATK-XX-01-v1.0.0
```

## Execution Command

```bash
cd /<workspace><name>-engine
python3 -c "
import sys
import json
sys.path.insert(0, 'src')
from atcXX.core.methodology import get_engine_info, select_methodology

info = get_engine_info()
print(json.dumps(info, indent=2))

result = select_methodology(
    '<Attack situation description>',
    'adversarial_attack'
)
print(json.dumps(result, indent=2))
"
```

## Requirements

```
# /<workspace> (dependency)
```

## Notes

- All required fields MUST be present (PersonalityVariant needs preferred_model and preferred_methodology)
- MethodologyProfile needs best_for list
- ModelRoute needs task_type as first field
- Engine must be registered in ENGINE_REGISTRY.yaml
- Engine can be invoked directly via Python (the specialist engine integration optional but recommended)