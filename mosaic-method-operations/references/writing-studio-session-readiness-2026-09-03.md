# Writing Studio / Research Lab session readiness (2026-09-03 principal co-working session)

Recipe + traps for verifying the studio pipeline is REALLY ready before
telling the principal "we can brainstorm now". Born from the principal challenge:
"are you ready or are you just telling me that as the operator agent?"

## Service facts
- Pipeline API runs as launchd KeepAlive agent `com.your-org.pipeline-api`
  (program: hermes venv python, `pipeline_api.py --port <studio-port>`).
- Auth: `WRITING_STUDIO_TOKEN` loaded from `<agent-home>/.env` (Bearer).
- Route truth = `GET /openapi.json` (199 paths). Do NOT guess route names or
  methods — probe the spec first. Traps hit live:
  - `/api/publication/venues` exists; `/api/publications/venues` also exists
    but returns a DIFFERENT shape — read the openapi entry for the method
    before calling. Several research endpoints are POST-only (405 on GET).
  - Health double-check: `/api/pipelines/health` (status ok, run counts).

## Model registry vs call path (BUILT-INERT trap)
- `writing-studio/model_registry.json` is DATA; `pipeline_api.py` holds the
  CALL PATHS. Adding a model to the registry makes it appear in
  `/api/harness/models/live` WITHOUT any ability to run it — an inert
  listing that looks like a capability. Verified case: added
  `xai/grok-4.20-reasoning` to the registry; `grep -c 'xai' pipeline_api.py`
  returned 0. Such additions MUST ship with an activation ticket
  (pattern: ACTIVATE task, closes only on real returned content through the
  studio, never on a registry read). Backup the registry before editing
  (`*.bak-pre-grok-260903` pattern).

## Verified capability lanes (as of 09-03)
- Grok live-news research: works through the HARNESS x_search tool
  (provider xai, credential_source xai-oauth, model grok-4.20-reasoning) —
  proven with a real current-week scan. Studio-NATIVE grok calls: NOT built
  (see activation ticket). Report these as separate facts.
- LLM 5.3 = elite drafting lane (registry, live).
- Venue registry (`/api/publication/venues`) holds ACADEMIC weights only
  (nature/arxiv/neurips class) — NO WIRED / TechCrunch / MIT TR entries.
  Any consumer-tech op-ed plan needs venue entries added first.

## Interrupted side-effect recovery
- A POST that gets interrupted (tool timeout / operation interrupt) leaves
  UNKNOWN state. Before retrying: read the resource list endpoint
  (e.g. `/api/research/scans`) and check whether the run/scan actually fired.
  Never count an interrupted POST as done or dead without the read.

## Session preferences (principal, 09-03)
- Content and outline BEFORE title. Title candidates first = wrong order;
  the title emerges from the writing ("Internet of Models" is too narrow as
  a title; use it as one face of a broader adaptive-composition thesis).
- Drafts are created through the studio surface (`POST /api/drafts`), not in
  chat — chat scaffolds are not studio state.
- principal wants a process-audit engine monitoring flows DURING live sessions;
  readiness claims must carry named gaps, not just green checks.
