---
name: evidence-driven-scoring-pipelines
description: Build and debug pipelines that convert textual or structured evidence into complex scoring engines without collapsing into simplistic heuristic scores.
---

# Evidence-Driven Scoring Pipelines

Use this skill when integrating transcripts, check-ins, logs, or other evidence into a real scoring/calculation engine.

## Core rule

Keep *scoring math* separate from *evidence interpretation* and *storage normalization*.

- Evidence interpretation may use heuristics to extract signals.
- The scoring engine must receive the **database-scored/native** calculator inputs, not a hidden weighted-average or 1-10 bridge.
- If storage schema requires bounded legacy fields, clamp only at the persistence boundary and preserve raw values separately.
- Visible 1-10 or 0-100 values may exist only as **presentation after TWC**; they must not become the scientific input layer.
- When describing the model, use the sequence **raw evidence -> database-scored native dimensions -> baseline/confidence/coupling -> TWC -> presentation conversion**.

### Do not reinvent TWC on a fresh organism (Cyber the operator agent 2026-08-02)

Ship healing/user-learning by **vendoring** `calculator.py` into `organism/scoring/` and calling `compute_twc` only. Never invent `burnout_risk` labels without TWC. Preferred check-in path: dim10 estimates → `DimensionScore(score=v/10)` → `compute_twc` (full sub-algorithm dataclasses need exact field scales or TWC collapses). Layers: L0 signals → L1 adapters → L2 owner-only baseline → L3 calculator → L4 healing → L5 OS. Emotional↔Psychological. B2BU = professional 8D; peer data only via fungal network. Details: `references/fresh-organism-layered-8d-learning.md`.

## Workflow

### Adaptive integration and integrity audits

This umbrella also covers narrower variants that focus on baseline-aware adapters, admin exports, or integrity verification. Keep those concerns in the same scoring class unless the domain genuinely needs a separate engine:

- `adaptive-scoring-pipeline-integration` — live adapter + baseline + admin/reporting integration
- `veritas-algo-integrity-check` — periodic integrity audits, drift detection, and self-referential loop checks for the scoring engine

The rule is the same: preserve the real calculator, keep evidence interpretation separate, and verify against the persisted record.


1. **Inspect the real calculator contract first**
   - Identify the true input fields, output object, and any coupling/coherence terms.
   - Do not infer a simpler surrogate model if a complex engine already exists.

2. **Map evidence directly to native inputs**
   - Populate the real dimension fields and sub-fields the calculator expects.
   - Use confidence-aware merging so higher-confidence evidence can override weaker defaults.
   - Preserve raw transcript/evidence signals in metadata for auditability.

3. **Model the product as layered time scales**
   - Keep **experience**, **quest**, and **goal** separate instead of collapsing everything into one generic action score.
   - Experiences are immediate evidence events.
   - Quests are repeatable routines that can adapt by state and context.
   - Goals are longer-horizon outcome targets that update as the user's baseline changes.
   - Reset or seal the daily accumulator at sleep when the domain is biologically tied to wake/sleep; use anchor-sleep logic for irregular schedules.
   - Let confidence rise during the wake session as evidence breadth, recency, reliability, and corroboration accumulate.
   - Treat confidence as certainty/coverage/corroboration, not as a gamified reward meter.

4. **Split shared primitives from domain specs when a product has multiple domains**
   - If the same scoring system serves two domains with different semantics, create:
     - one domain spec per domain
     - one shared primitives doc for the common math, schemas, and persistence rules
   - Keep the domain specs focused on domain meaning, boundaries, source sets, UI language, and acceptance criteria.
   - Keep the shared doc as the single canonical source for formulas, object shapes, threshold mechanics, and replay/audit rules.
   - Remove duplicated formulas from the domain specs once the shared doc exists.
   - Cross-link the three files so readers know where the canonical mechanics live.

5. **Require calculation rules in specs, not just definitions**
   - For any evidence-driven scoring document, definitions alone are not enough.
   - Include the math or explicit pseudocode for coverage, recency, corroboration, source reliability, field delta, and confidence update.
   - Define variable ranges, clamp behavior, and default constants early.
   - If a spec says a value should rise or fall, it should also say *how*.
   - A useful spec can be implemented from it without needing hidden arithmetic decisions.

