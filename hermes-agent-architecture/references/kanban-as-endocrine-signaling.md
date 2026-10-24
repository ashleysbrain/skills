# Kanban as Endocrine/Neural Signaling

Design pattern: Kanban board = circulatory system for hormonal/neural signals. Tasks = hormones. Profiles = target organs with specific receptors.

## Signaling Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     ORGANISM (the operator agent Fleet)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    Kanban Tasks    ┌──────────────────────┐  │
│  │  ORCHESTRATOR │ ─────────────────▶ │   TARGET PROFILES    │  │
│  │ (Hypothalamus)│  (Hormones/        │  (Target Organs)     │  │
│  │               │   Neurotransmitters)│                      │  │
│  └──────────────┘                    └──────────────────────┘  │
│        │                                      ▲                  │
│        │ Telegram/External                    │ Kanban_complete  │
│        ▼                                      │ (Feedback)       │
│  ┌──────────────┐                             │                  │
│  │   EXTERNAL    │                             │                  │
│  │   STIMULI     │                             │                  │
│  └──────────────┘                             │                  │
│                                               │                  │
└───────────────────────────────────────────────│──────────────────┘
                                                │
                    ┌───────────────────────────┼───────────────────┐
                    │                           │                   │
                    ▼                           ▼                   ▼
            ┌───────────────┐           ┌───────────────┐   ┌───────────────┐
            │     CNS       │           │  AUTONOMIC    │   │ ENDOCRINE/    │
            │   (Wave)      │           │  (Quartz)     │   │ IMMUNE        │
            │               │           │               │   │ (Seed/Allo)   │
            │ Receptors:    │           │ Receptors:    │   │               │
            │ coaching,     │           │ task_reg,     │   │ Receptors:    │
            │ mastermind,   │           │ pid_control,  │   │ surveillance, │
            │ resonance     │           │ lattice       │   │ diagnosis,    │
            └───────────────┘           └───────────────┘   │ growth        │
                                                               └───────────────┘
```

## Task as Hormone: Structure

```json
{
  "task_id": "t_a1b2c3d4",
  "title": "Coach sleep optimization via Physical→Emotional coupling",
  "assignee": "cns",
  "body": "User reports Physical=3.2, Emotional=4.1. Run Resonance Core frequency match. Impedance match to low energy. Output coaching protocol.",
  "parents": [],
  "metadata": {
    "hormone_type": "coaching_request",
    "target_receptor": "resonance_core",
    "priority": "high",
    "source": "telegram_user",
    "signal_strength": 0.8
  }
}
```

## Hormone Types (Task Categories)

| Hormone Type | Kanban Assignee | Receptor (Skill) | Physiological Analog |
|---|---|---|---|
| `coaching_request` | `cns` | `resonance_core`, `mastermind_core` | Neurotransmitter (dopamine/serotonin) |
| `regulation_task` | `autonomic` | `pid_control`, `lattice` | Autonomic reflex (baroreceptor) |
| `surveillance_scan` | `endocrine-immune` | `surveillance`, `diagnosis` | Immune patrol (T-cell) |
| `growth_signal` | `endocrine-immune` | `avrami_jmak`, `landau_phase` | Growth hormone / cytokine |
| `transport_sync` | `circulatory-skeletal` | `fabric`, `registry`, `transport` | Blood flow / lymph |
| `spawn_command` | `orchestrator` → FORGE/ARBITER | `talent_gate` | Stem cell differentiation signal |

## Receptor Expression (Skills as Receptors)

Each profile **expresses specific receptors** (skills) that determine which hormones it responds to:

```yaml
# CNS Profile receptors
receptors:
  - coaching_request      → kanban-orchestrator, ds-wave-coaching
  - mastermind_session    → kanban-orchestrator
  - resonance_analysis    → ds-wave-coaching

# Autonomic Profile receptors  
receptors:
  - regulation_task       → kanban-worker, quartz-lattice
  - pid_adjustment        → quartz-lattice
  - lattice_maintenance   → quartz-lattice

# Endocrine-Immune Profile receptors
receptors:
  - surveillance_scan     → sentinel-compliance-sweep
  - diagnosis_task        → sentinel-compliance-sweep
  - growth_signal         → aisha-md-health-scoring-cron-execution
  - intervention_command  → aisha-md-health-orchestration

# Circulatory-Skeletal Profile receptors
receptors:
  - transport_sync        → sibling-agent-fleet-analytics-sync
  - registry_update       → hermes-agent
  - genotype_registration → hermes-agent
```

## Signal Transduction: Task → Execution → Feedback

```
1. ORCHESTRATOR receives stimulus (Telegram message)
   │
   ▼
2. Decomposes into hormone signals (Kanban tasks with assignee=profile)
   │
   ▼
3. Kanban dispatcher delivers to target profile's inbox
   │
   ▼
4. Target profile WORKER spawns (expresses receptor/skill)
   │
   ▼
5. Worker executes: skill handles hormone → cellular response
   │
   ▼
6. Worker completes: kanban_complete(metadata={feedback_signal})
   │
   ▼
7. Feedback hormone circulates back → ORCHESTRATOR updates task graph
   │
   ▼
8. Homeostasis achieved or new hormones released
```

## Kanban Complete Metadata as Feedback Hormones

```python
kanban_complete(
    summary="Resonance coaching delivered: Physical 3.2→5.1 projected via 0.7 coupling to Emotional",
    metadata={
        "feedback_hormone": "coaching_response",
        "target_receptor": "orchestrator.task_graph",
        "signal_strength": 0.85,
        "coupling_effects": {
            "emotional": 0.7,
            "intellectual": 0.5
        },
        "homeostasis_restored": True,
        "next_signal": "monitor_emotional_24h"
    }
)
```

## Dependency Chains = Hormonal Cascades

```
CRH (orchestrator) → ACTH (cns) → Cortisol (endocrine-immune) → Glucose (circulatory)
     │                   │                    │                    │
  Kanban:             Kanban:              Kanban:              Kanban:
  create_task         create_task          create_task          create_task
  (parents=[])        (parents=[CRH])     (parents=[ACTH])     (parents=[Cortisol])
```

## Pitfalls

| Pitfall | Physiological Analog | Fix |
|---|---|---|
| Task without `assignee` | Hormone with no receptor | Always specify `assignee=<profile>` |
| Task without `parents=` | Hormone cascade without precursor | Link true dependencies via `parents=[task_ids]` |
| Multiple profiles handling same task | Receptor cross-reactivity (autoimmunity) | One assignee per task; use `kanban_link` for coordination |
| Orchestrator doing execution | Hypothalamus secreting insulin | Orchestrator ONLY decomposes/routes; workers execute |
| No `kanban_complete` feedback | Endocrine feedback loop broken | Every task must complete with feedback metadata |
| Shared Kanban board without tenant | Systemic vs local hormone confusion | Use `HERMES_TENANT` for namespace isolation |

## Verification Checklist

- [ ] Orchestrator creates Kanban tasks with correct `assignee` per body system
- [ ] Each profile has skills matching its receptor expression table
- [ ] Kanban tasks include `metadata.hormone_type` for routing visibility
- [ ] `kanban_complete` includes feedback hormone metadata
- [ ] Dependency chains use `parents=` not prose
- [ ] No cross-profile task execution (orchestrator doesn't coach, CNS doesn't surveil)
- [ ] Morphogen gradients mirror Kanban signal flow for organism-wide state