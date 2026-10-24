---
name: academic-conference-demos
description: Plan and execute live demos at academic poster sessions.
tags: [conference, demos, posters, academic-research, live-demos, exhibition]
---

# Academic Conference Demos

**Goal:** Execute successful live AI demos at academic conference poster sessions that engage attendees, showcase research effectively, and handle inevitable technical failures gracefully.

**Use when:**
- Preparing for poster sessions at conferences (NeurIPS, ICML, ACL, ASSC, TSC, etc.)
- Designing interactive elements for poster presentations
- Planning hardware setup and logistics for live demos
- Creating failover strategies for network-dependent demos
- Designing visual hierarchy for poster+demo integration

## Core Principles

1. **Reliability over complexity** - Simple working demos > complex broken demos
2. **Offline-first architecture** - Network failures are guaranteed at conferences
3. **Multiple interaction modes** - Live, pre-computed, video fallbacks
4. **Clear visual hierarchy** - 3-second rule for understanding value
5. **Presenter engagement** - Humans connect with humans, not just screens

## Workflow

### 1. Define Demo Objectives (1 month before conference)
- What research contribution are you showcasing?
- What should attendees understand in 3 seconds?
- What's the one-sentence hook?
- What interactive elements will engage visitors?

### 2. Design Offline-First Architecture
**Critical requirement:** Conference WiFi is notoriously unreliable (2000+ devices on one network)

**Implementation:**
- Run models locally on laptop or small GPU when possible
- Pre-compute complex results during setup time
- Use cached responses for common queries
- Have pre-generated example outputs ready
- Design demo to work entirely offline

**What fails:** Network-dependent demos without offline fallbacks

### 3. Create Multiple Demo Modes
**Four modes minimum:**
- **Live mode**: Real-time inference when feasible (simple tasks, <5s)
- **Pre-computed mode**: Showcase complex results instantly
- **Hybrid mode**: Live for simple tasks, pre-computed for complex
- **Demo video**: Backup when systems fail entirely

**Implementation:**
```python
# Example demo mode switching
class DemoMode:
    LIVE = "live"
    PRECOMPUTED = "precomputed"
    HYBRID = "hybrid"
    VIDEO = "video"

def get_demo_mode(network_status, complexity):
    if not network_status:
        return DemoMode.VIDEO
    if complexity == "high":
        return DemoMode.PRECOMPUTED
    return DemoMode.LIVE
```

### 4. Design Interactive Elements
**What works:**
- Pre-defined scenarios/templates users can select (dropdowns, buttons)
- Real-time visualizations (heatmaps, attention graphs, decision trees)
- Live metrics dashboards (accuracy, speed, confidence scores)
- Before/after comparisons that update live
- Interactive parameter sliders with instant visual feedback

**What fails:**
- Free-text input that's hard to validate
- Complex multi-step workflows
- Long-running computations (>5 seconds)
- Requiring attendees to create accounts or log in

**Engagement hooks:**
- "Try it yourself" mode with guided prompts
- Leaderboards or live comparison to baselines
- Scenario selectors (e.g., "ethical dilemma", "creative task")
- "Stump the AI" challenges with immediate responses

