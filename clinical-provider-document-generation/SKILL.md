---
name: clinical-provider-document-generation
description: Generate clinical provider documents from proprietary health scoring data for healthcare appointments. Covers multi-specialist algorithm audit, product positioning as clinical decision-support tool, patient data integration, and PDF delivery.
category: operations
version: 1.0
---

# Clinical Provider Document Generation

Produce healthcare-provider-ready documents that explain Divinity Science scoring methodology, present patient data with clinical context, and position the scoring system as a clinical decision-support product.

## When to Use
- Preparing for a healthcare provider appointment (ADHD, psych, PCP, specialist)
- User needs a document explaining their scoring methodology to a new or existing provider
- User needs multi-specialist audit of a health scoring algorithm (clinical, mathematical, pharmacological)
- User needs to position a scoring product for clinical/professional use
- Generating follow-up score reports for providers between appointments
- Creating condition-specific clinical briefs (ADHD, BP2, sexual health, nutrition, etc.)

## Procedure

### 1. Gather All Algorithm Code and Current Data
Read the relevant scoring engine files before writing anything:
- ADHD Daily Engine: `~/your-workspace/hydra-os/intel/health-private-plans/ADHD-SUBSCORE-DAILY-ENGINE.py`
- ADHD Fusion: `~/your-workspace/hydra-os/products/principal-8d-tracker/adhd_fusion.py`
- Support Subscores: `~/your-workspace/hydra-os/products/principal-8d-tracker/support_subscores.py`
- EF Tracker: `~/your-workspace/health-private/ef-panel/ef_tracker.py`
- TWC Scoring: Load skill `proprietary-twc-scoring` for formula reference
- Patient health profile: `~/your-workspace/health-private/principal-health-profile.md`
- Current scores: Query `ashley_unified_health.db` and `ashley_ef_tracker.db`

### 2. Multi-Specialist Algorithm Audit
Run three audit perspectives on the algorithms before writing the document:

**Clinical Neuropsychology (PhD-level review):**
- Map each domain to DSM-5-TR criteria
- Evaluate behavioral proxy validity per domain
- Check profile adaptation for clinical soundness
- Identify missing measurement dimensions per current research
- Compare against established instruments (Barkley EF, Brown ADD, CAARS, CPT)

**Mathematical Rigor:**
- Verify formula correctness and edge cases
- Check weight normalization convergence
- Evaluate confidence model linearity assumptions
- Analyze fusion formula appropriateness (fixed vs adaptive)
- Identify double-counting risks in cascade scoring
- Check EWMA smoothing parameters for optimal temporal resolution

**Psychopharmacology / Psychiatry:**
- Evaluate medication response modeling (stimulant PK curves)
- Check comorbidity confounds (ADHD vs BP2 emotion regulation)
- Assess scoring granularity for detecting dosage changes
- Review check-in question clinical appropriateness
- Evaluate diagnostic modifier calibration

### 3. Structure the Clinical Document
Required sections in order:
1. **What This Document Is** — product positioning as clinical decision-support, NOT diagnostic instrument
2. **System Architecture Overview** — layer diagram (condition engine → support subscore → TWC fusion)
3. **Condition-Specific Engine** — all domains with formulas, DSM alignment, behavioral proxies, profile adaptation
4. **Support Subscore Integration** — scoring modes (passive/proxy/direct), dimension impact map, anti-double-counting
5. **TWC Fusion** — blend formula with clinical rationale for weighting
6. **Parallel Systems** (EF COMPASS, etc.) — diagnostic modifiers with clinical justification
7. **Confidence Model** — transparency about score reliability
8. **Current Patient Data** — live scores with visual bar charts, clinical signal interpretation
9. **Methodology Audit Notes** — known limitations and planned improvements (shows rigor to providers)
10. **References** — peer-reviewed citations (2023+ preferred)
11. **Document Control** — system version, schema, data storage classification, developer

### 4. Writing Standards for Clinical Documents
- **No AI telltales** — follow AGENTS.md writing standards (no em-dashes, no "Furthermore/Moreover")
- **Precise clinical language** — use DSM-5-TR terminology, avoid colloquial descriptions
- **Product-positioned** — frame as a clinical decision-support tool that could serve other patients
- **Provider-friendly** — assume the reader has zero context about Divinity Science
- **Transparent about limitations** — explicitly state what the system does NOT do
- **Include "Not a diagnostic instrument" disclaimer** — every document must carry this
- **Use contractions, vary sentence length** — conversational but professional
- **Tables over prose for data** — providers scan, they don't read

