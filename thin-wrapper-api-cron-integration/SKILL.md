---
name: thin-wrapper-api-cron-integration
category: software-development
description: Expose an existing CLI or pure-function engine through a thin HTTP API and cron-safe wrapper without duplicating core logic.
version: 1.0.0
---

# Thin Wrapper API + Cron Integration

Use this skill when an existing local engine, script, or scorer needs to be:
- exposed through a lightweight HTTP API
- callable from cron or another scheduler
- verified with tests, syntax checks, and smoke runs
- kept DRY so the core logic stays in one place

## Class of task
The task class is: **wrap existing production logic in a thin API and/or cron entrypoint, then verify the wrapper with sample payloads and scheduled-job dry runs**.

## When to Use
Use this skill when:
- there is already a working CLI script or pure Python function
- you need a small FastAPI/Flask/HTTP wrapper around it
- you need a cron-safe shell wrapper or install script
- request/response payloads should remain JSON-friendly and simple
- the core engine must not be reimplemented in the wrapper
- the wrapper output must also feed an existing scorecard, dashboard, or other composite result without changing behavior when the sidecar payload is absent
- you need a repeatable path from local script → API → scheduled execution

## Core Principles
1. **Keep business logic in one module**.
2. **Wrap, don’t rewrite**: import or load the existing engine instead of copying scoring logic.
3. **Make wrappers thin**: validate inputs, call the engine, return JSON or write files.
4. **Make cron safe**: stable paths, explicit env vars, no interactive prompts.
5. **Verify every layer**: syntax, unit test, API smoke test, and dry-run cron entry.

## Recommended Workflow

### 1) Inspect the existing engine
Identify:
- the callable function(s) to reuse
- the current CLI arguments or file inputs/outputs
- any required environment variables
- what can be reused directly vs what needs a wrapper

### 2) Add a thin API wrapper
Preferred pattern:
- import the engine module directly when possible
- if the filename is not import-friendly, load it by path with `importlib.util`
- expose a `/health` endpoint
- expose a `/score` or `/run` endpoint that passes JSON through to the engine
- keep the request model permissive if the input shape may evolve

### 3) Add a cron-safe shell wrapper
Preferred pattern:
- resolve paths relative to the repo or script directory
- accept overrides via environment variables
- create output/log directories if needed
- call the engine in a non-interactive way
- write logs for cron troubleshooting

### 4) Add an installer or dry-run script
If cron is part of the task:
- generate the cron line in `--dry-run` mode first
- support `--apply` only when explicitly requested
- avoid silently overwriting unrelated crontab entries
- make schedule and paths configurable with env vars

### 5) Add tests
Minimum useful coverage:
- API health endpoint returns ok
- API endpoint accepts a representative payload
- wrapper reaches the engine and returns expected keys
- fusion or adapter layer preserves backward compatibility when sidecar data is missing
- cron shell script passes `bash -n`
- dry-run installer prints a valid cron entry

### 6) Verify with live smoke runs
Recommended verification order:
1. `bash -n` for shell scripts
2. Python import or module load smoke test
3. `pytest` for the wrapper tests
4. sample API request or direct function call
5. cron dry-run output
6. sample wrapper execution with temp input/output paths

## Common Pitfalls
- Rewriting the engine inside the API wrapper instead of importing it
- Forgetting to make filenames importable or loadable by path
- Making the cron wrapper interactive
- Hardcoding repo-specific paths that break outside one machine
- Installing cron entries without a dry-run preview
- Testing only the engine and not the wrapper layer
- Returning raw exceptions from the API without a clean HTTP error
- Writing the entire API server in one file — write_file has a ~8K token content limit; split into `engine.py` (core logic), `api.py` (routes), `run_server.py` (entry point), each under ~15KB
- Binding to port 8000 without checking first — that port may be occupied by other services (Honcho, etc.); always check or default to a less common port (e.g. 8088)
- PYTHONPATH not set for src-layout packages — when the engine code lives under `src/modulename/core.py` but `run_server.py` is at the repo root, uvicorn can't find the module. Fix: `PYTHONPATH=src python3 -m uvicorn api.server:app --port PORT`. Alternative: add `sys.path.insert(0, ...)` at the top of the server file.
- **Proxy-mode servers need stdlib only** (2026-07-17): When the wrapper's job is to proxy HTTP calls to EXISTING backend services (not wrap a local function), use `http.server.SimpleHTTPRequestHandler` + `urllib.request` from the Python stdlib. No Flask/FastAPI dependency needed. The server reads config from YAML at boot, serves static HTML from a directory, and proxies GET/POST to backend endpoints. This pattern is ideal for standalone organism/client repos that must be deployed on machines where only Python 3 is guaranteed. See `cyber-gg-blueprint/organism/cyber_gg_server.py` as a reference implementation.

## Suggested File Shapes
- `*_engine.py` or existing core script: core logic stays here
- `*_api.py`: thin FastAPI wrapper
- `run-*.sh`: cron-safe shell wrapper
- `install-*-cron.sh`: dry-run/apply cron installer
- `tests/test_*.py`: API and wrapper smoke tests

## Verification Checklist
- [ ] Core engine remains the single source of truth
- [ ] API wrapper calls the existing engine
- [ ] Cron wrapper runs non-interactively
- [ ] Dry-run cron output looks correct
- [ ] Tests cover the wrapper, not just the engine
- [ ] Sample payload round-trips successfully
- [ ] Output paths, logs, and env overrides work

## Related Skills
- `test-driven-development` for test-first wrapper creation
- `subagent-driven-development` for multi-file implementation work
- `code-review` for the final audit before merge
- `model-recommendation-maintenance` when the wrapper exposes model-routing or model-selection changes
