# Canvas Rendering Pitfalls in Web Prototypes

Detailed reference for debugging HTML5 `<canvas>` rendering issues that are
invisible in code review but obvious in a screenshot. These bugs produce
symptoms users describe as "neon ball of colors," "text is invisible," or
"chart looks wrong / tiny / blurry."

---

## 1. CSS Variables Don't Work in Canvas Context

**Symptom**: Text or shapes drawn on canvas are invisible, black-on-dark, or
render in unexpected colors.

**Root cause**: `ctx.fillStyle = 'var(--text)'` passes the literal string
`"var(--text)"` to the canvas engine, which cannot resolve CSS custom
properties. It silently falls back to the previous fillStyle or renders black.

**Detection**:
```bash
grep -n "var(--" index.html | grep -i "fillStyle\|strokeStyle\|font"
```

**Fix**: Replace every CSS variable in canvas context calls with the actual
hex/rgb value:
```javascript
// BROKEN — renders invisible
ctx.fillStyle = 'var(--text)';
ctx.fillStyle = 'var(--text-dim)';

// FIXED — use the actual hex value
ctx.fillStyle = '#e2e8f0';     // --text
ctx.fillStyle = '#94a3b8';     // --text-dim
ctx.fillStyle = '#64748b';     // --text-mute
```

If your `:root` defines custom colors, keep a JS-side mirror object:
```javascript
const C = { text:'#e2e8f0', dim:'#94a3b8', mute:'#64748b' };
ctx.fillStyle = C.text;
```

---

## 2. Math.random() Inside Draw Functions

**Symptom**: Chart lines, node positions, or coupling values change every time
the canvas redraws (on resize, tab switch, data update). The visualization
looks unstable / flickering.

**Root cause**: Using `Math.random()` to generate visual properties (line
width, opacity, positions) inside a `draw()` function that runs on every
render cycle.

**Detection**:
```bash
grep -n "Math.random" index.html
```
If any hit is inside a `draw()`, `render()`, or canvas-related function, it's
likely the cause.

**Fix**: Replace random values with deterministic data:
```javascript
// BROKEN — different widths every redraw
const couplingStrength = 0.5 + Math.random() * 0.5;

// FIXED — use real data or fixed constants
const couplingStrength = dim.coupling; // from a data array
// or
const couplingStrength = 0.7; // fixed value
```

---

## 3. Canvas Default Sizing (300x150)

**Symptom**: Canvas content renders tiny, blurred, or in the wrong position.
The visualization appears crushed into a small area regardless of CSS sizing.

**Root cause**: `<canvas>` has default internal dimensions of 300x150. CSS
`width:100%` only changes the display size, not the drawing buffer. Content
drawn at coordinates based on `canvas.width` uses the 300x150 buffer.

**Detection**:
```javascript
// In browser console:
const c = document.getElementById('myCanvas');
console.log(c.width, c.height);  // 300 150 = BUG if CSS says otherwise
```

**Fix**: Set internal dimensions explicitly before drawing:
```javascript
function initCanvas(canvas) {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  // Now canvas.width/height match the display size
}
```

Also handle resize — but recompute positions, not just redraw:
```javascript
window.addEventListener('resize', () => {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  computePositions();  // recalculate node positions for new dimensions
  draw();
});
```

For high-DPI rendering (retina), multiply by devicePixelRatio:
```javascript
const dpr = window.devicePixelRatio || 1;
canvas.width = canvas.offsetWidth * dpr;
canvas.height = canvas.offsetHeight * dpr;
ctx.scale(dpr, dpr);
```

---

## 4. Excessive shadowBlur Creates Neon Glow

**Symptom**: Canvas nodes/circles have an intense glowing aura that makes
text unreadable and the visualization look like a "neon ball." Colors bleed
into each other.

**Root cause**: `ctx.shadowBlur` set to high values (15-20px+) on every node,
especially combined with bright fill colors.

**Fix**: Keep shadowBlur low for subtle aesthetics:
```javascript
// TOO MUCH — creates unreadable neon
ctx.shadowBlur = 20;
ctx.shadowColor = '#10b981';

// SUBTLE — clean, readable
ctx.shadowBlur = 6;
ctx.shadowColor = '#10b981';
```

Always reset `ctx.shadowBlur = 0;` after drawing the shadowed element, before
drawing text or other elements that shouldn't have shadows.

---

## 5. Duplicate Function Definitions (Silent Override)

**Symptom**: You fix a function, reload, and the fix doesn't take effect. The
old behavior persists.

**Root cause**: The same function name is defined twice in the file. JavaScript
uses the last definition. Your fix in the first definition is silently
overwritten.

**Detection**:
```bash
grep -n 'function setupMetricToggle' index.html
# If you see 2+ line numbers, you have duplicates
```

**Fix**: Delete the stale definition. Keep only the corrected one.

---

## Debugging Workflow for Canvas Issues

1. **Screenshot first** — visual bugs are obvious in a screenshot but invisible
   in code. Take one before and after each fix.
2. **Check canvas dimensions** — `console.log(canvas.width, canvas.height)` in
   the browser console. If it shows 300x150, you have the sizing bug.
3. **Grep for CSS vars in canvas calls** — `grep "var(--" file | grep -i fill`
4. **Grep for Math.random in draw functions** — `grep "Math.random" file`
5. **Grep for duplicate function definitions** — `grep -c 'function <name>'`
6. **Check shadowBlur values** — `grep "shadowBlur" file`
7. **After each fix, hard-refresh** (Cmd+Shift+R) and re-screenshot to verify.
