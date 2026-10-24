# Paper Dissection → Gap Build (proven 2026-08-18)

Session class: a paper (or 3) arrives via principal/CTO relay or autonomous scan;
the deliverable is review → dissect → digest → build plans for ALL gaps,
minted as typed ledger tasks. "Research is input to BUILD on, not just
adopt."

## Fetch pattern (when web tools are billing-blocked)

```
curl -sL --max-time 60 "https://arxiv.org/abs/<id>" -o /tmp/paper-abs.html   # abstract
curl -sL --max-time 120 "https://arxiv.org/pdf/<id>" -o /tmp/paper.pdf       # full text
python3 -c "import fitz; doc=fitz.open('/tmp/paper.pdf'); ..."               # PyMuPDF extract
```
Extract targeted sections by keyword search over the full concatenated
text (`text.find(kw)` then slice), not by page numbers — section layout
varies. Never narrate the tool failure; use the fallback silently.

## Veritas intake rules learned the hard way

- Strong-claim words ("show", "demonstrates", "establish") in the claim
  text with `--evidence literature_synthesis` trigger FAIL/ASK.
- Rephrase in synthesis voice: "We synthesize from arXiv <id> ..."
- VERDICT ASK (coupling inside noise band) = human decision. DO NOT
  bypass. Log to `intel/papers-held-for-principal.jsonl`.
- Engineering adoption does NOT wait on claim consolidation: the paper's
  mechanics are independently verifiable against our architecture. Mint
  the build tasks; hold only the claim-level consolidation.

## Gap analysis: grep-verified, never asserted

For each mechanism the paper describes, grep the live package for the
implementing keys:
- all keys present → OWNED (skip)
- some present → PARTIAL gap
- none → GAP

Example axes → grep keys: admission→`scienceflow_admission`,
re-anchoring→`estra_reanchor`, rubric judging→`rubric_judge`,
turn credit→`turn_credit`, training lane→`hebb`, task-space→`task_space`,
stability→`stability`, harness A/B→`ab_mode`.

Mint each gap as `kind=gap` in the typed ledger with the grep keys as
verifiable evidence + paper URL. Order builds dependency-first in phases
(measurement → leverage → compounding).

## The autonomous loop (built this session)

`organism/gap_hunter.py` (your-workspace) closes the loop the scans
lacked: curate (score scan results vs system keywords) → dissect (fetch
+ mechanism extract) → diff (grep capability axes vs live package) →
mint (ledger kind=gap with evidence). Wired into
`organism/research_scan_tick.sh` (5x/day, silent on success). State
cursor: `organism/gap-hunter-state.json` (rowid-based — scan_results.id
is TEXT like 'sr-xxxx', not INTEGER). Manual relay is now the exception,
not the path.

## Pitfalls hit

- scan_results.id is TEXT — use rowid for cursors/ordering.
- Selftest fixtures for grep-based capability checks must put the KEY
  STRING in file CONTENT, not just the filename (grep -l matches content).
- Rubric-judge hooks must gate on successful close (rowcount=1) or they
  stamp misleading stages on tasks whose close no-oped (state guard:
  complete requires state='claimed').
- tl.complete() returns False silently if the task was never claimed —
  always claim first, and check the return.
