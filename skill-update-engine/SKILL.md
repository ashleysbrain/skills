---
name: skill-update-engine
description: Operating model for a daily/weekly/monthly update engine that scans market signals, synthesizes candidate skill updates, and feeds them through a 3-stage review cycle with anti-duplication rules, revise-and-resubmit handling, and human review touchpoints.
category: operations
version: 1.0.7
metadata:
  hermes:
    tags: [operations, update-engine, skills, cadence, automation, anti-duplication]
    related_skills: [open-core-skill-architecture, nexus-auto-remediation, sentinel-compliance-audit, sibling-agent-fleet-analytics]
    lenses: [FORGE, ARBITER, PARALLAX, SENTINEL, NEXUS]
---

## Example 3: Target-Calibration Alert (Philosophical Shortfall Persisting 3+ Days)
**Date:** 2026-07-12  
**Watchdog session:** (this session)  
**Review job run:** 2026-07-12 03:27 AM (status: ok)  
**Engine report:** Emitted §13.1 JSON block with `pipeline_status: "nominal"`, `shortfall_label: "philosophical"`  
**Pattern observed:** This is the 3+ consecutive day with the same philosophical shortfall on the 8D V1 family review.

### Watchdog Output
```
## ALERT: Divinity Health V1 Skill Product Review - Target Calibration Issue

**Date:** 2026-07-12
**Job ID:** c37a1090869d
**Last Run:** 03:27 AM (status: ok)

### Current Status vs. Target

| Metric | Target | Actual | Gap |
|--------|--------|--------|-----|
| New skills recommended | 3 | 0 | -3 |
| Updates generated | 5 | 0 | -5 |

### Gap Classification

**Philosophical shortfall (not structural)**

The engine ran successfully and produced a nominal report. The shortfall is labeled as "philosophical" because:

- The V1 core + support pair (`8d-pattern-awareness` + `8d-snapshot-report`) was reviewed and assessed as **coherent and complete**
- Pipeline status: `nominal` (no stall, no scan failure)
- The engine correctly determined that no new skills or updates are needed at this time

### Root Cause

The "3 new / 5 updates per day" target profile does not match the maintenance-phase reality of this skill family. The V1 family has been stable and complete for multiple consecutive days; the engine is correctly reporting "family complete" rather than forcing artificial candidates.

### Recommendation

**Action:** Downgrade this target dimension to maintenance mode or revise the target profile to match the current phase (e.g., 0 new / 0–2 updates/day for maintenance monitoring).

The engine is operating correctly. The persistent shortfall is a target-calibration issue, not a pipeline failure. Per skill-update-engine §R15, philosophical shortfalls on coherent families should not trigger daily alerts after the first cycle.
```

### Classification
- **Template used:** Target-calibration alert (philosophical shortfall persisting 3+ days)
- **Routing:** Alert (escalated from informational) — target-calibration issue per R15
- **Escalation trigger:** 3+ consecutive days with same `philosophical` shortfall root cause
- **Corrective action:** Revise target profile to maintenance-phase cadence (0 new / 0–2 updates/day) or expand scope to adjacent domains

---

*Generated from live watchdog runs on 2026-06-23, 2026-06-25, and 2026-07-12. Update this file when new alert patterns emerge.*

**Role panel:** FORGE (technical architecture), ARBITER (task dispatch), SCOUT (trend scoring / watchlist), PARALLAX (QA/compliance), SENTINEL (safety/compliance), NEXUS (automation/remediation), plus open-core product strategist lens.

## 1. Purpose

Keep every the operator agent/OpenClaw skill current with market changes (new models, deprecations, API shifts, competitor patterns, user behavior shifts) without requiring manual curation for each update. This is an **internal-first operating model**: test it on us before turning any part of it into a public release pattern. The engine should be **edit-first**, not new-skill-first: review the current skill set before inventing a new one, and prefer strengthening existing skills when that achieves the goal more cleanly. The engine produces at least **3 candidate updates per 24-hour cycle** and routes them through a 3-stage pipeline: Scan → Synthesize → Ship, with an explicit **revise-and-resubmit** loop for near-miss candidates that can be made safe or more complete.

## 2. Roles & Responsibilities

**ARBITER — Dispatcher (runs daily 04:00 UTC)**
- Reads the update backlog and assigns scan tasks to FORGE and NEXUS.
- Prioritizes by: (a) skills with `use_count > 10` in `.usage.json`, (b) skills not patched in 7+ days, (c) skills flagged by SENTINEL as stale.
- Enforces the "3 candidates minimum" rule — if fewer than 3 candidates emerge, expands the scan radius (more sources, looser relevance threshold).
- Writes dispatch manifest to `~/.sibling-agent/workspace/intel/skill-engine/dispatch-YYYY-MM-DD.json`.

**FORGE — Architect (runs daily 04:30 UTC)**
- Scans defined signal sources (see §4) for changes affecting skill domains.
- Classifies changes into buckets: `model_deprecation`, `api_change`, `new_capability`, `competitor_move`, `user_pattern_shift`, `dependency_update`.
- Produces raw candidate cards: `{skill_id, change_type, source_url, summary, confidence, impact}`.
- Writes candidates to `~/.sibling-agent/workspace/intel/skill-engine/candidates-YYYY-MM-DD.json`.

**SCOUT — Trend Scorer (runs daily 04:45 UTC)**
- Reads the raw candidate stream plus the persistent watchlist.
- Computes `benefit_score`, `risk_score`, and `priority_score` for every candidate.
- Updates `~/.sibling-agent/workspace/intel/skill-engine/watchlist.json` so promising skills stay visible across days.
- Emits the top 3 eligible items for the ship window, sorted by `priority_score`.

**NEXUS — Automator (runs daily 05:00 UTC)**
- Auto-generates patch content for high-confidence candidates (confidence ≥ 0.85, impact ≤ "low").
- For medium/low-confidence candidates, creates a draft patch but flags for PARALLAX review.
- Runs anti-duplication check (see §6) before writing any patch.
- Applies patches to `skills-library/` and logs to `patch-log-YYYY-MM-DD.jsonl`.
- Triggers `fleet_analytics.py sync` after batch patch.

