---
name: external-content-qa-pipeline
description: Mandatory QA review for ALL external-facing content before delivery. Covers AI telltale detection, human voice verification, factual accuracy, and the full review pipeline. the principal's standing rule — nothing goes out without QA.
tags: [qa, content, external, telltales, review, prism, writing, operations]
version: 1.1
---

# External Content QA Pipeline

## When to Use
- ANY content going outside the organization (applications, papers, blog posts, social media, emails to external parties, grant submissions, pitch decks, website copy)
- ANY team-facing or internal document before it is presented to the principal (team updates, meeting briefs, roadmap docs, PDFs rendered for her review). The gate is not just for external publication. See pitfall #12.
- After any agent drafts external or team-facing content
- Before delivering documents to the principal for final review
- Before rendering a branded PDF from any draft. The render step must not fire until the scan returns clean.
- When the principal says "make sure this gets QA review" or references the QA process

## The Rule (the principal's Standing Directive — 2026-03-31)

**"Anything that gets written for external publication in any form always needs QA review."**

This is non-negotiable. No exceptions. If it leaves the organization, it gets reviewed.

## Pipeline

```
Agent drafts → QA Review → Fix issues → Re-review if needed → the principal approval → Publish/Submit
```

### Step 1: Agent Drafts Content
- Any agent can draft (WORMHOLE for BD, QUILL for content, ATLAS for papers, etc.)
- Draft saved to appropriate path
- Agent marks content as NEEDS_QA

### Step 2: QA Review (Mandatory)
Assign to QA agent (PARALLAX, or spawn a QA reviewer through FORGE+ARBITER talent gate).

#### AI Telltale Scan (ZERO TOLERANCE)

The gate runs BEFORE the PDF render step. A script lives at `scripts/scan_ai_tells.py` (under the `ai-tell-removal-gate` companion skill). Run it: exit 0 = clean, exit 1 = telltales found and the document does not ship. The scanner is authoritative; manual eyeballing is the floor, not the ceiling. In the 2026-07-07 gamification team-update session, the scanner caught a phrase ("just paint on") that a manual pass had missed.

**Banned punctuation:**
- ❌ No em dashes (—) or en dashes (–). Replace with commas, periods, colons, or rewrite.

