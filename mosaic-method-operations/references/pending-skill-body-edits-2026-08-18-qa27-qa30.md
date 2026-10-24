# Pending SKILL.md body edits 2026-08-18 evening (QA-27 + QA-30)

Parked here because _read_before_write refuses edits to existing SKILL.md
bodies (verified 08-18; fresh skill_view does not satisfy the guard). Apply
via curator when the guard is lifted. Both references exist on disk now.

## mosaic-os-architecture SKILL.md — add to Session References list:

- `references/persona-variation-qa-pass-27-2026-08-18.md` — five-source
  declarative-vs-operative audit method (registry/engines/pins/router/
  FLEET_REGISTRY/agents.yaml cross-check); findings M1-M8 incl.
  sherman_router never reading personas/registry.json, L9 variation column
  unenforced, Osler/Bernard ECS collision; persona coverage 25/86.

## your-stack-operations SKILL.md — add to References list:

- `references/qa-pass-30-fresh-brain-rotation-2026-08-18.md` — principal directive:
  DIFFERENT specialist brains per audit phase on repeat QA passes (5-phase
  rotation Tawara/Codd/Kuramoto/Popper/Harvey recorded in report header as
  L9 dogfood); registry-vs-doc vocabulary audit method; sticky-error health
  semantics (read last_error + cycle count together); QA-pass numbering
  collides across parallel sibling sessions — grep RUN-RECORD before naming.

## Also worth adding to your-stack-operations pitfalls (body edit):

- QA-pass report numbering: siblings mint passes in parallel; before naming
  audit/QA-PASS-N, `grep -o "QA pass [0-9]+" audit/RUN-RECORD.md | sort -u`.
- specialist_gate routing window is 5 minutes; long probe phases can outrun
  it — re-route before the consolidation write step.
