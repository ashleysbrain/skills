# Writing Studio Auth and Runtime Verification (Aug 2026)

## Auth Persistence Architecture

### Localhost (the principal) — Zero Prompt
1. Page loads (public path, no auth needed)
2. `_checkAuth()` fires on DOMContentLoaded
3. Detects localhost → fetches `/api/auth/local-token`
4. Stores token in `localStorage` (persists across browser restarts)
5. Fetch wrapper injects `Authorization: Bearer <token>` on every request

### Tailscale (the principal) — One-Time Prompt
1. Page loads → API call → 401 (no token)
2. Prompt appears → the principal enters token
3. Stored in `localStorage`
4. Never prompted again (persists across sessions)

### Stale Token Handling
If token is rotated:
1. Stored token is stale → first API call gets 401
2. `_checkAuth()` detects 401 response
3. Clears stale token from localStorage
4. Re-prompts for new token
5. (On localhost: auto-refetches from local-token endpoint)

## 16-Endpoint Verification Protocol

Test every Writing Studio view by hitting each API endpoint with the auth token:

```python
TOKEN = fetch("/api/auth/local-token")  # localhost only
endpoints = [
    "/api/auth/local-token", "/api/drafts?stage=all",
    "/api/pipelines/runs", "/api/feed", "/api/actions",
    "/api/topics", "/api/build-queue", "/api/research/search?q=test",
    "/api/science-base", "/api/calendar", "/api/calendar/mesh?days=365",
    "/api/library", "/api/connections", "/api/industries",
    "/api/recommendations", "/api/pipelines/health",
]
# All must return 200
```

**Pitfall:** Endpoint names use hyphens (`/api/build-queue`) not slashes
(`/api/build/queue`). Easy to get wrong. Always grep the HTML for actual fetch
calls to find the real endpoint names.

## Pipeline Output Quality Report Format

After running VERITAS, read the checkpoint JSON (NOT the `.run()` return value):

```python
with open("/tmp/veritas_process_state_<TIMESTAMP>.json") as f:
    state = json.load(f)

draft = state["current_draft"]          # the actual text
citations = state["citations"]          # gathered papers (flat list)
final = state["final_output"]           # QA results
cs = final.get("citation_support", {})  # checked, phantom_count, supported_count
mc = final.get("metric_check", {})      # fabricated_count
panel = state["stage_results"]["5"]     # panel_verdict (NOT "verdict")
```

**Quality gates to verify:**
- Draft > 3000 words
- Citation markers in text match References section
- `phantom_count == 0`
- `fabricated_count == 0`
- Em dashes == 0 (QA should have cleaned them)
- AI telltales == 0

## Server Lifecycle

- Server: `pipeline_api.py` on port 8310 (FastAPI/uvicorn)
- Gateway: port 8305
- Restart after code changes: kill PID, restart with
  `<agent-home>/hermes-agent/venv/bin/python3 pipeline_api.py --port 8310`
- Verify restart loaded new code: check `ps -p PID -o lstart=` against commit time
