# Adversarial Gap Analysis Results: Veritas + Crucible Dual Pipeline

**Date:** August 3, 2026
**Reviewers:** the specialist engine (falsifiability), Systems Architect (operational), the specialist engine (human factors)
**Scope:** Design spec for twin research validation pipelines before code implementation

## Summary

- **37 total gaps** identified across 3 reviewers
- **7 CRITICAL** (must fix before code)
- **16 HIGH**
- **13 MEDIUM**
- **1 LOW**

## The 7 CRITICAL Gaps

### POP-002: No falsifiable claim of research superiority
The design cannot be proven superior to a single specialist pipeline without defined success metrics.
**Fix:** Define metrics per pipeline type:
- Veritas: peer review acceptance rate, citation index, expert consensus rating
- Crucible: GitHub stars on code repos, LinkedIn engagement, practitioner adoption

### POP-011: Surface validity trap
Process completes without error but produces garbage. All stages pass but content is wrong.
**Fix:** Ground truth verification gate in Stage 7. Every claim must trace to a real source with a quote.

### ARCH-001: Session crash loses in-flight state
**Fix:** Per-stage checkpointing to disk. RESOLVED in veritas_process.py and crucible_process.py.

### ARCH-002: No rate limiting on citation APIs at scale
At 50+ papers/month, citation APIs (arXiv, Crossref) hit rate limits.
**Fix:** Token bucket limiter per API. arXiv: 1 req/3s. Crossref/OpenAlex: exponential backoff on 429.

### ARCH-003: Federation handoff fails silently
No circuit breaker, retry logic, or degraded mode for cross-organism communication.
**Fix:** Circuit breaker pattern (3 failures opens circuit for 5 min). Fallback to single-organism mode.

### ARCH-006: Federation single point of failure
All cross-organism work flows through :port. If down, collaboration dies.
**Fix:** Passthrough mode on extended outage. Cache recent federation results locally.

### KAHN-002: Human-panel disagreement has no resolution protocol
When human disagrees with adversarial panel verdict, no process exists.
**Fix:** Human veto right with required justification. Veto triggers secondary panel review or logged override.

## HIGH Priority Gaps (top 5)

1. **POP-007:** Citation verification checks existence but not support. A real paper cited to support an unsupported claim passes. Fix: semantic similarity check between claim and cited abstract (reject if < 0.7).
2. **POP-005:** Panel consensus threshold undefined. Fix: 2/3 agreement or documented dissent.
3. **POP-003:** Evidence sufficiency threshold. Minimum: 5 peer-reviewed sources for Veritas, 3 implementations for Crucible.
4. **POP-010:** QA acceptance test suite. Mandatory checks: all citations verified, no hallucinated refs, logical structure complete, readability score.
5. **ARCH-004:** Engine "slow but not dead" cascades to timeout. Fix: per-stage SLA tracking, circuit breaker on 5 degraded calls.

## Reviewer Breakdown

- **the specialist engine:** 12 gaps (2 CRITICAL, 7 HIGH, 3 MEDIUM) - falsifiability, acceptance criteria, ground truth
- **Systems Architect:** 14 gaps (4 CRITICAL, 5 HIGH, 5 MEDIUM) - rate limiting, federation resilience, deadlock detection, observability
- **the specialist engine:** 11 gaps (1 CRITICAL, 4 HIGH, 5 MEDIUM, 1 LOW) - cognitive friction, voice overfitting, panel bias, conflict resolution

## Remediation Status

| Gap | Status | Fix Location |
|-----|--------|-------------|
| ARCH-001 | RESOLVED | veritas_process.py, crucible_process.py (checkpoint + resume) |
| ARCH-002 | RESOLVED | Citation verification subsystem (rate limiting built in) |
| POP-002 | PLANNED | Success metrics to be tracked post-publication |
| POP-011 | PLANNED | Ground truth gate to be added to Stage 7 |
| ARCH-003 | PLANNED | Federation circuit breaker (sibling-agent domain) |
| ARCH-006 | PLANNED | Federation passthrough mode (sibling-agent domain) |
| KAHN-002 | PLANNED | Human veto protocol to be added to output delivery |
