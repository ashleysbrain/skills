# 8D Sleep Phenotype Tokens (Warm Midnight)

Extracted verbatim from `8d-sleep-pwa/src/index.css` + `App.tsx` on 2026-06-27.
This is the canonical phenotype the user references as "looks like the 8D Sleep app."
Any new DS product that should share this design language uses these tokens directly.

## CSS Variables (`:root`)

```css
/* Backgrounds — warm midnight, NOT cold navy */
--night-deep:    #080d1a;
--night-surface: #0f1525;
--night-elevated:#161e35;

/* Accents — ONE hero color (moonlight amber) */
--moonlight:     #e8d5a0;
--moonlight-dim: #9a8866;
--whisper-teal:  #3a6b6b;
--dawn-warm:     #c4956a;

/* Text — warm off-white, never pure white */
--starlight:     #c4d4e8;
--dusk:          #5a6a8a;

/* Borders — warm-tinted, near-invisible */
--border-night:  rgba(200,190,170,0.08);

/* Radii — mixed per golden ratio */
--radius-sm:   6px;
--radius-md:   16px;
--radius-lg:   26px;
--radius-pill: 999px;

/* Golden Ratio Spacing Scale (base = 8px) */
--space-xs:  5px;   /* 8/phi */
--space-sm:  8px;   /* base */
--space-md:  13px;  /* 8*phi */
--space-lg:  21px;  /* 13*phi */
--space-xl:  34px;  /* 21*phi */
--space-2xl: 55px;  /* 34*phi */

--phi: 1.618033988749895;
```

## Signature Visual Elements

### Breathing Glow (the primary signature)
```css
.breathing-glow {
  width: 120px; height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle at 50% 45%,
    rgba(232,213,160,0.18) 0%,
    rgba(232,213,160,0.08) 35%,
    rgba(232,213,160,0.02) 60%,
    transparent 75%);
  animation: breathe 4000ms ease-in-out infinite;
}
/* Center dot */
.breathing-glow::after {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: rgba(232,213,160,0.5);
  box-shadow: 0 0 16px 3px rgba(232,213,160,0.15);
}
@keyframes breathe {
  0%,100% { transform: scale(0.97); opacity: 0.85; }
  50%     { transform: scale(1.03); opacity: 1; }
}
```

### Mucha-Inspired Background Lines (barely visible organic curves)
```html
<svg class="mucha-bg" viewBox="0 0 440 800" preserveAspectRatio="none">
  <path d="M-30,200 Q80,160 180,240 T460,200" stroke="rgba(232,213,160,0.018)" stroke-width="1" fill="none"/>
  <path d="M-30,340 Q100,300 220,380 T460,340" stroke="rgba(58,107,107,0.015)" stroke-width="1" fill="none"/>
  <path d="M-30,520 Q120,480 240,560 T460,500" stroke="rgba(232,213,160,0.012)" stroke-width="1" fill="none"/>
  <path d="M-30,640 Q90,600 200,660 T460,600" stroke="rgba(196,149,106,0.01)" stroke-width="1" fill="none"/>
</svg>
```
CSS: `position:fixed; inset:0; z-index:0; opacity:0.5; pointer-events:none;`

### Grain Overlay (breaks the "too clean" AI look)
```css
body::after {
  content: '';
  position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: overlay;
}
```

## Layout DNA

| Property | Value |
|---|---|
| Container max-width | 440px (mobile-first, centered) |
| Body background | #050811 (deeper than --night-deep) |
| App padding | var(--space-xl) var(--space-lg) = 34px 21px |
| Typography | -apple-system / Helvetica Neue, weight 200-300 |
| Line height | 1.75 |
| Score display | 56px, weight 200, --moonlight color, tabular-nums |

## Navigation Pattern

Sticky bottom nav with backdrop blur, 4 faculty buttons:
```css
.nav-container {
  background: rgba(10,14,26,0.85);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-night);
  padding: var(--space-sm);
}
.nav-item.active { color: var(--moonlight); background: rgba(232,213,160,0.08); }
```

## Progressive Disclosure Pattern

First-sight view: ONE feeling, ONE number, ONE tap to depth.
- Breathing glow at top
- Single large score number (weight 200)
- One-sentence status subtitle
- "View details" ghost button that expands into dimension bars
- Action buttons at bottom

## Animations (slow, breathing, never urgent)

```css
@keyframes fadeUp { from { opacity:0; transform:translateY(10px) } to { opacity:1; transform:translateY(0) } }
@keyframes barGrow { from { transform:scaleX(0) } to { transform:scaleX(1) } }
```
Timing: 600-800ms, cubic-bezier(0.25,0.1,0.25,1), staggered delays.

## Branding Rule

"Powered by Divinity Science" appears ONLY as a small footer badge:
```css
.ds-badge-footer { text-align:center; font-size:10px; font-weight:300; color:var(--dusk); opacity:0.4; letter-spacing:1px; }
```
Never in the header. The product name stands alone.