6. **Revise specs from reviewer feedback explicitly**
   - When a user provides annotated comments, numbered notes, or handwritten feedback on a spec/PDF, answer point-by-point.
   - Convert each comment into a concrete design decision, wording change, or main-body section change so the revision trail is auditable.
   - If feedback touches session boundaries, confidence growth, or daily reset logic, prefer sleep-based framing over calendar-day framing unless the domain is explicitly calendar-bound.
   - If the user says the document feels clunky, appendix-heavy, or hard to read, reorganize the content into the main narrative rather than stacking more appendices onto the end.
   - Preserve the user's original question structure when possible; use a dedicated response section instead of burying the answer in prose.

7. **Keep specs human-readable, not appendixed**
   - Put formulas, thresholds, defaults, and implementation order next to the section they govern.
   - Reserve appendices for raw artifacts, source excerpts, or non-essential references.
   - If useful content ends up in an appendix during drafting, absorb it into the relevant main section before shipping the spec.
   - If the document is mixing human and business domains, stop and split it into companion docs rather than trying to keep both in one appendix-heavy spec.
   - If the user explicitly says the scoring language is wrong, fix terminology at the source and re-run the verification pass before claiming the doc is corrected.

8. **Keep baseline adaptation scientifically honest**
   - Baseline calibration should modify priors, confidence, or field values only when supported by evidence.
   - Do not hide a normalization layer that re-creates a simplistic scoring bridge.
   - Treat display values, database constraints, and raw calculator inputs as distinct layers.
   - If transcript evidence is sparse, enrich the evidence model upstream rather than inflating downstream scores.
   - Prefer population defaults first, then trait-based personalization, then state-based adaptation, then response-history learning.
   - Preserve short-term adjustment options and long-term scheduling options as separate controls.

9. **Verify with the real engine**
   - Run a direct dry-run through the production entrypoint.
   - Probe the calculator output independently when debugging.
   - Confirm the persisted DB row matches the expected engine/tag/version metadata.
   - If support modules exist (nutrition, sexual health, EF/ADHD overlays), apply them after the real calculator run, not before.

## Multi-stage pipeline data-flow integrity patterns

When building pipelines with 5+ sequential stages that pass data between
each other, these failure patterns cause SILENT data loss. Each was found
by line-by-line tracing of actual code, not by trusting cached audit claims.
All verified in the VERITAS pipeline (2026-08-08).

### Key-name mismatch (#1 silent data loss pattern)

Stage A stores data under key X, Stage B reads key Y. No error thrown.
Data silently lost. The writer and reader were written in different sessions
and never reconciled.

Example: Stage 2 stores `arxiv_results`, Stage 4 reads
`s2.get("papers", s2.get("findings", {}))`. Result: drafting stage produces
content from the raw idea only, with zero research context.

**Fix:** Verify key names by reading the writer's output dict and the
reader's `.get()` calls. Use `grep` to trace every key from creation to
consumption. Do NOT trust variable names that "look right."

### Revision orphan (result computed but never applied)

A revision or improvement stage produces output, stores it in a result
list or local variable, but never writes it back to the shared state
field. Downstream stages use the pre-revision content.

Example: Stage 6 revision sends draft to Wernicke, stores result in
`revisions` list, but `self.state.current_draft` is never updated. The
revision text exists in the results JSON but never reaches the output.

**Fix:** After any revision/improvement stage, write the result back to
the shared state: `self.state.current_draft = revised_text`. Also update
any cached copies in downstream stage results (`stage_results[4.6]["full_draft"]`).

### Output truncation cascade

Multiple truncation points added independently silently destroy content.
Each was sized for a different output format and never recalibrated when
the pipeline started producing full-length papers.

Pattern: `_extract_draft_content` truncates to `fd[:port]` (33% of a
4000-word paper). Stage 6 sends `current_draft[:2000]` to Wernicke (8%).
Stage 5 panel reviews `content[:3000]` (12%). Stage 4.5 sends `draft[:3000]`.

**Fix:** Audit ALL truncation points against actual output sizes. A
4000-word academic paper is ~24000 chars. Truncation to 8000 chars loses
66% of the content. Set limits proportional to expected output or remove
them entirely.

### Revision overwrite danger

When writing revision results back to the shared draft, a revision engine
(like Wernicke) receives truncated input and may return a short snippet.
Writing that snippet back REPLACES the full draft.

