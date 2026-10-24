# the operator agent Repo Structure — Canonical Artifact Placement

The the operator agent repo is the organism's home. ALL organism architecture artifacts
go here, not in your-workspace panel directories or root.

## Location

`/<workspace> operator agent/`
Remote: `github.com/your-org/the operator agent.git`

## Directory Layout (existing)

| Directory | Purpose |
|-----------|---------|
| `organism/` | Organism infrastructure (agents.yaml, process flow code, build queue) |
| `docs/` | Architecture docs (PHYSICS-THREAD.md, ECS-THREAD.md, neuro specs) |
| `ds-*-engine/` | Individual engine source directories (ds-tawara-engine, ds-lichtheim, etc.) |
| `ecs.py` | Canonical ECS engine registry (source of truth, 48+ engines) |
| `DS-ECS-SPEC.md` | ECS specification document |
| `REGISTRY.yaml` | Human-readable registry dump from ecs.py |
| `organism/agents.yaml` | Agent interface contracts (switch-brain targets) |
| `kanban/` | Project registry and kanban artifacts |
| `knowledge-canon/` | Curriculum and institutional knowledge |
| `scripts/` | Operational scripts |
| `marketing-sprint/` | Marketing campaign artifacts |
| `opendesign/` | Design system outputs |
| `8D360AI/` | AI health scoring framework |
| `8D360-Human/` | Human health scoring framework |
| `ds-wave-*-panel-private/` | Advisory panel notes (review outputs only, NOT organism artifacts) |

## Placement Rules

1. **Engine source code** → `ds-<scientist>-engine/src/` inside the operator agent
2. **Organism specs** (SOFTWARE-FACTORY, REPRODUCTIVE-PROCESS-FLOWS, etc.) → `docs/` or `organism/` inside the operator agent
3. **Process flow code** (the operator agent-production-flow.py, ilf_conduct.py, etc.) → `organism/` inside the operator agent
4. **ECS registry** → always `ecs.py` at the operator agent root (source of truth)
5. **Engine verification tools** (engine_depth_gate.py) → `scripts/` inside the operator agent if organism-specific, or keep in your-workspace root if workspace-level
6. **Advisory panel review notes** → may stay in panel directories, but the artifacts they PRODUCE go to the operator agent

## Common Mistake Pattern

Session creates organism spec in:
`your-workspace/ds-wave-gamification-advisory-panel-private/SOFTWARE-FACTORY-DESIGN.md`

Correct location:
`your-workspace/your-org/the operator agent/organism/SOFTWARE-FACTORY-DESIGN.md`
or
`your-workspace/your-org/the operator agent/docs/SOFTWARE-FACTORY-DESIGN.md`

## Other Repos in your-org Org

- `your-org/8d-sleep` — the 8D Sleep PWA product
- `your-org/ds-wave-coaching-engine` — coaching engine standalone

These are product repos. The the operator agent repo is the organism itself.
