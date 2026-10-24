# Panel verdicts: canned 404s, MCP env interpolation, transcript salvage (2026-08-18)

Continuation of the share-wall session: elite QA panel (Bichat membrane
autopsy -> Popper falsification -> Tanenbaum plumbing audit) over the
zero-visibility diagnosis. Corrections and techniques that outlive the session.

## 1. Canned 404s — page existence is UNPROVEN by API (Popper, verified live)

GET /v1/pages/<id> returns byte-identical `object_not_found` bodies for
(a) real-but-unshared page IDs and (b) RANDOM garbage UUIDs. The canned
text ("Make sure the relevant pages ... are shared with your integration")
names the right fix but is NOT evidence the page exists.

Consequences:
- Page IDs mined from browser Sessions files are UNVERIFIED until a grant
  lands or the page loads in the owner's browser.
- The flip condition that falsifies the whole permission diagnosis:
  post-grant HTTP 200 on a page + STILL-empty /v1/search. If that ever
  happens, the "empty grant set" verdict is wrong — re-open the case.

## 2. Enterprise admin path is a dead end for page grants

Settings -> Connections / Enterprise connection settings govern MEMBER
INSTALL rights and are plan-gated; they do not grant page access. Do not
send the user there. The only unblock is the per-page (or parent-page)
connection made by a user with page rights.

## 3. MCP env interpolation: braced form only

Defect chain seen live: MCP Notion server 401 -> config patched to
`NOTION_TOKEN: $NOTION_API_KEY` -> still broken, because the operator agent's
interpolation regex (tools/mcp_tool.py:516, `\$\{([^}]+)\}`) matches ONLY
`${VAR}`. Unbraced stays literal; the server authenticates with the string
`$NOTION_API_KEY`.

Fix: `NOTION_TOKEN: ${NOTION_API_KEY}`.
Verification (through the real code path, not YAML parsing):

```bash
/<workspace> -c "
import sys; sys.path.insert(0, '/<workspace>')
from hermes_cli.env_loader import load_hermes_dotenv
load_hermes_dotenv()
from tools.mcp_tool import _interpolate_env_vars
print(_interpolate_env_vars('\${NOTION_API_KEY}'))"
```

Resolved output should start `ntn_`. Then respawn BOTH MCP process trees
(desktop-app and gateway each spawn one); `/reload-mcp` covers CLI sessions,
the gateway tree needs its own restart. `ps -E` on macOS does NOT reliably
show process env (probe-verified) — verify by function (a live call), not
by env scans.

## 4. Framing lesson for user-facing diagnosis

"Where the fix is performed" (Notion's UI) is not "whose action it is"
(ours, administratively). Telling the principal the break was "on Notion's side"
read as "their system is broken" — imprecise framing of a true mechanism.
Name the mechanism AND the owner of the unblock action in the same breath.

## 5. Transcript-salvage pattern for timed-out subagents

A research subagent that times out with ZERO files written usually still
banked its full measurement trace in
`<agent-home>/cache/delegation/live/<deleg_id>/task-N.log` (one line per
event, tool call + result). Read the transcript, extract the load-bearing
measurements as a labeled fact list (M1, M2, ...), then re-dispatch a
WRITE-ONLY brief: same deliverable, facts pre-digested, "do NOT read files,
do NOT run commands, one write_file call." Salvaged a 900s-timeout plumbing
audit this way at ~2 min cost. Bonus: the digest step is where the parent
catches its own defects — this run the transcript exposed the unbraced-var
bug above.
