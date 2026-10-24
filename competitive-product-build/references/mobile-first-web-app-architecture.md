# Mobile-First Web App Architecture (Vanilla JS, No Build Step)

**Proven:** June 2026, BetterSleep 8D sleep wellness app. 22 files, ~2,900 lines, fully functional in under 2 hours.

## When to Use

When native app tooling blocks (Xcode, Android Studio, SDK issues, code signing) or when the fastest path to a testable product is needed. User can open on phone immediately via LAN IP.

## Architecture Principles

1. **Zero dependencies** — no npm, no node_modules, no build step
2. **ES modules** — `type="module"` in HTML, bare `import` between files
3. **Web Audio API** for procedural sound (no audio files needed)
4. **localStorage** for state persistence (no backend needed for MVP)
5. **Hash-based router** — works on GitHub Pages / any static host
6. **PWA manifest + service worker** — offline, "add to home screen"
7. **CSS custom properties** — theme tokens, no preprocessor
8. **`python3 -m http.server 3000`** — instant local dev server

## Component Pattern (No Framework)

Each view is a class with `render(container)` and optional `destroy()`:

```javascript
export class SomeView {
  constructor(services) { this.services = services; }
  
  async render(container) {
    container.innerHTML = `<div class="view">...</div>`;
    this._bindEvents(container);
  }
  
  _bindEvents(container) {
    container.querySelector('#btn')?.addEventListener('click', () => { ... });
  }
  
  destroy() { /* cleanup intervals, listeners */ }
}
```

## State Management Pattern

Reactive state with localStorage persistence and subscriber notifications:

```javascript
export class State {
  get(key) { /* dot-notation access */ }
  set(key, value) { /* save + notify subscribers */ }
  subscribe(key, callback) { /* return unsubscribe fn */ }
}
```

## Audio Engine Pattern (Web Audio API)

Procedural sound generation — no audio files, no downloads:

- **White noise**: random samples → buffer source
- **Pink noise**: Voss-McCartney algorithm on random samples
- **Rain**: bandpass-filtered noise (3000 Hz center, lowpass 8000 Hz)
- **Ocean**: LFO-modulated noise (0.08 Hz oscillator controlling filter frequency)
- **Forest**: sine oscillator with vibrato at very low volume
- **Fan**: noise through tight lowpass filter (400 Hz)

Spatial audio: `StereoPanner` nodes with randomized pan values.

## CSS Theme Tokens

```css
:root {
  --bg-primary: #0a0a0f;
  --bg-secondary: #12121a;
  --surface-1: #16213e;
  --accent: #7c5cfc;
  --text-primary: #e8e8f0;
  --nav-height: 64px;
  --safe-bottom: env(safe-area-inset-bottom, 0px);
}
```

Mobile-first: max-width 480px container, flex column, bottom nav fixed, viewport-fit cover.

## Serving

```bash
cd <product>-web && python3 -m http.server 3000
# Open on phone: http://<MAC_LAN_IP>:3000
```

For production: deploy to GitHub Pages, Netlify, Vercel, or any static host. No build step needed.
