# the specialist engine Rename — 2026-06-27

## What Happened
The the specialist engine Design Engine (:port) was renamed to **the specialist engine** to prevent collision with the "Da Vinci process" (the creative workflow: Concept -> Goethe -> Wernicke -> Bell -> Luria).

## The Problem
The agent kept claiming "running the Da Vinci process" while never actually routing through the creative organs. The name collision masked a process vacuum: "Da Vinci" could mean either the engine at :port or the creative workflow. The user identified this as the root cause of poor creative output.

## The Fix
- Engine name: the specialist engine -> the specialist engine (François Boucher, 1703-1770)
- Directory: ds-design-engine -> ds-boucher-engine
- Port: :port (unchanged)
- ECS code: DS-ECS-04.09.01-v1.0.0
- 20 files updated in your-org/the operator agent repo (commit d015706)
- Creative Cortex (:port) RETAINS the "Da Vinci" name — it IS the creative brain/DMN

## Files Changed
- ds-boucher-engine/src/design/core/engine.py — ENGINE_NAME, PORT, seed
- ds-boucher-engine/src/api/server.py — health endpoint, FastAPI title
- ds-boucher-engine/src/design/organs.py — all docstrings
- ds-boucher-engine/src/design/phi.py — module docstring
- ds-boucher-engine/src/design/core/methodology.py — engine_name, class docstring
- ds-boucher-engine/src/design/core/philosophy.py — layer header
- ds-boucher-engine/run_server.py — startup script
- ds-boucher-engine/tests/test_design_engine.py — port assertions (8094 -> 8116)
- ENGINE_REGISTRY.yaml — directory, engine_name, scientist, ecs_code
- DS-ECS-SPEC.md — engine table row
- ds-engine-registry/ecs.py — all directory references
- ds-nervous-system/body_systems.py — engine list
- docs/BRAND-DNA.md — design engine path
- docs/generate_organ_chart.py — organ chart tuple
- docs/generate-fleet-atlas.py — fleet atlas dict key

## Naming Convention Lesson
When an engine name collides with a process name:
1. Rename the ENGINE, not the process (processes are harder to rewire)
2. Choose a scientist from the same domain (Boucher = decorative arts/design production)
3. Keep the port unchanged (external references depend on it)
4. Update ALL cross-repo references in one commit (grep for directory + engine_name + scientist)
5. Update the skill library pitfall from "MUST be renamed" to "RESOLVED"
6. Add `renamed_from` field in registry for traceability
