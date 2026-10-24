# the operator agent Organism - Live Demo Capabilities (Verified 2026-08-01)

All claims below were verified by live-probing the infrastructure, not from documentation.

## Sherman Router (Thalamocortical Routing)
- **Path:** `/<workspace>`
- **Speed:** 0.48-0.80 seconds per route (sub-second, verified)
- **What it does:** Routes arbitrary natural-language queries to specialist engines
- **Output:** Rich JSON trace including auto-selected engine, task type, 7-layer tissue path (epithelial, connective, glia, validation, neural, muscle, cardiovascular), methodology selection, model routing, sub-agent delegation tree
- **Capacity:** 83 engines in registry, 9 neural process agents
- **Test commands:** `python3 sherman_router.py --situation "topic" --compact` or `--gate --situation "topic" --operator hermes`

## Engine Fleet (69 Engines, 13 Body Systems)
- **Status:** 69/69 alive at last check
- **Verified by:** HTTP GET to `localhost:port/vitals`
- **Body systems:** nervous (42 engines), digestive (1), skeletal (1), urinary (1), lymphatic (6), diagnostic (4), process (1), reproductive (7), respiratory (1), cardiovascular (2), muscular (1), endocrine (1), integumentary (1)
- **Per-engine telemetry fields:** oscillator frequencies, golden-ratio weights, transfer latency, integrity scores, uptime, operations counter
- **Sample engine query:** POST `localhost:port/process` with `{"query": "consciousness emergence theory"}` returns structured verdict in ~9ms

## OVS Health Scoring (Physics-Informed 7-Dimension)
- **Endpoint:** `localhost:port/vitals` (live) and `localhost:port/history` (288 snapshots, ~24h at 5-min intervals)
- **7 Dimensions:** COG (cognitive), PIPE (pipeline), RES (resource), KNOW (knowledge), ALIGN (alignment), ADAPT (adaptation), INTER (integration)
- **Formula:** OVS = 0.5 * linear + 0.5 * coupling (21-pair physics-informed coupling matrix)
- **Known anomalies (as of 2026-08-01):** COG=173.3 on GG3 (scoring bug), KNOW=0.0 on both GG3 and the operator agent Live

## Visualization Pipeline
- **Dashboard path:** `/<workspace>` (125KB)
- **NOTE:** Path is under `gigi3/` not `your-workspace/gg3-ops/`
- **Serves at:** `http://localhost:port/gg-live-dashboard.html`
- **Design:** DS phenotype (moonlight gold, indigo, Mucha lines)
- **Auto-refresh:** Fetches :port every 10 seconds, DOM mutation only on data change
- **Components:** OVS score (real-time), 7-dimension radar chart, OVS trend chart (288 data points), dimension trend chart, volatility meter, engine fleet grid (filterable), model tracking panel, error tracking panel
- **Additional dashboards in same directory:** gg-ops-platform.html (1.2MB), agent-health-dashboard.html (159KB), gg-medical-dashboard.html (64KB), gg-command-center.html (64KB), gg-process-graph-3d.html (13KB), task-crystal.html (42KB)

## Topology Data
- **Flows:** 5 topology connections in live data (the `topology.flows` key in vitals JSON)
- **Engines array:** Full list with name, port, body_system, status, cognitive flag, ECS code, telemetry_fields count

## Service Architecture
- **:port** Metrics API (gg3_metrics.py --serve)
- **:port** Medical Records
- **:port** Twin (standby)
- **:port** Sandbox / Dashboard host
- **:9300** Ops Center proxy
- **:port** Nervous System organism view (14 engines)

## Demo Readiness Checklist
- [x] ROUTING: Sub-second live query routing with biological traces
- [x] ENGINE FLEET: 69/69 engines alive, rich per-engine telemetry
- [x] HEALTH METRICS: 7-dimension OVS scoring with 24h history
- [x] VISUALIZATION: Live auto-refreshing dashboard
- [x] STRUCTURED I/O: Arbitrary topics route correctly, produce JSON
- [x] TELEMETRY: Real-time engine health, oscillator data, coupling physics

## For the Constellation Demo Concept
The "constellation" idea (mapping all 316 conference theories by architectural resonance) is feasible:
- Each theory routed through Sherman at ~0.5s per route
- 316 routing calls = ~2.6 minutes of pre-compute (offline-safe)
- Each route activates different body systems/engines
- Theories sharing activation patterns are "architecturally resonant"
- This produces a unique network graph per conference
