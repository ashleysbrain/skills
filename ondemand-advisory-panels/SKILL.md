---
name: ondemand-advisory-panels
description: On-demand and recurring advisory panels with isolated sub-memory. Resume by topic name. Adversarial seats mandatory. Cutting-edge scanning required.
version: 1.0.0
---

# On-Demand Advisory Panels

## Trigger
User says anything like "resume [topic] panel", "run my [topic] advisory", "legal panel update", or mentions a specific case/topic panel by name.

## Architecture

### Registry
- Master index at `/<workspace>`
- Lists ALL on-demand panels (active + archived)
- Each panel has: Panel ID, Display Name, Created date, Status, Workspace Path, Area

### Panel ID Format
`[domain]-[topic-slug]-[YYYY-MM]`
Examples: `legal-protective-order-2026-06`, `legal-custody-2026-08`

### Panel Workspace Structure
Each panel lives at `/<workspace>[panel-id]/`
```
[panel-id]/
  coaches/           # Advisor persona files (generic, not named after real people)
  CASE_FILE.md       # Case facts, timeline, evidence log, parties, legal standing
  SESSION_LOG.md     # Running log of every session (appended, never overwritten)
  STRATEGY_BOARD.md  # Living strategy document, updated each session
  COACHING_CONTEXT.md # Panel-specific context (board purpose, seats, constraints)
```

### Sub-Memory System (3 files per panel)
1. **CASE_FILE.md** — The facts. Populated by the principal via voice. Updated by agent. Panel reads it every run.
2. **SESSION_LOG.md** — Running history. Every session appended. Nothing lost between visits.
3. **STRATEGY_BOARD.md** — Living strategy. Evolves as case develops. Updated each session.

## How to Resume a Panel
1. Read `/<workspace>`
2. Match user's invocation to a Panel ID (fuzzy match on topic slug or display name)
3. Read the workspace's CASE_FILE.md, SESSION_LOG.md, STRATEGY_BOARD.md, COACHING_CONTEXT.md
4. Read all coach profiles from coaches/ directory
5. Run the panel with full case context loaded

## Specialist Brain Concurrent Review Pattern

When the user asks for a comprehensive organism or system review with multiple dimensions (e.g., "review our organism and new objectives for robotics," "what philosophy should we use," "need several options for next project"), use the specialist-brain concurrent delegation pattern:

**Pattern:**
1. Route task through the specialist engine for specialist selection: `python3 /<workspace> --gate --situation "<situation>" --operator hermes`
2. Dispatch 2-3 concurrent delegate_task subagents with different specialist brains:
   - Design/creative cortex specialist (the specialist engine) — redesign, dimension work, creative problems
   - Quality gate/systems specialist (the specialist engine) — closed loops, architecture, validation
   - Strategic conduction specialist (the specialist engine) — business options, prioritization, build targets
3. Each subagent gets full context, same workspace access, runs in background
4. Use background=true dispatch (return delegation_id immediately) — do not wait
5. While panels run, deepen context reading (competitive landscape, audits, philosophy docs)
6. Synthesize all panel results when complete into consolidated plan with options

**Why concurrent?** Specialist brains operate on different physics/philosophy. Andreasen thinks in creative cortex patterns. Luria thinks in quality gates and failure modes. Tawara thinks in strategic rhythm and business physics. Running them in parallel produces orthogonal insights that wouldn't emerge from sequential thinking. This is the mastermind principle in action — multiple specialists examining the same question from different angles, then synthesizing.

**When to use this pattern:**
- User asks "review X, Y, Z and give me options"
- Multiple domains need simultaneous analysis (philosophy + architecture + business)
- User says "take time" and "run reviews concurrently"
- Complex organism/strategic questions with interlocking dimensions
- Any situation where the user wants SEVERAL options, not one recommendation

**Key parameters:**
- Background delegation: `delegate_task(background=true)` — return ID, don't block
- Rich context: pass workspace paths, key files, user preferences in context field
- Clear deliverable: each panel must produce concrete options, not vague strategy
- Time budget: user said "take time" — allow panels to run, don't rush synthesis

