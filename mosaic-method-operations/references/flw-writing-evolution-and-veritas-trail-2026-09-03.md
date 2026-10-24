# FLW-WRITING v0.2 Evolution + Veritas Trail Discipline (2026-09-03)

## 1. Flow evolution law (principal 2026-09-03 10:43)
"As the systems evolve, the process flow needs to evolve... without me
having to call it out." When any routing/admission mechanism is replaced
ecosystem-wide (e.g. Sherman route -> physics admission gate + TRI station
routing), the SAME pass must scan every registered flow for the stale
mechanism — the propagation scan is PART of the edit, not an afterthought.

Recipe that shipped FLW-WRITING v0.1 -> v0.2:
1. Census `stores/flow-registry.json` for the outdated mechanism
   (`json.dumps(f).lower()` match) — 59 flows, found 3 Sherman refs.
2. Classify each hit: legitimately owned (FLW-DISPATCH, FLW-ADMISSION —
   Sherman IS the router organ; route/gate is its own flow) vs stale
   consumer (FLW-WRITING — only true outlier).
3. Backup registry (`cp flow-registry.json flow-registry.json.bak-<tag>`),
   edit stages + append EVOLUTION note with principal-order citation + linked
   task ids, bump version, set verified date + evidence.
4. Sync PROCESS-FLOWS.md same pass (Flow 19 header block with [EVO]
   marker) so registry and doc-of-record never diverge.
5. Re-run the stale-mechanism scan to prove zero residue outside
   dispatcher-owned flows.

FLW-WRITING v0.2 stages: ingest / admission gate (physics F=cost-T*info) /
station route (TRI) / research (live-news lane) / draft / adversarial
verdict / brand-voice / qa gates / publish queue (principal approval gate).
Adversarial-verdict stage born from same-day principal corrections (5WH
single-brain pass, inline outline rewrite) — no candidate reaches principal
without a kill-shot attempt first.

## 2. Broken-engine verdicts are NOT verdicts (Veritas stage-3 'choices')
`POST /api/veritas/run` returned status=failed, reason "Stage 3 verdict:
FAIL" — but stage_results['3'].skeleton showed `error: 'choices'` on ALL
variants (strong/qualified/contrarian). That is an LLM-response parse
failure inside the engine, not a substantive evaluation. BEFORE reporting
any pipeline FAIL to the principal: open the state file
(`/tmp/Veritas_process_state_<ts>Z.json`), inspect stage_results for
`error` keys. Same run also exposed stage-2 contract mismatches
(okeefe_encode/retrieve expect float lists, given text; humboldt_landscape
needs metric_type) — one run can carry several integration defects.
File engine defects to the engine lane with repro + state path; route the
substantive work through triangle meanwhile so the adversarial pass
actually happens.

## 3. Admission-gate REDO = decompose, don't argue
physics_gate.py on a whole-flow pass returned REDO (stress delta +0.70,
"traded uncertainty for load"). The compliant move is decomposing into
per-stage gated passes (each came back GO, F=-0.30). Treat a REDO as a
instruction about task SHAPE, not an obstacle to retry harder.

## 4. Stage-trail presentation (principal 2026-09-03 10:47)
"Send it back through the actual process flow... show me what it looks
like through the process flow." The deliverable is the TRAIL: each stage
named, its real status (DONE / IN FLIGHT / BLOCKED / PENDING), live
evidence per stage, and blocking stages marked honestly. Theater-free:
weak stage output (e.g. brainstorm auto-domain misdetect) is reported as
QA input feeding the defect ticket, not hidden. Record the trail INTO the
draft artifact (draft content append) so the studio holds provenance.

## 5. Studio API field notes
- POST /api/brainstorm takes `idea` (NOT seed_idea/topic; those 400 with
  the misleading "Seed idea is required"). tone dict: formality/
  assertiveness/technical_depth/custom_instructions.
- POST /api/brainstorm/novelty-scan takes `claim`; returns verdict
  CLEAR/CROWDED/TAKEN + top_overlap + prior_art[] with urls.
- VeritasRunRequest: idea, evidence_level, output_formats, author,
  pre_gathered_evidence (principles/papers/search_terms), search_terms.
- Draft PUT /api/drafts/{id}: HTML-escapes entities (&#x27; for
  apostrophes) — substring verification must account for escaping.
