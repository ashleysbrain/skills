---
name: professional-agent-pdf-profiles
description: Generate professional PDF agent profiles using the master HR template. Covers the full pipeline from profile markdown to styled PDF output, plus the multi-agent section fill workflow.
tags: [sibling-agent, agents, pdf, forge, variations, profiles, credentials, master-template]
version: 2.0
---

# Professional Agent PDF Profiles

Use when the principal requests agent persona PDFs, profile documents, formatted master profiles, or any structured handoff that should render with the master template before PDF delivery. This includes simplified executive-friendly methodology summaries when they still need the exact master-template look and section structure, *and* full persona bundles with 17-section profiles, variation registries, elite credential stacks, and personality variants.

This skill also covers multi-agent profile bundles where each persona must be rendered as a complete master-template profile and then merged into one PDF handoff for offline use.

## PDF Generation — THE ONLY APPROVED METHOD

```bash
python3 ~/.sibling-agent/workspace/output/generate-profile-pdf.py \
    /path/to/AGENT-profile.md \
    /tmp/AGENT-profile.pdf
```

**Script:** `~/.sibling-agent/workspace/output/generate-profile-pdf.py`
**CSS source:** Reads inline CSS from `~/.sibling-agent/workspace/output/master-hr-template.html`
**Engine:** weasyprint + pandoc
**Reference PDF:** `~/.sibling-agent/workspace/intel/agents/codes/MASTER-HR-TEMPLATE-REFERENCE.pdf`

the principal confirmed "Yessssss this is the template" on 2026-03-30 after 4 rejections of other tools.

### Design Specs (from master-hr-template.html)
- Header gradient: `#1a1a2e` → `#16213e` → `#0f3460`
- Section border accent: `#e94560` (red)
- Body text: `#1a1a2e`
- Header subtitle: `#a8b2d1`
- Header meta text: `#8892b0`
- Header meta labels: `#ccd6f6`
- TOC links: `#0f3460`
- Table headers: `#1a1a2e` background, white text
- Font: Segoe UI / system-ui, 11px base
- Page: A4, 1.5cm margins
- Badge colors: `#00b894` (active), `#e94560` (template)

### Batch Generation
```bash
cd ~/.sibling-agent/workspace/output
for f in ../intel/agents/codes/*-profile.md; do
    name=$(basename "$f" -profile.md)
    python3 generate-profile-pdf.py "$f" "/tmp/${name}-profile.pdf"
done
```

### Bundle Delivery for Multi-Agent Panels
When the user wants several personas delivered as one offline packet:
1. Generate each full profile PDF separately.
2. Merge them into one bundle PDF in panel order.
3. Verify the bundle by rendering at least the first page and one interior page from a later profile.
4. Confirm the rendered pages show the master template header, the correct section structure, and no clipping in long tables or variation blocks.

### REJECTED TOOLS — DO NOT USE
| Tool | the principal's Response | Date |
|------|-------------------|------|
| `md-to-pdf.py` (fpdf2) | "This is markdown pdf" | 2026-03-30 |
| `generate-agent-profile-pdf.py` (custom weasyprint) | "This isn't the right design or format" | 2026-03-30 |
| `md-to-pdf` npm + `adhd-pdf.css` | "This works for now but this isn't the same format" | 2026-03-30 |
| `md-to-pdf` npm + Qubit Brand V3.0 CSS | "This isn't the template I like" | 2026-03-30 |
| `generate-profiles.py` (old weasyprint) | Wrong cover design, different color scheme | 2026-03-30 |

## Profile Structure — MASTER-HR-TEMPLATE (17 Sections)

Template: `~/.sibling-agent/workspace/intel/agents/codes/MASTER-HR-TEMPLATE.md` (981 lines, 41KB)

### Section Ownership (Phase 2 Specialist Fill)
| Section | Owner | What |
|---------|-------|------|
| S1 Agent Overview | FORGE | Employee#, job codes, reporting chain |
| S2 Job Description | FORGE | GENERAL role info, NOT agent-specific |
| S3 Variation Registry | FORGE | 10-variation table |
| S4 Variation Profiles | FORGE | Full task lists for ALL 10 personas |
| S5 8D Wellness | VITALS | 8D scores, TWC, SAS, Protocol v2 |
| S6 Score History | METRICS | Rolling 90-day scores |
| S7 Fleet Gap Analysis | SCOUT | Why agent exists, what breaks without them |
| S8 Team Compatibility | CATALYST | Cross-agent interaction ratings |
| S9 Core Functions | ARBITER | Capacity allocation table (must total 100%) |
| S10 30-Day Onboarding | CATALYST | Week-by-week deliverables |
| S11 Deployment Spec | FORGE | Model config, escalation triggers |
| S12 Journal Integration | SENTINEL | Journal format, compliance |
| S13 Version Tracking | FORGE | Changelog |
| S14 Analytics Tracking | METRICS | Variation performance table |
| S15 Switching Protocol | FORGE | Trigger-to-variation mapping |
| S16 Scientific Validation | HALO | Research citations |
| S17 Appendices | NEBULA | Reference docs, final QA |

### Two Profile Tiers
- **Core ops agents (59):** Full 17-section MASTER-HR-TEMPLATE
- **VERITAS reviewers (99):** Lighter 10-section VERITAS-REVIEWER-TEMPLATE

## Critical Content Rules

