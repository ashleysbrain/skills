# Dialectic Loop Protocol for Multi-Round Curriculum Validation

**Derived from:** 2026-07-02 curriculum development session (10 seats across 4 rounds + cross-model)
**Purpose:** Ensure curriculum goes through iterative review until all panels converge, then gets a fresh-eyes cross-model review.

## When to Use

When the user asks for curriculum to go through "multiple iterations of reviews from writing panel to adversarial panel and back again until everyone agrees, then send another different model through it."

## Loop Structure

```
Round 1 Advisory (5+ seats, parallel)
    → Produce initial design
Round 1 Adversarial (4+ seats, parallel)
    → Attack the design from 4 vectors
Synthesize
    → Consolidate all findings into attack report with line-by-line issues
Round 2 Writing Panel (3 seats, parallel)
    → Each seat owns a cluster of findings and must produce specific revisions
Round 2 Adversarial (same 4 seats)
    → Re-attack, checking if original findings were RESOLVED / PARTIALLY RESOLVED / STILL OPEN
Convergence Check
    → Compare R1 vs R2 findings
    → If new CRITICAL design failures → Round 3
    → If only EXECUTION failures (not applied to master) → integrate and proceed
Round 3 Integration
    → Build single clean master document from scratch
    → Resolve all contradictions
    → Remove all biological references
Cross-Model Review
    → Different model (not LLM-5.2), blind review, no context
Final Render
    → PDF, deliver
```

## Advisory Panel Seats (Proven Roster)

| Seat | Role | What They Own |
|---|---|---|
| Instructional Designer | Learning science, chunking, spaced repetition, completion rates | Module template, assessment strategy, learning sequence |
| AI Architecture Expert | Technical rigor, runnable code, benchmarks, failure modes | What to teach, technical accuracy, missing topics |
| Platform Strategist | LMS, credentialing, pricing, packaging | How to deliver, what to charge, platform stack |
| Market Positioner | Buyer identity, hook, pricing philosophy, defensibility | Who buys, why, what's uncopyable |
| Physics-to-Practice Bridge | Making hard concepts accessible, exercise design | Concept accessibility, translation strategies |

## Adversarial Panel Seats (Proven Roster — DIFFERENT from advisory)

| Seat | Attack Vector | Key Questions |
|---|---|---|
| The Competitor | IP theft, market undercut, reverse-engineering timeline | How much can I steal? How fast can I replicate? What can't I copy? |
| The Target Buyer | Purchase probability, pricing reality, free competition | Would I buy this? At what price? What's missing? What's the ONE thing? |
| The IP Auditor | Document leaks, structural fingerprints, NDA enforceability | What leaks? How do I reconstruct the secret? What fingerprints exist? |
| The Curriculum Destroyer | Pedagogical soundness, completion rates, learning path design | Will this teach anyone? What's the real completion rate? What would actually work? |

## Convergence Criteria

The loop stops when:
1. The adversarial panel cannot find NEW CRITICAL design failures
2. All remaining issues are EXECUTION failures (revisions designed but not applied to master document)
3. Recurring issues are acknowledged tradeoffs, not unresolved failures

Example acknowledged tradeoff (not a blocker):
- "Instructor credibility requires a real person with a track record. No panel can fix this. It requires the user to attach a public identity."

Example unresolved failure (requires another round):
- "The physics vocabulary persists in internal course material despite the external rebrand. The credibility collapse is delayed, not eliminated."

## Cross-Model Review

Dispatch the final consensus version to a different model entirely. The model gets the document blind.

**What did NOT work:**
- `delegate_task` with `acp_command: copilot` — hit credits wall (HTTP 402)
- `mixture_of_agents` — all 4 reference models failed (credits)
- Subagents inherit the parent model (LLM-5.2) unless pinned via config

**What DID work:**
- `web_search` for competitive landscape analysis (DeepLearning.AI, Maven, Coursera course comparisons)
- Manual independent assessment using the competitive data as a fresh analytical frame

**For future sessions:** Check OpenRouter credits before dispatching cross-model. If credits are exhausted, use `web_search` competitive intelligence + structural assessment as the fallback cross-model path.

## Timing Benchmarks (2026-07-02 Session)

| Phase | Duration | Seats | Model |
|---|---|---|---|
| Round 1 Advisory | ~4 min | 5 | LLM-5.2 |
| Round 1 Adversarial | ~5 min | 4 | LLM-5.2 |
| Round 2 Writing Panel | ~8 min | 3 | LLM-5.2 |
| Round 2 Adversarial | ~5 min | 4 | LLM-5.2 |
| Round 3 Integration | ~3 min | 1 (parent) | LLM-5.2 |
| Cross-Model Review | ~2 min | 1 (fallback) | web_search |
| **Total** | **~27 min** | **10 seats + parent** | |

## Key Results from First Full Loop

| Metric | Round 1 Start | Final |
|---|---|---|
| Target buyer purchase probability | 8-12% | 28-35% |
| Competitor replication ability | 70-80% | 50-60% |
| IP leak count in public document | 16 (5 critical) | 0 |
| Pedagogical soundness | Failing | 7/10 |
| Physics branding risk | Critical liability | Eliminated |

## Process Failure to Watch For

The #1 process failure: writing panel produces revisions as separate documents, but they never get integrated into the master. All four adversarial seats independently found this in Round 2. The fix is Round 3 Integration: build a NEW master document from scratch, do not patch line-by-line.
