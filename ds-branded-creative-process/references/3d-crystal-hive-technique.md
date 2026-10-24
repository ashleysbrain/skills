# 3D Crystal Hive Technique (APPROVED)

**Status:** Active — this is the approved 3D visual metaphor for data-heavy DS products.  
**Retires:** `3d-constellation-technique.md` (orbit approach — rejected, looked like planets).  
**Date:** 2026-06-27  
**Approved iteration:** v5 (after 4 rejections: flat tables → word-swap → orbit → stacked boxes → crystal v1 → crystal v2 APPROVED)

## When to Use

- Task management / task engine products (The Lattice, fleet task structures)
- Fleet health monitoring dashboards
- Any product where live, changing data should FEEL like a growing organism
- Multi-world clustering (user/company as crystal cluster)

## The Approved Concept

**One solid crystal that grows as work gets done.** Not orbits, not planets, not stacked boxes. A faceted gemstone with 8 color-coded arms radiating from a breathing golden seed core. Tasks are facets that crystallize into the structure when completed.

### Why This Was Approved

The user's progression of feedback:
1. "This looks like planets in orbit" — REJECTED the orbit/constellation approach
2. "This isn't visually appealing and doesn't look like a crystal" — REJECTED stacked boxes
3. "Why did you choose these stones for these dimensions?" — APPROVED the gemstone palette reasoning (see below)

The key insight: the user wanted ONE SOLID STRUCTURE, not discrete objects floating in space. The crystal metaphor (one object growing outward) matched better than the constellation metaphor (separate objects orbiting).

## Concept Exploration Pattern (MANDATORY before coding)

This is the process that produced the approved output. Run it EVERY time for 3D/interactive work:

1. **Study the real-world metaphor.** If building a crystal, study crystallography: faceted geometry (octahedrons, hexagonal prisms), refraction, lattice structures, color zoning in real minerals (fluorite, amethyst, quartz). Pull reference images or read mineralogy basics.

2. **Explore 3-5 visual concepts as text.** Describe geometry, materials, lighting, camera behavior for each. Example:
   - Concept A: Stacked cubes (REJECTED — looks like Minecraft)
   - Concept B: Orbiting spheres (REJECTED — looks like planets)
   - Concept C: Faceted crystal growth (APPROVED — looks like a gemstone)

3. **Compose the palette with semantic reasoning.** Each color must map to the dimension's psychological meaning AND work in 3D dark space (MeshStandardMaterial properties, not just hex codes).

4. **Write a visual brief.** Geometry specification, material properties, lighting direction, camera behavior, color assignments. The user must approve this before code.

5. **THEN code.**

## Gemstone Palette System (the specialist engine 3D Extension)

The approved palette maps 8D dimensions to real gemstones. Each color was chosen by the specialist engine based on:
- Psychological meaning of the dimension
- Physical light properties for 3D dark-space rendering
- Visual distinction when facets overlap (transmissive materials refract beautifully)

| Dimension | Gemstone | Hex | Three.js | Rationale |
|-----------|----------|-----|---------|-----------|
| Physical | Citrine | `#d4a547` | `0xd4a547` | Somatic heat, metabolism, kinetic energy. Anchors with warmth. |
| Psychological | Fluorite | `#4ab5a5` | `0x4ab5a5` | Emotional equilibrium, cooling, internal stability. Balances physical warmth. |
| Intellectual | Amethyst | `#9a6bc4` | `0x9a6bc4` | Highest visible frequency. Deep focus, abstract cognition. |
| Social | Sapphire | `#6a8ab8` | `0x6a8ab8` | Communication, trust, relational bonds. |
| Spiritual | Clear Quartz | `#e8dcc0` | `0xe8dcc0` | Synthesis of all wavelengths. Pure light, clarity, transcendence. |
| Vocational | Obsidian | `#b07a5a` | `0xb07a5a` | Earthy, dense, forged under pressure. Craft and daily output. |
| Financial | Tourmaline | `#7a9a5a` | `0x7a9a5a` | Organic resource accumulation, stability, compounding growth. |
| Environmental | Celestine | `#7ab8c8` | `0x7ab8c8` | Spacious, atmospheric. Ecosystem and habitat. |

### MeshStandardMaterial Properties

For 3D rendering, colors need volumetric properties:
```javascript
// Done/crystallized facet — solid, polished
new THREE.MeshStandardMaterial({
  color: dimThree, emissive: dimThree, emissiveIntensity: 0.2,
  metalness: 0.2, roughness: 0.12, transparent: true, opacity: 0.92,
});

// Open/floating facet — translucent, pulsing
new THREE.MeshStandardMaterial({
  color: dimThree, emissive: dimThree, emissiveIntensity: 0.06,
  metalness: 0.1, roughness: 0.3, transparent: true, opacity: 0.35,
});

// Ghost/forming facet — barely visible wireframe
new THREE.MeshStandardMaterial({
  color: dimThree, emissive: dimThree, emissiveIntensity: 0.01,
  metalness: 0, roughness: 0.5, transparent: true, opacity: 0.08,
});
```

## Architecture (Three.js r128, single-file HTML)

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

