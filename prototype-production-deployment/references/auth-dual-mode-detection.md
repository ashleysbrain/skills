# Frontend Auth Dual-Mode Detection

## The Problem
When migrating from a static-token auth backend to JWT auth, the frontend
HTML gets updated to show a login/signup form. But if the live local server
still runs the OLD backend (no `/api/auth/login` endpoint), the login form
appears and nothing works. The user is locked out.

This happened TWICE in one session. The user's exact words: "I need to get
into the writing studio and you just kicked me out." Then again: "it is
making me fill it out and i can't get into it still."

## WRONG Probe (does not work)

Probing `/api/auth/me` and checking for 404 DOES NOT WORK. The legacy
server's auth guard intercepts ALL API routes before route matching, so
`/api/auth/me` returns **401 Unauthorized** (not 404). The detection logic
never triggers the legacy fallback path. The user sees the login modal
and cannot get past it.

```javascript
// BROKEN: this returns 401 on legacy servers, not 404
const probe = await fetch(API + '/api/auth/me');
if (probe.status === 404) { // NEVER TRUE on legacy backend
  // legacy fallback...
}
```

## CORRECT Probe (verified working)

Probe the LEGACY endpoint `/api/auth/local-token` instead. This endpoint
exists ONLY on the legacy server (returns 200 + a token). On the new JWT
server it returns 404 (endpoint doesn't exist). This is a reliable signal:

```javascript
async function _checkAuth() {
  // Step 1: Probe for LEGACY backend via local-token endpoint
  window._legacyAuth = false;
  try {
    const probe = await _originalFetch.call(window, API + '/api/auth/local-token');
    if (probe.ok) {
      // LEGACY backend — auto-fetch token, skip login modal entirely
      window._legacyAuth = true;
      const d = await probe.json();
      if (d.token) { _setAuthToken(d.token); }
      window._authReady = true;
      window._authResolve();
      return;
    }
  } catch(e) { /* server might be down */ }

  // Step 2: NEW JWT backend — standard JWT auth flow
  const token = _getAuthToken();
  if (!token) {
    _showAuthModal();
    window._authReady = false;
    window._authResolve();
    return;
  }
  // Validate token against /api/auth/me...
}
```

Key insight: probe for what the LEGACY server HAS (local-token endpoint),
not what the NEW server has. A positive signal (200 OK) is more reliable
than a negative one (404) because auth guards can intercept and transform
404s into 401s.

## Also: Gate the 401 Handler

The fetch wrapper's 401 auto-redirect must NOT fire on the legacy backend
(legacy backend returns 401 for unauthenticated requests as normal flow):

```javascript
if (response.status === 401
    && !url.includes('/api/auth/')
    && _getAuthToken()
    && !window._legacyAuth) {   // <-- this check is critical
  _clearAuthToken();
  _showAuthModal();
}
```

## localStorage Key Migration

Old system: `ws_auth_token`
New system: `ws_jwt`

## Rule
Never push auth frontend changes to a live server unless the backend change
is already deployed, OR the frontend supports both auth modes via this
detection pattern. Test the detection by loading the page against BOTH
the old and new backends before declaring it done.
