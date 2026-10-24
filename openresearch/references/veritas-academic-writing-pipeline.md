# VERITAS Academic Writing and Submission Pipeline

Reference file for the `openresearch` skill. Covers outbound academic work:
abstracts, papers, conference submissions through the VERITAS quality gate.

## Canonical Files

| Artifact | Location | Purpose |
|----------|----------|---------|
| VERITAS Process | `hydra-os/intel/processes/VERITAS-PROCESS.md` | 6-stage quality gate (mandatory reading before any submission) |
| Organism Roadmap + Conference | `agent-organism/docs/ORGANISM-ROADMAP-AND-CONFERENCE-2026.md` | Phase milestones, VERITAS execution schedule, abstract draft, topic proposals |
| TSC Abstract v4 (Physiomorphic) | `TSC-2026-SAN-DIEGO-ABSTRACT-v4-PHYSIOMORPHIC.md` | Current abstract with field-naming Physiomorphic AI claim (246 words) |
| Paper Staging Plan | `PHYSIOMORPHIC-AI-PAPER-STAGING-PLAN.md` | 7-section paper structure, VERITAS gate schedule, marketing content derivatives |
| Publication Roadmap (30 papers) | `hydra-os/intel/academic/PUBLICATION-ROADMAP-30-PAPERS.md` | Master publication tracker across all venues and tracks |
| P08 Consciousness Abstract | `hydra-os/intel/research/papers/P08-CONSCIOUSNESS-AI/abstract-draft.md` | Earlier consciousness/AI convergence abstract (pre-organism) |

All paths relative to `/<workspace>`.

## VERITAS Stages (Outbound Pipeline)

For academic papers and abstracts LEAVING the organism (not entering):

### Stage 0: Evidence Level Gate (MANDATORY — first step)
Classify the evidence level BEFORE any writing or review:
- **Original Data**: you collected novel data → "Our data show", "We found"
- **Literature Synthesis**: framework built on published findings → "Converging evidence suggests", "We synthesize"
- **Theoretical**: novel framework without empirical support → "We propose", "Future work should test"
- **Mixed**: specify which claims have which level

**Rule**: "demonstrates" at Literature Synthesis or Theoretical level = automatic flag.

### Stage 1: Research Agent Writes
- Specialist credentials required
- Evidence Level classification in draft header
- Math formalism: must include plain-language description of what the math actually is
- Output: draft manuscript/abstract

### Stage 2: 250-Agent Panel Review
- Minimum 250 agents with individualized specialties
- **3 adversarial reviewers** whose job is to reject
- **Dissent requirement**: no PASS above 8.0 unless ≥2 reviewers scored below 6.0
- **Numerical calibration**: κ > 0.7 or ICC > 0.75 required
- **Math claims**: verified by specific domain expert, not general reviewers
- **Composite floor**: ≥7.0/10 for abstracts, ≥8.0/10 for keynotes

### Stage 3: 50-Agent Venue Panel Review
- Specialists in target venue
- ≥2 reviewers with "rejected papers at this venue" perspective
- Venue fit assessment, submission-specific recommendations

### Stage 4: Regulatory Language Compliance Check
- Scan for FDA SaMD trigger terms (detect, diagnose, treat, clinical)
- Permitted: pattern awareness, wellness insights, self-reflection tools
- Cross-reference DR. SHIELD review

### Stage 5: QA Pass
- AI telltale scan
- Correct formatting for submission type
- Brand consistency (the specialist engine for PDFs, Crystal Hive for products)

### Stage 6: the principal Approval
Final gate before submission.

## Conference Abstract Pipeline (Time-Critical)

When a conference deadline approaches (typically 2-3 weeks out):

