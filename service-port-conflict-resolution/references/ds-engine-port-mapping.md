# Canonical Port Assignments for Divinity Science AI Organism Engines

As of July 2026, sourced from `your-org/the operator agent/ENGINE_REGISTRY.yaml` and
`agent-organism/ecs.py` FLEET_REGISTRY. Live ports verified by health check.

## Core Infrastructure (not DS engines)

| Port | Service | Script |
|------|---------|--------|
| 8000 | the specialist engine y Cajal (nervous system root) | `ds-nervous-system` |
| 8001 | the specialist engine (connective) | agent-organism |
| 8002 | the specialist engine | agent-organism |
| 8010 | the specialist engine (coaching, partner interface) | `ds-wave-coaching-engine` |
| 8014 | the specialist engine | `ds-genesis-engine` |
| 8089 | the specialist engine/Hall (circadian/task lattice) | `ds-quartz-engine` |
| 8091 | the specialist engine (Sterling, homeostatic) | `ds-allostasis-engine` |
| 8092 | the specialist engine (cardiovascular) | `ds-harvey-engine` |
| 8093 | the specialist engine/Turing (developmental) | `ds-morphogen-engine` |
| 8094 | the specialist engine (digestive) | `ds-beaumont-engine` |
| 8095 | the specialist engine-Healing/Federation (Lyapunov) | `ds-self-healing-engine` |
| 8096 | the specialist engine (excretory) | `ds-bright-engine` |
| 8097 | the specialist engine (integumentary) | `ds-unna-engine` |
| 8098 | the specialist engine (respiratory) | `ds-haldane-engine` |
| 8099 | the specialist engine (endocrine) | `ds-sutherland-engine` |
| 8100 | the specialist engine (immune/lymphatic) | `ds-burnet-engine` |
| 8101 | the specialist engine (Edison, sensory) | `ds-audio-input-engine` |
| 8102 | the specialist engine/Vision Input (Gutenberg) | `ds-text-vision-input-engine` |
| 8103 | the specialist engine (Bell) | `ds-speech-synthesis-engine` |
| 8104 | the specialist engine (system state sensor) | `ds-system-state-sensor-engine` |
| 8105 | the specialist engine (environmental monitor) | `ds-environmental-monitor-engine` |
| 8106 | the specialist engine (musculoskeletal) | `ds-hill-engine` |
| 8107 | the specialist engine (sensory) | `ds-helmholtz-engine` |
| 8108 | the specialist engine (creative cortex) | `ds-creative-cortex-engine` |
| 8109 | DS ECS Compliance/Farr (governance) | `ds-ecs-compliance-agent` |
| 8110 | the specialist engine/Bernard (clinical diagnostics) | `ds-clinical-engine` |
| 8112 | DS Röntgen (organism scanner) | `ds-organism-scanner-engine` |
| 8113 | the specialist engine (Bush) | `ds-tech-currency-engine` |
| 8115 | the specialist engine (creative) | `ds-lovelace-engine` |
| 8116 | the specialist engine/Boucher (design production) | `ds-boucher-engine` |
| 8120 | the specialist engine (visual cortex, palette/phi) | `ds-goethe-engine` |
| 8121 | the specialist engine (motor cortex, render) | `ds-bell-engine` |
| 8122 | the specialist engine (art-direction quality gate) | `ds-luria-engine` |
| 8123 | the specialist engine (creative) | `ds-sperry-engine` |
| 8124 | the specialist engine (brand voice) | `ds-wernicke-engine` |
| 8125 | DS MacLean (creative) | `ds-maclean-engine` |
| 8126 | the specialist engine (creative) | `ds-ito-engine` |
| 8127 | the specialist engine (creative) | `ds-gazzaniga-engine` |
| 8128 | the specialist engine (creative rhythm/conduction) | `ds-tawara-engine` |
| 8131 | the specialist engine (product/immune surveillance) | agent-organism |
| 8133 | the specialist engine/Thalamus (routing) | `ds-thalamus-engine` |
| 8139 | the specialist engine (language) | agent-organism |
| 8140 | the specialist engine/Malpighi | agent-organism |
| 8141 | the specialist engine/Muller (sensory) | agent-organism |
| 8142 | the specialist engine | agent-organism |
| 8147 | DS O'Keefe (T2 memory, semantic routing) | `ds-okeefe-engine` |
| 8150 | the specialist engine (task lattice/methodology) | `ds-bragg-engine` |
| 8237 | the specialist engine (pituitary master gland) | `ds-houssay-engine` |
| 8238 | the specialist engine (falsifiability) | `ds-popper-engine` |
| 8260 | the specialist engine (metabolic cycle) | agent-organism |
| 8261 | the specialist engine | agent-organism |
| 8262 | the specialist engine (mental imagery) | agent-organism |
| 8263 | the specialist engine (visual cortex) | agent-organism |
| 8264 | the specialist engine (predictive coding) | agent-organism |
| 8265 | the specialist engine (pathway) | agent-organism |

