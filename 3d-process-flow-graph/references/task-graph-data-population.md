# Task Graph Data Population (Work Board 3D View)

## Problem

The Work Board "3D Graph View" (`taskGraphInstance` in `gg-ops-platform.html`)
showed 0 nodes despite having 3 work orders and 69 engines in `ORGANISM_DATA`.
Two runtime crashes prevented data from loading:

1. `flowPipelineCache` was null → `Object.keys(null)` threw
2. `ORGANISM_DATA.topology` was treated as an array → `topology.forEach is not a function`

## Root Cause: ORGANISM_DATA.topology Structure

The topology is NOT a flat array of `{ source, target }` edges. It is:

```javascript
ORGANISM_DATA.topology = {
  engines: {
    "the specialist engine": { upstream: ["the specialist engine"], downstream: ["the specialist engine", "the specialist engine"] },
    "the specialist engine": { upstream: ["the specialist engine"], downstream: ["the specialist engine", "the specialist engine"] },
    // ... 13+ engines
  }
}
```

## Correct Iteration Pattern

```javascript
var topo = (typeof ORGANISM_DATA !== 'undefined' && ORGANISM_DATA &&
            ORGANISM_DATA.topology && ORGANISM_DATA.topology.engines)
           ? ORGANISM_DATA.topology.engines : {};
var addedLinks = {};
Object.keys(topo).forEach(function(engineName) {
  var eId = 'engine_' + engineName;
  if (!nodeIds[eId]) {
    // Find engine in ORGANISM_DATA.engines for richer node info
    var engInfo = null;
    if (ORGANISM_DATA.engines) {
      for (var i = 0; i < ORGANISM_DATA.engines.length; i++) {
        if (ORGANISM_DATA.engines[i].name === engineName) { engInfo = ORGANISM_DATA.engines[i]; break; }
      }
    }
    nodes.push({
      id: eId,
      name: engineName + (engInfo && engInfo.code ? ' [' + engInfo.code.substring(0, 20) + ']' : ''),
      status: (engInfo && engInfo.alive) ? 'engine' : 'backlog',
      val: 4,
      group: 'engine'
    });
    nodeIds[eId] = true;
  }
  // Add downstream connections (avoid duplicates)
  var downstream = topo[engineName].downstream || [];
  downstream.forEach(function(targetName) {
    var tId = 'engine_' + targetName;
    var linkKey = eId + '->' + tId;
    if (!addedLinks[linkKey]) {
      addedLinks[linkKey] = true;
      if (!nodeIds[tId]) {
        nodes.push({ id: tId, name: targetName, status: 'engine', val: 4, group: 'engine' });
        nodeIds[tId] = true;
      }
      links.push({ source: eId, target: tId, type: 'topology', color: '#3a6b6b' });
    }
  });
});
```

## Null-Safe flowPipelineCache Access

```javascript
// WRONG — crashes if flowPipelineCache is null
var pipelines = typeof flowPipelineCache !== 'undefined' ? flowPipelineCache : {};
Object.keys(pipelines).forEach(...)  // Object.keys(null) throws!

// CORRECT — null-checked
var pipelines = (typeof flowPipelineCache !== 'undefined' && flowPipelineCache)
                ? flowPipelineCache : {};
```

## Always-Visible Text Labels (Sprite Pattern)

`nodeLabel()` only shows on hover. For permanent labels:

```javascript
// Inside createTaskNodeObject(node), after glow spheres:
var label = node.name || node.id || '';
if (label.length > 40) label = label.substring(0, 37) + '...';
var lc = document.createElement('canvas');
lc.width = 256; lc.height = 64;
var lctx = lc.getContext('2d');
lctx.fillStyle = 'rgba(8,13,26,0.85)';
lctx.fillRect(0, 0, 256, 64);
lctx.strokeStyle = color;  // node's status color
lctx.lineWidth = 2;
lctx.strokeRect(1, 1, 254, 62);
lctx.font = 'bold 14px Inter, sans-serif';
lctx.fillStyle = '#e8d5a0';
lctx.textAlign = 'center';
lctx.textBaseline = 'middle';
lctx.fillText(label, 128, 22);
if (node.status) {
  lctx.font = '10px JetBrains Mono, monospace';
  lctx.fillStyle = color;
  lctx.fillText(node.status.toUpperCase(), 128, 44);
}
var lTex = new T.CanvasTexture(lc);
var lMat = new T.SpriteMaterial({ map: lTex, transparent: true, depthTest: false });
var lSprite = new T.Sprite(lMat);
lSprite.scale.set(24, 6, 1);
lSprite.position.set(0, -baseSize * 2.5, 0);
g.add(lSprite);
```

Key: `depthTest: false` ensures labels render through other objects.

## 3d-force-graph API: Getters are Functions

```javascript
// WRONG — scene is a function, not a property
taskGraphInstance.scene.fog  // undefined
taskGraphInstance.graphData.nodes  // undefined

// CORRECT — call the function to get the value
taskGraphInstance.scene().fog  // THREE.FogExp2
taskGraphInstance.scene().children  // array
taskGraphInstance.graphData().nodes  // array
taskGraphInstance.graphData().links  // array
```

## STATUS_COLORS Extension

Add `pipeline` and `engine` status types to the colors map:

```javascript
var STATUS_COLORS = {
  backlog: '#5a6a8a',
  queued: '#5a6a8a',  // Added — work orders use "queued" not "backlog"
  triaged: '#818cf8',
  in_progress: '#e8d5a0',
  review: '#c4956a',
  testing: '#fbbf24',
  blocked: '#ef4444',
  escalated: '#f97316',
  done: '#22c55e',
  pipeline: '#6366f1',  // Added for pipeline stage nodes
  engine: '#3a6b6b'     // Added for engine topology nodes
};
```

## Link Type Extensions

Add `pipeline` and `topology` to the link color/width functions:

```javascript
.linkColor(function(link) {
  if (link.type === 'block') return 'rgba(239,68,68,0.7)';
  if (link.type === 'parent') return 'rgba(232,213,160,0.7)';
  if (link.type === 'pipeline') return 'rgba(99,102,241,0.6)';
  if (link.type === 'topology') return 'rgba(58,107,107,0.5)';
  return 'rgba(99,102,241,0.5)';
})
.linkWidth(function(link) {
  if (link.type === 'block') return 4;
  if (link.type === 'parent') return 3;
  if (link.type === 'pipeline') return 3.5;
  if (link.type === 'topology') return 2;
  return 2.5;
})
```

## Verification

After fix, the graph should show 16+ nodes with 18+ links:

```javascript
// In browser console after clicking "3D Graph View":
JSON.stringify({
  nodes: window.taskGraphInstance.graphData().nodes.length,  // 16+
  links: window.taskGraphInstance.graphData().links.length,  // 18+
  fog: window.taskGraphInstance.scene().fog.constructor.name, // FogExp2
  spores: window.taskGraphInstance.scene().children.filter(function(c) { return c.type === 'Points' }).length  // 1
})
```
