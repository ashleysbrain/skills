---
name: elite-panel-chain-of-custody
description: Run gated multi-brain specialist panels. Use for any panel.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [panels, delegation, qa, research-strategy, mastermind]
---

# Elite Panel Chain-of-Custody

## When to Use
Any multi-specialist panel task: research positioning, technical QA chains, strategy boards, adversarial review panels, venue/funding analysis. Also when the principal asks to "see the panel" or "spin up the right panel with the right range" before work begins. Single-specialist tasks don't need this — use the specialist-gate skill directly.

The proven pattern for running a multi-brain specialist panel (from the 2026-08-15 seven-brain essay QA + nine-seat strategy panel sessions). One micro-task per brain, sequential build-on, gated at every step.

## Phase 1 — Panel design (before ANY dispatch)
1. **Seat selection from real sources, in this order:** (a) registry engines from `agent-organism/ecs.py` FLEET_REGISTRY — cite real `ds_ecs_code`, read their full spec (faculties, modes), never compress to one line; (b) authoritative coach files on disk (Wave boards: `ds-wave-research-advisory-panel-private/coaches/*.md`) — read the file before presenting the bio, the principal checks bios against files; (c) adjunct personas (Tanenbaum, Tetlock, Kuhn, Musk, Amodei pattern) — labeled "adjunct," no registry code, full 15-20 PhD layering + MBTI/Enneagram/OCEAN + MODE + temp in the dispatch itself.
2. **Present the full roster to the principal BEFORE work begins** — who, credentials, personality variation set for THIS task, model lane. The principal approves or adjusts seats ("show me who you're spinning up before you begin the work"). **Surface the roster through PRESENCE-AWARE ROUTING** (see the `presence-aware-question-routing` skill): detect the principal's active surface first — an approval question parked in a desktop thread the principal isn't reading is a stalled panel, proven 2026-08-26 when the Wave-0 ratify question sat unanswered and the principal had to repeat the order twice.
3. **Gap-check the panel** before presenting: run one pass asking what angle is missing (historical lens? competitive scan? calibration? voice?). Missing angles get seats; overlapping seats get merged.