**PARALLAX — QA (runs daily 06:00 UTC)**
- Reviews all medium/low-confidence candidates from the past 24h.
- Validates patches against: (a) skill's existing SKILL.md structure, (b) open-core boundary rules (no moat leakage), (c) banned-word compliance.
- Returns verdict: `approve`, `reject`, `revise` (with notes).
- Writes QA report to `~/.sibling-agent/workspace/intel/skill-engine/qa-YYYY-MM-DD.json`.

**SENTINEL — Compliance (runs daily 07:00 UTC, piggybacks on existing audit)**
- Extends the daily compliance audit with a skill-integrity check.
- Verifies no patched skill broke its `version` field, `references/` linkage, or template integrity.
- Checks that no candidate introduced PHI, proprietary logic, or safety violations.
- Separates **hard-block** failures from **salvageable** failures.
- Flags skills where `patch_count` spiked > 5 in 24h (potential thrashing).

**Product Strategist Lens — Weekly Review (Mondays 09:00 UTC, human-optional)**
- Aggregates the past week's candidate pipeline metrics: candidates generated, approved, rejected, auto-shipped, manual-intervention-required.
- Identifies skills that are chronically untouched or chronically rewritten.
- Adjusts scan priorities for the next week.
- Produces a one-paragraph "skill portfolio health" summary for the operator.

## 3. Three-Stage Pipeline

### Stage 1: Scan (04:00–05:00 UTC)

Triggered by ARBITER. FORGE and NEXUS run in parallel.

- **Signal sources** (see §4 for concrete list).
- Output: `candidates-YYYY-MM-DD.json` — flat array of candidate cards.
- Minimum 3 candidates. If scan produces fewer, ARBITER injects a "market sweep" candidate that broadens source coverage for the next cycle.

### Stage 2: Synthesize (05:00–06:00 UTC)

SCOUT computes the running watchlist scores, then NEXUS processes the top candidates:

1. **Update watchlist** using the scoring reference in `references/release-priority-scoring.md`.
2. **De-duplicate** against the `applied-updates` registry (see §6).
3. **Classify** confidence/impact:
   - `high confidence + low impact` → auto-ship (NEXUS applies patch, no human review).
   - `medium confidence or medium impact` → draft patch, queue for PARALLAX.
   - `low confidence or high impact` → draft summary only, queue for PARALLAX + human escalation.
4. **Generate patches** using the existing skill authoring pattern: modify SKILL.md, add to `references/`, update version.
5. **Log** every action in `patch-log-YYYY-MM-DD.jsonl`.

### Versioning & Release Identity

Every skill update that ships through this engine must carry explicit release metadata. Do not ship vague labels like "updated" or "new version".

## Edit-first release policy

Before adding a new skill, the engine must ask:
- can this be solved by editing an existing skill?
- can this be a reference update instead of a new skill?
- can this be a support/bridge/ops update to a current family member?
- is this really a class-level umbrella, with session-specific detail better parked in `references/`?
- is the new artifact actually necessary, or is it just duplicate surface area?
- would strengthening one umbrella skill reduce long-term sprawl more cleanly than adding a sibling skill?

Daily target:
- **Default maintenance target:** 1 new skill max per day and 5 updates to current skills per day.
- **Job-specific target profiles override the default** when the cron prompt or operator sets explicit metrics (for example, 3 recommended new skills and 5 updates per day).
- Report against the **active target profile**, not the default, and call out any gap in counts plainly.
- **The engine is a PRODUCER, never an observer.** It must never emit `[SILENT]`. `[SILENT]` is the watchdog/observer-layer suppression marker (see §13.2); when the engine itself emits it, message delivery is suppressed and the cycle's report never reaches a human. Even when the active target is fully met and nothing material changed, the engine must emit a brief nominal report containing the §13.1 JSON block (with `pipeline_status: "nominal"` and the met counts). Only the *watchdog* that monitors the engine may emit `[SILENT]`.
- If a job mixes scopes (for example, health review vs. skill-product review), follow the prompt's declared scope and keep the report aligned to that lane.
- if a day has less signal, prefer updates and refinements over new skill creation.
- if a new skill is created, it should be justified as a true gap rather than convenience.
- if a new skill is created, it should be justified as a true gap rather than convenience

This is intentionally concise and skill-dense: strengthen what already exists before expanding the library.

Use this identity format for the shipped skill or release artifact:

`[Family] — [Release Class] — v[SemVer] — [Release Date]`

Recommended class mapping for this engine:
- `core` — user-facing skill with primary workflow value
- `support` — reference, guide, QA, or helper layer
- `bridge` — compatibility, translation, or migration layer
- `fork` — derivative variant of an existing family member
- `ops` — internal workflow or fleet utility

SemVer bump rule:
- `patch` → wording fixes, references, examples, non-breaking clarifications
- `minor` → additive workflow steps, new guidance, new helper/reference behavior
- `major` → breaking workflow change, renamed contract, or redesigned output shape

Operational rule:
- the version field in the skill frontmatter must move forward before the patch can ship
- a candidate without a valid version bump is not shippable
- the current stable core anchor is the comparison point, not the first-ever release
- internal test-only releases still get versioned; they are not exempt from release identity

### Stage 3: Ship (06:00–07:00 UTC)

PARALLAX reviews queued candidates. SENTINEL runs compliance check.

- **Harness-regression guard (mandatory, T-261005-0132):** between PARALLAX approval and NEXUS apply, every candidate that edits a skill/boot/adapter file in a registered component family runs `python3 /<workspace> --check-edit <candidate> --component <name>` (RRSI-lawful: ID/OOD deltas on the pinned hold-out battery, annealed edit budget, OOD ratchet). Exit 0 SHIP -> apply; exit 1 -> route the candidate to `revise` with the guard's reason (overfit signature, over-budget, free-energy skip, ratchet floor); exit 2 -> halt the lane for that component (battery drift/tamper, run `--run`). After applying a SHIPPED edit: `--post-ship-repin --component <name> --edit-id <id>`. Strictly neutral edits (dID=0, dOOD=0) require explicit `--allow-neutral`.
- Approved patches: NEXUS commits to `skills-library/` and updates `.usage.json` patch metadata.
- Rejected patches: logged with reason, candidate archived.
- **Salvageable near-misses:** if a candidate fails for a fixable reason, PARALLAX returns a revise note instead of a dead rejection. NEXUS/FORGE can patch the candidate and re-submit it through SCOUT and SENTINEL on the next cycle.
- Revise patches: notes sent back to FORGE for next cycle refinement.
- Final state: `shipped-YYYY-MM-DD.json` with all applied updates.

