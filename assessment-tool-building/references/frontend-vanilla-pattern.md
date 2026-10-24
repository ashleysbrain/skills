# Assessment Tool Frontend Pattern (Vanilla HTML/CSS/JS)

When building a web interface for an assessment tool API, use vanilla HTML/CSS/JS
with no framework and no build step. This keeps the interface co-located with
the tool and servable by the FastAPI StaticFiles mount.

## Architecture

Three files in a `web/` subdirectory next to the tool:

```
*_tool.py
*_data.py
web/
  index.html    # Three divs: screen-start, screen-test, screen-results
  style.css     # Dark theme, CSS variables, no framework
  app.js        # State machine + fetch calls to API
```

Or a single-file build (`personality_test.html`) with everything inline.
The single-file approach is easier to share, review, and serve from any
static server. Use it for the canonical UI; keep the multi-file version
in the tool directory for the StaticFiles mount.

## Provenance & Tribute Pattern (learned 2026-08-07)

Every assessment tool MUST honor its scientific origins. This is a hard
requirement, not decoration.

### Naming

The tool is named after the researchers who created the instrument:

```html
<title>The Goldberg-Johnson Personality Inventory · IPIP-NEO</title>

<div class="brand-header">
  <div class="brand-name">GOLDBERG</div>
  <div class="brand-name-sub">— JOHNSON</div>
  <div class="brand-tagline">Personality Inventory · IPIP-NEO</div>
</div>
```

NEVER invent a catchy brand name. User explicitly rejected "Fathom" as
"ridiculous." The scientist surnames ARE the brand.

### Tribute section (on start screen)

A visible attribution block below the start form:

```html
<div class="tribute-section">
  <div class="tribute-title">In Tribute</div>
  <div class="tribute-grid">
    <div class="tribute-card">
      <div class="tribute-name">Lewis R. Goldberg</div>
      <div class="tribute-role">Creator of the IPIP</div>
      <div class="tribute-desc">Pioneered the lexical hypothesis...</div>
      <a class="tribute-link" href="https://ipip.ori.org/" target="_blank" rel="noopener">ipip.ori.org</a>
    </div>
    <div class="tribute-card">
      <div class="tribute-name">John A. Johnson</div>
      <div class="tribute-role">Developer of IPIP-NEO-120</div>
      <div class="tribute-desc">Developed the 120-item short form...</div>
      <a class="tribute-link" href="https://personal.psu.edu/..." target="_blank" rel="noopener">personal.psu.edu</a>
    </div>
  </div>
  <a class="institution-link" href="https://ipip.ori.org/" target="_blank" rel="noopener">
    Oregon Research Institute · Eugene, Oregon
  </a>
</div>
```

The institution link at the bottom is required. Links must open in new tabs
with `rel="noopener"`.

### Source citation in consent block

```html
<p><strong>What this is:</strong> A personality inventory built on the
IPIP-NEO, using public-domain items from the International Personality
Item Pool. Developed by John A. Johnson (Penn State) from the framework
created by Lewis R. Goldberg (Oregon Research Institute). Scores use
population norms from over 600,000 respondents.</p>
```

## Screen Pattern

Each screen is a `<div class="screen">`. Only one is `.active` at a time.

```javascript
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}
```

Three screens:
1. **Start**: Name input + version selector + begin button + tribute section. Creates a session via POST.
2. **Test**: One item at a time, 1-5 scale grid. Auto-saves responses via PUT.
3. **Results**: OCEAN domain bars, facet bars, measurement confidence, personalization insights, calculation transparency, narrative report, safety disclaimer.

## Auto-Save Pattern

Each response saves immediately on click — do NOT batch:

```javascript
opt.addEventListener('click', () => {
  state.responses[itemId] = val;
  api(`/api/.../session/${state.sessionId}`, 'PUT', {
    responses: { [itemId]: val }
  }).catch(e => console.error('Save failed:', e));
});
```