**Banned phrases and words:**
- ❌ "Furthermore," "Moreover," "In conclusion," "It is worth noting"
- ❌ "delve," "tapestry," "landscape," "leverage," "utilize," "facilitate," "encompass"
- ❌ "It's important to note that," "This highlights," "This underscores"
- ❌ "I am reaching out" / "I am writing to" / "I am writing regarding" / "I am writing to request" (staple of AI-generated emails and letters. Use plain openers: state why you're contacting them directly.)
- ❌ "[Subject] landscape" (e.g., "litigation landscape," "technology landscape")
- ❌ No perfectly balanced three-item lists everywhere
- ❌ No overly formal academic tone where casual is appropriate

**Positive patterns to use instead:**
- ✅ Vary sentence length (mix short punchy with longer)
- ✅ Use contractions where natural
- ✅ Specific, concrete language (not vague platitudes)
- ✅ Direct, plain-English openers for letters/emails ("I found your firm through..." / "I'm looking for an attorney who...")

#### Human Voice Check
- Does this sound like a REAL person wrote it?
- Is there genuine specificity and personality?
- Are there details only the real author would know?
- Flag sections needing personal anecdotes or real data
- Score: 0-10 (must be 8+ to pass)

#### Factual Accuracy
- No claims of credentials people don't have (the principal does NOT have a PhD)
- No fabricated publications, awards, or metrics
- No exaggerated claims without evidence
- Verify all specific assertions
- For academic content, audit citations at two levels: named-author coverage AND implicit load-bearing scientific lineages
- A DOI/title check alone is insufficient; each source must be the correct primary or canonical source for the exact claim
- Run a reverse-relevance pass: every bibliography entry must support a specific sentence, mechanism, distinction, or lineage (no citation padding)
- Confirm the live submission form's reference-field style and whether references count toward the abstract word limit
- Score: 0-10 (must be 9+ to pass)

#### Content Quality
- Is it compelling for the target audience?
- Is positioning clear and differentiated?
- Does it answer what the recipient actually wants to know?

### Step 3: Fix Issues
For EVERY issue found:
1. Quote the exact problematic text
2. Explain why it fails QA
3. Provide a suggested replacement
4. Create revised version (v2, v3, etc.)

### Step 4: Log in Analytics
Every QA review MUST be logged in the qa_tracking table:
```sql
INSERT INTO qa_tracking (
    task_id, content_path, content_type, reviewer_agent, reviewed_at,
    ai_telltale_count, em_dash_count, banned_phrase_count,
    human_voice_score, factual_accuracy_score, overall_pass,
    issues_found, revision_number
) VALUES (...);
```

### Step 5: the principal Approval
External content always gets the principal's final eyes (per WRITING-WORKFLOW.md).

#### Architecture Encryption (MANDATORY for any content referencing the DS organism)

the principal's standing rule (2026-07-02): "We do NOT want to give away our biological isomorphisms so we must always use technology analogs. We do not want to give away our secret sauce without encrypting it and making it more complex to decipher."

The biological isomorphism (mapping body systems, tissue types, and named scientist methodologies to AI engine architecture) is the compound moat. It must NEVER appear in external-facing content. Every biological concept has a public technology analog that is functionally identical but obscures the biological source.

**What is SECRET (never in external content):**
- Biological body-system to engine mappings (nervous, cardiovascular, immune, etc.)
- Named scientist methodology per engine (Ramon y Cajal, Kuramoto, Maxwell, etc.)
- Body-part analogies (thalamus, hippocampus, vagus nerve, tissue types)
- The specific combination of physics plus biology (the compound moat)
- The actual organism topology (engine count, port assignments, tissue connectivity)
- Proprietary 8D/TWC scoring formula
- Creative organs mapped to brain regions

**What is TEACHABLE (not our secret):**
- The five physics concepts (superposition, entanglement, free energy, critical slowing, adiabatic) as published physics
- Physics-informed thinking as an approach to AI agent design
- Multi-agent coordination patterns (standard vocabulary)
- Evidence-based scoring approach (not the proprietary formula)
- Semantic task routing concept (not the thalamocortical mapping)

**Encryption checklist (run before ANY external content ships):**
- [ ] No references to specific biological systems (nervous, cardiovascular, immune, etc.)
- [ ] No scientist names associated with specific engines
- [ ] No body-part analogies (thalamus, hippocampus, vagus nerve, etc.)
- [ ] No references to tissue types
- [ ] No references to specific engine topology (port numbers, engine count)
- [ ] No references to proprietary scoring formula
- [ ] All examples use standard software engineering vocabulary
- [ ] Physics concepts presented as general principles, not mapped to specific software decisions

Full mapping table (internal biological term to public technology analog): see `references/architecture-encryption-map.md`

Score: 0-10 (must be 10 to pass — any biological fingerprint fails the gate)

#### Cross-Document Figure & Spec Consistency (MANDATORY for any product/business doc family)

When a deliverable belongs to a family of related documents (principal business plan + company profile + product roadmap + pitch deck + website copy for the same product/subsidiary), a single-doc QA pass is insufficient. Figures and core specs drift apart across independently-edited docs with no single source of truth, and a customer or investor reading two docs together will spot the contradiction immediately.

**Run this check whenever QA-ing a product/business doc that has sibling documents.**

The check:
1. Enumerate the sibling docs (same product, same subsidiary, same launch)
2. Read them together in one pass
3. Compare EVERY numeric claim and core spec across all docs:
   - Product specs (category counts, tier counts, reviewer counts, feature lists)
   - Financial figures (revenue projections, margins, pricing, breakeven volumes)
   - Market sizing (TAM, segment sizes, market share percentages)
   - Capability claims (team size, throughput, turnaround times)
   - KPIs and targets
4. Flag ANY disagreement. Two docs, two numbers for the same metric = FAIL.
5. For each contradiction, require a single canonical value and a note on which docs must be corrected.

**Common drift patterns (from 2026-07-06 VERITAS dogfood of the OCTAD subsidiary docs):**
- Category count: exec summary says "10-category", company profile says "8 rigorous categories" — same product, same launch, core spec disagrees
- Reviewer count: "30-50 reviewers" in one section, "250 reviewers" in the competitive moat section — capability inflation when the bigger number appears in sales-facing copy
- Revenue: exec summary Y1=$52K, conservative table Y1=$35K, target table Y1=$60K, company profile Y1=$52K — three sources, three numbers for the same metric
- Breakeven arithmetic: stated breakeven volume off by 4x from fixed-costs ÷ contribution-margin — recompute every breakeven figure, do not trust stated values
- Margin %: "58-63%" in exec summary, "60%/64%/65%" in detail table, "62%/58%/63%" in a sibling doc

**Also verify these claim types that carry legal/reputational risk:**
- Outcome guarantees the company cannot control (e.g., "90%+ acceptance rate" for a pre-submission review service — we review, the journal accepts; promising acceptance is promising a decision outside our control). Reframe as a metric we DO control (e.g., "review score ≥9.0 achieved for X% of submissions").
- Evasion-adjacent guarantees (e.g., "money-back if flagged by AI detection" — implicitly sells detection evasion, attracts the wrong customers). Scope any AI-detection refund to "flagged erroneously," not "flagged."
- Unsourced market statistics ("competitor X has 90%+ market share" with no citation). Fabricate-or-cite rule: every market-share or market-size claim needs a source or must be removed.

Score: 0-10 (must be 9+ to pass — any cross-doc contradiction on a core spec or financial figure fails the gate)

## Content Type Routing

| Content Type | Primary QA Agent | Threshold |
|---|---|---|
| Academic paper / abstract / conference submission | the specialist engine (HERMES lane) + VERITAS pipeline (250-agent panel + 50-venue panel) | Per `references/veritas-academic-writing-workflow.md` — NEVER route to sibling-agent for academic writing |
| Grant/application | PARALLAX or QA reviewer | Telltale 0, Voice 8+, Accuracy 9+ |
| Blog/LinkedIn | QUILL self-review + telltale scan | Telltale 0, Voice 7+ |
| Social media | Telltale scan (automated) | Telltale 0 |
| Email to external | Telltale scan | Telltale 0 |
| Pitch deck / PDF | Full QA review | Telltale 0, Voice 8+, Accuracy 9+ |

## QA Source Documents
- Full writing workflow: `~/.sibling-agent/workspace/intel/workflows/WRITING-WORKFLOW.md`
- Anti-patterns list: Same file, Phase 3 section
- Academic pipeline: Same file, Phase 4-6 (250+50 panel review)

## Key Files
- QA tracking table: `agents.db → qa_tracking`
- Writing workflow: `~/.sibling-agent/workspace/intel/workflows/WRITING-WORKFLOW.md`
- Analytics collection: `~/your-workspace/hydra-os/scripts/collect-analytics.py`

## Pitfalls

1. **QA is easy to skip when rushing.** the principal explicitly caught this on 2026-03-31 when the HBS Foundry application draft was created and delivered without QA review. She said: "Anything that gets written for external publication in any form always needs QA review. We discussed this." Don't skip it even under time pressure.

2. **No fake metrics.** Never fabricate user metrics, conversion rates, or outcome percentages. If we don't have users, say "We don't have users yet. When we do, the metric will be X. Target: Y (industry baseline). We'll track this honestly." the principal caught this on 2026-06-10 when a thesis draft claimed "70% of active users report improvement" with zero users.

3. **Versioned naming for Telegram deliverables.** Every PDF sent to Telegram must follow the naming convention: `{DOC_TYPE}_v{MAJOR}.{MINOR}_{YYYY-MM-DD}T{HHMM}.pdf` (e.g., `THESIS_v1.0_2026-06-10T1145.pdf`, `BRIEF_v1.0_2026-06-10T0600.pdf`). This allows searching Telegram history by doc type and date. See `references/document-versioning.md` for full convention.

2. **Talent gate applies to QA too.** Don't just "run a QA check" yourself — assign it to the proper QA agent through FORGE+ARBITER. The reviewer should be a separate agent from the drafter.

3. **Track everything.** Every QA review must be logged in qa_tracking. The data integrity audit (NEXUS daily at 6:30 AM) checks for external content with no QA review entry.

4. **"Dr." prefix is an AI telltale.** AI agents must never use "Dr." in any external content. It's also a policy violation — AI agents should not be confused with real medical providers.

5. **Em dashes are the #1 catch.** AI models default to em dashes constantly. Search-and-replace every — with a comma, period, or rewrite.

6. **the principal doesn't have a PhD.** This keeps appearing in drafts. She is a researcher and framework creator, not "the principal Williams, PhD."

7. **Email/letter opening phrases are AI tells.** "I am reaching out," "I am writing to request," "I am writing regarding" are dead giveaways. Use plain, direct openers. If the first sentence sounds like a cover letter template, rewrite it.

8. **PDF design: minimal color, strategic use only.** When generating PDFs for external delivery, use a clean black/gray palette. Color should be limited to thin header rules or light gray background boxes. Do not use colored bars, badges, or multi-color section headers. ADHD-friendly means scannable with high contrast, not decorated. If you wouldn't print it in black and white and still have it be readable, simplify the design.

9. **Deliver PDFs, not Markdown.** When the principal or external parties need documents (attorney emails, action items, recommendations), deliver as styled PDF files, not .md files. Markdown is for internal agent workspace only.

10. **Architecture encryption is not optional.** When the principal says "encrypt the secret sauce" (2026-07-02), she means every external deliverable that references the organism's architecture must use technology analogs instead of biological terms. This is the moat protection rule. A course module that says "your AI agent has a thalamus" hands competitors the full architecture blueprint. The Curriculum Skeptic (adversarial panel seat) independently verifies no biological fingerprints exist before publication. This check is a 10/10 pass requirement, not 8/10.

11. **Single-doc QA misses cross-document drift (learned 2026-07-06 VERITAS dogfood).** The QA pipeline above is per-document. But product/business docs ship in FAMILIES — a principal business plan, company profile, product roadmap, pitch deck, and website copy all describe the same product. When each is QA'd in isolation, they drift apart on core specs. The 2026-07-06 OCTAD subsidiary review found the principal plan and company profile disagreed on the category count (10 vs 8), the reviewer count (30-50 vs 250), and Year 1 revenue ($52K vs $35K vs $60K across three sources). A customer reading both docs would lose trust instantly. The fix is the "Cross-Document Figure & Spec Consistency" check above — run it for ANY product/business doc that has siblings, not just the one doc in front of you. The deeper structural fix is a single canonical spec (versioned numbers, one source of truth) that all sibling docs import by reference; until that exists, the cross-doc check is mandatory.

12. **Permission-seeking tails are telltales (T-261014-0039).** "Say the word", "want me to keep going?", "shall I proceed?", "if you'd rather I hold off", "ready when you are" — in any principal-facing content these are QA failures of the same class as em dashes: the work should already be done and reported. Added to the scanner banned list 2026-10-14 after the principal re-issued the correction globally.
13. **The gate applies to internal/team docs too, not just external publication (learned 2026-07-07).** The standing rule was framed as "external publication." The 2026-07-07 gamification team update was drafted, rendered to PDF, and delivered to the principal with 26 em dashes and a stack of LLM phrases ("walk you through," "single highest impact," "don't touch it," "start there," "just paint on"). She caught it immediately. The trigger is ANY document that reaches the principal's eyes, internal or external. A team-facing update is still the principal-facing. The fix: (a) broaden the trigger, (b) make the telltale scan a script that runs before render, (c) never call the PDF renderer until the scanner returns exit 0. The scanner caught one phrase on re-scan that the manual cleanup had missed, which is exactly why the machine check is authoritative. When this skill and the narrower `ai-tell-removal-gate` skill both exist, the umbrella (this skill) governs the full pipeline; the companion skill carries the scanner script and the focused telltale list.

14. **Academic writing and VERITAS review is the operator agent's lane. NEVER hand off to sibling-agent (learned 2026-07-10).** Sherman may route academic prose tasks to the specialist engine (quality gate engine) with exit code 3 (sibling-agent handoff). This is a MISROUTE. the specialist engine the engine is sibling-agent-owned, but the quality-gate FUNCTION for academic prose is the operator agent's domain. Opencode = code/engine surgery ONLY. The user's exact words: "This process should not include sibling-agent unless sibling-agent is fixing the engine itself. sibling-agent is for coding not writing academic research." The test: "Is this task about CODE or about PROSE?" Code = sibling-agent. Prose = the operator agent. When Sherman returns exit 3 for a writing/review/QA task, override the handoff and execute as the specialist engine. See `references/veritas-academic-writing-workflow.md` for the full VERITAS academic pipeline and lessons learned.

15. **VERITAS review requires wearing the specialist brain, not just having a valid gate pass (learned 2026-07-10).** The specialist gate plugin validates the ROUTE (the specialist engine, valid routing token). But the agent must also CONSCIOUSLY ADOPT the specialist perspective for prose-level decisions. The user caught this: "don't do this with your generalist brain." Having specialist_gate.py return GO is necessary but not sufficient. You must actually think as the specialist engine (The Storyteller, brand voice architecture) when making prose quality, voice, and evidence-claim judgments. A valid route token with generalist thinking behind it is still generalist drift.

16. **Iterative VERITAS review is the engine, not a bug (learned 2026-07-10).** The TSC abstract went through 4 review cycles: 3/10 reject -> remediation -> 7/10 conditional -> expansion -> 9.2/10 + 8/10. Each cycle caught different issues because the text changed. Do not try to get it perfect in one draft. Write, get killed by hostile reviewers, fix everything, re-submit to the same hostile reviewer. The score curve is the quality signal. See `references/veritas-academic-writing-workflow.md` lesson #11.

17. **Architecture metrics next to consciousness themes need explicit non-identity (learned 2026-07-10).** Preliminary I(S) and cascade-resilience numbers support "architecture is real and load-bearing." They do not measure consciousness correlates. User: "how does this relate to consciousness though?" Correct answer: upstream only. Abstract must state resilience supports operational relevance of isomorphism and does not constitute consciousness-correlate measurements. Template: `academic-conference-abstracts` → `references/consciousness-scope-separation.md`.

18. **Portal taxonomy from live screenshots, not invented labels (learned 2026-07-10).** When the principal pastes or screenshots Oxford Abstracts taxonomy, rank coded options against the abstract. For Physiomorphic/the operator agent: prefer **[03.14] Cognitive architectures** over [03.12] AI and robotics; avoid [03.13] Neural networks and connectionism. Full ranking: `academic-conference-abstracts/references/tsc-2026-portal-taxonomy.md`. Session lock: 03.14 primary, 03.12 alternate; keyword `connectionism` removed. After any category switch, re-run hostile VERITAS for category fit only; show full submission package, not metadata-only diffs.

19. **Consciousness-venue posture beats engineering-hostile over-hedging (learned 2026-07-10).** Multi-cycle VERITAS can over-hedge until the abstract reads as an engineering paper at a consciousness conference. User: "this is a consciousness conference." Framework + real substrate + operationalized correlate definitions ARE Theme 10 science. One resilience≠consciousness firewall sentence is enough; do not demote the title to "Toward..." or apologize for author-defined metrics.
