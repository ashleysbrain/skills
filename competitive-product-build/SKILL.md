---
name: competitive-product-build
description: "Build new products by researching a target competitor exhaustively, mapping their UX/features, then enhancing with proprietary methodology. Full 8-phase lifecycle from target selection through launch. Also called the Copy-Then-Enhance pattern or Vibe Coding Business Process."
tags: [product, competitive, build, copy-enhance, vibe-coding, lifecycle, methodology]
version: 1.0
---

# Competitive Product Build (Copy-Then-Enhance)

Build new software products by systematically studying a target competitor, then releasing an enhanced version that adds proprietary methodology the competitor lacks.

## When to Use

- User wants to build a product inspired by or competing with an existing app
- User describes a "vibe coding" project — AI-accelerated product development
- The product will enhance an existing market category with a unique scoring/analysis layer
- Any "clone + improve" product development request

## The 8-Phase Process

### Phase 0: Target Selection & Competitive Research

**Goal:** Exhaustively understand the target product — features, UX, tech stack, pricing, complaints, market position.

Steps:
1. Launch a dedicated research subagent (delegate_task) to study the target product
2. Research dimensions: feature inventory, UX flows, design language, tech stack, pricing tiers, app store complaints, market data (downloads, revenue, acquisition history)
3. Identify the target's #1 and #2 weaknesses — these become the primary enhancement opportunities
4. Document findings in `research/<TARGET>-COMPETITIVE-REPORT.md`

**Key pitfall:** Don't skip the complaints/weakness analysis. The best enhancement opportunities come from 1-star reviews, not feature lists.

**Tool:** `competitive-product-teardown` skill for multi-product landscapes; single delegate_task for one target.

### Phase 1: Agent Brain Assembly

**Goal:** Build domain-specific agent brains that will inform the product's unique value proposition.

Steps:
1. Identify the knowledge domains the product needs (e.g., sleep science, physics/math for scoring)
2. For each domain, build a specialist agent brain — a structured knowledge base mapping the domain to the product's enhancement methodology
3. Each brain covers: domain fundamentals, mapping to product dimensions, scoring/analysis logic, evidence sources