### 5. Patient Data Presentation
- Always query live data from SQLite databases (never stale numbers)
- Present domain scores with visual bar charts (Unicode block characters)
- Include 30-day trends when available (mean, range, days)
- Flag the primary clinical signal (which domain is floor/ceiling)
- Provide clinical interpretation of the pattern (not just numbers)
- Include current medications and pharmacokinetic context

### 6. PDF Generation Pipeline
```bash
# Step 1: Write markdown document
# Step 2: Generate styled HTML with pandoc
pandoc "INPUT.md" -t html5 --standalone --embed-resources \
  --css=/tmp/clinical_style.html \
  --metadata title="TITLE" \
  -o /tmp/clinical_styled.html

# Step 3: Convert HTML to PDF with weasyprint
weasyprint /tmp/clinical_styled.html "OUTPUT.pdf"
```

**Style template** — create a CSS file with:
- `@page { size: letter; margin: 0.85in; }`
- Dark headers, clean sans-serif body font
- Monospace for code/formulas
- Alternating row colors for tables
- Border-bottom separators for h1/h2

**Fallback note:** xelatex/pdflatex are NOT installed. Always use pandoc→html→weasyprint pipeline. Never attempt pdflatex directly.

### 7. Deliver
- Save PDF to `~/your-workspace/health-private/`
- Send via MEDIA: path in response
- Offer to send via Telegram or iMessage if needed for the appointment

## Specialist Agent Delegation
When OpenRouter credits are available, spawn specialist review agents via `delegate_task`:
- Use `google/gemini-2.5-pro` via OpenRouter for all specialist agents
- Give each agent a full persona (credentials, institution, expertise)
- Provide complete algorithm code in the task context
- Request structured output with specific sections
- Each agent needs `web` toolset for literature research

**When OpenRouter is depleted (learned 2026-05-27):**
- Run all three specialist reviews directly in the main session
- Use established scientific knowledge from algorithm code and calibration files
- Reference known literature (Barkley, Brown, DSM-5-TR, Bijlenga, Surman, Rozatkar)
- Still produce the full audit — do NOT skip or abbreviate

## Key Files
- Output directory: `~/your-workspace/health-private/`
- Naming: `DS-{CONDITION}-Clinical-Provider-Document.{md,pdf}`
- ADHD engine: `~/your-workspace/hydra-os/intel/health-private-plans/ADHD-SUBSCORE-DAILY-ENGINE.py`
- ADHD fusion: `~/your-workspace/hydra-os/products/principal-8d-tracker/adhd_fusion.py`
- Support subscores: `~/your-workspace/hydra-os/products/principal-8d-tracker/support_subscores.py`
- EF tracker: `~/your-workspace/health-private/ef-panel/ef_tracker.py`
- EF Compass table is in `ashley_unified_health.db` (table `ef_compass_daily`), NOT in `ashley_ef_tracker.db` (that DB exists but is empty)
- Unified health DB: `~/your-workspace/health-private/ashley_unified_health.db`
- EF tracker DB: `~/your-workspace/health-private/ef-panel/ashley_ef_tracker.db` (DEPRECATED — do not use for queries, use ashley_unified_health.db instead)

## Document Split Patterns

### Two-Document Split (standard)

When the user asks for separate documents (learned 2026-05-27), produce two distinct deliverables:

**Document 1: Scoring Methodology Reference** (`DS-{CONDITION}-Scoring-Methodology.{md,pdf}`)
- No patient data — purely explains how the system works
- Reusable across appointments and providers
- Sections: architecture overview, domain definitions with weights, behavioral proxies, profile personalization, scoring modes, confidence model, output types, limitations, references
- Tone: "Quick reference" style — tables over prose, visual diagrams for architecture
- Designed to be read and understood in under 5 minutes

**Document 2: Patient Scoring Report** (`DS-{CONDITION}-Patient-Scoring-Report.{md,pdf}`)
- Only live data — no methodology explanation (that's Document 1's job)
- Per-appointment, regenerates each time from live DB queries
- Sections: TWC summary with trend, 8D scores with visual bars, EF COMPASS with Natural vs Actual (gap analysis), sub-component scores (nutrition, sexual health), key patterns/signals, data quality notes
- Include 30-day trend tables when data available
- Always include: current vs Flourishing-day comparison, primary clinical signal callout
- Flag data quality (how many days have full scores vs gaps)

