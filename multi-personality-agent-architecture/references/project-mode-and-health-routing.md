# Project Mode + Health Routing Notes

Session-derived implementation notes for multi-personality / multi-mode agents.

## What changed in practice
- The source generator must emit `personaLayers` and `modeMetadata` for every agent entry.
- Project mode is an **overlay**, not a new permanent identity.
- Dispatch should resolve the active brain/mode **before** work starts.
- Task routing should remain roster-first: use the approved agent roster before inventing a new persona.

## Dispatch semantics
- `base` = stable default persona
- `task` = short-lived execution lens for a bounded job
- `project` = mission-scoped overlay tied to an ongoing initiative

## CRITICAL: Health Engine ≠ Persona Panel

When the user asks for the "health engine", "QAI health engine", "self-healing health engine",
or any request involving behavior/telemetry-based scoring, anomaly detection, guardrails, or
self-healing — this is a **WELLNESS SCORING ENGINE**, not a persona panel design task.

**DO NOT:**
- Design agent personas, brain architectures, or personality panels
- Route to multi-personality panel assembly patterns
- Substitute agent-brain architecture for scoring-engine architecture

**DO:**
- Focus on behavioral telemetry pipelines (objective signals)
- Build deterministic scoring with algorithm integrity checks
- Implement anomaly/drift detection on dimension scores
- Add self-healing guardrails (auto-correction, not persona shifts)
- Separate "agent health" from "user satisfaction" rigorously
- Treat self-assessment as weak signal only
- Route to: `proprietary-twc-scoring`, `health-scoring-daily-pipeline`, `qubit-gr-8d360-scoring-pipeline`, `aisha-md-health-orchestration`

## Health-engine design note

For a self-healing agent health engine, keep scoring grounded in **behavioral evidence**, not self-report.

Recommended rails:
- external telemetry first
- deterministic checks for algorithm integrity
- explicit drift/anomaly detection
- separate "agent health" from "user satisfaction"
- treat self-assessment as weak signal only

## Panel / persona expectations
When the user asks for a panel before any summary:
- show the roster and mode assignment first
- include full persona credentials, not partial profiles
- stop before research/synthesis until the user approves the lineup

## Verification cues
A correct implementation should be able to answer:
- Which agent persona handled the task?
- Which mode was active?
- Was the task routed by roster or improvised?
- Did the health check rely on behavior rather than self-report?

## Practical follow-up
If the project uses JSON roster outputs, verify every entry contains:
- `personaLayers`
- `modeMetadata`
- a clear active mode label (`base` / `task` / `project`)
