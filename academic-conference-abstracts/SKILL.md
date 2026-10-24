---
name: academic-conference-abstracts
description: Draft and submit word-limited abstracts to academic conferences.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes:
    tags: [Academic, Conference, Abstract, Submission, TSC, Interdisciplinary]
    category: research
    related_skills: [ml-paper-writing, openresearch, ds-genome-transcription]
---

# Academic Conference Abstract Submission Skill

Draft and submit short (150-300 word) abstracts to academic conferences through
portal systems (Oxford Abstracts, EasyChair, CMT, etc.). Covers venue taxonomy
mapping, category selection, word-count discipline, and the full submission
workflow for interdisciplinary venues outside the standard ML conference circuit.

## When to Use

- Drafting a word-limited abstract for an academic conference submission
- Mapping a venue's Call for Abstracts taxonomy against what you are building
- Selecting the right category/theme in a conference portal
- Managing the submission checklist for a portal-based system

## When NOT to Use

- Full paper writing with page limits, LaTeX templates, citation workflows (use `ml-paper-writing`)
- Research paper structuring for CS venues with double-blind review (use `ml-paper-writing`)
- Grant proposals or fellowship applications (separate workflow)

## How to Run

1. **Find the primary source.** Get the Call for Abstracts PDF or page directly. See Pitfall #1.
2. **Extract the taxonomy.** Categories, themes, sub-topics, word limit, deadline.
3. **Verify the deadline against the live portal.** See Pitfall #2.
4. **Map the taxonomy against what you are building.** Category fit first, then theme fit. See Procedure.
5. **Draft the abstract.** Ground in the actual architecture/product, not aspiration. Track word count.
6. **Present title + category + themes + word count** for user approval.
7. **Run the submission checklist.** See Quick Reference.

## Quick Reference

```
Abstract Submission Checklist:
- [ ] Call for Abstracts PDF downloaded and taxonomy extracted
- [ ] Deadline verified against live portal (NOT the PDF date)
- [ ] Category selected (from the portal dropdown options)
- [ ] Primary theme selected
- [ ] Secondary theme selected (if applicable)
- [ ] Title entered (leads with the novel contribution)
- [ ] Abstract pasted (within word limit, verified with wc -w)
- [ ] Keywords entered
- [ ] Author information added
- [ ] Presentation preference selected (oral / poster / either)
- [ ] Submitted before deadline
```

### Presentation-format decision rule

Treat oral, poster, and either as strategic format choices, not as judgments of whether the research is "good enough."

1. Verify the live portal's exact options and whether "either" permits oral consideration with poster reassignment. Do not assume every conference handles fallback identically.
2. Recommend **oral** when the abstract supports a clear short-talk narrative: problem, contribution, method, result or test plan, and significance.
3. Recommend **poster** when the work depends on dense diagrams, exploratory discussion, or many implementation details that benefit from extended one-to-one explanation.
4. Recommend **either with oral preferred** when that option preserves eligibility for a talk without blocking poster consideration.
5. If the portal requires one choice and a field-defining abstract has a coherent narrative plus defensible evidence or falsifiability, choose **oral**. Applying for an oral slot does not claim the research is complete.
6. For a new field or paradigm, weigh authorship and category-establishment value. An oral talk gives the originator a stronger venue to define the term in their own voice.

For the TSC Physiomorphic AI submission, the oral case is supported by a complete narrative: the neuromorphic/physiomorphic distinction, the operator agent architecture, physics-informed mechanisms, preliminary isomorphism and resilience results, and a falsifiable prediction. If the portal offers "either," select it with oral preferred; if only one format can be chosen, select oral.

## Procedure

### Step 1: Primary Source First

Download the Call for Abstracts PDF directly from the conference website. Do not
hunt through secondary sources (conference blog posts, university pages, social
media announcements) looking for the taxonomy. The CfA PDF is the authoritative
source for categories, themes, word limits, and submission guidelines.

```bash
# Download the CfA PDF directly
curl -L -o /tmp/cfa.pdf "https://conference-site.edu/call-for-abstracts.pdf"

# Extract text
python3 -c "
import subprocess, sys
result = subprocess.run(['pdftotext', '/tmp/cfa.pdf', '-'], capture_output=True, text=True)
print(result.stdout)
" 2>/dev/null || python3 -c "
import fitz
doc = fitz.open('/tmp/cfa.pdf')
for page in doc:
    print(page.get_text())
"
```

If `web_extract` fails on the PDF URL, use `curl` to download and `pdftotext` or
`pymupdf` (`fitz`) to extract. The PDF is the ground truth, not the website HTML.

### Step 2: Taxonomy Extraction

Record the taxonomy in a structured format:

| Element | What to Capture | Example |
|---------|-----------------|---------|
| Categories | Top-level dropdown options in portal | Physical & Biological Sciences, Philosophy, Cog Sci |
| Themes | Numbered sub-topics in the CfA | "7: Can AI be conscious?" |
| Word limit | Maximum abstract length | 250 words |
| Deadline | Submission cutoff | July 15, 2026 |
| Portal URL | Submission system link | Oxford Abstracts instance |

### Step 3: Map Taxonomy Against Reality

**Source of truth is the LIVE portal dropdown (and user screenshots), not
guessed free-text categories.** When the user sends taxonomy screenshots,
vision-read every coded option and rank against the abstract. CfA PDFs may
list themes only; Oxford Abstracts uses numbered codes like [03.14].

Map against what you are ACTUALLY building. Rate each option:

- **PRIMARY** — work directly is this class of contribution
- **SECONDARY** — tangential
- **WEAK** — touch only
- **NO FIT** — discard (connectionism/PDP unless truly learned weights)

Select ONE portal taxonomy code. Themes (when separate): primary = what you
deliver; secondary = what motivates. Do not stretch a weak fit.

**TSC 2026 live ranking for Physiomorphic/the operator agent (screenshots 2026-07-10):**
1. **[03.14] Cognitive architectures** — best (architecture paper)
2. [03.12] Artificial intelligence and robotics — safe broad
3. [04.05] Emergence, nonlinear dynamics and complexity — physics home
Avoid [03.13] Neural networks and connectionism. Full tree:
`references/tsc-2026-portal-taxonomy.md`.

**User lock (2026-07-10):** After comparing all portal screenshots, the principal
locked **03.14 primary, 03.12 alternate**. Keywords: `cognitive architecture`
in, `connectionism` out. Abstract body already matched cognitive-architecture
framing ("biologically-grounded multi-agent architecture") — no body rewrite
required for the taxonomy lock. When categories change: update portal fields +
keywords + checklist in the same turn, then show the **full consolidated
package** (title, taxonomy, themes, abstract, keywords, word count, portal URL),
not a metadata-only diff.

### Step 4: Draft the Abstract

Ground the abstract in the actual system architecture. Read the architecture
docs, the fleet registry, the product specs. Every claim must trace to a real
artifact.

**Four-paragraph structure (scales to 250 words):**

| Paragraph | Job |
|-----------|-----|
| 1 | System description: what it is, the methodological approach |
| 2 | Mechanisms: the specific mathematical/scientific models in use |
| 3 | Measurement: how you quantify the claims (framework, indicators) |
| 4 | Reframe: why this matters to the field (not restating paragraph 1) |

**Title leads with the novel contribution.** The user prioritizes the novel
methodological angle (e.g., "biological isomorphism") over the measurement angle
(e.g., "functional indicators"). The title tells reviewers what is NEW.

### Step 5: Word Count Discipline

Track word count with `wc -w` after every edit. Typical limits are 200-300 words
(TSC 2026 portal limit = 500). **Maintain an 8-10 word safety margin** — portal
counters tokenize differently than `wc`. See Pitfall #28.

