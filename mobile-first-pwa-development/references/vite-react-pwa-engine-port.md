# Vite + React PWA: Physics Engine Port Walkthrough

Reference based on the 8D Sleep build session (June 2026). The task: take a
Swift Kuramoto scoring engine and turn it into a running browser app.

## When This Pattern Applies

- You have an existing engine in Swift/Python/C++ and need it in the browser
- You need React components (radar charts, gauges, forms) — not just vanilla JS
- You want instant HMR and native ESM (no esbuild bundling step)
- No server-side rendering or API routes needed (pure client-side PWA)

## Project Scaffold (4 config files)

```
my-app/
├── package.json          # type: module, vite + react deps
├── vite.config.ts        # plugin-react, server.host: true
├── tsconfig.json         # target ES2020, jsx: react-jsx, strict
├── index.html            # PWA meta tags, manifest link, #root div
├── public/manifest.json  # display: standalone, theme_color
└── src/
    ├── main.tsx          # ReactDOM.createRoot + CSS import
    ├── App.tsx           # main app component
    ├── engine/           # ported physics (pure TS, zero deps)
    ├── components/       # React UI
    └── styles/           # CSS
```

### package.json (minimal)

```json
{
  "name": "my-pwa",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite --host",
    "build": "tsc && vite build",
    "preview": "vite preview --host"
  },
  "dependencies": { "react": "^18.3.1", "react-dom": "^18.3.1" },
  "devDependencies": {
    "@types/react": "^18.3.3", "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1", "typescript": "^5.5.3", "vite": "^5.3.4"
  }
}
```

## Engine Port: Swift → TypeScript

### xorshift RNG (32-bit, browser-safe)

Swift uses `UInt64` xorshift. BigInt in browser JS fails on bitwise ops and
loses precision on division. Use 32-bit instead:

```typescript
private rngState: number;  // initialized from seed
private nextRand(): number {
  let h = this.rngState;
  h ^= h << 13;
  h ^= h >>> 7;
  h ^= h << 17;
  this.rngState = h >>> 0;  // force unsigned 32-bit
  return this.rngState / 0xffffffff;
}
```

### Euler-Maruyama step (identical structure to Swift)

```typescript
step(dt: number = 0.01): void {
  const deriv = new Array(this.n).fill(0);
  for (let i = 0; i < this.n; i++) {
    let cSum = 0;
    for (let j = 0; j < this.n; j++) {
      if (i === j) continue;
      cSum += this.coupling[i][j] * Math.sin(this.phases[j] - this.phases[i]);
    }
    deriv[i] = this.frequencies[i] + (this.globalCoupling / this.n) * cSum;
  }
  for (let i = 0; i < this.n; i++) {
    this.phases[i] += deriv[i] * dt;
    if (this.noiseStd > 0)
      this.phases[i] += this.gaussNoise() * this.noiseStd * Math.sqrt(dt);
    this.phases[i] %= 2.0 * Math.PI;
    if (this.phases[i] < 0) this.phases[i] += 2.0 * Math.PI;
  }
}
```

### Order parameter (TWC computation)

```typescript
orderParameter(): { coherence: number; averagePhase: number } {
  let re = 0, im = 0;
  for (const theta of this.phases) { re += Math.cos(theta); im += Math.sin(theta); }
  const r = Math.sqrt(re * re + im * im) / this.n;
  return { coherence: r, averagePhase: Math.atan2(im, re) };
}
twcPercent(): number { return this.orderParameter().coherence * 100; }
```

### Frequency mapping from scores

```typescript
// score (0-100) → natural frequency ω (0.5 - 2.0 Hz)
setFrequenciesFromScores(scores: number[]): void {
  this.frequencies = scores.map(s => 0.5 + (Math.max(0, Math.min(100, s)) / 100) * 1.5);
}
```

### Sigmoid calibration (psychometric S-curve)

```typescript
private sigmoid(raw: number): number {
  return 100 / (1 + Math.exp(-0.08 * (raw - 50)));
}
```

## Common Port Bug: Missing Public Methods

When porting Swift to TypeScript, the scoring pipeline may call methods on the
model that you forgot to port. In the 8D Sleep session, `setCouplingMatrix`
was missing — the button hung on "Running..." with no visible error.

**Fix:** Audit the Swift class's public interface before finishing the port.
Create a checklist: every `func` in the Swift file → corresponding TypeScript
method. Test via the dynamic import pattern (see SKILL.md) before wiring to React.

## React Component Patterns (no chart library)

### SVG Radar Chart (8 dimensions)
- Calculate polygon points from scores using trigonometry
- Grid rings at 20/40/60/80/100 as nested polygons
- Gradient fill via `<defs><radialGradient>`
- Dimension labels positioned outside the outer ring

### Canvas Oscillator Visualization
- `requestAnimationFrame` loop updating phases each frame
- Draw oscillators as colored dots on a circle
- Faint coupling lines between strongly-coupled pairs
- Center readout showing live TWC (order parameter)
- Play/Pause toggle via state

### Circular Gauge (TWC)
- SVG circle with `strokeDasharray` for arc length
- `strokeDashoffset` animation via CSS transition
- Color thresholds: green (≥75), amber (≥50), orange (≥30), red (<30)

## Dev Server + Verification Workflow

```bash
# 1. Start dev server (background, long-lived)
npx vite --host    # background=true in the operator agent terminal

# 2. Health check
curl -s http://localhost:5173 | head -20

# 3. Navigate browser, snapshot to verify render
# 4. Click demo button, snapshot to verify interaction
# 5. If stuck: browser_console with dynamic import to isolate engine bugs
# 6. Fix, HMR auto-reloads, re-test
```

## Production Build

```bash
npx vite build    # outputs to dist/
# Deploy dist/ to Vercel, Netlify, or any static host
```

No server, no backend, no API keys. The entire app (including the physics
engine) runs in the browser. This is the privacy-first architecture: zero
network calls during analysis.