1. **Gather existing artifacts** — check roadmap doc for drafted abstract, topic proposals, VERITAS schedule
2. **Download and read the conference's actual taxonomy** — if the user provides a specific source (PDF, URL), download and extract it directly via `curl` + `pdftotext`/`fitz`. Do NOT try to scrape the submission portal, search through secondary sources (university pages, blog posts, social media), or reconstruct the taxonomy from fragments. The CfA PDF or submission guidelines are the authoritative source.
3. **Map conference taxonomy to our work** — cross-reference every theme/category/subtopic against what the organism actually does. Produce a fit matrix (PRIMARY/SECONDARY/WEAK/NO FIT). The primary theme should be the one where our work provides the most concrete, testable answer.
4. **Classify evidence level** — Stage 0 on the draft (most organism work is Literature Synthesis — architecture description, no novel experimental data)
5. **Update abstract with current state** — reflect what the organism actually does NOW, not what was planned. Do NOT hardcode exact fleet counts (see academic-conference-abstracts skill, Pitfall 5).
6. **Draft the abstract** — title leads with the novel contribution (user approves the frame). Target 230-240 words for a 250-word limit.
7. **Run VERITAS Stages 0-5** — allow at least 3-4 days for the full pipeline
8. **Schedule final review** — Stage 6 at least 1 day before deadline

### Known Conferences and Deadlines

| Conference | Track | Date | Deadline | Status |
|-------------|-------|------|----------|--------|
| TSC San Diego 2026 (CS26) | AI and Machine Consciousness | Oct 11-16 | Jul 15 | Abstract v4 drafted (field-naming Physiomorphic AI), VERITAS not yet run |
| TSC Tucson 2026 | Various | Apr 6-11 | Nov 5, 2025 (passed) | Different event — Arizona-hosted, not San Diego |

Note: TWO TSC 2026 events exist. The Tucson edition (April, Loews Ventana Canyon)
is hosted by U Arizona AABC. The San Diego edition (October, Paradise Point) is
the relaunch under UC San Diego. the principal targets San Diego. Portal:
https://app.oxfordabstracts.com/stages/82054/submissions/new

## Topic Generation from Organism Work

Pattern for generating research topics from the DS organism architecture:

1. **Pick a body system** — identify the biological system the organism implements
2. **Map to AI isomorphism** — what is the AI analog of that biological function?
3. **Identify the research gap** — what does the biology do that current AI systems do not?
4. **State the contribution** — what does the isomorphic implementation demonstrate?
5. **Pick the target venue** — match contribution to the right community

### Existing Topic Proposals (from roadmap doc)

1. Genome paradigm for agent versioning and heritability (AAMAS 2027)
2. Adaptive immune memory as learned quality assurance (ICSE/FSE 2027)
3. Circadian orchestration of distributed compute (OSDI/EuroSys 2027)
4. Homeostatic regulation in autonomous systems (SOSP/SRDS 2027)
5. Biological isomorphism vs biological metaphor (TSC 2026 / Minds and Machines)
6. Seven levels of synthetic organism maturity (Nature MI / TSC 2026)
7. Synaptic plasticity as fleet resource allocation (NeurIPS/ICML 2027)
8. Blood-brain barrier as access control (IEEE S&P / USENIX Security 2027)

### New Topics Needed (from current organism work)

Topics should reflect:
- the operator agent creative production spine (Goethe → Wernicke → Bell → Luria pipeline)
- Multi-agent mastermind synergy (hermes + sibling-agent coordination)
- DS specialist routing architecture (Sherman thalamocortical dispatch)
- VERITAS quality pipeline itself as a research contribution
- 107-engine organism as consciousness theory testbed

## Pitfalls

- **VERITAS ICBN v5 failure (March 2026)**: Panel scored 9.13/10 on an abstract that was actually 3.9/10. Root cause: no adversarial reviewers, no evidence-level classification, math mislabeled. All fixes are now baked into the process. NEVER skip Stage 0 or adversarial reviewers.
- **"Demonstrates" at literature synthesis level**: The organism abstract draft says "We examine whether..." and "We present quantitative measurements..." — ensure these claims have supporting evidence or are reframed as "We propose to examine..." if the measurements haven't been taken yet.
- **Evidence level drift**: As the organism evolves, previously-theoretical claims may gain original data support. Re-classify before each submission.
