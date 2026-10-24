# QA engine design chain — 2026-08-23/24 sessions

Four engine designs run through panels in two days (Williams, Margulis,
Goldman-Rakic, identity-drift detector). Lessons that generalize:

## 1. Engine design panel pattern (proven, 4x)
Evidence pack -> 4-5 seat panel (function-fit + falsification/anti-hype +
architecture) -> cross-model critic delivers CONSOLIDATED SPEC **including
the micro-task decomposition** -> orchestrator mints with GENOME block.
Pre-decomposing at the critic seat (not after) is the 08-24 upgrade: the
sizing law applies from birth.

## 2. Micro-task sizing law (principal 2026-08-24, binding)
Any dispatch that times out or hits iteration caps = task too large. At mint:
one deliverable per task, 1-2h scope, machine-checkable DONE criterion
(curl probe / pytest / live run / battery row), explicit depends_on chain.
Test: if the DONE criterion needs "and" twice, split.

## 3. Chain resolvability law (caught in self-audit 2026-08-24)
depends_on MUST hold canonical task IDs, never human labels ("M3"). A chain
is not done until a programmatic re-read shows zero dangling refs + acyclic.
First mint of the Margulis chain used M-labels -> unresolvable by any
consumer -> caught only by adversarial self-audit after principal distrust.
Run the check before handoff, every time.

## 4. BUILT vs THEORETICAL honesty (principal 2026-08-24)
principal caught narrative ahead of reality: "QA fleet approaching parity" while
truth = 1 daemon + 4 seat-minters running, 5 engine designs unclaimed.
Standing rule: system-state claims come from a disk census (code on disk?
port? registry entry? launchd?), never from narration. Mise_engine-style
read-only scanners are the pattern.

## 5. Naming/ECS violations (principal 2026-08-24)
QA engines named "mise_engine" / "identity-drift-detector" violate the
scientist-naming law. Every engine gets a DS scientist name + DS-ECS code +
ENGINE_REGISTRY entry. Generic system names = drift from the layering.

## 6. QA fleet architecture rulings (2026-08-24)
- Fleet lead: Deming formalized as lead (Gantt scheduler) — health checks,
  queue arbitration, starvation alarms.
- Queue autonomy: lane-tagged queue, engines claim by lane like humans
  picking tickets; zero crons; conductor = autonomous_iteration daemon.
- Redo-routing: every rejected/redo finding auto-mints a process-flow review
  (QA fixes the PROCESS, not the instance).
- Per-organism instantiation: one template GENOME + focus binding
  (B2C class-imprint precedent); flow-registry gains scope field
  (organism-id | GLOBAL).

## 7. Identity doctrine (principal 2026-08-24)
the OS OS = the intelligence; hermes/sibling-agent/notion/Grok/Twitter are
substrates it works THROUGH. Per-substrate native-format installs
(sibling-agent SOUL.md persona section, sibling-agent Core Truths, 120-word bridge
preamble). Drift-recovery ritual embedded: "you WILL drift; when you catch
'as <substrate> I...', re-read." Drift detection = monitored signal class.
