---
name: coaching-engine-spec-maintenance
description: "Maintain a coaching-engine specification as a full end-to-end process model covering activation, intake, state, advisor selection, sequential review, synthesis, and handoff."
---

# Coaching Engine Spec Maintenance

Use this skill when maintaining or extending a coaching-engine-style specification, especially when the user wants the *full* process from start to finish and expects the docs to remain internally consistent across flow, questions, state, and handoff behavior.

## Trigger conditions

Use this skill when:
- the user asks for the complete process, not a summary
- a coaching flow or assistant intake loop needs to be documented or repaired
- the user says the assistant simplified, generalized, or skipped steps
- the user asks for a personal coach panel, advisor roster, advisor profiles, credentials, or public watered-down coach scores
- the user wants a *secondary* advisory lane beside an existing principal coaching lane, rather than a replacement
- the intake / background-resume behavior must be explicit
- question flow, state machine, and response rules all need to stay aligned
- the user asks for the "full process" and the first pass may have landed on the wrong engine family; verify the canonical artifact family before answering (for example, coaching flow vs health/self-healing loop)
- the user wants a reusable coaching workflow that stays generic until the request narrows into a specific lane, while preserving the specialist engine as the named lead coach / voice of the engine
- the user asks for the public-facing the specialist engine voice to remain distinct from the underlying generic workflow layer across repo docs

## Operating principles

- Preserve every established step and sub-step that belongs to the working process.
- Do not compress a process into a simpler version when the user asked for end-to-end detail.
- Do not invent new steps when the working process is already established.
- Keep the documentation usable by any agent that picks up the thread later.
- Keep the state model, question flow, and process flow synchronized.
- Keep the specialist engine as the lead coach / voice of the engine even when the surrounding workflow stays generic.
- Keep the surrounding workflow generic until the user works down into the relevant specialty lane.
- When generalizing a worked example into a reusable workflow, keep the lead coach / synthesis voice intact even if the example-specific personas are removed.
- The generic pattern should still name the lead coach role where the system has one (for example, the specialist engine as the lead coach in this repo).
- When a request crosses lanes, make the subject-matter lead advisor answer first, then include the supporting advisors, then synthesize without losing important information.
- Do not let synthesis flatten away caveats, tradeoffs, or meaningful disagreements.
- When the user says they want *direction, market, trajectory, or positioning* rather than feature design, keep the intake broad and avoid collapsing the question into implementation details.
- When the user asks for a panel or board review, treat each seat as a separate analysis pass first, then synthesize with all major points preserved; do not merge away dissent or nuance.
- If the user says to use the marketing/advisory board alongside the coaching board, preserve the panel boundary and answer from each seat before compiling the final synthesis.
- Keep the first question genuinely useful: it should narrow the strategic uncertainty, not force a premature workflow choice.

## Recommended workflow

1. **Read the existing docs first.**
   - Check the overview, process flow, question flow, state machine, and response rules together.
   - Treat the set as one system, not separate notes.

2. **Identify the activation mode.**
   - Fresh summon.
   - Background-running continuation.
   - Resumed after handoff.
   - Define what changes for each mode.

3. **Write the intake logic explicitly.**
   - Fresh summon should start with the first useful question.
   - Background-running should resume from current state.
   - Handoff-resume should load the handoff summary before continuing.