0. **Never deliver a draft as the final profile.** If the principal says a profile is incomplete, regenerate or replace it with the full master version before PDF delivery. Verify the markdown contains the complete section set expected for that profile tier.
1. **S2 Job Description = GENERAL role info.** Not agent-specific. What this ROLE does, not what this instance does. the principal flagged 2026-03-30.
2. **S4 needs FULL task lists for all 10 personas.** Not 3-5 items. Comprehensive potential tasks per persona. the principal: "All agents need potential tasks for all 10 personas. Not just a handful."
3. **Agent scope boundaries matter.** AISHA-MD is ONLY for the principal's personal health. She is NOT responsible for fleet wellness (that's AISHA/the operator agent). She convenes panels with research agents (HALO, DARK-MATTER, AURORA) to verify science/math. the principal corrected this 2026-03-30.
4. **VERITAS reviewer names must include "AI".** "Dr. Alexander Petrov AI", "Cognitive Science AI Reviewer". No human-sounding names.
5. **AI telltale audit before external content.** Zero em dashes, zero AI patterns.
6. **Subagent batching:** 6 agents per subagent max for profile creation. Larger batches time out.
7. **Cross-reference drift:** When any agent's role changes, grep all profiles for their name and update collaboration sections.
8. **Credential completeness:** For full-profile PDFs, include explicit professional and educational credential sections even when the credentials are internal/role-relevant rather than external degrees.
9. **Model policy enforcement:** If the user says the fleet should avoid Anthropic, update both the profile markdown and the DB-backed model fields before rendering the PDF.
10. **Canonical template alignment:** If the user says the profile should match the Talent Gate / master template more closely, compare against the canonical template and the live DB first instead of freehand rewriting. Use `references/master-template-alignment.md` as the checklist for visible credentials, model sync, and PDF verification.
11. **Agent personas are versioned, not public figure mirrors.** Do not create profiles that mirror public figures (Grant, Deci/Ryan, Prochaska, etc.). Instead: versioned personas with internal credential stacks (PhD-equivalent, board-certified supervisor, 15+ years research synthesis), embedded frameworks (ACRF, RECF, TFACF, GAF, SMIF, CEC), and explicit versioning protocol (Major/Minor/Patch). Each version is a complete, self-contained artifact supporting A/B testing and atomic rollback. See DS HELM SOUL.md Sections 2, 5, 18, 19 for reference implementation. (2026-06-10)

## Model & Credential Policy Addendum

- The profile PDF should reflect the current operating policy, not a stale model line copied from an old draft.
- If no external human credentials are known, write internal/auditable credentials rather than inventing universities or certifications.
- Keep professional credentials and educational credentials in separate sections so reviewers can audit them independently.
- Verify the rendered PDF contains both sections and the intended model line before delivery.

## PDF for Non-Profile Documents (Plans, Reports, etc.)

The `generate-profile-pdf.py` script is designed primarily for agent profile markdown because it parses profile-specific metadata. For general documents (plans, reports, research), use `md-to-pdf` npm with extracted master template CSS.

```bash
# Save the CSS below to /tmp/plan-styles.css (or a permanent location)
# Then run:
md-to-pdf DOCUMENT.md \
    --stylesheet /tmp/plan-styles.css \
    --pdf-options '{"format":"A4","margin":{"top":"1.5cm","bottom":"1.5cm","left":"1.5cm","right":"1.5cm"},"printBackground":true}'
```

**Important exception:** if the document is intentionally being rendered as a master-template handoff and you can provide profile-style metadata (`Employee`, `Role`, `Domain`, `Model`, `Status`, `Empire Blueprint Version`, `Protocol Version`) plus `## Section N` headings, `generate-profile-pdf.py` can still be used successfully even for a plain-language methodology explainer. That is the right choice when the user wants the exact master-template styling and a structured narrative instead of a generic report layout.

The CSS must match the master template colors (#1a1a2e headers, #e94560 section borders, #1a1a2e table headers with white text, Segoe UI 11px). A matching CSS file exists at `/tmp/plan-styles.css` (recreate from the skill if missing — copy the style block from master-hr-template.html and simplify for non-profile docs).

**Pitfall:** verify where the markdown file actually landed before rendering. In this workspace, relative file writes can end up under a nested workspace path, so use `search_files` or absolute paths if the PDF command says the file is missing.

**Proven 2026-03-30:** Scheduling plans, XP reviews, partner briefings, database schemas, and security reports all rendered correctly with md-to-pdf + plan-styles.css. The profile generator produced 6KB from an 893-line doc because it couldn't parse non-profile metadata — always use md-to-pdf npm for non-profile documents unless you are deliberately using the master-template exception above.

This was discovered 2026-03-30 when the profile generator produced a 6KB HTML from an 893-line scheduling plan — it dropped all content because it couldn't parse profile metadata fields.

## Key Files
- **Master template:** `intel/agents/codes/MASTER-HR-TEMPLATE.md`
- **PDF generator:** `output/generate-profile-pdf.py`
- **HTML CSS source:** `output/master-hr-template.html`
- **Reference PDF:** `intel/agents/codes/MASTER-HR-TEMPLATE-REFERENCE.pdf`
- **Reviewer template:** `intel/agents/codes/VERITAS-REVIEWER-TEMPLATE.md`
- **FORGE variation template:** `intel/agents/codes/FORGE-10-variations.md`
- **All profiles:** `intel/agents/codes/[NAME]-profile.md`
- **Database:** `intel/agents/database/agents.db`
- **Document versioning convention:** `skills-library/software-development/coaching-engine-spec-maintenance/references/document-versioning-convention.md`

All paths relative to `~/.sibling-agent/workspace/`.