**Example from this session (2026-06-06):**
User asked: "review our organism and new objectives for robotics, etc. and help me with what we need to build next to birth a successful company and keep the the operator agent organism and her twin healthy. is there a health scoring system we can capitalize off of that can help us get our ai healthy and keep itself healthy autonomously forever using science? can we come up with an 8d for ai since 8d for ai seem s a bit off? what philosophy should we use? take time on this with specialist brains and run the reviews concurrently and iterate as many times as needed until we get a solid plan together. I need several options for next project to work on today. take your time I will be back in a while"

Dispatched three concurrent panels:
1. the specialist engine — Redesign 8D for AI with native dimensions (not borrowed human categories)
2. the specialist engine — Autonomous self-healing closed loop design (detect→diagnose→fix→learn)
3. the specialist engine — Business strategy and build options for today (robotics vs 8D360AI vs dogfooding vs curriculum)

Each panel received full context about the workspace, existing frameworks, competitive research, and user constraints. Results consolidate into ranked options with concrete next tasks.

**NOT the same as on-demand panels:** This is a concurrent specialist delegation pattern, not a registered on-demand panel workspace. It fires once per strategic review session, not on a schedule. Use ondemand-advisory-panels for recurring boards or case-specific legal panels. Use this concurrent pattern for one-off organism/strategic reviews.

## How to Create a New Panel
1. User describes the situation/topic
2. Generate Panel ID: `[domain]-[topic-slug]-[YYYY-MM]`
3. Create workspace at `/<workspace>[panel-id]/`
4. Create coaches/ directory
5. Create CASE_FILE.md with initial facts from user's description
6. Create SESSION_LOG.md (empty, ready for first session)
7. Create STRATEGY_BOARD.md (empty, ready for first session)
8. Create COACHING_CONTEXT.md with panel purpose and seat definitions
9. Build generic advisor profiles (not named after real people) with full 12-section format
10. Register panel in PANEL_REGISTRY.md
11. Run first session immediately

