# Share-wall triage: from zero-result search to exact page IDs (2026-08-18)

Session: team product ideas in Notion; ingestion blocked; resolved to a
precise diagnosis + armed watcher. Companion to SKILL.md diagnosis chain.

## Verified sequence

1. **Auth check** — `ntn api v1/users/me` returns 200 + workspace name
   ("the specialist engine" @ Divinity Science). Proves token validity only.
2. **Search** — `ntn api v1/search -X POST` (POST REQUIRED, see below)
   returns `results: []` across every query. MCP Notion server meanwhile
   returns 401 (stale token in its config) — two DIFFERENT failure
   states coexisting; diagnose each separately.
3. **Local browser mining** — the user's Chrome holds the real workspace
   page URLs. History DB: only public/marketing/dev pages. Sessions
   (SNSS) files: live workspace URLs. Mine Sessions:
   ```bash
   strings "$HOME/Library/Application Support/Google/Chrome/<Profile>/Sessions/"* \
     | grep -oE 'app\.notion\.com/p/[0-9a-f]{32}' | sort -u
   ```
   Yielded 2 IDs: one main page (`?v=` view param = database-backed),
   one secondary.
4. **Direct probe** — `GET /v1/pages/<id>` with Bearer token:
   404 `object_not_found` + "Make sure the relevant pages and databases
   are shared with your integration 'the specialist engine'". The pages EXIST;
   the error names the exact fix and the exact integration name.
5. **Watcher** — background poll loop (20s) on the known IDs; on first
   200, ingestion auto-fires. Don't ask the user to "tell me when done".

## ntn CLI syntax correction

`ntn api v1/search query="x"` (as documented in the bundled notion
skill) FAILS: `400 invalid_request_url`. Correct form:
`ntn api v1/search -X POST query="x"`. Search is POST-only via ntn.

## Browser-session caveats

- Profile matters: only the profile actually used for Notion had the
  URLs (Default in this case; probe all of Default/Profile 1/2/...).
- Safari History.db, Arc/Brave/Edge: zero Notion hits — don't burn
  turns there before Chrome Sessions pays out.
- osascript tab enumeration only sees CURRENT tabs; Sessions files
  persist closed tabs too and need no window focus.

## Outcome state at session end

Pages still unshared at handoff (user chose the UI connect action);
watcher armed (20s poll, 600-poll budget). Pattern is the deliverable:
zero-result search + valid token ≠ dead end; browser Sessions → ID
probe converts it into an actionable admin instruction.
