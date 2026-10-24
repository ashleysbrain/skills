---
name: zcode
description: Delegate coding and repo tasks to ZCode, the Z.ai LLM coding agent CLI. Use when the user asks for ZCode specifically, wants a second coding agent's take, or for parallel hands-on-keyboard coding work in a repository.
tags: [zcode, coding, delegation, agents, cli]
---

# ZCode Delegation

## When to Use

- The user says "use zcode", "ask zcode", or names ZCode in a task
- A repo task would benefit from a second autonomous coding agent with its own tools and sessions
- You want to hand off a self-contained coding chore and get the result back

## How to Run

ZCode is installed at `~/.local/bin/zcode` (wrapper around the CLI bundled with the ZCode.app desktop app). Headless one-shot:

```bash
zcode --prompt "<task description>" --cwd /path/to/repo --mode yolo --json
```

- `--mode`: `build`, `edit`, `plan`, or `yolo` (default `yolo` for `--prompt`)
- `--attach <file>`: attach a local file to the prompt; repeat for multiple files
- `--resume <sessionId>` or `-c`: resume a previous ZCode session (sessionId format `sess_...`)
- `--target "<goal>"`: set/replace the session goal in headless mode
- `--json`: machine-readable output — prefer this when parsing the result
- `zcode -c --prompt "<follow-up>"`: continue the latest session for that directory

## Notes

- First use requires `zcode login` (Z.AI OAuth, browser) if credentials are not already shared from the desktop app.
- ZCode runs on the LLM Coding Plan; heavy use draws down that plan's quota.
- The bridge is two-way: ZCode has the operator agent configured as an MCP server (`hermes mcp serve`), so ZCode agents can read and send messages in the operator agent conversations via the hermes messaging-bridge MCP tools.
