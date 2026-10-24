# OpenClaw runtime overlay retrofit

Use this reference when the fleet already has a live `agents.db` and partial persona infrastructure, but the runtime truth is split across DB rows, repo-local SOUL files, and stale canonical registries.

## Trigger pattern

- the live DB already exists and supports fields like `brain`, `project_mode`, or `persona_layers`
- `agent_personas` exists structurally but is empty or incomplete
- one or more target seats are missing from the DB entirely
- the canonical JSON registry is stale, mismapped, or missing a seat the user wants made live now
- the user wants system-agent philosophy routing separated from the specialist engine style advisor routing

## Retrofit sequence

1. Query the live DB first.
   - confirm the target seats exist or do not exist
   - confirm whether `agent_personas` has rows
   - inspect schema for `agents` and `agent_personas`
2. Check the runtime artifact layer.
   - variation registry files
   - SOUL/AGENT files
   - canonical seed JSON / registry files
3. If the canonical registry is stale, do not wait for a full registry rewrite.
   - create a runtime overlay artifact for the live contract
4. Mirror missing seat-local SOUL files into the live runtime repo before pointing overlays at them.
5. Create four explicit artifacts:
   - `live-seat-overrides-YYYY-MM-DD.json`
   - `live-routing-contract-YYYY-MM-DD.md`
   - `runtime-personas-YYYY-MM-DD.json`
   - deterministic loader script
6. Run the loader script against the real DB.
7. Verify with direct queries.

## Minimal artifact contract

### Seat overlay JSON
Should include, per seat:
- `id`
- `name`
- `brain`
- `role`
- `department`
- `world`
- `soulFile`
- `projectMode`
- `philosophyStack`
- `personaLayers`
- `routingRules.defaultVariation`
- `routingRules.taskTags`

### Routing contract markdown
Must explain:
- execution philosophy stack vs advisor philosophy stack
- the specialist engine distinction: coaching engine, not self-healing runtime brain
- task-tag-to-variation defaults in plain language

### Persona manifest JSON
One entry per persona row to seed:
- `agent_name`
- `persona_code`
- `persona_name`
- `persona_type`
- `domain_focus`
- `authorized_tools`
- `status`

### Loader script
Must do deterministic upserts:
- upsert seats into `agents`
- upsert personas into `agent_personas`
- preserve rerunnability
- print created/updated counts

## Verification queries

After applying, verify at least:

```sql
SELECT display_name, role, brain, project_mode, persona_layers
FROM agents
WHERE display_name IN ('COSMOS', 'FORGE', 'the specialist engine');
```

```sql
SELECT a.display_name, COUNT(*) AS persona_count
FROM agent_personas ap
JOIN agents a ON a.id = ap.agent_id
WHERE a.display_name IN ('COSMOS', 'FORGE', 'the specialist engine')
GROUP BY a.display_name;
```

## Concrete lessons from the 2026-06-06 run

- The live DB had 76 agents and zero persona rows before the retrofit.
- COSMOS existed, but FORGE and the specialist engine were not registered as live seats in the DB.
- the specialist engine needed to be made live as a dedicated coaching seat with `project_mode=COACHING` and advisor philosophy layers.
- The runtime needed a hard split between:
  - execution philosophy stack: COSMOS, FORGE
  - advisor philosophy stack: the specialist engine
- Local SOUL files had to be mirrored into the OpenClaw workspace before the overlay paths were valid.
- The successful implementation created 2 seats, updated 1 seat, and inserted 30 persona rows.
- A later fleet-normalization pass exposed a second boundary rule: the **live fleet manifest** must be built from the DB-backed roster, not from the union of `codes/` files plus DS-prefixed aliases.
- DS-prefixed alias copies are useful for outward-facing naming consistency, but they must be treated as file aliases, not as new agents.
- For sub-100 live-fleet work, the trustworthy artifact is the DB-backed manifest (for example `ds-live-fleet-profile-manifest-YYYY-MM-DD.json`), while broader code-library coverage can exceed the live roster and should be labeled separately.

## Pitfall

Do not claim the system is live just because markdown artifacts exist.
A fleet retrofit is only actually live when:
- the overlay files exist,
- the seat files resolve,
- the DB rows exist,
- and direct SQL verification confirms the expected seats and persona counts.
