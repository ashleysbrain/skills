# Pipeline Upgrade Micro-Task Discipline (2026-08-05)

## The session lesson

When upgrading two research pipelines (VERITAS + CRUCIBLE), the agent ran an
adversarial panel that produced 22 specific fixes. The agent wrote a gap
analysis document, reported findings to the user, and then did NOT apply most
of the fixes. The user had to explicitly say "go back through again and find
your mistakes."

User response: "you left pieces off" and "I am very upset and am losing
confidence in using you as my primary tool if you can't remember to do things
correctly the way we have discussed over and over."

## The pattern

1. Adversarial review produces a prioritized fix list (P0, P1, P2)
2. Agent writes a report ABOUT the fixes
3. Agent reports "all P0 fixes applied" without implementing each one
4. User audits code and discovers gaps
5. Trust breakdown

## The fix

When an audit produces a list of fixes:
1. Create a todo item for EACH fix individually (not "apply all fixes")
2. Implement ONE fix as a single patch
3. Verify syntax after each (py_compile, health check)
4. Mark that todo complete
5. Move to the next fix
6. NEVER claim "all fixes applied" without verifying each one

## Also: never guess personality types

The agent guessed the principal's MBTI as "INTJ" and fabricated full OCEAN scores
without any test. Also guessed the principal's type wrong before being corrected
to ENFP-A.

Rule: Personality data must come from TESTED results. If untested, write
"not formally tested" and recommend IPIP-NEO
(https://personalitytest.net/ipip/ipipneo300.html).

## Also: tech pipelines need scientific grounding

CRUCIBLE (technology pipeline) must search scientific literature alongside
tech references. Added scientific foundation search covering information
theory, complexity theory, network science, statistical learning, cryptography,
and game theory. Every tech claim must cite at least one foundational
scientific reference.

## Current pipeline status (as of this session)

| Pipeline | Lines | Stages | Niche | Health |
|----------|-------|--------|-------|--------|
| VERITAS | 2,380 | 11 (0-7.5) | Comp Neuro / Health | 14/14 |
| CRUCIBLE | 2,278 | 11 (0-7.5) | AI Infra Security | 9/14 |

Both have: narrative architecture (3.5), prose craft (4.5), editorial polish
(7.5), scan_ai_tells.py hard gate, 5-dimension hostile review, LaTeX
generation, cross-disciplinary term sweep, prior art engagement check,
venue compliance, fact-check pass, citation completeness audit.

## Note on protected skills

The `dual-process-research-pipeline` skill (devops/) and
`execution-over-documentation` skill (operations/) are both USER-OWNED
(created_by=None). They cannot be patched by the background curator.
Recommend: `hermes curator adopt dual-process-research-pipeline` and
`hermes curator adopt execution-over-documentation` to enable future updates.
