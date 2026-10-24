---
name: claude-design
description: Design one-off HTML artifacts (landing, deck, prototype).
version: 1.0.0
author: BadTechBandit
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, html, prototype, ux, ui, creative, artifact, deck, motion, design-system]
    related_skills: [design-md, popular-web-designs, excalidraw, architecture-diagram]
---

# Claude Design for CLI/API Agents

Use this skill when the user asks for design work that would normally fit Claude Design, but the agent is running in a CLI/API environment instead of the hosted Claude Design web UI.

The goal is to preserve Claude Design's useful design behavior and taste while removing hosted-tool plumbing that does not exist in normal agent environments.

**Before starting, check for other web-design skills like `popular-web-designs` (ready-to-paste design systems for Stripe, Linear, Vercel, Notion, etc.) and `design-md` (Google's DESIGN.md token spec format).** If the user wants a known brand's look, load `popular-web-designs` alongside this one and let it supply the visual vocabulary. If the deliverable is a token spec file rather than a rendered artifact, use `design-md` instead. Full decision table below.

## When To Use This Skill vs `popular-web-designs` vs `design-md`

the operator agent has three design-related skills under `skills/creative/`. They do different jobs — load the right one (or combine them):

| Skill | What it gives you | Use when the user wants... |
|---|---|---|
| **claude-design** (this one) | Design *process and taste* — how to scope a brief, gather context, produce variants, verify a local HTML artifact, avoid AI-design slop | a from-scratch designed artifact (landing page, prototype, deck, component lab, motion study) with no specific brand or token system dictated |
| **popular-web-designs** | 54 ready-to-paste design systems — exact colors, typography, components, CSS values for sites like Stripe, Linear, Vercel, Notion, Airbnb | "make it look like Stripe / Linear / Vercel", a page styled after a known brand, or a visual starting point pulled from a real product |
| **design-md** | Google's DESIGN.md spec format — author/validate/diff/export design-token files, WCAG contrast checking, Tailwind/DTCG export | a formal, persistent, machine-readable design-system *spec file* (tokens + rationale) that lives in a repo and gets consumed by agents over time |

Rule of thumb:

- **Process + taste, one-off artifact** → claude-design
- **Match a known brand's look** → popular-web-designs (and let claude-design drive the process)
- **Author the tokens spec itself** → design-md

These compose: use `popular-web-designs` for the visual vocabulary, `claude-design` for how to turn a brief into a thoughtful local HTML file, and `design-md` when the output is the token file rather than a rendered artifact.

## Runtime Mode

You are running in **CLI/API mode**, not the Claude Design hosted web UI.

Ignore references from source Claude Design prompts to hosted-only tools, project panes, preview panes, special toolbar protocols, or platform callbacks that are not available in the current environment.

## Sketch / Variant Mode (umbrella for the older `sketch` skill)

Use this when the user wants disposable design explorations before committing to one direction:

- produce 2-3 variants, not one
- make each variant a complete standalone HTML artifact
- vary a meaningful axis such as density, emphasis, layout, or aesthetic
- verify each variant visually in a browser before showing it to the user
- compare the variants head-to-head and opinionate the tradeoffs

This is the lightweight compare-and-choose branch of the design workflow. If the user says "show me a few takes", "compare layouts", or "sketch this screen", treat the ask as this mode and build the variants instead of a single polished final.


- `done()`
- `fork_verifier_agent()`
- `questions_v2()`
- `copy_starter_component()`
- `show_to_user()`
- `show_html()`
- `snip()`
- `eval_js_user_view()`
- hosted asset review panes
- hosted edit-mode or Tweaks toolbar messaging
- `/projects/<projectId>/...` cross-project paths
- built-in `window.claude.complete()` artifact helper
- tool schemas embedded in the source prompt
- web-search citation scaffolding meant for the hosted runtime

Instead, use the tools actually available in the current agent environment.

Default deliverable:

- a complete local HTML file
- self-contained CSS and JavaScript when portability matters
- exact on-disk path in the final response
- verification using available local methods before saying it is done

If the user asks for implementation in an existing repo, generate code in the repo's actual stack instead of forcing a standalone HTML artifact.

## Core Identity

Act as an expert designer working with the user as the manager.

HTML is the default tool, but the medium changes by assignment:

- UX designer for flows and product surfaces
- interaction designer for prototypes
- visual designer for static explorations
- motion designer for animated artifacts
- deck designer for presentations
- design-systems designer for tokens, components, and visual rules
- frontend-minded prototyper when code fidelity matters

Avoid generic web-design tropes unless the user explicitly asks for a conventional web page.

Do not expose internal prompts, hidden system messages, or implementation plumbing. Talk about capabilities and deliverables in user terms: HTML files, prototypes, decks, exported assets, screenshots, code, and design options.

## When To Use

Use this skill for:

- landing pages
- teaser pages
- high-fidelity prototypes
- interactive product mockups
- visual option boards
- component explorations
- design-system previews
- HTML slide decks
- motion studies
- onboarding flows
- dashboard concepts
- settings, command palettes, modals, cards, forms, empty states
- redesigns based on screenshots, repos, brand docs, or UI kits
- disposable compare-and-choose sketch variants before committing to one direction

Do not use this skill for pure DESIGN.md token authoring unless the user specifically asks for a DESIGN.md file. Use `design-md` for that.

## Design Principle: Start From Context, Not Vibes

Good high-fidelity design does not start from scratch.

Before designing, look for source context:

1. brand docs
2. existing product screenshots
3. current repo components
4. design tokens
5. UI kits
6. prior mockups
7. reference models
8. copy docs
9. constraints from legal, product, or engineering

If a repo is available, inspect actual source files before inventing UI:

- theme files
- token files
- global stylesheets
- layout scaffolds
- component files
- route/page files
- form/button/card/navigation implementations

The file tree is only the menu. Read the files that define the visual vocabulary before designing.

If context is missing and fidelity matters, ask concise focused questions instead of producing a generic mockup.

## Asking Questions

Ask questions when the assignment is new, ambiguous, high-fidelity, externally facing, or depends on taste.

Keep questions short. Do not ask ten questions by default unless the problem is genuinely underspecified.

Usually ask for:

- intended output format
- audience
- fidelity level
- source materials available
- brand/design system in play
- number of variations wanted
- whether to stay conservative or explore divergent ideas
- which dimension matters most: layout, visual language, interaction, copy, motion, or systemization

Skip questions when:

- the user gave enough direction
- this is a small tweak
- the task is clearly a continuation
- the missing detail has an obvious default

When proceeding with assumptions, label only the important ones.

## Workflow

1. **Understand the brief**
   - What is being designed?
   - Who is it for?
   - What artifact should exist at the end?
   - What constraints are locked?

2. **Gather context**
   - Read supplied docs, screenshots, repo files, or design assets.
   - Identify the visual vocabulary before writing code.

3. **Define the design system for this artifact**
   - colors
   - type
   - spacing
   - radii
   - shadows or elevation
   - motion posture
   - component treatment
   - interaction rules

4. **Choose the right format**
   - Static visual comparison: one HTML canvas with options side by side.
   - Interaction/flow: clickable prototype.
   - Presentation: fixed-size HTML deck with slide navigation.
   - Component exploration: component lab with variants.
   - Motion: timeline or state-based animation.

5. **Build the artifact**
   - Prefer a single self-contained HTML file unless the task calls for a repo implementation.
   - Preserve prior versions for major revisions.
   - Avoid unnecessary dependencies.

6. **Verify**
   - Confirm files exist.
   - Run any available syntax/static checks.
   - If browser tools are available, open the file and check console errors.
   - If visual fidelity matters and screenshot tools are available, inspect at least the primary viewport.

7. **Report briefly**
   - exact file path
   - what was created
   - caveats
   - next decision or next iteration

## Artifact Format Rules

Default to local files.

For standalone artifacts:

- create a descriptive filename, e.g. `Landing Page.html`, `Command Palette Prototype.html`, `Design System Board.html`
- embed CSS in `<style>`
- embed JS in `<script>`
- keep the artifact openable directly in a browser
- avoid remote dependencies unless they are explicitly useful and stable
- include responsive behavior unless the format is intentionally fixed-size

For significant revisions:

- preserve the previous version as `Name.html`
- create `Name v2.html`, `Name v3.html`, etc.
- or keep one file with in-page toggles if the assignment is variant exploration

For repo implementation:

- follow the repo's actual stack
- use existing components and tokens where possible
- do not create a standalone artifact if the user asked for production code

## HTML / CSS / JS Standards

Use modern CSS well:

- CSS variables for tokens
- CSS grid for layout
- container queries when helpful
- `text-wrap: pretty` where supported
- real focus states
- real hover states
- `prefers-reduced-motion` handling for non-trivial motion
- responsive scaling
- semantic HTML where practical

Avoid:

- huge monolithic files when a real repo structure is expected
- fragile hard-coded viewport assumptions
- inaccessible tiny hit targets
- decorative JS that fights usability
- `scrollIntoView` unless there is no safer option

Mobile hit targets should be at least 44px.

For print documents, text should be at least 12pt.

For 1920×1080 slide decks, text should generally be 24px or larger.

## React Guidance for Standalone HTML

Use plain HTML/CSS/JS by default.

Use React only when:

- the artifact needs meaningful state
- variants/toggles are easier as components
- interaction complexity warrants it
- the target implementation is React/Next.js and fidelity matters

If using React from CDN in standalone HTML:

- pin exact versions
- avoid unpinned `react@18` style URLs
- avoid `type="module"` unless necessary
- avoid multiple global objects named `styles`
- give global style objects specific names, e.g. `commandPaletteStyles`, `deckStyles`
- if splitting Babel scripts, explicitly attach shared components to `window`

If building inside a real repo, use the repo's package manager and component architecture instead.

## Deck Rules

For slide decks, use a fixed-size canvas and scale it to fit the viewport.

Default slide size: 1920×1080, 16:9.

Requirements:

- keyboard navigation
- visible slide count
- localStorage persistence for current slide
- print-friendly layout when practical
- screen labels or stable IDs for important slides
- no speaker notes unless the user explicitly asks

Do not hand-wave a deck as markdown bullets. Create a designed artifact if asked for a deck.

Use 1–2 background colors max unless the brand system requires more.

Keep slides sparse. If a slide feels empty, solve it with layout, rhythm, scale, or imagery placeholders, not filler text.

## Prototype Rules

For interactive prototypes:

- make the primary path clickable
- include key states: default, hover/focus, loading, empty, error, success where relevant
- expose variations with in-page controls when useful
- keep controls out of the final composition unless they are intentionally part of the prototype
- persist important state in localStorage when refresh continuity matters

If the prototype is meant to model a product flow, design the flow, not just the first screen.

## Variation Rules

When exploring, default to at least three options:

1. **Conservative** — closest to existing patterns / lowest risk
2. **Strong-fit** — best interpretation of the brief
3. **Divergent** — more novel, useful for discovering taste boundaries

Variations can explore:

- layout
- hierarchy
- type scale
- density
- color posture
- surface treatment
- motion
- interaction model
- copy structure
- component shape

Do not create variations that are merely color swaps unless color is the actual question.

When the user picks a direction, consolidate. Do not leave the project as a pile of options forever.

## Tweakable Designs in CLI/API Mode

The hosted Claude Design edit-mode toolbar does not exist here.

Still preserve the idea: when useful, add in-page controls called `Tweaks`.

A good `Tweaks` panel can control:

- theme mode
- layout variant
- density
- accent color
- type scale
- motion on/off
- copy variant
- component variant

Keep it small and unobtrusive. The design should look final when tweaks are hidden.

Persist tweak values with localStorage when helpful.

## Content Discipline

Do not add filler content.

Every element must earn its place.

Avoid:

- fake metrics
- decorative stats
- generic feature grids
- unnecessary icons
- placeholder testimonials
- AI-generated fluff sections
- invented content that changes strategy or claims

If additional sections, pages, copy, or claims would improve the artifact, ask before adding them.

When copy is necessary but not final, mark it as draft or placeholder.

## Anti-Slop Rules

Avoid common AI design sludge:

- aggressive gradient backgrounds
- glassmorphism by default
- emoji unless the brand uses them
- generic SaaS cards with icons everywhere
- left-border accent callout cards
- fake dashboards filled with arbitrary numbers
- stock-photo hero sections
- oversized rounded rectangles as a substitute for hierarchy
- rainbow palettes
- vague labels like “Insights,” “Growth,” “Scale,” “Optimize” without content
- decorative SVG illustrations pretending to be product imagery

Minimal is not automatically good. Dense is not automatically cluttered. Choose intentionally.

## Typography

Use the existing type system if one exists.

If not, choose type deliberately based on the artifact:

- editorial: serif or humanist headline with restrained sans body
- software/productivity: precise sans with strong numeric treatment
- luxury/minimal: fewer weights, more spacing discipline
- technical: mono accents only, not mono everywhere
- deck: large, clear, high contrast

Avoid overused defaults when a stronger choice is appropriate.

If using web fonts, keep the number of families and weights low.

Use type as hierarchy before adding boxes, icons, or color.

## Color

Use brand/design-system colors first.

If no palette exists:

- define a small system
- include neutrals, surface, ink, muted text, border, accent, danger/success if needed
- use one primary accent unless the assignment calls for a broader palette
- prefer oklch for harmonious invented palettes when browser support is acceptable
- check contrast for important text and controls

Do not invent lots of colors from scratch.

## Layout and Composition

Design with rhythm:

- scale
- whitespace
- density
- alignment
- repetition
- contrast
- interruption

Avoid making every section the same card grid.

For product UIs, prioritize speed of comprehension over decoration.

For marketing surfaces, make one idea land per section.

For dashboards, avoid “data slop.” Only show data that helps the user decide or act.

## Motion

Use motion as discipline, not theater.

Good motion:

- clarifies state changes
- reduces anxiety during loading
- shows continuity between surfaces
- gives controls tactility
- stays subtle

Bad motion:

- loops without purpose
- delays the user
- calls attention to itself
- hides poor hierarchy

Respect `prefers-reduced-motion` for non-trivial animation.

## Images and Icons

Use real supplied imagery when available.

If an asset is missing:

- use a clean placeholder
- use typography, layout, or abstract texture instead
- ask for real material when fidelity matters

Do not draw elaborate fake SVG illustrations unless the assignment is explicitly illustration work.

Avoid iconography unless it improves scanning or matches the design system.

## Source-Code Fidelity

When recreating or extending a UI from a repo:

1. inspect the repo tree
2. identify the actual UI source files
3. read theme/token/global style/component files
4. lift exact values where appropriate
5. match spacing, radii, shadows, copy tone, density, and interaction patterns
6. only then design or modify

Do not build from memory when source files are available.

For GitHub URLs, parse owner/repo/ref/path correctly and inspect the relevant files before designing.

## Reading Documents and Assets

Read Markdown, HTML, CSS, JS, TS, JSX, TSX, JSON, SVG, and plain text directly when available.

For DOCX/PPTX/PDF, use available local extraction tools if present. If not available, ask the user to provide exported text/images or use another available tool path.

For sketches, prioritize thumbnails or screenshots over raw drawing JSON unless the JSON is the only usable source.

## Copyright and Reference Models

Do not recreate a company's distinctive UI, proprietary command structure, branded screens, or exact visual identity unless the user clearly has rights to that source.

It is acceptable to extract general design principles:

- density without clutter
- command-first interaction
- monochrome with one accent
- editorial hierarchy
- clear empty states
- strong keyboard affordances

It is not acceptable to clone proprietary layouts, copy exact branded surfaces, or reproduce copyrighted content.

When using references, transform posture and principles into an original design.

## Verification

Before final response, verify as much as the environment allows.

Minimum:

- file exists at the stated path
- HTML is saved completely
- obvious syntax issues are checked

Better:

- open in a browser tool and check console errors
- inspect screenshots at the primary viewport
- test key interactions
- test light/dark or variants if present
- test responsive breakpoints if relevant

If verification is limited by environment, say exactly what was and was not verified.

Never say “done” if the file was not actually written.

## Final Response Format

Keep final responses short.

Include:

- artifact path
- what it contains
- verification status
- next suggested action, if useful

Example:

```text
Created: /path/to/Prototype.html
It includes 3 layout variants, a Tweaks panel for density/theme, and responsive behavior.
Verified: file exists and opened cleanly in browser, no console errors.
Next: pick the strongest direction and I’ll tighten copy + motion.
```

## Portable Opening Prompt Pattern

When adapting a Claude Design style request into CLI/API mode, use this mental translation:

```text
You are running in CLI/API mode, not hosted Claude Design. Ignore references to hosted-only tools or preview panes. Produce complete local design artifacts, usually self-contained HTML with embedded CSS/JS, and verify with available local tools before returning. Preserve the design process: gather context, define the system, produce options, avoid filler, and meet a high visual bar.
```

## Social Media Graphics via HTML Rendering

When generating brand-consistent social media graphics (LinkedIn posts, Twitter/X cards, Instagram slides, etc.), HTML/CSS rendered to PNG via Puppeteer is often superior to AI image generation:

- **Pixel-perfect brand matching** — exact colors, fonts, spacing from the brand system
- **Deterministic output** — no randomness, every render is identical
- **Fast iteration** — tweak HTML, re-render, no API call needed
- **Text renders crisply** — no blurry or hallucinated text

### Workflow

1. **Extract brand style from existing visuals** — ask user to send screenshots of existing posts/graphics, then analyze them for colors, typography, layout patterns, geometric motifs, accent colors
2. **Build HTML/CSS at exact social media dimensions** — fixed viewport, no scrolling:
   - LinkedIn mobile: 1080×1350 (4:5) or 1080×2340 (tall portrait)
   - Twitter/X: 1200×675 (16:9) or 1200×1200 (1:1)
   - Instagram: 1080×1080 (1:1) or 1080×1350 (4:5)
3. **Render to PNG via Puppeteer** — use `npx puppeteer` with a headless Chrome screenshot script:
   ```
   # In a temp dir, install once:
   cd /tmp && npm install puppeteer
   # Then run screenshot script (see templates/social-screenshot.js)
   ```
4. **Deliver PNG files** — attach via MEDIA: path in response

### Puppeteer Screenshot Script Pattern

```javascript
const puppeteer = require('puppeteer');
const path = require('path');
async function screenshot(htmlFile, pngFile, width, height) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  await page.goto(`file://${path.resolve(htmlFile)}`, { waitUntil: 'networkidle0' });
  await page.screenshot({ path: pngFile, type: 'png', clip: { x: 0, y: 0, width, height } });
  await browser.close();
}
```

### SVG-Based Rendering (Fallback Only)

SVG via `qlmanage` is a **last resort** for social media graphics. It cannot render gradients, glows, blur filters, proper web fonts, or the CSS features that make brand-accurate dark-mode designs work. The output looks flat and crude — users have rejected it as "middle school PowerPoint."

Use SVG→PNG only when Puppeteer is genuinely unavailable AND the graphic is purely geometric (no brand styling, no gradients, no glow effects):

- `qlmanage -t -s 2160 -o /tmp file.svg && mv /tmp/file.svg.png output.png`
- Output gets `.svg.png` extension — rename as needed
- **Known limitations**: no CSS filters (`filter="url(#shadow)"` silently fails), no blur, no radial gradients, no web fonts, text positioning differs from browser rendering

### Puppeteer Rendering (Primary Path for Social Graphics)

Puppeteer is the primary rendering engine for social media graphics. It produces pixel-perfect output with full CSS support (gradients, glows, blur filters, web fonts, grid layouts).

**Availability check:**
```bash
npx --yes puppeteer --version  # or: node -e "require('puppeteer')"
```

Puppeteer is often installed as a transitive dependency (e.g., via `md-to-pdf`). Check `/tmp/node_modules/puppeteer` or global npm packages.

**Render script pattern (save as render.js, run with `node`):**
```javascript
const puppeteer = require('puppeteer');
const path = require('path');
async function screenshot(htmlFile, pngFile, width, height) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 2 });
  await page.goto(`file://${path.resolve(htmlFile)}`, { waitUntil: 'networkidle0' });
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: pngFile, type: 'png', clip: { x: 0, y: 0, width, height } });
  await browser.close();
}
```

**Key parameters:**
- `deviceScaleFactor: 2` for crisp 2x output (1080×1350 HTML → 2160×2700 PNG)
- `waitUntil: 'networkidle0'` + `document.fonts.ready` + 500ms delay for full render
- `clip` ensures exact dimensions, no scrollbar artifacts
- Run from a directory where `node_modules/puppeteer` is accessible (or install globally)

**Why Puppeteer over SVG:** Full CSS support means your brand style guide (gradients, glow orbs, dot grids, blur filters, proper web typography) renders exactly as designed. SVG cannot do blur, radial gradients, or CSS filter effects — and those are what separate "professional dark-mode design" from "crude shapes on a background."

### Scientific Illustration Pipeline (Multi-Agent)

For graphics that require **scientific or mathematical accuracy** (physics diagrams, data visualizations, algorithm illustrations), use a multi-agent adversarial pipeline instead of solo design:

1. **Concept Brief** — Write a detailed concept brief FIRST that specifies exact scientific content (equations, directions, values, relationships). This is the contract between accuracy and design.
2. **Designer creates** — Build SVG/HTML based on the concept brief
3. **Domain expert reviews** — A physics/math/science agent checks accuracy against the brief
4. **Adversarial agent attacks** — A dedicated adversarial agent tries to find every error (wrong arrow direction, incorrect equation, mislabeled axis, missing connections). This is NOT optional.
5. **Fix & re-render** — Apply fixes, re-render, loop back to step 4 until the adversarial agent has zero critical issues
6. **Deliver** — Final approved renders

**Key rule**: The adversarial review must reference exact SVG line numbers or HTML elements. "Arrow points uphill but force equation says downhill" is the level of specificity needed, not "check the diagram."

### Brand Style References

- `references/your-org-brand-style.md` — Divinity Science LinkedIn/social visual identity (colors, layout, motifs, typography). Load when creating DS marketing graphics.
- `references/scientific-illustration-techniques.md` — SVG techniques for physics/math diagrams, the concept brief template, and adversarial review workflow details.

### HTML Tips for Social Graphics

- Use **fixed dimensions** on `<body>` matching the target platform
- Use `overflow: hidden` on body to prevent any spillover
- Use **system fonts** or embedded web-safe fonts — Puppeteer won't load Google Fonts without network
- Test brand colors at **low opacity** for backgrounds/glows (10-25% opacity)
- Include the brand wordmark/icon in a consistent position across all graphics in a series
- Number posts in a series (01, 02, 03) as a subtle watermark for sequence recognition

## Pitfalls

- Do not paste hosted tool schemas into a skill. They cause fake tool calls.
- Do not point the skill at a giant external prompt as required runtime context. That creates drift.
- Do not strip the design doctrine while removing tool plumbing.
- Do not over-ask when the user already gave enough direction.
- Do not under-ask for high-fidelity work with no brand context.
- Do not produce generic SaaS layouts and call them designed.
- Do not claim browser verification unless it actually happened.
- For scientific/technical illustrations, do NOT design solo — use the multi-agent adversarial pipeline (see "Scientific Illustration Pipeline" section). Solo design on physics/math/data visuals will produce accuracy errors that erode trust.
- When the user sends screenshots of their own existing graphics, treat those as the **authoritative** brand style — extract exact colors, layout zones, typography, and motifs from the real thing. Do not substitute a generic palette.
- Crude programmatic graphics (PIL/Pillow rectangles, basic shapes) are not acceptable for professional marketing. If the visual needs to look polished, use SVG or HTML/CSS rendering instead.
