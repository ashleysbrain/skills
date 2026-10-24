# 3D Graph Editing API Reference

Details for implementing edit mode in the 3d-force-graph process flow tool.

## Edit Mode State

```javascript
var editMode = false;
var connectMode = false;
var connectSource = null;  // node ID of source when drawing a connection
var nodeCounter = 1000;    // counter for user-created nodes (usr_1001, usr_1002, ...)
```

## Adding Nodes

When the user clicks empty background in edit mode, use `screen2GraphCoords` to convert the 2D click position to 3D graph coordinates:

```javascript
.onBackgroundClick(function(event){
  if (editMode && !connectMode) {
    var coords = graphInstance.screen2GraphCoords(event.offsetX, event.offsetY, 0);
    showAddNodeDialog(coords);
  }
})
```

The dialog prompts for name, type (engine/gate/router/source/sink), and description. The new node is pushed to `ONTOLOGY.nodes` and `updateGraph()` is called.

## Connecting Nodes

Two-click pattern: click source (green selection ring appears), then click target. A prompt asks for edge type and optional condition.

```javascript
.onNodeClick(function(node, event){
  if (editMode && connectMode) {
    if (!connectSource) {
      connectSource = node.id;
      updateGraph();  // re-render to show selection ring
    } else if (connectSource !== node.id) {
      addConnection(connectSource, node.id);
      connectSource = null;
      connectMode = false;
    }
  } else {
    openDetail(node);
  }
})
```

The selection ring is a `THREE.TorusGeometry` added in `createNodeObject()` when `connectSource === n.id`:

```javascript
if (editMode && connectSource === n.id) {
  var sel = new THREE.Mesh(
    new THREE.TorusGeometry(Math.max(0.5, 9), 0.5, 8, 32),
    new THREE.MeshBasicMaterial({color: '#22c55e', transparent: true, opacity: 0.8})
  );
  sel.rotation.x = Math.PI / 2;
  g.add(sel);
}
```

## Deleting

- **Delete node**: `onNodeRightClick` in edit mode. Removes from `ONTOLOGY.nodes` and all connected edges from `ONTOLOGY.edges`.
- **Delete link**: `onLinkClick` in edit mode. Removes the matching edge from `ONTOLOGY.edges`.

## Position Preservation (CRITICAL)

When `updateGraph()` is called after any edit, existing nodes must keep their positions. Without this, the entire graph re-layouts and nodes fly around:

```javascript
function updateGraph() {
  var data = buildGraphData();
  var oldData = graphInstance.graphData();
  if (oldData && oldData.nodes) {
    var posMap = {};
    oldData.nodes.forEach(function(n) {
      posMap[n.id] = {x: n.x, y: n.y, z: n.z, fx: n.fx, fy: n.fy, fz: n.fz};
    });
    data.nodes.forEach(function(n) {
      if (posMap[n.id]) {
        n.x = posMap[n.id].x;
        n.y = posMap[n.id].y;
        n.z = posMap[n.id].z;
        if (posMap[n.id].fx) {
          n.fx = posMap[n.id].fx;
          n.fy = posMap[n.id].fy;
          n.fz = posMap[n.id].fz;
        }
      }
    });
  }
  graphInstance.graphData(data);
  graphInstance.d3ReheatSimulation();
}
```

## Breathing Animation

Engine nodes have glow halos that pulse. The animation traverses the Three.js scene each frame:

```javascript
var breathPhase = 0;
function animateBreathing() {
  breathPhase += 0.02;
  if (graphInstance) {
    var scene = graphInstance.scene();
    if (scene) {
      scene.traverse(function(obj) {
        if (obj.userData && obj.userData.isGlow) {
          obj.material.opacity = 0.08 + Math.sin(breathPhase) * 0.04;
          obj.scale.setScalar(1 + Math.sin(breathPhase) * 0.05);
        }
      });
    }
  }
  requestAnimationFrame(animateBreathing);
}
```

Glow meshes must be marked: `glowMesh.userData.isGlow = true` when created in `createNodeObject()`.

## Curved Links

Use `linkCurvature()` accessor. Different edge types get different curvature values for visual distinction:

```javascript
function getLinkCurvature(link) {
  if (link.edgeData.type === 'feedback') return 0.5;
  if (link.edgeData.type === 'cross_flow') return 0.3;
  if (link.edgeData.type === 'conditional') return 0.2;
  return 0.15;
}

graphInstance.linkCurvature(function(l) { return l.curvature || 0.15; });
```

## d3Force Pitfall

`d3Force('charge')` returns the force function, not the graph instance. Cannot chain:

```javascript
// WRONG — breaks the chain, .nodeLabel is not a function on the force object
graphInstance = ForceGraph3D()(c)
  .d3Force('charge').strength(-120)
  .nodeLabel(...);  // TypeError!

// CORRECT — set force separately after the chain
graphInstance = ForceGraph3D()(c)
  .graphData(data)
  .backgroundColor('#080d1a')
  // ... rest of chain ...
  .onEngineStop(function() { ... });

var chargeForce = graphInstance.d3Force('charge');
if (chargeForce) chargeForce.strength(-120);
```
