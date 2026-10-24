# Revenue Crisis Panel — 9-Seat Sequential Chain (2026-08-20)

Run: 9 seats, sequential chain-of-custody, glm-5.3 elite lane, runway <1 month
(principal-confirmed crisis mode). Files live in `your-workspace/revenue-panel/`.
Evidence pack built from template `templates/strategy-panel-evidence-pack.md`.

## Roster + landing order
| # | Seat | Mandate delta (beyond uniform §7) | Status at review |
|---|---|---|---|
| 1 | Jamie Dimon — crisis arbitration | ≤14 vs ≤30d cash classes; daily non-negotiable; zero-conversion stress test; 30-day freeze list | LANDED, gate PASS |
| 2 | Madhavan Ramanujam — pricing | pressure-test price points; package design; payment structure; pre-decided discount ladder (ADHD principal — no live math) | LANDED, gate PASS |
| 3 | Elad Gil — unit economics | pilots/month capacity; 90-day system math; services-vs-grants interaction; concentration risk; weekly metric | LANDED, gate PASS |
| 4 | Aaron Ross — pipeline/ICP | exact buyer; 30-target list in 2h no paid tools; copy-paste email skeletons; cadence; day-14 falsifier | in flight |
| 5–8 | Thompson / Karpathy / Kozyrkov / Fogg | value capture; research→notoriety; kill metrics; principal execution system | pending |
| 9 | the specialist engine falsify → the specialist engine consolidate | falsify converged plan, then ONE dossier | pending |

## Chain mechanics that worked (the reusable part)

1. **Chain-state file** (`revenue-panel/PANEL-STATE.md`): table of seats,
   persona-source paths, status, verdict-file paths, delegation IDs + all run
   rules. Written BEFORE seat 1 dispatch, patched after every landing. Any
   compaction/interruption resumes from it without re-deriving anything.
2. **Per-seat loop, exact order:** batch-complete →
   (a) `read_file` the verdict file (subagent self-report ≠ proof; summaries
   in the batch-complete message are head+tail truncated — the FILE is the
   deliverable) → (b) `brain_integrity_gate.py <delegation_id> "<expected
   persona>" elite` → (c) patch the state row to LANDED+GATED → (d) dispatch
   next seat whose brief lists ALL prior verdict paths in order.
3. **Anti-re-litigation inheritance:** each next seat's brief opens with what
   prior seats ruled and states the boundary explicitly ("do not re-arbitrate
   sequencing — price what he ranked"). Prevents chain thrash; keeps each
   seat additive.
4. **Uniform contract + per-seat mandate deltas:** every seat answers the
   same §7 shape (verdict / ranked top-3 / one kill / setup install /
   UNVERIFIED flags, <800 words) PLUS a seat-specific (a)–(e) mandate matched
   to its specialty. Comparability across seats + depth per specialty.
5. **One binding parameter, surfaced once:** runway number asked in a single
   clarify BEFORE seat 1, then locked into the pack. Seats never re-ask the
   principal; they flag UNVERIFIED instead.
6. **Convergence checks validate the chain:** Ramanujam's negotiation floor
   ($7.5K) independently converged with the advisor's economic floor — cited by both
   as "convergence, not coincidence". When two seats' independent math meets,
   bank it as a load-bearing number.

## Pitfalls hit (all resolved in-run)

- **Evidence pack needs its own QA before seat 1 reads it:** two typos
  (stray token in §6, sloppy path) were patched pre-dispatch. Seats inherit
  pack errors verbatim.
- **Sibling-edit warning on the chain-state file:** a patch returned
  "_warning: modified by sibling subagent" (a seat had self-routed its
  specialist gate, touching shared state). Rule: read-before-write on
  chain-state, verify the sibling change is benign, keep going.
- **Seats hitting their own local write-gates is normal:** seat 2 was blocked
  by a baseline-first gate on new-file write and self-resolved by pre-creating
  the file/dir. Not a failure — note it in the landing summary and move on.
- **Dispatch context as ordered file pointers, not prose:** every brief =
   numbered file list (pack → prior verdicts in order → persona file →
   strategy locks → chain state) + "if a path 404s, search by distinctive
   filename substring". Zero inline file bodies = zero corruption surface.

## Notable rulings (context for the dossier consolidator)
- Dimon: "built a factory, never sent an invoice" — behavior gap, not
  strategy gap; 3 touches/day before any build work; B2C killed 30d.
- Ramanujam: price card list $12K / partner $9.5K / floor $7.5K; trades not
  gifts; only permitted in-call sentence pre-decided.
- the advisor: 2 pilots/mo hard cap (principal hours bind, not fleet); $28–40K by day 90 =
  bridge to SBIR window; weekly metric = cash collected; newsletter killed.