### Human Escalation Path

Only these conditions require human intervention:
- `high impact` candidate (affects safety, PHI boundary, or core business logic).
- `confidence < 0.5` on a skill with `use_count > 20` (high-stakes ambiguity).
- SENTINEL flags a compliance violation on a shipped patch.
- Pipeline stalls for 2+ consecutive days (no candidates generated).

## 4. Human Touchpoints

Human intervention is built in so the system stays aligned to operator intent:

- **Daily:** a human reviewer inspects the top 3 eligible candidates before final release selection.
- **Weekly:** a human receives the portfolio health report and pipeline metrics summary; the packet is intended for a teammate/operator, not just the model.
- **Monthly:** a human performs a mandatory reset/audit pass on the portfolio, safety boundaries, and release ladder.
- **Near-miss candidates:** if a candidate is close to passing, it stays alive in the watchlist and can be revised rather than discarded.
- Treat `revise` as an active state, not a dead end; preserve the evidence, edit plan, and next review date.
- When turning this process into a user-facing document, rewrite it as an operational SOP or command-to-AI flow, not a conversation recap; preserve the substantive content while reorganizing it for execution.

## 5. Signal Sources (Concrete)

**Daily scan targets:**
- `~/.sibling-agent/cron/jobs.json` — model field changes, new jobs, disabled jobs.
- `<agent-home>/models_dev_cache.json` — new models available, deprecated models.
- `skills-library/.usage.json` — usage pattern shifts (spikes, drops, new skills).
- OpenRouter model catalog API (free model availability changes).
- Gateway error logs (`<agent-home>/logs/errors.log`) — recurring error patterns indicating skill drift.
- **Skill manifest integrity** — for each patched skill, enumerate all subdirectories (`references/`, `templates/`, `scripts/`, `attachments/`) and compare against the SKILL.md manifest. Unlisted files on disk or dead manifest entries are surfaced as candidates. This catches the drift pattern where files accumulate across sessions without the runtime manifest being updated. Pay special attention to `attachments/` directories — they are non-standard and often invisible to narrow `references/`-only grep patterns.
- **Dead inline references** — scan each skill's SKILL.md body for all support-directory paths (`references/`, `scripts/`, `templates/`, `attachments/`) that do not exist on disk. Cross-skill references (e.g., skill A pointing to skill B's `references/` file) are a common drift source in skill families. Flag these as `bug` candidates with confidence ≥ 0.90.
- **Redundant section detection** — check whether a SKILL.md has multiple sections that list the same support files (e.g., a "Manifest" section AND a "References" section with identical file lists). This inflates SKILL.md length without adding information and confuses the agent about which section is canonical. Flag as `bug` with confidence ≥ 0.90. Fix: collapse the duplicate into a pointer to the canonical listing section. See `references/manifest-reconciliation-commands.md` for the detection technique (including the three-way inconsistency pattern: manifest + body citation + missing file) and observed instances. See `scripts/verify-patch-manifest.sh` for the reusable post-patch verification script.

**Weekly scan targets:**
- Git log on `<agent-home>/hermes-agent/` — core framework changes that affect skill APIs.
- Release notes from model providers (Anthropic, Google, OpenAI, NVIDIA).
- Competitor agent platform changelogs (if tracked).

**Monthly scan targets:**
- Full skill portfolio audit — every skill gets a freshness score.
- User feedback aggregation (if feedback channel exists).
- Dependency version drift check (Python packages, API versions).

## 6. Release Cadence

**Daily:**
- Low-impact factual patches: model name updates, reference link fixes, error pattern additions, manifest drift corrections.
- "Family complete" is valid pipeline output. If the engine reviews a coherent family and finds no gap, reporting zero new skills is correct — it is not a pipeline stall.
- When reporting zero new skills, explicitly label the reason: **"structural"** (scan failed, sources unavailable, model error) vs. **"philosophical"** (family reviewed and found coherent, no genuine gap exists). Watchdogs and downstream consumers use this label to route alerts correctly.
- Current-skill edits are preferred over new-skill creation when they preserve the goal with less surface area.
- Human reviewer selects the final release from the top 3 eligible candidates before ship.
- Target: 5 updates to current skills, 1 new skill max when truly justified.
- Stagger cron minute offsets so collection, sync, review, and summary jobs do not collide in the same minute when they share a cadence family.

**Weekly (human-required, Mondays):**
- Medium-impact patches: new workflow steps, updated reference files, skill description refinement.
- Product strategist review of pipeline metrics and watchlist drift.
- Human receives a report package with the week’s approvals, rejects, revisions, and near-misses.
- Target: 5+ candidates reviewed, 2+ shipped.

### Monthly
- High-impact patches: safety boundary changes, new skill creation, skill deprecation/retirement.
- Full portfolio freshness audit.
- Anchor version bump for any `core` release class skill.
- Human audit of the release ladder, safety behavior, and watchlist retention rules.
- Review whether repeated new-skill requests should instead be converted into current-skill edits or reference updates.
- Target: portfolio health score ≥ 80%, zero stale (>30 day) high-use skills.

## 7. Anti-Duplication Rules

1. **Applied-updates registry:** Every shipped patch is recorded in `~/.sibling-agent/workspace/intel/skill-engine/applied-updates.jsonl` with fields: `{date, skill_id, change_type, source_hash, patch_summary}`.
2. **Source hash:** Each candidate carries a `source_hash = SHA256(change_type + skill_id + normalized_summary)`. Before generating a patch, NEXUS checks this hash against the registry. Exact match = skip.
3. **Semantic dedup:** If `source_hash` differs but `skill_id + change_type` matches an entry from the past 7 days, the candidate is merged into the existing entry rather than creating a duplicate patch.
4. **Skill-scope dedup:** A skill may only receive one patch per `change_type` per day. Multiple candidates for the same skill+type are merged into a single compound patch.
5. **Version gate:** A patch that would change a skill's version must increment from the current version in SKILL.md. NEXUS validates this before applying.