### 5. Hardware Setup
**Minimum viable setup:**
- Laptop with 16GB+ RAM
- External monitor (27" preferred for visibility)
- Power strip and extension cord (congress centers have limited outlets)
- Pre-downloaded models and data
- Backup USB drive with demo files

**Ideal setup:**
- Two laptops (primary + backup)
- Two external monitors (one for demo, one for paper/code)
- Small GPU box if running large models locally
- Tablet for attendees to interact independently
- Portable WiFi hotspot as backup (10GB+ data plan)

**Screen arrangement patterns:**
- **Split screen**: Code/architecture on left, live demo on right
- **Three-screen**: Paper on left, demo in center, metrics/code on right
- **Vertical orientation**: Portrait mode for poster, landscape for demo

**Power considerations:**
- 1-2 outlets per poster board, shared with 4-8 posters
- Power strips essential but create tripping hazards
- Battery backup (UPS) prevents crashes from power interruptions
- Bring 2x the cables you think you need

### 6. Network Strategy
**Multi-layer approach:**
```
Primary: Conference WiFi
Secondary: Personal hotspot (10GB+ data plan)
Tertiary: Offline-only mode
Fallback: Pre-computed results or demo video
```

**If using APIs:**
- Batch requests during non-peak hours
- Implement exponential backoff
- Cache all successful responses
- Have local model fallbacks for critical paths
- Set aggressive timeouts (5 seconds max)

### 7. Poster-Demo Integration
**Physical layout patterns:**

1. **Side-by-side**: Poster on left, demo table on right
   - Pros: Easy to reference poster while explaining demo
   - Cons: Requires wide poster board

2. **Stacked**: Poster top, demo below
   - Pros: Works on standard poster boards
   - Cons: Demo may be at awkward height

3. **Table extension**: Poster on board, demo on table in front
   - Pros: Optimal height for demo interaction
   - Cons: Takes up more floor space

**Cross-referencing:**
- On poster: Figure numbers match demo sections, "See live demo" callouts
- On demo: Poster title and authors visible, references to paper sections
- QR codes linking to paper, interactive demo, GitHub repo

**QR code strategy:**
- Generate multiple QR codes (paper, demo, code, video)
- Make them large (3" x 3" minimum)
- Label each clearly ("Paper", "Demo", "Code")
- Test with multiple phone cameras
- Use URL shorteners with analytics
- Place at eye level on poster board

### 8. Visual Design Guidelines
**Information hierarchy:**

**Top section (above eye level):**
- Title: 72-96pt, bold, readable from 10ft
- Authors and affiliations: smaller but visible
- One-sentence contribution hook

**Middle section (eye level):**
- Key figure showing main result
- 3-4 bullet points of contributions
- Method diagram (simple, not overwhelming)

**Bottom section (below eye level):**
- Detailed results (tables, graphs)
- References and acknowledgments
- QR codes and contact info

**Typography:**
- Headings: Sans-serif, bold (Helvetica, Arial, Calibri)
- Body text: Sans-serif for readability (Arial, Roboto)
- Math: LaTeX-style with clear notation
- Code: Monospace for examples (Courier, Consolas)

**Sizing guidelines:**
- Title: 72-96pt
- Authors: 36-48pt
- Section headings: 32-40pt
- Body text: 18-24pt
- Figure captions: 16-20pt
- References: 14-16pt

**Color and design:**
- 2-3 colors maximum (avoid rainbow)
- High contrast for text
- Consistent color coding (same color = same concept)
- White background for readability
- Test grayscale printing (8% of men are colorblind)

### 9. Handling Failures
**Network failures:**

**Automatic detection:**
- Ping test every 30 seconds
- API timeout threshold (<5 seconds)
- Fallback mode trigger when connectivity drops

**Manual transition cues:**
- "Let me show you the offline version"
- "Here's a pre-computed example"
- "I'll walk through a recorded demo"

**What to say:**
- "Conference WiFi is struggling, let me show you the cached results"
- "We have pre-computed examples that show the same functionality"
- "The live demo is struggling, here's what it would look like"

**What NOT to say:**
- "This never happens"
- "The network is terrible"
- "I don't know why this isn't working"

**Demo crashes:**
**Immediate actions:**
1. Switch to backup laptop or pre-computed mode
2. Acknowledge the issue transparently
3. Pivot to recorded demo or handout walkthrough
4. Collect contact info for follow-up

**Recovery script:**
```bash
#!/bin/bash
# Quick demo restart script
killall python  # Clear stuck processes
python demo_main.py --offline  # Start in safe mode
```

**Pre-crash preparation:**
- Document exact steps to restart demo
- Have "emergency mode" with minimal dependencies
- Test crash recovery during setup

### 10. Audience Interaction
**Pause mechanisms:**
- Implement explicit pause buttons for interruptions
- "Stop/Pause Demo" button for interruptions
- "Quick Question" mode that suspends computation
- Bookmark feature to return to interesting states
- Screenshot/save current state for discussion

**Multi-threaded interaction:**
- Demo runs in background while presenter talks
- Presenter uses hand gestures (not clicks) to highlight points
- Demo has "auto-pilot" mode for hands-free demonstration
- Separate presenter screen shows different content than audience screen

**Question categories:**
- **Technical questions**: Show code/architecture on second screen
- **Domain questions**: Have pre-prepared domain-specific examples
- **Philosophical/ethical questions**: Have ethics discussion prompts prepared

### 11. Conference-Specific Considerations

**NeurIPS (Neural Information Processing Systems):**
- Largest ML conference (10,000+ attendees)
- Poster sessions are 2+ hours, high traffic
- Mix of industry and academia
- Prepare for hundreds of visitors
- Emphasize technical contributions
- Have code repository ready

**ICML (International Conference on Machine Learning):**
- Similar scale to NeurIPS
- Slightly more theoretical emphasis
- Strong industry presence
- Focus on theoretical contributions
- Include mathematical explanations

**ASSC (Association for the Scientific Study of Consciousness):**
- Smaller, more specialized (1,000-2,000 attendees)
- Interdisciplinary (neuroscience, philosophy, psychology, AI)
- Longer poster sessions with deeper conversations
- Prepare for 15+ minute conversations
- Have philosophical discussion prompts ready
- Emphasize consciousness-related findings

**TSC (Towards a Science of Consciousness):**
- Similar to ASSC but more inclusive of speculative approaches
- Stronger philosophy and first-person science presence
- More open to novel methodologies
- Be prepared for diverse theoretical frameworks
- First-person experience demonstrations valuable

**ACL (Association for Computational Linguistics):**
- NLP-focused, strong industry presence
- Demo track specifically for interactive systems
- High expectations for real-world applicability
- Emphasize practical applications
- Interactive NLP demos expected

## Critical Pitfalls

### Technical Pitfalls

**Network dependency without fallbacks**
- Demo relies on cloud API calls
- Conference WiFi goes down or becomes unusably slow
- API rate limits kick in from multiple concurrent requests
- Result: Demo hangs, attendees walk away
- **Fix:** Offline-first architecture with multiple fallback modes

**Complex setup dependencies**
- Requires specific GPU/CUDA versions not available
- Multiple Docker containers or services that must coordinate
- Database connections that fail in conference network environment
- Result: Demo never works or requires constant debugging
- **Fix:** Test on actual conference hardware, simplify dependencies

**Long-running computations**
- Demo requires 30+ seconds to produce output
- Attendees get bored and leave before results appear
- Queue forms, reducing effective demo capacity
- Result: Low engagement, frustrated presenters
- **Fix:** Pre-compute complex results, limit live demos to <5 seconds

**Poor error handling**
- Unhandled exceptions crash the demo
- Vague error messages ("something went wrong")
- No recovery path or fallback mode
- Result: Demo appears broken, presenter looks unprepared
- **Fix:** Graceful error handling, explicit fallback modes

### Design Pitfalls

**Information overload**
- Walls of text explaining methodology before showing results
- Too many controls and options
- Complex workflows that require explanation
- Result: Attendees don't engage
- **Fix:** 3-second rule, clear visual hierarchy, show results first

**Unclear input-output relationship**
- It's not obvious what to click or type
- Output doesn't clearly relate to input
- No indication of what the system is doing
- Result: Confusion, abandonment
- **Fix:** Clear affordances, visual feedback, progress indicators

**Lack of context**
- Demo doesn't explain why this research matters
- No comparison to baselines or previous work
- Missing connection to paper's claims
- Result: Attendees don't remember the demo or paper
- **Fix:** Clear value proposition, link to paper, show impact

### Social Pitfalls

**Presenter focus on demo, not audience**
- Presenter watches demo screen, ignores attendees
- No greeting or invitation to try the demo
- No questions asked to engage visitors
- Result: Low interaction, missed opportunities
- **Fix:** Greet every attendee, invite participation, use pause buttons

**Inability to handle questions during demo**
- Demo requires presenter's full attention
- No pause/stop mechanism for questions
- Presenter can't explain while demo runs
- Result: Missed networking and feedback opportunities
- **Fix:** Pause buttons, auto-pilot mode, multi-screen setup

## Checklists

### Pre-Conference (1 month before)
- [ ] Define clear demo objectives
- [ ] Create offline-first architecture
- [ ] Design poster with demo integration
- [ ] Implement multiple demo modes
- [ ] Prepare technical handouts

### Pre-Conference (1 week before)
- [ ] Test demo on non-development hardware
- [ ] Create pre-computed examples
- [ ] Generate QR codes and test them
- [ ] Prepare backup demo materials
- [ ] Practice 20+ demo runs

### Day Before Conference
- [ ] Test on actual conference hardware
- [ ] Verify all dependencies
- [ ] Create emergency restart procedures
- [ ] Pack backup cables, power strips, drives
- [ ] Print backup poster and handouts

### Day Of Conference (2 hours before)
- [ ] Arrive early, claim power outlets
- [ ] Set up multi-screen configuration
- [ ] Test network connectivity
- [ ] Run demo 5 times consecutively
- [ ] Position screens for maximum visibility

### During Poster Session
- [ ] Greet every attendee
- [ ] Invite participation ("try it yourself")
- [ ] Use pause buttons for questions
- [ ] Switch modes if technical issues occur
- [ ] Collect contact information for follow-up

### After Conference
- [ ] Follow up with interested contacts
- [ ] Release demo code and materials
- [ ] Document lessons learned
- [ ] Plan improvements for next conference

## Strategy

### Post-Demo Follow-Up

**Immediate follow-up:**
- Collect email addresses for interested attendees
- Offer to run their specific scenario later
- Schedule follow-up meetings during conference
- Connect on LinkedIn/academic social platforms

**Conference follow-up:**
- Email demo video and slides to contacts
- GitHub repository with full demo code
- Blog post summarizing conference feedback
- Update demo based on attendee suggestions

### Continuous Improvement

**What top researchers do differently:**
- Test extensively on conference-like networks
- Have 3+ fallback modes
- Assign roles (one person demos, one person talks)
- Create attendee journey (hook → demo → follow-up)

**What to avoid:**
- Only tested on development machine
- Single point of failure (no backups)
- Presenter distracted by running demo
- Assume attendees will figure it out themselves

## The Viral Conference Demo Strategy (Google Earth Pattern)

The most powerful conference demo strategy in tech history is Google Earth's "fly to your house" hook. Researched from primary sources (Bill Kilday's "Never Lost Again," SIGGRAPH reports, Map Happenings blog).

