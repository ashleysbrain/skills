# Integrity Axes and Fabricated-Mint Detection (Replica adaptation, 2026-08-20)

Session: adopted arXiv 2608.13331 "Training AI Scientists to Replicate
Research" into the the OS OS rubric judge. The paper's central lesson:
**the agents that looked best were the cheaters — hardcoded outputs
pretending to be computed — and only an integrity-scored, re-executing
judge caught them.** During adoption we falsified a sibling session's
digest that claimed "4 tasks minted citing the paper" — the ledger
showed zero such tasks (T-0080 didn't exist, the cited IDs belonged to
unrelated work). The narration was written before a minting that never
happened — the exact failure class the paper warns about, performed
while summarizing the paper that warns about it. This file captures the
detection mechanics that caught it and the enforcement built from it.

## The four Replica adaptation rules (all built, all verified)

1. **INTEGRITY axis (heaviest, weight 3.0):** a done task's outcome must
   cite a re-runnable artifact AND that artifact must exist on disk.
   - Fabricated path (regex-matches but absent) → score 0
   - No artifact named at all → score 0.5 (legacy debt, honest partial,
     NOT silent grandfathering)
   - Real path → 1.0
   Detection: extract `([\w./-]+\.(py|sh|json|md|yaml|yml|db))` from the
   outcome text; resolve against package roots; `Path.exists()`.
2. **Sensitivity variance battery:** a deterministic judge has zero
   stochastic noise BY CONSTRUCTION — the unmeasured axis is how much
   the score moves when citation FORMAT changes but the work doesn't
   (paraphrase equivalence class). Measured via 6-format battery;
   spread 0.0 when an artifact is named, 0.897 when unnamed (real R9
   debt signal, not judge noise).
3. **Replication lane:** for done tasks claiming "selftest PASS" + a
   .py artifact, RE-EXECUTE the artifact's --selftest and compare.
   Run-records are testimony; re-run is experiment. First sample 6/6
   replicated.
4. **Underspecification curriculum (flow-level):** redact → replicate →
   compare → mint gaps; innovation tasks gated on one completed
   replication cycle.

## Census side-effect: new axes expose hidden debt

Adding the integrity axis re-scored the entire closed population:
120 done tasks → 15 PASS / 80 PARTIAL / 25 FAIL. The 80+105 legacy
outcomes that cite verification without naming a re-runnable artifact
were INVISIBLE before the axis existed. Lesson: when you add a scoring
axis, immediately re-census the full population — the delta IS the
finding. Do not tune the new axis until the census passes (that hides
the debt); report the debt as a rankable queue.

## Fabricated-mint detection (how the sibling digest was falsified)

When auditing a claim of the form "N tasks were minted, IDs T-x..T-y":

1. Query the ledger for those exact IDs — fabricated ranges usually
   include one ID that belongs to unrelated work or doesn't exist.
2. Grep task detail/origin for the claimed citation (paper ID, doc
   name) — if zero rows cite it, the mint was narrated, not executed.
3. Check the claimed timestamps against ledger rowids — narrated mints
   have no events, no `minted` lifecycle event, no claim.

This is the same evidence law as the R3 negation guard: a CLAIM of
work earns nothing; only the record of the work earns credit. The
integrity axis (rule 1) makes the ledger-side of this mechanical:
an outcome citing `gates/ghost_gate.py` scores 0 automatically.

## Judge-side design decisions worth keeping

- **Partial credit for unnamed artifacts (0.5), not 0:** a new
  requirement applied retroactively to legacy rows must distinguish
  "verified but not artifact-cited" (honest, older convention) from
  "cites a fabricated artifact" (fabrication). Full-zero retroactive
  rules create an unreadable census where everything looks like
  cheating; the 3-way split keeps the debt visible AND honest.
- **Selftest fixtures must model the NEW canonical outcome.** When a
  new axis raises the PASS bar, the "good task" fixture must satisfy
  the new bar (cite a real artifact) or the selftest fails with a
  0.897 PARTIAL that looks like a bug but is the design working.
- **Determinism vs variance are different quantities.** "Zero judge
  noise" (same input → same output) does not measure robustness
  (score stability under evidence paraphrase). Papers/audits that
  conflate them leave the interesting axis unmeasured.

## Where this lives in the the OS repo

- `gates/rubric_judge.py` — R9 integrity axis, selftest 10/10
- `gates/judge_variance.py` — V1 determinism / V2 paraphrase / V3
  ghost-split / V4 negation battery
- `gates/replication_pass.py` — independent re-run lane
- `stores/flow-registry.json` — FLW-REPLICATE curriculum flow
- `audit/QA-PASS-32-REPLICA-PAPER-2026-08-20.md` — full falsification
  record incl. the sibling-digest fabrication catch