Single-file pattern can also auto-advance to the next item after a brief
delay (250ms) for better UX on long tests:

```javascript
function selectResponse(val) {
  responses[activeItems[currentIdx].id] = val;
  showItem(); // re-render to show selected state
  setTimeout(() => {
    if (currentIdx < activeItems.length - 1) { currentIdx++; showItem(); }
  }, 250);
}
```

## Keyboard Support

Press 1-5 to answer, arrow keys to navigate. This matters for 120-item tests.

## API Response Shape (learned 2026-08-07)

The `/items` endpoint returns an ENVELOPE, not a bare array:

```json
{ "count": 300, "items": [{ "id": "I001", ... }] }
```

ALWAYS extract the items array:

```javascript
const data = await res.json();
allItems = data.items || data; // fallback if API changes to bare array
```

The session creation response includes a `responses` dict with all item IDs
as keys (null initially). Use this to filter the active item set:

```javascript
const sessData = await sessRes.json();
const sessionKeys = Object.keys(sessData.responses || {});
const keySet = new Set(sessionKeys);
activeItems = allItems.filter(it => keySet.has(it.id));
```

This correctly handles both 120-item and 300-item versions.

## API Base URL Detection

```javascript
const API = (window.location.port === '8311' || window.location.port === '')
  ? ''  // same origin if served by the API server
  : 'http://localhost:port';  // cross-origin during dev
```

## Results Visualization

- Domain bars: width = (mean / 5) * 100, color per domain, with colored glow (box-shadow at 33% opacity)
- Facet bars: thin pill bars, moonlight-dim fill, tabular-nums score
- Measurement confidence (physics): cards with label + verdict value
- Personalization insights: humanized directives (see Psychological Safety Layer)
- Calculation transparency: forward/reverse scoring explanation + per-domain formula
- Narrative report: raw text report from API

## Design Constraints (DS organism — the operator agent phenotype, BINDING)

ALL DS interactive interfaces use the the operator agent phenotype. This is non-negotiable and
was corrected across multiple sessions. The canonical tokens live in
`docs/gg-phenotype.css`. Read that file before writing any CSS.

### Mechanical pre-code gate (run BEFORE writing any CSS)

1. Assert `--bg-primary` is `#080d1a` or `#0a0e1a` (DARK). If any element has a light background, STOP.
2. Assert `--accent` is `#6366f1` (INDIGO). If you wrote `#58a6ff` (GitHub blue), `#4ad6b4` (teal), or `#ffd700` (gold), STOP.
3. Assert card radius is `16px` (`--radius`). Not 8px, not 12px.
4. Assert grain overlay SVG is present in `body::after`. If missing, add it.
5. Assert fonts are imported. Inter + Space Grotesk (numbers) via Google Fonts `<link>` in `<head>`.
6. Assert NO native form controls are visible (`<select>`, `<input type=radio>`, `<input type=checkbox>`).

### the operator agent phenotype token reference (canonical)

```
--night-deep:   #080d1a     (page background)
--night-surface:#0f1525     (card background)
--night-elevated:#161e35    (elevated elements, inputs)
--moonlight:    #e8d5a0     (warm gold accent, CTAs, headers)
--moonlight-dim:#9a8866     (dimmed gold — NOTE: 6-digit hex, not 7)
--starlight:    #c4d4e8     (body text)
--dusk:         #5a6a8a     (secondary text, labels)
--indigo:       #6366f1     (primary accent)
--indigo-light: #818cf8     (light accent, selected states)
--border:       rgba(200,190,170,0.08)
--radius:       16px        (cards)
--radius-sm:    10px        (buttons, inputs)
--radius-pill:  100px       (progress bars, badges)
```

Fonts: Inter (body), Space Grotesk (numbers/stats), DM Mono (code only).
Never use mono on stats or numbers. Use `font-variant-numeric: tabular-nums` instead.

### CRITICAL: No native HTML form controls (learned 2026-08-07)

