# Skill Rubric Field Spec (living rubrics)

[sibling-agent | the specialist engine (DS-ECS-CEL-07.03.01-v1.0.0) | skill-library curation | physics-PM mode]

Adopted T-261004-0075 (build station, first pass; seq 8 — Arana/NVIDIA
Skill2Env: practitioner-written skills carry enough structure to become
tests; the strongest argument for skill repositories is not training, it
is what a properly written skill BECOMES: reusable capability + evaluation
asset + behavioral contract).

## Field definition

A skill's rubric is the measurable-criteria companion to its procedure:

| Part | Contains | Falsifiable form |
|------|----------|------------------|
| MUST | 2-5 criteria for correct execution | exit code, count, schema field, rendered artifact — checkable by a reviewer or script |
| MUST-NOT | failure modes the skill prevents | each maps to a documented pitfall; violation is observable |
| GOOD-LOOKS-LIKE | concrete definition of excellent output | a reviewer can score pass/fail without judgment calls |

Placement: in the skill body under `## Rubric` for short rubrics, or
`references/rubric-<skill>.md` for long ones. SKILL.md must link it either
way. Ownership + versioning ride the existing skill-directory structure
(git history = versioning; governing umbrella = ownership).

## Evolution rule (living)

- Skill misfires in a session -> the SAME curation pass updates the rubric.
  The rubric is where "evolve by use" lands.
- Rubric/body divergence = drift; reconcile in one change, never leave
  them split.
- Population is adiabatic: add rubrics when a skill is next touched; no
  mass edits. Census metric: skills-with-rubrics % (genome 8D coherence
  metric for T-261004-0075).

## Why measurable criteria (physics)

GENOME physics for T-261004-0075 (DS O'Keefe seat): retrieval probability
of a procedure decays without context anchors; a rubric is the context
anchor that keeps a skill's criteria findable and load-bearing long after
authoring. A skill without measurable criteria cannot fail a test, so it
cannot be falsified, so its "done" claims are decorative (FALSIFIABILITY
BUILD GATE alignment).

## External validation

- NVIDIA Skill2Env (Arana intake, verified boards/archive/seq-08 +
  gg_retry_jobs.py + ds-barry ledger): 3,400 public Agent Skills ->
  ~8,000 executable environments with rubrics derived from the skill text;
  +4.7 Terminal-Bench 2.1 after 300 RL steps. Method-rewarding vs
  outcome-only cost points but produced behavior closer to the skill —
  rubrics encode the method, not just the outcome.
- Format note (seq 22, doc-validation only — source NOT independently
  verified, scope-dropped at review station #71980): external curated
  knowledge as markdown (OKF-style) is format-compatible with our
  SKILL.md exchange format; markdown skills remain the interchange unit
  for external knowledge exchange.

## Seed state (2026-10-06)

- skill-library-curation: rubric seeded inline (exemplar).
- Coverage baseline: 1/~200+ skills — census metric live, no mass edit.
