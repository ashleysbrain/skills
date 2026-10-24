# Health-Engine Project Modes

Session note: the Qubit AI health engine should use project-mode overlays on the existing rostered agents, not a brand-new permanent persona panel.

## Core correction
- **Base persona stays stable**
- **Project mode is additive only**
- **Do not recreate agents that already exist**
- **Resolve the active mode before dispatch**

## For Qubit health-engine work
Use existing health/scoring agents as the base layer, then add a project lens for the mission:
- health orchestration
- deterministic scoring
- anomaly detection
- self-healing remediation
- boundary / firewall enforcement

## Practical rule
If the user says "project mode", "lens", or "mode" in this lane:
1. find the approved rostered agent
2. attach the project overlay
3. emit mode metadata in the dispatch record
4. keep the base persona unchanged

## Common failure to avoid
- inventing a new five-brain panel when the right move is to reuse the current roster with project overlays
- drifting from scoring-engine work into persona-panel design
- collapsing base/task/project into one generic identity