### Core Elements

1. **Seed Core** — OctahedronGeometry(0.35, 0), gold MeshStandardMaterial, 4-second breathing cycle matching phenotype `@keyframes breathe`. Brightens as tasks crystallize. CoreLight (PointLight) pulses with it. Glow sprite behind using CanvasTexture radial gradient.

2. **Crystal Arms (8)** — Hexagonal prism segments (CylinderGeometry, 6 sides) tapering outward along 3D-spread directions (DIRS array, balanced from camera). Each arm has NUM_SLOTS positions along it. Segments are oriented to point along arm direction via Quaternion.setFromUnitVectors.

3. **Task Facets** — OctahedronGeometry nodes offset perpendicular to arm. Done=solid+gold edge highlights. Open=translucent+pulsing+rotating. Ghost=wireframe+faint. Size scales with urgency.

4. **Crystal Bonds** — QuadraticBezierCurve3 between coupled arm endpoints, color blended from both dimensions' gemstones, opacity scaled by coupling strength.

5. **Ambient** — 400 background stars (Points), 80 floating gold dust motes (AdditiveBlending), Mucha SVG behind canvas, grain overlay.

6. **Lighting** — HemisphereLight (blue sky/dark ground split) + warm DirectionalLight key + cool DirectionalLight fill + golden PointLight at core.

### Three.js r128 API Notes

- Use `THREE.ACESFilmicToneMapping` for cinematic look
- Use `THREE.FogExp2(0x080d1a, 0.06)` for depth fade into night
- `renderer.toneMappingExposure = 1.2` for warm highlights
- **NO OrbitControls** in r128 global build — implement manual orbit:
  ```javascript
  let orbitAngleX=0.6, orbitAngleY=0.5, orbitDist=6.5;
  let isDragging=false, autoRotate=true;
  // spherical coordinate camera, pointer events, wheel zoom
  // autoRotate resumes after 3s idle
  ```
- **CDN importmaps DO NOT WORK** in embedded browsers. Use global `<script>` tag, NOT `<script type="module">` + importmap.

### Phenotype Mapping

| 8D Sleep phenotype element | Crystal hive equivalent |
|---|---|
| `.breathing-glow` radial gradient | Core octahedron + glow sprite, 4s breathe cycle |
| Mucha background lines | Same SVG paths behind canvas |
| Grain overlay | Same `body::after` noise filter |
| Moonlight amber accent | Core emissive (0xe8d5a0), Clear Quartz arm |
| Ultra-thin typography | UI overlay text at weight 200-300 |
| Sticky bottom nav | Same nav with backdrop blur |
| Progressive disclosure | Tap facet → frosted glass detail panel at screen edge |

### Crystallize Interaction

When user taps an open facet and hits "Crystallize":
1. Task status changes from 'open' to 'done'
2. Task mesh animates: flash bright (emissive spike), then settle to solid
3. Arm segment animates: opacity fades up, emissive brightens
4. Core brightens incrementally
5. TWC score updates
6. UI counters update (crystallized/floating/forming)

```javascript
// Flash animation pattern
pendingAnimations.push({
  elapsed: 0, duration: 1.0,
  onFrame(p) {
    const flash = p < 0.3 ? p/0.3 : 1;
    const settle = p > 0.3 ? (p-0.3)/0.7 : 0;
    mesh.material.emissiveIntensity = 0.1 + flash*0.8 - settle*0.6;
    mesh.scale.setScalar(1 + flash*0.4 - settle*0.2);
  },
  onComplete() { /* set final material */ }
});
```

## Typography (the specialist engine UX Gate for 3D)

The approved typography rules for 3D product UI:
- **Weight 200** for all titles and large numbers (ultra-thin, elegant)
- **Weight 300** for body text and labels
- **Letter-spacing 0.3-4px** (generous, varies by element size)
- **Color**: monochromatic text ONLY (moonlight/starlight/dusk). Colors come from the 3D crystal itself, not from text.
- **Font**: `-apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'Segoe UI', sans-serif`
- **Numbers**: tabular-nums for all score displays
- **Detail panel**: frosted glass (`backdrop-filter:blur(30px)`), 1px gold-tinted border, at screen edge not on top of the crystal

## Verification

After building, verify via console:
```javascript
// Check WebGL active, Three.js loaded, scene built
const gl = document.getElementById('crystal-canvas').getContext('webgl');
renderer.render(scene, camera);
const px = new Uint8Array(4);
gl.readPixels(gl.canvas.width/2, gl.canvas.height/2, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
// Center pixel should be non-zero (golden core)
JSON.stringify({webgl: !!gl, three: typeof THREE !== 'undefined', corePixel: [px[0],px[1],px[2]]});
```

## Dimension-Specific Crystalline Shapes (MANDATORY)

The user explicitly rejected simple shapes (cubes/squares) for dimension nodes: "I don't like the square as a shape it is too simple. It needs to be a bit more complex than this and look crystaly." Every 8D dimension must use a DISTINCT crystalline polyhedron — no BoxGeometry, no simple prisms.

### The 8 Polyhedra (all crystalline, all distinct)