**Fix:** Guard with a length ratio check:
```python
if revised_len > 50 and revised_len >= orig_len * 0.6:
    self.state.current_draft = revised_text
```
This prevents a 200-word revision response from overwriting a 4000-word draft.

### Type safety in dict access

`narrative = s35.get("narrative_structure", "")` can return a dict if the
engine response is structured. Then `narrative[:500]` throws
`TypeError: unhashable type: 'slice'`.

**Fix:** Always check type before slicing:
```python
if not isinstance(narrative, str):
    narrative = json.dumps(narrative)
```

### ast.parse() ≠ runtime working

`python3 -c "import ast; ast.parse(open('file.py').read())"` passes for code
with nested f-string quote issues (`f"...{d.get("key","")}..."`) because the
AST parser handles them. But the Python runtime fails with
`SyntaxError: f-string: unmatched '('`. Always run the actual function, not
just AST validation.

### Adversarial verification technique

To find data-flow gaps in a multi-stage pipeline, do NOT trust previous
audit claims. Re-read the actual code line by line:

1. For each stage function, find what keys it WRITES to `stage_results`
2. For each stage function, find what keys it READS from `stage_results`
3. Cross-reference: every key read in stage N must be written in stage <N
4. Check truncation: every `[:N]` slice against actual output sizes
5. Check type safety: every `.get()` result before slicing/indexing
6. Run the pipeline end-to-end and check the ACTUAL output text

This technique caught 8 real gaps in a pipeline that had been "audited"
3 times previously. The previous audits checked that functions existed
(grep), not that data actually flowed between them.

## Self-audit before claiming pipeline works (2026-08-11)

The adversarial verification technique above caught 8 real gaps in VERITAS.
The same technique applied to a freshly-built extraction pipeline
(Research Hub, 2026-08-11) caught 9 defects including 2 CRITICAL:

1. **CRITICAL: Extraction step never called** — `self.extractor = None`
   in `__init__`, never initialized. The extraction engine existed as dead
   code. The pipeline produced passages but zero findings. Wire every
   pipeline stage end-to-end before claiming it works.
2. **CRITICAL: Verification gate never wired** — NLI module existed but
   `process_pdf()` never called it. Anti-hallucination gate was decorative.

**Lesson:** Building modules is not building a pipeline. A pipeline is the
DATA FLOW between modules. After writing each stage, trace the actual data
path: does the output of stage N reach the input of stage N+1? Run the
pipeline end-to-end on a real input and verify the final output contains
data from every stage. Module-level unit tests do not catch wiring gaps.

This applies to ANY multi-stage pipeline: extraction, scoring, research,
generation. The failure mode is identical: each module works in isolation,
the pipeline produces plausible-looking output, but entire stages are
silently skipped because the wiring was never completed.

## Multi-domain evidence classification architecture (2026-08-11)

When building evidence pipelines that must serve multiple research domains
(medical, AI/ML, nutrition, neuroscience, climate, education, economics),
do NOT build separate per-domain pipelines. Build ONE universal extraction
engine with domain overlays.

**Universal layers (field-agnostic):**
1. Extraction: GROBID + passage extraction + quote verification + NLI
2. Study design detection: ~40-50 patterns covering ALL fields (RCT, meta-analysis, cohort, benchmark, theoretical, ethnography, etc.)
3. Evidence quality scoring: universal 9-tier hierarchy (meta-analysis of RCTs > single RCT > quasi-experimental > cohort > case-control > cross-sectional > case report > mechanistic/in vitro > expert opinion). Broadly agreed across EBM, Campbell Collaboration, WWC, Cochrane.

**Domain overlays (50-150 lines each, composable):**
- Medical: PICO extraction, GRADE upgraders/downgraders, FDA language scan, modality classification
- ML/CS: code release check, benchmark standardness, seed reproducibility
- Neuroscience: power analysis flag for underpowered fMRI (N<20)
- Nutrition: funding source extraction, FFQ reliability flag
- Climate: model vs observation tagging, IPCC confidence language
- Economics: identification strategy classification (IV, DID, RDD)

Overlays COMPOSE — a gut-brain paper gets neuroscience + nutrition + immunology
overlays simultaneously. Separate pipelines cannot do this.

**User correction (2026-08-11):** "Should we even use these sub fields and
break them down or should we break them down a different way?" — The user
recognized that sub-field decomposition mirrors academic departments, not
how evidence actually works. An RCT is an RCT regardless of field. The
correct axis is study design + evidence quality, with lightweight domain
overlays for field-specific concerns.

