# MCP 2026-07-28 ("stateless era", community "2.0") — spec digest + organism landing map

Source: modelcontextprotocol.io specification changelog, curl-fetched full
text, 2026-08-20. Primary-source verified. Community calls it "2.0" because
it is a hard break from the 2025-11-25 stateful redesign.

## What changed

1. **Stateless core** — `initialize` handshake REMOVED as a requirement.
   Version + capabilities ride in `_meta` per request. Servers can
   crash/restart without session loss.
2. **`server/discover` RPC** — servers MUST advertise protocol versions,
   capabilities, identity before clients select a version.
3. **`subscriptions/listen`** — single long-lived POST stream replaces
   `resources/subscribe`; opt-in change notifications with subscriptionId
   tags (toolsListChanged etc.).
4. **MRTR** — server returns `resultType: input_required` + `inputRequests`;
   client retries with `inputResponses`. Replaces server-initiated
   roots/sampling/elicitation.
5. **Tasks extension** — official `io.modelcontextprotocol/tasks`:
   `tasks/get` polling, `tasks/update` client input, unsolicited handles.
6. **`ttlMs` + `cacheScope`** on all list/read results (skip redundant
   polls).
7. **OpenTelemetry** traceparent/tracestate/baggage in `_meta`.
8. **Error codes renumbered** -32020..-32099 spec-reserved.

## Deprecated (12-month removal window — do-not-build list)

Roots, Sampling, Logging (use stderr/OTel), HTTP+SSE transport, OAuth
Dynamic Client Registration (replaced by Client ID Metadata Documents).

## Where each landed in the organism (2026-08-20, bus #2575/#2577/#2580)

| Mechanism | Landing |
|---|---|
| server/discover | `your-stack/adapters/mcp/mosaic_mcp_server.py` v1.2.0 (identity: Divinity Science owner, PhysioCore exclusive global license) |
| subscriptions/listen | same server — registers, stdio emission disclosed-static |
| stateless _meta requests | same server — no-handshake tools/call verified live |
| ttlMs/cacheScope | same server (tools/list ttlMs=300000) + prober snapshot |
| fleet era-detection | `your-stack/adapters/mcp/mcp_discover_probe.py` (discover probe + legacy initialize fallback, transition-only drift-to-bus) |
| self-healing sensing | `organism/real_sensors.py` `sense_mcp` (telemetry-only dim; self-refresh >900s; launchd tick `com.your-org.self-healing-loop`) |
| tasks extension | NOT built — declared "planned" in discover payload; sibling-agent lane (bus tasks-alignment) |
| MRTR, OTel | not yet adopted |

## Fleet snapshot at adoption

10 enabled servers (13 disabled not probed): `mosaic` = only
stateless-2026-07-28 server in fleet; 8 legacy-era alive; context7 HTTP 400
(dead, baselined). Snapshots: `~/your-org/organism/registry-live/`.

## Open follow-ups

- Bus alignment to tasks extension (idempotent `tasks/get` polling replaces
  re-escalation; fixes #2561-class duplicate handoffs) — sibling-agent lane.
- A2A v1.0 Agent Cards share identity fields with discover — one emit can
  serve both (fold into registry reconciliation #2566).
- the operator agent-side MCP client era-compat verification before relying on
  2.0-only features.
