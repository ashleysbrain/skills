# PENDING SKILL.md patch (parked 2026-08-18 — background patch blocked by read-before-write guard)

Foreground curator: apply via skill_manage patch. Two edits.

## Edit 1 — expand credential storage point 3 with the braced-form trap

OLD:
```
3. Any MCP Notion server config in the operator agent — a stale token here keeps returning
   401 even after (1) and (2) are fixed.
```

NEW:
```
3. Any MCP Notion server config in the operator agent — a stale token here keeps returning
   401 even after (1) and (2) are fixed. Env-var references in MCP `env:`
   blocks MUST use the braced form `${NOTION_API_KEY}`: the operator agent interpolates
   only `${VAR}` (tools/mcp_tool.py `_ENV_VAR_PATTERN`), so unbraced
   `$NOTION_API_KEY` passes through as a literal string and the server 401s
   with the variable name as its token — surviving config "fixes" and
   restarts. Verify through the real path (env_loader.load_hermes_dotenv()
   then mcp_tool._interpolate_env_vars), never by YAML-parsing alone; and
   remember running MCP processes are stale until respawned from fixed config
   (desktop-app and gateway spawn SEPARATE trees — both need the respawn).
```

## Edit 2 — update the References list

OLD:
```
- `references/connection-session-2026-08-14.md` — full session detail:
  machine-specific env facts, exact probe transcripts, storage commands.
```

NEW:
```
- `references/connection-session-2026-08-14.md` — full session detail:
  machine-specific env facts, exact probe transcripts, storage commands.
- `references/share-wall-triage-2026-08-18.md` — zero-result search →
  browser-Sessions ID mining → canned-404 direct probe → armed watcher.
- `references/panel-verdicts-2026-08-18.md` — elite-panel corrections:
  canned 404s disprove "page exists", Enterprise path dead end, braced-form
  MCP env interpolation fix + verification recipe, framing lesson,
  transcript-salvage pattern for timed-out subagents.
```
