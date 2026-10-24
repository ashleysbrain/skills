---
name: organism-adversarial-engine-building
description: Build adversarial engines with complete DS organism architecture (5 ECS layers, 17 methodology layers) to stress-test business strategies with specialist brains
last_updated: 2026-07-02
---

# Adversarial Engine Building — Full Organism Architecture

## Purpose

Build adversarial engines with complete DS organism architecture (5 ECS layers, 17 methodology layers) to stress-test business strategies with specialist brains, NOT generalist drift.

## When to Use

- When tasked with adversarial attacks, strategy stress-testing, or vulnerability analysis
- When the user says "not in the generalist brain" or "use specialist brains"
- When building engines that represent real adversarial agents (Porter, Kessler, Buffett, Brooks, Kahneman)
- When avoiding protocol violations: "NEVER act as a generalist — generalist drift breaks the mastermind"

## Critical Pitfall: Generalist Drift

**SIGNAL TO STOP:** You're pretending to run adversarial attacks as yourself.

**RED FLAGS:**
- Headers show "the specialist engine, pre-route" but you never actually routed
- You're writing adversarial content without invoking the specialist engine
- You're simulating adversarial responses without proper specialist routing
- User feedback: "It still feels like this may be generalist work"

**FIX:** Stop immediately. Build adversarial engines with full organism architecture first.

## Organism Engine Structure (REQUIRED)

Each adversarial engine MUST have:

### Methodology Layer (Layer 4) — methodology.py

**File structure:**
```
ds-atk-XX-<name>-engine/src/atcXX/core/methodology.py
```

**Required components:**

1. **Institutions** — Elite institutions tied to the scientist's lineage
```python
INSTITUTIONS = [
    Institution(
        name="Harvard Business School",
        short_code="HBS",
        location="Boston, Massachusetts, USA",
        methodology="Porter's Five Forces framework",
        methodology_code="PORTER-FIVE-FORCES-1979",
        relevance="Key papers + why it matters",
        key_papers=["Paper 1", "Paper 2"],
        ranking_year=2025,
    ),
]
```

2. **Personalities** — Behavioral profiles (must include preferred_model and preferred_methodology)
```python
PERSONALITIES = [
    PersonalityVariant(
        name="The Porter Analyst",
        archetype="Strategic analyst",
        traits=["systematic", "analytical", "ruthless", "evidence-driven"],
        communication_style="How they speak",
        decision_speed="deliberate",
        risk_tolerance="calculated",
        preferred_model="claude-sonnet-4-20250514",  # REQUIRED
        preferred_methodology="ATC-M01",  # REQUIRED
    ),
]
```

3. **Sub-Agents** — Personality-specific sub-agents
```python
SUB_AGENTS = [
    SubAgentSpec(
        role="Five Forces Analyzer",
        purpose="Analyze industry structure",
        required_expertise=["competitive_intelligence", "market_research"],
        personality="The Porter Analyst",
        task_type="adversarial_attack",
        can_spawn_further=True,
    ),
]
```

4. **Methodologies** — Analytical frameworks
```python
METHODOLOGIES = [
    MethodologyProfile(
        code="ATC-M01",
        name="Five Forces Analysis",
        institution="Harvard Business School",
        description="Analyze industry structure",
        best_for=["competitive_intelligence", "market_research"],  # REQUIRED
        parameters={
            "threat_of_new_entrants": "high|medium|low",
            # ... more parameters
        },
    ),
]
```

5. **Model Routes** — Task-specific model routing
```python
MODEL_ROUTES = [
    ModelRoute(
        task_type="adversarial_attack",  # REQUIRED
        model="claude-sonnet-4-20250514",
        provider="anthropic",
        reason="Best for strategic analysis",
    ),
]
```

6. **Methodology Layer Class** — Must inherit from MethodologyLayerBase
```python
class CompetitiveAnalysisMethodology(MethodologyLayerBase):
    """Porter's Five Forces + Rumelt's Strategy Kernel"""

    def __init__(self):
        super().__init__(
            engine_name="DS ATC-01 Competitive Analysis",
            body_system="adversarial",
            eight_d_dimension="intellectual",
            institutions=INSTITUTIONS,
            methodologies=METHODOLOGIES,
            personalities=PERSONALITIES,
            model_routes=MODEL_ROUTES,
            version="1.0.0",
        )
```

