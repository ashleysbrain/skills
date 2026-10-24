---
name: dual-process-research-pipeline
description: Use when building VERITAS or CRUCIBLE research pipelines.
---

# Dual-Process Research Pipeline (VERITAS + CRUCIBLE)

## When to Use
Building or maintaining the 7-stage research validation pipelines that route through the operator agent organism engines. VERITAS validates academic research (GG3/the principal). CRUCIBLE validates technology research (Cyber the operator agent/the principal).

## Architecture

### VERITAS (Academic Pipeline)
- **Location:** `/<workspace>` (970 lines)
- **Repo:** `gigi3/organism/veritas_process.py`
- **Organism:** GG3 (the principal), host ports 8xxx block
- **Voice:** the specialist engine, 8D wellness focus
- **Panel:** 8 seats (Popper, Kahneman, Wernicke, Luria, Goethe, Bell, Harvey, domain expert)
- **Run:** `python3 veritas_process.py --health-check` (ON HOST, not in Docker)
- **Full run:** `python3 veritas_process.py --idea "..." --evidence-level theoretical --output-formats arxiv,linkedin`

### CRUCIBLE (Technology Pipeline)
- **Location:** `/<workspace>` (1542 lines)
- **Repo:** `cyber-gg-blueprint/crucible_process.py`
- **Organism:** Cyber the operator agent (the principal), container ports 9xxx block
- **Voice:** INTJ/technical/The Creator
- **Panel:** 9 seats (adds Security/Red Team + Systems Engineering + Bentham utility)
- **Run:** MUST run inside Docker container: `docker exec cyber-gg-8400 python3 /app/crucible_process.py --health-check`
- **Full run:** `docker exec cyber-gg-8400 python3 /app/crucible_process.py --idea "..." --evidence-level theoretical`

## Port Blocks (Critical)
- **GG3 engines:** 8xxx on HOST (8108, 8124, 8120, etc.) - run VERITAS on host
- **Cyber the operator agent engines:** 9xxx INSIDE container (9108, 9124, 9120, etc.) - run CRUCIBLE inside Docker
- **Do NOT run VERITAS inside GG3 Docker** (8xxx ports are not mapped into container)
- **Do NOT run CRUCIBLE on host** (9xxx ports are not mapped out of container)

## 7 Stages (Both Pipelines)
0. Evidence gate (reject insufficient evidence levels)
1. Topic refinement + engine health check
2. Research gathering (arXiv, OpenAlex, Crossref citations)
3. Physics validation (free energy, Kuramoto, critical slowing, Bayesian)
4. Adversarial panel (sequential, not concurrent)
5. Internal revision loop
6. Multi-format output generation
7. Human review touchpoint

## Engine Health Gating
Both pipelines PAUSE and checkpoint if any required engine is DOWN. They do NOT produce output with dead engines. This is the core design principle.

## Gap Analysis
37 gaps identified (7 CRITICAL, 16 HIGH, 13 MEDIUM, 1 LOW).
Full analysis: `/<workspace>`

### 7 CRITICAL Gaps (must fix)
1. No falsifiable success metrics defined
2. Surface validity trap (garbage passes through stages undetected)
3. No crash recovery beyond checkpointing
4. No API rate limiting (will fail at 50+ papers/month)
5. Federation single point of failure (no circuit breaker)
6. Federation redundancy missing
7. No human escalation/veto protocol

## Federation (NOT YET BUILT)
- GET `/api/federation/status` works on both containers (200)
- POST `/api/federation/handoff` returns 501 on both (sibling-agent task)
- Federation server (:port) not running
- :port port conflicts with the specialist engine on host

## Pitfalls
- Cyber the operator agent engines asleep: Andreasen, O'Keefe, Friston, Kuramoto, Harvey need waking inside container
- VERITAS copied into GG3 Docker will show all engines DOWN because 8xxx ports are not mapped in
- Crucible on host will show all engines DOWN because 9xxx ports are not mapped out
- Always verify which environment you are in before running health checks
