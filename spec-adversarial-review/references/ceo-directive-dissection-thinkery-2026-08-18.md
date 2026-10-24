# principal Directive-Message Dissection → Adversarial Design Review (2026-08-18, Thinkery)

Case study: a long ADHD-pattern principal voice message asked for an
adversarial design review + iterated plan of a studio section, with
explicit process constraints. Pattern below generalizes to any
directive-dense brainstorm/redesign request.

## Step 0 — Dissect the message BEFORE any review work

ADHD-pattern messages: dense, non-linear, self-repeating, mixing
directives with context and questions. Do not treat as one blob.

1. Transcribe the ask into a numbered directive list (D1..Dn), merging
   repeats, preserving EVERY unique point — the sender explicitly
   expects each one hit even though repeated ("hit every point even
   though I've repeated myself").
2. Classify each directive: build / review / question-back / constraint.
3. Constraints on the REVIEW ITSELF (no code changes, iterate the plan
   N times before returning, which philosophies must be respected) go
   into the review's own contract — violating them is a review failure
   even if findings are good.

## Step 1 — Ground-truth digest with live falsification

Before panels argue: mechanical digest of the artifact (grep the
codebase for each claimed capability; curl the live surfaces; count
lines/endpoints). Each implicit claim gets a falsification test
("X exists in surface Y" → grep for X in Y's code path). This session:
4 of 4 implicit claims about the studio's brainstorming section were
falsified or weakened — the entire finding set came from Step-1
evidence, not panel opinion.

## Step 2 — Multi-brain adversarial passes, one lens each

Route each pass through a DIFFERENT named specialist (physics-PM
decides routing, never asks the principal what's next):
- Falsification brain: claims → grep/live evidence → F#. 
- Architecture brain: monolith vs service boundaries, one-source-of-
  truth verdicts, bridge reuse, consent/data-flow direction.
- Usability brain: any-background-user walkthrough, progressive
  disclosure, keyboard-first, plain-words law.
- Motivation brain: points/lineage/streak integration with EXISTING
  engines (one-writer law — no new point physics).

## Step 3 — Plan artifact, versioned, with blocking questions capped

- Plan = phases × microtasks × gates, each microtask mappable to the
  task ledger.
- Cap blocking questions at ~3; everything else becomes a stated
  physics-PM default. The principal's explicit rule: "you don't need to ask
  me what you should do next" — decide and state the default.
- Version the plan doc (v1, v2...) and iterate internally per D13
  (many planning→QA loops BEFORE the principal sees it).

## Step 4 — Pen-in/pick-up discipline

When the directive says pause existing work ("put a pen in it"):
write the resume guarantee FIRST (ledger + persistent memory record of
in-flight items) before starting the new thread. Lost morning work is
a worse failure class than a late plan.

## Pitfalls found this session

- Session paths go stale across compaction: verify the canonical repo
  location by locating a known gate file (`find -name surgical_gate.py`)
  before ANY ledger read — a pruned mirror produced a 0-byte ledger
  read and a false "catastrophic data loss" alarm. The org repo was
  intact; the panic was the defect.
- the operator agent-internal gates (specialist-gate expiry, baseline-first,
  blocked-script cache) fire on long design sessions: re-route through
  specialist_gate.py whenSherman expires >5 min; park refused writes as
  references/pending-*.md; run blocked heredocs from the saved cache
  path.
