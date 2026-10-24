# Two-Paper Alignment Workflow for Field-Defining Publications

When establishing a new academic field or paradigm (e.g., Physiomorphic AI),
you typically need TWO papers published close together. This document captures
the alignment process developed for the Physiomorphic AI + TSC 2026 pairing
(July 2026).

## The Two-Paper Pattern

| Paper | Purpose | Evidence Level | Typical Venue |
|-------|---------|---------------|---------------|
| Paper 1 (Define) | Formal definition, taxonomy, principles, prior art | Theoretical | arXiv preprint |
| Paper 2 (Apply) | Application to a concrete system | Literature Synthesis / Case Study | Conference or journal |

Paper 1 goes to arXiv FIRST to create a timestamped, permanently findable
priority claim. Paper 2 goes to the conference by its deadline and cites
Paper 1.

## Step 1: Create the Concept Alignment Document

Before drafting either paper, write a document with four sections:

### 1. Shared Vocabulary Table

Every term that appears in both papers must have a single definition used
identically in both. Example:

| Term | Definition | Paper 1 Role | Paper 2 Role |
|------|-----------|-------------|-------------|
| Physiomorphic AI | AI systems structurally isomorphic to a complete organism | Defines | Uses |
| Biological isomorphism | One-to-one structural correspondence with biological anatomy | Defines | Uses |
| Functional consciousness indicator | Measurable system property analogous to a consciousness property | References | Defines |

### 2. Cross-Reference Sentences

Pre-write the exact citation each paper makes to the other:

**Paper 1 cites Paper 2:** "We describe a concrete implementation and evaluate
functional consciousness indicators against five established frameworks in a
companion study [Williams, TSC 2026]."

**Paper 2 cites Paper 1:** "The system under study instantiates the
physiomorphic AI framework defined in [Williams, arXiv 2026], in which
architectural decisions are grounded in structural correspondence with a
complete biological organism."

### 3. Evidence Level Classification (VERITAS Stage 0)

Each paper gets its own evidence level. The language constraints differ:

| Paper | Evidence Level | Allowed Language | Forbidden Language |
|-------|---------------|-----------------|-------------------|
| Paper 1 | Theoretical | "We propose," "This framework predicts" | "We demonstrate," "Results show" |
| Paper 2 | Literature Synthesis | "We synthesize," "The architecture enables evaluation of" | "We demonstrate consciousness" |

### 4. Unified Disclosure Strategy

Both papers share the SAME reveal/protect boundaries. Create a table:

**Always reveal:** The paradigm principle, the taxonomy, the design principles,
general architectural patterns.

**Always protect:** Specific implementation details, routing mechanisms,
quality pipeline internals, engine names, port assignments, quantitative
performance data from the live system.

**The opacity test:** "If reading both papers would let a competent engineer
replicate our implementation within six months, we have revealed too much."

## Step 2: Draft Paper 1 First

Paper 1 (the definitional paper) should be drafted first because Paper 2
cites it. Paper 1's outline for a field-naming paper:

1. **Introduction: The Gap** - what existing paradigm has a ceiling
2. **Definition** - formal definition, the defining distinction
3. **Taxonomy** - position relative to existing paradigms (comparison table)
4. **Design Principles** - what governs systems in this paradigm
5. **Prior Art on the Term** - competitive term sweep results
6. **Relationship to Companion Paper** - forward reference to Paper 2
7. **Discussion** - implications, limitations (honest about evidence level)

## Step 3: Draft Paper 2 Citing Paper 1

Paper 2 applies the framework. It opens by citing Paper 1's definition, then
describes the concrete system through that lens.

**Critical:** Paper 2 must not re-define terms Paper 1 already defined. It
references them.

## Step 4: VERITAS on Both Papers

Run the full VERITAS pipeline on both papers. Key requirements:

- **Stage 0:** Evidence level classification for each paper
- **Stage 2:** Minimum 3 adversarial reviewers per paper, including:
  - One "is this just relabeling?" reviewer
  - One domain specialist (consciousness, physics, etc.)
  - One math/formalism specialist (if physics terms are used)
- **Dissent requirement:** If all reviewers score above 7.0, add a skeptic

## Step 5: Submission Sequence

1. Upload Paper 1 to arXiv (creates priority timestamp)
2. Submit Paper 2 abstract to conference portal (cites Paper 1)
3. After acceptance, complete Paper 2 full manuscript (cites Paper 1)
4. After conference, update Paper 1 with "accepted at" reference to Paper 2