7. **Export Functions** — the specialist engine entry points
```python
def select_methodology(situation: str, task_type: str = None) -> dict:
    """the specialist engine entry point: select appropriate methodology"""
    methodology = CompetitiveAnalysisMethodology()
    result = methodology.select_all(situation, task_type or "adversarial_attack")
    result["adversarial_context"] = {
        "attack_type": "competitive_analysis",
        "seat_count": 5,
        "primary_frame": "porter_five_forces",
        "secondary_frame": "rumelt_strategy_kernel",
    }
    return result

def get_engine_info() -> dict:
    """Return engine metadata for the specialist engine"""
    return {
        "engine_name": "DS ATC-01 Competitive Analysis",
        "ds_ecs_code": "DS-ECS-ATK-01-01-v1.0.0",
        "port": 8201,
        "body_system": "adversarial",
        "eight_d_dimension": "intellectual",
        "role": "Competitive intelligence adversarial engine",
        "scientist": "Michael Porter + Richard Rumelt",
    }
```

### Registration (REQUIRED)

Register in `/<workspace>`:
```yaml
- directory: ds-atk-01-competitive-engine
  engine_name: DS ATC-01 Competitive Analysis
  port: 8201
  scientist: Michael Porter + Richard Rumelt
  body_system: adversarial
  ds_ecs_code: DS-ECS-ATK-01-01-v1.0.0
```

## DS-ECS Naming Convention

Adversarial engines use DS-ECS-ATK prefix:
- DS-ECS-ATK-01-01-v1.0.0 (Competitive Analysis)
- DS-ECS-ATK-02-01-v1.0.0 (Regulatory Attack)
- DS-ECS-ATK-03-01-v1.0.0 (Moat Stress-Test)
- DS-ECS-ATK-04-01-v1.0.0 (Timeline Hack)
- DS-ECS-ATK-05-01-v1.0.0 (Customer Psychology Breaker)

Format: DS-ECS-ATK-<engine_number>-<version>-<minor>.<patch>

## Port Allocation

Adversarial engines use ports 8201-8205:
- 8201: Competitive Analysis
- 8202: Regulatory Attack
- 8203: Moat Stress-Test
- 8204: Timeline Hack
- 8205: Customer Psychology Breaker

## Common Adversarial Specializations

| Engine # | Scientist(s) | Domain | Primary Frame |
|----------|-------------|--------|---------------|
| ATC-01 | Michael Porter + Richard Rumelt | Competitive intelligence | Porter's Five Forces |
| ATC-02 | David Kessler | Regulatory compliance | FDA/FTC enforcement |
| ATC-03 | Warren Buffett + Charlie Munger | Moat vulnerability | Buffett's moat + Munger's lollapalooza |
| ATC-04 | Fred Brooks | Timeline feasibility | Brooks' Law + No Silver Bullet |
| ATC-05 | Daniel Kahneman + Richard Thaler | Customer psychology | Cognitive biases + Nudge economics |

See `references/adversarial-engines-catalog.md` for complete catalog of built engines.

## Methodology Layer Base Class

Critical fields from `/<workspace>`:

**MethodologyProfile:**
- `code` (required)
- `name` (required)
- `institution` (required)
- `description` (required)
- `best_for` (required) — list of task types
- `parameters` (optional)

**PersonalityVariant:**
- `name` (required)
- `archetype` (required)
- `traits` (required) — list
- `communication_style` (required)
- `decision_speed` (required)
- `risk_tolerance` (required)
- `preferred_model` (required) — model name
- `preferred_methodology` (required) — methodology code

**SubAgentSpec:**
- `role` (required)
- `purpose` (required)
- `required_expertise` (required) — list
- `personality` (required)
- `task_type` (required)
- `can_spawn_further` (optional)

**ModelRoute:**
- `task_type` (required)
- `model` (required)
- `provider` (required)
- `reason` (required)

## Execution Pattern