## Final-gate enforcement audits (decorative-gate detection, 2026-08-15)

A pipeline's last stage ("QA & output") has a distinct failure class: checks that
RUN but don't BLOCK. Audit method (proven on VERITAS stage 7):

1. Inventory every check + threshold, then classify each as **enforced**
   (returns/aborts/rewrites output) vs **advisory** (logged or tagged onto a
   status string like `complete_with_quality_issues` — artifact still ships).
2. Trace READERS of every check result; a result with zero downstream readers is
   decorative no matter how sophisticated the check.
3. Watch computed-but-unused signals: a `phantom`-citation count that is detected
   but a gate reading only the `weak` count = gate wired for show.
4. Exception handlers at the gate stage that still emit output
   (`complete_with_errors`) convert crashes into pseudo-success.
5. Diff the backend's settable status strings against the frontend poller's
   matched statuses — unmatched statuses fall through silently and the UI renders
   a synthesized success narrative while quality warnings rot unread.
6. Report the blocking-condition list explicitly; if empty, the gate certifies
   nothing → verdict DECORATIVE (vocabulary: SOUND / PARTIALLY SOUND /
   DECORATIVE / BROKEN).

Case study with exact line evidence and prescribed fixes:
`references/veritas-stage7-gate-audit.md`.

## Verdict semantics in multi-approach gates (2026-08-16)

Stage-7 audits ask "does the gate block?"; the stage-3.1 VERITAS physics-gate
audit (Bridgman operationalism grading, two principal-initiated runs killed) asks the
inverse: **does a blocking verdict measure what it claims?** A gate can be fully
enforced and still invalid. Five rules, proven on `veritas_engine.py validate()`:

1. **Vote-counting is valid only if every Boolean shares one referent.** Four
   heterogeneous statistics — free-energy (economics of *running* the validation),
   coupling (reviewer agreement), criticality (convergence through data that may
   not exist), Bayes (the claim itself) — collapsed into a pass-count. That adds
   meters to kilograms, and the verdict text ("majority of approaches reject")
   was false against its own inputs: zero approaches had measured rejection.
2. **Abstention must shrink the denominator, never sign either side.** FE "SKIP"
   (cost > info gain — a property of the instrument, not the claim) scored as a
   failure vote; CRIT "NO HISTORY" *passed* by verb-absence (`"TIPPING" not in
   verdict` → True). A non-measurement cannot be affirmative evidence either way.
   Beware one word carrying two opposite operational consequences in the same
   codebase (pre_flight SKIP → early return; free_energy SKIP → reject vote).
3. **A threshold decision inside its own noise band is not a decision.**
   Posterior 0.493 ± 0.177 against a 0.5 cut: |mean − threshold| ≪ σ, P ≈ coin
   flip. Correct verdict is INCONCLUSIVE + gather evidence or escalate — the
   module's own "BORDERLINE" label was overridden by a hard `> 0.5` cut in the
   synthesizer.
4. **Bucket-keyed "confidence" constants are not probabilities.** confidence=0.15
   keyed to pass-count measures the arithmetic of the voting procedure, nothing
   else — and a downstream ABORT-ON-FAIL guard then treats it as ground truth
   sufficient to kill human-initiated runs.
5. **Killing numbers dominated by unmeasured constants are priors, not
   evidence.** F = 0.18 was mostly the hand constants cost=0.2 and T=0.5 — the
   gate killed runs on its own assumptions about itself, not on claim data.

Hard-ABORT vs downgrade-to-flag vs ask-the-human (ranked by operationalism):
ABORT only for performed, decisive, unambiguous measurements (e.g., a verifiable
linguistic fact like a strong-claim word without original data); FLAG for
economics votes and missing-data states; ASK-THE-HUMAN for any statistic inside
its own noise band — the human who launched the run is the other available
instrument.

Full case study with reproduction and line numbers:
`references/veritas-stage31-physics-gate-audit.md`.

## Pitfalls

