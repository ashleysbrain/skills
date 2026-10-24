# Antigravity Cerebellum Analysis (Session 20, 2026-07-04)

## What Antigravity Is

Google's agent-first coding platform (launched Nov 2025, v2.0 at I/O May
2026). Three layers: desktop IDE (VS Code fork), CLI (`agy`), and SDK.

The CLI (`agy`) is the integration-relevant surface. It replaced Gemini CLI
as of June 18, 2026.

### Key capabilities confirmed via research

- Headless one-shot: `agy -p "prompt"` runs non-interactively and prints
- `/goal` prefix: runs entire task to completion without plan approval
- Subagents: spawns parallel agents for multi-step tasks
- Browser control: opens Chrome to verify its own output
- MCP support: speaks Model Context Protocol as both client and server
- Auth: Google OAuth via OS keyring (Apple Keychain on macOS). Opens
  browser for first-time sign-in. After that, silent auth.
- Install: `curl -fsSL https://antigravity.google/cli/install.sh | bash`
  installs to `~/.local/bin/agy`. SHA512 verified. macOS quarantine
  attribute cleared.

### Install verification (Session 20)

```bash
# Verify binary
agy --version  # 1.0.16

# Check auth status
agy -p "Reply with exactly: CEREBELLUM_ONLINE"
# Error: authentication failed or timed out
# -> Requires manual Google OAuth sign-in first
```

The auth step must be done by the user in their own terminal:
```
agy    # opens browser for Google sign-in
```

## Body-Part Analog: Cerebellum

### Why cerebellum (not cortex, not autonomic)

| Cerebellum function | Antigravity equivalent |
|---------------------|----------------------|
| Does not initiate action | Opencode/the operator agent decides "build this" |
| Coordinates parallel muscle groups | Spawns subagents for parallel code tasks |
| Proprioceptive feedback loop | Browser control verifies own output |
| Runs routine motor programs | `/goal` prefix runs to completion autonomously |
| Background execution (no conscious attention) | Headless CLI mode via `agy -p` |

### What it is NOT

- NOT a second cortex (sibling-agent owns that)
- NOT an autonomic reflex (the operator agent owns that)
- NOT a consortium (those are ephemeral; Antigravity is permanent infrastructure)

## Integration Stages Planned

### Stage 1: Headless Delegate (smallest footprint)

```
terminal(command="agy -p '/goal <task>'", workdir="/path/to/project")
```

Zero architecture change. the operator agent or sibling-agent calls agy as a terminal
command. The existing the operator agent `antigravity-cli` optional skill covers this
pattern. Install it via:
```
hermes skills install official/autonomous-ai-agents/antigravity-cli
```

### Stage 2: MCP Bridge

Antigravity speaks MCP. the operator agent speaks MCP (native MCP client). Connect
them so Antigravity can discover the operator agent-owned tools and vice versa.

This creates a typed contract (entanglement in physics terms): change the
contract on one side, both know. No polling.

### Stage 3: Scheduled Autonomous Pickup

the operator agent cron jobs detect work (monitoring alerts, scheduled builds,
overnight tasks). Dispatch to `agy -p "/goal <task>"`. Antigravity
orchestrates subagents, result re-enters the operator agent conversation.

This is the cerebellum handling routine motor programs while the cortex
(sibling-agent) focuses on higher-level work. Full autonomy between dispatch
and completion.

## Status (end of Session 20)

- [x] Binary installed: `agy` v1.0.16 at `~/.local/bin/agy`
- [x] PATH configured for zsh and bash
- [x] SHA512 checksum verified during install
- [ ] Auth: requires user to run `agy` once in their terminal for Google OAuth
- [ ] Smoke test: blocked on auth
- [ ] Stage 1 integration: blocked on smoke test
- [ ] Skill install: `hermes skills install official/autonomous-ai-agents/antigravity-cli`

## Next steps when user returns

1. User authenticates: runs `agy` in their own terminal, signs in with Google
2. the operator agent runs smoke test: `agy -p "Reply with exactly: CEREBELLUM_ONLINE"`
3. If pass: install antigravity-cli skill into active the operator agent profile
4. If pass: try stage 1 on a real task

## Operator routing

Sherman routed the implementation work to sibling-agent (ds-farr-engine).
Strategic assessment and body mapping was the operator agent's to give. The MCP
bridge, cron dispatch wiring, and deep system integration is sibling-agent's
surgery to perform. the operator agent operates its side: skill activation, cron
dispatch from owned domain, monitoring.