## 8. Pipeline Metrics (Tracked Weekly)

- `candidates_generated` — total raw candidates from scan.
- `candidates_unique` — after dedup.
- `manifest_drift_corrections` — files added to or removed from skill manifests during reconciliation.
- `reference_consolidation_candidates` — skills flagged for having >15 reference files.
- `patches_auto_shipped` — high-confidence, no review needed.
- `patches_reviewed` — went through PARALLAX.
- `patches_rejected` — QA rejected.
- `patches_shipped` — total applied to skills
- `current_skill_edits` — shipped updates that modified existing skills instead of creating new ones
- `new_skills_created` — brand-new skills created after edit-first review
- `human_escalations` — count of human-required interventions
- `pipeline_stall_days` — consecutive days with zero candidates
- `portfolio_freshness_score` — % of skills patched in last 30 days
- `revise_queue_depth` — count of near-miss candidates awaiting fixes and rescore
- `version_bump_compliance` — % of shipped candidates with valid forward-moving SemVer updates

## 9. Concrete File Layout

```
~/.sibling-agent/workspace/intel/skill-engine/
├── dispatch-YYYY-MM-DD.json          # ARBITER daily dispatch manifest
├── candidates-YYYY-MM-DD.json        # FORGE raw candidates
- `patch-log-YYYY-MM-DD.jsonl`        # NEXUS patch log (append-only)
├── qa-YYYY-MM-DD.json                # PARALLAX QA verdicts
├── shipped-YYYY-MM-DD.json           # Final state of shipped updates
├── applied-updates.jsonl             # Master dedup registry (append-only)
├── weekly-metrics-YYYY-WNN.json      # Weekly pipeline metrics
├── monthly-audit-YYYY-MM.json        # Monthly portfolio audit results
└── config.yaml                       # Engine configuration (thresholds, sources)

## 9.1 Report Output Rule

When the engine produces a human-readable report for a human reviewer, generate it as **PDF when available**. If PDF generation is unavailable in the current environment, fall back to a readable Markdown version rather than dropping the report entirely.

## 9.2 Document Transformation Rule

When converting between PDF and Markdown, preserve *all substantive content*. Clean symbols, encoding artifacts, and weird punctuation if needed, but do not silently delete sections, examples, checklists, references, or release metadata. If a conversion requires cleanup, do it losslessly and verify that the restored Markdown still contains the full process.
```

## 10. Configuration (config.yaml)

```yaml
scan:
  daily_sources:
    - cron_jobs_json
    - models_dev_cache
    - skill_usage
    - openrouter_catalog
    - error_logs
  - skill_manifest_integrity
  weekly_sources:
    - hermes_agent_git_log
    - provider_release_notes
  monthly_sources:
    - full_portfolio_audit
    - dependency_drift
  min_candidates_per_day: 3

pipeline:
  auto_ship_confidence_threshold: 0.85
  auto_ship_max_impact: low
  human_escalation_impact: high
  human_escalation_confidence_below: 0.5
  stall_alert_days: 2
  revise_retry_limit: 2

dedup:
  source_hash_algorithm: sha256
  semantic_merge_window_days: 7
  max_patches_per_skill_per_day: 1

roles:
  arbiter_cron: "0 4 * * *"
  forge_cron: "30 4 * * *"
  nexus_cron: "0 5 * * *"
  parallax_cron: "0 6 * * *"
  sentinel_cron: "0 7 * * *"  # piggybacks existing audit
  weekly_review_cron: "0 9 * * 1"
```

## 11. Risks

**R1 — Free model volatility breaks the pipeline.** The entire engine runs on cron jobs using free-tier models. If all free models break simultaneously (proven pattern — see NEXUS Lesson 11), the pipeline stalls entirely. *Mitigation:* Pin the engine's own cron jobs to a paid fallback model (gemini-2.5-flash via API key). The engine is business-critical; it should not ride on volatile free tiers.

**R2 — Hallucinated patches ship without review.** Low-confidence auto-ship is gated at 0.85, but LLM-generated patches can still introduce subtle errors (wrong API endpoints, fabricated version numbers, invented references). *Mitigation:* PARALLAX validates every patch against the actual skill file structure, not just the candidate metadata. SENTINEL checks for version consistency and reference integrity.

**R3 — Dedup registry grows unbounded.** `applied-updates.jsonl` is append-only. Over months, this becomes a large file that slows hash lookups. *Mitigation:* Monthly compaction job that archives entries older than 90 days into a compressed archive and keeps only the last 30 days hot.

**R4 — Skill thrashing.** If a skill receives conflicting patches across days (e.g., model A recommended, then model B, then model A again), the skill oscillates. *Mitigation:* The "semantic merge window" rule (7 days) catches same-type changes. Additionally, SENTINEL flags skills with `patch_count` delta > 5 in 24h.

**R5 — Open-core boundary leakage.** An auto-generated patch could inadvertently expose proprietary scoring logic, calibration weights, or private thresholds that belong in the premium layer. *Mitigation:* PARALLAX runs an explicit boundary check against the skill's open-core boundary map (if one exists in `references/`). Skills without a boundary map are not eligible for auto-ship.

**R6 — Candidate starvation under low-signal conditions.** If the market is quiet (no model changes, no API shifts), the pipeline may fail the "3 candidates minimum" rule. *Mitigation:* ARBITER injects a "market sweep" candidate that broadens source coverage. Also accept "no-op" candidates (verified skill is still current) as valid pipeline output.

**R7 — Gateway-down blocks all pipeline stages.** Every stage depends on `sibling-agent cron` infrastructure. If the gateway is down (proven pattern — multiple NEXUS lessons), the entire pipeline stalls. *Mitigation:* NEXUS already has gateway-down fallback procedures (assessment-only mode, direct SQLite queries). The skill engine should mirror this pattern — fall back to file-based operations when the gateway is unavailable.

**R8 — Cross-profile skill contamination.** The engine patches skills in `skills-library/`, but if multiple profiles share the same skill directory, a patch intended for one profile affects all. *Mitigation:* The engine should only patch skills under the profile it's configured for. Use `get_hermes_home()` to resolve the correct profile path.

