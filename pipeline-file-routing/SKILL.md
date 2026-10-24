---
name: pipeline-file-routing
category: devops
description: "Edit runtime pipeline files only, not blueprint copies."
version: 1.0.0
---

# Pipeline File Routing

The VERITAS and CRUCIBLE pipeline files exist in multiple copies. Only ONE copy actually runs. Editing the wrong copy means fixes don't take effect.

## Runtime Files (EDIT THESE)

`pipeline_api.py` imports from the workspace root:

```
./veritas_process.py    <- RUNTIME (what pipeline_api.py loads)
./crucible_process.py   <- RUNTIME (what pipeline_api.py loads)
```

Verify before editing:
```bash
grep -n "import.*veritas\|import.*crucible" pipeline_api.py
```

## Blueprint Copies (DO NOT EDIT — reference only)

```
./gigi3/organism/veritas_process.py                 <- gigi3 blueprint
./gg3-blueprint/organism/veritas_process.py          <- stale 970-line old version
./cyber-gg-blueprint/crucible_process.py             <- duplicate of runtime
./cyber-gg-blueprint/organism/crucible_process.py    <- different version (1596 lines)
```

## How to Know Which File Runs

1. `pipeline_api.py` line ~248: `from crucible_process import CruciblePipeline`
2. Python resolves bare module imports to the current working directory
3. Working directory is `/<workspace>`
4. Therefore `./crucible_process.py` is the runtime file.

## Failure Mode (documented 2026-08-10, msg 1721)

Opencode built CVE verification and py_compile syntax checking into `cyber-gg-blueprint/organism/crucible_process.py`. Code was correct. But pipeline_api.py imports from `./crucible_process.py`. Fixes had zero effect at runtime.

## Prevention Rule

Before editing ANY pipeline file:
```bash
grep "from.*import\|import " pipeline_api.py | grep -i "veritas\|crucible"
```

Only edit the file at `./` root. Propagate to blueprint copies as a separate explicit step AFTER the runtime fix is verified.