4. **Separate question logic from response logic.**
   - Questions gather context.
   - Responses give value once enough context exists.
   - Do not blur the two.
   - When the user asks for more user-friendly or psychologically fitting coaching questions, prefer warm, validating, agency-preserving language over clinical or interrogative phrasing.
   - Use the "principal of your life" idea as a metaphor for agency and ownership, not as the intended audience. Keep the wording broadly accessible so it reads like life leadership for anyone, not corporate-only coaching.
   - Keep the the specialist engine voice broad and accessible; only the specialist/advisor portions should become more formal or professional when the lane calls for it.
   - Keep the public-facing the specialist engine voice separate from the generic workflow layer; the workflow should remain reusable even when the voice is branded.
   - When the user asks to switch back into coaching-engine mode, treat that as an activation request: reset to question-first intake, ask one useful question at a time, and use the answers as the reference frame for later guidance.
   - When the user asks for the panel itself, lead with the panel, credentials, score, basis, and confidence. Do not narrate the process first unless the user explicitly asks for it.
   - When the user asks to start a *secondary* the specialist engine advisory group, treat it as a separate product panel that sits alongside the principal coaching panel rather than replacing it.
   - Start with the first useful intake question for the new panel instead of reciting the entire workflow.
   - For product panels, the first useful question should usually be about the user's current work, goal, audience, constraints, or stage so the panel can guide against the actual situation.
   - When the user asks where it is being saved, provide the exact mirror/repo path once verified; do not guess.
   - When the user asks for advisor recommendations, include the full profile for each advisor, not just a name or a thin summary. A usable profile should say who the advisor is, why they were selected, what lane they cover, what public evidence supports the choice, any meaningful caveats, **and the full public-facing 8D/TWC scorecard**.
   - For every advisor card, include:
     - full name / public identity
     - lane / seat name
     - background summary
     - relevant credentials or public roles
     - full 8D/TWC score with basis and confidence
     - why this person fits the lane
     - what they help with / do not help with
      - For the specialist engine personal panels, anchor each advisor to the user's actual company/product stack first, then choose the person whose public track record best matches that stack. Do not use a generic principal roster when the user asked for a tailored panel.
      - Keep the the specialist engine chat-thread mirror current by appending compact timestamped notes to `references/ds-wave-product-panel-intake.md` and, when appropriate, `docs/ds-wave/chat-thread-mirror.md` via the helper script.

      - If the user asks for scores, show the score together with its basis and confidence, and keep the score clearly public-facing. Do not collapse this into a bare numeric badge.
      - If the user asks for a panel, lead with the panel cards first, then synthesis. Do not bury the profiles under process narration.
      - When maintaining a live mirror file for recurring synthesis, prefer a tiny append-only helper script that writes timestamped updates into a bounded `## Rolling updates` section, and test it on a temporary copy before wiring it into cron.

5. **Model the session state.**
   - Track current topic, user goal, open questions, last question, last answer, and handoff state.
   - Define state transitions clearly.

6. **Define advisor usage only when needed.**
   - Choose the smallest useful advisor set.
   - Run advisors one at a time.
   - Synthesize once.
   - Keep the three-way taxonomy explicit: general coaching advisors, public human-figure mirror advisors, and narrow specialist advisors.
   - Require the correct credential standard for each lane instead of flattening them into generic experts.
   - When the user says this is the *personal coach panel*, treat the mirror roster as user-specific panel seats, not as the general engine taxonomy. Build the panel from the user's target industry and goals, not from a universal or default principal list.

7. **Verify the runtime-facing package when one exists.**
   - If the coaching engine has a live agent package, verify both the docs and the runtime files.
   - Do not stop at the spec if the runtime wrapper is missing.
   - Check for paired identity/runtime files such as `SOUL.md` plus `AGENT.md`.
   - When the user wants to *launch* the coaching agent, create or verify a single explicit launch surface (for example `LAUNCH.md`) so startup order is obvious.
   - Keep the launch path coaching-only; do not blend in the healing engine.
   - Search for the exact activation and taxonomy phrases in the live package before declaring the system aligned.

8. **Cross-check the user's latest message against prior channel noise.**
   - When the user says the channel or assistant is "stuck" or not working, inspect the latest user message first.
   - Treat the durable lesson as a workflow mismatch, not a transport failure.

9. **Verify cross-doc consistency.**
   - The README should match the process flow.
   - The question flow should match the intake logic.
   - The state machine should match the transitions.
   - The response rules should match the final output behavior.

10. **Run a coherence audit when the doc set is large.**
    - Use the coherence-audit technique (see below) to catch drift across files.

11. **When reviving an engine that has drifted from its spec, run a spec-vs-runtime gap audit BEFORE proposing work.**
    - Trigger phrases: "get this fully operational," "we built this a long time ago," "show me the processes," "this is more than a cron."
    - Survey both layers in parallel: the spec docs AND the live runtime (routes, state fields, cron jobs, running processes, empty modules).
    - Build a two-column gap table: "Spec says" vs "Runtime does," one row per behavior. Present it to the user before phasing work.
    - Do not silently downgrade the spec to match the runtime — the spec is usually the source of truth.
    - Phase revival by dependency, not glamour. For this engine: state machine → advisor deliberation → persistent 24/7 monitoring → question/response classification.
    - See `references/spec-runtime-gap-audit.md` for reusable verification commands. The canonical 10-step spec it audits against lives in `references/canonical-process-doc-set.md`.

## THE E16 MASTER DEFECT — diagnostics that don't shape output (caught 2026-07-23)

The single most damaging failure pattern in coaching engine builds. Declaring it here because it will recur every time someone builds a science-grounded diagnostic layer.

