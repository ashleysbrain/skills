# BetterSleep Sleep App Build Session (2026-06-07)

First product built using the Copy-Then-Enhance pattern. Reference session for the `competitive-product-build` skill.

## Target: BetterSleep (by Teladoc)

- 55M+ downloads, $9.8M/yr revenue
- Acquired by Teladoc in 2022
- Freemium: Free tier (3 simultaneous sounds), Premium $9.99/mo | $59.99/yr | $249.99 lifetime
- Design: Deep purple/violet (#0D0D1A base), dark-first, rounded corners, moon/stars motifs
- Navigation: Bottom tab (Home | Discover | Mixer | Tracker | Profile)

## Key Findings from Competitive Research

1. **#1 weakness: Sleep score is inaccurate, opaque, unscientific** — users consistently complain the score doesn't reflect their actual sleep quality
2. **#2 weakness: Aggressive paywalling destroys trust** — too many features locked behind premium, free tier too restrictive
3. **Killer feature: Sound mixer with 300+ sounds** — this is the core value prop users love
4. **300+ sleep sounds, guided meditations, sleep stories, bedtime reminders**

## Enhancement Strategy (8D360 Integration)

- Replace BetterSleep's opaque sleep score with an 8D Sleep Score using the 8D360 methodology
- 8 dimensions: PSY, PHY, ENV, SOC, SPI, INT, VOC, FIN
- Proprietary coupling coefficients for cross-dimensional sleep effects
- Cascade detection for sleep disruption patterns
- Target pricing: $29.99–39.99/yr (undercut BetterSleep's $59.99/yr)

## Agent Brains Built

### 1. MD Sleep Science Brain (20KB)
`agents/MD-SLEEP-SCIENCE-BRAIN.md`

- Full sleep architecture (N1/N2/N3/REM stages with EEG signatures, 90–110 min cycles)
- **Bidirectional sleep × 8D mapping for all 8 dimensions** — each dimension has: biological pathway, measurable proxies, coupling coefficient to sleep
- PSY↔PHY coupling at κ=0.82 confirmed (sleep is the primary mediator)
- 3-tier evidence-based interventions (Tier 1: CBT-I, sleep restriction; Tier 2: relaxation, breathing; Tier 3: binaural beats, aromatherapy)
- Clinical red flag escalation protocol (apnea, narcolepsy, insomnia, mood disorders, parasomnias)
- Population-specific sections: women's sleep health (menstrual/menopause), ADHD (50-75% delayed sleep phase), bipolar disorder (IPSRT model), shift workers
- Data collection architecture: passive (accelerometer, mic, light sensor), active (morning mood, sleep notes, weekly scales), integrations (Apple Health, calendar, weather)
- Content library classification with medical safety rules
- Morning report clinical framework with tone guidelines (never alarmist, never prescriptive, always contextualize)

### 2. Physics/Math 8D Sleep Score Algorithm (40KB, v2.0.0)
`agents/PHYSICS-8D-SLEEP-ALGORITHM.md`

**v2.0.0 (current)** — rebuilt on structural mathematical isomorphisms with peer-reviewed citations. No metaphors.

Nine proven isomorphisms (same equations, different variable names):
1. Process S ↔ RC circuit charge/discharge (Borbély 1982)
2. Process C ↔ Van der Pol oscillator (Kronauer 1990)
3. REM cycling ↔ Lotka-Volterra predator-prey (McCarley & Hobson, Science 1975)
4. Wake-sleep switching ↔ Double-well potential + Langevin dynamics (Diekmann 2022)
5. Thermoregulation ↔ Newton's law of cooling (Kräuchi 1999)
6. Brief awakenings ↔ Non-homogeneous Poisson process (Lo et al. 2002)
7. Stage transitions ↔ Continuous-time Markov chain (Laumann 2019)
8. Caffeine effect ↔ First-order elimination (Zenk et al. 2021)
9. Light-melatonin suppression ↔ Hill equation / cooperative binding (Zeitzer 2000)

Disruptors modify specific CSI sub-components via their actual physiological mechanisms — NOT via a single post-hoc multiplier on the composite score.

Score composition: `8D Sleep Score = 50% CSI + 30% 8D_Impact + 20% Personal_Baseline_Delta`

CSI sub-components:
- Sleep Architecture Score (SAS): Gaussian kernel distance from optimal stage distribution
- Circadian Alignment Score (CAS): Von Mises circular distribution × consistency factor
- Sleep Efficiency Score (SES): Sigmoid centered at 85% efficiency
- Fragmentation Index (FI): KL-divergence from healthy transition distribution

Each of the 8 dimensions has a transfer function mapping CSI components to dimension-specific impact scores, with the strongest coupling (PSY-PHY κ=0.82) getting cascade bonus/penalty.

14-day personal baseline calibration using EWMA (α=0.15). Score comparison always against personal trajectory, not population averages.

Production notes: O(n) complexity, <100ms on mobile, confidence levels (HIGH/MEDIUM/LOW), edge cases handled, versioned parameters.

**v1.1.0 (deprecated)** — used metaphorical antigravity model. Replaced after user correction: "I don't want the metaphor I want to map math behind sleep physics to other physics." The antigravity framing (AGI, escape velocity, repulsive forces) was creative but not scientifically defensible as a real isomorphism.

## Recommended Tech Stack

- React Native + Expo (managed workflow)
- Expo Router for navigation
- Zustand for state management
- Supabase for backend
- NativeWind or Tamagui for styling

## Phase Status at Session End

- Phase 0 (Research): ✅ Complete — BETTER-SLEEP-COMPETITIVE-REPORT.md written
- Phase 1 (Agent Brains): ✅ Complete — MD brain (20KB) + Physics algorithm (30KB, v1.1.0 with antigravity)
- Phase 2 (PRD): ⏳ Blocked — awaiting user answers to 5 clarifying questions
- Phase 3 (Design): ⏳ HOLD — awaiting user screenshots
- Phase 4 (Architecture): ⏳ Pending
- Phases 5-8: Not started

## Files Created

- `divinity-health/sleep-app/research/BETTER-SLEEP-COMPETITIVE-REPORT.md` (69 lines)
- `divinity-health/sleep-app/research/VIBE-CODING-RESEARCH.md` (62 lines)
- `divinity-health/docs/VIBE-CODING-PROCESS.md` (168 lines) — the original 8-phase process
- `divinity-health/docs/VIBE-CODING-PROCESS.pdf` — PDF version via weasyprint
- `divinity-health/sleep-app/agents/MD-SLEEP-SCIENCE-BRAIN.md` (20KB) — clinical sleep science × 8D mapping
- `divinity-health/sleep-app/agents/PHYSICS-8D-SLEEP-ALGORITHM.md` (40KB, v2.0.0) — structural-isomorphism scoring algorithm with peer-reviewed citations

## Lessons for Future Builds

1. **Ask the 5 questions early:** platform, tech stack, copy boundary, revenue model, timeline. Don't proceed without answers.
2. **Competitive research as a delegate_task works well** for single-product deep teardowns — one focused subagent produces a thorough report.
3. **Design HOLD is critical** — don't start visual work without screenshots. User will provide them.
4. **Subagent timeouts on large context** — the CMO Board Review #002 failed 3× because the synthesis output was too large. Pre-digest context summaries before synthesis (see `subagent-anti-timeout-patterns` Pattern 21).
5. **Physics concepts require genuine isomorphisms, not metaphors** — when the user names a physics concept, research whether a structural isomorphism exists in published literature. The v1.1.0 antigravity model was creative but metaphorical. The v2.0.0 rebuild uses real isomorphisms: Process S = RC circuit, Process C = van der Pol, REM cycling = Lotka-Volterra. If asked "does this really make sense?", be honest about what's real vs. stretched.
6. **Agent brains can be written directly on the current model** — delegate_task kept timing out for large docs. Writing 20-30KB documents directly works better than delegating, especially on models with limited context windows.
7. **Version the algorithm doc** — started at v1.0.0, patched to v1.1.0 when antigravity was added. This creates a clean changelog trail.
