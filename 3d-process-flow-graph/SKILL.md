---
name: 3d-process-flow-graph
description: Build 3D force-directed process flow GRAPHS (not viewers) for the the operator agent organism. Editable with add/remove nodes, draw connections, delete links. Palantir-inspired ontology layers, fungal curved links with flowing particles, breathing glow nodes, the operator agent phenotype.
version: 2.0.0
category: software-development
---

# 3D Process Flow Graphing Tool

Use when building or modifying the 3D process flow graph for the the operator agent organism. This is a GRAPHING TOOL, not a read-only visualization. Users must be able to add nodes, draw connections between them, delete nodes and links, and edit properties — a 3D Visio, not a picture.

## CRITICAL LESSON: Build a Tool, Not a Viewer

The user explicitly asked for "a 3D version of Visio or some other graphing tool." The first build was a read-only viewer. The user rejected it: "you completely deleted some of the really cool functions i told you i loved and you arent finishing the work."

**Rule: When the user says "graphing tool" or "Visio," they mean EDITABLE.** The graph must support:
- Add node (click background in edit mode)
- Connect nodes (click source, then click target)
- Delete node (right-click in edit mode)
- Delete link (click link in edit mode)
- Edit properties (detail panel with edit actions)

If you build a viewer, you have not completed the task.

## Architecture

Three files in `hydra-os/`:
- `gg-process-graph-3d.html` — standalone HTML shell with sidebar, canvas, edit controls, status bar, detail panel
- `gg-process-graph-data.js` — the ontology data model (94 nodes from FLEET_REGISTRY, 153 edges, 12 pipelines)
- `gg-process-graph-app.js` — application logic with editing, layer toggle, pipeline highlight, node detail, breathing animation

Data was generated from the real `agent-organism/ecs.py` FLEET_REGISTRY (68 engines + 2 legacy aliases). Every engine in the fleet is represented.

## 3-Layer Ontology Model (Palantir-inspired)

Researched Palantir Foundry ontology (YouTube video by Chad Wahlquist, Nov 2025). Their model is Data + Logic + Actions. Maps to our 3 layers:

1. **Semantic** (Data) — tissue connections between engines (static structure). All engines and their physical wiring.
2. **Kinetic** (Logic) — process flow paths overlaid on topology. Which engines fire in what order for each pipeline.
3. **Dynamic** (Actions) — gates, conditions, feedback loops only. Decision points and non-linear patterns. Uses `dagMode(null)` for free-form layout.

## Fungal/Mycelial Aesthetic (USER REQUIREMENT)

The user explicitly said "I really really love the visual for the fungal network." This aesthetic MUST be applied to the 3D graph, not just the 2D SVG in the Birthing Center.

Key visual elements:
- **Curved links** via `linkCurvature()`. Feedback loops curve at 0.5 (semi-circular), cross-flows at 0.3, conditionals at 0.2, sequential at 0.15. Straight lines look dead.
- **Flowing data particles** (spores): 3 particles per active link, traveling source to target. Use `linkDirectionalParticles(3)`, `linkDirectionalParticleSpeed(0.003)`, `linkDirectionalParticleWidth(2)`.
- **Breathing glow halos** on engine nodes: a `requestAnimationFrame` loop pulses opacity (0.08 plus/minus 0.04 sine) and scale (1 plus/minus 0.05 sine) on the glow mesh objects. Mark them with `userData.isGlow = true` for traversal.
- **Grain overlay**: SVG fractal noise at 0.025 opacity, `mix-blend-mode: overlay`.

## Edge Types

| Type | Color | Curvature | Description |
|------|-------|-----------|-------------|
| sequential | moonlight | 0.15 | A then B |
| parallel_fork | indigo-light | 0.15 | A spawns B + C simultaneously |
| parallel_join | teal | 0.15 | B + C merge into D |
| conditional | amber | 0.20 | A goes to B IF condition, else C |
| feedback | red | 0.50 | B sends back to A (loop) |
| cross_flow | indigo (dim) | 0.30 | Engine shared across pipelines |
| tissue | dusk (dim) | 0.15 | Physical tissue connection |

## Node Types and 3D Shapes

