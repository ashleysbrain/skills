---
name: specialist-panel-ideation
description: Use when brainstorming N ideas via named-expert panel.
version: 1.0.0
metadata:
  hermes.category: creative
  hermes.tags: [brainstorming, ideation, panel, product, viral, conference]
---

# Specialist Panel Ideation

Use when the user asks to brainstorm, ideate, or generate multiple product
ideas for a specific context (conference, launch, campaign). The panel
produces diverse ideas from distinct expert perspectives, then the parent
agent synthesizes and ranks them.

## When to Use

- "Give me 10 ideas for a product/tool/app"
- "Brainstorm viral products for [event/audience]"
- "Come up with ideas for [conference/launch]"
- Any multi-idea generation task where diversity of perspective matters

## When NOT to Use

- Single-idea refinement (use scope-specific-assistant-mode)
- Technical implementation planning (use writing-plans)
- Marketing content production (use marketing-consortium)

## The Pattern (6 Steps)

### Step 1: REQUIREMENTS EXTRACTION (before any panel)

Extract EVERY requirement from the user's message into a numbered list.
This is the most common failure point: the agent latches onto ONE reference
or example and narrows the entire brainstorm to that single dimension.

User correction (2026-08-05): "go back through my message with precision
and ensure that you're hitting every one of the topics that I brought up."

CHECKLIST before building the panel:
- [ ] Re-read the full user message
- [ ] Extract every requirement, constraint, preference, goal
- [ ] Count them (if fewer than 5, re-read)
- [ ] A reference link is INSPIRATION, not a template
- [ ] Build a requirements matrix to score ideas against later

### Step 2: PANEL DESIGN

Each seat is a NAMED real-world expert with:
- Real credentials (university, institution, publications)
- 5-layer methodology profile (L1 Physics, L2 Cognitive, L3 API/Role,
  L4 Methodology, L5 Philosophy)
- ISOLATED perspective: each seat thinks ONLY about their domain

Minimum 5 seats, maximum 8. More than 8 dilutes quality. The user said
"more than 5" for panels.

Panel composition should include:
- 1-2 domain experts (the specific field the product serves)
- 1 viral/mechanics expert (what makes things spread)
- 1 product/strategy expert (network effects, aggregation)
- 1 design expert (visual artifact quality)
- 1 constraint expert (privacy, simplicity, or whatever the binding constraint is)

### Step 3: DISPATCH (sequential — one at a time)

Each seat gets their OWN subagent with:
- Their persona, credentials, and 5-layer profile
- The FULL requirements brief (not a summary)
- Their specific lens instruction ("think ONLY about X")
- Output format: name, description, viral hook, build effort, coverage notes
- A HARD OUTPUT BUDGET (see Pitfall 12): cap the response length
  explicitly in the goal ("under 900 words total")

**Dispatch ONE subagent at a time and wait for its result before
dispatching the next.** User directive (2026-08-14, verbatim): "don't run
them in parallel, concurrently only." Do NOT use the multi-task batch
form of delegate_task for panel seats, even though the delegation limit
allows 3 concurrent children. If panel has 6+ seats, combine 2-3 seats
per subagent (as distinct persona sections in one compact response) so
the total number of sequential rounds stays at 2-3.

### Step 4: SYNTHESIS (parent agent does the thinking)

The parent agent MUST do the intellectual synthesis work. This is
non-delegable. Read the raw ideas, then:
- Kill duplicates and weak variants
- Score each surviving idea against the FULL requirements matrix
- Rank by total score
- Identify the physics recommendation (biggest impact, smallest action)
- Identify the top pick and the stretch bet

Detection signal: if the output could be produced by concatenating subagent
summaries with transitions, it is not elite synthesis. THINK. Make
non-obvious connections. Kill weak ideas even if a specialist pitched them.

### Step 5: DELIVERABLE FORMAT

Present as a ranked table with every requirement scored 0-3, plus a
physics recommendation section explaining the smallest-action/biggest-impact
choice.

## Requirements Matrix Scoring

Each idea is scored against EVERY requirement from Step 1. Missing a
requirement is not an automatic disqualifier, but it must show in the score.

Example:
```
| Rank | Idea | Viral | Connection | Utility | Privacy | Signup | Build | TOTAL |
|------|------|-------|------------|---------|---------|--------|-------|-------|
| 1    | X    | 3     | 3          | 2       | 3       | 3      | M     | 20    |
```