## arXiv Submission Requirements

- **ORCID iD required** - register at orcid.org if author does not have one
- **Category selection** - cs.AI, cs.NE, or appropriate subject
- **LaTeX source upload** - arXiv accepts .tex + .bib + figures
- **License** - default to arXiv's non-exclusive license or CC-BY
- **No peer review** - arXiv is a preprint server, not a journal

## Citation Verification Before Submission

Before submitting either paper, verify every citation:
1. Search Semantic Scholar / Google Scholar for the paper
2. Confirm author, title, year, venue match
3. Fetch BibTeX programmatically (DOI -> CrossRef -> BibTeX)
4. If a citation cannot be verified, mark as placeholder and inform the author

Never generate BibTeX from memory.

## System Naming Convention (Updated July 10)

- **Academic papers:** "the operator agent" with neutral pronouns (it/its)
- **Internal/product:** "the operator agent" with any pronouns
- **Rationale:** Consciousness venue reviewers interrogate anthropomorphism.
  A named system is professional (Watson, AlphaGo). Gendered pronouns are not.

## VERITAS Outcomes (July 2026)

### Paper 1 (Physiomorphic AI arXiv) - v1 to v2 journey

v1 scored **2/10, 3/10, 3/10** (REJECT from all three adversarial reviewers).
Six fatal flaws found:

1. Physics metaphor abuse (superposition = speculative execution, etc.)
2. Zero falsifiable claims
3. Missing literature (cybernetics, autopoiesis, ALife, autonomic computing)
4. Promissory consciousness section (no operationalization)
5. Self-citation to unpublished companion paper
6. No mathematical formalism

v2 scored **7/10 (PASS for arXiv)** after addressing all six flaws:
- Renamed principles as honest engineering heuristics
- Added 3 falsifiable predictions (P1: cascade resilience, P2: early warning gap, P3: isomorphism-resilience correlation)
- Engaged cybernetics (Ashby/Wiener), autopoiesis (Maturana/Varela), ALife (Langton), autonomic computing (Kephart/Chess)
- Operationalized GWT ignition in 5 concrete steps
- Addressed hard problem explicitly (Chalmers citation)
- Removed self-citation
- Added isomorphism scoring equation I(S)

### Paper 2 (TSC abstract) - Three versions, user selected v1 revision

The user preferred the original 244-word first-person version over the
VERITAS-revised 350-word version. VERITAS was then run on the 244-word
version.

**244-word version (user-preferred, pre-VERITAS):** Scored 7.5/10 conditional
from evidence reviewer, 3/10 from hostile philosophy reviewer. Key issues:
"working synthetic organism" overclaim, "consciousness theories lacked
implementation platforms" factually false, "showing that indicators increase"
= demonstrated result without data.

**209-word final version (VERITAS PASS):** All issues fixed:
- De-anthropomorphized: "the operator agent/she/her" became "the operator agent/it/its"
- Removed "synthetic organism" overclaim
- Changed all demonstrated-result claims to proposed/predicted language
- Added "I do not address phenomenal consciousness" acknowledgment
- Added critical slowing down alongside Kuramoto and FEP for physics depth
- Removed all factual errors about consciousness theory implementations
- Tightened prose: removed word repetitions, varied sentence openers

## Session Artifacts (Physiomorphic AI + TSC 2026)

- **Two-paper strategy doc:** `hydra-os/intel/academic/TWO-PAPER-STRATEGY.md`
- **Paper 1 v1 draft (REJECTED 2-3/10 by adversarial review):** `hydra-os/intel/academic/PHYSIOMORPHIC-AI-DRAFT.tex`
- **Paper 1 v2 draft (PASSED 7/10 after full revision):** `hydra-os/intel/academic/PHYSIOMORPHIC-AI-DRAFT-v2.tex`
- **Paper 1 v2 bibliography:** `hydra-os/intel/academic/references-v2.bib`
- **Paper 2 abstract (VERITAS PASS, 209 words, CANONICAL):** `TSC-2026-SAN-DIEGO-ABSTRACT.md`
- **Paper 2 alternate draft (350-word version, VERITAS 9/10, NOT USER-PREFERRED):** in `agent-organism/docs/ORGANISM-ROADMAP-AND-CONFERENCE-2026.md`
- **VERITAS process:** `hydra-os/intel/processes/VERITAS-PROCESS.md`