### The 5 Viral Pillars

1. **PRESENTER-DRIVEN, NOT KIOSK** - The magic required a skilled operator. The personal Q&A ("Where are you from?") was part of the experience. You drive the demo, not the screen.

2. **THE PERSONAL HOOK** - "What's your address?" Everyone has one. 15 seconds from space to their driveway. Narcissism + visual shock + cognitive dissonance = unforgettable.

3. **GASPS DRAW CROWDS** - The audible reactions of early visitors drew curious onlookers. The "holy shit" moment was visible to passersby.

4. **EVANGELIST MULTIPLIER** - Each person who experienced it immediately told colleagues: "You HAVE to go see this." The recommendation was specific: "They type in YOUR address."

5. **VIP INFECTION** - When keynote speakers experienced the demo privately, they referenced it spontaneously in their talks.

### Finding Your "Everyone Has One" Hook

Google Earth's genius was that every person has a hometown. For your demo, identify what EVERY attendee at your specific conference has in common:

- At a consciousness conference: every researcher has a THEORY of mind
- At a health conference: every attendee has a BODY
- At an AI conference: every researcher has a MODEL

The hook must work for ALL attendees, even those whose work seems unrelated to your system. If half the audience cannot use your demo meaningfully, the viral mechanic breaks.

### Comparable Viral Demos
- Oculus at E3/GDC - "you have to try this" lines
- Wii at E3 2006 - physical personal experience
- Spotify Wrapped - personalized data you share
- Apple iPhoto demos - "your life, organized"