**R9 — Circular dependency with nexus-auto-remediation.** NEXUS runs both the auto-remediation cycle and the skill update engine. If the engine patches the NEXUS skill itself, it could break the remediation cycle that keeps the engine running. *Mitigation:* The `nexus-auto-remediation` skill is on a protected list — patches to it require human review regardless of confidence.

**R10 — Metric drift obscures real problems.** If the pipeline reports "3 candidates generated, 1 shipped" every day but the candidates are trivial (typo fixes, link updates), the metrics look healthy while the portfolio stagnates. *Mitigation:* Weekly product strategist review includes a "candidate quality" assessment — not just volume. Flag weeks where all shipped patches are `impact: trivial`.

**R11 — Non-standard `attachments/` directory causes invisible drift.** Some skills accumulate files in `attachments/` instead of the standard `references/`, `templates/`, or `scripts/` directories. Standard manifest reconciliation grep patterns only look for `references/` paths, so files in `attachments/` are invisible to the check and silently drift. *Mitigation:* The manifest reconciliation scan must enumerate all subdirectories (`references/`, `templates/`, `scripts/`, `attachments/`) and compare against the SKILL.md manifest. Flag skills using `attachments/` as structural candidates for directory normalization.

**R12 — Premium namespace leakage in public frontmatter.** Public-facing skills may list premium-layer skill names in their `related_skills` frontmatter (e.g., `8d360-unified-scoring-pipeline`, `adhd-ef-compass-v3`). If the skill is ever published or shared, those names expose the private namespace. *Mitigation:* SENTINEL's skill-integrity check should flag any `related_skills` entry that references a skill not present in the public skill directory. If the referenced skill is premium-only, the frontmatter entry should use a generic label instead or be removed before public release.

**R13 — Reference accumulation threshold.** When a skill accumulates more than 15 reference files, maintenance cost rises and the skill becomes harder for the runtime agent to navigate. Session-specific editing notes, one-off rendering corrections, and tailored examples are common culprits. *Mitigation:* SCOUT should flag skills with `references/` count > 15 as consolidation candidates. The fix is to merge related session-specific files into a single authoritative reference (e.g., five report-editing notes → one `report-editing-guide.md`), not to delete content.

**R14 — Dead references in non-standard support directories.** The dead-inline-references scan historically focused on `references/` paths only. Dead links to `scripts/`, `templates/`, or `attachments/` paths (e.g., a `scripts/render_user_facing_report.py` reference where no `scripts/` directory exists) are equally valid pipeline candidates but invisible to a narrow `references/`-only grep. *Mitigation:* The scan must enumerate all four standard support directories (`references/`, `scripts/`, `templates/`, `attachments/`) when checking inline paths against disk. Flag any path mentioned in SKILL.md that resolves to a non-existent file.