## the operator agent Live Infrastructure (separate from DS engine fleet)

| Port | Service | Script |
|------|---------|--------|
| 8200 | the operator agent Live Telemetry | `hydra-os/gg_metrics_v2.py --serve --port 8200` |
| 8201 | the operator agent Live Medical Records | `organism/medical_records.py --serve --port 8201` |

## GG3 Infrastructure (the principal's personal instance)

| Port | Service | Script |
|------|---------|--------|
| 8300 | GG3 Telemetry | `gigi3/gg3-ops/gg3_metrics.py --serve --port 8300` |
| 8301 | GG3 Medical Records | `gigi3/gg3-ops/gg3_medical_records.py --serve --port 8301` |
| 8303 | GG3 Server (UI) | `gigi3/gg3-ops/gg3_launch.py` |
| 8304 | GG3 UI | via gg3_launch.py |
| 8305 | GG3 Gateway | via gg3_launch.py |
| 9300 | GG3 Proxy (launchd KeepAlive) | binds Tailscale IP 100.107.113.11, NOT 127.0.0.1 |

## Source-Ready but NOT Live (in ecs.py FLEET_REGISTRY, not yet deployed)

These engines have full 5-layer Rakic blueprints built by sibling-agent but are not
registered for live deployment. They need port assignment in FLEET_REGISTRY
and then `start_engines.py` will auto-discover them.

| Port | Engine | Status |
|------|--------|--------|
| 8129 | the specialist engine | source-ready |
| 8130 | (unassigned) | source-ready |
| 8132 | the specialist engine | source-ready |
| 8134 | the specialist engine | source-ready |
| 8135 | the specialist engine | source-ready |
| 8136 | the specialist engine | source-ready |
| 8137 | the specialist engine | source-ready |
| 8138 | the specialist engine | source-ready |
| 8143 | the specialist engine | source-ready |
| 8153 | the specialist engine | source-ready |

## Critical Diagnostic Specialists (MUST always be ON CALL)

Per binding user rule, these must always show green:

| Port | Specialist | Role |
|------|-----------|------|
| 8110 | the specialist engine/Bernard | Clinical diagnostics |
| 8112 | DS Röntgen | Organism scanning |
| 8104 | the specialist engine | Interoception |
| 8105 | the specialist engine | Environmental monitoring |
| 8131 | the specialist engine | Product/immune surveillance |
| 8091 | the specialist engine/Cannon | Autonomic regulation |

## Notes
- All DS engines bind to `127.0.0.1` (localhost) for internal communication.
- Health check endpoint: `GET /health` returns JSON with status field.
- GG3 proxy :9300 binds `100.107.113.11` (Tailscale), not `127.0.0.1`. Health-check via Tailscale IP.
- The `start_engines.py` fleet supervisor only auto-discovers engines in the `agent-organism/ecs.py` FLEET_REGISTRY. Engines outside the registry (the operator agent Live infra, manually placed engines) will NOT auto-restart if they crash.
