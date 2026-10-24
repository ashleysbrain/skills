# Enforcement-Before-Proof (2026-08-17, the OS CI)

## The two catches, same session, same class

**Catch 1 — "CI runs it on every push."**
PROC-FLOWS.md Flow 7 and a ledger close-record both claimed the
surgical gate's chain-ok step "runs on every push" immediately after
the workflow file was committed. The wiring commit itself turned CI
red (run 32066387826): the new selftest had a real defect
(insertion-edit verify semantics). The enforcement claim was written
BEFORE any green run existed. Grade B as worded; the evidence arrived
only with green run 32067283844 four commits later.

**Catch 2 — minted-in-the-past task IDs.**
An O'Keefe memory note (persistence layer) stated layer gaps were
"minted T-260817-0016..0021" while only -0016 actually existed. The
sequence had been PLANNED in the note and read back as DONE. Corrected
by re-minting honestly (-0017..-0022, in ledger order) and closing
them with real outcomes.

## The rule

An enforcement/integration claim graduates from B to A ONLY when:
- the first GREEN run ID exists (CI), or
- the log/DB row exists (scheduled jobs, events, ledger mints).

Merged config is intent. The claim is written AFTER the run ID, never
before. If you must reference the wiring before it proves itself, say
"wired, first run pending" — that phrasing survives audit.

## Why this bites harder than spec-as-build

The plausibility trap is stronger: the workflow file IS real, the step
IS in the YAML, the commit IS pushed. Everything is true except the
verb tense. "Runs on every push" (present, continuous) vs "is wired to
run" (config state). Same class as crontab-theater (schedule is not
function), one layer deeper (merged config is not green run).

## Verification command pattern

`gh run list --limit 1` after every push; cite the run ID + conclusion
in the run-record. A ledger close outcome that cites a run ID must
match a run that concluded success.
