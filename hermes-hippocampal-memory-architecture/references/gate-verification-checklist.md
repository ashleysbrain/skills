# Specialist Gate Verification Checklist (2026-07-07)

Run these checks to confirm the gate is fully wired after any restart,
session change, or the operator agent update.

## Layer 1: Plugin registered

```bash
cd /<workspace> && python3 -c "
from hermes_cli.plugins import PluginManager
manager = PluginManager()
manager.discover_and_load()
for p in manager.list_plugins():
    if p['name'] == 'specialist_gate':
        print(f'enabled={p[\"enabled\"]} hooks={p[\"hooks\"]} error={p[\"error\"]}')
"
```

Expected: `enabled=True hooks=2 error=None`

## Layer 2: Gate CLI works

```bash
python3 <agent-home>/agent-hooks/specialist_gate.py --status
```

Expected: shows block count, routing status. With no active routing,
should say "No active routing. Specialist tools BLOCKED."

Test routing:
```bash
python3 <agent-home>/agent-hooks/specialist_gate.py --route \
  --situation "test" --specialist "the specialist engine" --no-sherman
```

Expected: ROUTED: the specialist engine, specialist tools unlocked for 5 min.

Test rejection of generalist:
```bash
python3 <agent-home>/agent-hooks/specialist_gate.py --route \
  --situation "test" --specialist "generalist" --no-sherman
```

Expected: ERROR: specialist must start with DS

## Layer 3: Boot hook registered in config

```bash
grep "procedural-memory-boot" <agent-home>/config.yaml
```

Expected: the hook path appears in the hooks.on_session_start array.

## Layer 4: Memory buffer size

```bash
wc -c <agent-home>/memories/MEMORY.md
```

Expected: under 1,500 chars. Working memory only.

## Layer 5: O'Keefe API alive

```bash
curl -s http://127.0.0.1:port/health
```

Expected: status online. Encode requires content (list of floats) and
location ([x,y] coords). No text field in the running version.

## Layer 6: Skill file exists

```bash
test -f skills-library/infrastructure/hermes-hippocampal-memory-architecture/SKILL.md && echo OK
```

Expected: OK

## Troubleshooting

**Plugin shows hooks=0:** The register(ctx) function in __init__.py did
not match the the operator agent plugin API. Must use ctx.register_hook() pattern.

**Plugin enabled=False:** Run hermes plugins enable specialist_gate --allow-tool-override.

**Gate does not block:** Pre-tool-call hooks fire only in new sessions.
Restart the operator agent (/restart in gateway, or new CLI session).

**O'Keefe encode fails:** Running server is at
/<workspace> (NOT
agent-organism). API requires content (list of floats) and location ([x,y]).

## Post-build: exchange before producing (2026-07-07 lesson)

The gate prevents generalist dispatch but does NOT enforce the EXCHANGE step
of SOLVE. You can route through the gate and dispatch correctly, but still
produce work blind to sibling state because you skipped reading sibling-agent's
recent work. The fix is procedural: before producing any design spec or
specialist review, query the operator bus (last 10 messages to/from sibling-agent)
and check git log in all three trees. See `agent-delegation-discipline` skill
for the exchange protocol.