**Why split:** Providers keep the methodology doc as a standing reference and only need fresh scoring data per visit. The methodology doc can also be shared with other providers without exposing patient data.

### Three-Document Split (multi-provider appointment)

When the user is seeing multiple provider types or wants documents tailored to different clinical audiences (learned 2026-05-28), produce three deliverables:

**Document 1: TWC & Sub-Algorithm Overview** (`DS-TWC-Clinical-Provider-Overview.{md,pdf}`)
- Audience: PCP, prescriber, NP — any provider who needs to understand the scoring system at a high level
- No patient data — purely methodology
- Accessible language, avoid deep math
- Covers: 8 dimensions, 3 scoring layers, coupling matrix, sub-component modifiers, score labels, how to use the data clinically, references
- Goal: Read in under 5 minutes, understand what the numbers mean and how to use them

**Document 2: Condition-Specific Algorithm Deep Dive** (`DS-{CONDITION}-Algorithm-Deep-Dive.{md,pdf}`)
- Audience: Psychologist, psychotherapist, neuropsychologist — provider who needs the math and clinical validity
- No patient data — purely methodology at specialist level
- Covers: all domains with DSM-5-TR alignment, passive metrics, sigmoid response curves, medication PK modeling, comorbidity differentiation (e.g., ADHD vs BP2), double-counting prevention, confidence model, known limitations, extensive references
- Include formulas, parameter tables, and calibration rationale
- Goal: Specialist can evaluate the methodology's clinical soundness

**Document 3: Patient Scoring Report** (same as two-document split's Document 2)

**Why three:** Different providers need different depth. A PCP prescribing stimulants needs the overview. A therapist doing CBT needs the deep dive on EF domains and behavioral proxies. Both need the patient data report. The split also lets the patient hand the overview to any future provider without the deep-dive overwhelming them.

## Health Evidence Synthesis as a Product Family

When a research or methodology skill is being adapted into a health-facing product, split it into three reusable modes instead of one overloaded skill:

1. **Health Methodology Review and Consolidation** - the public core. Review health research, drafts, and protocols, then convert them into a bounded, implementation-ready, non-diagnostic health spec.
2. **Health Pattern Review for Patient 0** - personal health signals, journals, transcripts, and wearable trends. Summarize patterns and confounders without diagnosing.
3. **Provider-Ready Health Brief Builder** - turn health evidence into a concise provider handoff with facts, confidence, limitations, and clinician questions.

Use explicit claim-status labels for incomplete evidence: validated, supported but incomplete, hypothesis, provisional, must not ship.

See [references/health-evidence-synthesis-patterns.md](references/health-evidence-synthesis-patterns.md) for the conversion rubric and claim-status labels.

## Database Schema Reference (ashley_unified_health.db)

Key column names that differ from what you might expect:
- `daily_scorecard.int_score` — NOT `intel_dim` or `int`
- `daily_scorecard.ef_compass_overall` — overall EF score
- `ef_compass_daily` — has both `_natural` (pre-modifier) and actual columns for each domain
- `ef_compass_daily.{domain}_natural` — natural capacity before diagnostic modifier
- `ef_compass_daily` columns: date, activation, focus, effort, emotion, memory, action, self_monitoring, activation_natural, focus_natural, effort_natural, emotion_natural, memory_natural, action_natural, self_monitoring_natural, compass_overall, evidence_count_total, created_at
- `twc_history` — separate table with TWC + momentum + label per date
- Many days have NULL TWC/scores — always handle None in formatting

## Pitfalls
- NEVER present scoring as a validated diagnostic instrument
- NEVER use stale/cached scores — always query live DB data
- NEVER include API keys, tokens, or credentials in clinical documents
- NEVER skip the multi-specialist audit — providers respect rigor
- NEVER assume the provider knows anything about Divinity Science
- NEVER use xelatex/pdflatex for PDF generation — not installed, will fail
- NEVER let OpenRouter depletion block document delivery — do the work directly
- NEVER put patient data in the methodology document or methodology in the patient report
- ALWAYS include "Not a diagnostic instrument" disclaimer
- ALWAYS include peer-reviewed references
- ALWAYS save both .md source and .pdf output
- ALWAYS handle NULL values in DB queries — many days have sparse data
