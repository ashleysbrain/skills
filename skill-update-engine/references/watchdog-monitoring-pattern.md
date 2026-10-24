# Watchdog Monitoring Pattern for Skill Update Engine

This document defines the monitoring contract between the skill update engine and downstream watchdog cron jobs. Watchdogs consume engine output to verify daily targets are met and alert on drift.

## Required Engine Output Format

Every engine run that produces a report **must** emit the following JSON block so watchdogs can programmatically classify shortfalls:

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

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `new_skills_recommended` | Yes | Integer count of new skill candidates synthesized this cycle. |
| `updates_generated` | Yes | Integer count of updates to existing skills (patches, reference additions, manifest fixes, etc.). |
| `target_profile` | Yes | Name of the active target profile (e.g., `v1-health-review`, `default-maintenance`). |
| `shortfall_label` | **Yes (when targets not fully met)** | `structural` (scan failed, sources unavailable, model error, pipeline stall) OR `philosophical` (family reviewed and found coherent, no genuine gap exists). |
| `shortfall_reason` | When `philosophical` | One-sentence explanation of why the family is complete. |
| `pipeline_status` | Yes | `nominal`, `degraded`, or `stalled`. |
| `candidates_unique` | Yes | Integer count after dedup. |
| `patches_shipped` | Yes | Integer count of patches applied this cycle. |

## Watchdog Alert Template (for Direct Output)

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

## Watchdog State-DB Reconstruction

When the JSON block is missing, the watchdog must reconstruct what the engine actually shipped by querying `state.db` directly — do **not** default delivered counts to 0. A single-job stall (R16) commonly occurs *after* several patches have been applied, so the true delivered count is often greater than zero even when no report was emitted. The concrete recipe (resolve session id, confirm the last assistant message is truncated, count `{"success": true, "diff": …}` payloads, group by patched skill) lives in `references/watchdog-state-db-reconstruction.md`.

Key pitfalls captured there:
- `session_search` FTS can return zero hits for today's run before indexing catches up — fall back to direct `sqlite3` queries, do not conclude "no session found" from an empty FTS result.
- The cron-output `.md` dump is raw and may be truncated; it is not a curated report. `state.db` is authoritative.
- A stall with `{"success": true, "diff":}` payloads in the session means patches landed — classify as `structural` (stall) but report the real delivered count, not 0.

## Related Risks

- **R15 — Watchdog target-profile mismatch with edit-first policy**: When a watchdog tracks the engine against an expansion-phase target (3 new/5 updates) but the engine correctly operates in maintenance mode (0 new/2-3 updates), persistent alert fatigue occurs. The `shortfall_label` field resolves this by letting the watchdog distinguish structural vs philosophical shortfalls.
- **R6 — Candidate starvation under low-signal conditions**: If the market is quiet, the pipeline may fail the "3 candidates minimum" rule. ARBITER injects a "market sweep" candidate. This is a structural shortfall if the sweep also fails.

## Single-Job Mode Enforcement

For review jobs running in single-job mode (entire pipeline in one cron job), see `references/single-job-mode-enforcement.md` for the mandatory JSON-first emission pattern, timeboxing requirements, and watchdog contract compliance.