## Interactive Demo Concept Design Workflow

When designing an interactive demo for a poster session, follow this iterative process:

### Phase 1: Research (BEFORE designing)
1. Research cutting-edge visualization technologies available NOW (not last year)
2. Research how biological/living systems are visualized beautifully
3. Audit your system's ACTUAL real-time capabilities (routing speed, telemetry, dashboards)
4. Research the specific conference's poster requirements from the actual acceptance email or website
5. Research past viral conference demos in the target field

### Phase 2: Concept Generation (multi-panel, iterative)
- Spin up panels with DIFFERENT skill sets, not just one type of advisor
- Include at minimum: experience designer, data visualization artist, domain scientist
- Do NOT force a concept the user rejected. Kill it completely and rethink from scratch.
- The user must approve the core direction before building begins

### Phase 3: Elite Review (BEFORE building)
Have world-class domain experts review the concept:
- A domain scientist (e.g., consciousness researcher) who can identify credibility risks
- A network/complexity scientist who can assess scientific validity
- A media artist who can assess visual impact
- See `references/tsc-2026-elite-reviews.md` for the full review pattern

### Phase 4: Prototype and Harden
- Build offline-first (conference WiFi is guaranteed to fail)
- Test at 60fps or die
- Three-layer failure fallback: live, cached, recorded