| Type | Shape | Color Source |
|------|-------|-------------|
| engine | Sphere + breathing glow halo | Body system color |
| gate | Octahedron (diamond) | Amber |
| router | Torus | Indigo-light |
| source | Small sphere + ring | Green |
| sink | Dark sphere + ring | Dusk |

## Three.js Loading in the Ops Platform

The `3d-force-graph` UMD bundle does NOT expose `THREE` as a global. See `references/threejs-loading-patterns.md` for the importmap + ES module + retry solution. This is critical for any custom `nodeThreeObject` or `linkThreeObject` callback in the ops platform.

## Edit Mode Implementation

See `references/editing-api.md` for the full editing API details and code patterns.

Key functions:
- `toggleEditMode()` — toggles edit state, shows/hides hint bar, changes cursor
- `toggleConnectMode()` — enters connect mode (click source then target)
- `showAddNodeDialog(coords)` — uses `graphInstance.screen2GraphCoords(offsetX, offsetY, 0)` to get 3D position from click
- `addConnection(sourceId, targetId)` — prompts for edge type and condition
- `deleteNode(nodeId)` — removes node and all connected edges
- `deleteConnection(edgeData)` — removes a single edge
- `updateGraph()` — preserves existing node positions when data changes (critical for not disorienting the user)

## Integration

In `gg-ops-platform.html`, the Process Flows sub-tab has a List View / 3D Ontology Graph toggle. The 3D view embeds the standalone tool via iframe. `switchFlowView('3d')` and `switchFlowView('list')` toggle between views.

The ops platform's existing flow editor (drag-and-drop stages, gate editor, engine selector) is NOT replaced. It coexists as the "List View." The 3D graph is the "3D Ontology Graph" view.

## Font Loading (CRITICAL)

Standalone HTML tools MUST load fonts via `<link>` tags. CSS variables alone do NOT load fonts:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

Without these tags, the browser falls back to system fonts (Helvetica/SF Mono), which looks AI-generated. The user detected this immediately. **JetBrains Mono** for monospace (canonical per `ds-engine-shared/phenotype_ds.py`). IBM Plex Mono was REJECTED 2026-07-13 ("I do NOT like that font" — its dotted zeros). All numeric elements need `font-feature-settings: "tnum" 1, "zero" 1` on the `body` element. When swapping fonts across files, grep ALL HTML files in the directory (`grep -rn "IBM.Plex" *.html *.js`), not just the active one — the 2026-07-13 fix touched 8 files.

## Data Generation

NEVER hardcode engine lists. The graph data (`gg-process-graph-data.js`) now fetches LIVE from the ECS Registry API at `:port/api/ecs/registry` (69 real engines with dependency_graph, body_systems, categories), pipeline definitions from `:port/api/ecs/pipeline-usage` (10 real pipelines with stages, gates, route_rules), topology from `:port/topology` (real upstream/downstream wiring), and live engine status from `:port/` (alive/dead state per node). The old static 94-node hardcoded array was replaced with `fetchOntology()` — an async function that builds the ONTOLOGY object from real API responses. See `scripts/generate-graph-data.py` for the original static generator (now superseded by live fetch).

### API field name mapping (CRITICAL — caused rendering failure)

The registry API (`:port/api/ecs/registry`) returns engines with field `name` (dir name like `ds-allostasis-engine`) and `engine_name` (display name like `the specialist engine`). Code that referenced `eng.dir` or `eng.display_name` failed silently. Always use `eng.name` for the dir and `eng.engine_name` for display. Similarly, `eng.cognitive_layer` (not `eng.cognitive`).

### Browser fetch URL: use 127.0.0.1 not localhost

Browser fetches to `http://localhost:port/` fail silently on macOS when the browser tries IPv6 (`::1`) first and the server only listens on IPv4 (`127.0.0.1`). Always use `http://127.0.0.1:PORT/` in browser-side fetch calls. This caused spawn-requests and graph-data fetches to fail with no visible error.

### Default layer must be "all" not "semantic"

The graph defaults to `currentLayer='semantic'` which only shows tissue edges (16 of 120). This makes the graph look nearly empty. Default to `currentLayer='all'` so all 120 edges are visible on load. Add an "All" button to the layer toggle UI as the first (active) option.

## Mycelial Visual System (v3 rebuild — 2026-07-13)

