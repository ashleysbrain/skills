# 3D Living Constellation Technique

Proven build pattern from the Task Engine (2026-06-27). When a DS product
involves live, changing data (tasks, fleet health, dimensions), use this
pattern instead of flat tables. The phenotype's craft language (Warm Midnight
palette, breathing glow, Mucha lines) maps directly onto 3D elements.

## When to Use

- Task management / task engine products
- Fleet health monitoring dashboards
- Any data viz where state changes over time and the user should FEEL the change
- Multi-world clustering (multiple users/companies as separate clusters)

## Architecture (Three.js r128, single-file HTML)

Load Three.js from CDN:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

### Core Elements

1. **Coherence Core** — golden icosahedron at center, emissive, with outer
   glow shell (transparent BackSide sphere). Breathing animation at 4000ms
   matching phenotype's `@keyframes breathe`. Brightens as tasks complete.

2. **Dimension Nodes** — 8 nodes in a ring (radius ~4.5), each an
   IcosahedronGeometry. Color by health:
   - Leverage dim: moonlight gold (#e8d5a0) + rotating torus ring
   - Weak dim: dawn warm (#c4956a) + pulse animation
   - Healthy: whisper teal (#3a6b6b)
   - Y-offset scatter for 3D depth (sin-based)
   - Text sprite labels above each node

3. **Task Nodes** — OctahedronGeometry floating near their dimension.
   - DO tasks: teal, DEFER tasks: amber
   - Size scales with urgency
   - Independent float phase (sin/cos bobbing)
   - Coupling line to parent dimension

4. **Coupling Lines (κ matrix)** — QuadraticBezierCurve3 between dimension
   pairs, pulled toward center at midpoint. Violet (#7c6da8), opacity scaled
   by coupling strength.

5. **Starfield** — 300 points at distance 20-35 for ambient depth.

### Interaction

- Orbit: mousedown+drag rotates camera (spherical coords theta/phi)
- Zoom: wheel/pinch adjusts camera radius
- Auto-rotate: slow ambient until user grabs
- Click/tap: raycaster detects node hits, opens detail panel
- Hover: emissive intensity boost on hovered node

### State-Change Animation (the key feature)

When a task completes, its node **collapses into the core**:
```javascript
// On completion: mark done, start collapse timer
node.userData.done = true;
node.userData.collapseStart = clock.getElapsedTime();
node.userData.collapseFrom = node.position.clone();

// In animate loop: lerp position toward origin, shrink scale, brighten emissive
const progress = Math.min(1, (t - collapseStart) / 1.2);
node.position.lerpVectors(from, new THREE.Vector3(0,0,0), easeIn(progress));
node.scale.setScalar(Math.max(0.01, 1 - progress));
node.material.emissiveIntensity = 0.5 + progress * 2; // flash on merge
if (progress >= 1) node.visible = false;

// Core brightens with each completion
coreBrightness = Math.min(1.0, coreBrightness + 0.08);
```

### Phenotype Mapping

| 8D Sleep phenotype element | 3D constellation equivalent |
|---|---|
| `.breathing-glow` radial gradient | Core icosahedron + glow shell, same 4000ms breathe cycle |
| Mucha background lines | SVG behind canvas, same paths, lower opacity |
| Grain overlay | Same `body::after` noise filter |
| Moonlight amber accent | Core emissive color (0xe8d5a0) |
| Ultra-thin typography | UI overlay text at weight 200-300 |
| Sticky bottom nav | Same nav container with backdrop blur |
| Progressive disclosure | Tap node → detail panel slides up |

### Color Constants (Three.js hex)

```javascript
const MOONLIGHT = 0xe8d5a0;
const MOONLIGHT_DIM = 0x9a8866;
const WHISPER_TEAL = 0x3a6b6b;
const DAWN_WARM = 0xc4956a;
const STARLIGHT = 0xc4d4e8;
const DUSK = 0x5a6a8a;
const VIOLET = 0x7c6da8;  // coupling only, extremely sparingly
const NIGHT = 0x080d1a;
```

### Multi-World Extension

The architecture supports multiple clusters (one per user/company) orbiting a
shared core or existing as separate constellation groups at different 3D
positions. Each world gets its own set of dimension nodes and task nodes.

## Verification

After building, verify via console:
```javascript
// Check WebGL active, scene built, nodes present
JSON.stringify({
  webgl: !!canvas.getContext('webgl'),
  three_loaded: typeof THREE !== 'undefined',
  dimension_nodes: dimensionNodes.length,  // should be 8
  task_nodes: taskNodes.length,            // should match task count
})

// Test task completion animation
completeTask('T-104');
// Verify: task removed from open list, core brightened, score updated
```

## Pitfalls

- **Z-fighting on overlapping nodes**: scatter Y-offsets and float phases so
  nodes never sit at the same depth for long.
- **Performance on mobile**: cap pixel ratio at 2, use low-poly geometry
  (detail=1-2 on icosahedrons, 0 on octahedrons).
- **CDN reliability**: Three.js r128 from cloudflare has been stable. If the
  user environment blocks CDNs, vendor the file locally.
- **Orbit control confusion**: auto-rotate should stop on first user
  interaction (mousedown or touchstart) and not restart. Users expect manual
  control after grabbing.

## Reference Implementation

`/<workspace>`
Served live at `http://127.0.0.1:4174/` (python3 http.server on port 4174).
