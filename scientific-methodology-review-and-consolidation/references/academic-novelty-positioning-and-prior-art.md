# Academic Novelty Positioning and Prior-Art Engagement

Derived from the Physiomorphic AI hostile VERITAS review (2026-07-10, session 2). The manuscript had already passed a prior VERITAS cycle (v1 FAIL → v2 PASS at 7/10) for physics-metaphor abuse and falsifiability issues. This cycle found a **different class of problems** that the original checks did not cover: novelty positioning against adjacent fields, depth of prior-art engagement, citation completeness, and whether empirical results are novel or merely replications of known findings.

Use these checks for ANY position/paradigm/field-introduction paper, not just ones with physics metaphor issues.

---

## Check 10: Closest-Prior-Art Depth Audit

### The Problem

A paper cites a key predecessor for a narrow purpose (e.g., "Arbib used the word physiomorphic") while the cited work actually does substantively what the paper claims as its own contribution (e.g., Arbib's schema theory is an explicit functional-to-structural mapping with comparative model evaluation). Citing the work but under-describing its contribution makes the paper's novelty claim appear stronger than it is.

### Detection Method

1. **For each cited predecessor, read the cited work's abstract and key sections (not just the title).**
2. **Ask: Does this work do substantively what my paper proposes?** Not just "use the same word" but "perform the same function."
3. **If yes, does my paper acknowledge that depth of overlap?** Or does it cite the work narrowly?
4. **Identify the SINGLE closest predecessor** — the work that, if a hostile reviewer knew it well, would most undermine the novelty claim.

### Worked Example

| Paper Claims | Cites Arbib For | Arbib Actually Does | Gap |
|---|---|---|---|
| "organism-level reference architecture with explicit mapping" | "Arbib discussed a broader physiomorphic direction" | Schema theory: perceptual/motor schemas as dynamic systems mapped to brain regions with explicit structural-functional integration. BODB database for comparative model evaluation. Decades of "systems of systems" integration work. | Paper under-credits by 90% |

### Fix

Either (a) explain concretely how the proposed formalism differs from the predecessor's framework, or (b) acknowledge the predecessor as a direct precursor and claim only incremental novelty.

---

## Check 11: Empirical-Result Novelty Assessment

### The Problem

A paper reports an experimental result as evidence for its paradigm, but the result is a well-established finding in a different field that the paper does not engage with. The result is real but not novel, and does not distinguish the proposed paradigm from known alternatives.

### Detection Method

1. **State the finding in domain-general terms.** (e.g., "structured graph retains more function under random node removal than random graph")
2. **Search the established literature for this finding.** (e.g., Albert et al. 2000, network robustness theory)
3. **Is the finding predicted by existing theory independent of the paper's framework?** If yes, the finding is not evidence FOR the framework.
4. **What control would be needed to make it evidence?** (e.g., degree-sequence-matched, modularity-matched controls)

### Worked Example

The Physiomorphic AI case study found biologically organized dependency graphs outperform random graphs under perturbation. This is a well-known result: structured/hierarchical/modular graphs are more robust to random failure than Erdos-Renyi random graphs (Albert, Jeong, Barabasi 2000). The paper acknowledges controls were weak but does not acknowledge that the result itself is expected from existing theory.

### Fix

- Cite the established result literature explicitly
- State that the observed effect is predicted by existing theory independent of the paradigm
- Identify the specific control condition that would distinguish paradigm-specific benefit from known architectural advantages

---

## Check 12: Citation Completeness Audit

### The Problem

A field-introduction paper claims to survey adjacent traditions but omits foundational works that a reviewer in those fields would consider mandatory.

### Detection Method

For each tradition the paper positions against:

1. **What is the foundational text?** (e.g., von Bertalanffy 1968 for general system theory, Rosen 1991 for relational biology)
2. **What is the current dominant formal framework?** (e.g., Friston's FEP/Markov blanket for organism-level self-organization)
3. **What is the closest empirical methodology?** (e.g., MAPE-K architecture for autonomic computing)
4. **Is each cited or explicitly dismissed?**

### Missing Citation Categories

| Category | Example | Why It Matters |
|---|---|---|
| Foundational text of a cited tradition | von Bertalanffy 1968 (General System Theory) | Omitting the origin text signals unfamiliarity |
| Current dominant framework | FEP/Markov blanket for organism self-organization | Not engaging with the strongest existing formalism is a vulnerability |
| Direct methodological precursor | IBM MAPE-K for autonomic computing | The precursor has an explicit mapping architecture |
| Empirical baseline literature | Albert et al. 2000 for network robustness | Without this, the case study has no comparative context |
| Trademarked/prior commercial use | Oakley PhysioMorphic™ | Claims to document prior uses comprehensively but misses a trademark |

### Fix

Add missing citations. For each, either integrate into the related-work narrative or explain why it is not directly comparable.

---

## Check 13: Field-Introduction vs Position-Paper Calibration

### The Problem

A paper claims to "introduce a field" but the actual novelty is methodological framing (a useful taxonomy, boundary conditions, a falsifiability protocol) rather than a new conceptual contribution. This over-calibration invites hostile reviewers to reject novelty claims wholesale.

### Detection Method

Separate the paper's claims into categories:

| Claim Type | Test | Example |
|---|---|---|
| Conceptual novelty (new idea) | Does this idea not exist in any form in the literature? | Physiomorphic AI as a concept: NO (Arbib, Hwang, others already use the term) |
| Methodological novelty (new framework) | Is the formalism or protocol new even if the idea isn't? | Four-part isomorphism measure with boundary conditions: YES |
| Empirical novelty (new evidence) | Does the data show something not previously observed? | Case study result: NO (known network science finding) |
| Programmatic novelty (new research program) | Does the paper define a new research trajectory? | Falsifiable predictions with disconfirmation conditions at inception: YES |

If conceptual and empirical novelty are absent, the paper is a **position paper** or **research program proposal**, not a field introduction. Frame it accordingly.

### Why This Matters

A hostile reviewer assessing a paper titled "X: A Framework for Y" will look for evidence that X is genuinely new. If the conceptual content overlaps heavily with existing work (schema theory, autonomic computing, cybernetics), the reviewer will reject the "field introduction" framing and score the paper down for overclaiming. But the same paper framed as "A Falsifiable Research Program for X" with honest novelty scoping can score 7/10.

---

## Check 14: Trademark / Prior Commercial Use Search

### The Problem

A paper claims comprehensive documentation of prior uses of a coined term but misses trademarked or commercial uses that a quick search would find.

### Detection Method

1. Search `"term"` + trademark symbol
2. Search `"term"` + patent filings
3. Search `"term"` + product names
4. Search USPTO / WIPO trademark databases

### Worked Example

"PhysioMorphic" is a live Oakley, Inc. trademark for lens geometry. The paper documents academic uses (Richards 1989, Manimaran 2024, Hwang 2026, Arbib 2025) but omits the commercial trademark. While this does not affect the scientific argument, it undermines the "comprehensive prior use" claim.

---

## Composite Score Calibration for Position/Paradigm Papers

When scoring a position or paradigm paper on a 10-point scale, use this rubric:

| Score | Meaning | Typical Characteristics |
|---|---|---|
| 8-10 | PASS | Genuine conceptual novelty, strong formalism, validated predictions, comprehensive prior art, novel empirical evidence |
| 6-7 | PASS (minor revisions) | Incremental conceptual novelty, useful methodological framing, honest limitations, adequate prior art, preliminary evidence |
| 4-5 | REVISE | Self-aware but overclaiming, under-engages closest prior art, case study is not novel, missing key citations |
| 1-3 | REJECT | Metaphor abuse, unsupported claims, no falsifiability, no prior art engagement, circular evidence |

A paper that is honest, well-written, and methodologically self-aware but overclaims novelty and under-engages prior art typically scores **5/10 REVISE**. This is not a failure of the paper's quality but of its calibration. The fix is re-framing, not re-writing.

---

## The "Known Result" Trap in Case Studies

When a paradigm paper includes a preliminary case study, the most common failure is: **the result is real but not novel, and is equally consistent with multiple alternative explanations that are better established than the paradigm.**

### Pattern

1. Paper proposes paradigm X
2. Paper reports case study showing system built with X outperforms naive baseline
3. The naive baseline is the weakest possible control (e.g., random rewiring)
4. The result is predicted by existing theory Y (e.g., network robustness) without needing X
5. Paper acknowledges controls are weak but still frames result as "consistent with prediction"

### Fix

Either (a) upgrade controls to distinguish paradigm-specific benefit from known alternatives, or (b) explicitly state that the result is a known finding and the case study serves only as an illustration, not evidence.