User correction: "the drop down in the very first screen is already an ugly
element that doesn't fit in." Native `<select>` dropdowns render with OS-level
styling that completely breaks the the operator agent phenotype. They look foreign and cheap.

NEVER use native `<select>`, `<input type="checkbox">`, or `<input type="radio">`
as visible UI elements. Replace with phenotype-native custom controls:

- **Dropdown / selector**: segmented toggle (grid of `.version-card` divs with
  selected state: indigo top-bar, glow, border highlight). See `personality_test.html`
  for the working pattern.
- **Radio scale (1-5)**: grid of `.scale-btn` divs, selected state with indigo
  border + background + glow. Hide the actual radio input if accessibility
  requires one.
- **Toggle / switch**: custom CSS pill with sliding indicator.

Native controls are acceptable ONLY for `<input type="text">` (which can be
fully styled) and `<button>` (fully styleable). Everything else needs custom UI.

### Other DS constraints

- NO emojis in UI (custom SVG line-art, 1.5px stroke)
- DS prefix on everything
- Moonlight accent line under headers (68px wide, 40% opacity)
- Breathing glow animation on key metrics/progress bars
- Subtle gradient on progress bars (teal -> indigo -> moonlight) with leading-edge glow dot

## Psychological Safety Layer (the specialist engine display-layer humanization)

