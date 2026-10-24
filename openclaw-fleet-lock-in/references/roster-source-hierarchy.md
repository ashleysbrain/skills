# OpenClaw roster source hierarchy

## What this note captures
Session-level lesson: when the user says the roster is incomplete, the broader OpenClaw roster may include more than the the operator agent-facing roster. In at least one fleet-lock task, the user explicitly asked to check the inactive roster too and stressed that the work should reuse existing agents rather than recreate identities.

## Durable workflow pattern
- Start with the broadest authoritative roster available.
- Check for inactive / archived / lineage entries before concluding the fleet is small.
- Treat role assignment, skillsets, and operating brains as overlays on existing agents.
- Do not interpret a smaller dashboard roster as the full fleet unless verified.
- If the user says the fleet has "way more than 72 agents" or mentions hundreds of agents, assume roster sparsity is a source-selection problem until proven otherwise.
- When the user wants new roles or brains, map them onto existing agents first; do not recreate agents just to satisfy the new criteria.

## Common mistake to avoid
- Rebuilding from the wrong roster source and then inventing new personas to fill the gap.
- Dropping inactive lineage because it looks non-operational.
- Collapsing multiple agent inventories into one without preserving provenance.

## Deliverable cue
If the user asks for a lock-in or persona allocation, the output should clearly distinguish:
- existing agents being reused
- inactive / archived lineage retained for visibility
- any genuinely new personas proposed as separate additions
