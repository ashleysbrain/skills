# Gateway startup hook: deterministic boot render

Session-derived note for the operator agent gateway boot flows.

## Problem observed
A startup hook was originally implemented by passing `<agent-home>/BOOT.md` to a one-shot agent. The checklist itself was fine, but the agent interpreted it and made an initial bad render attempt, which produced the error:

- `--engine is required unless --all is used`

## Durable fix
For deterministic startup work, have the hook execute the command directly instead of asking an agent to interpret the checklist.

Example pattern:

```python
subprocess.run(
    [sys.executable, str(RENDER_SCRIPT), "--root", str(HYDRA_ROOT), "--all"],
    cwd=HYDRA_ROOT,
    check=False,
    capture_output=True,
    text=True,
)
```

## Verification pattern
After the render:
- confirm the process exit code is 0
- confirm the expected artifacts exist, e.g.
  - `memory/generated/aisha-ai/MEMORY.md`
  - `memory/generated/aisha-gd/MEMORY.md`
  - `memory/generated/aisha-md/MEMORY.md`
- log the rendered count explicitly so startup logs show the hook completed

## Pitfall
Do not turn deterministic boot work into a mini-agent task unless the boot logic truly requires reasoning or branching. Startup hooks should be boring and reproducible.
