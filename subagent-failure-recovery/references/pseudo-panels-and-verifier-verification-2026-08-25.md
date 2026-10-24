# Pseudo-panels, unbound personas, verifier-verification (2026-08-25)

Companion to `takeover-ban-and-boundary-attribution-2026-08-25.md` from the
same session. Three fabrication-class failure modes caught by the principal, plus
the repair patterns that worked.

## 1. Pseudo-panels (Q2 violation)

The principal's original suspicion: "'elite' is going to be a lie... something
baked in as a standardized message output and not actually factual live
data." The routing audit (pulled from actual delegation manifests) proved
it: **no named specialist ever executed the work.** "the specialist engine design
seats," "10-brain panels" — every one was ONE generic glm process with
role-prompts, or one subagent writing N sections.

Laws minted (task ledger, Q1/Q2):
- **Panel claims = dispatch counts.** "Panel of N" requires N real dispatch
  records with distinct processes.
- **One model in N roles must be labeled exactly that** in every output's
  honesty header: "1 process, N role seats, model X." Persona names in
  headers without bound dispatch = narration fiction, fabrication class.
- Static quality labels ("elite") are banned from outputs unless computed
  from live ledger data (grades from QA history, decaying with performance).

## 2. Verify the verifier (the layered-catch pattern)

The session's flow sweep ran Pass A → B → C → adversarial panel, and errors
appeared at EVERY layer, each in a different direction:
- Pass A (self-executed, protocol violation): magnitudes inflated 2–28×
  (counted cancelled as open), one failure class missed entirely.
- Pass B: correct mechanisms, wrong magnitudes (inherited A's counts).
- Pass C: caught B's magnitudes, but its own flagship refutation ("23/24
  FLW-HANDOFF closes are ghost-replay duplicates of one message") was
  FALSE — a direct ledger check showed 23 distinct titles, zero matching
  the claimed message, all with outcome records.
- The panel: killed one sub-claim ("35/52 paper flows" unreproducible),
  amended all five fixes.

**Rule: the parent must spot-check the FINAL pass's key numbers against the
raw store before reporting them upward.** Multi-pass does not converge to
truth by depth alone; each layer needs one direct-data check from the
orchestrator.

## 3. Snapshot-path rumors propagate between subagents

Two different subagents in the same campaign independently reported "both
live task-ledger.db files are 0 bytes." The live ledger was 2.6MB / 1,842
rows, readable at that moment. One subagent's stale-path assumption entered
the shared context and the next one repeated it as established fact.

**Rule: any claim about a live store's readability is verified by the parent
touching the store directly** — `os.path.getsize` + one query. A specific
snapshot citation makes a subagent MORE credible-sounding, not more correct.

## Repair pattern

For bypassed/narrated work: re-dispatch the analysis step as a genuinely
independent process whose explicit mandate includes judging whether the
bypassed output distorted anything (verdict vocabulary: clean / biased-toward
X / missed Y). The repair dispatch — not the apology — closes the incident.
