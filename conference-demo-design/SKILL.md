---
name: conference-demo-design
description: Interactive prototypes for conference demos and posters.
tags: [conference, poster, demo, prototype, interactive]
---

# Conference Interactive Demo Design

Use when preparing a poster, demo, or exhibition for an academic or industry conference. Covers the full pipeline: brainstorming the interactive hook, designing the physical+digital experience, building offline-first, and engineering word-of-mouth virality through the event.

## When to Use

- User has an accepted poster/presentation at a conference and wants an interactive prototype
- User wants to "draw crowds" or "go viral through the event"
- User references a famous conference demo (Google Earth, etc.) as the bar
- User wants speakers to reference their poster/demo from the main stage
- User asks to brainstorm "what prototype to build" for a conference

## Core Philosophy

The poster is NOT the deliverable. The EXPERIENCE at the poster is the deliverable. The poster is the backdrop for a live, interactive encounter that makes each attendee feel personally addressed.

## The "Personal Hook" Framework

The single most important design question: **What does EVERY attendee have that your demo can make personal?**

Reference case: Google Earth at telecom conferences (~2005). Everyone has a birthplace/hometown. "Fly to your birthplace" made a planetary-scale tool intimate. People lined up. Speakers referenced it.

### Finding the Hook for Any Domain

| Domain | Universal Hook | Personalization Mechanism |
|--------|---------------|--------------------------|
| Consciousness research | Everyone has a theory of mind + a secret wonder about machine consciousness | Connect their research to your system |
| Health tech | Everyone has a body that sometimes fails | Show their health pattern |
| AI/ML | Everyone has an opinion on AGI timelines | Let them test their prediction |
| Developer tools | Everyone has a bug they gave up on | Run their failure case live |
| Academic conferences (general) | Everyone has a paper and wants to know who their hidden neighbors are | Map all conference papers against your system, show hidden connections |

### Hook Validation Criteria
1. **Universal** - every attendee has one, no exceptions
2. **Specific** - no two attendees produce the same output
3. **Shareable** - the output is worth showing to a colleague
4. **Offline-safe** - does not require real-time data the conference WiFi cannot provide

## Workflow

### 0. Audit System Capabilities + Research Visualization (BEFORE designing the demo)

**This step is MANDATORY before any concept design.** Designing a demo without knowing what is technically feasible causes rework cycles.

- Run a capability audit of the system being demoed (live probe, not documentation)
- Research cutting-edge visualization techniques (Three.js WebGPU, particle systems, shaders, WebGL)
- Research biological/neural visualization patterns (connectomes, Kuramoto models, reaction-diffusion, free energy visualization)
- Write all findings to reference files

### 1. Research the Reference Demo
Study the reference demo the user cites. Delegate to a subagent. Write to `/tmp/<reference>_conference_impact.txt`.

### 2. Spin Up a World-Class Advisor Panel
Assemble 3 advisors with DIFFERENT genius types:

| Advisor Archetype | Optimizes For |
|---|---|
| Experience Designer (Chesky) | How it FEELS. The personal takeaway. The collectible artifact. |
| Impossible Tech (Abrash) | The PRESENCE moment. The visceral "that shouldn't be possible." |
| Spatial Computing (Underkoffler) | The BODY engagement. Using physical space, not just screens. |

Synthesis: Spatial gives the STAGE, Impossible gives the MOMENT, Experience gives the TAKEAWAY.

### 3. Design the Experience Arc

```
APPROACH -> ENTER -> [INTERACT] -> [IMPOSSIBLE MOMENT] -> LEAVE WITH PROOF
```

**MANDATORY: Validate with user after each concept round.** Present a ONE-SENTENCE version of the concept. Ask: does this land? Do not spin more panels before checking. The user is the sole author and knows the thesis better than any panel. Early validation saves entire wasted brainstorm cycles.

**Concept validation question to ask the user:** "When you picture someone walking away from your poster saying 'you HAVE to go see this,' what is the thing they just experienced?"

### 3b. Map Demo Interactions Against the FULL Thesis

Before committing to any interaction, verify it serves the whole argument:
- List every claim in the abstract/paper
- Map each proposed demo element to which claim it supports
- If one element dominates but only supports one sub-claim, it is over-indexed
- The demo must serve the full thesis, not one advisor's favorite feature

### 4. Engineer the Viral Loop
1. Every person gets a DIFFERENT output
2. The hallway conversation writes itself
3. The phrase that travels (one-sentence hook people repeat)
4. The collectible (physical cards = visible social proof)
5. Speaker bait (make demo relevant to plenary topics)