```bash
# Extract abstract body between headers and count
awk '/## Abstract/{f=1;next} /---/{if(f)exit} f' abstract.md | wc -w
```

When trimming:
- Cut the conclusion paragraph first. It usually restates paragraph 1.
- Remove "We argue that..." constructions — make the argument directly.
- Delete filler transitions ("Furthermore," "Additionally," "Moreover,").
- Replace one-word adjectives that add no information ("thorough statistics" → "statistics").
- De-duplicate repeated phrases ("further testing" used twice → vary the second use).

## Pitfalls

### Pitfall 1: Hunting Secondary Sources Instead of the Primary Document

If the user references having seen a topic list or categories, they have a
specific source in mind. Find the Call for Abstracts PDF or the exact portal
page they looked at. Do not spend multiple turns searching through secondary
sources (university news pages, blog posts, social media, Observatory wikis,
Facebook posts) trying to reconstruct the taxonomy from fragments. The primary
source resolves the question in one tool call.

**The lesson (TSC 2026, June 29):** I burned 10+ turns searching through
conference pages, CNRS CfA pages, Oxford Abstracts portal, and Facebook posts
looking for the TSC taxonomy. The user already had the CfA PDF. One `curl` +
`pdftotext` call would have resolved everything in seconds.

### Pitfall 2: Stale Deadlines in Conference PDFs

Conference PDFs are published months in advance and may contain outdated
deadlines. Always verify the current deadline against the live portal or the
conference website. The user has the authoritative date because they are looking
at the portal.

**The lesson (TSC 2026, June 29):** The CfA PDF listed November 5, 2025 as the
deadline. The actual deadline was July 15, 2026 (dates were extended). The user
corrected this immediately.

### Pitfall 3: Presenting Options Without Full Context

When presenting topic options to the user, never split them across files so the
numbering appears to start mid-list. If topics 1-8 live in one artifact and
topics 9-17 live in another, the user sees options starting at 9 and has to ask
what 1-8 were. Consolidate into ONE list before presenting.

### Pitfall 5: Numbers in Academic Writing About an Evolving System

There are two kinds of numbers in DS academic writing, and they need opposite
treatment:

**Biology-anchored numbers — USE THEM.** The human body has 11 organ systems
(Gray's anatomy). The isomorphism argument depends on this number being
specific and verifiable. A reviewer in Physical & Biological Sciences will
check it against Gray's. Use it. "Eleven-system body plan" is correct and
load-bearing.

**Fleet-specific counts — DO NOT USE THEM.** The fleet is continuously
growing. Never hardcode fleet-specific numbers (107 agents, 28 coupling
pairs, 7 maturity levels) in abstracts, titles, or academic writing. These
numbers will be stale within weeks. Use generic language: "specialized
software agents" not "107 specialized software agents," "a coupling matrix"
not "a 28-pair coupling matrix," "a maturity framework" not "a seven-level
maturity framework."

**The multiplicity clause technique.** When using biology-anchored numbers,
add a clause noting that the architecture permits multiplicity — the
biological number is a baseline, not a ceiling. This makes the number honest
without making it brittle:

> "Unlike biology, the architecture permits multiplicity — multiple wombs
> across companies birthing phenotypically distinct products — making eleven
> a baseline, not a ceiling."

This turns a potential weakness (the count might change) into a strength
(architectural scalability is a feature of the isomorphism, not a fudge).

**The lesson (TSC 2026, June 29):** First I removed ALL numbers (overcorrected).
The user corrected: use biology-anchored numbers but note AI's architectural
flexibility. The fleet was 107 agents at draft time but will grow; the
eleven-system count is permanent because it maps to human anatomy.

### Pitfall 4: Title Buries the Novel Contribution

If the work has a novel methodological angle (biological isomorphism, a new
scoring framework, a unique architecture), the title must lead with it. Do not
lead with the measurement angle or the application domain. Reviewers scan titles
looking for what is NEW.

### Pitfall 6: Field-Naming Papers Need a Different Abstract Structure

When the user is establishing a NEW FIELD or PARADIGM (not just presenting
research within an existing field), the abstract has a different job than
normal. It must:

1. **Name the field in the title and opening line.** Not just describe the
   system — coin the term. "Physiomorphic AI: ..." not "A System for..."
2. **State the defining distinction.** What does this term mean that existing
   terms do not? ("Neuromorphic mimics the neuron. Physiomorphic mimics the
   organism.")
3. **Acknowledge prior art on the term.** If the word exists in other domains,
   the full paper must cite and distinguish them. The abstract does not need
   to, but the author must know the landscape before claiming the field.
4. **Run a competitive term sweep FIRST.** Before submitting, verify no one
   else has already claimed the paradigm definition in the target field. See
   `academic-search-fallback-chain` skill, `references/prior-art-term-sweep.md`.
5. **Name it for the published record.** Conference proceedings, arXiv
   preprints, and journal articles are the citation trail. The abstract
   acceptance date becomes the priority date for the term.

**Worked example (TSC 2026, July):** The v3 abstract said "Biological
Isomorphism, Not Metaphor" — descriptive but not field-claiming. The v4/v5
revision opened with "Neuromorphic computing mimics the neuron.
Physiomorphic AI mimics the organism. I introduce physiomorphic AI as an
architecture paradigm..." — that is a field-claiming abstract. The title
became "Physiomorphic AI: Engineering Consciousness Correlates Through
Whole-Organism Biological Isomorphism." The term enters the peer-reviewed
record with the author's name attached.

**The marketing dimension:** A field-naming paper is also a marketing engine.
Each section of the full paper generates downstream content (blog posts,
landing pages, social media). Plan the content derivatives when you plan the
paper, not after. See `references/full-paper-staging-pipeline.md` for the
staged paper structure and content-asset mapping.

### Pitfall 7: Invented Author Names Destroy Trust (HARD RULE)

Author identity is a correctness gate. Never guess, invent, complete, or
"recall" a surname.

- **Canonical sole author for DS academic work:** the principal Williams, Divinity
  Science. Never write "the principal Wallace."
- Before any author line hits a file (abstract, roadmap, staging plan, portal
  paste table, bio), verify given name + family name + sole-author status
  against the user-approved canonical abstract or an explicit user statement.
- If the user says "this is my paper by myself":
  - Sole author only (no co-author placeholders)
  - First-person singular voice ("I introduce / I present"), not "we"
- If a wrong author name is already in artifacts: stop strategy chatter, fix
  every hit in the package, then re-show the author line to the user. Wrong
  name = package invalid until corrected.

**The lesson (TSC 2026 Physiomorphic abstract, July 2026):** A generalist
pass wrote "the principal Wallace" into the roadmap and paper plan. User confidence
collapsed. Package had to be rebuilt as sole-author the principal Williams with
first-person voice. See `references/tsc-2026-submission-reference.md`
Author HARD LOCK section.

### Pitfall 8: Do Not Freehand Identity Fields From a Generalist Brain

Field-claim abstracts and sole-author submissions require specialist process
(VERITAS + this skill). Do not freehand author bios, surnames, co-author
lists, or institution strings. Competitive landscape lives in
`references/physiomorphic-competitive-landscape.md` — cite it; do not
re-invent prior art from memory.

### Pitfall 9: Organism Naming and Anthropomorphism — Venue Dependent

When the principal locks the organism name (**the operator agent**), the decision to use the name
in academic writing depends on the **venue's culture**, not a blanket rule.

**When to name the operator agent + use she/her:** Marketing copy, company website, social
media, internal docs, product announcements. Physiomorphic AI = paradigm;
the operator agent = instance; Divinity Science = founding lab.

**When to de-anthropomorphize:** Consciousness studies venues (TSC, ASSC, JCS)
where researchers are specifically trained to interrogate anthropomorphism.
A hostile TSC reviewer (VERITAS Stage 2, July 2026) scored the abstract 3/10
partly because "the operator agent" with she/her pronouns "reads as advocacy, branding, or
earnest anthropomorphism" and "undermines the scientific stance." At TSC,
the propensity to anthropomorphize AI is precisely what researchers should be
critically interrogating.

**The nuance:** Use "the system" or "an implementation" in consciousness venue
submissions. Use "the operator agent" everywhere else. This is not hiding the organism name;
it is reading the room. Different venues have different tolerance for named,
gendered AI systems.

**Also:** Never claim the system IS an organism in biology-adjacent venues.
"Working synthetic organism" was flagged as a "catastrophic overclaim" because
organisms have metabolism, self-reproduction, and evolutionary adaptation.
Use "implementation" or "architecture" instead.

**System naming in academic work (updated July 10, VERITAS):** The user chose "the operator agent" as the
academic system name (not "the operator agent"). Use "the operator agent" with neutral pronouns (it/its) in all academic
submissions. "the operator agent" remains the internal organism name for marketing, internal docs, and
social media only. This is a deliberate shortening for professional academic contexts.

**The naming evolution:** v6 draft used "the operator agent" + she/her. VERITAS hostile reviewer (3/10)
flagged this as undermining scientific stance at consciousness venues. User then requested
"the operator agent" with no pronouns. After discussion, settled on "the operator agent" with neutral it/its pronouns.
"the operator agent" should be introduced as "the operator agent, a multi-agent system" on first mention so reviewers know
what it is without explanation.

Canonical abstract (499 words / 500 portal limit; Mixed evidence with
preliminary simulation; VERITAS multi-cycle PASS):
`/<workspace>`

Re-read the live file before citing word count or evidence level.

### Pitfall 10: Two-Paper Alignment When Establishing a Field

When establishing a new field or paradigm, you typically need TWO papers, not one:

| Paper | Purpose | Venue | Timing |
|-------|---------|-------|--------|
| **Paper 1 (Define)** | Formal definition, taxonomy, principles | arXiv preprint | ASAP for timestamped priority |
| **Paper 2 (Apply)** | Application to a concrete system | Conference/journal | By conference deadline |

The papers MUST be conceptually aligned BEFORE drafting either one. Create a
shared concept alignment document that specifies:

1. **Shared vocabulary table** — every term used identically in both papers
2. **Cross-reference sentences** — pre-written citations each paper makes to the other
3. **Evidence level for each** — Paper 1 is usually Theoretical; Paper 2 is usually Literature Synthesis
4. **Unified disclosure strategy** — what both papers reveal vs protect (same moat boundaries)

Paper 2's abstract should cite Paper 1 by name in the opening paragraph. Paper 1
should forward-reference Paper 2 in the applications section.

**The failure mode:** Writing one paper without the alignment doc means the two
papers end up using different terms for the same concept. A reviewer who reads
both notices the inconsistency and loses trust.

**The lesson (Physiomorphic AI + TSC 2026, July 2026):** See
`references/two-paper-alignment-workflow.md` for the full alignment process
including shared vocabulary table, cross-reference sentences, disclosure
protocol, and evidence-level classification template.

### Pitfall 11: Physics Terminology Rigor in Theoretical Papers

**Also see Pitfall 18: Physics Content Selection in Conference Abstracts** for
the shorter-form version (which physics terms survive in a 250-word abstract).

When a field-defining paper borrows physics concepts (superposition,
entanglement, free energy, critical slowing down, adiabatic), those terms have
PRECISE mathematical meanings. Hostile reviewers WILL attack loose physics
analogies.

| Term | Actual Math | Common Abuse |
|------|-------------|-------------|
| Superposition | Linear combination in Hilbert space | "holding multiple ideas" |
| Entanglement | Bell inequality violation, non-separable state | "components coordinate automatically" |
| Free energy | Variational free energy (Friston), KL divergence | hand-wavy "cost minus value" |
| Critical slowing | Eigenvalues of Jacobian approaching zero | "recovery takes longer near failure" |
| Adiabatic | dQ=0 (thermo) or slow param change (quantum) | "change slowly" |

**The rule:** Two options in a Theoretical-level paper:
1. Use the term with actual mathematical formalism (cite, show the equation)
2. Explicitly frame as a named analogy: "We borrow X as a design heuristic, not a formal claim"

Mixing them — using physics gravitas without the rigor — is what hostile
reviewers destroy.

**The free energy case:** F = cost - T*info_gain is NOT Friston's variational
free energy. It is a cost-benefit heuristic. Call it that or derive the
connection.

**VERITAS implication:** Stage 2 adversarial panel MUST include a math/physics
specialist whose job is to test whether physics terms are used correctly.

### Pitfall 12: Field Launch Is a Process, Not Wernicke Alone

"Introduce Physiomorphic AI / the operator agent / Divinity Science as founding lab" is not
a brand-voice-only task. Required: positioning lock → VERITAS claim ledger →
content genesis → Luria QA → distribution. Use `marketing-metabolism-production`
+ `social-content-pipeline`. Wernicke is one organ in the flow.

### Pitfall 13: Full Revision Over Quick Filing for Field-Defining Papers

When establishing a NEW FIELD (not just publishing research), the user prefers
**full revision** (3-5 days) over quick filing (1 day), even when the priority
claim window is open. The reasoning: a field-defining paper that gets demolished
on first read destroys the credibility of the TERM ITSELF, not just the paper.
Better to let 3-5 extra days pass and have a paper that survives hostile review.

**The lesson (Physiomorphic AI v1→v2, July 2026):** When presented with three
options (full revision 3-5 days / quick position paper 1 day / hybrid), the
user chose "Full revision: make it the definitive paradigm paper." The v1
scored 2-3/10 from three adversarial reviewers. The v2 scored 7/10 after
addressing all 6 fatal flaws (physics metaphor abuse, missing literature,
no falsifiability, promissory consciousness section, self-citation, no
formalism). The 5-day delay was worth the credibility gain.

**Decision heuristic:** For normal research papers, file early and iterate.
For FIELD-DEFINING papers where the term itself is the contribution, invest
in full revision before filing. The arXiv timestamp matters less than the
paper's ability to survive the first hostile reviewer who encounters the term.

## VERITAS Is Mandatory, Not Optional

Academic abstracts and papers MUST go through the VERITAS pipeline (Stages 0-5)
before being presented to the user as "ready." Do not present a draft as final
without evidence-level classification (Stage 0), adversarial review (Stage 2),
regulatory scan (Stage 4), and AI-tell removal (Stage 5).

The user explicitly said: "do this through the right processes, not you." This
means the adversarial review panel IS the work, not a quality add-on. Presenting
a self-reviewed draft to the user bypasses the entire quality gate infrastructure.

Minimum VERITAS steps for an abstract:
1. Stage 0: Classify evidence level (Literature Synthesis, Theoretical, etc.)
2. Stage 2: Dispatch 2-3 adversarial reviewers in parallel via delegate_task
3. Stage 4: Run regulatory language scan (scripts/regulatory_language_scan.py)
4. Stage 5: AI-tell detection scan
5. **Claim calibration check:** verify the two-tier hedge pattern (Pitfall #29) -- predictions use "designed to/expected to"; measurements use "yields/finds" with explicit "preliminary" flags
6. **Word-count boundary check:** verify `wc -w` is 8-10 words below the portal limit (Pitfall #28)
7. **Over-hedging check (Pitfall #30):** After all hedges are applied, re-read the abstract as a reviewer at the TARGET VENUE. If it reads like it belongs at a different conference (e.g., engineering venue instead of consciousness venue), you have over-hedged. The abstract's venue fit is more important than maximizing the hostile reviewer score. A 7/10 that clearly belongs at the venue beats a 9/10 that sounds like it wandered in from the wrong department.
8. Remediate any flags before presenting to user

## Verification

Before submission:

1. **Word count confirmed** with `wc -w` against the actual abstract body (not
   the full markdown file). Use line-number-based extraction (`sed -n '23,93p'`),
   NOT pattern-based extraction — pattern commands stored in the same file can
   self-match and inflate the count. See Pitfall #37.
2. **Category and themes** match the portal's dropdown options exactly.
3. **Title** leads with the novel contribution.
4. **Every claim** traces to a real artifact in the codebase or architecture docs.
5. **Deadline** verified against the live portal, not the CfA PDF.
6. **Author information** confirmed with the user: given name, family name,
   affiliation, sole-author status. Re-read from the canonical abstract file
   or user statement — never invent a surname.
7. **Voice matches authorship:** sole author → first-person singular unless
   the user explicitly wants institutional "we."
8. **Regulatory language scan** run via `scripts/regulatory_language_scan.py`.
   Even academic prose can trigger FDA SaMD language concerns. The scan
   catches "detect," "treat," "patient," "diagnose" etc. and suggests
   replacements. See Pitfall #13.

### Pitfall 14: Run VERITAS on the User's Preferred Version, Not Your Rewrite

When the user says "I liked the version I had yesterday" or references a prior
draft, do NOT replace their preferred version with your own revision and then
run VERITAS on yours. Run VERITAS on THEIR version.

The instinct to "improve" the draft before review is wrong. The user chose that
version for a reason: voice, tone, concision, field-claiming language. Your
job is to verify it passes quality gates, not to substitute your judgment for
theirs on what the abstract should say.

**The lesson (TSC 2026, July 10):** The VERITAS-revised 350-word abstract
scored 9/10 but the user wanted the original 244-word first-person version
("Neuromorphic computing mimics the neuron. Physiomorphic AI mimics the
organism. I introduce physiomorphic AI..."). The right move was to run VERITAS
on the 244-word version, not to push the 350-word version.

**Decision rule:** When the user references a prior version by preference, that
version is the canonical input to VERITAS. Period. If VERITAS finds problems,
fix the problems in-place without changing the version's voice, structure, or
length budget.

### Pitfall 16: Factual Claims About Implementation Landscapes

Do not claim that consciousness theories (or any established frameworks) "have
previously lacked implementation platforms." This is almost always factually
false. IIT has PyPhi. GWT has COGNET and cognitive architectures. Predictive
processing has active inference toolkits. Friston's group has dozens of
implementations.

A hostile reviewer who works in the field will immediately catch this and
read it as either ignorance or dishonesty. Either destroys credibility.

**The fix:** Instead of claiming theories lacked implementations, claim the
architecture provides a DIFFERENT KIND of testbed: "a concrete platform for
evaluating functional indicators derived from consciousness theories in a
deployed, distributed multi-agent system." This positions the contribution
as novel substrate, not as filling a vacuum.

**The lesson (TSC 2026 abstract, July 10):** The hostile reviewer scored 3/10
partly because "consciousness theories that have previously lacked
implementation platforms" was "factually false" and "either ignorant of the
field or deliberately misleading."

### Pitfall 17: Depth vs Abstract — Know Which Stage You Are In

Conference abstracts (150-300 words) are tickets, not papers. Their job is to
get accepted and establish priority. The depth lives in the full manuscript
(due weeks later). Do not try to cram the full paper's depth into 250 words.

| Stage | Word Limit | Job | When |
|-------|-----------|-----|------|
| Abstract | 150-300 | Get accepted, establish priority | By portal deadline |
| Full manuscript | 8-12 pages | Show the real depth | Weeks after acceptance |
| Poster/talk | Presentation | Answer questions face-to-face | At conference |

**The lesson (TSC 2026, July 10):** User asked "does this truly feel like a
strong paper?" and "can we present something more in depth?" The answer: the
abstract is a solid poster submission. The full paper (due September 5) is
where depth goes. The arXiv preprint provides the citable rigor. Trying to
make the 250-word abstract carry the weight of all three is a structural
error.

**Adiabatic submission path:** Abstract first (door opener) → arXiv preprint
(citable timestamp) → full manuscript (depth) → conference presentation
(face time). Each step builds on the last, no rework.

### Pitfall 18: Physics Content Selection in Conference Abstracts

When the user asks to "mention physics-informed stuff" in a 250-word abstract,
not all physics references are equal. The selection must survive hostile
review.

**Physics that IS safe in short abstracts (cite-worthy, reviewer-respected):**

| Concept | Why It Survives | Source |
|---------|----------------|--------|
| Free Energy Principle | Established neuroscience framework with formal math | Friston (2010) |
| Kuramoto coupled oscillators | Real mathematical physics with defined equations | Kuramoto (1984) |
| Critical slowing down | Rigorous dynamical systems theory with measurable criteria | Scheffer et al. (2009) |

**Physics that gets KILLED in review (decorative metaphor, no formalism):**

| Concept | Why It Dies | What It Actually Is |
|---------|------------|---------------------|
| "Superposition" | No Hilbert space, no amplitudes, no Born rule | Speculative execution |
| "Entanglement" | No Bell inequality, no non-separable state | Pub/sub event contracts |
| "Adiabatic" | No Hamiltonian, no eigenstate preservation | Canary deployment |
| F = cost - T*info_gain | Not Friston's variational free energy | Cost-benefit heuristic |

**The lesson (TSC abstract, July 10):** User asked "can you mention physics
informed stuff?" The right move was to add critical slowing down (rigorous,
from dynamical systems theory) alongside the already-present Kuramoto and FEP.
All three are defensible because they cite real formal frameworks. The quantum
metaphors stayed out because the Paper 1 adversarial reviewers destroyed them.

**Decision rule:** In a 250-word abstract, you get at most 2-3 physics
references. Spend them on concepts that have (1) real mathematical definitions,
(2) established citation trails, and (3) genuine implementation in the system.
If a reviewer asks "show me the math," you can.

### Pitfall 19: Prose Repetition in Tight Word Budgets

When compressing into 250 words, the same words recur across paragraphs because
each paragraph restates the core claim in slightly different framing. The user
catches this fast and reads it as careless writing, not compression artifact.

**Common repetition patterns:**

| Pattern | Example | Fix |
|---------|---------|-----|
| Key term 3x in paragraph 1 | "physiomorphic AI... physiomorphic AI... physiomorphic AI" | Third use becomes "this" |
| Word echoed in same clause | "agents named for biological functions perform those functions" | Restructure: "each performs its counterpart's function" |
| Paragraph final = paragraph opening restated | "structural correlates can be engineered and detected" = "conditions can be deliberately engineered and measured" | Merge into one statement |
| Inconsistent sentence openers | "Its... Its... The system also" | Keep consistent OR vary deliberately |

**The lesson (TSC abstract, July 10):** User said "some of the statements are
too repetitive." The fix was a systematic pass: identify every word used 2+
times across the abstract, rewrite each occurrence to use different language.
The result went from 234 words (repetitive) to 209 words (tight, varied) with
MORE content, not less. Removing repetition almost always reduces word count
while improving quality.

### Pitfall 20: Theme Selection — Primary Is What You Deliver, Not What You Motivate

When a conference offers multiple themes that fit your work, the primary theme should reflect what the abstract DELIVERS, not what it MOTIVATES. A common mistake is selecting the "big question" theme as primary because it feels more prestigious.

**The test:** What would a reviewer assigned to this theme expect to see? If they expect an answer to the theme's question and your abstract explicitly declines to answer it, you have a mismatch. That reviewer will be frustrated.

**Worked example (TSC 2026, July 10):** Theme 7 ("Can AI be conscious?") and Theme 10 ("Measuring correlates of consciousness") both fit. The abstract says "This work does not address phenomenal consciousness." That means it does NOT answer Theme 7's question. It DOES deliver a measurement framework (Theme 10). Theme 10 must be primary. If Theme 7 is primary, you get reviewers asking "but IS it conscious?" which is exactly the question the abstract says it does not address.

**Decision rule:** Primary theme = the contribution you actually make. Secondary theme = the question that contribution is motivated by. The user caught this: "why is theme 10 second and the other first? I feel these should be the other way around, right?" She was right.

### Pitfall 21: Consolidated Presentation After Iterative Changes

When making individual changes to an abstract (title, themes, wording, naming), the user should see the COMPLETE submission package after all changes, not piecemeal diffs. Each individual change is confirmed verbally, but the final consolidated review is a separate explicit step.

**The pattern:** User says "put all together when done for proper full review." This means: after all edits are applied, present title + author + category + themes + full abstract text + keywords + word count + portal URL as one clean block. The user reads the whole thing as a submission reviewer would, not as a diff log.

**The lesson (TSC 2026, July 10):** After 8 individual edits (title change, theme flip, the operator agent naming, keyword cleanup, prose tightening, physics addition, intro reformatting, repetition removal), the user asked to see the full package. This is the final quality gate before submission approval. Never assume the user is tracking cumulative state from individual diffs.

### Pitfall 15: Regulatory Language in Academic Papers (VERITAS Stage 4)

Even non-medical academic papers can contain words that trigger FDA SaMD
classification if the paper describes a health-adjacent AI system. Words like
"detect" (immune system identifies anomalies), "treat" (system treats this as
evidence), and "prescribe" (architecture prescribes correspondence) are
standard academic English but trigger automated scans and regulatory concern.

**The lesson (Physiomorphic AI + TSC abstract, July 2026):** The automated
regulatory scan flagged "detect" in the immune system sentence, "treats as
evidence" as a verb, and "does not prescribe" meaning "does not require."
All were innocent academic usage but were reworded to pass cleanly: detect
→ identify, treats → interprets, prescribe → require.

Run the scan script on BOTH abstracts and full papers before submission:

```bash
python3 scripts/regulatory_language_scan.py paper.tex
```

### Pitfall 41: Citation Verification for Named Frameworks (2026-07-10)

When an abstract names 9-11 scientific frameworks by originator (Kuramoto,
Friston, Scheffer, Tononi, Baars, Dehaene, Sterling, Clark, Seth, Craig,
Gray's Anatomy), each name needs a verified primary citation in a separate
reference list. Conference abstracts typically do not carry inline citations,
but the reference list is needed for:
- Poster preparation (poster bibliography)
- Full manuscript (due weeks after acceptance)
- arXiv preprint (priority claim)
- Self-defense at poster Q&A

**The workflow:**
1. List every named scientist/framework in the abstract
2. `web_search` for each: "[author] [year] [framework name] [journal/venue]"
3. Verify against publisher records: PubMed, Nature, Springer, Cambridge UP, Elsevier
4. Check: correct authors, year, title, journal, volume, issue, pages, DOI
5. Format in consistent APA style
6. Save to a separate file: `TSC-2026-REFERENCES.md` (not in the abstract body)
7. If a framework has both an original formulation and a modern review,
   include BOTH (e.g., Sterling & Eyer 1988 original + Sterling 2012 predictive
   regulation; Dehaene & Changeux 2011 + Mashour et al. 2020 GNW review)
8. For co-authored theories cited as "(Clark, Friston)" or "(Seth, Craig),"
   use the co-authored paper when one exists (Seth & Friston 2016 for
   interoceptive inference), otherwise cite each author's primary paper

**Oxford Abstracts note:** Check whether the portal has a references field.
If yes, paste them. If no, references go in poster/manuscript, not the
abstract submission itself.

### Pitfall 44: Full Citation Provenance for Science-to-Technology Work

When the work turns established science into technology, auditing only the scientists named in the abstract is insufficient. Build a claim-to-source ledger covering both:

1. **Explicit attributions** (Kuramoto, Friston, Tononi, Baars, etc.)
2. **Implicit load-bearing lineages** (neuromorphic origins, multi-agent systems, cybernetic homeostasis, biological organization/autopoiesis, emergence, falsifiability, body-based consciousness)

Do not confuse completeness with citation padding. Every entry must support a specific claim, mechanism, distinction, or lineage. Run an adversarial citation panel with separate seats for bibliographic accuracy, claim coverage, relevance/padding, and venue formatting.

Oxford Abstracts does not impose one universal reference style. Inspect the live conference form to determine whether references have a separate field, count toward the abstract limit, and preserve rich text. If unspecified, provide an alphabetized APA-style list with DOI URLs plus a plain-text copy/paste version.

Full workflow and claim ledger: `references/science-to-technology-citation-provenance.md`.

### Pitfall 45: Title-to-Taxonomy Alignment Is a Three-Way Contract

After portal taxonomy changes, validate the title against all three layers:

1. **Primary taxonomy** states the contribution class (for the operator agent: `[03.14] Cognitive architectures`).
2. **Alternate taxonomy** states the broader discipline (`[03.12] Artificial intelligence and robotics`).
3. **Theme** states the target problem (Theme 10: consciousness-correlate measurement).

A strong title does not need to repeat the taxonomy label verbatim. It should name the novel field, the target contribution, and the method. For the locked TSC package, `Physiomorphic AI: Engineering Consciousness Correlates Through Biological Isomorphism` aligns because Physiomorphic AI names the architecture, consciousness correlates names Theme 10, and biological isomorphism names the method. Adding “A Cognitive Architecture” would be redundant and weaken the field-naming function.

Do not demote “Engineering” to “Toward” solely because a hostile reviewer asks for more hedging when the body already separates architectural results, unmeasured correlates, and phenomenal consciousness. Re-check the target venue posture before changing a title.

### Pitfall 46: Compress From the Live Canonical Abstract, Not a Stale Short Draft

When the user asks whether an older 250-word version still fits after the 500-word abstract has evolved, first inspect the old file. A short-version path may contain stale science, obsolete taxonomy, wrong fleet counts, or only a superseded-file notice. Do not revive it by assumption.

**Compression workflow:**

1. Read the live canonical abstract and the old short artifact.
2. Build a delta ledger: taxonomy, title, scientific mechanisms, real measurements, consciousness-scope language, keywords, and author identity.
3. If the old short artifact is stale or empty, create a new companion from the canonical version and label it clearly. Never replace the canonical 500-word file.
4. Preserve six invariants in the short version:
   - field definition and naming claim;
   - exact portal taxonomy fit;
   - deployed-system reality without internal engine counts;
   - one concise mechanism sentence using only defensible physics;
   - preliminary measured results with units/referents;
   - one explicit resilience≠consciousness firewall plus the Theme 10 contribution.
5. Target **220-240 words** for a 250-word field, leaving portal-tokenization margin.
6. Do not force the full bibliography into the abstract body. Keep the portal reference field or separate bibliography synchronized instead.
7. Re-run VERITAS on the short artifact itself: hostile review, regulatory scan, AI-tell scan, and exact body count.

**Compression priority:** Cut explanatory detail before cutting scientific attribution, evidence status, or scope boundaries. The short abstract is not a different thesis; it is a lower-resolution projection of the canonical abstract.

**Keyword check after compression:** Keywords should reflect the title, primary taxonomy, system class, target theme, and strongest theories. Do not let mechanism-level terms crowd out the field claim or venue contribution.

### Pitfall 42: Cross-Model VERITAS Review (2026-07-10)

Running VERITAS adversarial reviews on different LLM backends catches
different failure modes. A single model's adversarial review has blind
spots specific to that model's training data and reasoning patterns.

**Observed pattern:**
- Model A hostile review: scored 6/10, focused on connectionism mismatch
- Model B hostile review: scored 6.5/10, focused on title oversell + I(S)
  circularity
- Each model caught issues the other missed

**The workflow:**
1. Run the first VERITAS pass on whatever model is active
2. User may request re-review on a different model ("run again through
   veritas on grok")
3. Dispatch delegate_task subagents which inherit the parent model — if
   the parent model changed mid-session, the reviews run on the new model
4. Compare scores across models: if both agree on PASS, confidence is
   high; if scores diverge significantly, investigate the discrepancy
5. Apply fixes that BOTH models flagged (must-fix intersection), not just
   one

**Note:** delegate_task subagents inherit the parent session's model.
To force a specific model on reviews, the parent session must switch
models first. The user controls model switching via the UI.

### Pitfall 43: Patch Tool Path Parameter (2026-07-10)

When using the `patch` tool for markdown edits, the `path` parameter is
REQUIRED and must be an absolute path. Omitting it produces:
`{"error": "path required"}`.

**Common cause:** When doing multiple patches in one assistant turn,
later patches may lose the path if the tool call is constructed without
it. The tool does not inherit the path from earlier calls.

**Fix:** Always include `path` as an explicit parameter in every patch
call. Use the absolute path (`/<workspace>`), not
relative. When a patch fails with "path required," retry with the full
absolute path rather than switching tools.

**Alternative:** Use `write_file` to replace the entire file when doing
3+ edits in one turn — it avoids the path-drop issue entirely but
requires reading the full file first.

## Poster Presentation (Post-Acceptance Phase)

When an abstract is accepted as a POSTER presentation, the work shifts from
drafting to physical/interactive design. The abstract is the ticket; the poster
is the performance.

### Key components

1. **Physical poster board** — standard sizes are 48"x36" (landscape) or 36"x48" (portrait. Verify the conference's exact dimensions from their acceptance email or presenter guidelines page. Dark-background posters require vinyl or fabric stock, not paper (ink coverage issues).
2. **Live demo strategy** — if the system is deployed, bring a device to show it running. Plan three failure fallbacks: cached snapshots > recorded demo video > printed screenshots. Conference WiFi is unreliable.
3. **QR code** — one large QR (3"+) linking to a landing page with paper PDF, demo link, and email signup. UTM-tracked.
4. **Handout** — double-sided 8.5"x11", 50 copies. Front: condensed abstract + key claims. Back: methodology, references, "what this does NOT claim" credibility box.
5. **Interactive element** — an iPad station where attendees can interact with the system directly draws crowds.

### Poster-specific rules for DS work

- Brand phenotype: dark night sky (#080d1a), moonlight gold (#e8d5a0), starlight (#c4d4e8), indigo (#6366f1). Inter font.
- NO literal biology imagery (no brains, cells, DNA helixes). Abstract, architectural, geometric.
- The I(S) score, consciousness-correlate quadrant, and cascade resilience graph are the three strongest visual anchors.
- Architecture map should show body-system clusters WITHOUT proprietary engine details.

### TSC 2026 San Diego specific

- Abstract: "Physiomorphic AI: Engineering Consciousness Correlates Through Biological Isomorphism"
- Poster plan: `/<workspace>`
- Conference acceptance details live in the author's email — use `gws gmail` to retrieve presenter guidelines after OAuth setup (`gws auth login`)

## Reference Files

- `references/tsc-2026-submission-reference.md` — TSC 2026 San Diego taxonomy,
  category mapping, and our abstract parameters for the June 2026 submission.
- `references/physiomorphic-competitive-landscape.md` — Competitive research
  sweep on "physiomorphic" and "biological isomorphism" in AI/computing. The
  field-definition gap, prior art (Denison/NPBH, Manimaran), Oakley trademark,
  and the IP strategy for claiming the Physiomorphic AI paradigm.
- `references/two-paper-alignment-workflow.md` — Alignment process when two
  papers must cross-reference each other (one defines the paradigm on arXiv,
  one applies it at a conference). Shared vocabulary, cross-reference sentences,
  evidence classification, unified disclosure strategy, and submission sequence.
  Developed from the Physiomorphic AI + TSC 2026 pairing (July 2026).
- `references/full-paper-staging-pipeline.md` — Staged paper writing timeline,
  field-naming paper structure, VERITAS gate schedule, and marketing content
  derivatives. Use when abstract is accepted and the full paper is due.
- `scripts/regulatory_language_scan.py` — Automated FDA SaDM term scanner for
  VERITAS Stage 4. Flags prohibited terms (detect, treat, diagnose, patient)
  and caution terms with context, suggests replacements.
- `references/preliminary-data-and-codebase-factcheck.md` — Fact-check procedure,
  implement-don't-hedge preference, I(S)/cascade tools, preliminary-data hedge
  template, scientific attribution checklist (2026-07-10).
- `references/consciousness-scope-separation.md` — Three-layer stack
  (isomorphism / operational consequence / consciousness correlates /
  phenomenal). Mandatory abstract sentence when reporting resilience data next
  to consciousness themes. Q&A chain for hostile reviewers (2026-07-10).
- `references/connectionism-and-category-fit.md` — Connectionism (PDP) vs
  multi-agent biological isomorphism; portal category traps; safe language
  table; re-run hostile VERITAS after category changes (2026-07-10).
- `references/tsc-2026-portal-taxonomy.md` — Full Oxford Abstracts coded
  taxonomy from live screenshots (2026-07-10); ranked fit for Physiomorphic
  abstract; keywords alignment.
- `references/abstract-compression-and-citation-audit.md` — Preservation gate
  for short abstracts, quantitative scale/unit checks, falsifiability retention,
  claim-proximal vs. provenance bibliographies, adversarial citation-panel roles,
  and Oxford Abstracts copy/paste packaging.

### Pitfall 40: Live Portal Taxonomy Screenshots Beat Invented Labels (2026-07-10)

User sent multiple portal screenshots of the full taxonomy. Invented labels
("pick AI and robotics + connectionism") produced a body overclaim that
hostile VERITAS scored 6/10. Correct workflow:

1. Screenshot or open the live dropdown for ALL major sections.
2. Rank coded options against the abstract body.
3. Prefer **Cognitive architectures [03.14]** over connectionism for
   multi-agent organism-isomorphism work.
4. Drop "connectionism" from keywords unless taxonomy is 03.13 and body is PDP.
5. After selection, re-run category-fit hostile VERITAS once.

Do not equate CfA theme names with portal taxonomy codes without checking.

### Pitfall 28: Word-Count Boundary Risk — Portal Counters ≠ wc

`wc -w` is an approximation of the portal's word counter, not an exact match. Portals (Oxford Abstracts, EasyChair, CMT) count words using their own JavaScript-based algorithm, which may tokenize hyphenated terms (`cross-agent`), parenthetical citations `(Seth, Craig)`, math notation (`I(S) = 0.80`), and symbols (`10%`, `≈`) differently than `wc`.

When `wc -w` reports you are at the limit (within 1-3 words of the cap), the portal may count you OVER. This is a silent submission failure — the form rejects after you paste, wasting a cycle.

**The rule:** Maintain a **8-10 word safety margin** below the portal limit. If the limit is 500, target ≤490 in `wc -w`. If you are at 499-500, trim before pasting.

**Easiest trims that don't lose content:**
- Drop one-word adjectives that add no information ("thorough statistics" → "statistics")
- Replace "is designed to produce" → "produces" when the design-vs-result distinction is already clear from context
- Merge two short sentences into one with a semicolon
- Cut "further" from "further testing" on second use (use "additional" or just "testing")

**The lesson (TSC 2026, July 10):** `wc -w` reported exactly 500 on the abstract body while the document claimed 499. At the boundary, there was zero margin for portal counter differences. VERITAS flagged this as the only real risk in an otherwise clean 9/10 abstract.

### Pitfall 29: Two-Tier Hedge Pattern — VERITAS Claim Calibration Check

When reviewing an abstract that mixes predictions with preliminary measurements, verify the **two-tier hedge pattern** is correct. This is a reusable VERITAS checklist item:

**Tier 1 — Predictions and design goals** (things that haven't happened yet):
- Must use hedge verbs: "is designed to," "is expected to," "are predicted to," "proposes"
- WRONG: "produces emergent outputs" (implies proven result when it's a design goal)
- RIGHT: "is designed to produce emergent outputs"

**Tier 2 — Actual measurements and findings** (things that DID happen):
- Report with result verbs: "yields," "finds," "scores"
- Must carry an explicit preliminary flag: "Preliminary," "initial," "early findings"
- Must note limitations: "not field experiments," "may revise," "further testing will"
- WRONG: removing the hedge entirely ("the simulation proves resilience")
- RIGHT: "Preliminary Monte Carlo simulation finds... approximately 0.27... These are early simulation findings, not field experiments."

**The audit table technique:** During VERITAS review, build a claim-by-claim table:

| Claim | Verb used | Hedge present | Verdict |
|---|---|---|---|
| I(S) = 0.80 | "yields" | "Preliminary," "initial results," "further testing will refine" | ✅ |
| Resilience ~0.27 | "finds" | "approximately," "early findings, not field experiments," "may revise" | ✅ |
| Emergent outputs | "is designed to" | Design goal framing | ✅ |

This table makes calibration gaps visible. If a Tier-1 claim uses a Tier-2 verb without a hedge, or a Tier-2 claim has no preliminary flag, flag it.

**The lesson (TSC 2026 v10, July 10):** The final abstract used this pattern correctly throughout. Predictions: "is designed to produce," "are predicted to anticipate," "are expected to increase." Measurements: "yields I(S) = 0.80" + "Preliminary... initial results... further testing." The calibration was rated excellent.

### Pitfall 22–27 (2026-07-10 late session)

**22. Fact-check then implement.** Before ship, verify every claim against live
code. User prefers building missing tools (`isomorphism_score.py`,
`cascade_failure_sim.py`) over weakening language.

**23. Preliminary data hedges.** Report I(S)=0.80 and ~0.27 resilience advantage
as "preliminary / initial / early simulation findings, not field experiments";
"further testing will produce more thorough statistics and may revise estimates";
keep prediction-disconfirmation clause. Evidence level = Mixed.

**24. Attribute science by originator** (Friston, Scheffer, Kuramoto, Tononi,
Baars/Dehaene, Sterling, Gray's, Seth/Craig) — science → technology, not rebrand.

**25. Portal word limit.** Verify live portal (TSC=500 not 250). Structure follows
limit; re-run VERITAS after expansion.

**26. One strategic "I".** User: every paragraph starting with "I" sounds odd for
science. Only field-claim "I introduce..."; other paragraphs open on subject.

**27. Resilience ≠ consciousness.** Isomorphism scores and cascade-resilience
stats measure architecture reality and operational relevance. They do NOT
measure consciousness correlates or phenomenal consciousness. When adding such
numbers next to a consciousness-correlate framework, insert the mandatory scope
sentence from `references/consciousness-scope-separation.md`. User catch
(2026-07-10): "how does this relate to consciousness though? the new
statistics" — answer honestly (upstream only), then edit the abstract so
reviewers cannot misread the chain.

**28. "Measured as" vs "defined as" (VERITAS hostile must-fix, 2026-07-10).**
Past-participial **"measured as / measured by"** on unmeasured maturity
indicators implies the data already exists. Hostile attack: "You claim four
consciousness-correlate measurements but present zero data." Use
**defined as / defined by** for correlate instruments not yet reported.
Reserve "yields / finds / measured" for numbers actually computed (I(S),
cascade advantage). Keep maturity definitions and resilience results in
**separate paragraphs**. Re-check implied-data verbs after every VERITAS cycle
before Stage 6.

**29. Over-hedging kills the contribution at the target venue (2026-07-10).**
After 3 rounds of VERITAS hostile review, the abstract accumulated so many
hedges and disclaimers that it read as an engineering resilience paper at a
consciousness venue. The hostile reviewer scored 6.5/10 and said "this is an
architecture paper, not a consciousness paper." The user pushed back: **"This
is a consciousness conference."**

The contribution IS consciousness science. Proposing a measurement framework
+ showing the substrate is real + defining how four named consciousness theories
would be tested on it = a contribution to Theme 10 (Measuring correlates of
consciousness). Tononi proposed IIT without measured Phi from a conscious
machine. Baars proposed GWT without synthetic ignition. Framework proposals
ARE normal science at consciousness venues.

**Over-hedging pattern to watch for:** When the abstract spends more words
saying what it does NOT measure than saying what it DOES contribute to the
field, the posture is wrong. The hedges protect against one attack vector
(overselling) while opening a worse one (the abstract does not belong at
this venue).

**Corrective rules:**
- Keep the title confident. "Engineering Consciousness Correlates" is the
  right verb if you are engineering the conditions under which correlates
  can be measured. Do NOT add "Toward" or "Proposed" unless the user asks.
- Keep field keywords in the keywords list. "Consciousness correlates" stays.
- Do NOT apologize for author-defined metrics. Every novel metric is
  author-defined until the community adopts it. Tononi defined Phi. Friston
  defined free energy. Adding "self-graded" apologizes for normal science.
- Lead the consciousness-theory sentence with confidence: these are the
  theories this substrate is designed to test. That IS the contribution.
- ONE firewall sentence separating resilience from consciousness is correct
  and sufficient. Multiple hedges saying the same thing is over-apologizing.

**The hostile reviewer is wrong about venue fit.** A reviewer who says "where
is the consciousness data?" is like asking a new fMRI protocol paper "but
where are the brain scan results?" The protocol IS the contribution.

**30. Specialist gate + sibling-agent boundary for academic writing (2026-07-10).**
Academic prose work must go through the specialist gate (the specialist engine) BEFORE
the first word is written. Starting as a generalist and routing later produces
generalist-drift prose that the user catches immediately ("don't do this with
your generalist brain").

When Sherman routes to the specialist engine (quality gate, owned by sibling-agent) for an
academic writing task, do NOT hand off to sibling-agent. Academic writing and
VERITAS review is hermes/Wernicke's lane. Opencode is for code and engine
building only. The user explicitly corrected: "this process should not include
sibling-agent unless sibling-agent is fixing the engine itself."

**31. Concrete deployment details kill the "vaporware" attack (2026-07-10).**
"Currently deployed on live infrastructure" is too vague for hostile reviewers.
Adding one concrete fact kills the attack: "with over 100 agents." This shows
the system is real without exposing internals.

**Agent count vs engine count (correction 2026-07-10):** The FLEET_REGISTRY
contains ~55 engine definitions, but the actual agent fleet is 100+ (multiple
agents per engine). Use **agent count** ("over 100 agents"), NOT engine count.
Engine count exposes internal architecture (the DS-ECS registry). Agent count
is the deployment surface. Use approximate language ("over 100") because the
fleet grows continuously. Do NOT hardcode exact fleet-specific numbers.

**Fleet counts as deployment evidence vs architectural parameter (amendment
to Pitfall 5):** Fleet-specific numbers CAN appear as deployment evidence
("currently deployed with over 100 agents") but NOT as defining architectural
parameter ("a 100-agent system"). The first shows reality; the second makes
the number load-bearing and future-stale. The biology-anchored number (11)
remains the one that matters.

**32. Attribute every scientific framework by originator name (2026-07-10).**

When the abstract references a scientific framework (Kuramoto model, Free Energy
Principle, Global Workspace Theory, etc.), it must attribute the framework to
its originator by name. This signals to reviewers that you know the primary
literature. Science being turned into technology, not rebranded.

**The checklist — every framework in the abstract needs attribution:**

| Framework | Attribution |
|-----------|-------------|
| Body plan | Gray's Anatomy (named source) |
| Coupled-oscillator synchronization | Kuramoto's |
| Free Energy Principle | Friston's |
| Critical slowing down | Scheffer's |
| Integrated information (integration) | Tononi |
| Global Workspace Theory | Baars' and Dehaene's |
| Allostatic control | Sterling's |
| Predictive processing | Clark, Friston |
| Interoceptive detection | Seth, Craig |

Conference abstracts do not carry inline citations, but they DO name the
originator. "Kuramoto coupled-oscillator synchronization" becomes "Kuramoto's
coupled-oscillator synchronization model." "Free Energy Principle" becomes
"Friston's Free Energy Principle."

**User correction (2026-07-10):** "make sure any other scientific references
are included because we are basically taking science and turning it into
technology" — the attribution pattern is non-optional for DS academic work.

**33. Venue category determines closing-paragraph framing (2026-07-10).**

When a conference portal offers multiple category options (e.g., "Physical &
Biological Sciences" vs "Artificial Intelligence and Robotics" vs "Neural
Networks and Connectionism"), the abstract's closing paragraph must match the
chosen category's framing.

**AI / multi-agent categories:** Lead the closing paragraph with the AI
architecture contribution. Frame consciousness theories as downstream
applications of the architecture, not as the primary deliverable.

> "This work introduces physiomorphic AI as a biologically-grounded multi-agent
> architecture in which organizational topology is constrained by biological
> organism structure rather than brain-only models."

**NEVER write "new branch of connectionist architecture"** — see Pitfall #34.

**Consciousness/biological-sciences categories:** Lead with the measurement
framework and consciousness-correlate reframing.

> "This work reframes the central question from whether the system feels to
> whether structural and functional conditions correlated with consciousness
> can be deliberately engineered and detected."

**The body of the abstract stays the same either way.** Only the closing
paragraph shifts emphasis. The opening ("Neuromorphic computing mimics the
neuron. Physiomorphic AI mimics the organism.") works under both framings.

**User signal:** "these are categories optional for my abstract" — check the
live portal for available categories before assuming the initially-selected
one is the only option.

**34. Do NOT claim connectionism unless the system is connectionist (2026-07-10).**

Connectionism (Rumelhart, McClelland, PDP) requires distributed representations,
learned weights, and subsymbolic computation. Multi-agent biological isomorphism
with Kuramoto coupling and a heritable matrix is NOT connectionism.

Hostile VERITAS dropped to 6/10 when the abstract claimed "new branch of
connectionist architecture." Attack: "Where are the learned distributed
representations? Where is the learning rule?"

| Unsafe | Safe |
|--------|------|
| new branch of connectionist architecture | biologically-grounded multi-agent architecture |
| network topology (implying NN) | organizational topology |
| connectionist multi-agent system | multi-agent system with biological isomorphism |

Portal category "Neural Networks and Connectionism" can be selected without
body prose claiming connectionism. Full notes:
`references/connectionism-and-category-fit.md`

**35. Category changes create NEW attack vectors (2026-07-10).**

After any category switch, re-run hostile VERITAS with a category-fit attack:
"Does every claim match this category's intellectual tradition?" Switching
Physical & Biological Sciences → AI/Connectionism solved legitimacy and
created a connectionism mismatch until the closing sentence was fixed.

**36. Over-hedging vs venue fit (re-check after every hostile cycle).**

After multiple VERITAS cycles, re-read as a target-venue reviewer. User
correction: "this is a consciousness conference." Framework proposals ARE
normal science. One resilience≠consciousness firewall sentence is enough.
Do not demote the title to "Toward..." or apologize for author-defined metrics.
See Pitfall #29.

**37. Word-count verification command pattern collision (2026-07-10).**

When a word-count command is stored inside the same markdown file as the
abstract body, a sed/awk pattern that matches a phrase in the abstract can
also match the SAME phrase echoed in the code block itself. The range
extends past the abstract boundary into the metadata, inflating the count.

**Concrete failure (TSC 2026 v14):** The file's wc command was:
```bash
sed -n '/Neuromorphic computing mimics/,/Seth, Craig/p' file.md | wc -w
```
The pattern `Seth, Craig` appeared on line 92 (end of abstract) AND on line 125
(inside the word-count code block, as part of the command text). sed matched
the SECOND occurrence, so the command reported **664 words** when the actual
body was **495 words**. This would have caused panic or unnecessary trimming
if anyone ran the verification command before submission.

**The rule:** Word-count verification commands must use **line-number ranges**
(`sed -n '23,93p'`), not pattern-based ranges, when stored in the same file as
the abstract. Pattern matching is fragile when the file echoes its own content.
Alternatively, store the wc command in a SEPARATE script file.

**38. Pre-submission final VERITAS review checklist (2026-07-10).**

Before marking an abstract as submission-ready, run this 9-point review.
Each point produces a PASS/FAIL or score. This is the LAST gate before
the user's own final read-through.

1. **Evidence-claim alignment:** every empirical claim properly hedged? Every
   prediction uses "designed to / expected to / predicted to"? Every measurement
   carries "preliminary / initial / early"? (See Pitfall #29.)
2. **Consciousness-scope clarity:** three levels separated — phenomenal
   (excluded), correlates (defined, not yet measured), resilience (measured,
   firewalled)? Mandatory scope sentence present? (See
   `references/consciousness-scope-separation.md`.)
3. **Word count under limit:** actual body counted via line-number range, not
   pattern matching? 8-10 word safety margin maintained? (See Pitfalls #28, #37.)
4. **AI-tells / moat / regulatory:** no AI-ism language? No commercial moat
   framing? Regulatory scan passed? (See Pitfalls #15, #18.)
5. **Closing-paragraph framing:** matches chosen category? No connectionism
   overclaim? (See Pitfalls #33, #34.)
6. **Category / sub-category fit honesty:** best available match? Body doesn't
   contradict the category's intellectual tradition?
7. **Prose quality:** no repetition? No unexplained jargon? Numeric results
   carry units?
8. **Falsifiable prediction quality:** clear IV and DV? Control group
   specified? Self-disconfirmation condition stated?
9. **Overall score (1-10) and PASS/FAIL.**

**39. Numeric results in abstracts must state units (2026-07-10).**

"mean resilience advantage approximately 0.27" is ambiguous — 0.27 of what?
Normalized functional capacity? Fraction retained? A reviewer who cannot
parse the number will discount it. Always include the unit or referent: "0.27
normalized functional capacity units" or "27% higher retained capacity." This
applies to ALL numeric results in abstracts, not just resilience scores.