## Step 6: ADVERSARIAL REVIEW (mandatory before showing user)

The user explicitly does NOT trust first-pass ideation output. After
synthesis, run an adversarial panel that reviews every idea before
delivery.

User correction (2026-08-05): "send it through an adversarial panel,
because I don't trust your first work, so spin up our adversarial panel,
make sure that they aren't generalists."

The adversarial panel has 4 reviewers, each isolated with real credentials:

- **Falsifiability reviewer** (the specialist engine): can you TEST whether each idea
  will go viral? What is the falsifiable prediction? Kill ideas with no
  measurable viral hypothesis.
- **Audience realism reviewer**: would the target audience ACTUALLY use
  this? What assumptions are wrong? Is it a technologist's fantasy?
- **Viral mechanic reviewer**: what is the ACTUAL viral loop, not the
  hoped-for one? Where does the sharing loop break? A utility with no
  loop is not a viral product.
- **Dignity/intelligence reviewer**: does this respect the audience's
  intelligence? Or is it a gimmick that will be mocked?

Each reviewer gives PASS/FAIL/REVISE on every idea with specific reasoning.
Consolidate into a verdict table. Kill the losers (expect 40-50% kill rate).
Re-rank survivors.

IMPORTANT: The adversarial review often KILLS ideas that scored well in
the initial synthesis. The TSC Atlas scored 19/21 in synthesis but was
KILLED 1/4 in adversarial review because it had no viral loop. Trust the
adversarial verdict over the initial scoring.

### Adversarial review execution options

1. **Dispatch as subagent** — BUT keep the context lean. Do NOT have the
   subagent load heavy skills (adversarial-elite-panel-review,
   specialist-panel-ideation, ds-popper-audit). Loading 3 skills ate the
   full iteration budget and the subagent hit max_iterations before
   writing ANY output. See Pitfall 7 below.

2. **Execute in-host** — if the subagent approach fails (max_iterations,
   context overflow), run the 4 reviewers directly in the parent agent.
   This is more reliable for adversarial review because it requires
   synthesis across reviewers, not isolated work.

Prefer in-host execution for adversarial review unless the panel is
trivially small (2-3 ideas).

## Pitfalls

1. **Anchoring on a reference** — if the user gives a LinkedIn post,
   competitor, or example, that is ONE input among many. Do not collapse
   the entire brainstorm to replicating that one reference.

2. **Combining seats too aggressively** — if you pack 7 seats into 3
   subagents and lose the silo isolation, the perspectives blend. Keep
   each seat's section distinct in the output.

3. **Listing without ranking** — the user wants a DECISION, not a menu.
   Rank the ideas. Recommend the top pick. Identify the physics-optimal choice.

4. **Skipping the requirements matrix** — without scoring each idea
   against every requirement, you cannot prove coverage. The user will
   catch missing requirements and call it generalist drift.

5. **Narrowing to one category** — if all 10 ideas are variants of "make
   a map," you have collapsed the solution space. Diversity of product
   type matters even when the user says "I don't care what categories."

6. **ENGLISH ONLY** — all panel dispatches, subagent contexts, synthesis,
   adversarial review, and output must be in English. Include "respond
   in English" in every subagent context field. The user corrected this
   when a response appeared in another language.

7. **Subagent max_iterations from heavy skill loading** — if a subagent
   loads 3+ skills via skill_view before doing its work, the context
   budget is consumed and the subagent hits max_iterations before writing
   any output. Lesson: do NOT have adversarial review subagents load
   heavy reference skills. Pass the rules directly in the context field.
   Alternatively, execute adversarial review in-host.

8. **Excuses about tooling failures** — when search tools (x_search,
   web_search, web_extract, Firecrawl) fail due to credits/billing,
   do NOT present the failure to the user as a blocker. The user
   correction (2026-08-05): "You are capable of figuring this out."
   Fallback chain: Startpage via curl -> Wikipedia API via curl ->
   browser navigation to content sites -> in-host knowledge synthesis.
   NEVER say "I cannot do this because X tool is down." Find another way.

9. **Showing ideas before adversarial review** — the user explicitly
   does not trust first-pass ideation. Do not present the ranked ideas
   without running Step 6 (adversarial review) first. Present the ideas
   AND the adversarial verdicts together.