## Isolation Rules
- Case details NEVER enter primary agent memory (MEMORY.md or USER.md)
- Each panel workspace is self-contained
- Panel coach profiles are GENERIC (no real-person names)
- When resolved: move to Archived in registry, freeze workspace (don't delete)
- Multiple panels can exist simultaneously with zero cross-contamination

## AI Prefix Rule (All Panels)
All advisory board members that adopt human personas (named after real public figures) MUST have "AI " prefixed to their display name in every file:
- **Coach profile `name:` field** (YAML frontmatter): `name: AI Bradley Merrill Thompson`
- **Coach profile `# Title` line**: `# AI Bradley Merrill Thompson — FDA Regulatory`
- **COACHING_CONTEXT.md Board Seats section**: `**AI Bradley Merrill Thompson** — FDA Regulatory`
- **Any output, PDF, or deliverable** referencing the advisor by name

This applies across ALL panels — recurring (principal, CTO, Marketing, Product, COO, Design, Research, Legal, Gamification) and on-demand. Non-human seats (The Adversary, The Anti-Gamification Advocate, generic role titles like "Consumer Protection Attorney") do NOT get the prefix.

**When bulk-renaming coaches (all panels at once):**
1. Update `name:` in YAML frontmatter of every coach `.md` file
2. Update the `# Title` line in the same file
3. Update COACHING_CONTEXT.md "Board Seats" sections (use Python, not sed — see pitfalls below)
4. Verify no double-prefixes (`AI AI `)
5. Verify titles weren't stripped of their `—` separator

**Bulk-update script pattern:**
```python
import os, re
for root, dirs, files in os.walk(panels_base):
    if not root.endswith('/coaches'): continue
    for f in files:
        if not f.endswith('.md') or f in skip_list: continue
        fp = os.path.join(root, f)
        with open(fp) as fh: content = fh.read()
        match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
        current = match.group(1).strip()
        if current.startswith('AI '): continue
        new_name = f'AI {current}'
        content = content.replace(f'name: {current}', f'name: {new_name}', 1)
        # Also fix # Title line
        content = re.sub(rf'^# {re.escape(current)}', f'# {new_name}', content, flags=re.MULTILINE)
        with open(fp, 'w') as fh: fh.write(content)
```

For COACHING_CONTEXT.md Board Seats updates, use a proper Python function that matches the `**Name** — Role` pattern and prepends "AI " to the name, rather than sed regex which can eat the `—` separator or miss `Dr.` prefixed names.

## Coach Profile Format (12 sections)
Same as all the specialist engine boards:
1. Identity
2. Biography (generic, credentialed)
3. Detailed Framework
4. Voice Patterns
5. Decision Style
6. the specialist engine (adapted to panel context)
7. 10+ Coaching Questions
8. Red Lines
9. Output Format
10. Lane Boundaries
11. Style Guide
12. 200+ Word Sample Output

### Cutting-Edge Scanning (mandatory for all boards)
Every advisor must scan for the latest developments in their domain as part of each run. User explicitly requires: "We must always be on the cutting edge in every area." This means:
- Every board's cron prompt must include web research for the latest tech/competitive moves in that board's domain
- Coach profiles should include scanning as part of their Output Format section
- Weekly briefs must include a "Cutting-Edge Scan" or equivalent section with real findings (not fabricated)

## Reference Files
- `references/panel-workspace-template.md` — Canonical file structure and templates for new panel workspaces. Copy and adapt when creating a new panel.
- `references/build-direction-statement-pattern.md` — Reusable pattern for synthesizing multi-panel convergence into a principal-approval build-direction / scope-cut document (1-2 pages, markdown + PDF).
- `references/product-thesis-co-writing.md` — Process for co-writing product theses with advisory panels, including the pre-write codebase check, adaptive-engine framing, and PDF generation pipeline. Includes key decisions from the 8D360 thesis session (2026-06-10).
- `references/coaching-plain-english-pattern.md` — Pattern for translating technical board output into plain-English principal coaching. Every synthesis must define jargon, use analogies, explain decisions in business terms, and never escalate without coaching. User correction (2026-06-11).
- `references/meeting-prep-blocker-resolution-pattern.md` — When a panel has a standing blocker lingering across sessions, compute the answer BEFORE the meeting. Turns "discuss the problem" into "here is the answer." Worked example: XP formula stress test that collapsed a 2-week blocker before the 11am gamification meeting.

## Dialectic Session Process (3-Stage)

On-demand panels should use a three-stage dialectic process for maximum strategic quality:

**Stage 1: Advisory Team Assessment**
- Each advisor provides: assessment, top 3 actions, questions for the principal
- All in the advisor's own voice per their profile

**Stage 2: Red Team Attack** (MANDATORY — every board has adversarial seats)
- Red team advisors attack the strategy from the opponent's perspective
- Find holes, evidence gaps, strategy flaws, underestimated risks
- Probability-weighted vulnerability assessments
- **User has explicitly corrected this: "Build in an adversarial in every board, even this one."** Even niche boards, even lower-priority boards, even strategy-only boards. Never propose a board without adversarial seats.

**Stage 3: Orchestrator Synthesis**
- Takes strongest advisory recommendations
- Addresses every red team vulnerability
- Produces hardened strategy with prioritized actions
- Questions for the principal organized by urgency: MUST ANSWER NOW / NEED WITHIN 48 HOURS / CAN WAIT

### Session Output
Each session writes to:
- `SESSION_[N]_OUTPUT.md` — full session transcript (Stage 1 + Stage 2 + Stage 3)
- `SESSION_LOG.md` — appended summary of session
- `STRATEGY_BOARD.md` — updated living strategy
- `CASE_FILE.md` — updated with any new facts from the principal

### Subagent Scaling
- 13+ advisor profiles are too large for a single subagent. Split into batches of 3-5 per delegate_task call.
- Red team can run in parallel with advisory batches.
- Final synthesis may time out reading large files — be prepared to write synthesis directly.
- If a subagent times out, relaunch immediately per standard retry discipline.

## Voice Commands
- Use specific, descriptive names: "Tesla legal panel" not just "legal panel"
- User may have multiple panels in the same domain (multiple legal panels, etc.)
- Panel IDs include topic slug + date to disambiguate
- Fuzzy match on invocation: "resume my Tesla legal panel" → match on topic slug

## Engine-Embedded Advisory Boards (Seed Engine Pattern)

Advisory boards can live WITHIN engine project structures, not just in standalone `ds-wave-ondemand-panels/` workspaces. This pattern applies when:
- A the specialist engine product project needs its own advisory board
- The board's purpose is to advise on the product AND validate engine phase gates
- The board needs mixed composition (AI mirrors + DS agents + generic roles)

### Directory Structure
```
ds-seed-engine/projects/<project>/advisory-board/
  coaches/              # Advisor profiles
  CASE_FILE.md          # Market research, competitive findings, project facts
  SESSION_LOG.md        # Running session history
  STRATEGY_BOARD.md     # Living strategy with phase gate status
  COACHING_CONTEXT.md   # Board purpose, seats, engine phase mapping
  PANEL_REGISTRY.md     # Panel registration
```

### Mixed Composition Rules
An engine-embedded board can mix three types of advisors:
1. **AI mirrors** (AI prefix) — real public figures with verified credentials, e.g., "AI Matthew Walker — Sleep Neuroscience"
2. **DS personalities** (DS prefix) — science-named agents from the fleet, e.g., "DS WADDINGTON — Seed Engine Orchestrator"
3. **Generic roles** (no prefix) — composite/role-based seats, e.g., "The App Store Skeptic — Platform Risk"

All three types follow the same 12-section coach profile format. The DS personality seats act as methodology bridges — they map every product decision back to the engine's physics layers and phase gates.

### Phase Gate Integration
The board's COACHING_CONTEXT.md must include a "Seed Engine Integration" section mapping each engine phase to specific board responsibilities:
- Nucleation: Board validates market DNA
- Specification: Board defines germ layers
- Construction: Board monitors SOC cascade risk
- Integration: Board validates phase transition readiness
- Launch: Board runs pre-flight checkpoint
- Evolution: Board governs iteration dynamics

### Registration
Engine-embedded boards are registered in BOTH:
1. The project's `advisory-board/PANEL_REGISTRY.md`
2. The master panel index at `ds-wave-ondemand-panels/PANEL_REGISTRY.md` (cross-reference only)

## Legal / Insurance Claim Panels (Special Variant)

When a panel serves a legal claim, insurance dispute, or litigation matter, use the **legal claim panel pattern** — a specialized variant with plaintiff's attorney framing, insurance-carrier-aware strategy, preservation-letter urgency tiers, and landmark case research.

Key differences from standard on-demand panels:
- **5-seat composition**: Insurance Claims Strategist, Domain Systems Expert, Subrogation & Recovery Attorney, Biomechanics & Injury Valuation, Litigation Risk Analyst
- **Plaintiff's attorney perspective by default** (not neutral/advisory)
- **Insurance carrier correction protocol**: when the user corrects which carrier is involved, rebuild the entire strategy immediately — carrier identity changes duty-to-defend, bad faith dynamics, subrogation alignment, and policy language
- **Time-sensitive urgency tiers**: THIS WEEK / 30 DAYS / 60 DAYS with preservation letters as #1 priority
- **Landmark case research required**: recent verdicts, subrogation cases, regulatory actions in the domain
- **38-question framework** across policy, incident, equipment, injuries, and carrier actions
- **Data preservation urgency**: manufacturer telemetry overwrites in 30-90 days; preservation letter is always the #1 action item

Full pattern: `references/legal-claim-panel-pattern.md`

### Honcho (Wave Engine) API for Panel Backing

When using the Wave Engine's Honcho API (`http://127.0.0.1:port/v3/`) to back a panel workspace:

- **Peer cards are arrays of strings**, NOT objects. Use: `{"peer_card": ["fact1", "fact2", ...]}` — not `{"peer_card": {"facts": [...], "questions": [...]}}`
- **Messages require `peer_id`**. Every message POST to `/sessions/{id}/messages` must include a `peer_id` field.
- **Peer listing uses POST** `/workspaces/{id}/peers/list` with empty body `{}`, not GET.
- **Session messages listing uses POST** `/workspaces/{id}/sessions/{id}/messages/list` with empty body `{}`, not GET.
- **JSON via curl is fragile** — use Python to generate the JSON payload to a temp file, then `curl -d @/tmp/payload.json` to avoid shell quoting issues.
- **Correction: peer_card overwrites**. PUT to `/peers/{id}/card` replaces the entire card, not appends.

## No Crons (On-Demand Panels Only)
On-demand panels have NO cron jobs. They fire when the principal invokes them. This is the key difference from recurring advisory boards (principal, Marketing, etc.)

## Recurring Panels (Cron-Driven)
Some panels use the same workspace architecture (coaches/, CASE_FILE.md, etc.) but run on a cron schedule instead of on-demand invocation. These are registered in PANEL_MEMORY_INDEX.md alongside on-demand panels.

Key differences from on-demand:
- Have a cron job with a schedule (daily, weekly, etc.)
- May use `context_from` to read output from upstream panels
- Deliver output automatically to the user's chat
- Lower-priority panels may run weekly instead of daily

Creating a recurring panel follows the same steps as on-demand (workspace, coaches, CASE_FILE, etc.) PLUS:
1. Create a cron job with the appropriate schedule
2. Wire `context_from` to any upstream panels whose output this board needs
3. Register the cron job ID in PANEL_MEMORY_INDEX.md
4. The cron prompt must instruct the agent to read the workspace files and produce output

Naming convention for recurring panels: `ds-wave-[board]-advisory-panel-private`

## principal Advisory Board Output Format (ADHD-Critical)

The principal board is NOT a synthesizer that reprints all panel outputs. It is a **cross-panel prioritizer** that tells the principal exactly what to focus on and why. This is the single most important board output — if it's confusing, nothing else matters.

**User correction (2026-06-10):** "I'm not sure what I need to do next," "why are these next steps," "I don't want principal recommendations to only include principal stuff — I need the principal to guide me on what to focus on: marketing? products? what's the most important thing?"

### Mandatory Format for principal Brief

```
## 🎯 THE ONE THING
[Single most impactful action across ALL panels. Not just principal items.
 One sentence: WHAT to do and WHY it matters most right now.]

## 📋 PRIORITY STACK
1. [ACTION] — Why this now: [reason]. From: [which panel]. ~[time est]
2. [ACTION] — Why this now: [reason]. From: [which panel]. ~[time est]
3. [ACTION] — Why this now: [reason]. From: [which panel]. ~[time est]
[Max 5-6 items total]

## ✅ WHAT'S OFF THE LIST
[List anything the user was worried about that is DONE or SCRATCHED.
 Be explicit: "the principal CTO questions — SCRATCHED, not pending." 
 This prevents guilt loops and "stop saying I haven't been doing shit."]

## 🤔 DECISIONS NEEDED
[Only if the principal must choose between options. Keep to 1-2 max.
 State the tradeoff clearly, give your recommendation, mark it OPTIONAL.]
```

### Rules
- **Cross-domain prioritization.** The principal board ranks actions from ALL upstream panels (Marketing, Product, CTO, Research, COO, Design). It does not privilege its own domain.
- **WHY THIS NOW is mandatory.** Every action must explain sequencing. If the principal doesn't know *why* something is priority #2 instead of #5, the brief has failed.
- **WHAT'S OFF THE LIST prevents guilt.** ADHD users replay "I should be doing X" on loop. Explicitly clearing completed/scratched items is as important as telling them what to do.
- **No walls of text.** If the brief is longer than one screen on a phone, it's too long. The principal board's job is to compress, not to reprint.
- **PDF output must be clean.** No green-wall PDFs. Headers, bold actions, white space. See `references/ceo-brief-format.md` for the tested prompt structure.

See `references/ceo-brief-format.md` for the full cron prompt that produces this format.

## Pitfalls
- **NEVER pause recurring crons when the user says "pause and come back later" about a BUILD task.** They mean pause the creative/build work, not pause the scheduled crons. Confirm before pausing.
- **NEVER use non-English text in any output.** English only, always. Headers, labels, body text — all English.
- **Do not stuff panel operational details into primary memory.** Panel schedules, job IDs, coach rosters belong in the panel workspace files and PANEL_MEMORY_INDEX.md. Primary memory gets ONE pointer line.
- **On-demand panels use generic advisors.** No real-person names in on-demand panel coach profiles. Highly credentialed but fictional. Recurring panels may use real public figures with verified credentials as advisory seats (the user approves each roster).
- **Sub-memory isolation is mandatory.** Case details, legal facts, personal situation details must NEVER enter MEMORY.md or USER.md. They stay in the panel workspace files.
- **Do not flag scratched or completed items as pending.** If the user has already addressed something (e.g., questions that were scratched because they didn't align, tasks the user already called attention to), do NOT list them as incomplete or outstanding. The user will push back hard: "Stop saying I haven't been doing shit." Check with the user before including any item in a "pending" or "action needed" list.
- **Always check for existing drafts before writing from scratch.** When a board produces a deliverable (build-direction statement, scope cut, regulatory brief), it may already exist as a draft in the panel workspace. Search the workspace files first. If a draft exists but is stale or poorly written, rewrite it clean rather than starting from a blank page — but know it's there so you don't duplicate effort or contradict prior work.
- **Multi-panel synthesis for principal approval documents.** When producing a build-direction statement, scope-cut, or similar cross-panel document for principal approval: (1) delegate a subagent to read ALL relevant panel workspaces and extract convergence points, (2) write a clean 1-page document grounded in actual panel outputs with "what's in / what's out / milestones / assumptions / safety" structure, (3) generate a clean PDF alongside the markdown, (4) present with explicit approve/edit/reject framing so the user can act immediately. The document should show which panel recommended what, not just aggregate into generic advice.
- **COACHING_CONTEXT sync after coach renames.** When renaming coach `name:` fields (e.g., adding AI prefix), the COACHING_CONTEXT.md "Board Seats" section also lists advisor names. You MUST update both locations. Using sed regex on COACHING_CONTEXT is fragile — it can eat `—` separators between name and role, or miss names with "Dr." prefixes. Use Python with a proper match function instead.
- **Cron scheduling collision check for new panels.** Before setting a new panel's cron schedule, list all existing crons (`cronjob action=list`) and check for time-slot conflicts. Example: FORGE-ARBITER runs daily at 6 AM — don't put a new panel at 6 AM on Monday. Pick a clean gap (e.g., 5:30 AM Monday, or mid-hour offsets like :15, :30, :45).
- **Verify PDF delivery before reporting success.** When a panel's cron job status shows "ok", that only means the job ran — it does NOT mean the PDF was generated, is non-empty, or was delivered. Before telling the user "the X panel ran," verify: (1) the expected PDF file exists at the output path, (2) it has non-zero file size, (3) it was generated today. If a PDF is missing, say so explicitly rather than implying success. The user has corrected this: "my marketing PDF didn't come through, and I see principal PDF didn't."
- **Upstream panel completion check before principal brief.** When compiling the principal morning brief, check that each upstream panel in the cascade (Research, CTO, Marketing, Product, COO, Design) actually produced output — not just that the cron job ran. A panel that "ran" but produced no PDF or empty output is a failed panel for briefing purposes. Flag any gaps explicitly.
- **Cross-board consistency: boards must not contradict each other on committed actions.** If one board (Marketing) schedules an action and the user agrees (e.g., "3-part LinkedIn series, posting tomorrow"), another board (principal) cannot silently drop it from the priority list. The principal board must check for user commitments in upstream panel outputs before deprioritizing. When a committed action is deprioritized, acknowledge the commitment and give the user an explicit opt-out.
- **Panels ADVISE, they do not prescribe schedules or daily task lists.** User correction (2026-06-11): "The product team's trying to give me a schedule and I don't feel like that is appropriate." Panels output recommendations and strategic guidance. They do NOT tell the principal when to work on what or how to restructure their calendar. The Executive Task Manager (the specialist engine at `/<workspace>`) handles energy matching, deadline pressure, cognitive load, and daily task ordering. The correct flow: panels advise → lattice synthesizes all board outputs into a prioritized daily task table → principal executes. When a panel prescribes a weekly schedule, it is overstepping. Panels own WHAT and WHY. The lattice owns WHEN.
- **Product thesis for adaptive engine products: don't force single-dimension wedge.** When the product's core value is adaptivity (it reads the user and coaches whatever dimension they need), do NOT apply the "pick one dimension to launch with" pattern. The wedge is the engine's adaptive intelligence, not a specific dimension. Locking to one dimension contradicts the product's core value proposition. User correction (2026-06-10): "The machine engine itself is the beauty behind it."
- **Board output MUST include plain-English coaching, not just technical jargon.** User correction (2026-06-11): "you're not giving me much information... you're not really telling me what those mean... you're not helping me here. You're not giving me any coaching." When a board session (especially red team or synthesis) uses technical terms (unit economics, HRTF, CAC, LTV, patent claims), the synthesis MUST define each term in plain English with a real-world analogy (e.g., "unit economics negative = spending $2 to make $1.50 per customer, like losing 50¢ on every cup of lemonade"). Every decision escalated to the user must explain WHAT it means, WHY it matters, and WHAT happens if they choose each option. A board output that lists "HRTF: build or license?" without explaining what HRTF is and what each choice means is a failed output. The user is a principal making business decisions, not an engineer who already knows the terminology.
- **Red team factual claims MUST be verified before presenting to the user.** Subagents can hallucinate patent numbers, legal claims, competitor data, and regulatory citations. In a BetterSleep product panel (2026-06-11), the red team cited patent US10764983B2 as covering mic-based sleep tracking — but that patent is actually about "auto-calibrating light dimming load controllers." The wrong patent number was presented as a CRITICAL severity finding and nearly caused the user to spend $3-8K on an unnecessary patent attorney. **Process:** When red team advisors cite specific patents, laws, regulations, or external facts, the orchestrator MUST verify at least one claim via web search before including it in the synthesis. If verification fails or the claim is wrong, flag it explicitly and correct it in the output. Never present an unverified red team factual claim at CRITICAL severity.
- **When user pushes back on a red team claim, verify independently before defending the red team.** User correction (2026-06-11): User said "can't we do something different that gets around this patent?" and their instinct was correct — their 8D scoring method IS a genuine design-around. But the agent initially defended the red team's position instead of checking whether the user's reasoning was valid. When the user pushes back with domain reasoning, treat it as a hypothesis worth testing, not resistance to overcome. The user often understands their own methodology better than the red team understands it.
- **Pre-launch products: adjust validation questions.** For products with no users yet, don't ask "name 5 people who'd be upset if it disappeared." Ask instead about people who've shown interest, volunteered, or reached out. Segment questions for pre-launch should focus on shared frustration and motivation, not user attachment. User correction (2026-06-10): "I don't have users right now... I don't know how I'll have five real women."
- **Don't gender-restrict segments without evidence.** If interest has come from multiple genders, don't assume "women only" from initial framing. Make segments behavioral, not demographic. User correction (2026-06-10): "More than women have reached out about this."
- **API key search order.** When looking for user-provided API keys (Perplexity, Gemini, etc.), check shell config files FIRST (~/.zshrc, ~/.bashrc, ~/.bash_profile, ~/.profile) before checking the operator agent config, .env files, or environment variables. The user keeps keys in their shell config and will push back hard if you claim a key doesn't exist: "I've already given you a [provider] API. I shouldn't be having to give you another one."
- **Check existing code before recommending builds.** Before any advisory panel recommends "build X," search the codebase (hydra-os/products/, hydra-os/scripts/) for existing implementations. the principal has ADHD and will forget what's already built. Recommending a rebuild of something that took days to build the first time erodes trust fast. The 8D scoring system (8,400+ lines across 22 files) was already complete when a panel recommended building scoring from scratch. User correction (2026-06-10): "I shouldn't have to point you back to the work... I have ADHD, I'm going to forget."
- **Product thesis must reflect what exists, not just what's planned.** When a panel co-writes a product thesis or strategy document, include an explicit "what's already built" section. the specialist engine had a complete algorithm system (calculator.py, scoring_pipeline.py, coupling matrices, sigmoids) before the first thesis draft was written. Omitting built work makes the company look less mature than it is and leads to recommendations that duplicate effort.
