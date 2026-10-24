# Platform-First Architecture Pattern

**Problem:** Positioning and architecture focused on single engine (coaching) when product is the full platform: health data + coaching engine + task engine + scoring + gamification.

**User Correction:** "This is assuming that the only product is the wave coaching engine... the product is much bigger than just the DS wave coaching engine... the questions you're asking aren't the right questions for an all-encompassing answer."

## The Platform Layers (Locked in Thesis)

| Layer | Component | What It Does |
|-------|-----------|--------------|
| 1 | Health Data Platform | Perplexity Health clone: EHR (1.7M+ providers), wearables, labs, biomarkers, AI health Q&A |
| 2 | the specialist engine Engine | Adaptive AI coaches ANYTHING (dog training, parenting, career, finance, fitness, principal advisory). Uses 8D state as intelligence layer. |
| 3 | **the specialist engine Engine** | Crystal lattice task management. Auto-capture → auto-clarify → auto-organize → self-healing lattice. 5 personalities. |
| 4 | 8D Scoring (PIML) | Physics-informed ML moat. 8 dimensions grounded in named physics models. Coupling matrix (28 pairs). TWC coherence. |
| 5 | Gamification | Progress tracking, achievements, streaks grounded in behavioral science |

## Two Engines, One Intelligence Layer

```
┌─────────────────────────────────────────────┐
│           8D SCORING (PIML)                 │
│   Shared intelligence layer underneath      │
│   Quartz (tasks) + Wave (coaching)          │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐     ┌───────────────┐
│  DS WAVE      │     │  DS QUARTZ    │
│  Coaching     │     │  Task Mgmt    │
│  Engine       │     │  Engine       │
│               │     │               │
│ 4 modes:      │     │ 5 personalities: │
│ One-Off       │     │ Alfred        │
│ Goal-Oriented │     │ Drill Sergeant│
│ Situational   │     │ Big Sister    │
│ Advisory      │     │ Nagging Best  │
│ Panels        │     │ Gentle Coach  │
└───────┬───────┘     └───────┬───────┘
        │                     │
        └──────────┬──────────┘
                   ▼
         ┌─────────────────┐
         │  DIVINITY       │
         │  HEALTH APP     │
         │  (User sees     │
         │   one system)   │
         └─────────────────┘
```

## Integration Points

- **Wave → Quartz:** Coaching creates tasks → Quartz auto-organizes into lattice
- **Quartz → Wave:** Task completion feeds 8D scoring → Wave adapts coaching
- **Both → 8D Scoring:** Every interaction updates coupling matrix, TWC
- **User picks personality** for Quartz (Alfred, Drill Sergeant, etc.)

## 15-Second Positioning (Platform, Not Engine)

> **Divinity Health is the only AI life coach that sees your whole picture: your health data, your stress, your finances, your relationships, your tasks. And it coaches and executes whatever needs attention most using real science, not generic advice.**

**Key elements:**
- "Sees your whole picture" — health data + wellness + tasks
- "Coaches AND executes" — two engines working as one
- "Real science, not generic advice" — PIML moat
- Category: "AI Life Coach" (not wellness app, health tracker, 8D coach, to-do list)

## First 30 Seconds (Platform Experience)

1. **One open question:** "What's going on right now?"
2. **User speaks:** "Exhausted, stressed about money, haven't slept in weeks"
3. **System parses 8D + coupling:** Psychological + Physical + Financial + coupling
4. **PIML priors generate insight:** "Stress, sleep, and finances pulling on each other"
5. **User picks one:** "Sleep"
6. **Wave gives protocol** → **Quartz instantly breaks into lattice** (wind-down 9 PM, phone out, magnesium)
7. **One task at a time, matched to energy, lattice self-heals**

## Thesis Update Checklist

When adding new engine/component:
- [ ] Add as new Layer in Product section
- [ ] Update "What's already built"
- [ ] Update v1 scope
- [ ] Update Long-term vision
- [ ] Update The Wedge
- [ ] Update Category positioning
- [ ] Update First 30 Seconds experience
- [ ] Update How Coaching Works → "How Coaching and Execution Work Together"
- [ ] Update What This Unlocks (Marketing, Product, CTO, Design, COO)
- [ ] Update lock confirmation line

## Anti-Patterns to Avoid

❌ Positioning single engine as the product
❌ "Week 1/Week 2" human timelines for AI builds
❌ Questions that assume single-engine scope
❌ Forgetting task engine in platform narrative
❌ Separate intelligence layers (must be ONE 8D scoring)