### 5. Pre-load Conference Data
Pre-bake: all session topics, co-presenter names, abstract titles, plenary themes. Store locally (SQLite/JSON). Attendee enters name, system recognizes them and references their abstract.

### 6. Offline-First Architecture

```
Layer 1: Live demo (full functionality, local)
Layer 2: Cached snapshots (pre-computed results)
Layer 3: Recorded demo loop (4K video)
Layer 4: Printed screenshots (physical backup)
```

### 7. Physical Setup Checklist

**Hardware:** MacBook Pro, iPad (angled for standing), external monitor, iPhone hotspot (backup), battery pack, power strip, extension cord, backup MacBook.

**Print:** 300 personal artifact cards, 50 handout summaries, 3" QR codes, business cards with poster number.

**Logistics:** Arrive 2 hours early, run demo 5x before doors open, mount display at eye level.

### Pitfall: Acting as middleman instead of elite thinker (2026-08-01)
The user said: "What brain are you using to do this work? It's super generic and not elite or world class."

**What happened:** Advisory panels were dispatched, their outputs were summarized and relayed to the user verbatim. The agent acted as a transcription layer, not a thinker. Generic "LinkedIn with a biology wrapper" social networking suggestions were produced instead of elite-level analysis.

**Fix:** When the user asks for "world-class" or "elite" work, the agent must DO the thinking, not delegate and narrate. Subagents provide raw material. The agent's job is to synthesize at a level beyond what any individual subagent produced. If your synthesis sounds like it could come from a consultant deck, it is not elite. The user detects this instantly.

**The test:** Would this specific output impress a domain expert, or does it sound like a smart generalist summarizing what domain experts said? If the latter, redo it.

### Pitfall: Producing generic social/SaaS features for a scientific context (2026-08-01)
When asked about post-conference networking, the response was "opt-in network" and "the operator agent facilitates introductions." This is startup pitch language applied to consciousness science.

**Fix:** For a scientific audience, every feature must have scientific justification. "Networking" should be framed as "discovering structural holes in the citation network" and "generating falsifiable predictions from cross-domain connections." The user is a scientist presenting to scientists. SaaS patterns insult the audience.

## Pitfalls

### Pitfall: Demoing features instead of delivering an experience
If your demo could be replaced by a YouTube video, it is wrong.

### Pitfall: Relying on conference WiFi
Conference WiFi WILL fail. Offline-first is non-negotiable.

### Pitfall: Latency kills presence
Hard gate: 60fps render, sub-2s response.

### Pitfall: One-person demo creates a queue
Design for SPECTATORS: what they see while waiting must compel them to stay.

### Pitfall: Giving away proprietary architecture
Show anatomy, not schematic. No ports, no internals, no routing weights.

### Pitfall: Forgetting the speaker reference strategy
Map demo moments to plenary session themes.

### Pitfall: Forcing unrelated interactions into one composite experience (2026-08-01)
When synthesizing multiple advisor pitches into one experience, DO NOT bolt separate interactions together with a forced causal link. The user will immediately see the seam.

**What happened:** Three advisors pitched three separate demos. The synthesis said "wound the part of the organism that maps to your research topic." This made no sense. Why would studying IIT mean you want to lesion a thalamus? Two great demos wearing the same costume.

**User correction (verbatim):** "I don't understand how processing their research through the operator agent makes a wound. I don't get it."

**Fix:** When combining advisor ideas, every step must connect CAUSALLY to the next. Test each causal link by asking: "Why would doing step N make someone WANT to do step N+1?" If the answer requires mental gymnastics, the link is forced. Either find a genuine causal connection or let one interaction stand alone. A single coherent interaction beats a Frankenstein of three.

**The validation test:** Can you explain the full experience in ONE sentence where every clause follows logically? If you need "and then" or "which also" to bridge steps, the concept is not unified.

### Pitfall: Over-indexing on one feature that isn't the central thesis (2026-08-01)
A single advisor can hijack the entire concept if one interaction is viscerally compelling. Cascade resilience (wound/heal) was pitched hard and the panel ran with it, but it only supports self-regulation, which is 1 of 4 consciousness correlates. It is not the whole thesis.

**User correction (verbatim):** "I still don't like this. It's too clunky and far fetched. I don't like how much attention we are putting on the wound healing process, unless that's the whole physiomorphic AI argument."

**Fix:** Before committing to any single interaction, map it against the paper's full thesis. If the interaction only supports one sub-claim, it should not dominate. The demo must serve the whole argument, not one advisor's favorite feature.

