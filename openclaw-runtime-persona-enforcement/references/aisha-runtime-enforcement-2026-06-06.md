# AISHA Runtime Enforcement Example — 2026-06-06

## What changed
A live OpenClaw runtime enforcement pass added `DS AISHA` as an active runtime seat with:
- execution philosophy stack
- task-based variation routing
- COSMOS-first executive guidance
- verified linkage to `AISHA-profile.md` and `AISHA-10-variations.md`

## Files touched
- `intel/agents/runtime/live-seat-overrides-2026-06-06.json`
- `intel/agents/runtime/runtime-personas-2026-06-06.json`
- `intel/agents/runtime/live-routing-contract-2026-06-06.md`
- `intel/agents/runtime/apply_live_runtime_overlay_2026_06_06.py`
- generated/verified again through `fix_ds_live_fleet_manifest_2026_06_06.py`

## Durable lessons

### 1) Patch the generator, not just the generated files
Manual edits to the runtime JSON are not enough when `apply_live_runtime_overlay_*.py` rewrites them. The generator must be patched in the same session or the change will be lost.

### 2) Upsert by code plus normalized display names
The apply script initially failed because it tried to insert a seat whose code already existed in a differently normalized runtime state. The durable fix was to make the seat lookup search by:
- `code`
- current display name
- alternate DS-prefixed / unprefixed display name

This avoids `UNIQUE constraint failed: agents.code` during reruns.

### 3) The manifest fixer can flatten richer routing clauses
`fix_ds_live_fleet_manifest_*.py` reconstructs `personaLayers` from a standard canonical function. That means highly specific runtime enforcement clauses may not survive into the normalized fleet manifest or DB text unless the fixer is also extended.

Examples of clauses that may be lost if only stored in overlay-specific layers:
- executive-guidance ordering
- every-task credential/variation requirements
- subagent routing annotations

### 4) Treat these as the real enforcement surfaces
For specialized routing behavior, the most reliable live surfaces are:
- seat overlay JSON
- runtime persona manifest
- apply script logic
- routing contract markdown

The normalized fleet manifest is still important for visibility and verification, but it may not carry all overlay-specific semantics unless explicitly taught to.

## Verification pattern used successfully
- Run overlay apply script.
- Run manifest fixer/regenerator.
- Query `agents` for the seat row.
- Query `agent_personas` count for the seat.
- Confirm profile/variation source files appear in the fleet manifest.
- Confirm fleet summary counts changed as expected.

## Concrete outcomes from this session
- runtime apply completed after the upsert fix
- `created_agents: 1`
- `updated_agents: 3`
- `created_personas: 10`
- `updated_personas: 30`
- live fleet count increased from 78 to 79
- execution stack count increased from 12 to 13
