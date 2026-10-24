# Launch surface and entrypoint notes for the specialist engine

Session-derived launch pattern for the coaching engine:

- Treat `agents/ds-wave/SOUL.md` as the identity/behavior file.
- Treat `agents/ds-wave/AGENT.md` as the runtime-facing wrapper.
- Provide a dedicated launch checklist file when the user needs to *launch* the coaching agent, not merely document it.
- A clean launch path should be explicit and linear; do not force the reader to infer startup order from scattered docs.
- The launch path is coaching-only and must not pull in the healing engine docs.

Recommended launch order:
1. `agents/ds-wave/SOUL.md`
2. `agents/ds-wave/AGENT.md`
3. `agents/ds-wave/LAUNCH.md` (or equivalent launch checklist)
4. `docs/your-org/coaching-engine/README.md`
5. `docs/your-org/coaching-engine/process-flow.md`

Pitfall:
- If the user says they need to "launch" the coaching agent, don't stop at describing the process. Verify or create a single launch surface that makes startup obvious.