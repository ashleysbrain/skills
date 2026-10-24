# Conference Demo Research: What Works, What Fails

Compiled from research on NeurIPS, ICML, ACL, TSC, ASSC conference demo patterns.

## What Works

### Technical
1. **Offline-first architecture** - Run models locally, pre-compute results. Conference WiFi is notoriously unreliable (2000+ devices).
2. **Simplified input paths** - Dropdowns, buttons, constrained interactions. Avoid free-text that's hard to validate.
3. **Multiple demo modes** - Live, pre-computed, hybrid, video backup.
4. **Sub-5-second response** - Long computations kill engagement. Attendees leave before results appear.

### Engagement
1. **3-second value proposition** - Bold title, visible output, one-sentence hook.
2. **Interactive elements that draw crowds:**
   - Real-time visualizations (heatmaps, dashboards, metrics)
   - Before/after comparisons
   - Parameter sliders with instant feedback
   - "Try it yourself" guided prompts
   - Leaderboards or live comparisons
3. **Physical elements:**
   - Multiple screens (laptop + external monitor)
   - QR codes linking to paper, demo, video (3" x 3" minimum)
   - Handouts with demo instructions
   - Physical artifacts attendees can take

## What Fails

1. **Network dependency** - Cloud API calls die when WiFi fails. Demo hangs, attendees walk.
2. **Complex setups** - Multi-container Docker, specific GPU versions, database connections.
3. **Long-running computations** - 30+ seconds = attendee leaves.
4. **Poor error handling** - Unhandled exceptions, vague errors, no recovery.
5. **Information overload** - Walls of text before showing results.
6. **Presenter watches demo, not audience** - No greeting, no invitation to try.

## Logistics

### Hardware Setup
- **Minimum:** Laptop (16GB+ RAM), external monitor (27"), power strip, extension cord, backup USB
- **Ideal:** Two laptops (primary + backup), two monitors, tablet for independent interaction, portable hotspot, battery backup

### Screen Arrangement
- **Split screen:** Code/architecture left, live demo right
- **Three-screen:** Paper left, demo center, metrics right
- **Portrait orientation** for poster, landscape for demo

### Power
- 1-2 outlets per poster board, shared with 4-8 posters
- Power strips essential but create tripping hazards
- Battery backup prevents crashes from power interruptions
- Bring 2x the cables you think you need

### Network Strategy
```
Primary: Conference WiFi
Secondary: Personal hotspot (10GB+ data plan)
Tertiary: Offline-only mode
Fallback: Pre-computed results or demo video
```

### Setup Timeline
- **Day before:** Test on actual hardware, verify all downloads, create offline fallback, print backups
- **2 hours before:** Arrive, claim power outlet, test network, run demo 5x consecutively, set up multiple modes, position screens

### QR Code Strategy
- Multiple QR codes (paper, demo, GitHub, video)
- 3" x 3" minimum size
- Label each clearly
- Test with multiple phone cameras
- Place at eye level on poster board
- Top-right of poster for high visibility

## Visual Design Patterns

### Typography
- Title: 72-96pt (readable from 10ft)
- Authors: 36-48pt
- Section headings: 32-40pt
- Body text: 18-24pt
- Figure captions: 16-20pt

### Color
- 2-3 color maximum (avoid rainbow)
- High contrast for text
- Consistent color coding
- Test grayscale printing for colorblind accessibility
- Avoid red/green combinations

### Poster-Demo Integration
- **Side-by-side:** Poster left, demo table right (needs wide board)
- **Stacked:** Poster top, demo below (standard board)
- **Table extension:** Poster on board, demo on table in front

### Cross-Referencing
- Figure numbers match demo sections
- "See live demo" callouts next to key results
- QR codes linking to demo for later access

## Google Earth Conference Moment (Reference Case)

Google Earth (originally Keyhole/EarthViewer) debuted at telecom/tech conferences around 2003-2005.

**What made it work:**
1. **Universal personal hook:** "Fly to your birthplace." Every person has a hometown.
2. **Visceral wow factor:** Smooth zoom from space to street level felt impossible.
3. **Quick interaction:** 30-60 seconds per person, high throughput.
4. **Spectator appeal:** Watching someone else fly to their home was compelling.
5. **Word-of-mouth engine:** "You have to try this" spread through the event.
6. **Speaker references:** Keynote speakers demoed it or referenced it organically.

**Replication framework:**
- Identify the universal personal hook for your domain
- Make the interaction fast (under 90 seconds)
- Ensure spectators enjoy watching
- Create a phrase that travels ("Go try X at poster Y")
- Map to plenary topics for speaker references