### Pitfall: Skipping iterative concept validation with the user (2026-08-01)
Three full rounds of advisor panels were run before the concept converged. Round 1 forced a composite. Round 2 forced the same composite with a causal chain. Round 3 was killed because the scope expanded beyond three advisors. The convergence only happened when the user was asked directly: "what is the hook in your gut?"

**Fix:** After each round of concept generation, present the user with a ONE-SENTENCE version of the concept and ask: does this land? Do not spin three more panels before checking. The user is the sole author and knows the thesis better than any panel. Early user validation saves entire wasted brainstorm cycles.

### Pitfall: Designing the demo before researching visualization capabilities (2026-08-01)
The concept was designed first, then the team tried to figure out if the visualization was feasible. This caused multiple rework cycles. Research what is visually possible (WebGL, Three.js WebGPU, particle systems, shader-based techniques) BEFORE committing to a demo concept.

**Fix:** Sequence: (1) audit the system's real capabilities, (2) research cutting-edge visualization options, (3) THEN design the demo concept constrained by both. Feasibility shapes concept, not the reverse.

### Pitfall: The "pre-broadcast" strategy
Google Earth had CNN Iraq War coverage to prime audiences BEFORE the conference. Your demo needs an equivalent: publish a provocative pre-conference essay or paper that attendees read before arriving. They show up primed and seek out your poster.

### Pattern: The Constellation — structural hole discovery as the personal hook (2026-08-02)

When the user has a system that can process multiple inputs and the audience is a community of researchers, the personal hook may be DISCOVERING HIDDEN CONNECTIONS between their work and others'.

**The concept**: Pre-process ALL conference abstracts/papers through the system. Each produces a unique activation pattern. Two papers that activate similar pathways are "architecturally resonant" even if they sound nothing alike on the surface. The attendee enters their topic and sees:
1. Their theory placed in a constellation of all conference papers
2. Hidden neighbors they didn't know about
3. A take-home card showing their research neighbors

**Why this is the Google Earth equivalent**: Every researcher has a theory. That theory activates specific pathways in a structured system. Showing them which other theories resonate through the same pathways is the equivalent of "fly to your house." It is deeply personal, universally applicable, and something only their system can do.

**Critical caveat from elite review panel (Anil Seth, SFI, Barabasi)**: This concept is NUMEROLOGY unless validated:
- Run null model (random mapping baseline)
- Run BERT/LDA baseline comparison (does the architecture see what standard NLP misses?)
- Run stability analysis (same abstracts twice, same result?)
- Overlay with citation network (where they diverge = true structural holes)
- Frame as "instrument output" not "AI truth"

**The phrase that travels**: "Go see what the operator agent says about YOUR theory."

See `references/elite-review-methodology.md` for the four-reviewer validation gauntlet and `references/poster-constellation-concept.md` for the full concept with Anadol aesthetic specs, Seth rigor requirements, and SFI catalytic potential analysis.

## Specialist Routing

- **the specialist engine** for brainstorming and experience design
- **the specialist engine** for poster layout and visual design
- **the specialist engine** for real-time visualization aesthetics
- **the specialist engine** for poster PDF and handout rendering

## Reference

- `references/tsc-2026-poster-specs.md` - TSC 2026 San Diego poster specs (board dimensions, session details, co-presenters)
- `references/the operator agent-live-demo-capabilities.md` - What the operator agent can actually do live (verified by probing infrastructure). Read this before designing any the operator agent demo.
- `references/conference-demo-research.md` - Past conference demo patterns (699 lines of logistics, what works, what fails)
- `references/google-earth-conference-strategy.md` - The 5 viral conference pillars from Google Earth's legendary demo
- `references/google-earth-tessellation-for-ai-organisms.md` - Quadtree/pyramid data architecture mapped to AI organism agent routing
- `references/tsc-2026-conference-structure.md` - Full TSC 2026 program data: schedule, 14 plenary topics, concurrent tracks, poster sessions, hackathon details, all 48 confirmed speakers. Read this before designing any TSC-specific tool or demo.
- `references/elite-review-methodology.md` - Four-reviewer panel methodology (domain expert, network scientist, meta-scientist, artist). The validation gauntlet. 90-second answer template. Epistemic framing rules.
- `references/visualization-aesthetic-spec.md` - Anadol-level aesthetic specs for living-system visualizations: breathing rates, color discipline, particle behavior, instant-death mistakes. Read before any visualization concept is finalized.

## Related Skills

- **`social-content-pipeline`** - Conference-adjacent social media content
- **`p5js`** - Interactive sketches for rapid prototypes