The user explicitly said "the 3d graph view of the work board still looks like random floating dots and NOT like the fungal network. this didn't get changed at all." The original v2 build had curved links and breathing glow, but the links were thin lines (width 0.5-2.5px) and nodes were small spheres — visually it looked like a standard node-link diagram, not a fungal network. A full visual rebuild was needed.

### Thick Mycelial Tubes (not thin lines)

The `3d-force-graph` library renders links as **3D cylinder tubes** when `linkWidth > 1` and as **thin lines** when `linkWidth <= 1`. The original build used widths 0.5-2.5, so most links rendered as hairlines. Rebuild uses widths 2-6:

```javascript
function getEdgeWidth(e){
  if(activePipeline&&e.pipeline===activePipeline)return 6;
  if(e.type==='feedback')return 4;
  if(e.type==='cross_flow')return 2.5;
  if(e.type==='tissue')return 2;
  return 3;
}
```

Edge opacity also boosted from 0.12-0.4 range to 0.35-0.7 range in `EDGE_TYPES`.

### Atmospheric Rendering Layer

Three additions transform a standard graph into a fungal network:

1. **Fog** — `scene.fog = new THREE.FogExp2(0x080d1a, 0.0035)` adds depth falloff. Nodes in the distance fade into the background, creating the sense of peering into a 3D space.

2. **Ambient spore particles** — 800 `THREE.Points` objects drifting in a spherical shell (radius 120-350) around the graph. Each spore has a random velocity (±0.15/axis/frame), wraps when it exits the shell. Colors from palette: moonlight [0.91,0.84,0.63], indigo [0.39,0.40,0.95], teal [0.29,0.84,0.71], dimmed 0.3-0.7. Uses a canvas-generated radial gradient texture for soft circular sprites with `THREE.AdditiveBlending`.

3. **Enhanced lighting** — Replace default lights with: `AmbientLight(0x1a2035, 0.6)` + `PointLight(0xe8d5a0, 0.8, 300)` at (0,100,50) + `PointLight(0x6366f1, 0.5, 300)` at (-100,-50,-80) + optional `PointLight(0x4ad6b4, 0.3, 200)` at (100,-80,60). The warm moonlight + cool indigo creates a bioluminescent feel.

### Bioluminescent Node Rendering

Custom `nodeThreeObject` creates multi-layer glow per node:
- **Core sphere**: `MeshPhongMaterial` with `emissive` color and `emissiveIntensity: 0.3` (alive) or `0.05` (dead)
- **Inner glow halo**: `MeshBasicMaterial` with `opacity: 0.2`, `blending: AdditiveBlending`, `depthWrite: false`
- **Outer bioluminescent halo**: same but `opacity: 0.08`, larger radius
- **Dead engines**: red torus ring around the node
- **Expedite work orders**: golden pulse ring with `userData.isPulseRing = true`

Breathing animation traverses scene for `userData.isGlow` and `userData.isOuterGlow` objects, modulating opacity and scale on sine waves with different phases.

### Glow Sheath on Links

Custom `linkThreeObject` adds a wider translucent cylinder (2.5× the link width) with `AdditiveBlending` around each link, creating a glow effect. The built-in renderer draws the solid tube; the custom object adds the glow sheath.

## CRITICAL: Two Separate 3D Graphs in the Ops Platform

The ops platform (`gg-ops-platform.html`) has TWO completely separate 3D graph instances:

1. **`taskGraphInstance`** (container: `#taskGraph3d`) — the Work Board's "3D Graph View" button. Renders work orders as nodes with dependency links. This is what the user sees when clicking "3D Graph View" on the Work Board. Originally had `linkWidth(0.5)` (hairlines) and no custom node objects — looked like "random floating dots."

2. **`graphInstance`** (in iframe loading `gg-process-graph-3d.html`) — the Process Flows "3D Ontology Graph" toggle. Renders the full engine ontology (130 nodes, 120 edges).

**When the user says "the 3D graph looks like random floating dots," they almost certainly mean `taskGraphInstance` on the Work Board**, not the ontology graph. Both must have the mycelial visual system applied. The `initTaskGraph()` function must be rebuilt with the same fungal visuals (thick tubes, glow nodes, fog, spores, enhanced lighting) as the ontology graph.