The scoring backend uses organism-internal language ("directives", "stability
assessment", "this human", trait labels like "crumbles under pressure"). This
language is correct for machine-to-machine communication but VIOLATES healthy
psychological principles when shown directly to a human.

Build a client-side `humanizeDirective()` function that transforms API output
into person-centered, strength-based, non-pathologizing framing WITHOUT touching
the backend scoring. The backend stays correct; the display changes.

Key transformations:
- "this human" -> "you"
- "crumbles under pressure" -> "may feel heightened stress during crises"
- "high neuroticism" -> "a tendency toward emotional sensitivity"
- "low neuroticism" -> "strong emotional resilience"
- "high/low [trait]" -> describe the adaptive pattern, not the label
- "extreme traits" -> no trait is extreme; "balanced profile" when none trigger
- "CRITICAL: measurement unreliable" -> "INSUFFICIENT: too much inconsistency to interpret reliably"

### Required UI elements for psychological safety

1. **Informed consent block** on start screen: what this is (research-grade
   instrument, norms source), what it is NOT (not a clinical diagnostic, no
   pathology assessment), data handling (local session, no external transmission).
2. **Safety disclaimer** at bottom of results: "Personality scores describe
   patterns, not destiny. Traits shift with context and intentional growth.
   High or low scores are not better or worse. If any result feels inaccurate,
   trust your self-knowledge over a questionnaire."
3. **Section rename for human readers**:
   - "Organism Directives" -> "Personalization Insights"
   - "Physics-Informed Measurement Quality" -> "Measurement Confidence"
   - "Calculation Transparency" -> "How Scores Are Calculated"
   - "Personality Report" -> "Your Narrative Report"
   - "Ongoing Recommendations" -> "Personalization Insights"
4. **Strength-based framing**: when no traits trigger adaptations, say
   "Your profile is balanced across all domains" not "No extreme traits detected."

### Design philosophy

Traits are adaptive in context. High openness is not better than low openness.
The assessment captures a snapshot of behavioral tendencies, not a diagnosis
or a permanent label. Every piece of copy should reflect this epistemic humility.

## Functional Verification After Design Passes (learned 2026-08-07)

A beauty pass that produces a gorgeous but non-functional UI is a FAILED
deliverable. After any CSS/design work, ALWAYS verify the full flow works:

1. Reload the page in the browser
2. Click through: start screen -> test -> answer items -> finish -> results
3. Check the browser console for fetch errors
4. Verify API connectivity with a raw fetch: `fetch('http://localhost:PORT/api/...').then(r=>r.json()).then(d=>console.log(d))`
5. Verify the items array is correctly extracted from the API envelope
6. Verify the session is created and item count matches the selected version
7. Verify scoring produces domains + facets + physics analysis
8. Verify all results panels populate (no "Loading..." stuck states)

Never declare a design pass complete based on a screenshot alone. The
screenshot can look perfect while the JavaScript is silently broken.

## Serving

The FastAPI API serves the frontend via StaticFiles mount:

```python
STATIC_DIR = Path(__file__).parent / "gigi3" / "organism" / "tools" / "ipip_neo120" / "web"
if STATIC_DIR.exists():
    app.mount("/personality/ui", StaticFiles(directory=str(STATIC_DIR), html=True), name="personality-ui")
```

The `html=True` flag serves index.html at `/`.

For development, serve the single-file UI from any static server:

```bash
python3 -m http.server 8899  # serves personality_test.html at :port
```

The API auto-detects cross-origin and points to `localhost:port`.

## UI-API Response Format Mismatch (learned 2026-08-06)

The most common UI failure is the frontend expecting one data shape and the
API returning another. In the IPIP-NEO build, sibling-agent's UI JavaScript
expected flat dicts (`domains.O = 3.5`) but the API returns arrays of objects
(`domains[0].mean = 3.5`). Result: empty domain bars, empty facet charts.

ALWAYS verify the UI's JavaScript accesses the SAME field names the API
actually returns. After writing or receiving UI code, do a visual pass:
fetch a real scored result from the API and trace the path the JS takes
through the response object. If any field access returns `undefined`, the
rendering breaks silently.

Example fix pattern:
```javascript
// WRONG (assumes flat dict by domain code):
domains[d]  // where d = 'O' -> undefined

// RIGHT (array of objects):
d.domain_code  // iterate the array, access .mean, .interpretation
```

Also check: when a sibling operator (sibling-agent) adds placeholder divs
(`<div id="recPanel">Loading...</div>`) but no fetch/JS to populate them,
the panels say "Loading..." forever. Always verify that every `id=` in the
HTML has corresponding JavaScript that fetches data and sets `.innerHTML`.

## Verified Build

Built 2026-08-06 for IPIP-NEO personality test (backend + initial UI).
Beauty pass 1 2026-08-07: `personality_test.html` rewritten with full the operator agent phenotype
(grain, moonlight accent, 16px radius, breathing progress bar, segmented version
toggle replacing native `<select>`).
Beauty pass 2 2026-08-07: the specialist engine psychological safety layer added
(informed consent, humanized directives, safety disclaimer, strength-based framing).
Full build 2026-08-07: renamed to "The Goldberg-Johnson Personality Inventory,"
added tribute section with researcher attribution and institution links, fixed
API integration bugs (items envelope extraction, cross-origin port detection,
version filtering by session keys), verified full end-to-end flow in browser.
Scientific accuracy pass 2026-08-07: correlation/causation language corrected
throughout wellness map, physics concepts relabeled as measurement quality
indicators, percentile disclaimers added, all 30 facets given separate
actionHigh/actionLow fields, adversarial subagent review run (found and fixed
critical growth-edge bug where low-facet cards showed high-facet advice).

- `personality_test.html` (canonical single-file UI, ~55K chars, the operator agent phenotype + Kahneman layer + Goldberg-Johnson tribute + 8D wellness map + 30-facet guide + scientific accuracy pass)
- `gigi3/organism/tools/ipip_neo120/web/index.html` (3227 chars — still GitHub dark phenotype, needs sync)
- `gigi3/organism/tools/ipip_neo120/web/style.css` (5426 chars — WRONG phenotype, needs sync)
- `gigi3/organism/tools/ipip_neo120/web/app.js` (9831 chars)

NOTE: `gigi3/.../web/` files still use the old GitHub-dark phenotype (#0d1117, #58a6ff).
They need to be synced to the the operator agent phenotype. The canonical pattern lives in
`personality_test.html` at the workspace root.
