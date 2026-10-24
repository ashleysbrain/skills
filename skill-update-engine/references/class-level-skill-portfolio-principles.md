# Class-Level Skill Portfolio Principles

Use this reference when updating the skill library.

## Portfolio shape
- Prefer class-level umbrella skills over one-session-one-skill entries.
- Keep the umbrella skill broad enough to remain useful across repeated sessions.
- Put session-specific detail, examples, transcripts, and recovery notes in `references/`.
- Put reusable scaffolds and copyable patterns in `templates/`.
- Put deterministic checks, probes, and rerunnable actions in `scripts/`.

## Update rule
- If a session reveals a durable workflow, technique, or pitfall, update the governing umbrella skill in the same session when possible.
- If the learning is too specific for SKILL.md, capture it in a reference file and add a one-line pointer from SKILL.md.
- When a user preference affects how a class of tasks should be handled, encode it in the governing skill body, not only in memory.

## Anti-sprawl rule
- Do not turn every narrow episode into a new skill.
- When two skills overlap strongly, prefer strengthening the umbrella and parking the evidence in references/.
- Treat repeated narrow fixes as a sign to broaden the class-level skill rather than adding another sibling skill.