10. **THEORY-FIRST BENCHMARK/PRODUCT DESIGN (2026-08-13)** — NEVER design a
    benchmark, product, or deliverable by starting from your own internal
    theory/framework and trying to make it a benchmark. That is backwards.
    User: "that benchmark is shit... not just a made up theory that I'm
    trying to create a benchmark for." Start from: what do people ALREADY
    need and worry about? What gap exists in the market? Run market
    research (what exists, what's missing) BEFORE designing the solution.
    Harvey's Legal Agent Bench works because it tests something real people
    already need — it did NOT start from "our legal theory should be a
    benchmark." A benchmark that only makes sense for your own architecture
    is not a benchmark, it is marketing.

11. **CHECK AUTHORITY BEFORE CLAIMING DOMAIN** — DS does not have medical,
    clinical, or diagnostic credibility. Any benchmark/proposal leaning on
    health assessment, planted pathologies, or clinical validation will be
    rejected. Know what authority DS actually has (AI architecture,
    physics-informed multi-agent systems, organism design) and operate
    within it. User: "we don't have medical credibility and clinical
    backing."

12. **SUBAGENT OUTPUT LENGTH vs API TIMEOUT (2026-08-14)** — full
    4-5-ideas-per-seat payloads (~2-3K words) exceeded the 90s
    non-streaming API window: subagents died with "API call timed out
    after 90s" or completed with the summary TRUNCATED mid-first-idea,
    losing 8+ minutes of panel work. Fix (validated): shrink each
    dispatch to 2-3 seats, cap ideas at 3 per seat, and put an explicit
    word budget in the goal ("under 900 words total") plus per-idea caps
    ("under 90 words per idea") in the context. An 81s completion with
    full payload beat the 482s/731s timeouts. Also: completed delegation
    results re-enter as conversation messages only after the parent's
    turn ends — the on-disk task log truncates summaries, so do not
    treat the log tail as the full result.

13. **DEADLINE-AWARE TRACK SELECTION (2026-08-14)** — when the venue
    deadline is <30 days out, bias topic selection toward the
    non-archival Findings/short-paper track (4-page datasets, negative
    results, critiques) rather than full archival Proceedings papers.
    Check the CFP's date table FIRST and state the days-remaining in the
    panel brief so every seat sizes effort honestly (S/M/L for the real
    window, not an idealized quarter).

## Reference: TSC 2026 Panel Example

The first instance of this pattern was a viral conference product
brainstorm for TSC 2026 (The Science of Consciousness). Panel was 8 seats:
Anil Seth, Christof Koch, Andrew Huberman, Ben Thompson, the specialist engine,
Latanya Sweeney, B.J. Fogg, Jake Epstein pattern. Produced 15 raw ideas,
synthesized to 10 ranked ideas. Full requirements matrix had 21 items.
See `references/viral-conference-market-research.md` for 9 case studies
of viral conference products (Meerkat, Foursquare, GroupMe, Clubhouse,
Slack, Hopin, Kahoot, Periscope, Jake Epstein) with the winning formula
and failure patterns distilled.

See `references/adversarial-review-example.md` for a concrete example
of Step 6 adversarial review applied to the TSC 2026 brainstorm,
showing the 50% kill rate and how ideas that scored well in synthesis
were killed by the adversarial panel.

See `references/multi-round-concept-refinement.md` for the pattern of
iterating a single concept through successive adversarial rounds
(Round 1, Round 2 with different brains), plus corrections for
reviewer overreach (public data is NOT private data, two-tier data
depth is not inequality).

See `references/ml4h-2026-emotion-ai-topic-brief.md` for the ML4H 2026
instance: venue mechanics (Findings-track bias under deadline pressure),
live 2026 emotion-AI hotness signals (functional-emotions interpretability,
companion-app dependency discourse, EU AI Act Art 5, multimodal emotion
SOTA), and the compact-dispatch pattern that beat the API timeout.

Full deliverable: ~/your-workspace/TSC-2026-TEN-IDEAS.md

## Related Skills

- `scope-specific-assistant-mode` — creative brainstorming think-don't-narrate rule
- `agent-consortium-design` — ephemeral task swarms (different from ideation panels)
- `anti-generalist-gate` — requirement extraction + anchor trap detection
