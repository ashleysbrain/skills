# Canvas Charts Without Dependencies

Pure Canvas 2D API implementations of radar chart, semicircular gauge, and
sparkline. Zero external libraries. Each handles devicePixelRatio (DPR) scaling
for crisp rendering on retina displays.

Based on the 8D Sleep web app session (June 2026).

## Common Pattern: DPR Scaling

All three charts share this resize/setup pattern:

```javascript
class SomeChart {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.dpr = window.devicePixelRatio || 1;
        this.resize();
    }
    resize() {
        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = rect.width * this.dpr;
        this.canvas.height = rect.height * this.dpr;
        this.ctx.scale(this.dpr, this.dpr);
        this.w = rect.width;
        this.h = rect.height;
    }
}
```

Call `resize()` on window resize (debounced) then `draw()` again.

---

## Radar Chart (8 dimensions)

Draws an N-axis spider/radar chart with concentric grid rings, axis lines,
a filled score polygon with gradient, data points, and labels.

Key design points:
- N points positioned at `(i / N) * 2π - π/2` (start at top, go clockwise)
- Grid: 4 concentric polygons at 25/50/75/100% radius
- Optional previous-scores overlay (dashed) for before/after comparison
- Radial gradient fill from center (more opaque) to edge (more transparent)
- Labels positioned OUTSIDE the outer ring using `labelDist = radius + padding`

```javascript
draw(scores, previousScores) {
    const ctx = this.ctx;
    const cx = this.w / 2, cy = this.h / 2;
    const radius = Math.min(this.w, this.h) / 2 - 50;
    const n = this.dimensions.length;
    ctx.clearRect(0, 0, this.w * this.dpr, this.h * this.dpr);

    // Grid rings
    for (let ring = 1; ring <= 4; ring++) {
        const r = (radius * ring) / 4;
        ctx.beginPath();
        for (let i = 0; i < n; i++) {
            const a = (i / n) * 2 * Math.PI - Math.PI / 2;
            const x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r;
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = ring === 4 ? 'rgba(255,255,255,0.12)' : 'rgba(255,255,255,0.05)';
        ctx.stroke();
    }

    // Score polygon
    ctx.beginPath();
    const points = [];
    for (let i = 0; i < n; i++) {
        const a = (i / n) * 2 * Math.PI - Math.PI / 2;
        const val = (scores[this.dimensions[i].key] || 0) / 100;
        const x = cx + Math.cos(a) * radius * val;
        const y = cy + Math.sin(a) * radius * val;
        points.push({x, y, angle: a, val});
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();

    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
    grad.addColorStop(0, 'rgba(99,102,241,0.35)');
    grad.addColorStop(1, 'rgba(99,102,241,0.05)');
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.strokeStyle = '#6366f1';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Data points + labels (outside ring)
    for (let i = 0; i < n; i++) {
        const p = points[i], dim = this.dimensions[i];
        ctx.beginPath();
        ctx.arc(p.x, p.y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = dim.color;
        ctx.fill();
        // Label
        const ld = radius + 28;
        const lx = cx + Math.cos(p.angle) * ld;
        const ly = cy + Math.sin(p.angle) * ld;
        ctx.font = '11px system-ui, sans-serif';
        ctx.fillStyle = 'rgba(255,255,255,0.7)';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(dim.icon, lx, ly - 8);
        ctx.font = 'bold 10px system-ui, sans-serif';
        ctx.fillStyle = dim.color;
        ctx.fillText(Math.round(scores[dim.key] || 0), lx, ly + 6);
    }
}
```

---

## Semicircular Gauge (TWC score 0-100)

Draws a 180-degree arc gauge with a colored fill proportional to the score.
Includes glow effect, large score number, and quality label.

Key design points:
- Background arc: `arc(cx, cy, radius, π, 2π)` (left to right, top half)
- Score arc: `arc(cx, cy, radius, π, π + π * (score/100))` (partial fill)
- Color thresholds: green ≥75, indigo ≥50, amber ≥30, red <30
- `shadowBlur` creates the neon glow effect on the arc
- Score text centered at `(cx, cy - 10)` with quality label below

```javascript
draw(twc) {
    const ctx = this.ctx;
    const cx = this.w / 2, cy = this.h * 0.72;
    const radius = Math.min(this.w / 2 - 20, this.h - 40);
    ctx.clearRect(0, 0, this.w * this.dpr, this.h * this.dpr);

    // Background arc
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI, 2 * Math.PI);
    ctx.strokeStyle = 'rgba(255,255,255,0.08)';
    ctx.lineWidth = 14; ctx.lineCap = 'round';
    ctx.stroke();

    // Score arc
    const frac = Math.max(0, Math.min(1, twc / 100));
    let color = twc >= 75 ? '#10b981' : twc >= 50 ? '#6366f1' : twc >= 30 ? '#f59e0b' : '#ef4444';
    ctx.shadowColor = color; ctx.shadowBlur = 20;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI, Math.PI + Math.PI * frac);
    ctx.strokeStyle = color; ctx.lineWidth = 14;
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Score text
    ctx.font = 'bold 48px system-ui, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(Math.round(twc), cx, cy - 10);
    ctx.font = '11px system-ui, sans-serif';
    ctx.fillStyle = 'rgba(255,255,255,0.4)';
    ctx.fillText('TWC', cx, cy + 18);
}
```

---

## Sparkline (7-day mini trend)

Draws a small line chart with gradient fill underneath. Used in dimension
cards to show per-dimension 7-day trends.

Key design points:
- Normalized to 0-100 Y range with padding
- Gradient fill under the line (opaque at top, transparent at bottom)
- Last data point marked with a dot
- Graceful empty state ("—") when fewer than 2 data points

```javascript
draw(values) {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.w * this.dpr, this.h * this.dpr);
    if (!values || values.length < 2) { /* draw placeholder */ return; }

    const pad = 6, min = 0, max = 100;
    const stepX = (this.w - pad * 2) / (values.length - 1);

    // Fill area
    ctx.beginPath();
    ctx.moveTo(pad, this.h - pad);
    for (let i = 0; i < values.length; i++) {
        const x = pad + i * stepX;
        const y = this.h - pad - ((values[i] - min) / (max - min)) * (this.h - pad * 2);
        ctx.lineTo(x, y);
    }
    ctx.lineTo(pad + (values.length - 1) * stepX, this.h - pad);
    ctx.closePath();
    const grad = ctx.createLinearGradient(0, 0, 0, this.h);
    grad.addColorStop(0, this.color + '40');
    grad.addColorStop(1, this.color + '05');
    ctx.fillStyle = grad;
    ctx.fill();

    // Line
    ctx.beginPath();
    for (let i = 0; i < values.length; i++) {
        const x = pad + i * stepX;
        const y = this.h - pad - ((values[i] - min) / (max - min)) * (this.h - pad * 2);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.strokeStyle = this.color; ctx.lineWidth = 2;
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.stroke();
}
```

---

## Canvas vs SVG Decision

| Factor | Canvas | SVG |
|--------|--------|-----|
| Many elements (100+ data points) | Better (no DOM overhead) | Slower |
| Interactive hover/click on elements | Harder (manual hit detection) | Easier (DOM events) |
| Responsive resize | Must manually redraw | Automatic via viewBox |
| Animation | Must use requestAnimationFrame | CSS transitions work |
| Print/PDF export | Raster (pixelated) | Vector (crisp) |

For PWA dashboards with moderate element counts and no per-element interaction,
Canvas is simpler (no SVG namespace management) and performs well. For charts
needing interactive tooltips or CSS animations, SVG is more ergonomic.
