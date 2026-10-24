# Three.js Loading Patterns for 3d-force-graph in the the operator agent Ops Platform

## Problem

The `3d-force-graph` UMD bundle from unpkg includes Three.js internally but
does NOT expose `THREE` as a global variable. Any custom `nodeThreeObject`
or `linkThreeObject` callback that references `THREE.SphereGeometry`,
`THREE.MeshPhongMaterial`, `THREE.FogExp2`, etc. will fail with
`ReferenceError: THREE is not defined`.

## Attempted Solutions That DO NOT Work

1. **Loading `three.min.js` from cdnjs (r160)** — r160+ uses ES modules.
   The `<script>` tag loads but `THREE` is not assigned to `window`.

2. **Loading `three.min.js` from cdnjs (r150)** — r150 is the last UMD build,
   but in practice still did not expose `THREE` globally when loaded alongside
   `3d-force-graph` (the UMD bundle may detect and consume/overwrite it).

3. **Prototype chain extraction** — Creating a temp graph instance and
   traversing `Object.getPrototypeOf(scene)` to find `constructor.THREE`.
   The UMD closure does not leak the THREE namespace. Do not attempt.

4. **Loading Three.js BEFORE 3d-force-graph** — Causes `Multiple instances
   of Three.js being imported` warning and the library may still not use
   the externally loaded THREE.

## Working Solution: Importmap + ES Module + Retry

### In the HTML `<head>` or before the main script:

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

### In the JavaScript (retry pattern):

```javascript
var taskTHREE = null;

function ensureTaskTHREE() {
  if (taskTHREE) return taskTHREE;
  if (typeof THREE !== 'undefined') taskTHREE = THREE;
  return taskTHREE;
}

function initTaskGraph() {
  var T = ensureTaskTHREE();
  if (!T) {
    // THREE.js ES module still loading — retry in 200ms
    var container = document.getElementById('taskGraph3d');
    if (container) container.innerHTML = '<div style="padding:40px;text-align:center;color:var(--dusk);font-size:12px">Loading 3D engine...</div>';
    setTimeout(initTaskGraph, 200);
    return;
  }
  if (taskGraphInstance) { updateTaskGraph(); return; }
  // ... build graph using T.SphereGeometry, T.MeshPhongMaterial, etc.
}
```

### In each function that uses Three.js:

```javascript
function createNodeObject(node) {
  var T = ensureTaskTHREE();
  if (!T) return null;
  var color = new T.Color('#6366f1');
  var g = new T.Group();
  var sg = new T.SphereGeometry(Math.max(0.5, 4), 20, 20);
  // ...
  return g;
}
```

## Standalone HTML Pages (Different Pattern)

Standalone HTML files like `gg-process-graph-3d.html` CAN load Three.js
separately because they don't have the 3d-force-graph conflict:

```html
<script src="https://unpkg.com/3d-force-graph"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r150/three.min.js"></script>
```

Use r150 from cdnjs (last UMD build). r160+ requires the importmap approach.

## Key Takeaway

When using `3d-force-graph` with custom Three.js objects:
- **Standalone pages**: load Three.js r150 separately (simple)
- **Ops platform (complex page)**: use importmap + ES module + retry (robust)
- **Never** reference `THREE` directly in functions — always use `var T = ensureTaskTHREE()` first
