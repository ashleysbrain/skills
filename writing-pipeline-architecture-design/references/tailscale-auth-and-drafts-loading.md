# Tailscale Auth + Drafts Loading Bug (2026-08-10)

## Symptom
User sees zero drafts in Writing Studio despite 5 drafts existing in the DB
and the API returning them correctly with auth.

## Root Cause
The `/api/auth/local-token` endpoint was restricted to `127.0.0.1` only:
```python
if client_ip not in ("127.0.0.1", "::1", "localhost"):
    raise HTTPException(403, "Local token only available from localhost")
```

When accessed via Tailscale (`100.107.113.11:port`):
1. Token auto-fetch returns 403
2. No token set in localStorage/sessionStorage
3. All subsequent `/api/drafts` calls return 401
4. Adiabatic cache stores empty drafts list
5. Even after server restart, browser serves stale empty cache

## Fix (3 Parts)

### 1. Backend: Allow Tailscale IPs
```python
client_ip = request.client.host if request.client else ""
is_local = client_ip in ("127.0.0.1", "::1", "localhost")
is_tailscale = client_ip.startswith("100.")
if not (is_local or is_tailscale):
    raise HTTPException(403, "Local token only available from localhost or Tailscale")
```

### 2. Frontend: Detect Tailscale Hostname
```javascript
const isTailscale = window.location.hostname.startsWith('100.');
if ((isLocal || isTailscale) && !_getAuthToken()) {
    // Auto-fetch token
    const r = await _originalFetch.call(window, API + '/api/auth/local-token');
    // ...
}
```

### 3. Frontend: Clear Cache on 401
```javascript
if (r.status === 401) {
    localStorage.removeItem('ws_auth_token');
    sessionStorage.removeItem('ws_auth_token');
    _adiabaticStore = {};  // Clear stale empty drafts cache
    // Re-fetch token, then reload
}
```

## Verification
- 5 drafts returned with auth via curl
- `curl -s http://localhost:port/api/drafts?stage=all` (no auth) = 401
- `curl -s -H "Authorization: Bearer $TOKEN" http://localhost:port/api/drafts?stage=all` = 5 drafts

## General Pattern
When "data not loading" in a cached SPA with auth:
1. Check if auth token endpoint is IP-restricted
2. Check if adiabatic cache serves stale pre-auth state
3. The cache+auth interaction: a 401 can cache an empty response that persists
   even after auth is fixed — must explicitly clear cache on auth failure

## Status: FIXED (commit f6b0007)
Both the principal (localhost) and the principal (Tailscale) now get zero-prompt access.
The fix was applied to both `pipeline_api.py` (backend IP check) and
`writing-studio.html` (frontend Tailscale detection + cache clear).