Each dimension maps to a real crystal form built via `ConvexGeometry` from canonical vertex sets:

| Dimension | Polyhedron | Faces | Crystal Habit | Build Method |
|-----------|-----------|-------|---------------|-------------|
| Physical | Rhombic dodecahedron | 12 rhombic | Garnet | `ConvexGeometry(scaleTo(rhombicdodec(), R))` |
| Spiritual | Tetrahedron | 4 | Tetrahedrite | `TetrahedronGeometry(R)` |
| Intellectual | Dodecahedron | 12 pentagonal | Pyrite | `DodecahedronGeometry(R)` |
| Social | Icosahedron | 20 triangular | Rare minerals | `IcosahedronGeometry(R)` |
| Environmental | Octahedron | 8 triangular | Diamond/fluorite | `OctahedronGeometry(R)` |
| Vocational | Cuboctahedron | 14 (8 tri + 6 sq) | Archimedean | `ConvexGeometry(scaleTo(cuboct(), R))` |
| Financial | Truncated octahedron | 14 (8 hex + 6 sq) | Kelvin cell | `ConvexGeometry(scaleTo(truncOct(), R))` |
| Psychological | Rhombicuboctahedron | 26 | Archimedean | `ConvexGeometry(scaleTo(rhombicub(), R))` |

### Vertex Set Generators (Three.js r128)

```javascript
const S2 = Math.SQRT2;
function perms(a,b,c){
  const v=[]; const base=[[a,b,c],[a,c,b],[b,a,c],[b,c,a],[c,a,b],[c,b,a]];
  for(const [x,y,z] of base) for(const sx of [1,-1]) for(const sy of [1,-1]) for(const sz of [1,-1])
    v.push(new THREE.Vector3(x*sx,y*sy,z*sz));
  return v;
}
function unique(verts,eps=1e-4){
  const out=[]; const seen=new Set();
  for(const v of verts){const k=v.toArray().map(n=>n.toFixed(3)).join(',');
    if(!seen.has(k)){seen.add(k); out.push(v);}}
  return out;
}
// Cuboctahedron: permutations of (±1,±1,0)
function cuboct(){const v=[];for(const a of[1,-1])for(const b of[1,-1]){v.push(new THREE.Vector3(a,b,0));v.push(new THREE.Vector3(a,0,b));v.push(new THREE.Vector3(0,a,b));}return unique(v);}
// Truncated octahedron: permutations of (0,±1,±2)
function truncOct(){const v=[];for(const p of[[0,1,2]]){for(const perm of[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]){for(const s1 of[1,-1])for(const s2 of[1,-1])for(const s3 of[1,-1]){v.push(new THREE.Vector3(p[perm[0]]*s1,p[perm[1]]*s2,p[perm[2]]*s3));}}}return unique(v);}
// Rhombicuboctahedron: (±1,±1,±(1+√2)) and all permutations
function rhombicub(){const t=1+Math.SQRT2;return unique([...perms(1,1,t)]);}
// Rhombic dodecahedron (Catalan dual of cuboctahedron): (±1,±1,±1) ∪ (±2,0,0) perms
function rhombicdodec(){
  const v=[];
  for(const a of[1,-1])for(const b of[1,-1])for(const c of[1,-1])
    v.push(new THREE.Vector3(a,b,c));
  for(const a of[2,-2]){v.push(new THREE.Vector3(a,0,0));v.push(new THREE.Vector3(0,a,0));v.push(new THREE.Vector3(0,0,a));}
  return unique(v);
}
```

### Why No Cubes

The user's rejection was explicit: squares/cubes look like Minecraft, not crystals. Real crystals grow as faceted polyhedra (octahedrons, dodecahedrons, rhombic dodecahedrons). The Physical dimension was originally a `BoxGeometry` cube and was replaced with a rhombic dodecahedron (garnet crystal habit). **Never use `THREE.BoxGeometry` for any dimension node.**

## Pitfalls

- **NEVER use BoxGeometry/cubes for dimension nodes.** The user explicitly rejected squares as "too simple" and not crystaly. Use the polyhedron mapping above.
- **ImportMap doesn't work in embedded browsers.** Always use `<script>` global tag for Three.js r128.
- **Z-fighting on overlapping segments.** Offset task nodes perpendicular to arm direction.
- **Performance on mobile.** Cap pixel ratio at 2, use low-poly geometry (detail=0-1).
- **autoRotate must stop on grab and resume after idle.** 3-second timeout before resume.
- **Pixel reads after heavy WebGL calls can timeout.** Limit readPixels calls to 1-2 per check.
- **Phenotype ≠ layout.** The craft language (palette, motion, type, grain) is shared across products. The STRUCTURAL design (crystal arms, faceted growth, task-as-facet) is product-specific. Never word-swap content into the reference product's layout.
- **Brief ≠ phenotype.** The sibling-agent brief may specify its own aesthetic tokens. The LIVE REFERENCE PRODUCT the user points at is the phenotype authority. When they conflict, follow the reference product.

## Reference Implementation

`/<workspace>`  
Served live at `http://127.0.0.1:4174/` (python3 http.server on port 4174).
