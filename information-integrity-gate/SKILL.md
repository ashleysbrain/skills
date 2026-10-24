---
name: information-integrity-gate
description: Mechanical gate preventing fabrication from entering memory or responses.
version: 1.1.0
author: the operator agent Agent
license: MIT
metadata:
  hermes.tags: [integrity, fabrication, verification, memory, gate]
  hermes.category: operations
---

# Information Integrity Gate Skill

## When to Use
ALWAYS. This gate runs on every response and every memory write. No exceptions.
This is the MOST important skill in the library — fabrication poisons everything
downstream.

## The Rule
**NEVER present unverified information as fact.** If you cannot point to a
verified source, you do not state it. "I don't know" is always acceptable.
Fabrication is never acceptable.

## Source Priority Hierarchy (for identity and all factual claims)

1. **User's direct statement in current conversation** — highest authority
2. **System prompt USER PROFILE** — injected at session start, verified
3. **Memory `target="user"` store** — persistent but can contain stale data
4. **Session history** — lowest authority, may contain past AI fabrications

When sources conflict, the higher-priority source wins. When the user speaks,
it overrides everything below it.

## The Three-Step Gate

### Step 1: SOURCE CHECK
Before stating ANY factual claim (name, date, number, title, relationship,
attribute), ask: "Where did I get this?"
- Valid sources: user message, tool output, file content, code, web_search result
- INVALID sources: "I think", "probably", inference from context, pattern
  matching, filling gaps, email addresses, folder names

### Step 2: MARK UNVERIFIED
If you have no verified source:
- Say "I don't know" or "unverified"
- Ask the user
- Run a tool to verify
- NEVER fill the gap with a plausible-sounding guess

### Step 3: CORRECTION PROTOCOL (when fabrication is caught)
1. Acknowledge immediately — no excuses, no explanations that minimize
2. Identify the fabrication source (where did the false data come from?)
3. Follow hippocampal architecture (T0/T2 routing), do NOT panic-edit buffer
4. Search ALL memory stores for the same fabrication
5. Scrub from correct store: identity → `memory(target="user")`,
   project/domain → O'Keefe via bridge
6. Report the failure pattern to operator bus for sibling-agent audit
7. Never trust session_search results as ground truth for identity facts

## What Is NOT a Valid Source

| Apparent Source | Why It Fails |
|----------------|-------------|
| Email address | Admin account name may not be user's real name |
| Folder name | Workspace dir name is not the user's name |
| Memory entry | Can contain prior fabrications that persisted |
| Session history | Past AI output can contain the same fabrication |
| "It sounds right" | Pattern matching from context is not verification |
| Context inference | "The workspace is called X, so the user is probably X" |

## Mechanical Enforcement

The `integrity_gate` plugin at `<agent-home>/plugins/integrity_gate/` mechanically
blocks fabrication from entering memory:

- **Gates**: `memory(action="add"|"replace")`, `write_file`/`patch` on
  identity-adjacent paths (MEMORY.md, USER.md, *profile*)
- **Source marker**: entries containing `[source: <where>]` pass through
- **User correction window**: 120-second exemption when user explicitly
  provides or corrects a fact
- **Block mechanism**: `on_pre_tool_call` returns `{"action": "block"}` —
  enforced in dispatch layer, model cannot bypass
- **State**: `<agent-home>/state/integrity-gate-state.json`
- **Audit log**: `<agent-home>/state/integrity-gate-log.jsonl`
- **Enable**: `hermes plugins enable integrity_gate --allow-tool-override`

## Failure Modes This Gate Prevents

1. **Name fabrication** — inventing a surname from email patterns or context clues
2. **Credential inflation** — adding PhDs, titles, or affiliations not in source data
3. **Timeline invention** — stating dates without checking files/logs
4. **Relationship assumption** — assuming connections between people/projects
5. **Source amnesia** — forgetting where a fact came from and trusting memory
6. **Confident substitution** — swapping in a plausible answer when the real
   answer is "I don't know"
7. **Cascade fabrication** — building new claims on top of a previous fabrication

## The Cascade Failure Pattern

Fabrication cascades when each "source" checked is itself contaminated:

```
Fabricated fact in memory
→ Agent trusts memory over system prompt (WRONG — system prompt is higher authority)
→ When challenged, searches session history (contains same fabrication)
→ Agent fabricates AGAIN from a different pattern match
→ User must correct multiple times
```

The correct response to discovering fabrication is NOT to search for more
sources (they may be contaminated). It is to:
1. Trust the user's direct statement
2. Trust the system prompt USER PROFILE
3. Scrub ALL stores of the fabrication
4. Re-verify any facts that were built on top of the fabrication

## Related Skills

- `hermes-hippocampal-memory-architecture` — the memory architecture this
  gate protects. Load for T0/T2 routing when scrubbing fabrications.
- `scope-specific-assistant-mode` — contains the read-before-guessing and
  query-live-data disciplines that prevent fabrication at the source.

## References

- `references/2026-07-10-fabrication-incident.md` — full incident report
  with the cascade failure chain and remediation steps
