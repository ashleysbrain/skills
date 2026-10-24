# MCP Server Production Wiring — session record (2026-08-18, hermes)

Context: QA Pass 23 found the mosaic MCP server functional over stdio
but registered in zero clients ("callable-in-principle, not
serving-anyone"). principal directive: market deep-dive, gap audit, roadmap,
autonomous execution in microtasks. Tasks T-260818-0144..0147 closed;
Phases 1-3 minted as T-0148..0151. CI green runs: 32174698534,
32175194417.

## Root blocker (the one nobody could see)

the operator agent' own MCP client was silently dead: the venv's `pydantic-core`
was 2.48.0 while `pydantic` required exactly 2.46.4 → `import mcp`
raised ModuleNotFoundError (pydantic_core._pydantic_core missing) →
MCP discovery disabled itself with no visible error. Even a registered
server would have loaded zero tools.

FIX (durable, environment-setup class):
```
cd <agent-home>/hermes-agent
./venv/bin/pip install --force-reinstall --no-deps "pydantic-core==2.46.4"
./venv/bin/python -c "from mcp.client.session import ClientSession; import mcp.client.streamable_http as sh; print('ok')"
```
NOTE: installing the *latest* pydantic-core (2.48.0) does NOT fix it —
pydantic pins its exact ABI twin. Must match pydantic's requirement.

## Tool-usage laws discovered (these cost real time)

1. **MCP configs need ABSOLUTE paths.** `hermes mcp add mosaic
   --args "~/your-org/..."` → "Failed to connect: Connection
   closed" because tilde does not expand in subprocess spawn. Absolute
   path connects first try.
2. **Direct ClientSession probe beats `hermes mcp test`.** The CLI was
   blocked by an unrelated interrupted-update cryptography/rust build;
   the raw probe (asyncio + stdio_client + call_tool) is stronger
   evidence anyway — it exercises the same discovery library.
3. **Routing REFUSE on unroutable task text is CORRECT gate behavior.**
   Probe tasks must contain routable keywords ("verify/audit/review")
   or dispatch returns REFUSE "no capability class matched" — which is
   L1+L2 working, not a server bug.
4. **operator_bus.py post flags**: `--type` (not --kind) from
   {handoff,result,status,alert,ping,pong,design_request,design_spec,
   build_request} and `--content` (not --body).

## Market findings (live curl 2026-08-18; web_search/Firecrawl was down)

- Transports: stdio = newline-delimited JSON-RPC over client-launched
  subprocess. 2025-06-18 era moves session metadata to per-request
  `_meta.io.modelcontextprotocol/*`; a stateless request-loop server is
  compliant across BOTH eras (era-safe negotiation: echo known
  2024-11-05/2025-03-26/2025-06-18, fallback oldest).
- Official MCP Registry: preview 2025-09-08, API freeze v0.1 since
  2025-10-24. Listing before v1 GA = rework risk → held in
  superposition, quarterly re-scan.
- @modelcontextprotocol/sdk (TS): v1.30.0, 2026-07-27 — ecosystem live.
- Direct curl to modelcontextprotocol.io + registry + raw.githubusercontent
  works when web tools are unconfigured (direct-source-research fallback).

## CI pattern: machine-state independence

First round-trip CI run (32174366797) FAILED: dispatch GO requires the
technology-registry (~/your-workspace/technology-registry), absent on
the clean ubuntu runner; dispatch_gate correctly fail-stop REFUSEs.
Resolution: `adapters/mcp/mcp_roundtrip_test.py` asserts the CONTRACT
with branch-correct invariants — GO path requires WHO+WHICH+ADMIT join
keys; fail-stop path requires the refusal to name the registry and
carry the routing sub-record. CI logs confirm the clean runner
exercised the fail-stop branch; local runs exercise the GO branch.

## Repo hazard: overnight-volley cron sweeps dirty trees

The overnight-volley bus-intake cron committed my uncommitted
working-tree files (CI workflow + roundtrip test) into ITS commit
(d532224, 19:00:57) — its run failed on the GO-only assertion two
minutes before my own commit landed the same files. Lesson: commit
promptly after VERIFY; don't leave in-flight edits dirty across a
cron tick boundary.

## Deliverables

- `adapters/mcp/mosaic_mcp_server.py` v1.1.0 (era-safe negotiation)
- `adapters/mcp/mcp_roundtrip_test.py` (CI step + manual probe)
- `docs/MCP-PRODUCTION-ROADMAP.md` (findings F1-F6, gaps G1-G8,
  phases 0-4)
- hermes config `mcp_servers.mosaic` (8/8 tools) + sibling-agent.jsonc
  `mcp.mosaic`; message-bus msg 2274
