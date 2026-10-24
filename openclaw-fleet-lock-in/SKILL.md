---
name: sibling-agent-fleet-lock-in
description: Lock OpenClaw fleet work to the full target-fleet source, preserve existing agents, include inactive lineage, and categorize existing agents without recreating identities.
version: 1.0.0
author: the operator agent Agent
license: MIT
---

# OpenClaw fleet lock-in

Use this skill when the user asks to work on the OpenClaw roster, fleet, or persona/agent organization.

## Canonical source
- Treat the full **target-fleet** / OpenClaw roster as the canonical baseline when the user asks for "all agents" or says the visible roster is incomplete.
- When the roster is locked for an active task, record the canonical artifact path in `<agent-home>/.session-state.json` and keep subsequent edits on that same path unless the user explicitly authorizes a new canonical deliverable.
- Do **not** assume a the operator agent-facing roster is exhaustive if a broader OpenClaw roster, inactive roster, archived roster, or lineage file exists.
- When the user specifically says "check the inactive roster too" or "look at the sibling-agent roster, not just the operator agent," expand the source set immediately and verify both active and inactive pools before drawing conclusions.
- Include **active**, **inactive**, **archived**, and **lineage** entries when the source set contains them.
- Do not silently narrow the scope to a smaller dashboard-only or active-only roster.
- See `references/roster-source-hierarchy.md` for the common source-ordering pattern and a session note on roster scope errors.

## Overlay vs identity
- Treat requested "skillsets," "roles," "brains," and "operating criteria" as overlays on existing agents unless the user explicitly asks for a new persona identity.
- Reuse the existing agent pool first; enrich the roster rather than cloning it.
- If a new identity is unavoidable, call that out explicitly and separate it from the preserved roster.

## Core rule
- **Reuse existing agents. Do not recreate identities by default.**
- The task is to **revise, categorize, and enrich** existing agents with skillsets, operating roles, brains, and lane assignments.
- If a new identity is unavoidable, call that out explicitly and separate it from the preserved roster.

## Organization pattern
When rebuilding or presenting the fleet:
1. Start from the full roster inventory.
2. Separate current active agents from inactive/archived lineage.
3. Split the presentation into distinct taxonomies when needed:
   - **real roster agents** (existing OpenClaw agents)
   - **operational systems / engine layers** (brains, wrappers, orchestration layers, health or persona engines)
   - **board advisors / coaching-engine personas**
4. Group real agents by world / domain / family / role.
5. Add skillset overlays, operating brains, and category labels to the existing agents.
6. Keep lineage notes so it is clear what already exists versus what is being proposed.

## Source verification for roster corrections
- Verify the roster against the real OpenClaw source of record (for example the actual fleet DB or canonical exported roster), not only a the operator agent-facing subset.
- Treat cron jobs, wrappers, scheduled check-ins, and automation labels as **non-agent operational artifacts** unless the source of record marks them as agents.
- If the user is correcting headcount (for example "we have way more than 72 agents"), explicitly compare the visible roster against the broader OpenClaw source before editing the deliverable.
- When rebuilding a PDF/HTML roster artifact, preserve existing agents and enrich them with new skillsets, roles, and brains rather than manufacturing replacement personas.
- See `references/roster-taxonomy-and-source-correction.md` for the session note covering the OpenClaw-vs-the operator agent scope mistake and the fix.

## Editing policy
- Prefer **patching existing artifacts** over creating new versions or duplicate files.
- If the user says "don't recreate files" or "lock this in," treat that as a hard preference for in-place updates and stable canonical outputs.
- Preserve the user's requested terminology and category names.
- Keep agent identities fixed: categories, advisory panels, operating rules, and skill overlays may change, but names should not be rewritten unless the user explicitly asks.
- When the user requests a surgical edit, modify the source artifact in place and rebuild the same deliverable; do not substitute a condensed summary for the full profile pack.
- If the user names a stray label to remove, delete only that exact label and verify the source before editing so the underlying agent identity is untouched.
- For OpenClaw fleet work, maintain the full elite credential stack and variation overlays in the deliverable; do not compress them into a lock-in summary.

## Lock-state persistence
When this skill locks a canonical artifact:
1. Write the lock state (filename + path) to MEMORY.md so it survives context compression.
2. Before any fleet-related artifact generation, check MEMORY.md for a locked artifact.
3. If a locked artifact exists, **always patch it in place — never create a new parallel file.**
4. If the user explicitly asks for a new file, confirm and note the exception in memory.

## Anti-proliferation rule
- Do NOT generate multiple versions of the same fleet artifact in one session (e.g., lock-in.pdf, surgical-v1.pdf, surgical-v2.pdf, elite-phd-ds-wave.pdf).
- If the canonical artifact already exists and has been sent to the user, PATCH it in place. The file count for any single fleet deliverable should be 1, not 8.
- If you catch yourself about to write a new filename variant, STOP. Patch the existing one instead.
- Exception: the user explicitly asks for a separate deliverable (e.g., "split by fleet"). In that case, still patch each sub-file in place on subsequent edits.

## Verification
Before delivering:
- confirm the roster includes the intended full scope
- confirm inactive lineage is visible if requested
- confirm existing agents were not duplicated as new identities
- confirm the categorization matches the user’s discussion and role criteria

## Common failure modes
- Using only the active roster and missing inactive lineage
- Treating scheduled jobs or wrappers as agents
- Creating new personas when the user asked to reuse existing ones
- Delivering a condensed lock-in / categorization summary when the user asked for the full persona profiles with elite credential stacks and operating rules
- Producing multiple alternate roster files instead of locking one canonical fleet

## Session-specific lessons
- See `references/elite-credential-pack-lesson.md` for the reminder that the full persona profile pack, not the condensed summary, is the correct deliverable when the user calls out missing elite credentials.