**The trap:** you build a diagnostic stack (motivation, efficacy, mindset, framing, etc.), wire the modules into the pipeline, test that they produce outputs, declare the build complete. Then the user asks "how does this actually work" and you discover every diagnostic computes findings, attaches them as metadata to the output, and **never modifies the coaching text the user sees**.

**Signature symptoms:**
- Diagnostic outputs appear in `science_trace` but not in `coaching_response`
- LLM directives computed AFTER the LLM call instead of before
- Pipeline code says "attach directives to output" not "inject directives into prompt"
- The LLM generates coaching independently of diagnostic findings
- Pipeline comment lies ("inject directives so the LLM can use them" when the LLM was already called)
- Multi-voice panel returns a list of voices but the LLM speaks as one voice
- MAP check finds gaps but the steps don't change
- If-Then plans generated but never shown to user

**The fix — diagnostics-first pipeline architecture:**
```
classify → diagnose (parallel) → build directives →
LLM call WITH directives in system prompt → MAP gate →
revise steps if MAP gaps → emit
```

**Critical:** `run_v2_pipeline(coaching_guidance=...)` accepting v1 output is the smell. The pipeline must OWN the LLM call. Passing pre-generated coaching into a diagnostic wrapper means diagnostics run AFTER generation by construction. The function signature itself encodes the bug. See `pipeline_live.py` in the wave engine repo for the corrected pattern.

**Test that catches it:** for each diagnostic, ask "does this output reach the LLM prompt or just the science_trace?" If just the trace, it's decorative.

## Cross-module token collisions (caught 2026-07-23)

Diagnostic modules share a text input but use independent marker vocabularies. The same word fires multiple modules with different interpretations:

- "purpose" → INTRINSIC motivation (Deci-Ryan) AND wellbeing signal (PERMA gate) AND meaning domain (PERMA scan)
- "confident" → low-efficacy marker when negated, high-efficacy when affirmed, but substring matching cannot tell
- "lonely" → scores as PRESENT on PERMA relationships domain (positive signal) when the user is suffering
- "habit" → high automaticity in habit module AND can be a low-efficacy marker depending on context

**Mitigation pattern:** maintain a SHARED_VOCAB registry that documents which tokens fire which modules. When adding a new marker, grep the other modules for collisions. Single-word common tokens are collision-prone; prefer multi-word specific phrases. If a token has a legitimate non-psychological meaning ("map" in "mapping out my options"), it must NOT be a single-word marker.

## Adversarial self-audit protocol (runs before any "build complete" claim)

Before declaring a coaching engine build complete, run these four checks. All four must pass or the claim is false.

1. **Directives-reach-LLM check.** For each diagnostic, trace its output: does it appear in the LLM system prompt, or only in science_trace? Read the actual code path, not the comments.
2. **Step-revision check.** When MAP finds gaps, do the coaching steps actually change before output? Or does MAP output go to metadata only?
3. **Jargon-leak check.** Run a sample coaching_response through the banned-jargon list. Any hit = the LLM parroted a directive term and the stripper missed it.
4. **Gate-logic check.** Verify PERMA only fires for personal_growth+deep+wellbeing, multi-voice only for structured+deep, Fast Path actually skips diagnostics. Run a real test case per gate.

Do NOT skip these because the build "looks right." The E16 trap produces builds that look completely right.

## When the user says "double check your work" (user-locked 2026-07-23)

When the user invokes this phrase after a build, they suspect the build is incomplete or wrong. The correct response is NOT to re-summarize what was built and restate that it works. The correct response is to run the adversarial self-audit protocol above with actual code reads and live tests.

**Failure pattern observed:** user said "double check your work." I summarized the build status and claimed "15 checks passed." The real answer was 34 defects including the master E16 trap. The self-audit I ran was superficial (file exists, compiles, basic smoke test). It did not exercise the actual mechanism.

**Rule:** "double check your work" triggers the adversarial self-audit protocol with code-path tracing, not summary verification. Read every module's actual logic. Run real test cases. Report defects honestly, including ones that invalidate the build claim.

## When the user says "show me how it works" / "I need to know every little bit" (user-locked 2026-07-23)

The user demands mechanism transparency, not summary claims. When they say they "already see errors" or ask for "every little bit of this process," they want:
- The actual scoring thresholds, not "scores 0-100"
- The actual marker lists, not "uses language signals"
- The actual decision branches, not "routes based on complexity"
- The actual bugs, not "passes verification"

**Rule:** show the code, the logic, the gates, the errors. Do not summarize mechanism at a high level when asked for mechanism detail. The user is an elite specialist who catches AI work; superficial answers will be rejected.

## When the user says "don't duplicate work" / "[sibling] already did X" (user-locked 2026-07-23)