- Do **not** ship a parallel "user learning" shell that invents burnout/TWC without `calculator.compute_twc`.
- Do **not** default check-ins through full sub-algorithm dataclasses unless field scales match the calculator contract; prefer dim10→DimensionScore for lightweight check-ins.
- Do **not** bake author/peer baselines into a blank-slate organism — owner-only adaptive baseline.
- Do **not** add a covert 1-10 bridge in front of a complex calculator.
- Do **not** confuse storage normalization with the scoring algorithm.
- Do **not** let a transcript adapter overwrite stronger evidence with weaker defaults.
- Do **not** round display values and then treat them as the source of truth.
- Do **not** assume a score is correct just because the code compiles; verify the engine path and the persisted row.
- Do **not** tune the calculator to compensate for missing evidence when the real fix is to add a source adapter.
- Do **not** treat transcript-only evidence as sufficient when calendars, wearables, finance, messages, or task history are available.
- Do **not** collapse immediate actions, repeated routines, and long-term goals into one scoring layer.
- Do **not** assume one routine timing fits all users; shift-worker and chronotype cases need special handling.
- Do **not** anchor daily reset logic to midnight when the product is explicitly sleep-linked; use sleep/wake boundaries or a clear anchor-sleep model.
- Do **not** answer reviewer feedback with generic prose when the user asked for point-by-point responses tied to concrete spec changes.
- Do **not** leave core formulas, defaults, or source-set rules stranded in an appendix if they belong to the main design.
- Do **not** merge human-level and organization-level scoring into one spec when the domains have different clocks, baselines, and vocabulary.
- Do **not** propose a menu of disconnected physics frameworks (quantum tunneling, string theory, Gibbs free energy, Boltzmann distributions) hoping one sounds right. Only propose frameworks that share variables with the existing math stack and produce real calculations.
- Do **not** present qualitative analogies ("quantum tunneling models ADHD hyperfocus") as scoring extensions. If it doesn't produce a number from machine-measured data, it's not a calculation.
- Do **not** validate a physics-informed model against synthetic data generated by the SAME physics the model encodes. This is circular: the model "knows" the generating process and will always appear to outperform an unconstrained baseline. The PIML prototype audit (2026-06-13) caught this exact flaw — a model tested against data from its own coupling matrix showed "4-12x improvement" that was actually 6% on the primary metric. Always validate against data from a DIFFERENT generative process or against real user data. See `scientific-methodology-review-and-consolidation` skill for the full detection pattern.
- Do **not** let an LLM-generated preliminary score be structurally inconsistent with the deterministic engine that processes it. If the LLM reports a preliminary TWC of 41.5 but the base dimensions it provides compute to a structural floor of 55.4, the 13.9-point gap will be silently absorbed by the rescore engine and reported as "improvement." In the the specialist engine audit (2026-06-13), 77-91% of rescore deltas were LLM inconsistency correction, not real wellness change. Always verify structural consistency: compute the floor from the LLM's own components and flag if `preliminary_TWC < structural_floor`.
- Do **not** hardcode scoring invariants that prevent the system from detecting legitimate negative results. A rule like "positive evidence must never produce a lower score" creates a one-tailed measurement bias — the system cannot detect patterns where one dimension improves while the aggregate should decline. If the monotonicity rule is clinically necessary, disclose it in any metric derived from these scores and track the unconstrained score alongside the clinically adjusted score. See `scientific-methodology-review-and-consolidation` Check 7 for the full Popperian critique.
- Do **not** conflate bounded numerical output with safe system output. A scoring engine that constrains scores to [0, 100] does NOT make the system "unable to hallucinate" if an LLM generates coaching text. Physics constraints on scalar scores do not constrain LLM text generation. Any claim that the "system cannot produce impossible results" is a category error if the system includes LLM-backed text output. See `scientific-methodology-review-and-consolidation` Check 8.
- Do **not** maintain multiple `classify_twc` / `tier_label` functions with different scales and thresholds across files in the same codebase. If `calculator.py` uses a 0-1 scale with 6 labels, `rescore_engine.py` uses 0-100 with 7 labels, `build_report.py` uses 0-10 with 3 labels, and `adhd_fusion.py` uses 0-1 with RED/YELLOW/GREEN — the same score produces wildly different classifications depending on which code path runs. Canonicalize to one scale and one label set, then apply proportional conversion at each call site. The the specialist engine audit (2026-06-13, Popper Finding 2) found exactly this pattern across 4 files.
- Do **not** claim citation counts in product/marketing docs that are not backed by a verifiable citation list. A claim of "37 citations" with zero citations listed is a ghost citation — a severity-1 integrity issue that invalidates the document. Every citation count must map to actual entries with author, year, journal, and DOI/URL. The VERITAS dogfood audit (2026-06-11) caught this: marketing docs claimed 37 citations but only 7 were verified to exist. Fix: add a Citation Verification Gate to the review process and quarantine docs that fail it.
- Do **not** present a multi-question decision menu after completing a physics-scoring design. When you have finished the design and the remaining work is implementation-detail curation (which parameters, which values, which policy), lock those details yourself with stated rationale and hand off. The user's role is veto-only, not co-authorship of the parameter space. Presenting 4 open-ended questions ("confirm the situation vector?", "which triples?", "permit asymmetric κ?", "what evidence policy?") after a sound design triggered "I cant tell what you are asking of me" on 2026-06-28. See `adhd-choice-discipline` skill for the full pattern.
- Do **not** compute circadian midpoint by naively averaging onset and offset times for sleep periods crossing midnight. `(23.5 + 7.0) / 2 = 15.25` (3:15 PM) is wrong; the correct midpoint is ~3:25 AM. Fix: `if offset < onset: midpoint = ((onset + offset + 24) / 2.0) % 24 else: midpoint = (onset + offset) / 2.0`. This bug silently destroys the Von Mises circadian alignment score for any user who sleeps across midnight (most of the population). Caught in 8D Sleep build (2026-06-15).
- Do **not** iterate over a dict that mixes nested dicts with scalar values and call `.get()` on every entry. When a detail dict accumulates both structured sub-dicts (e.g., `{'N1': {'actual': 5, 'target': 5, 'deviation': 0}}`) and scalar metadata keys (e.g., `'exponent': 2.34`), iterating with `min(detail, key=lambda k: detail[k].get('deviation', 0))` raises `AttributeError: 'float' object has no attribute 'get'`. Fix: filter first with `isinstance(v, dict)` before calling dict methods, or keep metadata in a separate key namespace. Caught in 8D Sleep SAS scoring (2026-06-15).
- Do **not** vote-count heterogeneous gate statistics (economics, agreement, missing-data, posterior) into a single pass-count verdict — each Boolean must share one referent or the sum is meaningless and the verdict text will misdescribe its own inputs.
- Do **not** score an abstention as a failure vote (FE SKIP → reject), nor let a missing-data state pass by verb-absence (`"TIPPING" not in "NO HISTORY"` → True). Abstention shrinks the denominator; it never signs either side.
- Do **not** cast a hard threshold cut on a statistic that sits inside its own uncertainty band (0.493±0.177 vs 0.5). That is INCONCLUSIVE, not a NO vote — and never let a synthesizer override a module's own BORDERLINE/UNCERTAIN label with a hard cut.
- Do **not** wire a hard ABORT-ON-FAIL guard to a verdict produced from bucket-keyed confidence constants (0.95/0.75/0.45/0.15 keyed to pass-count) — those constants measure the voting arithmetic, not claim probability, and will kill human-initiated runs on nothing.