**Example (from Divinity Health sleep app):**
- MD brain (20KB): sleep architecture stages, bidirectional sleep × 8D dimension mapping for all 8 dimensions, 3-tier evidence-based interventions, clinical red flag escalation protocol, population-specific sections (women's sleep, ADHD, bipolar, shift workers), data collection architecture, morning report clinical framework
- Physics/Math brain (30KB): 5 physics frameworks (attractor basins, antigravity fields, entropy, coupled oscillators, network theory), full mathematical definitions for each scoring component, CSI → 8D Impact → Personal Baseline Delta composition, production implementation notes

**Key pitfall:** Don't build agent brains until Phase 0 research is complete. The brains need to target the competitor's specific weaknesses.

**User preference — physics models in algorithms:** When the user names a physics concept for use in a scoring algorithm, research whether a genuine structural isomorphism exists in the published literature (same equations, different variables). If yes, build the full mathematical treatment with peer-reviewed citations. If no, say so honestly — do NOT force a metaphorical mapping or dress up a heuristic with physics language. The user values intellectual honesty over creative framing. Every equation must trace to a published source. Disruptors modify specific scoring sub-components via their actual physiological mechanisms, not via a single post-hoc multiplier on the composite score.

### Phase 2: PRD (Product Requirements Document)

**Goal:** Translate competitive research + agent brain outputs into a buildable spec.

Steps:
1. Write the PRD from the competitive report + agent brain outputs
2. Structure: product vision, target user, core features (copied from target), enhancement features (proprietary), tech stack, data model, API design
3. For each copied feature: describe the behavior/UX to replicate (never copy proprietary code/algorithms)
4. For each enhancement: describe the proprietary methodology integration

**Key pitfall:** Ask clarifying questions BEFORE writing the PRD — platform, tech stack, copy boundary (what NOT to copy), revenue model, timeline. Use `adhd-choice-discipline` — default to one strong proposal.

### Phase 3: Design System

**Goal:** Create the visual design language.

Steps:
1. Wait for user to provide screenshots of the target product (DESIGN IS ALWAYS ON HOLD until screenshots arrive)
2. Map the target's design system: colors, typography, spacing, navigation patterns, iconography
3. Adapt for the new brand: replace color palette, update typography, add proprietary dimension indicators
4. Document in a design system file

**Key pitfall:** Never start design work without screenshots. The user will provide them — don't guess.

### Phase 4: Architecture & Tech Stack

**Goal:** Define the technical architecture.

Steps:
1. Select tech stack based on PRD requirements (default recommendation: React Native + Expo for mobile, Next.js for web)
2. Design data model (users, health data, scores, history)
3. Define API layer (Supabase/Firebase for backend)
4. Create architecture diagram
5. Document in `architecture/` directory

**Vibe coding stack recommendation (proven):**
- React Native + Expo (managed workflow)
- Expo Router for navigation
- Zustand for state management
- Supabase or Firebase for backend
- NativeWind or Tamagui for styling

### Phase 5: Feature Build

**Goal:** Implement features one at a time using AI-assisted coding.

Steps:
1. Scaffold the project (Expo init, directory structure, dependencies)
2. Build one feature per AI conversation — this is the #1 quality multiplier for vibe coding
3. For each feature: spec the feature in detail, then implement
4. Test on device after each feature

**Key pitfall:** 76% of vibe coding projects hit the 80/20 wall — the first 80% goes fast, the last 20% (edge cases, polish, performance) takes 4x longer. Manage scope aggressively. Ship MVP first.

### Phase 6: QA & Testing

**Goal:** Validate the product works correctly.

Steps:
1. Test all copied features against target app behavior
2. Test all enhancement features against PRD spec
3. Test the proprietary scoring/analysis layer against known inputs
4. Fix bugs in priority order (crashers → incorrect behavior → polish)

### Phase 7: Launch

**Goal:** Ship to users.

Steps:
1. App store submission (App Store Connect + Google Play Console)
2. Landing page / marketing site
3. Pricing tier setup
4. Launch announcement

### Phase 8: Post-Launch Iteration

**Goal:** Improve based on real user feedback.

Steps:
1. Monitor app store reviews and complaints
2. Track usage analytics
3. Iterate on the proprietary scoring/analysis layer
4. Add features from the backlog

## Cross-Phase Rules

1. **Spec before code.** Always write the spec (what it does) before implementing. This is the #1 quality multiplier for AI-assisted development.
2. **One feature per AI conversation.** Don't try to build 3 features in one prompt. Context gets lost.
3. **Copy behavior, not code.** Replicate the UX and feature behavior. Never copy proprietary algorithms, code, or assets.
4. **Enhancement is separate.** Build the copied features first, then add proprietary enhancements as distinct features. Don't intertwine them.
5. **Hold design until screenshots.** The user provides visual reference — don't start design without it.
6. **Ask early, build once.** Clarify platform, tech stack, copy boundary, revenue model, and timeline before Phase 2. Re-work is expensive.

## Directory Structure

```
<product-name>/
├── research/
│   ├── <TARGET>-COMPETITIVE-REPORT.md
│   └── <OTHER>-RESEARCH.md
├── docs/
│   ├── PRD.md
│   ├── DESIGN-SYSTEM.md
│   └── ARCHITECTURE.md
├── architecture/
│   └── diagrams/
├── agents/
│   ├── <domain>-brain.md
│   └── <scoring>-algorithm.md
└── src/              (actual code, Phase 4+)
```

## Pitfalls

- **Skipping competitive research** — you'll build features the target already does better. Research first, always.
- **Copying too much** — copy UX behavior, not code. The legal line is behavior vs. implementation.
- **Building before clarifying** — ask the 5 questions (platform, tech stack, copy boundary, revenue, timeline) before any build work.
- **Designing without screenshots** — hold until the user provides visual reference.
- **Subagent timeouts on large research** — see `subagent-anti-timeout-patterns` Pattern 21 (output truncation). Pre-digest large research into summaries before synthesis.
- **Scope creep in Phase 5** — the 80/20 wall is real. Ship MVP, iterate.
- **Adding gamification/engagement layers before core ships** — user explicit: "It's too early. We need the most basic product to launch." Strip everything that isn't core value delivery from MVP. No gamification, no advanced scoring UI, no personality settings until core flow works end-to-end.
- **Wrong engine/agent names in docs** — the specialist engine = task engine (not Alfred, not anything else). Check memory and CURRENT-AGENTS.json before writing agent names into deliverables. Every wrong name erodes trust.
- **AI fluff instead of thorough research** — user says "I'm not talking about just AI giving me some bullshit fluff." When researching competitors, run through multiple subagents, cross-reference multiple sources, include revenue data, MAU, App Store ratings, user complaints. Surface-level AI summaries are rejected. Use delegate_task with 3 parallel research agents for competitive landscapes.
- **Red team patent/legal claims can be hallucinated** — When competitive research or advisory red teams cite specific patents, trademarks, or legal risks, VERIFY the claim independently (web search the patent number, check the assignee, read the actual claims). In a BetterSleep session (2026-06-11), the red team cited US10764983B2 as a sleep tracking patent covering the product — but that patent is about light dimming controllers. The hallucinated patent was presented as a CRITICAL blocker and nearly triggered unnecessary legal spending. Always verify before escalating legal/patent/IP claims to the user.
- **Writing product docs yourself instead of dispatching to elite agents** — user: "Make sure that you're not doing this, that this is dispatched, right? To agents that have the right skills at the elite product agents to write this." Delegate to PhD-level product specialists, don't write docs directly.
- **Asking the user to run terminal commands they can't execute** — When the user says a terminal command isn't working after 2+ attempts, STOP troubleshooting the command and PIVOT to a different approach. Example: user couldn't accept Xcode license via terminal (sudo + password issues). Repeating the instruction caused visible frustration and damaged trust. Correct response: "Skip Xcode, building as a mobile-first web app instead." The user expects you to unblock yourself, not ask them to debug their terminal. **Hard rule: if a setup step requires the user to type a command, it's a design failure.**
- **Stopping to ask permission when nothing is actually blocking** — user (2026-06-12): "Keep going. Only stop if what you need from me is ACTUALLY blocking you." The user wants relentless forward progress. If the next step can be done without user input (no Apple Developer account needed for simulator, no Firebase needed for mock backend, no screenshots needed for code), keep building. Stop ONLY when you hit a genuine blocker that requires human action.
- **Treating Apple Developer account as a build blocker** — You can write all Swift code, create the full project structure, test imports, and verify architecture without Xcode or an Apple Developer account. Build everything that CAN be built. The account is only needed for device testing and App Store submission.
- **Subagent timeouts on large file reads + writes** — When delegate_task subagents timeout (600s limit), switch to doing the work directly. Subagents work best for parallel research or isolated code tasks. For sequential file-heavy work (read 3 files → analyze → write 2 files), the overhead of agent boot + file reads often exceeds the timeout. Fall back to direct tool calls.
- **Building engine API without checking existing patterns first** — Before writing a new engine's API server, read the existing engine servers for the established pattern (FastAPI + Pydantic models + uvicorn). The pattern is: `src/api/server.py` (routes), `run_server.py` (entry point), `tests/test_*.py`. Mirror the structure exactly — don't invent a new layout.

## Seed Engine Integration

The the specialist engine Engine (`ds-seed-engine/`) provides phase-gated project management for competitive builds, backed by 4 real physics layers (Avrami nucleation, Landau phase transitions, Per Bak SOC, CPM/PERT critical path). Use it for any multi-week product build:

| Seed Phase | Maps to Copy-Then-Enhance Phase | Gate Criteria |
|------------|--------------------------------|---------------|
| Nucleation | Phase 0 (Target Selection) | Avrami X >= 0.7, Landau T < Tc |
| Specification | Phase 1-2 (Brains + PRD) | 3 germ layers defined (Ectoderm=UI, Mesoderm=Backend, Endoderm=Core) |
| Construction | Phase 3-4 (Design + Architecture) + Phase 5 (Feature Build) | Critical path features complete, SOC risk managed |
| Integration | Phase 6 (QA + Testing) | Landau eta >= 0.9, all inhibitors resolved |
| Launch | Phase 7 (Launch) | Avrami X >= 0.95, zero critical bugs |
| Evolution | Phase 8 (Post-Launch Iteration) | SOC governs change avalanches |

**Key rule:** No phase executes until the prior phase's gate passes. principal override logged. Immutable audit trail.

**Methodology inheritance:** Each product is a project WITHIN `ds-seed-engine/projects/`. When the engine updates, all active projects must re-validate. See `physics-informed-engine-development` skill for full inheritance protocol.

**Seed agents (dispatch execution to these, don't do it yourself):**
- DS WADDINGTON — orchestrates phase gates
- DS TURING — pattern detection (clones competitor patterns)
- DS GOULD — strategy/pace (when to sprint vs stabilize)
- DS MARGULIS — integration (merges 8D + cloned product + platform)
- DS MAYR — market fit (product-market speciation)
- DS MCCLINTOCK — quality (finds and fixes defects)

## Research Integration Layer (Phase 2.5 — Health/Science Products)

For health/wellness products that could participate in academic research, add a ResearchKit/FHIR integration layer between Phase 2 (PRD) and Phase 3 (Design):

### Architecture Components
1. **ResearchKit** — Consent flow, surveys (PSQI, ISI, ESS, MEQ), active tasks (PVT, SSS)
2. **CareKit** — Longitudinal care plans, symptom tracking, insights dashboard
3. **HealthKit** — Read sleep analysis, heart rate, HRV, respiratory rate; write sleep staging
4. **FHIR R4 export** — Use `StanfordBDHG/ResearchKitOnFHIR` (Stanford) or `microsoft/healthkit-on-fhir` (Microsoft) to bridge ResearchKit data to university REDCap/i2b2 systems
5. **CSV/JSON export** — Simpler studies that don't need FHIR
6. **ClinicalTrials.gov API** — Study catalog scraping for in-app study matching

### Advisory Board Expansion
Add a 3-coach Research Advisory Panel:
- **ResearchKit Integration Strategist** — Technical architecture, IRB pathway, FHIR pipeline
- **Sleep-Science Methodologist** — Study design, statistical validation, publication strategy (PSQI/ISI/ESS baseline, PVT active tasks, construct validity studies)
- **University Partnership Architect** — Deal structures, IP negotiation, honorary degree pathway

### IRB Pathway
- Phase 1: Internal quality improvement (no IRB)
- Phase 2: Expedited review Category 7 at partner university (6-8 weeks, minimal risk)
- Phase 3: Full IRB for RCT (12-16 weeks)

### Data Export Pipeline
```
App → HealthKit (local) → ResearchKit (study data) → Firebase (encrypted sync)
  → FHIR Server (via Microsoft/Stanford libraries) → University REDCap/i2b2
```

### Validation Study Protocol (Minimum Viable)
- n=30, 2-week passive collection
- Compare 8D Physical score vs. actigraphy
- Compare 8D Psychological vs. PSQI/ISI questionnaires
- Target journals: JMIR mHealth, NPJ Digital Medicine, SLEEP

### SwiftUI App Structure (Proven for BetterSleep)
```
ProjectName/
├── Package.swift              # SPM: Firebase, ResearchKit, HealthKitOnFHIR
├── ProjectName/
│   ├── ProjectNameApp.swift   # @main entry, environment objects
│   ├── ContentView.swift      # TabView navigation
│   ├── Models/
│   │   └── DataModels.swift   # Dimensions, sessions, sounds, studies
│   ├── Views/
│   │   ├── DashboardView.swift     # Main dashboard + TWC ring
│   │   ├── DimensionView.swift     # 8D scores + coupling + healing
│   │   ├── SoundMixView.swift      # Spatial audio mixer (if audio product)
│   │   ├── ResearchPortalView.swift # Study matching + data export
│   │   └── SettingsView.swift      # Privacy, export, consent history
│   └── Services/
│       ├── HealthKitManager.swift   # Apple Health read/write
│       ├── ScoringEngineService.swift # Backend API client + FHIR/CSV export
│       ├── SpatialAudioEngine.swift  # AVAudioEngine + HRTF (if audio product)
│       └── ResearchManager.swift    # ResearchKit consent + baseline surveys
├── ProjectNameTests/
└── ProjectNameUITests/
```

### Key Libraries
- `https://github.com/ResearchKit/ResearchKit.git` (from: "2.2.0")
- `https://github.com/firebase/firebase-ios-sdk.git` (from: "11.0.0")
- `https://github.com/microsoft/healthkit-on-fhir.git` (from: "1.0.0")
- `https://github.com/StanfordBDHG/ResearchKitOnFHIR` (Stanford bridge)
- `https://github.com/danielgindi/Charts.git` (from: "5.0.0")

**Pitfall:** No Xcode on the build machine is NOT a blocker. Write all Swift source files directly, validate with `swift --version` check, and the project is ready to open in Xcode on any Mac. Don't let missing Xcode stop progress.

### Web-First Pivot (When Native Tooling Blocks)

When the user hits a native tooling wall (Xcode license acceptance, missing SDK, Apple Developer account delays, code signing failures), **immediately propose and execute a mobile-first web app** instead of troubleshooting the native tooling. The user gets frustrated fast when asked to do terminal commands they can't execute — don't repeat the command, don't troubleshoot, pivot.

**Web-first architecture (proven June 2026, BetterSleep 8D):**
- **MUST bundle with esbuild** — raw ES modules served by simple HTTP servers silently fail (blank screen, zero console errors). This is the #1 web dev lesson from June 2026. Bundle: `npx -y esbuild src/main.js --bundle --outfile=public/bundle.js --format=iife --target=safari15`
- Web Audio API for procedural sound generation (no audio files needed)
- localStorage for state persistence
- Hash-based router (works on GitHub Pages / any static host)
- PWA manifest + service worker for offline + "add to home screen"
- Mobile-first dark CSS with CSS custom properties
- `python3 -m http.server` for instant local testing
- Zero dependencies = zero tooling friction

**File structure (22 files, ~2900 lines for a full sleep app):**
```
<product>-web/
├── index.html              # PWA meta tags, viewport, font load
├── manifest.json           # PWA manifest
├── public/sw.js            # Service worker (cache-first)
├── src/
│   ├── main.js             # Entry point, SW registration
│   ├── app.js              # State + router + service init, component registry
│   ├── state.js            # Reactive state with localStorage persistence
│   ├── router.js           # Hash-based routing
│   ├── services/
│   │   ├── audio-engine.js # Web Audio API (procedural sounds + spatial)
│   │   ├── sleep-tracker.js
│   │   ├── scoring-engine.js
│   │   └── researchkit.js  # Survey + consent (web ResearchKit equiv)
│   ├── components/
│   │   ├── DashboardView.js
│   │   ├── SoundMixView.js
│   │   ├── SleepView.js
│   │   ├── InsightsView.js
│   │   ├── ResearchView.js
│   │   ├── SettingsView.js
│   │   ├── OnboardingView.js
│   │   ├── BottomNav.js
│   │   └── Modal.js
│   └── styles/
│       └── main.css        # Mobile-first dark theme
```

**Key rule:** Bundle with esbuild first, then serve `public/` directory with `python3 -m http.server 3002`. User opens `http://localhost:3002/bundle.html` in browser. Do NOT attempt to serve raw ES modules — blank screen will result.

## Reference Files

- `references/bettersleep-sleep-app-session.md` — first product built with this process (Divinity Health sleep app, June 2026). Includes competitive findings, enhancement strategy, tech stack choice, and phase gate lessons.
- `references/bettersleep-researchkit-integration.md` — ResearchKit/FHIR integration architecture, advisory panel structure, IRB pathway, validation study protocol, university partnership model. Built June 2026.
- `references/mobile-first-web-app-architecture.md` — Vanilla JS mobile-first PWA architecture (no build step, no framework). Proven pattern when native tooling blocks. Includes component pattern, state management, Web Audio API procedural sounds, and CSS theme tokens.

## Related Skills

- `competitive-product-teardown` — multi-product landscape research with PDF delivery
- `subagent-anti-timeout-patterns` — prevent delegation failures during research phases
- `technical-research-planning` — structured technology evaluation
- `adhd-choice-discipline` — minimize decision load, default to one strong proposal
- `writing-plans` — bite-sized implementation plans from PRD
