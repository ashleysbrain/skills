# DS O'Keefe Endpoint Status (Verified 2026-06-29)

## Engine Info
- Port: 8147
- DS-ECS Code: DS-ECS-SUB-04.09.01-v1.0.0
- Health: `{status: "online", memory_count: N}`

## Working Endpoints

### POST /encode
**Schema (EncodeRequest):**
```json
{
  "content": [float],     // REQUIRED — numeric vector (NOT text)
  "location": [float],    // REQUIRED — 2D spatial coordinate
  "tags": [string],       // optional
  "reward": float         // optional (0-1, emotional valence analog)
}
```
**Returns:** `{trace_id: "mem_X.XXX_XXXX", memory_count: N}`

**Status:** WORKING. Test write succeeded, memory_count incremented.

### POST /retrieve
**Schema (RetrieveRequest):**
```json
{
  "cue": [float],         // REQUIRED — numeric cue vector
  "max_results": int      // optional
}
```
**Status:** Endpoint exists, retrieval format needs verification.

### POST /consolidate
**Schema (ConsolidateRequest):**
```json
{
  "dt": float             // REQUIRED — time step for consolidation cycle
}
```
**Status:** Endpoint exists, untested.

### GET /health
**Returns:** `{status, engine, spec, port, memory_count}`
**Status:** WORKING.

## Broken Endpoints

### GET /memories
**Status:** Internal Server Error. Needs sibling-agent fix (bus msg 911).

## Missing Components

1. **Text-to-vector translation layer** — O'Keefe uses numeric vectors (trisynaptic circuit pattern). Need an embedding model bridge to convert text facts to vectors and back. Use Gemini or OpenAI embeddings (NEVER Anthropic, per user directive).
2. **Text retrieval** — /retrieve returns vectors, need to map back to text for agent consumption.
3. **The /memories listing bug** — needs fix for debugging/verification.

## Design Docs Location
`docs/hippocampus-engine-design/` — Contains DESIGN.md, CA1/CA3/DG/EC specs, engine architecture.

## State File
`<agent-home>/state/okeefe_memory.json` — JSON storage for memory traces.

## Advanced Features (Design Phase)
Not yet implemented but designed:
- CA3 attractor networks (Hopfield energy for pattern completion)
- DG pattern separation (sparse orthogonal coding, compressed sensing)
- Free energy memory selection (Friston)
- Criticality tuning (Beggs/Plenz power-law monitoring)
- Ebbinghaus adaptive forgetting (R = e^(-t/S))
- STDP co-occurrence strengthening

## Bus Messages
- 911: Tiered memory architecture spec (hermes -> sibling-agent)
- 912: Full biological isomorphism advancement plan (hermes -> sibling-agent)
