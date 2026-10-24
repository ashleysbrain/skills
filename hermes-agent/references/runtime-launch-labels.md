# Runtime launch labels and entrypoints

Use this when building or repairing a runtime-facing launch path for an engine/agent pair.

## Naming rule
- Use the *engine/system name* in titles and labels when the document describes the capability.
- Use the *agent/persona name* only for the runtime wrapper, controller, or persona-specific doc.
- Do not let a descriptive alias replace the canonical engine name in long-lived docs.

## Launch-path rule
- If the runtime needs a single entry page, add a `START-HERE` doc.
- The launch wrapper should point to the canonical engine docs, not to a descriptive alias.
- Verify the read order explicitly in the wrapper and launch guide.

## Safe pattern
1. `SOUL.md` for identity and voice.
2. `AGENT.md` for runtime wrapper rules.
3. `START-HERE.md` for the shortest launch path.
4. Canonical engine docs (`README.md`, `process-flow.md`, etc.).

## Verification
- Check headings and labels for alias drift.
- Check the read order includes the canonical engine name.
- Check the runtime wrapper does not silently rename the system.