# TSC 2026 Announcement Post Pattern (2026-08-03, rev 7)

## Lesson learned

the principal rejected rev 1 because it rehashed the existing LinkedIn pack content with a conference name attached. "You just rewrote what I already have and put a name on it."

Rev 4 used a narrative origin-story structure that was captivating BUT was later REJECTED because the narrative was fabricated (see correction below).

Rev 7 is the current approved version: states facts first, introduces theory at altitude, embeds genuine excitement without inventing history.

## CRITICAL: Never fabricate origin stories (learned 2026-08-03, binding)

the principal rejected the origin-story announcement post as "not a good post it is telling a false narrative and it is not factual." The fabricated narrative ("Two years ago I was building AI infrastructure the way everyone does. More agents. Bigger context windows. Longer tool lists. The stack kept getting heavier...") was entirely invented.

Rules:
- Do NOT invent timeline ("two years ago")
- Do NOT invent a frustration-to-insight arc
- Do NOT invent a "how I got here" section
- Genuine excitement IS allowed through anticipation phrasing, NOT through fabricated backstory
- When a post feels too dry without narrative, the fix is to add genuine excitement phrasing, NOT to invent history

## CRITICAL: No "poster" language (learned 2026-08-03, binding)

the principal does NOT want "poster," "poster number," or "poster presentation" in public copy. Frame as "I get to present my research at [conference]." Poster number and format are portal logistics, not public-facing content.

## Approved Structure (rev 7)

1. **Hook:** the actual news itself. "I get to present my research at [conference]."
2. **Sole author + field name.** One sentence.
3. **Genuine excitement.** One or two lines. Specific, not generic.
4. **Field definition at altitude.** Neuromorphic vs Physiomorphic. NOT a lecture.
5. **the operator agent.** "First system built on this paradigm, and she is live." Engines, not agents.
6. **Isomorphism score.** "Scored, not claimed" (NOT "measured"). 0.80 on zero-to-one.
7. **Falsifiable prediction.** The strongest credibility signal.
8. **Why this conference.** Why this audience specifically.
9. **What is coming.** Tease the architecture series with specificity.
10. **Audience callouts.** AI builders + consciousness researchers.
11. **Closing excitement.** "I genuinely cannot wait to share what comes next."
12. **Signature + closer.** "The posts start this week." (NOT "Bring your hardest objection" — the principal rejected that as too combative, 2026-08-03)
13. **CTA.** "If you want to learn more about the operator agent or build Physiomorphic AI systems with me, my inbox is open." (NOT "reach out" — AI tell)
14. **Hashtags.** 15 tags mixing niche brand + high-reach AI/research. See SKILL.md hashtag strategy section.

## Adversarial-cleared language (rev 7)

| Was | Now | Why |
|---|---|---|
| "I have been waiting to share this" | "I get to present my research at TSC 2026" | Generic LinkedIn bait replaced with actual news |
| "accepted my poster. Number 775." | "I get to present my research" | No poster language |
| "governing equations of its biological counterpart" | "operational principles of its biological counterpart" | "Governing equations" implies exact math replication |
| "engineered to function like a body" | "adopts the organizational structure of a biological body" | "Function like" implies functional equivalence |
| "structural correspondence is measured, not claimed" | "structural correspondence is scored, not claimed" | I(S) is a scoring methodology, not instrument measurement |
| "That number is not marketing." | (removed) | Self-undermining meta-commentary |

## Genuine excitement phrasing (approved by the principal)

- "something I could not stop thinking about"
- "now I get to put it in front of the people I most want to challenge me"
- "I cannot wait to share what comes next" (NOT "genuinely cannot wait" — "genuinely" is an AI tell, correction #38)

Do NOT use: "I have been waiting to share this" (generic, rejected).

## Anti-patterns (what failed)

- Fabricated origin stories or personal discovery narratives
- "Poster" or poster number in public copy
- Generic hooks ("I have been waiting to share this")
- "Measured" for the isomorphism score (use "scored")
- "Governing equations" (use "operational principles")
- "Function like a body" (use "adopts the organizational structure")
- Meta-commentary about marketing
- Rehashing the locked sentence with the same explanation as prior posts
- Describing the operator agent as "multi-agent system" (undersells; she is an operating system)

## Announcement Graphic Content Strategy

### What belongs on the graphic

- Field name (Physiomorphic AI)
- the operator agent name + "Now Live" label (NOT "First Implementation" or "First Living Organism")
- Proof point: "100+ specialized engines, each mapped to a biological system. An operating system that adopts the organizational structure of a biological body, not just a brain."
- Tagline: "The neuron was the beginning. The organism is the next scale."
- Author: the principal Williams / Divinity Science + the operator agent
- Conference name + city (top right: "Presenting at TSC 2026 / The Science of Consciousness · San Diego")
- Bottom right: "Multi-Agent Architecture / Biologically Structured / Not a Consciousness Claim"

### What does NOT belong on the graphic

- ~~Poster number~~
- ~~Sole Author~~
- ~~Accepted Poster Presentation~~
- ~~"First Living Organism"~~ (the operator agent is technology, not a living organism)
- ~~"First Implementation"~~ (too academic; "Now Live" emphasizes it is real)

### the operator agent graphic language (tested through 3 rejections)

1. "First Living Organism" -> REJECTED: "this is silly because the operator agent isn't a living organism"
2. "First Organism Built on This Paradigm" -> REJECTED: "it is technology not a real organism"
3. "First Implementation" -> REJECTED: too academic
4. "Now Live" -> APPROVED (emphasizes it is real running infrastructure)

On graphics, describe the TECHNOLOGY (engines, mapping, operating system), not the biology. Do NOT use "organism" as a noun for the operator agent on graphics.

### Graphic labels must EXPLAIN, not just name

A name alone with disconnected meta text does not work. the principal: "you can't really tell what the operator agent is by this." The bottom block must form a connected narrative: label (category) -> name (the operator agent) -> explanation (what it is, how it works, why it matters).

### Golden ratio composition (binding)

- Text zone = 38.2% of width (1/phi^2)
- Visual zone = 61.8% of width (1/phi)
- "ANNOUNCING" label at phi-minor from top (38.2%)
- Tagline at phi-major from top (61.8%) = the eye's natural rest point
- Author block at the bottom golden anchor
- No dead navy space

## Rendering Pipeline

1. **Diffusion** (NanoBanana/FAL/xAI) — museum quality. Always preferred when available.
2. **HTML/CSS + browser screenshot** — Cormorant Garamond + Inter fonts, SVG constellation with glow filters, golden ratio CSS layout. Serve via `python3 -m http.server 8753`, screenshot via `browser_navigate` + `browser_vision`. See `references/html-css-graphic-rendering.md`.
3. **Pillow** — acceptable ONLY for pure typography quote cards (no diagrams). Multiple Pillow iterations on complex compositions get progressively WORSE. Switch to HTML/CSS after 2 rejections.

## Pillow iteration trap

v1: flat text card (rejected: "just copying the words")
v2: constellation added but text unreadable (rejected: "can barely read this text")
v3: golden ratio layout but worse overall ("this is worse")
v4: solid left panel, brighter text (rejected: "too much open navy space, doesn't follow golden ratio")

Each pass added complexity but the Pillow rendering ceiling never improved. After 2 Pillow rejections, SWITCH to HTML/CSS.

## Ship file

`your-org-marketing/02-social-posts/TSC-2026-ACCEPTANCE-ANNOUNCEMENT.md`
