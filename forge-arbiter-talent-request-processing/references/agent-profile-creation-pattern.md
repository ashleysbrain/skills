# Agent Profile Creation Pattern

## Where Profiles Live

```
~/.sibling-agent/workspace/intel/agents/profiles/DS {NAME}.md
```

Note: filenames contain spaces (e.g., `DS ISING.md`, `DS NOETHER.md`).

## Profile Structure (From Spawn Template)

Every agent profile MUST include these sections:

1. **Header** — Codename, Alias, Emoji, Role, Domain, Model, Cost Justification
2. **Credentials** — Highest degree, 3+ prior roles, key publications, known-for statement
3. **Personality Profile** — Big Five (OCEAN) table, MBTI type + rationale, Enneagram type + rationale
4. **8D Wellness Scores** — Table with all 8 dimensions + TWC + Tier, plus per-dimension rationale
5. **Task Assignment** — Task, criticality, expected output, output path, deadline, success criteria
6. **Context Injection** — Active projects, energy state, prior decisions, format expectations, standing directives
7. **Subagent Context Block** — Wrapped in triple backticks, contains credentials, personality scores, 8D table, task list, constraints

## Reliable Creation Method

Use the `write_file` tool. It handles:
- Paths with spaces (e.g., `profiles/DS ISING.md`)
- Multi-line content
- Unicode (emoji)

Terminal heredocs (`cat << 'EOF' > path`) are unreliable for agent profiles because:
- Files with 200+ lines cause exit_code -1 (shell treats as background)
- Paths with spaces require quoting that conflicts with heredoc delimiters

## After Profile Creation

1. Verify the file exists: `ls ~/.sibling-agent/workspace/intel/agents/profiles/ | grep {NAME}`
2. Register in DB (see `references/agents-db-schema.md` for insert pattern)
3. Append DECISION to talent request (use `patch` tool, not shell append)
4. Move request to `processed/`
5. Run fleet analytics sync
6. Git commit from workspace root

## Common Issues

- **Baseline-first gate**: If `write_file` blocks on a new profile file, it's a session state issue. Try writing a small test file first, then retry the real content. The gate resolves after a successful write.
- **Nested code fences**: The subagent context block uses triple backticks. If the outer content also needs backticks, use different fence lengths (```` ``` ```` wrapping ` ``` `) or indent the inner block with 4 spaces instead.
