# Process Flow Guardrails

- Preserve the full process when the user asks for "start to finish" or says the earlier version was simplified.
- Distinguish fresh summon from background-running continuation before asking questions.
- Keep the question flow, state machine, and README overview synchronized with the process flow.
- If the user asks for the whole process again, include every established step and sub-step instead of compressing.
- Treat "stuck" reports as a cue to inspect the latest user message against the assistant's last turn for the actual workflow mismatch.
- When the process is already known, do not invent new steps or terminology.
- Keep advisor logic separate from intake logic and response logic.
