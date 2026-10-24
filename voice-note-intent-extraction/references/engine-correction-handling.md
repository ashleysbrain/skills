# Engine Correction Handling

## Session note
A user voice note corrected the agent after it invented a new health engine name and wrong conceptual frame.

### What the user actually meant
- The named system already existed.
- The request was to return to the existing artifact, not create a new engine.
- The user wanted the work run on the correct engine and correct lane.

### Agent behavior to preserve
- Treat “you already created this yesterday” as a hard cue to stop inventing and verify the existing artifact first.
- Separate:
  - **actual ask**: what the user wants done now
  - **context**: the story of how the system was discussed
  - **correction**: the exact thing the user says is wrong
- If a named engine or system is disputed, search for the canonical file/session before proposing a new label or architecture.

### Practical rule
When a voice note contains a correction like:
- “that’s not a new engine”
- “go back to the one we already created”
- “you’re making up the wrong frame”

then output a clean request summary and do not expand into speculative implementation until the existing artifact has been identified.