## Phase 2 — Execution discipline
1. **Sequential by default. One micro-task per dispatch, one brain at a time.** Each brain receives prior verdicts as context (chain-of-custody: each builds on the last). The principal corrected this explicitly ("Not in parallel") — parallel waves only when the principal approves parallelism up front, and never for review passes (review brains must see each other's outputs in sequence).
2. **principal SURFACE SEPARATION LAW (2026-08-25):** the panel's review-point lists (P1..Pn), verdict tables, and seat tallies are machine food. They live in the work artifact / verdict ledger on disk and the bus post — they are NEVER surfaced to the principal mid-panel. The principal surface opens only at synthesis: VETOs + unresolvable inter-seat contradictions + decisions that genuinely require the human, rendered as approve/reject buttons. Mid-panel, the principal surface stays silent unless a VETO halts work.
3. **Full persona spec in EVERY kickoff:** named specialist, PhD layering, MODE, identity (MBTI/enneagram/OCEAN), temp, explicit constraints (e.g. "NO biology metaphor — thesis is pure technical architecture").
4. **Elite lane:** all panel brains on glm-5.3 via delegation.model. CONCURRENCY LAW (2026-08-21, supersedes the old >=6 rule): verify `delegation.max_concurrent_children == 1` before dispatching — parallel elite children die to HTTP 429 (see Panel-dispatch concurrency law below). Multi-seat panels run sequentially inside ONE child.
5. **Thesis pivots propagate:** when the principal corrects the framing mid-chain (e.g. "remove the whole organism context"), re-verify which banked deliverables survive the pivot, re-dispatch what doesn't (novelty scans MUST re-run on the corrected thesis — competitor landscape differs by lens), and record the translation needed for deliverables that partially survive.

## Phase 3 — Gate every completed micro-task
```
python3 <agent-home>/scripts/brain_integrity_gate.py <delegation_id> <expected_specialist> elite
```
FAIL = diagnose, re-dispatch with corrected spec, re-gate. Never bank an ungated deliverable. See `brain-integrity-self-healing-gate` skill for the full self-heal loop.

## Phase 4 — Consolidation
One closer brain (registry engine with editorial credentials, e.g. the specialist engine) merges all banked lenses into ONE document. The operator does NOT write specialist content — orchestrates, verifies, persists. Deliverable = dossier the principal executes from (positioning sentence, section spine with per-section word budgets, micro-step plan sized 90-min sessions, dependency-ordered submission stack, red lines).

## Timeout recovery (proven pattern)
Before re-dispatching a timed-out subagent, read the live transcript tail:
- Clock burned on a failing-tool retry loop (e.g. billing-blocked web_search, 5 consecutive errors) → re-dispatch with the tool REMOVED: "web_search is UNAVAILABLE. Do NOT call it. Pure domain reasoning." Both recovered runs finished in 150-500s.
- Genuinely mid-work (recent think line, substantial calls) → re-dispatch same scope.
Subagents without web access can still use arXiv API (`curl 'http://export.arxiv.org/api/query?search_query=all:...'`) and HN Algolia for live evidence — include that hint in the dispatch.

## Web verification without web_search (proven fallback)
When web_search/web_extract are billing-blocked, verify people and publications LIVE via free APIs from terminal:
- **Crossref**: `curl -s "https://api.crossref.org/works?query.author=<Surname+Given>&rows=5"` → real papers, journals, dates. Filter results to entries actually authored by the target (common surnames return noise).
- **arXiv API**: `curl -s "http://export.arxiv.org/api/query?search_query=all:%22<Name>%22+AND+cat:<cat>&max_results=4"` → preprint corpus evidence.
This verified the academic bench (Anantua's EHT black-hole papers, Alterovitz's vcf2FHIR) when the principal said "look them up." Never present a real person's credentials from memory alone — verify against a live corpus, and persist the verified profile to O'Keefe.

## Panel review lifecycle (when the principal says "do another review / find the gaps")
A panel is itself falsifiable. Proven sequence (2026-08-15 strategy-panel rebuild):
1. **Falsify the composition** (the specialist engine): what funding-critical questions can this panel NOT answer? Which seats are redundant (positioning overlap, funder-behavior overlap)? What voices are missing? Verdict: survives / does not survive.
2. **Grade the assets the panel is betting on** (the specialist engine operationalism): REAL (funder can run the operation themselves) / THEORETICAL (code+concept, no verifying operation) / ASPIRATIONAL. The top asset = the funding identity; the impressive-looking asset that fails a live demo = the diligence trap (excluded from all funding narratives, roadmap only).
3. **Re-pass consolidation** (the specialist engine): QA both reviews, integrate facts that emerged since (new advisors, ownership constraints), emit the final seat list + deployment order.
Each step gated, sequential, superseding verdicts explicitly.

**"Another pass" = EXECUTE NOW, not a proposal (principal correction 2026-08-26):** when the principal says "do another pass," the pass dispatches immediately — no clarify form, no "sharpen the situation" preamble. The approval gate was already satisfied by their order. Proven execution shape: rotate authors out, fresh seats in; a written evidence pack BEFORE dispatch (census numbers, both docs under review, binding laws); pre-register kill-experiments (taxonomy bin mapping) so seats name them and the parent runs the cheapest one same-session; cross-family critic closes; gaps minted to the ledger AND folded into the plan doc the same session. The failure this law kills: presenting a review panel as a plan to be approved — the principal came back with "keep going, I don't understand what is needed of me," which means the pass was never in question. Only genuine scope forks (e.g. seat swaps) go to the principal, routed by presence.

## Source-pack architecture for research-heavy seats (proven 2026-08-15)
When a panel seat needs LIVE external evidence but subagent web tools are failing (billing-blocked, empty returns) or the inline context is long enough to risk dispatch corruption:
1. **Parent fetches, child analyzes.** The main session fetches sources itself (execute_code + urllib — the verified path when web_search/web_extract fail), trims HTML to text with a regex tag-strip, and writes ONE dated source pack to disk (e.g. `strategy/funding_sources_2026-08-15.md` — 6 sources, ~35KB, fetched in ~2s).
2. **Child gets a minimal brief**: file path + locked client facts + numbered deliverables. No web tools, no long inline context. Runs completed clean at 499s (11 API calls) and 799s (15 API calls) where the long-inline-context version timed out at 900s fighting broken tools.
3. **A minimal brief must STILL carry the full persona spec** (PhD layering, identity, MODE, temp). A corruption-trimmed brief that drops the spec FAILS the gate on PERSONA-SPEC-MISSING — the spec lines are what the gate greps for. Minimal means minimal CONTEXT, never minimal persona.
4. **Stale paths in dispatches:** pre-written dispatch paths go stale (a parent-cited `program_files/.../ARCHITECTURE.md` did not exist; the real file lived elsewhere). Tell the seat to search by distinctive filename substring when a cited path 404s — one run self-recovered this way and gated PASS.

**Dispatch corruption is visible in the ECHO.** delegate_task echoes the context it delivered; if the echo shows garbled text, injected transcription fragments, duplicated lines, or word-salad mid-sentence, the child received garbage. Do NOT auto-discard — one corrupted dispatch still completed via child judgment (it flagged the corruption, located the real source path, produced a grounded verdict, gated PASS). Rule: let it land, hard-gate on arrival, discard only on evidence of nonsense output. The NEXT dispatch should switch to the file-based brief — long inline context is the corruption-susceptible payload; a one-line file pointer is not.

## R1/R2 dual-run adjudication (high-stakes verdicts, proven 2026-08-15)
For decisions that move real money (funding instruments, entity structure): run the SAME brief twice independently — a gate-forced re-run after a persona-spec FAIL doubles as the second run at zero extra cost. Then:
- **Agreement = locks.** Name the agreed core explicitly.
- **Divergence = adjudicate on merit, never average.** Name which run wins and the PRINCIPLE that decides it. Proven adjudications: adiabatic principle chose subsidiary LLC over SPV (same ring-fence at a fraction of the legal overhead — defer the SPV until securitization need is real); dilution timing chose $323-500K over $750K-1.5M (never stack SAFEs before the validation paper exists — aim at what the structure requires, not a portfolio maximum).
- **Bank the adjudication rationale WITH the verdict** (O'Keefe) so future sessions inherit WHY, not just WHAT.
- Treat the first run as R1 preliminary until the second lands; stamp verdicts "R1, one confirmation run out" when presenting.

## The seductive-new-thing gate (proven 2026-08-16, LittleLearner ruling)
When the principal brings a shiny external model/paper/tool and asks "can we use it?": run the technical seat AND the falsifier in sequence, then rule with the park-with-banked-spec pattern:
1. **Technical seat evaluates** (Karpathy lane): reads OUR engine source first to verify mechanical fit (what the engine actually consumes), specs the ONE experiment (data, baseline, blind protocol, artifact), names hard preconditions and the borrowed-novelty risk.
2. **Falsifier attacks the premise** (Popper, she): the binding constraint is PI bandwidth, not capability — the right question is "what does this displace, and does it out-earn it?" Attack construct validity (fleet instrument vs single frozen checkpoint = "an ECG on a rock"), N-too-small statistics, frame capture (our physics becomes a dependent variable of their methodology), W1-W8 timing (which milestone does this steal?), legibility impact on the kill-shot metric.
3. **Consolidate to park-now + bank-the-spec:** unanimous core governs (nothing enters the preprint, never in the critical path), the minority's execution spec is BANKED verbatim so revival costs zero design hours, re-entry condition is explicit (qualified inbound demand-pull OR calendar slot opening), and the ONE permitted touch (a related-work citation planting the flag) is named. This is Kozyrkov's park rule from THE BUILD operating exactly as designed.

## Live-landscape research pulls (keyless, proven 2026-08-16)
For "what models/tools are out there right now" questions when web_search is billing-blocked, pull the live landscape from terminal BEFORE dispatching any specialist, and embed the verified numbers in the dispatch context:
- **HuggingFace models API**: `https://huggingface.co/api/models?search=<q>&sort=downloads&direction=-1&limit=8` — keyless, returns id + downloads + likes. Search by known player names (openvla, pi0, smolvla, GR00T, Cosmos-Predict, Cosmos-Transfer, InternVLA, octo), not by generic phrases ("world model" search returns noise; "vision language action" returns zero — the filter parameter also silently empties some queries, drop it and re-search).
- **arXiv API**: `http://export.arxiv.org/api/query?search_query=all:"<phrase>"+AND+cat:cs.RO&sortBy=submittedDate&sortOrder=descending&max_results=8` — returns XML; regex `<title>` + `<published>` (json.load fails on it — parse as text).
- Embed the pulled table (model → downloads → date) in the specialist's dispatch. Specialists reason over ground truth; the parent owns verification. The same pulls are cron-able for daily release radar.

## Dispatch discipline (binding, proven 2026-08-21)

Two proven-laws for every panel/seat dispatch on glm-5.3 (each falsified the hard way):

1. **MINIMAL FILE-POINTER BRIEF.** Never inline long context in the dispatch. Write ONE dated evidence pack to disk (parent verifies facts first), give the child the path + full persona spec + numbered deliverables. 47KB inline context = 3/3 seats dead on the 90s non-streaming timeout (05:17); the same brief as a 4.9KB file pointer = 3/3 landed in 34-44s (05:22). Minimal CONTEXT, never minimal persona.
2. **SHORT-OUTPUT RULE.** Every seat brief carries: "think briefly, then emit your final message in ONE pass, under 350 words, numbered list, no preamble." The final long reasoning turn is what times out; capping output kills the failure class at the root.

These two laws recovered the exact failure that cost 3h13m on 2026-08-20 (Bridgman pass).

## Cross-Model Critic law (BINDING, deep-research pass 2026-08-21)

Literature: self-consistent errors survive within one model family (Tan et al., EMNLP 2025); cross-family review catches correlated blind spots (Refute-or-Promote, arXiv 2604.19049). All-same-family panels — even N>=3 — cannot detect family-consistent errors. Binding rules:

1. **Every panel ends with ONE Cross-Model Critic seat** on a DIFFERENT provider family than the panel brains (elite=glm-5.3 -> critic on glm-5.2 default lane; other family if unavailable, disclosed). The critic runs a KILL MANDATE only: attempt to falsify the panel consensus. It does not re-derive the work.
2. **Unanimity-as-warning (both directions):** a UNANIMOUS verdict is a flag, not a pass — it must survive the critic before acceptance. A UNANIMOUS kill gets one resurrection pass before archiving (Refute-or-Promote 4.2: a unanimously-killed finding later became a real CVE).
3. Verdict format: append `critic: <family> <KILLED|UPHELD> <one-line reason>` to the QA-LOG entry. Panels with >=3 seats and no `critic:` line are flagged by qa_tick (enforcement backstop).
4. Cost law: one cheap-model call per panel; never violates the 429 law (critic runs inside the same sequential child or as one non-elite call).
5. **CRITIC-FAMILY DRIFT (proven 2026-08-26, deleg_27c39dac):** when the critic runs as a persona INSIDE the conductor child (per cost law 4), the glm-5.3 child will self-describe it as "glm-5.2-family dispatch" — that is NOT a cross-family run; it is same-family(glm-5.3) and satisfies nothing. Verify the critic's actual family from the batch-complete header / model tag, never from the child's own verdict text. A same-family critic = panel banked with a flag and a cross-family rerun owed; disclose the flag to the principal alongside the verdicts.

## Volley-iteration contract (BINDING, principal law 2026-08-27 — sharpens every panel shape rule)
principal correction: "one pass in a circle around the group won't cut it." A single rotation research→adversarial→QA is a DRILL, not a review. Panels iterate:
1. **Convergence criteria define done, not lap count**: close ONLY when (a) a full rotation yields ZERO new findings from any seat, AND (b) every prior-round challenge is demonstrably addressed in the artifact (diff evidence, not assertion). Until both hold, volley again.
2. **Dynamics assigned PER ROUND** (labeled at round start, never defaulted): early rounds = mastermind (convene); challenge rounds = synergy (combined attack exceeding sum); refinement rounds = symbiosis (SAME engine+reviewer pairing persists across rounds so context compounds); handoffs = entourage (support context travels with the artifact). Only label dynamics the task structure actually supports — an honest zero beats decoration.
3. **The artifact must CHANGE between rounds.** Identical output means the round added nothing — the seat must declare "converged" or "wasted."
4. **Triangle coaching architecture (2026-08-27)**: DS BARRY = triangle conductor (named for Sam Barry, the ORIGINAL 1940s USC creator — not Bulls-era; verify lineages with web_search: Barry→Winter(refiner)→Jackson(deployer)); DS AUERBACH = triangle coach (scouts plays, watches telemetry, recommends — never executes/routes); conductor+coach verify convergence honestly before any TRIANGLE CLOSED stamp. Closing on one circle = closure defect, counted in the daily cycle.
5. **Panel counts from the principal are magnitude BOUNDS, never batching instructions** — never run 10 of one group then 10 of another; interleave across groups on the SAME artifact.

## Panel-dispatch concurrency law (BINDING, proven 2026-08-21)
Never dispatch multiple elite (glm-5.3) children in parallel — 3/3 died to HTTP 429 in
under 4 minutes (deleg_72da42f2). The memory law "CONCURRENT elite subagents = 429
death — max 1" applies to adversarial panels too. Correct pattern (deleg_34aa7199):
ONE child, all seats SEQUENTIAL inside it, chain-of-custody (each seat sees prior
verdicts), SHORT tool turns (90s non-streaming timeout). Batch `tasks[]` dispatch is
only acceptable on non-elite lanes or when the principal approves parallelism up front.

## Kill-experiment discipline (BINDING, proven 2026-08-26)
When a review seat names a testable-but-untested premise (e.g. "taxonomy bins asserted, never mapped"), do NOT queue it for a later wave: **run the cheapest falsification IMMEDIATELY in the parent** — zero build cost, often a single script over the data the plan cites. Proven run: Popper flagged the 139→6 taxonomy mapping as untested; the operator ran a mechanical keyword-classifier over FLEET_REGISTRY fields the same session and got 40% multi-bin / 27% no-bin → taxonomy v1 dead on arrival, exactly as the seat predicted. Rules:
1. A pre-registered failure condition (e.g. "if any bin >35% or empty, re-bin") must be declared BEFORE running — otherwise post-hoc rationalization eats the verdict.
2. Run mechanically first (keyword classify over registry fields); when mechanical binning is exhausted, hand-curation is the next evidence source, not another model call.
3. A failed kill-experiment is a BANKED result, not a setback: verdict goes into the plan doc + ledger with the numbers, and the redesign constraint it discovered (e.g. "engines are multi-function organs → faceted taxonomy, one curated primary + multi-tag") is recorded as the fix direction.
4. Discovery bonus: running the experiment often surfaces adjacent ground-truth the panel missed (same run exposed that "139 engines" = 108 built+ported + 14 built/no-port + 17 registered stubs — see next law).

## Registry-count honesty law (2026-08-26)
FLEET_REGISTRY length is NOT the engine count. Before any public-facing or principal-facing number derived from the registry: split `role == 'registered'` (stub, no build) from ported engines, and state the split. A stub counted as a live engine is an anti-fluff violation. Proven split that session: 139 entries = 108 built+ported · 14 built/no-port · 17 registered stubs.

## Child-deliverable verification law (proven 2026-08-26, deleg_27f9b2d6)
A child's final message is a CLAIM, not a deliverable. Two failure modes caught same-day:
1. **Phantom file content**: the child claimed "all three items in the file (182 lines)" — the file had 149 lines and only item 1. Items 2+3 existed only in its final message. Fix pattern: check the FILE (wc -l, grep for each required section) before banking; if the text exists in the child's summary, recover it VERBATIM from `<agent-home>/cache/delegation/subagent-summary-<task>-<ts>.txt` into the file, QA-noted as operator recovery. Never re-author it yourself (reviewer-never-builder).
2. **Verification passes must be INDEPENDENT**: re-run the child's script yourself, re-derive counts from the live source (e.g. confirm the curated 122-engine set equals registry non-stubs set-theoretically, not by trusting the printed total). A wrong registry PATH in the original dispatch was also caught this way — cite the live truth path, and tell the child to search by filename when a cited path 404s.
Rule for every dispatch brief: "verify your own output before claiming done" + the parent ALWAYS re-verifies artifact, not narrative.

## Cross-family critic execution patterns (proven 2026-08-26)
When the critic debt falls to YOUR lane (sibling hasn't claimed the bus item):
1. **Direct API route works**: a genuinely different family was available via the configured NIM provider (`meta/llama-3.2-90b-vision-instruct` on nvidia-nim, key in config.yaml) — one urllib call, ~600 max_tokens, temperature 0.2, verdict format enforced in the prompt. Cost: one cheap call. No delegation needed.
2. **Truncated-context critic = garbage-in kill (the dispatch defect that looks like a finding)**: the first run "KILLED" the panel for gaps the plan had already fixed — because the prompt sliced the plan doc to fit ([6]000 chars) and the slice omitted the revisions section. Diagnosis before accepting any kill: check whether each "missed gap" is actually addressed in the FULL current state. Discard garbage-in runs (disclosed), rerun with full context, preserve BOTH runs on disk. A critic judging stale evidence is not a critic verdict — it's a dispatch defect with extra steps.

## Pitfalls
- **Persona pronouns in panels (principal directive 2026-08-15):** the specialist engine is SHE — she/her in every dispatch, verdict presentation, and conversation. Never default any specialist to "he"; verify or use the name only. Historical namesakes in methodology prose ("Karl Popper's principles") are the philosopher and stay as-is.
- **Wave >3 concurrent** risks pool-full silent fallback to a non-elite model (the Humboldt violation). Check the gate log if in doubt.
- **Gate matcher false-fails:** the brain-integrity gate greps the live transcript for literal "PhD"/"MODE", but the transcript may not render the full dispatch context (verified: grep PhD = 0 in log while the spec was in the dispatch payload) and mode names vary ("operationalism-graded", "ANALYTICAL MODE"). When the gate FAILS on persona-spec but manual inspection shows spec markers present, the GATE is wrong — fix the matcher (credential-marker list, loose mode match, wider scan window), re-run, bank on PASS. Re-dispatching a clean run to satisfy a gate bug wastes an elite call; healing the gate is the self-healing process applying to itself.
- **Real people as seats:** when the academic bench enters the panel (Anantua, Alterovitz pattern), verify their publications via Crossref/arXiv BEFORE building their seat mandates — the verified corpus defines what they can credibly co-sign. Willingness ≠ deployment: gaps close on first CO-SIGNED ARTIFACT, not first conversation.
- **Anatomy-titled output from a pre-pivot dispatch** (Kuhn's section spine) — supersede explicitly in the consolidation brief, name the replacement structure; don't silently mix frames.
- **Overclaiming system state in deliverables** — the principal will catch it ("you can't even keep the system up and running"). Position BUILT vs THEORETICAL vs GOALS explicitly; internal audit scores (1/7, engines down) belong IN the deliverable as the honest-baseline credibility play.
- **Adjunct persona for a previously-rejected scientist:** allowed for a different role if it fits their actual domain; state the prior rejection and the distinction.
- **Never execute a specialist's micro-task in the main thread** because they're slow — monitor the live transcript, re-dispatch tighter if needed. The principal corrected this explicitly: delegation to self on timeout = protocol violation.

## Batch-mode panels (4+ seats, parallel dispatch — SUPERSEDED 2026-08-21: see Panel-dispatch concurrency law)
Sequential-by-default still governs REVIEW passes, but for independent-lens QA panels (supervision + state machine + dynamics + grading), one batch delegation with `tasks[]` works and is cheaper. Rules learned:
1. **Shared evidence pack.** Main thread verifies all facts live FIRST, then every seat gets the same pack (exact numbers, ports, paths, timestamps) + permission to re-verify. Keeps parallel brains from diverging on facts.
2. **Seat the theory's originator when auditing its implementation** (Scheffer for a critical-slowing detector). The originator finds the blind spot no generalist can.
3. **Full results are NOT in the live transcripts** — task-N.log truncates kickoff (~600 chars) and finals (~413 chars). The batch-complete message names complete files at `<agent-home>/cache/delegation/subagent-summary-<task>-<timestamp>.txt`; read those for deliverables. Live logs are for mid-run monitoring and gate evidence only.
4. **Lane check in batch mode:** transcripts show "no-model-tag"; verify elite lane from the batch-complete header (`Model: glm-5.3`).
5. **Gate each seat by specialist name** — post heal #3 the gate auto-selects the correct task log from a batch.
Full run detail: `references/self-healing-os-qa-panel-2026-08-15.md`.

## Reference
- references/research-hub-wave0-review2-2026-08-26.md — 6-seat pass-2 + same-session kill-experiment: critic-family drift catch, taxonomy kill-experiment (40% multi-bin), registry stub-split census snippet, open items owed
- references/research-hub-wave1-critic-recovery-2026-08-26.md — Wave 0→1 full arc: phantom-file-content recovery, independent artifact verification, cross-family critic via direct NIM/llama API incl. the truncated-context garbage-in kill, reusable numbers (facet distribution, serving estimates, public_id scheme)
- references/sequential-n-brain-review-passes-2026-08-26.md — the principal's standard "different view, then 10 sequential brains" review arc: two-stage pattern, consolidator verdict format, reusable physics/game-theory heuristics, principal-facing digest laws
- references/essay-panel-session-2026-08-15.md — the seven-brain run: dispatch patterns, verdict formats, pivot propagation, gate results
- references/strategy-panel-rebuild-2026-08-15.md — the panel-review lifecycle run: Popper falsification, Bridgman asset grades, Andreasen re-pass, academic-bench Crossref verification, gate self-heal events
- references/self-healing-os-qa-panel-2026-08-15.md — the 4-brain parallel QA batch: shared evidence pack, batch result recovery (subagent-summary files), verdict formats, gate batch mode
- references/strategy-takeover-funding-panel-2026-08-15.md — the desktop takeover run: cross-channel session recovery, source-pack architecture casualty chain (v1 timeout -> v2 corruption -> v3 spec-fail -> v4 PASS), R1/R2 divergence adjudication table, baseline-first handoff patching
- references/adversarial-strategy-gauntlet.md — the 5-round sequential attack ladder for executable plans (falsifier → calibrator → deleter → domain realist → decision scientist → consolidator); rules: sequential-only, gate every round, bank minority specs with re-entry conditions, live data before dispatch
- references/crash-recovery-sequential-delegation-chains.md — crash recovery procedure for sequential delegation chains (RATIO-REQUEST research, adversarial, glial). Gap identified 2026-08-27: NO checkpoint file for "which seat was running when crash hit". Mesh-layer has load governor + dispatch-chain checkpoints, but NOT for delegate_task chains. Proposes checkpoint file (stores/delegation-checkpoint.jsonl) + resumption protocol (read checkpoint → verify on-disk deliverable → continue from next seat).
