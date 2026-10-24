---
name: sibling-agent-runtime-persona-enforcement
description: Maintain OpenClaw live persona/runtime overlays, DB seat rows, and manifest normalization so agent brains, variation routing, and enforcement survive regeneration.
---

# OpenClaw Runtime Persona Enforcement

Use this when working on OpenClaw agent-seat runtime enforcement: adding or changing live seats, persona manifests, overlay apply scripts, DB upserts, or fleet manifest normalization.

## When to use
- A user wants an agent brain changed in the *live runtime*, not just in profile markdown.
- You are editing `live-seat-overrides-*.json`, `runtime-personas-*.json`, or the runtime apply/fix scripts.
- You need to ensure variation routing, philosophy stack, and executive guidance survive regeneration.
- You are adding a new DS-prefixed live seat or aligning a non-DS seat with DS-normalized runtime state.

## Core rule
Do not stop after patching profile docs. Runtime enforcement in this stack usually requires **four layers** to agree:
1. canonical profile / variation artifacts
2. live runtime overlay JSON
3. DB `agents` + `agent_personas` rows
4. normalized live fleet manifest regenerated from the DB

If only one layer changes, the next regeneration pass may silently undo or hide the intended behavior.

## Standard workflow
1. **Inspect current live state first**
   - Check `live-seat-overrides-*.json`
   - Check `runtime-personas-*.json`
   - Check runtime scripts such as:
     - `apply_live_runtime_overlay_*.py`
     - `fix_ds_live_fleet_manifest_*.py`
   - Query SQLite for the target seat and persona rows.

2. **Patch the runtime overlay artifacts**
   - Add/update the seat in `live-seat-overrides-*.json`.
   - Add/update all task-routed personas in `runtime-personas-*.json`.
   - Update the live routing contract markdown if the operating rule changed.

3. **Patch the regeneration script, not just the generated JSON**
   - If `apply_live_runtime_overlay_*.py` generates those files, update it too.
   - Otherwise the next rerun will overwrite the manual JSON edits.

4. **Make DB upserts resilient**
   - When adding a seat that may already exist under a normalized name, match by **code or either display-name variant** rather than display name alone.
   - Prefer: existing row lookup by `code` plus both DS-prefixed and unprefixed display names.

5. **Regenerate and re-sync**
   - Run the overlay apply script.
   - Run the live fleet manifest fixer/regenerator.

6. **Verify with direct evidence**
   - Query `agents` for the target row.
   - Query `agent_personas` counts for the target seat.
   - Check the live fleet manifest entry.
   - Check the summary counts changed as expected.

## Durable pitfalls

### Pitfall: unique-code collision when a seat already exists under a different display name
A new insert can fail with `UNIQUE constraint failed: agents.code` if the script only matches on `display_name` and the DB already has the same seat code under a DS-normalized or legacy name.

**Fix:** change the upsert lookup to search by:
- canonical `code`
- current display name
- alternate DS/non-DS display name

Do this before rerunning the apply script.

### Pitfall: normalized manifest strips custom enforcement layers
The live fleet manifest fixer may rebuild `personaLayers` from a standard canonical function and omit richer custom clauses like:
- COSMOS-first executive guidance
- every-task locked variation
- AISHA-MD routing

**Implication:** the final normalized DB/manifest may show only the standard verified layer set even though the runtime overlay contains the richer enforcement rules.

**Practice:** treat the following as the hard enforcement surfaces for specialized routing rules:
- `live-seat-overrides-*.json`
- `runtime-personas-*.json`
- runtime apply script logic
- routing contract markdown

If the richer clauses must also survive in the normalized manifest/DB text, patch the normalization layer explicitly.

## Verification checklist
- Seat exists in `agents` with expected `code`, `display_name`, `brain`, `project_mode`, `status`.
- Persona count for the seat matches expected variation count.
- Live overlay JSON contains the seat and task-tag routing.
- Runtime persona manifest contains all persona codes for the seat.
- Regenerated fleet manifest contains the expected profile/variation source files.
- Summary counts reflect the added/updated seat.

## Good output shape for the user
Report:
- what files were patched
- what commands/scripts were actually run
- created vs updated DB/persona counts
- what is enforced directly in the normalized DB/manifest vs only in the runtime overlay

## References
- `references/aisha-runtime-enforcement-2026-06-06.md` — concrete example of fixing AISHA runtime enforcement, unique-code collision, and normalization-layer caveat.
