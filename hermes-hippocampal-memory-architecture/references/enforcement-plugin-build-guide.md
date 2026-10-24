# How to Build a Mechanical Enforcement Plugin (2026-07-07)

The specialist gate is one instance of a general pattern: a the operator agent plugin
that physically BLOCKS tool calls unless a precondition is met. This guide
documents the plugin API so future sessions can build new enforcement gates
without rediscovering it.

## The the operator agent Plugin System

Plugins live in `<agent-home>/plugins/<name>/` with two files:

- `plugin.yaml` — metadata, declares which hooks the plugin registers
- `__init__.py` — the hook callbacks, exposed via a `register(ctx)` function

## plugin.yaml format

```yaml
name: specialist_gate
version: "1.0.0"
description: "What this plugin enforces"
author: the operator agent Agent
hooks:
  - pre_tool_call
  - post_tool_call
```

## __init__.py registration pattern

The plugin must define a `register(ctx)` function that calls
`ctx.register_hook()`. This is the CORRECT pattern (verified working):

```python
def register(ctx) -> None:
    ctx.register_hook("pre_tool_call", on_pre_tool_call)
    ctx.register_hook("post_tool_call", on_post_tool_call)
```

WRONG pattern (does NOT work — plugin loads but hooks do not register):
```python
from hermes_cli.plugins import PluginRegistrar

def register(plugin: PluginRegistrar):
    plugin.register_hook(...)
```

## The pre_tool_call hook

This is the enforcement point. It fires BEFORE any tool executes. The hook
receives the tool name and arguments. If it returns a block directive, the
tool does NOT execute and the model sees the block message as the tool result.

```python
def on_pre_tool_call(tool_name: str, tool_args: dict) -> dict | None:
    # Check your precondition
    if not precondition_met(tool_name, tool_args):
        return {
            "action": "block",
            "message": "Block reason. Tell the model what to do to fix it."
        }
    # Return None to allow the tool call to proceed
    return None
```

The block happens mechanically in `model_tools.py` at the dispatch layer
(line ~1175). The model cannot bypass it.

## Enabling the plugin

```bash
hermes plugins enable <name> --allow-tool-override
```

Verify registration:
```python
from hermes_cli.plugins import PluginManager
manager = PluginManager()
manager.discover_and_load()
for p in manager.list_plugins():
    print(f'{p["name"]}: enabled={p["enabled"]} hooks={p["hooks"]}')
```

## Critical: hooks activate on next session

The plugin loads in the current session but `pre_tool_call` hooks only fire
in NEW sessions (after gateway restart). The current session is unaffected.
To activate: restart the gateway (`hermes gateway restart` from an external
shell, or `/restart` in Telegram).

## Pattern: state-based gates

The specialist gate uses a state file (`<agent-home>/state/specialist-gate-state.json`)
written by a CLI tool (`<agent-home>/agent-hooks/specialist_gate.py`). The agent
calls the CLI tool to "unlock" the gate before specialist work, and the
plugin's pre_tool_call hook checks the state file. This separates the
UNLOCK mechanism (CLI tool the agent calls) from the ENFORCEMENT mechanism
(plugin hook that blocks). The agent cannot bypass the plugin by simply not
calling the CLI — the default state is BLOCKED.

## What you can enforce

Any tool call can be gated: `delegate_task`, `write_file`, `patch`,
`execute_code`, `terminal`. Gate by:
- Tool name (block all delegate_task without routing)
- File path patterns (block write_file on specialist artifact paths)
- Argument content (block patch calls that modify engine code without
  specialist routing)

## Limitation (honest)

The hook fires before the tool runs, but there is no way to enforce that the
agent CALLS the gate CLI before trying the tool. The gate blocks by default
and unlocks on valid routing. If the agent never routes, all specialist tools
stay blocked — which is the correct behavior, but may confuse if the agent
does not understand why its tool calls are failing.