When engines are built, execute via direct Python invocation:
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
    'Attack situation description',
    'adversarial_attack'
)
print(json.dumps(result, indent=2))
"
```

See `references/adversarial-execution-pattern.md` for detailed execution workflow.

## Troubleshooting

**Issue:** AttributeError: 'X' object has no attribute 'to_dict()'

**Fix:** MethodologyLayerBase doesn't have to_dict(). Use select_all():
```python
methodology = EngineMethodology()
result = methodology.select_all(situation, task_type)
```

**Issue:** TypeError: PersonalityVariant.__init__() missing required arguments

**Fix:** PersonalityVariant requires `preferred_model` and `preferred_methodology` (not optional)

**Issue:** the specialist engine says "GENERALIST_REFUSED — no specialist matched"

**Fix:** Engine must be registered in ENGINE_REGISTRY.yaml and have methodology layer properly structured

**Issue:** Baseline-first gate blocking writes

**Fix:** Inspect baseline artifact first, then patch. This is a safety mechanism for critical edits.

## CRITICAL: Hardcoded-Seat Anti-Pattern (caught 2026-08-12 by 3 independent QA auditors)

The single most dangerous recurring defect in adversarial engines: a seat that
returns a **constant score regardless of input**. Three engines (ATK-01, ATK-03,
plus a hippocampus variant) shipped with seats hardcoding `score=0.5`, defeating
the entire point of an adversarial panel. An auditor cannot tell from the seat
*name* whether the computation is real — they must send **different inputs and
prove different outputs**.

**Where it hides:** Seats added late in the build as placeholders ("I'll compute
this later") that never get revisited. In ATK-01 it was Value Chain + Market
Positioning. In ATK-03 it was Munger Lollapalooza (Fisher Scuttlebutt and Lynch
Growth Moat were initially flagged but turned out to be false positives — they
respond to different input categories than the auditor tested with; see
`references/hardcoded-seat-detection.md` "Wrong-Input-Category False Positive").

**RULE: No seat may return a literal constant.** Every `SeatVerdict(score=...)`
must derive its score from the input data. If the seat is a stub, it must crash
loudly or raise NotImplementedError — never silently return 0.5.

**Verification (mandatory, not optional):** After building ANY multi-seat engine,
send ≥2 inputs that should produce different seat scores and assert the scores
differ. Example for ATK-01:
```
curl -X POST localhost:port/v1/analyze -d '{"value_chain":{"operations":0.9}}'  # VC should be ~0.1
curl -X POST localhost:port/v1/analyze -d '{"value_chain":{<all 9 activities at 0.9>}}'  # VC should be ~0.96
```
If the scores are identical, the seat is hardcoded. See
`references/hardcoded-seat-detection.md` for the full detection recipe.

## Type-Safety on Numeric Engine Inputs (caught 2026-08-12)

Adversarial engines crash when a caller passes a string where a float is expected
(e.g. `buyer_power="high"`). The fix is a defensive coercion helper applied to
**every** numeric parameter at the top of `assess_*` and `analyze`:

```python
@staticmethod
def _coerce_float(value, default=0.0):
    if value is None:
        return float(default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)
```

Call it on all numeric params up front. This applies to ALL engines, not just
adversarial — but adversarial engines are the worst offenders because they take
many free-form scoring inputs.

## Input-Ceiling Discipline (caught 2026-08-12)

Any parameter that feeds a non-linear / combinatorial calculation (component
counts, interaction matrices, O(n²) loops) MUST be clamped to a sane ceiling.
ATK-04's `component_count` with no ceiling produced nonsense output for inputs
above ~1000. Pattern: `component_count = max(0, min(1000, int(component_count)))`.

## Protocol Validation Checklist

After building adversarial engines, validate:

1. ✅ 5 ECS layers architecture documented (or built)
2. ✅ 17 methodology layers documented (or built)
3. ✅ Personality variants have preferred_model and preferred_methodology
4. ✅ Sub-agents have role, purpose, required_expertise, personality, task_type
5. ✅ Methodologies have best_for list
6. ✅ Model routes have task_type as first field
7. ✅ Engine registered in ENGINE_REGISTRY.yaml
8. ✅ Engine can be invoked via Python directly
9. ✅ select_methodology() returns adversarial_context
10. ✅ get_engine_info() returns engine metadata
11. ✅ **NO seat returns a hardcoded constant** (send 2 different inputs, assert different scores)
12. ✅ **All numeric inputs type-coerced** (engine survives `buyer_power="high"`)
13. ✅ **Combinatorial inputs clamped to ceilings** (no nonsense output at extreme values)

## References

- **Hardcoded-seat detection recipe:** `references/hardcoded-seat-detection.md` — input-differential test that catches seats returning constant scores. Run after every multi-seat build.
- Adversarial engine template: `references/adversarial-engine-template.md`
- Engine catalog: `references/adversarial-engines-catalog.md`
- Execution pattern: `references/adversarial-execution-pattern.md`
- Methodology base: `/<workspace>`
- Engine registry: `/<workspace>`
- the specialist engine router: `/<workspace>`
- Adversarial execution log (2026-07-02): See conversation context for ATC-01 attack results