## Physics-informed recommendation scoring (research writing)

When scoring research/writing opportunities (not health dimensions but topic
selection), apply the same physics principles but adapted for the information
domain. Proven in the Writing Studio recommendation engine (2026-08-07):

| Dimension | Formula | What It Measures |
|-----------|---------|------------------|
| Free Energy | F = cost - T * info_gain | Is this writing worth the compute? Lower F = better investment |
| Kuramoto | alignment to existing knowledge base | How well does it connect to canon/infrastructure? |
| Critical Slowing | citation velocity + emerging indicators | Is the field near a paradigm shift? |
| Bayesian | P(impactful \| trend, evidence, confidence) | Will this writing land? |

**Key lesson (user correction 2026-08-07):** Do NOT apply physics formulas to
fabricated data and call it a recommendation engine. The user caught static
JSON topics with physics math sprinkled on top: "where are you pulling these
recommendations from. these are too generic." The scoring is meaningless if
the underlying data is hand-written. Recommendations must pull from REAL
sources (canon.db findings, live arXiv API, Semantic Scholar citation data).

**Normalization calibration:** Physics scores that produce all-GO or all-DEFER
are miscalibrated. A healthy distribution is roughly 30-40% GO, 40-50% WATCH,
10-20% DEFER. If free_energy scores are all 0 or all 10, the cost/info_gain/T
constants need recalibration before presenting. Test with real data before
shipping.