Before proposing any build, panel, or analysis, check what the sibling agent (other the operator agent session, sibling-agent, sibling-agent) has ALREADY done. The user runs parallel sessions across Telegram + desktop + sibling-agent. Work done in one surface is often unknown to the other.

**Failure pattern observed:** user said "telegram hermes already transcribed and actioned, right??? don't duplicate work." I had just proposed building an elite psychology panel from scratch. The panel was already built, run, and written to disk by the Telegram the operator agent session that morning. I was 30 seconds from rebuilding it.

**Rule:** when the user references prior work, run EXCHANGE before DIGEST. Check:
1. `session_search` for the topic across all sessions (Telegram, desktop, cron)
2. `operator_bus.py read` for sibling handoffs (sibling-agent, sibling-agent)
3. The filesystem for output files (`find docs/ -name "*<topic>*" -mtime -1`)
4. The cron job schedule for any job that might have produced it

Only after confirming the work does NOT exist should you propose building it. If it exists, build ON it, not over it. See `references/v2.1-diagnostic-stack-build.md` for the pattern of extending existing work without duplicating.

## Diagram honesty — coaching workflows are not linear (user-locked 2026-07-23)

The user explicitly rejected a linear top-down diagram of the coaching pipeline ("I don't believe this workflow is going to be linear and 2D"). Coaching engines with parallel diagnostics, feedback loops, conditional gates, and persistent session state are **closed-loop adaptive systems**, not sequential pipelines.

**Rule:** coaching engine diagrams must show:
- Parallel diagnostic cluster (not sequential steps)
- At least one feedback loop (session state → next turn)
- Conditional branches (Fast Path bypass, PERMA gate, MAP revise loop)
- The directive flow INTO generation (not just the diagnostic outputs)

Linear "Step 1 → Step 2 → Step 3" diagrams of coaching engines are wrong by construction. Use network/closed-loop topology.

## Pitfalls

