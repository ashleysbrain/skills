---
name: technology-capability-registry
description: Use when cataloging or benchmarking external models/tools.
version: 1.0.0
author: the operator agent
license: MIT
metadata:
  hermes:
    tags: [registry, capability-benchmarking, model-selection, claimed-vs-measured, event-log]
    category: software-development
    related_skills: [claim-evidence-grading, ds-engine-registry-maintenance, tool-output-verification-discipline]
---

# Technology Capability Registry (external-tech catalog)

The registry of what everything OUTSIDE the fleet can do — the complement of
the internal engine registry (`ds-engine-registry-maintenance`, ecs.py).
Built 2026-08-17 for the Divinity Science internet-of-models architecture at
`~/your-workspace/technology-registry/` (registry.py, probe.py, events.py,
EVENTS-SPEC.md). This skill captures the durable architecture rules.

## When to use

- User asks "which external model/harness/tool is best for X"
- Building a model-selection layer that must not trust vendor marketing
- Seeding a catalog of external technologies (LLMs, world models, physics
  sims, harnesses like Perplexity, SaaS applications, vendor businesses)
- Designing capability propagation: one user's discovery updates all users
- Probing/benchmarking external tech on defined capability axes

## Core principles (non-negotiable)

1. **CLAIMED vs MEASURED separation.** Every entry stores `claimed` (source
   metadata, marketing, leaderboards) and `measured` (our own probe results)
   in separate fields. Selection/ranking reads ONLY `measured`. An unprobed
   entry NEVER ranks, no matter how impressive its claimed scores.
2. **Provenance discipline.** `claimed` holds only facts the source or the
   principal actually stated, with `source` + `source_verified` stamps. Anything
   from your own prior knowledge (model names, pricing, features you
   "remember") goes to `unverified_notes` quarantine — never into `claimed`.
   Prior knowledge in a provenance field is a fabrication-class defect.
3. **Prior rulings travel with entries.** Before adding an entity, search
   session history + O'Keefe for prior adversarial rulings about it (e.g.
   LittleLearner: gauntlet-run, parked, re-entry conditions). The entry
   carries the ruling (`status: parked`, `ruling_ref:` session id) so the
   decision survives context compaction.
4. **Substrate purity.** Different substrate classes (language / world /
   physics-sim) have DIFFERENT capability axes. A query's axes must resolve
   to exactly one substrate class — infer the substrate from the axes and
   REJECT cross-class queries. Never return one ranked list mixing
   incomparable substrates' scores.
5. **No hard-coded anything.** Entity kinds, categories, axes, and benchmark
   mappings are data in the registry JSON, not code branches. Adding a kind
   or axis = editing data.

## Registry schema shape

```
{
  "schema_version": "0.3.0",
  "substrate_classes": {          # per-class axes + interface contract
    "language":   {"axes": [...], "interface": "text-in/text-out"},
    "world":      {"axes": [physics_fidelity, interactive_latency,
                            action_conditioning, embodiment_transfer,
                            visual_consistency], ...},
    "physics-sim":{"axes": [...], "interface": "state-in/state-out"}
  },
  "entity_kinds": {               # model / harness / application / business
    "model":  {"categories": [...], "fields": [...]},
    "harness":{"categories": [search, coding, browser, ...], ...}
  },
  "benchmarks": {
    "internal": {"language": [...axes], "world": [...]},
    "external": {"mmlu-pro": {"maps_to": ["reasoning"]}, ...}
  },                              # external benchmarks map ONTO internal axes;
                                  # claimed leaderboard scores never dispatch
  "entries": [ {"id", "kind", "category", "substrate", "version",
                "status": "unprobed|probed|parked",
                "claimed": {...}, "measured": {...},
                "source", "source_verified", "unverified_notes": [...] } ]
}
```

## Event log (propagation without cron)

User directive: updates propagate event-driven, never via cron/polling.
Append-only JSONL (`events.jsonl`), event types: `registry.updated`,
`model.discovered`, `model.measured`, `model.evolved`, `model.deprecated`,
`harness.connected`. Subscribers pull deltas by `seq`.

