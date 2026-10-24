# Programmatic QA Methodology for Interactive HTML Prototypes

When verifying a large single-file HTML prototype (1000+ lines) with many
interactive elements, use these browser_console expressions to programmatically
verify each feature WITHOUT requiring visual inspection. This is essential when:

- The vision model is rate-limited or unavailable
- The prototype is too large for a single screenshot
- You need to verify 10+ interactive elements quickly
- You want repeatable, deterministic verification (not "it looks right")

## Phase 1: Function Existence Audit

Batch-check ALL onclick-referenced functions exist:

```javascript
JSON.stringify({
  toggleCard: typeof window.toggleCard,
  sendMessage: typeof window.sendMessage,
  playSound: typeof window.playSound,
  loadPreset: typeof window.loadPreset,
  startTimer: typeof window.startTimer
})
```

**Action**: Any `undefined` result = missing handler. The HTML references it
but the JS was never written. This is the #1 cause of "the page loads but
nothing works when I click X."

## Phase 2: Toggle/Card Behavior

Verify expand/collapse actually changes DOM state:

```javascript
(() => {
  const card = document.getElementById('card-0');
  if (!card) return 'no-card';
  const before = card.classList.contains('expanded');
  window.toggleCard(0);  // or whatever the function is
  const after = card.classList.contains('expanded');
  return `toggled: before=${before} after=${after} changed=${before !== after}`;
})()
```

## Phase 3: Canvas Rendering Verification

### Full-canvas scan (not just corner!)
```javascript
(() => {
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');
  const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  let nonEmpty = 0;
  for (let i = 3; i < imgData.data.length; i += 4) {
    if (imgData.data[i] > 0) nonEmpty++;
  }
  const pct = (nonEmpty / (canvas.width * canvas.height) * 100).toFixed(1);
  return `canvas=${canvas.width}x${canvas.height} drawn=${pct}% (${nonEmpty} px)`;
})()
```

**Critical pitfall**: Sampling only `getImageData(0, 0, 100, 100)` gives false
negatives. A canvas might be 1110x420 with all content in the center. Always
scan the full canvas or sample at known geometric positions.

### Pixel color verification at known positions
```javascript
(() => {
  const ctx = document.getElementById('myCanvas').getContext('2d');
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  // Sample center (should be the "sleep quality" node = gold)
  const center = ctx.getImageData(cx, cy, 1, 1).data;
  // Sample first dimension node position
  const radius = Math.min(cx, cy) - 50;
  const angle = -Math.PI / 2; // top
  const nodeX = Math.round(cx + radius * Math.cos(angle));
  const nodeY = Math.round(cy + radius * Math.sin(angle));
  const node = ctx.getImageData(nodeX, nodeY, 1, 1).data;
  return JSON.stringify({
    center: [center[0], center[1], center[2]],  // expect [251,191,36] = gold
    node: [node[0], node[1], node[2]]            // expect [16,185,129] = green
  });
})()
```

Compare against expected hex values:
- `[16, 185, 129]` = #10b981 (green)
- `[251, 191, 36]` = #fbbf24 (gold/yellow)
- `[249, 115, 22]` = #f97316 (orange)

## Phase 4: Click Handler Testing via dispatchEvent

```javascript
(() => {
  const canvas = document.getElementById('myCanvas');
  const rect = canvas.getBoundingClientRect();
  const scale = rect.width / canvas.width;
  // Calculate click position at a known node
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const radius = Math.min(cx, cy) - 50;
  const angle = -Math.PI / 2;
  const nodeX = Math.round(cx + radius * Math.cos(angle));
  const nodeY = Math.round(cy + radius * Math.sin(angle));

  canvas.dispatchEvent(new MouseEvent('click', {
    clientX: rect.left + nodeX * scale,
    clientY: rect.top + nodeY * scale,
    bubbles: true
  }));

  const modal = document.getElementById('modalOverlay');
  const title = document.querySelector('#modalBody .modal-title');
  return `modalOpen=${modal && modal.style.display !== 'none'} title=${title ? title.textContent : 'none'}`;
})()
```

## Phase 5: Audio Engine Verification

```javascript
(() => {
  // Test audio playback
  AudioEngine.init();
  window.toggleSound('rain', 'rain');  // or whatever the play function is

  // Check state after a beat
  const state = {
    ctxExists: !!AudioEngine.ctx,
    ctxState: AudioEngine.ctx ? AudioEngine.ctx.state : 'null',
    activeSounds: Object.keys(AudioEngine.active || {}),
    sampleRate: AudioEngine.ctx ? AudioEngine.ctx.sampleRate : 0
  };

  // Stop it
  window.toggleSound('rain', 'rain');

  return JSON.stringify(state);
  // Expect: ctxState='running', activeSounds=['rain']
})()
```

## Phase 6: Trend Chart / Data Visualization Toggle

```javascript
(() => {
  const btns = document.querySelectorAll('.metric-toggle, .chart-toggle');
  // Find a non-active button
  const target = Array.from(btns).find(b => !b.classList.contains('active'));
  if (!target) return 'no-toggleable-buttons';

  const wasActive = target.classList.contains('active');
  target.click();
  const isNowActive = target.classList.contains('active');

  // Check if siblings were deactivated (proper radio behavior)
  const siblings = Array.from(btns).filter(b => b !== target);
  const anySiblingActive = siblings.some(b => b.classList.contains('active'));

  return `toggle: ${target.textContent} wasActive=${wasActive} nowActive=${isNowActive} siblingStillActive=${anySiblingActive}`;
})()
```

## Phase 7: Chat/Coach Message Flow

```javascript
// For chat-like interfaces (sleep coach, assistant, etc.)
(() => {
  const input = document.getElementById('chatInput');
  const sendBtn = document.getElementById('chatSend');
  if (!input || !sendBtn) return 'no-chat-ui';

  // Type a message
  input.value = 'test message';
  input.dispatchEvent(new Event('input', { bubbles: true }));

  // Check if send is wired
  const sendWired = typeof window.sendChatMessage === 'function';

  // Check for typing indicator presence after send
  const beforeCount = document.querySelectorAll('.chat-msg').length;
  window.sendChatMessage();
  const afterCount = document.querySelectorAll('.chat-msg').length;

  return `sendWired=${sendWired} msgsBefore=${beforeCount} msgsAfter=${afterCount}`;
})()
```

## Summary Checklist

For a prototype with N interactive features, you should be able to produce
a table like:

| Feature | Method | Result |
|---------|--------|--------|
| Influence cards | classList before/after | PASS |
| Trend toggles | click + classList check | PASS |
| Gauge drill-down | dispatchEvent + modal check | PASS |
| Dimension network | getImageData full scan | PASS (4.3% drawn) |
| Audio engine | AudioContext.state | PASS (running) |
| Breathing timer | button text change | PASS (Start→Stop) |
| Sleep coach | function existence | FAIL → BUILT → PASS |

This methodology was developed during the 8D Sleep prototype QA session
(2026-06-17) when the vision model was rate-limited and all 15+ features
needed verification before reporting completion to the user.
