PENDING REPLACE: this file's content should replace `references/multi-pass-fresh-brains-protocol.md`
(which currently holds only the literal string "placeholder" — see REPLACE note at bottom).

# Multi-Pass Fresh-Brains Protocol for Spec/Plan Adversarial Review

Session-proven pattern (2026-08-18, thinkery collab ADR v1→v3): when a principal asks for
"another thorough QA pass" on a plan/spec, each pass MUST use DIFFERENT specialist
brains with DIFFERENT attack vectors. Reusing the same panel produces diminishing
returns — pass 2 (Tanenbaum/Lamport/Popper) found ontology violations; pass 3
(Feynman/Harvey/Cannon) found circulation and testing defects pass 2 walked past.

## The pass-to-brain rotation (each brain owns ONE attack vector)

| Brain | Attack vector | What it asks |
|---|---|---|
| the specialist engine | Falsification | "What live probe would refute this claim?" Run it. |
| the specialist engine | Ontology/isolation | "Does this create a second namespace / violate invariants (I1-I11)?" |
| the specialist engine | Event ordering | "Is the ordering claim real or decorative naming?" |
| the specialist engine | Simplicity / stranger test | "Can the whole plan be said in one breath? Do referenced files EXIST on disk?" |
| the specialist engine | Circulation loops | "Trace one unit of work end-to-end. Where does the loop FAIL TO CLOSE?" |
| the specialist engine | Failure homeostasis | "Where are the pain receptors? What breaks SILENTLY?" |

Key insight: each brain's question is orthogonal. Popper refutes claims; Feynman
refutes file-existence and complexity; Harvey finds OPEN LOOPS (write path exists,
read path never fires); Cannon finds MISSING SIGNALS (no CI, no janitor, silent expiry).

## Highest-yield techniques found across passes

1. **Registry-name tracing (Feynman, pass 3).** Docs reference registries by name
   (e.g. "FLEET_REGISTRY") that do not exist as files. NEVER join a design to a named
   registry without `find`-tracing it to an actual file on disk. In this session the
   canonical registry turned out to be `federation_state.json` + `agents.yaml`, and
   2 of 3 roster rows were ghosts pointing at nonexistent organisms.

2. **Recipient census on message buses (Harvey, pass 3).** When a plan says "X reads
   from the bus", run `SELECT DISTINCT to_op FROM messages`. If the intended reader
   class has ZERO historical messages, the loop has never closed and the feature is
   half-built plumbing. Fix pattern: require a round-trip ack event as the done-test.

3. **Test-floor check (Cannon, pass 3).** Before planning build layers on a repo,
   check `.github/workflows/` existence and `grep -c "def test_"`. A body with no CI
   gets an M0 "CI floor" layer inserted FIRST — every later layer's done-test rides
   on it. Law: a layer without a failure signal is not done.

4. **Consumer-naming for event taxonomies (pass 2).** Every proposed event type must
   name its consumer at design time. Zero-consumer event types are deleted, not
   shipped. ("Classified-but-not-consumed" applied to event streams.)

5. **Anti-decoration for distributed-systems terms (pass 2).** "Lamport-ordered",
   "CRDT", "exactly-once" in a single-writer design = decorative naming that violates
   the anti-decoration law. Use plain names (monotonic seq) until the second writer
   is measured to exist.

6. **Estimate striking (pass 2).** Hour estimates in a plan that hasn't started are
   invented numbers. Strike them; record measured effort after each layer completes.
   Keep only the relative free-energy order.

7. **Locked-doc gating (pass 2).** If any layer touches organism spin-up/trust/
   reproduction (external organisms, federation), gate it on reading the locked
   WOMB-ARCHITECTURE.md FIRST plus an explicit principal trust-model decision.

## Cross-pass consolidation rule

Each pass folds its findings into the SAME canonical ADR/doc (v1→v2→v3) with a
changelog table: finding #, brain, severity, what the prior version said, the fix.
Never spawn a competing doc. Close the pass's ledger task with the outcome; leave
principal decision questions in a numbered open-questions section (they accumulate across
passes — new passes may add questions, never silently resolve them).

## Commit discipline observed

One commit per artifact change (ADR commit, run-record commit), pushed; CI verified
green on the last code-bearing commit (docs-only commits may be paths-filtered out
of CI — check `gh run list` headSha against your commits before claiming "CI green
for this commit").

REPLACE: delete this pending file after copying its body over
references/multi-pass-fresh-brains-protocol.md (which is a bare "placeholder").