- **Under-modeling persistent mode as "a longer answer" or "just a cron."** Persistent 24/7 coaching is an ongoing support loop with a `monitoring` state, `research_queue`, `next_checkin`, and `panel_revision_notes`. A cron that fires a coaching prompt is a *trigger* for persistent mode, not the mode itself. The user's phrase "this is more than a cron" is the tell that you are under-modeling persistence. See `references/spec-runtime-gap-audit.md` and `references/canonical-process-doc-set.md`.
- **Skipping the spec-vs-runtime gap audit.** When the user says "get this fully operational" or "we built this a long time ago," the runtime has almost always drifted from the spec. Build the gap table first (spec says / runtime does, one row per behavior), present it, then phase the revival by dependency. See `references/spec-runtime-gap-audit.md` for the full technique.
- Summarizing away a process the user explicitly asked to see in full.
- Adding speculative steps just to make the doc look more complete.
- Letting the question flow, state machine, overview, and runtime-facing profile drift out of sync.
- Blurring the three advisor categories together after the user has already established a taxonomy.
- Answering from the nearest matching doc set when the user is actually referring to a different engine family (for example, treating a health/self-healing loop as if it were the coaching loop). First verify the artifact family and only then summarize or patch.
- Downgrading narrow specialist advisors just because the lane is narrow; keep them highly credentialed and elite within their focus.
- If the user asks for "credentials" and "public watered-down TWC," do not substitute internal TWC or vague bios. Use a public coach score format with explicit basis and confidence.
- Do not answer a panel request with a name-only roster when the user asked for profiles; each advisor should be presented with a full profile block, at minimum covering role fit, public evidence, what they add, and any caveats.
- For a user-specific panel, the match must be to the user's actual companies/products/goals, not a generic principal roster. If the fit is based on a niche product lane, pick that lane first and then choose the best public figure for it.
- If the user already has a canonical scoring scheme, preserve it exactly. Do not introduce a new rubric or normalization method in the reply.
- If the user says the process is wrong, respond result-first and only explain the process after the panel or answer is presented.
- **Panel cascade wiring**: When the coaching engine has advisory panels feeding into a principal board, wire them as a cascade (research panels → principal synthesis via `context_from`), not flat independent crons. The principal board's value is in synthesizing the research panels' output. See `advisor-panel-orchestration` skill for the full cascade pattern.
- **Activation-mode coverage drift:** operational docs (process-flow, state-machine) define all activation modes, but identity/behavior docs (SOUL, AGENT, README, question-flow) only reference a subset. This is the most common coherence failure. After defining modes in the operational layer, grep every other file for the activation-mode phrasing to confirm coverage.
- **Canonical-name drift:** when the repo owns an engine, use the actual engine name in titles, prose, and runtime wrappers instead of the generic description. Search for generic phrases like `coaching engine`, `algorithm engine`, and `healing engine`, then replace them with `8D Coaching` or `8D Heal AI` as appropriate.
- **Launch-surface drift:** if the user asks to *launch* the coaching agent, do not leave the startup path implicit. Add or verify a single launch checklist / entrypoint file and make the file order explicit.
- Treating background continuation the same as a fresh summon or the same as a handoff resume.
- Asking questions after enough context already exists.
- Dumping advisor notes instead of synthesizing a user-facing answer.
- Updating only memory when the lesson belongs in the skill body.
- Wiring advisory panel crons that produce generic advice instead of consuming actual scoring data. Every cron prompt must load the scoring spec, check for today's scores, and apply the coaching decision tree. A cron that runs without pulling real data is wasting the user's trust.
- Surfacing raw mathematical outputs (Ricci scalars, metric tensors, escape rates) to the user or in advisor briefs. Everything must be translated to plain language before delivery.
- **Recommending "build from scratch" for any scoring, coupling, or dimension algorithm without first searching hydra-os/products/principal-8d-tracker/ and hydra-os/scripts/ for existing implementations.** The complete 8D scoring system (8,400+ lines) already exists. User correction (2026-06-10): "I shouldn't have to point you back to the work."
- **Agent self-improvement cadence must be AI-speed, not human-speed.** Quarterly/annual cycles are too slow. The coaching engine guardian (DS HELM) runs: continuous (real-time scope checks), hourly (micro-batch quality review + drift detection), daily (full effectiveness analysis + research integration), weekly (comprehensive engine review + architecture assessment), monthly (strategic review + methodology benchmark). See DS HELM SOUL.md for full cadence. (2026-06-10)
- **Agent personas must be versioned, not public figure mirrors.** Do not create agents that mirror public figures (Grant, Deci/Ryan, etc.). Instead: build versioned personas with internal credential stacks (PhD-equivalent, board-certified supervisor, 15+ years research synthesis), embedded frameworks (ACRF, RECF, TFACF, GAF, SMIF, CEC), and explicit versioning protocol (Major/Minor/Patch). Each version is a complete, self-contained artifact supporting A/B testing and atomic rollback. (2026-06-10)
- **The coaching engine has FOUR modes, not two or three.** Every coaching interaction operates in exactly one mode: (1) One-Off — single question, strategic advice, no commitment; (2) Goal-Oriented — user sets a goal ("better sleep," "better swimmer"), engine builds plan, tracks progress, adapts using space-time geometry + PIML to predict and guide behavior; (3) Situational Threads — persistent thread for a specific case (legal, medical, divorce, workplace), preserves context/timeline, on-demand activation or scheduled cadence (e.g., weekly), archives when resolved; (4) Advisory Panels — persistent panel for long-term transformation, named seats, scheduled reviews, task tracking, cross-panel awareness. Space-time geometry + PIML algorithms are the through-line underneath all four modes. (2026-06-10)
- **Document versioning convention:** All deliverables use format `{DOC_TYPE}_v{MAJOR}.{MINOR}_{YYYY-MM-DD}T{HHMM}.pdf` (e.g., `THESIS_v1.0_2026-06-10T1145.pdf`, `CEO_BRIEF_v1.0_2026-06-10T0600.pdf`, `BOARD_BRIEF_MARKETING_v1.0_2026-06-10T1000.pdf`). Doc types: THESIS, CEO_BRIEF, BOARD_BRIEF_{BOARD}, CHECKLIST, REVIEW, SCORECARD, PROTOCOL, SPEC, TALENT, MEMORY. Major = fundamental restructure; Minor = updates within scope; Patch = typo fixes only. Every cron-produced deliverable MUST include versioned filename. (2026-06-10)

## Coherence-audit technique

When checking a multi-file coaching-engine doc set for internal consistency, use this approach:
1. Read ALL files (spec docs + runtime wrappers) in parallel.
2. Delegate a cross-document coherence check to a subagent, giving it the full file set and asking it to verify: naming consistency, definition completeness, activation-mode coverage, scoring conventions, required-reads alignment, truth-policy coverage, and cross-reference validity.
3. The subagent should report exact file + line numbers for every mismatch.
4. Apply targeted patches to the affected files, then verify each patch.

This catches drift that a single-file review would miss, especially when one doc defines a concept (e.g., 3 activation modes) but other docs only reference a subset (e.g., 2 modes).