### THREE.js Not Exposed by 3d-force-graph UMD Bundle

The `3d-force-graph` UMD bundle from unpkg includes Three.js internally but does NOT expose `THREE` as a global variable. Custom `nodeThreeObject` and `linkThreeObject` callbacks that reference `THREE.SphereGeometry`, `THREE.MeshPhongMaterial`, etc. will fail with `THREE is not defined`.

**Solution**: Add an importmap + ES module script to load Three.js and assign to `window.THREE`:

```html
<script src="https://unpkg.com/3d-force-graph"></script>
<script type="importmap">
{ "imports": { "three": "https://unpkg.com/three@0.160.0/build/three.module.js" } }
</script>
<script type="module">
import * as THREE from 'three';
window.THREE = THREE;
</script>
```

**CRITICAL**: ES module scripts load asynchronously. Regular `<script>` tags that call `initTaskGraph()` will run BEFORE `window.THREE` is assigned. Must add retry logic:

```javascript
function ensureTaskTHREE() {
  if (taskTHREE) return taskTHREE;
  if (typeof THREE !== 'undefined') taskTHREE = THREE;
  return taskTHREE;
}

function initTaskGraph() {
  var T = ensureTaskTHREE();
  if (!T) {
    // THREE.js not loaded yet (ES module still loading) — retry in 200ms
    setTimeout(initTaskGraph, 200);
    return;
  }
  // ... rest of init
}
```

All custom Three.js code in the ops platform must use `var T = ensureTaskTHREE()` at the top of each function and reference `T.SphereGeometry` etc., NOT `THREE.SphereGeometry` directly.

**Standalone HTML pages** (`gg-process-graph-3d.html`) can load Three.js separately via `<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r150/three.min.js"></script>` (r150 is the last version that ships a UMD build exposing `THREE` globally). But r160+ from any CDN uses ES modules only and will NOT expose `THREE` as a global without the importmap approach.

**DO NOT** try to extract THREE from the 3d-force-graph internal bundle via prototype chain traversal, constructor inspection, or temporary graph instances. This was attempted and failed — the UMD closure does not leak the THREE namespace. Use the importmap approach.

## Pitfalls

See `references/task-graph-data-population.md` for the Work Board task graph data structure fixes (topology object iteration, null cache crash, always-visible labels, API getter functions).