**SQL ambiguous columns in scoring queries (2026-08-07):** When JOINing
principles or findings with domains for scoring input, both tables share
column name `id`. A bare `SELECT id` in a JOIN produces
`sqlite3.OperationalError: ambiguous column name: id`. Always use explicit
table prefixes: `SELECT p.id as pid, p.title as ptitle, d.display_name as
domain FROM principles p JOIN domains d ON p.domain_id=d.id`. This class of
bug is silent in development (single-table queries work) and only surfaces
when the scoring pipeline joins to enrich domain metadata.

**Operator bus post CLI silently fails (2026-08-07):** The
`organism/operator_bus.py post` CLI reports success but may not write to the
database. The bus DB lives at the workspace root
(`message-bus.db`), not inside `organism/`. When a bus handoff MUST land
(e.g., handing off to sibling-agent for a build), write directly:
```python
conn = sqlite3.connect('message-bus.db')
c = conn.cursor()
c.execute("INSERT INTO messages (timestamp, from_op, to_op, msg_type, subject, content, status) VALUES (?,?,?,?,?,?,'pending')", ...)
conn.commit()
```
Verify with a SELECT after insert. Do not trust the CLI's success text alone.

## Useful checks

- `python -m py_compile` on changed modules
- direct dry-run of the live scoring entrypoint
- calculator probe with representative field sets
- DB row inspection for score engine/version/baseline metadata
- source-adapter coverage review: transcript, calendar, wearable, finance, social/messages, tasks/quests
- state- and sleep-boundary checks for day sealing and confidence growth

## Physics-informed scoring pattern

When building a scoring pipeline for a health/wellness domain, use **structural mathematical isomorphisms** — the same equations that describe a well-established physics domain also describe the biology, with identical mathematical structure and only the variable names changed. Every physics mapping must cite a peer-reviewed source.

**CRITICAL — no metaphors:** Do NOT use metaphorical physics language (e.g., calling disruptors "antigravity" or sleep an "attractor basin"). Instead, show the actual equation shared between the biology and the physics. Example: adenosine accumulation during wake follows `dS/dt = (S_max − S) / τ` — the same first-order ODE as capacitor charging in an RC circuit (Borbély 1982). That is an isomorphism, not an analogy.

**Proven isomorphisms in sleep science** (for reference when building sleep-related products):
- Process S (homeostatic pressure) ↔ RC circuit charge/discharge — first-order ODE
- Process C (circadian rhythm) ↔ Van der Pol oscillator — nonlinear limit cycle (Kronauer 1990)
- REM–NREM cycling ↔ Lotka-Volterra predator-prey — reciprocal inhibition (McCarley & Hobson, Science 1975)
- Wake–sleep switching ↔ double-well potential with Langevin dynamics — bistable switching (Diekmann et al. 2022)
- Thermoregulation ↔ Newton's law of cooling — `dT/dt = −k(T − T_set)` (Kräuchi 1999)
- Brief awakenings ↔ non-homogeneous Poisson process — memoryless point process (Lo et al. 2002)
- Caffeine effect ↔ first-order elimination / radioactive decay — `C(t) = C₀ · e^(−t/τ)` (Zenk et al. 2021)

**Disruptors modify specific sub-components, not the final score.** Caffeine reduces N3 penetration and increases SOL via Process S suppression. Blue light phase-shifts CAS via van der Pol forcing. Stress/noise increase FI via Langevin stochastic forcing. Never apply a single post-hoc multiplier to the composite score.

See `references/physics-informed-scoring-isomorphisms.md` for the full pattern with all isomorphisms, citations, and coaching integration.

**User preference:** When the user names a physics concept, research whether a genuine structural isomorphism exists in the published literature. If it does, build the full mathematical treatment with citations. If it doesn't, say so honestly — do not force a metaphor. Intellectual honesty is more valuable than a creative framing that can't withstand scrutiny.

### Extending an existing physics-based scoring system

When a scoring engine already uses physics-motivated math (Riemannian geometry, SDEs, optimal transport, etc.), extensions must pass all five checks before you propose them:

1. **Variable sharing** — the new math must use the same variables already in the pipeline (same V(x), same T_eff, same g_ij). If it requires entirely new inputs, it's a separate system, not an extension.
2. **Self-consistency** — the new framework must operate on the same dynamical system. Kramers escape rate works on the Langevin SDE because it *is* the standard result for that system. String theory doesn't work because the scoring engine has no vibrational modes.
3. **Zero human-rating preservation** — the extension must not introduce any subjective scales. Every new variable must be computable from counts, timestamps, ratios, or geometric quantities.
4. **Real calculations, not descriptions** — the extension must produce a number (escape rate, transition probability, susceptibility), not a qualitative framing ("quantum tunneling models ADHD hyperfocus").
5. **Layer extension, not layer addition** — the new math should deepen an existing layer (barrier diagnostics → escape probabilities) or fill a gap in the existing stack (static regime labels → physics-derived regimes), not create a disconnected parallel system.

**DO NOT propose a menu of physics frameworks hoping one sticks.** Pick the one or two that genuinely extend the existing math, explain *why* they fit the existing stack, and note what they share with it. A wrong extension proposed confidently and then rejected is worse than saying "I don't see a clean fit right now."

- `references/physics-informed-scoring-isomorphisms.md` for proven mappings and `references/gas-v2-extension-pattern.md` for the GAS v2.0 Kramers + Landau-Ginzburg extension as a worked example of this process.
- `references/research-hub-gap-analysis.md` — 25-gap inventory for academic paper extraction pipeline (GROBID + NLI + modality classification). Verified tools, Python environment notes, and the universal-engine-with-overlays architecture decision.

## Support files

- `references/physics-informed-scoring-isomorphisms.md` — structural isomorphism pattern for scoring pipelines: 9 sleep↔physics + 2 behavioral↔physics (Kramers, Landau-Ginzburg) mappings with citations, disruptor modeling, coaching integration, and the honesty-first rule.
- `references/gas-v2-extension-pattern.md` — worked example of extending GAS v2.0 with Kramers escape rate and Landau-Ginzburg phase transitions; includes the five-check evaluation criteria and user correction about not smashing disconnected frameworks together.
- `references/coupling-matrix-higher-order-tensor.md` — worked example of extending the 8D wellness coupling matrix from rank-2 (28 pairs) to rank-3 (triples) with situational gating, free-energy term selection, and adiabatic staging. Includes antagonistic coupling and the user-preference lesson about locking design details instead of presenting a questionnaire.
- `references/physics-informed-scoring-antigravity.md` — DEPRECATED. Superseded by `physics-informed-scoring-isomorphisms.md`. Retained for historical reference only (the antigravity metaphor approach was replaced by structural isomorphisms in v2.0.0).
- `references/session-2026-05-29-divinitygr-direct-evidence.md` — session notes, adapter lessons, and verification pattern for direct calculator input mapping.
- `references/direct-input-evidence-scoring.md` — adapter guidance for mapping evidence into native calculator inputs.
- `references/database-scored-vs-display-layer.md` — terminology correction: database-scored/native outputs first, presentation conversion only after TWC.
- `references/session-2026-05-29-progressive-confidence-review.md` — concise notes on sleep-sealed days, rising confidence across a wake session, and point-by-point review-response handling.
- `references/calculation-spec-template.md` — checklist/template for specs that need explicit formulas, bounds, and acceptance criteria.
- `references/progressive-confidence-attention.md` — progressive provisional-score UX: show value immediately, grow confidence as evidence accumulates, and reset on sleep/wake boundaries.
- `references/spec-structure-human-readable.md` — notes on reorganizing specs into one coherent narrative with formulas and thresholds in the main body.
- `references/domain-splitting-human-vs-business.md` — concise note on when to split person-level and organization-level scoring into companion specs, with naming and shared-primitives guidance.
- `references/fresh-organism-layered-8d-learning.md` — vendor calculator + L0–L5 learning/healing on blank-slate the operator agent; dim10 path; B2BU framing.
- `references/veritas-stage7-gate-audit.md` — VERITAS stage-7 output-gate audit: decorative-gate detection method, exact line evidence (weak-vs-phantom gating bug, `complete_with_quality_issues` non-blocking tag, UI poller status mismatch), prescribed fixes.
- `references/veritas-stage31-physics-gate-audit.md` — VERITAS stage-3.1 physics-gate operationalism audit: vote-counting over incommensurable statistics, SKIP-scored-as-reject / NO-HISTORY-scored-as-pass, threshold inside its own noise band, bucket-keyed confidence constants feeding a hard ABORT; graded fixes.