**Hardening (learned by adversarial self-audit):**
- `fcntl.flock(LOCK_EX)` around appends — concurrent user-ping writers will
  race and duplicate seq numbers without it
- `os.fsync()` after every append — tail loss on crash otherwise
- Stress test before trusting: 2 processes x 50 simultaneous emits, assert
  100/100 events, seqs monotonic AND unique
- User-ping-as-sensor: a request naming an unknown model emits ONE
  `model.discovered` (claimed facts only) -> schedules ONE probe -> all
  users inherit the measurement. Model facts propagate; user data never does.

## Probe design

Probes measure per-axis scores on OUR scenarios, not provider claims:
language axes (reasoning, instruction, abstention, long_context, speed) via
chat completions; physics-sim via conservation/impulse scenarios with
numeric tolerances; world models via action-conditioned rollout rubrics.
Each scenario declares which axes it scores — keep an explicit
scenario->axis mapping and machine-check EXACT coverage of all class axes
(name-matching coverage checks give false gaps). Probes refuse honestly
(NOKEY status) when credentials are missing — never fabricate scores.

## QA discipline for registry work

1. **Mechanical digest first**: every claim checked against live state
   before any reasoning (counts, file existence, git status).
2. **Adversarial self-pass on your own artifacts**: hunt provenance leaks,
   concurrency holes, version-field gaps, cross-substrate mixing, committed
   build artifacts. Expect to find defects — the 2026-08-17 pass found 6.
3. **Fix-verification re-digest**: after fixing, RE-RUN the original failing
   check. Fixes can be incomplete (one fix still mixed incomparable scores
   in a single ranked list until the re-digest caught it).
4. **Free-energy gate on gap closures**: score each proposed addition
   (cost, info_gain, T) — SKIP positive-F items until temperature rises
   (more data arrives). Log verdicts with inputs LABELED as estimates.
5. Run records: append to the audit ledger; a method name appears only with
   its execution record attached.

## Pitfalls

- **Shell-heredoc JSON corrupts silently** — hand-typed inline JSON produced
  four garbled payloads in one session (mangled ids, typo'd keys like
  `importl`/`safabest`), two of which got COMMITTED. Generate payloads in
  Python with strict schema validation (required keys, types, dependency
  resolution) before any write. Never author JSON in shell strings.
- **`git add -A` commits `__pycache__`** — write `.gitignore`
  (`__pycache__/`, `*.pyc`) in the FIRST commit of any new repo.
- **Voice/transcription garble of entity names** — "Little Helper" was
  LittleLearner. Resolve user-named entities against session history
  (session_search) before seeding or asking; a prior ruling may exist.
- **Fake test entries left behind** — if you seed a deliberate duplicate or
  test entry, remove it in the same pass; scrub the log after selftests.
- **Version fields from day one** — `model.evolved` events are useless if
  entries lack a `version` field; add it at schema creation, `null` allowed.
- **Slow CPU transcription is normal** — local whisper `base` on this Mac
  (Homebrew Python torch, no MPS) runs ~1.5x real-time: a 10-min voice note
  takes ~15 min. Always background=true + notify_on_complete, check
  `ps aux` CPU% to confirm it's decoding, never kill at 300s.

## Reference files

- `references/technology-registry-case-study-2026-08-17.md` — full build
  record: schema evolution v0.1->v0.3, the 6 adversarial defects + fixes,
  concurrency stress numbers, gate verdicts on gap closures, live external
  landscape snapshot (MCP/A2A/Letta/LangGraph/E2B), blocked-items honesty
  list.

## Relationship to sibling skills

- `ds-engine-registry-maintenance` — INTERNAL fleet registry (ecs.py). This
  skill is its external complement; Codd principle: each registry has one
  maintainer, every fact stored exactly once.
- `claim-evidence-grading` — the claimed/measured discipline here is an
  application of it, specialized to capability dispatch.
