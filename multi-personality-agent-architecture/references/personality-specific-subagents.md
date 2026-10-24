# Personality-Specific Sub-Agent Pools

**Established 2026-06-17.** User directive: sub-agents must be specific to the
personality type selected or task at hand, NOT general.

## Core Data Structures

```python
@dataclass
class SubAgentSpec:
    role: str               # e.g., "Hemodynamics Analyst"
    purpose: str            # what this sub-agent does
    required_expertise: List[str]
    personality: str        # which personality this serves (CRITICAL)
    task_type: str          # which task type this handles
    can_spawn_further: bool = False

@dataclass
class PersonalityVariant:
    name: str
    archetype: str
    traits: List[str]
    communication_style: str
    decision_speed: str       # deliberate | balanced | rapid
    risk_tolerance: str       # conservative | moderate | aggressive
    preferred_model: str
    preferred_methodology: str
    sub_agents: List[SubAgentSpec]  # 4 personality-specific sub-agents
```

## Indexing Pattern

The key insight: sub-agents are indexed by `(personality_name, task_type)` tuple,
not just by task type. This means the lead agent looks up sub-agents based on
which personality is currently active.

```python
# Build index: {(personality_name, task_type): [sub_agents]}
_sub_agent_index = {}
for p in personalities:
    for sa in p.sub_agents:
        key = (p.name, sa.task_type)
        _sub_agent_index.setdefault(key, []).append(sa)

def get_sub_agents_for_task(task_type="diagnosis"):
    """Get the 4 personality-specific sub-agents for the current task."""
    pn = _active_personality
    agents = _sub_agent_index.get((pn, task_type), [])
    # Fallback: try any personality for this task type
    if not agents:
        for (_, ttype), subs in _sub_agent_index.items():
            if ttype == task_type:
                agents = subs
                break
    return agents
```

## Standard Personality Archetypes (10 per engine)

| Archetype | Decision Speed | Risk Tolerance | Default Task |
|-----------|---------------|----------------|--------------|
| The Diagnostician | deliberate | conservative | diagnosis |
| The Emergency Responder | rapid | aggressive | emergency_response |
| The Researcher | deliberate | moderate | research_synthesis |
| The Practitioner | balanced | moderate | treatment_planning |
| The Innovator | balanced | aggressive | innovation_exploration |
| The Analyst | deliberate | conservative | monitoring |
| The Communicator | balanced | moderate | communication |
| The Strategist | balanced | moderate | optimization |
| The Specialist | deliberate | conservative | diagnosis |
| The Optimizer | balanced | aggressive | optimization |

## Scale

With 10 personalities x 4 sub-agents = 40 specialized sub-agent specs per engine.
Across 29 engines: 1,160 unique sub-agent specifications in the fleet.

## Model Routing (per sub-agent pool)

Sub-agents inherit model routing from their parent personality but can override:

| Task Type | Model | Reason |
|-----------|-------|--------|
| diagnosis | llm-vendor/glm-5.2 | Strong reasoning |
| emergency_response | google/gemini-2.5-flash | Fast inference |
| research_synthesis | llm-vendor/glm-5.2 | Deep context |
| treatment_planning | llm-vendor/glm-5.2 | Natural reasoning |
| monitoring | deepseek/deepseek-v3 | Data analysis |
| optimization | deepseek/deepseek-v3 | Numerical reasoning |
| innovation_exploration | xai/grok-4 | Creative thinking |

**NEVER use Anthropic models** for sub-agent routing.
