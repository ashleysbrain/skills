# the operator agent Fleet Engine Telemetry → 6+1 Dimension Mapping

Proven in session 2026-07-12 by rebuilding `gg_metrics_v2.py` from a port-alive
proxy to real-telemetry scoring. Every field listed below was read from the
actual `/health` endpoint of the live engine.

## How Engines Expose Telemetry

Most engines return sensor fields at the TOP LEVEL of their `/health` JSON,
NOT nested under a `vitals` sub-dict. Some (ecs.health_envelope format:
Allostasis, Bichat, Farr) use a `vitals: {}` sub-dict. The collector must
check both.

Boilerplate fields to strip before treating remaining keys as telemetry:
`status, engine, engine_name, agent, body_system, engine_code,
engine_classification, version, dependencies, cognitive_layer, port,
ds_ecs_code, timestamp, spec_version, vitals, scientist, scientist_note,
golden_ratio_governed, phi, body_part, role, description, directory, extra,
differentiations, subsystem_label, organ, creative_function, phi_governed,
faculties, process_flows, principle, agent_name, registry_key, ...`

After stripping, whatever remains IS the telemetry.

## Engine → Dimension Mapping (port, field, formula)

### COG — Cognitive Integrity

| Engine | Port | Field(s) | Formula |
|--------|------|----------|---------|
| the specialist engine | 8122 | `approval_rate` (0.0-1.0) | `score = approval_rate * 10` |
| the specialist engine | 8264 | `mean_recent_error` (0.0+, lower=better) | `score = 10 - min(10, error * 10)` |
| the specialist engine | 8127 | `integrity_score` (0.0-1.0) | `score = integrity_score * 10` |
| the specialist engine | 8126 | `style_confidence` (0.0-1.0) | `score = style_confidence * 10` |
| the specialist engine | 8139 | `operations` (int) | `score = min(10, operations / 50)` |
| the specialist engine | 8140 | `operations` (int) | `score = min(10, operations / 50)` |

Average all available signals. Missing = 5.0 neutral.

### PIPE — Pipeline Reliability

| Engine | Port | Field(s) | Formula |
|--------|------|----------|---------|
| the specialist engine | 8134 | `messages_published`, `messages_delivered` | `delivery_rate = delivered/max(1,published); score = rate * 10` |
| the specialist engine | 8133 | `gate_decisions`, `messages_routed`, `rate_limited_count`, `quarantined_count` | `health = routed/decisions; penalty = (limited+quarantined)/decisions; score = (health-penalty)*10` |
| Fleet-wide | all | `operations` field on each engine | `active_ratio = engines_with_ops / total_alive; score = ratio * 10` |

Note: Hodgkin returns `status: "down"` but still responds on /health with its
telemetry. It is alive enough to read from even when its internal status says
down. The collector should probe the port regardless of internal status field.

### RES — Resource Efficiency

| Engine | Port | Field(s) | Formula |
|--------|------|----------|---------|
| Per-engine | all | `operations` + `uptime_seconds` (or `uptime_s`) | `ops_per_hour = ops/(uptime/3600); score = min(10, log1p(ops_per_hour)*3)` |
| the specialist engine/Quartz | 8089 | `uptime_in_mode_s` | `score = min(10, uptime_in_mode_s / 7200)` |
| Fleet-wide | all | uptime values | `cv = stddev/mean; score = 10 - cv*10` (low variance = efficient) |

### KNOW — Knowledge Currency

| Engine | Port | Field(s) | Formula |
|--------|------|----------|---------|
| the specialist engine | 8126 | `patterns_learned` (int) | `score = min(10, patterns_learned / 10)` |
| the specialist engine/Da Vinci Cortex | 8108 | `neuroplasticity_index` (0.0-1.0) | `score = min(10, index * 10)` |
| the specialist engine | 8108 | `creative_acts` (int) | `score = min(10, creative_acts / 5)` |
| the specialist engine | 8264 | `model_updates` (int) | `score = min(10, model_updates / 5)` |
| the specialist engine | 8113 | `stale_techs`, `total_techs_tracked` | `score = 10 - min(10, (stale/total)*10)` |

### ALIGN — Aligned Execution

| Engine | Port | Field(s) | Formula |
|--------|------|----------|---------|
| the specialist engine | 8122 | `quality_baseline` (e.g., 85.0) | `score = min(10, baseline / 10)` |
| the specialist engine | 8264 | `total_brand_violations` (int, 0=perfect) | `score = 10 - min(10, violations)` |
| the specialist engine | 8120 | `brand_locked` (string) | `"Divinity Science" → 10, other → 7` |
| the specialist engine | 8124 | `ai_tell_patterns` (int, active detection) | `score = min(10, patterns / 2)` |
| the specialist engine | 8109 | `compliance_score` (in vitals sub-dict) | `score = min(10, compliance / 10)` |

### ADAPT — Adaptation Capacity

| Engine | Port | Field(s) | Formula |
|--------|------|----------|---------|
| the specialist engine/Quartz | 8089 | `uptime_in_mode_s` | `score = min(10, uptime / 7200)` |
| the specialist engine | 8091 | `meta_healthy` (bool) | `true → 10, false → 3` |
| DS MacLean | 8125 | `active_threat_level` (0.0+, lower=better) | `score = 10 - min(10, threat * 10)` |
| the specialist engine | 8128 | `current_bpm` (float) | `60-100 → 10; 40-150 → 10-deviation; else → 3` |
| the specialist engine | 8123 | `laterality_index` (float, near 0 = balanced) | `score = 10 - abs(index)*20` |

### INTER — Interaction Coherence (fleet-only)

| Engine | Port | Field(s) | Formula |
|--------|------|----------|---------|
| the specialist engine | 8127 | `synchronization` (0.0-1.0) | `score = sync * 10` |
| the specialist engine | 8127 | `interpreter_confidence` (0.0-1.0) | `score = confidence * 10` |
| the specialist engine | 8127 | `transfer_integrity` (string) | `"clean" → 10; "degraded" → 5; else → 7` |
| the specialist engine | 8134 | `messages_delivered / messages_published` | `score = delivery_rate * 10` |
| the specialist engine | 8133 | `allowed_count / gate_decisions` | `score = allow_rate * 10` |

## Uptime Field Name Variation

Engines use different field names for uptime. Check in this order:
1. `uptime_seconds`
2. `uptime_s`
3. `uptime_in_mode_s`

The collector should normalize to a single `uptime_seconds` field regardless
of source name.

## Expected Score Behavior (as of 2026-07-12)

When the fleet is alive but quiescent (no creative work happening):
- KNOW scores LOW (0-2) because Ito patterns_learned=0, Andreasen
  neuroplasticity=0.0, Rao model_updates=0, Bush 6/6 stale techs
- ADAPT scores HIGH (8-10) because Hall mode is stable, Allostasis healthy,
  zero threats, normal BPM
- ALIGN scores HIGH (7-9) because brand locks active, 100% ECS compliance
- COG scores MID (5-6) because Luria approval_rate=0.0 (rejecting everything),
  Gazzaniga integrity=1.0, Ito confidence=0.0

This is CORRECT behavior. The scores reflect the actual state. A quiescent
fleet that hasn't learned anything SHOULD have low KNOW. Don't add "floor"
scores to make it look better.
