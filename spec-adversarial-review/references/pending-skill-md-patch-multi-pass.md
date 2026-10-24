PENDING SKILL.md PATCH (apply in foreground curator run; background _read_before_write
guard refuses edits to existing SKILL.md even after fresh skill_view — known quirk).

Insert BEFORE the "## References" section of
software-development/spec-adversarial-review/SKILL.md:

---

## Multi-Pass Reviews ("another pass", different brains)

When the user asks for REPEATED passes on the same spec ("do another thorough QA
pass"), each pass MUST use a DIFFERENT specialist panel with orthogonal attack
vectors — reused panels find fewer new defects per pass. Proven rotation and the
techniques each brain contributed (registry-name tracing, message-bus recipient
census, CI test-floor check, estimate striking) live in
`references/multi-pass-fresh-brains-protocol.md`. Fold each pass's findings into
the SAME canonical doc as a changelog table — never spawn a competing spec.

---

Also: replace the body of references/multi-pass-fresh-brains-protocol.md (currently
the literal string "placeholder") with the body of
references/pending-multi-pass-fresh-brains-protocol.md, then delete both pending
files.
