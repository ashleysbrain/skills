# Physics Metaphor Abuse + Evidence-Level Language Discipline

## Detection recipe for Check 5 (Falsifiability) and Stage 0 (Evidence Level)

Derived from the Physiomorphic AI paper adversarial review (2026-07-10), where three independent reviewers scored a draft 2-3/10 with a shared fatal flaw: physics terms used as labels for standard engineering heuristics.

---

### The Pattern

A paper borrows terminology from physics (quantum mechanics, thermodynamics, dynamical systems) to name software engineering practices, without engaging with the underlying mathematics. This is the exact same intellectual move the paper criticizes when it calls out biological metaphor in AI ("'Neural' networks are not neurons").

### Detection Checklist

For each named "principle" or "law" in a position/theoretical paper:

1. **Does the term have a precise mathematical definition in physics?** (e.g., superposition = complex linear combination in Hilbert space; entanglement = non-factorable joint state violating Bell inequalities; adiabatic = $dQ=0$ thermodynamic or $|\langle m|dH/dt|n\rangle/|E_m - E_n|^2 \ll 1$ quantum)
2. **Does the paper use that definition, or an analogy?** If the paper says "analogous to quantum superposition" but has no Hilbert space, no amplitudes, no Born rule, it is decorative.
3. **Does the paper cite the primary physics literature for the term?** If it cites Friston for "free energy" but uses a different formula than Friston's variational free energy, that is a misattribution.
4. **Could a physics-literate reviewer be offended by the usage?** If yes, the term is being abused.

### Worked Example (Physiomorphic AI v1, scored 2/10 by physics reviewer)

| Claimed Principle | Physics Meaning | Actual Usage | Verdict |
|---|---|---|---|
| Superposition | $\|\psi\rangle = \Sigma c_i\|\psi_i\rangle$, complex amplitudes, Born rule | Holding multiple options open (speculative execution) | Metaphor abuse |
| Entanglement | Non-factorable state, Bell inequality violation | Typed contract notifications (pub/sub) | Metaphor abuse |
| Free energy $F = \text{cost} - T \times \text{info}$ | Friston: $\mathcal{F}(q) = D_{KL}[q(s)\|p(s\|o)] - \mathbb{E}_q[\log p(o)]$ | Heuristic cost-benefit threshold | Misattribution (different formula than cited source) |
| Critical slowing down | $\text{Re}(\lambda_{max}) \to 0^-$, $\rho(1) \to 1$ | Monitoring variance and latency | Analogy only |
| Adiabatic | $dQ=0$ (thermo) or slow Hamiltonian change preserving eigenstate (quantum) | Incremental deployment (canary releases) | Metaphor abuse |

### Fix Protocol

When metaphor abuse is detected:

1. **Rename the principle to its honest engineering equivalent.** "Superposition" becomes "deferred commitment." "Entanglement" becomes "typed contract coordination." "Free energy minimization" becomes "resource-value thresholding."
2. **If a connection to the formal framework genuinely exists, state it as analogy with explicit disclaimers.** Write the actual formula from the cited source alongside your formula. Say "This is NOT the variational free energy. We reference Friston's framework as intellectual motivation."
3. **Never cite a formal source (Friston, Scheffer, Bell) for a formula that does not appear in that source.**

---

## Evidence-Level Language Discipline (VERITAS Stage 0)

### The Rule

Every claim in a paper must use language appropriate to its evidence level. Mismatched language is an automatic VERITAS failure.

| Evidence Level | Allowed Language | Forbidden Language |
|---|---|---|
| Original Data | "Our data show," "We found," "Results demonstrate" | N/A (all language permitted if data backs it) |
| Literature Synthesis | "We synthesize," "Converging evidence suggests," "Established findings indicate" | "demonstrates," "results show," "our data indicate," "we prove" |
| Theoretical | "We propose," "This framework predicts," "Future work should test" | "demonstrates," "results show," "our data indicate" |

### Sentence-by-Sentence Audit Method

1. Extract every sentence containing a verb of assertion (demonstrate, show, prove, find, indicate, establish, confirm, exhibit)
2. For each, ask: What evidence level supports this claim?
3. If the verb exceeds the evidence level, flag for revision
4. A single "demonstrates" at Literature Synthesis level = mandatory revision

### Common Violation Patterns

- **"The system demonstrates consciousness"** at Theoretical level = fatal
- **"Our results show"** with no data section = fatal
- **"We present quantitative measurements"** when no measurements exist yet = fatal
- **"The architecture produces X"** when the paper proposes to measure X but has not measured it = fatal. Correct: "We propose measuring whether the architecture produces X"