## Critical Pitfall: Don't Force Rejected Concepts

When the user rejects a demo concept, KILL IT COMPLETELY. Do not attempt to patch, modify, or force-fit a rejected idea. User correction (2026-08-01): "I don't like how much attention we are putting on the wound healing process... it's too clunky and far fetched." The concept was forced through three iterations before being fully killed. Each iteration wasted time and eroded trust. When the user says they don't like something, do not try to convince them it will work. Pivot to a fundamentally different approach.

## Critical Pitfall: Do the Thinking Yourself

When running multi-panel creative work, do NOT act as a middleman summarizing subagent outputs. User correction (2026-08-01): "What brain are you using to do this work? It's super generic and not elite or world class." The agent was narrating panel summaries instead of synthesizing insights intellectually. When you dispatch panels, YOU must do the intellectual synthesis. Do not hand the user raw subagent summaries dressed up as your thinking. Read the outputs, identify the through-lines, make connections the subagents could not see, and present YOUR analysis.

## Poster Board Dimensions (Conference-Specific)

Always obtain the exact poster board dimensions from the actual acceptance email or conference website. Do not assume standard sizes.

Example (TSC 2026): Board is 4 feet high x 5 feet 10 inches wide. Poster must be SMALLER than those dimensions. This is wider than a standard 48x36 poster. The exact dimensions affect layout, visual hierarchy, and demo station placement.

## References

See `references/conference-demo-best-practices.md` for detailed research findings, company demo patterns, and conference-specific guidelines.

See `references/conference-demo-checklist.md` for printable checklists and setup timelines.

See `references/tsc-2026-elite-reviews.md` for the world-class review pattern (Anil Seth on consciousness claims, SFI on science-of-science validation, Refik Anadol on visualization aesthetics) and the Google Earth viral conference strategy research.

See `references/google-earth-conference-impact.md` for the full Google Earth viral conference playbook, psychological hook analysis, and comparable viral demo case studies.