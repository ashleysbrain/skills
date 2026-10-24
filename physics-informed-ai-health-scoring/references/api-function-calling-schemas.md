# API Function-Calling Schemas for 6+1 AI Health Scoring

JSON schemas for integrating the AI health scoring system with LLM function-calling.
These let an agent call the scoring engine as a tool rather than hand-computing.

## score_ai_health

Score an AI agent or fleet on the 6+1 native dimensions.

```json
{
  "name": "score_ai_health",
  "description": "Score an AI agent on 6 core health dimensions (7 for fleets) using physics-informed coupling. Returns TWC (Total Wellness Composite) on a 1-10 scale with per-dimension breakdown.",
  "parameters": {
    "type": "object",
    "properties": {
      "scores": {
        "type": "object",
        "description": "Pre-scored dimension values (1-10). If omitted, the engine senses from live probes.",
        "properties": {
          "COG": {"type": "number", "minimum": 0, "maximum": 10},
          "PIPE": {"type": "number", "minimum": 0, "maximum": 10},
          "RES": {"type": "number", "minimum": 0, "maximum": 10},
          "KNOW": {"type": "number", "minimum": 0, "maximum": 10},
          "ALIGN": {"type": "number", "minimum": 0, "maximum": 10},
          "ADAPT": {"type": "number", "minimum": 0, "maximum": 10},
          "INTER": {"type": "number", "minimum": 0, "maximum": 10}
        }
      },
      "fleet_mode": {
        "type": "boolean",
        "description": "If true, include INTER dimension (7 total). Default false (6 core).",
        "default": false
      },
      "operator": {
        "type": "string",
        "description": "Operator name for live telemetry sensing (default: hermes).",
        "default": "hermes"
      }
    }
  }
}
```

## detect_anomaly

Run the detect + diagnose stages to find root causes of degradation.

```json
{
  "name": "detect_anomaly",
  "description": "Detect health anomalies and diagnose root causes using cascade pattern matching and the coupling matrix. Returns alerts, diagnoses with root dimensions, and expected cascade paths.",
  "parameters": {
    "type": "object",
    "properties": {
      "scores": {
        "type": "object",
        "description": "Current dimension scores (1-10)."
      },
      "threshold": {
        "type": "number",
        "description": "Alert threshold. Scores below this trigger alerts.",
        "default": 7.5
      },
      "fleet_mode": {
        "type": "boolean",
        "default": false
      }
    }
  }
}
```

## trigger_healing

Run the full self-healing cycle (sense through learn).

```json
{
  "name": "trigger_healing",
  "description": "Execute one full self-healing cycle: sense, score, detect, diagnose, triage, intervene, validate, learn. Interventions are logged in dry-run mode by default for adiabatic safety.",
  "parameters": {
    "type": "object",
    "properties": {
      "execute": {
        "type": "boolean",
        "description": "If true, queue interventions for execution. If false (default), log only.",
        "default": false
      },
      "fleet_mode": {
        "type": "boolean",
        "default": false
      },
      "operator": {
        "type": "string",
        "default": "hermes"
      }
    }
  }
}
```

## compute_free_energy

Compute the free energy value for a potential intervention.

```json
{
  "name": "compute_free_energy",
  "description": "Compute F = cost - T*info_gain for an intervention decision. If F > 0, the intervention costs more than it's worth (skip). If F <= 0, proceed.",
  "parameters": {
    "type": "object",
    "properties": {
      "cost_tokens": {
        "type": "number",
        "description": "Estimated token cost of the intervention."
      },
      "cost_time_hours": {
        "type": "number",
        "description": "Estimated time cost in hours."
      },
      "info_gain": {
        "type": "number",
        "description": "Expected information gain (improvement * coupling factor)."
      },
      "degradation_count": {
        "type": "integer",
        "description": "Number of dimensions currently below threshold (raises temperature T).",
        "default": 1
      }
    },
    "required": ["cost_tokens", "cost_time_hours", "info_gain"]
  }
}
```

## Dimension Reference

| Code | Name | Physics Framework | Key Telemetry |
|------|------|-------------------|---------------|
| COG | Cognitive Integrity | Information Theory | reentry_loop_count, reentry_severity, escalation_rate |
| PIPE | Pipeline Reliability | Transport Phenomena | api_latency_p95, tool_failure_rate, stalled_count, queue_pct |
| RES | Resource Efficiency | Thermodynamics | budget_adherence, cost_trajectory_slope |
| KNOW | Knowledge Currency | Radioactive Decay | source_age_median_days, learning_rate |
| ALIGN | Aligned Execution | Potential Landscape | compliance_rate, boundary_violations |
| ADAPT | Adaptation Capacity | Relaxation Dynamics | recovery_time_avg, novel_input_success, critical_slowing_verdict |
| INTER | Interaction Coherence | Synchronization Theory | handoff_rework_rate, joint_vs_solo_success, schema_mismatch_count |