### The Self-Citation Trap

Citing your own unpublished companion paper ("Williams 2026, in submission") as the empirical foundation for a theoretical paper creates circular dependency. The theoretical paper claims the architecture matters; the companion supposedly demonstrates it; neither stands independently. Fix: either fold the empirical results into the same paper, or remove claims that depend on the unpublished companion.

---

## The Parallel Adversarial Dispatch Pattern (VERITAS Stage 2)

### When to Use

Any paper draft going through VERITAS Stage 2 requires at minimum 3 adversarial reviewers with DIFFERENT hostile perspectives, dispatched in parallel via `delegate_task` with the `tasks` array.

### Perspective Assignment

Each reviewer gets a distinct lens. Do NOT give them the same rubric. Diversity of hostility produces diversity of findings.

| Paper Type | Reviewer 1 | Reviewer 2 | Reviewer 3 |
|---|---|---|---|
| AI systems paper | Senior AI researcher ("is this novel?") | Domain specialist ("is the math right?") | Systems engineer ("does this scale?") |
| Consciousness paper | Consciousness philosopher ("does it abuse consciousness?") | Physics/math specialist ("are the formal claims rigorous?") | AI researcher ("is this just relabeling?") |
| Position/paradigm paper | Skeptic ("is this just a relabeling?") | Domain expert in cited field ("are the citations accurate?") | Falsifiability auditor ("can ANY claim be proven wrong?") |

### Post-Review Remediation

1. Collect all three scores. If all three score below 5.0, the paper CANNOT pass regardless of composite.
2. Build a fix table: flaw x all reviewers who flagged it x severity
3. Flaws flagged by all 3 reviewers are FATAL and must be fixed before re-review
4. Flaws flagged by 1-2 reviewers are MAJOR and should be addressed but may not require re-review
5. After remediation, run ONE focused re-review checking each fatal flaw: FIXED / PARTIALLY FIXED / NOT FIXED

### What Survived (the forced concession)

All three reviewers gave one forced concession each. This is the paper's salvageable core. The revision should build from what survived, not from what was killed. In the Physiomorphic AI case, all three conceded the taxonomy table and organism gap framing were genuine contributions. The revision rebuilt the paper around those.

---

## Full VERITAS Remediation Cycle: v1 FAIL to v2 PASS

### The Pattern (Proven 2026-07-10)

When a paradigm/position paper scores below 5.0 from all three adversarial reviewers, the remediation follows a specific sequence that reliably produces a passing v2:

1. **Collect all fatal flaws.** Tabulate: flaw x which reviewers flagged it x severity. Flaws flagged by all 3 are FATAL.
2. **Extract the forced concessions.** These are the salvageable core. Write them down separately. The v2 rebuilds around these.
3. **For each fatal flaw, write the fix before touching the paper.** This prevents partial fixes.
4. **Rewrite from scratch, not patch-by-patch.** A v1 that scored 2-3/10 cannot be patched to 7/10. The structural problems require a rebuild using the same bones (taxonomy table, organism gap framing) with new scaffolding (formalism, falsifiable predictions, honest terminology).
5. **Re-review with a single focused reviewer checking each original fatal flaw: FIXED / PARTIALLY FIXED / NOT FIXED.** Do not re-run the full panel. One focused check is sufficient and faster.

### The Decision Point: Full Revision vs Quick Filing

When the user is establishing a field priority claim, there is tension between speed (file the arXiv preprint now to lock the timestamp) and quality (fix the paper so it survives scrutiny). Present the choice explicitly:

- **Full revision** (3-5 days): The paper earns credibility. It will be the definitive reference. Reviewers who later encounter the term will find a rigorous paper, not a hand-wave.
- **Quick position paper** (1 day): File a tight 4-6 page version that defines the term, presents the taxonomy, and makes falsifiable predictions. No physics section, no consciousness section. Gets the timestamp.
- **Hybrid** (recommended for most cases): File the quick version now, expand later.

**User preference (observed 2026-07-10):** When establishing a field, the user chose "Full revision" over quick filing. The reasoning: a field-defining paper that gets demolished on first read destroys the credibility of the term itself. Better to spend 3-5 extra days and have a paper that survives hostile review.

### Score Trajectory

| Version | Reviewer 1 | Reviewer 2 | Reviewer 3 | Determination |
|---|---|---|---|---|
| v1 | 3/10 | 3/10 | 2/10 | REJECT (all below 5.0) |
| v2 | 7/10 (single re-review) | — | — | PASS for arXiv |

The v2 re-reviewer confirmed: "All six fatal flaws are addressed, not papered over." The key was structural rebuild, not cosmetic patching.