- **Building a viewer instead of a tool.** When the user says "graphing tool" or "Visio," they mean EDITABLE. If you cannot add/remove/connect in the graph, you have not completed the task.
- **Forgetting the fungal aesthetic.** The user loves the fungal network visual. Curved links, flowing particles, breathing glow are all mandatory, not optional. Straight lines and static nodes look dead.
- **Thin links = "random floating dots."** `linkWidth <= 1` renders as hairline lines. The user sees dots with invisible connections. Always use `linkWidth >= 2` for visible mycelial tubes. The library renders links as 3D cylinders when width > 1.
- **Two separate graphs — verify which one the user means.** The Work Board "3D Graph View" (`taskGraphInstance`) and the Process Flows "3D Ontology Graph" (`graphInstance` in iframe) are completely separate. Both need the mycelial visual system. When the user says "the 3D graph looks like dots," check which graph they're looking at.
- **THREE not defined in ops platform.** The `3d-force-graph` UMD does not expose THREE globally. Use importmap + ES module + retry logic. Do NOT attempt prototype chain extraction.
- **Missing font loading.** Standalone HTML pages must load Inter + JetBrains Mono via Google Fonts link tags. CSS vars alone do not load fonts. The user spots system fonts instantly. IBM Plex Mono was REJECTED (dotted zeros) — use JetBrains Mono (canonical per `ds-engine-shared/phenotype_ds.py`).
- **Font features must be on `body`, not just specific selectors.** `font-variant-numeric:tabular-nums` and `font-feature-settings:'tnum' 1,'zero' 1` set only on `.bb-vital-val` etc. means most numbers on the page do not get tabular numerals or dotted zeros. Put them on the `body` element so ALL text inherits them. User detected this across multiple sessions — if you only set it on specific CSS selectors, the body computed style shows `normal` and most numbers on the page do not get tabular numerals or dotted zeros.
- `ForceGraph3D().d3Force('charge').strength(-120)` returns the force object, NOT the graph instance. Do NOT chain `.nodeLabel()` after it. Set force strength in a separate statement after the chain ends.
- Three.js geometries need `Math.max(0.5, radius)` guards to prevent zero-size geometry errors.
- The `dagMode` should be set to `null` (not a string) for the Dynamic layer to allow free-form feedback loop layout.
- Body system colors override node type colors for engines. Both must be defined.
- **Hardcoded data = missing engines.** Always generate from FLEET_REGISTRY. A manual subset will always be incomplete (first build missed 40 of 69 engines).
- **Cross-reference pipelines.** The ops platform PIPELINES object and the 3D graph pipelines array must match. Any pipeline in one must be in the other (saas_sync and app_action were missed in the first build).
- **Position preservation on update.** When `updateGraph()` is called after editing, existing nodes must keep their positions. Store positions from the old graph data and restore them on the new data before calling `graphData()`. Without this, the entire graph flies around every time you add a node.
- **`d3ReheatSimulation()`** must be called after `graphData()` update to restart the force layout with the new data.
- **Cross-reference ALL pipelines.** After generating graph data, compare pipeline IDs against the ops platform `PIPELINES` object. Every pipeline in one must exist in the other. In this session, `saas_sync` and `app_action` existed in the ops platform but were missing from the 3D graph. Also check `ENGINE_PALETTE` for engines that exist as aliases (the specialist engine = speech synthesis alias, the specialist engine = rhythm legacy alias) and add them as nodes.
- **`ORGANISM_DATA.topology` is an object, NOT an array.** The structure is `{ engines: { "the specialist engine": { upstream: ["the specialist engine"], downstream: ["the specialist engine", "the specialist engine"] }, ... } }`. Iterating with `topology.forEach()` crashes (`topology.forEach is not a function`). Use `Object.keys(topology.engines).forEach()` and traverse each engine's `downstream` array to build edges. This caused `updateTaskGraph()` to fail silently with 0 nodes.
- **`flowPipelineCache` can be null at runtime.** `Object.keys(null)` throws `TypeError: Cannot convert undefined or null to object`. Always null-check before `Object.keys()`: `var pKeys = (cache && typeof cache === 'object') ? Object.keys(cache) : [];`. This crashed `updateTaskGraph()` even when topology data was valid.
- **3d-force-graph getters are FUNCTIONS, not properties.** `taskGraphInstance.scene` is a function (constructor name `Function`), not a Scene object. Call `taskGraphInstance.scene()` to get the actual THREE.Scene. Same for `graphData()` — call it to get `{ nodes, links }`. Checking `taskGraphInstance.scene.fog` without calling `scene()` will silently return undefined.
- **Always-visible node labels require Sprite + CanvasTexture.** The 3d-force-graph `nodeLabel()` only shows on hover. For always-visible labels, create a `THREE.Sprite` with a `CanvasTexture` drawn via 2D canvas (`fillText`), set `depthTest: false` so it renders through other objects, and add it as a child of the node group. Position below the node at `y: -baseSize * 2.5`. Scale to `(24, 6, 1)`. Without this, users see "just dots" with no context.
- **When work orders have no dependencies, the graph is just dots.** Populate the task graph with engine topology nodes (from `ORGANISM_DATA.topology.engines`) and pipeline stage nodes in addition to work orders. This creates mycelial flows even when WOs have no `blockedBy` or `parent` relationships. The user expects to see connected flows, not isolated dots.
- **Use `linkCurvature()` for mycelial aesthetic.** The 3d-force-graph API supports curved links via `linkCurvature(fn)`. Without it, links are straight lines and the graph looks dead. The user explicitly loves the fungal network aesthetic. Feedback loops should curve at 0.5, cross-flows at 0.3, sequential at 0.15.
- **Breathing animation requires `requestAnimationFrame`.** Create a global `breathPhase` counter, increment it each frame, traverse the scene for objects with `userData.isGlow = true`, and modulate their `material.opacity` and `scale` on a sine wave. This is what makes the graph feel alive.
- **`screen2GraphCoords` for click-to-add-node.** When the user clicks empty background in edit mode, use `graphInstance.screen2GraphCoords(event.offsetX, event.offsetY, 0)` to convert screen coordinates to 3D graph coordinates for the new node's initial position.
