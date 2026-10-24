# Python FastAPI Environment Troubleshooting (macOS, the operator agent workspace)

When building assessment tool APIs on this machine, the Python environment
situation is non-obvious. Here is the verified working configuration as of
2026-08-06.

## The Problem

The the operator agent agent venv at `<agent-home>/hermes-agent/venv/bin/python3.11` has a
broken `pydantic_core._pydantic_core` binary import. Attempting to import
FastAPI or Pydantic through this venv produces:

```
ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'
```

This is a compiled extension issue (the binary wheel doesn't match the
Python version or architecture). Do NOT attempt to fix the venv.

## The Fix

Use the system Python 3.14 with the user site-packages:

```bash
PYTHONPATH=~/Library/Python/3.14/lib/python/site-packages python3.14 server.py --port 8311
```

The user-site at `~/Library/Python/3.14/lib/python/site-packages/` has
working copies of:
- fastapi (0.135.1)
- pydantic (2.12.5)
- pydantic_core (2.41.5)
- uvicorn (0.41.0)

## Verification Command

Before launching, verify the stack works:

```bash
PYTHONPATH=~/Library/Python/3.14/lib/python/site-packages python3.14 -c \
  "import fastapi, pydantic, uvicorn; print(f'fastapi={fastapi.__version__}, pydantic={pydantic.__version__}, uvicorn OK')"
```

Expected output:
```
fastapi=0.135.1, pydantic=2.12.5, uvicorn OK
```

## Finding the Right PYTHONPATH

If the above path doesn't work (different Python version), discover it:

```bash
python3.14 -c "import sys; print([p for p in sys.path if 'site-packages' in p])"
```

Or check what's installed in user-site:

```bash
ls ~/Library/Python/3.14/lib/python/site-packages/ | grep -iE "fastapi|uvicorn|pydantic"
```

## The Pipeline API Pattern

The existing pipeline_api.py (on :port) uses the same pattern. It runs
under system python3.14 with user-site packages. Follow this pattern for
all new API servers in this workspace.

## Port Allocation

- :port = Pipeline API (VERITAS + CRUCIBLE)
- :port = Personality Test API (IPIP-NEO-120)
- :port, :port, :port = various DS engine uvicorn servers
- 8xxx range = organism engines
- 9xxx range = Cyber the operator agent engines

Always check port availability before binding:

```bash
curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://localhost:<port>/ 2>/dev/null
```

000 = free, anything else = in use.