**R15 — Watchdog target-profile mismatch with edit-first policy.** When a watchdog or monitor job tracks the engine against a target profile (e.g., \"3 new skills / 5 updates per day\"), but the engine's edit-first philosophy correctly determines that a coherent family needs no new skills, the result is persistent alert fatigue. The watchdog reports \"shortfall\" every cycle; the engine reports \"family complete.\" Both are correct in isolation but contradictory in combination. This has been observed to persist for 5+ consecutive days on the 8D V1 family review. *Mitigation:* (a) The watchdog target profile must distinguish \"structural shortfall\" (engine failing to scan or produce candidates) from \"philosophical shortfall\" (engine correctly finding no gap). (b) When a family has been reviewed as coherent and complete, the watchdog should downgrade that target dimension to \"maintenance mode\" rather than alerting daily. (c) The engine's report should explicitly state whether the shortfall is structural or philosophical so the watchdog can route accordingly. (d) If the same shortfall persists for 3+ consecutive days with the same root cause, it should be escalated as a target-calibration issue, not a pipeline issue. (e) Operators may consider expanding the scan scope to adjacent skill domains or revising the target profile to match the maintenance-phase cadence (e.g., 0 new / 2–3 updates/day) when the engine consistently reports philosophical shortfall. (f) **Watchdog output retrieval optimization:** For cron job output inspection, prefer direct filesystem access (`<agent-home>/cron/output/<job_id>/`) over `session_search` when possible. The cron output directory contains timestamped markdown files with the actual report content, making metrics extraction faster and avoiding the 1MB `session_search` truncation pitfall described in §13.1. Use `session_search` only as a fallback when the output file path is unknown or corrupted. **Observed pattern:** 2026-07-11 watchdog run successfully retrieved exact JSON block and counts from `2026-07-11_03-27-56.md` using direct filesystem reads, confirming this is more reliable than `session_search` for daily monitoring.

**R16 — Single-job execution stall on reference-heavy skills.** When the engine runs in single-job mode (one cron job executing all pipeline stages), the agent can stall while reading reference files from skills with large support directories (e.g., `8d-snapshot-report` has 10 support files across references/, templates/, scripts/). The session terminates before emitting the required JSON monitoring block, causing the watchdog to report a structural shortfall (0 candidates, 0 updates) even though the cron job shows "ok" status. *Mitigation:* (a) Implement the timeboxing and early-JSON-emission rules in Section 11.1. (b) Add a reference-file budget to the scan phase (max 3 files per skill unless it's the primary review target) and when scanning skill manifests, count references/ + templates/ + scripts/ + attachments/ files. If a skill has > 10 support files, read only the SKILL.md and manifest; skip deep reference inspection unless the skill is the primary review target. (c) Prefer the native multi-stage pipeline (separate cron jobs per role) for production review jobs. (d) If single-job mode is unavoidable, wrap the invocation in a timeout wrapper that forces JSON emission on session exit.

**R17 — Producer/observer confusion: engine emits `[SILENT]` after a read-only run.** Distinct from R16 (a stall where the report never assembles), this failure mode is the engine *completing cleanly* with cron status `ok`, making **only read-only calls** (`read_file`, `search_files`, `hermes skills check`, usage-stats reads) and **zero write calls** (`skill_manage` / `write_file` / `patch`), then emitting `[SILENT]` as its final output. `[SILENT]` is the watchdog suppression marker (§13.2); when the producer emits it, message delivery is suppressed and the cycle's report never reaches a human — so the shortfall becomes invisible until a watchdog reconstructs it. Root causes seen in the wild: (a) a weak free-tier model (e.g. `nemotron-3-super-120b:free`) defaults to `[SILENT]` as an escape hatch rather than doing synthesis work; (b) the skill historically instructed the engine to "return `[SILENT]`" on a met target, which the model over-generalizes to "return `[SILENT]` when you'd rather not produce." *Mitigation:* (i) The engine must NEVER emit `[SILENT]` — see the corrected rule in §6. (ii) **Structural invariant:** a producer run that makes zero write calls is a no-op run regardless of its final text; it must emit a report with the §13.1 JSON block and `shortfall_label: "structural"` explaining the zero-write outcome, never `[SILENT]`. (iii) The monitoring watchdog should audit the session's tool-call histogram: read-only-only + zero writes + final message `[SILENT]` ⇒ classify as a structural contract violation, not a met-target day. (iv) Pin the engine's own cron jobs off volatile free-tier models when they recurrently collapse to read-only + `[SILENT]` (echoes R1). Observed 2026-06-19 on the Divinity Health V1 review job `c37a1090869d`: 0 write calls, 5×`read_file` + 1×`search_files` + 8×`terminal` (all read-only), final message `[SILENT]` → reported 0/3 new, 0/5 updates.

## 11. Handoff Map

```
04:00 ARBITER ──dispatch manifest──▶ FORGE
04:30 FORGE   ──candidate cards───▶ NEXUS
05:00 NEXUS   ──draft patches─────▶ PARALLAX
06:00 PARALLAX──verdicts──────────▶ NEXUS (apply approved) + SENTINEL
07:00 SENTINEL──compliance check──▶ shipped-YYYY-MM-DD.json
09:00 Mon     ──weekly metrics───▶ Product Strategist (human-optional)
1st monthly ──portfolio audit───▶ Product Strategist (human-required)
```

Every handoff is a file write + log entry. No handoff depends on a live human response — the pipeline advances on its own, with human escalation as an async overlay.

## 11.1 Single-Job Execution Mode (Watchdog/Review Jobs)

**Problem:** The engine is designed as a multi-stage pipeline with separate cron jobs for each role (ARBITER → FORGE → SCOUT → NEXUS → PARALLAX → SENTINEL). However, some deployments (e.g., the Divinity Health V1 Skill Product Review job `c37a1090869d`) run the entire pipeline in a **single cron job** that loads this skill and executes all stages sequentially in one agent session.

**Risk:** In single-job mode, the agent can stall mid-execution when:
- Inspecting skills with many reference files (e.g., `8d-snapshot-report` has 8 references + 1 template + 1 script)
- Reading multiple skill manifests during the scan phase
- The session hits token/time limits before emitting the required JSON output block

**Observed failure:** The review job ran at 03:25–03:30 AM CDT (status "ok" in cron) but the session `cron_c37a1090869d_20260612_032533` ended mid-execution while the agent was still reading `8d-snapshot-report` references (a reference-heavy skill with 10 support files). No final summary or JSON block was produced → 0/3 new skills, 0/5 updates. **Repeat occurrence on 2026-06-13:** job completed with status "ok" but emitted zero JSON block — watchdog could not auto-classify shortfall. This illustrates the need for the reference inspection budget and early JSON emission in single-job mode.

**Hard Requirement for Single-Job Mode:** Every single-job execution **must** emit the Section 13.1 JSON block as the **very first substantive output** of the session, before any scanning, reading, or analysis begins.\n\n> **Implementation tip:** To emit the JSON block first, the agent should output a minimal valid JSON block immediately after loading the skill and determining the target profile, then update it incrementally as the pipeline progresses. See `references/single-job-mode-enforcement.md` for a concrete implementation template. This is not a mitigation — it is a contract requirement. The JSON block must contain at minimum:
```json
{
  "new_skills_recommended": 0,
  "updates_generated": 0,
  "target_profile": "<active-profile-name>",
  "pipeline_status": "nominal",
  "candidates_unique": 0,
  "patches_shipped": 0
}
```
If the session stalls later, the watchdog can still classify the run. Update the fields as the pipeline progresses, but the initial emission is mandatory.

**Enforced Mitigations for Single-Job Mode:**

1. **Timebox each phase** — set explicit step limits before starting:
   - Scan phase: max 5 skill inspections, max 3 reference files per skill
   - Synthesize phase: max 10 candidate cards, dedup immediately
   - Ship phase: emit JSON block **first**, then apply patches
   - If timebox expires, emit partial JSON with `pipeline_status: "stalled"` and `shortfall_label: "structural"`

2. **Emit JSON block FIRST** — write the monitoring JSON (Section 13.1) to the session as the **first substantive output**, not the last. This ensures watchdogs can classify the run even if the session stalls later. Implementation pattern: emit a minimal valid JSON block immediately after loading the skill and determining the target profile, then update it incrementally.

3. **Reference inspection budget** — when scanning skill manifests, count `references/` + `templates/` + `scripts/` + `attachments/` files. If a skill has > 10 support files, read only the SKILL.md and manifest; skip deep reference inspection unless the skill is the primary review target.

4. **Stall detection** — if the agent detects it has spent > 60% of the session budget on reference reading without producing candidates, abort the scan, emit the JSON block with current counts (even if zero), and set `pipeline_status: "stalled"`.

5. **Recovery protocol** — when a watchdog detects a stalled run (JSON block present but `pipeline_status: "stalled"` or missing entirely), the corrective action is: re-run the review job with an explicit "resume from scan" prompt that skips already-inspected skills.

6. **Watchdog-side contract enforcement** — the watchdog cron job **must** use the exact alert templates from Section 13.2. If the engine report lacks the JSON block, the watchdog must output the "JSON block missing" template verbatim, not a custom summary.

**Deployment recommendation:** For production review jobs, prefer the native multi-stage pipeline (separate cron jobs per role) over single-job mode. If single-job mode is required, wrap the invocation in a timeout wrapper that forces JSON emission on exit. See `references/single-job-mode-enforcement.md` for a concrete implementation template.


## 12. Verification Checklist

- [ ] `min_candidates_per_day` met for the past 7 days
- [ ] Zero `pipeline_stall_days` in the past 30 days
- [ ] `applied-updates.jsonl` dedup hash check passes on last 7 entries
- [ ] No skill received > 1 patch per `change_type` today
- [ ] All patched skills have manifest lists that match their full directory contents (references/, templates/, scripts/, attachments/)
- [ ] All auto-shipped patches have `confidence ≥ 0.85` and `impact ≤ low`
- [ ] SENTINEL compliance audit includes skill-integrity check
- [ ] Protected skills (nexus-auto-remediation, sentinel-compliance-audit) require human review
- [ ] `portfolio_freshness_score ≥ 80%` (skills patched within 30 days)
- [ ] Every shipped skill has explicit release identity: family, class, SemVer, and date
- [ ] Every shipped skill frontmatter version moved forward before ship
- [ ] Single-job execution runs complete within session timeout (emit JSON block before stall)
- [ ] No producer run emits `[SILENT]` — the engine is a producer, never an observer (R17); a zero-write-call run must still emit a §13.1 JSON block, never `[SILENT]`

## 13. Monitoring and Reporting

When monitoring the output of a skill update engine run (e.g., via a watchdog cron job), use the following steps to verify that the engine ran and met its target:

1. **Check the cron job status**: Use `hermes cron list` to find the job by name or ID and confirm its last run time and status.
2. **Retrieve the latest run output**: Use `session_search` with a query for the job name or ID to find the most recent session where the engine ran.
3. **Extract the metrics**: From the session output, look for the reported counts of new skill recommendations and total updates.
4. **Compare against targets**: Compare the extracted counts against the daily targets (e.g., 3 new skills, 5 updates). Report any gap.
5. **Label the gap**: If the engine did not run, report that as a structural issue. If it ran but missed targets, label the gap appropriately (e.g., "New skill recommendations: 0/3", "Updates: 2/5").

This monitoring pattern ensures that the skill update engine's output is visible and actionable for oversight.

### 13.1 Handling Large session_search Results (Watchdog Pitfall)

**Problem:** When monitoring cron jobs with many historical sessions (e.g., daily runs over weeks/months), `session_search` with a pattern like `cron_<job_id>` can return results exceeding the 1MB size limit. The tool output is truncated to a temp file path, making it impossible to extract the latest session ID directly.

**Observed failure pattern:** Watchdog calls `session_search(query="cron_c37a1090869d", sort="newest")`, receives a 1.4MB persisted output saved to `/var/folders/.../tool-*.txt`. Without the session ID, the watchdog cannot retrieve the actual session content to verify the engine's output. **Watchdog contract violation (2026-07-17):** Reporting counts as "unknown (truncated output)" without attempting the documented two-phase extraction is a protocol violation. The watchdog MUST attempt extraction before falling back to manual inspection.

**Mitigation pattern (terminal + grep approach):**

1. **Save the session_search output to a temp file** (this happens automatically when the result is large).
2. **Use grep to extract session IDs from the JSON**:
   ```bash
   grep -o '"session_id": "cron_<job_id>_[^"]*"' /var/folders/.../tool-*.txt | head -10
   ```
   This extracts all matching session IDs from the persisted JSON array.
3. **Select the most recent session** (first result from head, since session IDs are timestamped in `YYYYMMDD_HHMMSS` format).
4. **Call session_search with the specific session_id**:
   ```python
   session_search(session_id="cron_c37a1090869d_20260708_032506")
   ```
   This returns the full session content (since a single session is small enough to fit).

**Why this works:** Session IDs include timestamps (`cron_<job_id>_YYYYMMDD_HHMMSS`), so sorting by newest in the initial query and taking `head -1` from the extracted IDs gives the most recent run. The second call with `session_id` (not `query`) retrieves the complete session without truncation.

**Alternative pattern (when temp file path is not easily accessible):** Use `read_file` on the persisted output path that `session_search` returns, then parse with a simple Python or jq extraction to get the session_id field from the first result.

**Note:** This pitfall only applies when the watchdog needs to inspect the actual session content for metrics extraction. If the watchdog only needs to verify existence (e.g., "did any session run today?"), the truncated result may be sufficient. **Contract reminder:** When the watchdog cannot complete extraction, report the explicit failure reason and temp file path — do not use "unknown (truncated output)" as a fallback label.

## 13.1 Engine Report Output Format (Required for Watchdog Consumption)

Every engine run that produces a human-readable or machine-parsable report **must** include the following fields so downstream watchdogs can correctly classify shortfalls:

| Field | Required | Description |
|-------|----------|-------------|
| `new_skills_recommended` | Yes | Integer count of new skill candidates synthesized this cycle. |
| `updates_generated` | Yes | Integer count of updates to existing skills (patches, reference additions, manifest fixes, etc.). |
| `target_profile` | Yes | Name of the active target profile (e.g., "v1-health-review", "default-maintenance"). |
| `shortfall_label` | **Yes (when targets not fully met)** | One of: `structural` (scan failed, sources unavailable, model error, pipeline stall) OR `philosophical` (family reviewed and found coherent, no genuine gap exists). **This field is mandatory when either count is below target.** |
| `shortfall_reason` | When labeled `philosophical` | One-sentence explanation of why the family is complete (e.g., "V1 core + support pair assessed as complete; maintenance-only cycle"). |
| `pipeline_status` | Yes | One of: `nominal`, `degraded`, `stalled`. |
| `candidates_unique` | Yes | Integer count after dedup. |
| `patches_shipped` | Yes | Integer count of patches applied this cycle.

**Example minimal JSON block (embedded in report or emitted as sidecar):**
```json
{
  "new_skills_recommended": 0,
  "updates_generated": 3,
  "target_profile": "v1-health-review",
  "shortfall_label": "philosophical",
  "shortfall_reason": "V1 core + support pair assessed as complete; maintenance-only cycle",
  "pipeline_status": "nominal",
  "candidates_unique": 3,
  "patches_shipped": 0
}
```

**Watchdog routing rule:** When `shortfall_label == "philosophical"`, the watchdog MUST downgrade the alert to informational (or suppress if `pipeline_status == "nominal"`). Daily alerting on philosophical shortfalls is alert fatigue; escalate only after 3+ consecutive days with the same root cause as a target-calibration issue (see R15).

## 13.2 Watchdog Alert Template (for Direct Output)

When a watchdog cron job produces its own deliverable (not just internal routing), the output **must** follow this exact format:

**Silent (targets fully met):**
```
[SILENT]
```

**Structural shortfall (alert):**
```
The review job `<job_id>` **has not run yet for <date>** / **ran but failed to produce candidates**.

**Status for <date>:**
- Review job `<job_id>`: **not run** / **ran but produced 0 candidates**
- No session found for today's execution / Model error: <details>

**Today's delivery vs. targets:**
| Metric | Target | Delivered | Gap |
|--------|--------|-----------|-----|
| New skill recommendations | 3/day | 0 | **3** |
| Total updates | 5/day | 0 | **5** |

**Next corrective action:** Trigger the review job manually or investigate why the <time> cron trigger did not fire.
```

**Philosophical shortfall (informational — downgraded, no daily alert):**
```
The review job `<job_id>` ran today at <time> (status: ok) but output remains below target:

| Metric | Target | Delivered | Gap |
|--------|--------|-----------|-----|
| New skill recommendations | 3/day | 0 | **3** |
| Total updates | 5/day | 3 | **2** |

**Shortfall classification:** philosophical — <shortfall_reason>

**Next corrective action:** Expand review scope to adjacent skill domains beyond the core V1 8D pair, or revise standing target to match maintenance-phase cadence (0 new / 2–3 updates/day). Without scope expansion or target revision, this gap will persist daily.
```

**JSON block missing (alert — contract violation):**
```
The review job `<job_id>` ran but the engine report did not emit the required JSON block (section 13.1 contract). Watchdog cannot auto-classify shortfall.

**Manual inspection required:** Reconstruct delivered counts from `state.db` — see `references/watchdog-state-db-reconstruction.md` for the exact recipe (do NOT default counts to 0; a stall after patching is common).
```

**Watchdog execution note:** The watchdog's job is to verify that the engine ran and met targets for the current day. When the engine completes successfully with all targets met, the correct watchdog output is `[SILENT]` to suppress unnecessary delivery. The watchdog should NOT attempt to reconstruct or re-execute the engine's work — it is an OBSERVER, not a producer. Do not confuse the engine's contract (engine must NEVER emit `[SILENT]`) with the watchdog's contract (watchdog MUST emit `[SILENT]` when all is well).

## References

- Existing NEXUS auto-remedication lessons → `skills-library/operations/nexus-auto-remediation/SKILL.md`
- Open-core boundary rules → `skills-library/software-development/open-core-skill-architecture/SKILL.md`
- Release versioning reference → `skills-library/software-development/open-core-skill-architecture/references/release-versioning.md`
- `skills-library/operations/skill-update-engine/references/release-priority-scoring.md`
- `skills-library/operations/skill-update-engine/references/8d-skill-selection-rubric.md`
- `skills-library/operations/skill-update-engine/references/revise-and-resubmit-human-loop.md`
- `skills-library/operations/skill-update-engine/references/process-doc-output-pattern.md`
- `skills-library/operations/skill-update-engine/references/cron-output-retrieval.md`
- `skills-library/operations/skill-update-engine/references/manifest-reconciliation-commands.md`
- `skills-library/operations/skill-update-engine/references/internal-release-flow.md`
- `skills-library/operations/skill-update-engine/references/cron-schedule-spacing.md`
- `skills-library/operations/skill-update-engine/references/class-level-skill-portfolio-principles.md`
- `skills-library/operations/skill-update-engine/references/watchdog-monitoring-pattern.md`
- `skills-library/operations/skill-update-engine/references/watchdog-cron-implementation.md`
- `skills-library/operations/skill-update-engine/references/8d-snapshot-report-stall-pattern.md` — observed single-job stall on 8d-snapshot-report (10 support files) with 6 watchdog cycles, remediation protocol
- `skills-library/operations/skill-update-engine/references/single-job-mode-enforcement.md` — concrete implementation template for single-job mode (JSON-first emission, timeboxing, watchdog contract)
- `skills-library/operations/skill-update-engine/references/watchdog-state-db-reconstruction.md` — exact recipe for reconstructing delivered counts from `state.db` when the engine's JSON monitoring block is missing (do not default to 0); also covers R17 detection: the `[SILENT]`-from-producer classification and the tool-call histogram audit for no-op runs
- `skills-library/operations/skill-update-engine/references/divinity-health-v1-review-job-conflict.md` — documented prompt/skill conflict for the Divinity Health V1 review job (`c37a1090869d`): the job prompt instructs the engine to emit `[SILENT]` on met targets, directly contradicting the skill's producer contract (R17, §11.1). Observed 5+ consecutive stall cycles (Jun 12, 14, 16, 18, 22) with zero assistant output.
- `skills-library/operations/skill-update-engine/references/watchdog-alert-examples.md` — concrete watchdog alert outputs for the Divinity Health V1 review job: philosophical shortfall example (2026-06-23, downgraded to informational) and structural shortfall example (2026-06-25, full alert). Shows template compliance and classification logic.
- `skills-library/operations/skill-update-engine/references/watchdog-metrics-extraction-template.md` — step-by-step template for watchdogs to extract delivery counts and classify shortfalls from engine runs (structural vs. philosophical).
- `skills-library/operations/skill-update-engine/references/watchdog-large-session-retrieval.md` — two-phase pattern for retrieving specific cron job sessions when `session_search` exceeds the 1MB output limit. Uses grep to extract session IDs from persisted output, then calls `session_search(session_id=...)` for the full content.
- SENTINEL compliance audit → `skills-library/compliance/sentinel-compliance-audit/SKILL.md`
- Skill usage data → `skills-library/.usage.json`
- Model compliance guard → `skills-library/model-compliance-guard/SKILL.md`audit → `skills-library/compliance/sentinel-compliance-audit/SKILL.md`
- Skill usage data → `skills-library/.usage.json`
- Model compliance guard → `skills-library/model-compliance-guard/SKILL.md`