## Verification steps

Before finishing, confirm that:
- the full flow is represented from activation to handoff
- all three activation modes (fresh summon, background continuation, resumed after handoff) appear in EVERY doc that references activation behavior, not just the operational docs
- the question sequence is explicit
- the state transitions are explicit
- the docs do not contradict each other
- canonical phrasing (activation mode names, advisor category names, credential definitions) is word-for-word identical across all files
- the user’s established terminology and preferences are preserved
- every recommended advisor includes a full profile block, not just a name, when the user asked for advisor profiles

## Expert Research Agent Companion Pattern

When adding a new advisory board seat for a living expert (e.g., a researcher, author, or public figure), consider spinning up a **companion expert research agent** alongside the advisor profile. This agent continuously studies the expert's work and translates findings into engine-relevant recommendations.

### When to create a companion agent
- The expert is a living person with actively published research (not a historical figure)
- Their work directly informs engine parameters or product features
- The board needs current, evidence-rated summaries of their latest findings

### Agent creation workflow
1. **Create advisor profile** — Follow the standard advisor profile format (see existing coaches/*.md). Verify credentials accurately. State degree types precisely (DC vs MD vs PhD).
2. **Update COACHING_CONTEXT.md** — Add the new seat to the Board Seats list and Key Outputs section.
3. **Create expert agent spec** — Define codename, purpose, evidence rating system, operating rules, integration points, and model configuration. Use non-Anthropic models per HARD RULE.
4. **Set up weekly research cron** — Monday morning scan for new publications, replications, critiques. Configure with `enabled_toolsets: ["web", "search"]`, appropriate model (LLM-5.2 or Nemotron), and `deliver: origin` to the user's chat. Use `[SILENT]` pattern when nothing new is found.
5. **Define evidence rating system** — A (peer-reviewed, ready for calibration) through D (theoretical, conceptual only). This prevents over-reliance on pre-publication or observational data.

### Credential accuracy pitfall
When creating advisor profiles for experts with non-traditional credentials:
- State the actual degree (e.g., Doctor of Chiropractic = DC, not MD or PhD)
- Distinguish between peer-reviewed publications and retreat-based observational data
- Note university collaborations as "research partner" or "collaboration" unless a formal affiliation is verifiable
- Include a credential verification section with verified vs uncertain items
- Score against the board's credential rubric transparently

### Example: Dispenza integration (2026-06-16)
- Seat 6 added to Research Advisory Board: Consciousness & Neurophysics Research
- Companion agent DS-NEUROQUANT with 4-tier evidence rating (A-D)
- Weekly Monday 6AM CT cron on LLM-5.2
- Integration mapped: brain wave data → Wave Engine, HRV coherence → Allostasis, neuroplasticity rates → PIML bounds
- Credential stated as DC from Life University, not MD/PhD

## Scoring-algorithm integration

When the user asks to wire a scoring algorithm (GAS v2.0, TWC, or similar) into the coaching engine, use the pattern in `references/gas-scoring-coaching-integration.md`. This covers:
- Baseline establishment (14-day calibration, zero human ratings, state vector construction)
- Scoring cadence (daily/weekly/monthly) and what each tier computes
- Coaching decision tree (rules-first: classify regime, select focus, generate action, calibrate tone)
- How advisors consume interpreted outputs (never raw math)
- Cron prompt wiring (each prompt must load the spec, check for scores, apply the decision tree)
- DB schema for daily and per-goal scores
- Edge cases (missed days, mid-day regime changes, everything-stuck states)

Key principle: advisors see regime labels, breakthrough probabilities in plain language, and leverage directions. They never see Ricci scalars, metric tensors, or convergence parameters.

## Support files

- `references/ds-wave-product-panel-intake.md`
- `references/sibling-panel-layout.md`
- `references/panel-output-format.md`
- `references/artifact-family-disambiguation.md`
- `references/warm-question-tone.md`
- `references/gas-scoring-coaching-integration.md`
- `references/advisor-taxonomy-runtime-wrapper.md`
- `references/process-flow-guardrails.md`
- `references/launch-surface-entrypoint.md`
- `references/ai-speed-cadre.md`
- `references/voice-workflow-separation.md`
- `references/personal-coach-panel-taxonomy.md`
- `references/rolling-mirror-helper.md`
- `references/canonical-engine-naming.md`
- `references/biohacking-marketing-advisor-selection.md`
- `references/four-coaching-modes.md`
- `references/piml-product-moat.md`
- `references/document-versioning-convention.md`
- `references/canonical-process-doc-set.md` *(added 2026-07-19)*
- `references/spec-runtime-gap-audit.md` *(added 2026-07-19)*
- `references/ten-step-fork-architecture.md` *(added 2026-07-19)* — The 10-step flow is NOT linear. Three forks (confidence gate / single-vs-panel / session fate) are force multipliers; two feedback loops (confidence re-check / monitoring re-entry) govern iteration. Use this map to phase revivals: each fork's value depends on the infrastructure underneath it.
- `references/psychology-frameworks-gap-analysis.md` *(added 2026-07-21)* — Elite psychology panel gap analysis (Kahneman, Bandura, Dweck + Popper adversarial review). Contains the 9 systemic gaps all coaching engines share, 12 research-backed recommendations, the Wave Engine v2 11-step pipeline architecture (Purpose Lock through Dopamine Milestones), tiered implementation priority, Popper falsifiability critiques, and a full citation bank. Consult when designing or upgrading any coaching engine's psychological diagnosis layer. **Note:** The v2.0 11-step pipeline documented here was revised through Rounds 2-3 of the Mastermind Protocol. See `references/v2.1-converged-architecture.md` for the final branched pipeline with component status changes (Purpose Lock removed, Friction Score replaced, Dopamine Milestones re-grounded, PERMA gated, Two-Layer Output added).
- `references/v2.1-converged-architecture.md` *(added 2026-07-21)* — Final v2.1 converged architecture after 3-round Mastermind Protocol (panel + Popper adversarial review). Documents the branched Fast/Deep pipeline replacing the linear 11-step flow, all 12 active components with SETTLED/PROVISIONAL status and framework classifications, what changed from v2.0 and why (Purpose Lock removed, Synergy relabelled to Multi-Perspective Composition, Dopamine Milestones re-grounded in FR operant conditioning, Friction Score replaced with SRHI-derived Habit Automaticity Assessment, PERMA gated to personal_growth, Two-Layer Output Model added), full implementation spec details (function signatures, output structures), and the key citations added in Rounds 2-3. Consult when implementing the coaching engine's psychology layer or conducting similar multi-round architecture review panels.
- `references/v2.1-diagnostic-stack-build.md` *(added 2026-07-21)* — The actual code implementation of the v2.1 stack: module structure (`src/wave_coaching/v2/` subpackage with 11 modules), the pipeline integration pattern (wraps v1, does not break it), complexity-gate routing signals (depth cues and distress signals force Deep Path), the two-layer output model with banned-jargon list, framework classification tags, the diagnostic module shape, and the end-to-end testing pattern. Consult when implementing a similar science-grounded diagnostic layer on any coaching/advisory engine.
- `references/multi-round-adversarial-convergence.md` *(added 2026-07-23)* — Reusable workflow for any architecture/methodology review that needs to survive falsifiability scrutiny. The SETTLED / PROVISIONAL / OPEN / REMOVED component-status framework, the 3-round convergence loop, Path C parallel build strategy (Round 3 in background while SETTLED components go into code in foreground), falsification-criteria requirements for PROVISIONAL components, verification discipline, and the worked Wave Engine v2.1 example. Consult when designing any elite-panel architecture review with an adversarial reviewer seat.
- `references/wave-engine-v2-mastermind-example.md` *(added 2026-07-23)* — End-to-end worked example of the 3-round adversarial convergence on the Wave Engine v2.1 (panel + Popper). Round 1 gap analysis → Round 2 revisions addressing 5 critiques → Round 3 open-item resolution with 1 REMOVED, 1 SETTLED, 2 PROVISIONAL. Includes Path C parallelization strategy, the 12-component final architecture, integration handoff to sibling-agent via operator bus, and 6 reusable lessons (SETTLED/PROVISIONAL vocabulary, falsification criteria at build time, practitioner-frameworks-labeled-not-banned, two-layer output as demand-characteristics fix, FR-not-VR for ethical progress checkpoints, Path C free-energy optimization).
- `references/v2.2-diagnostics-first-pipeline.md` *(added 2026-07-23)* — The architectural pattern for coaching engines where diagnostics actually shape LLM output, not decorate it. Documents the E16 master defect (diagnostics computed but never injected into generation), the v2.1→v2.2 flip (diagnostics-first pipeline), the function-signature smell (`run_v2_pipeline(coaching_guidance=...)` encodes the bug), the MAP gate revision loop, session state persistence, the verification protocol (does each diagnostic reach the LLM prompt or just the science_trace?), and the 34-error audit catalog from the 2026-07-23 self-audit. Consult BEFORE claiming any diagnostic-layer build is complete.

## Runtime Coaching API (the specialist engine /v1/coach — built 2026-07-15)

The coaching engine now has a **live HTTP endpoint** on the specialist engine (port 8010):
`POST /v1/coach`. This is the runtime implementation of the coaching spec.

**What it does:**
- Takes any user input (text) + organism context (b2c/b2b/b2bu)
- Classifies the situation into 9 types (product_idea, business_strategy,
  advisory_panel, professional_advice, creative_project, personal_growth,
  technical_problem, team_management, everyday_task)
- Enforces hard boundaries (refuses harmful/illegal requests) and soft
  boundaries (adds medical/legal/financial disclaimers)
- Returns structured guidance: greeting, situation understanding, step-by-step
  path with engine assignments, clarifying questions, recommended advisory
  panels, recommended pipeline
- Includes Kuramoto coherence reading for organism state reference

**Frontend integration:** The Work Board's "Coach Me" button calls this
endpoint and renders a full coaching panel with context selector, step path,
questions, and action buttons (Create Work Order, Break Into Steps, Assemble
Panel, Continue Talking). Work orders created from coaching carry a
`coachContext` object with situation type, approach, steps, and panel
recommendations.

**Phase 2 UPDATE (2026-07-17):** The coaching endpoint now accepts two additional
optional parameters on `CoachRequest`:
- `model: Optional[str]` — overrides the config default model (e.g., "glm-4.7").
  If omitted, uses `config.yaml` `model.default` (glm-5.2).
- `voice: Optional[str]` — injects a voice-layer instruction into the system prompt.
  The voice acts as a translation membrane: it changes HOW the coaching is
  delivered (tone, rhythm, vocabulary) but does NOT change the substance.
  All 50 persona voices are available (Sage, Jobs, Rosie, Gandalf, etc.).

The full chain: `coach()` → `generate_coaching_guidance(model_override, voice)` →
`generate_llm_coaching(model_override, voice)`. The LLM call uses the overridden
model, and the system prompt gains a voice instruction appended to
`COACHING_SYSTEM_PROMPT`.

**Known gaps (found in self-audit 2026-07-15, MUST be fixed in remaining phases):**
- `conversation_history` parameter is accepted by the endpoint and passed to
  `generate_coaching_guidance()` but is NEVER USED in the guidance logic.
  Multi-turn coaching gives identical responses regardless of history.
- Hard refusal patterns are missing: general violence, illegal drug
  distribution, weapons manufacturing. Only hacking, malware, self-harm,
  and bomb-making are covered.
- Coaching does NOT adapt to user profile (archetype, goals, 8D scores).
  Every user gets identical coaching steps regardless of who they are.
- Templates don't auto-trigger coaching. User picks a template into the
  dispatch input, then must manually click "Coach Me" separately.

**v2.1 SCIENCE STACK INTEGRATION (2026-07-23):** Opencode integrated the
v2.1 diagnostic stack into the live API. Both the LLM path and the template
fallback path now wrap their output through `run_v2_pipeline()`, producing
the two-layer output structure (coaching_response + science_trace).

Live `POST :port/v1/coach` response now contains:
- `v2_enriched: true` — confirms v2.1 pipeline ran
- `path: "fast" | "deep"` — complexity gate routing
- `coaching_response` — clean user-facing Layer 1 (no jargon labels)
- `science_trace` — gated Layer 2 with frameworks_active, diagnostics,
  citations, visible_to_user=false
- `complexity_score`, `complexity_reason` — why the gate routed this way

Integration pattern (surgical, ~13 lines in api.py): `run_v2_pipeline()`
ACCEPTS v1 output and enriches it. Backward compatible — if v2 modules
fail, v1 output still returns. See `references/v2.1-diagnostic-stack-build.md`
for the module layout and integration contract.

**Updated status of the 2026-07-15 known gaps:**
- `conversation_history` — STILL UNUSED in v2.1 (multi-turn identity issue
  persists; not addressed by the science stack). P1 next.
- Hard refusal patterns — STILL MISSING general violence, drug distribution,
  weapons manufacturing. Add before any public launch.
- Profile adaptation — PARTIALLY ADDRESSED by v2.1: the complexity gate,
  motivation diagnosis, and efficacy calibration all read user signals
  and adapt the output. Full archetype/8D-score adaptation is still future
  work.
- Template auto-trigger — STILL UNCHANGED.

**See also:** `organism-service-development` →
`references/engine-endpoint-extension-pattern.md` for the backend pattern
(CORS, module structure, endpoint definition) used to build this.
