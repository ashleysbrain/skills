# Different-brain QA ladder (validated MR6-MR9, 2026-08-18, Connection Hub)

User demands: "thorough qa pass, different brain, mosaic methodology". The
ladder that worked on one artifact (32-surface connection hub + services):

1. BUILD (the specialist engine): coverage expansion + layout. Produces the claims.
2. ART DIRECTION (the specialist engine): hierarchy, info scent, plain language, brand,
   density. Found: jargon in footer, status vocabulary not plain.
3. CLAIM FALSIFICATION (the specialist engine, report-only): attack every live claim with
   measured probes; never repair. Found: wildcard bind, fonts egress,
   quarantine write amplification, tracked live DB. Graded C.
4. SYSTEMS TOPOLOGY (the specialist engine, report-only): persistence, SPOF, backups,
   retention, failure modes. Found: no backup (HIGH), uneven busy_timeout,
   zombies, unbounded growth.
5. STATE/ORDERING (the specialist engine, report-only): cross-store consistency, event
   ordering, id contracts, source-of-truth. Found: surface-id drift, stale
   census fields, ts heterogeneity.

Each brain found a defect class the others structurally could not: reviewers
see the surface, falsifiers see the claims, systems brains see the failure
modes nobody triggered yet. Builder NEVER reviews own build.

## Rules that made it work
- Mechanical digest (probes, drift checks, live state) BEFORE any brain argues.
- Report-only auditors + operator lane fixes after, each fix re-verified with a
  live probe (never a code read).
- FREEZE DISCIPLINE (Popper's process finding): remediation landing mid-audit
  churns the auditor's evidence landscape (PIDs, paths shift under their
  battery). Land fixes BETWEEN passes; if concurrent, the auditor must
  timestamp-anchor everything (costly).
- Salvage over re-dispatch when a pass times out: extract from transcript,
  verify, file with honest disposition.

## Payoff metric
Passes found: pass2 = 6 lanes of UI defects; pass3 = 8 defects incl. 3 sev-2;
pass4 = 10 topology gaps incl. the only HIGH; pass5 = 6 state gaps incl. the
two deepest structural ones (id contract, status source-of-truth).
