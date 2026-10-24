# Delegation Payload Corruption + Endpoint Generation Timeouts — session record 2026-08-21

Context: revenue-panel Panel #3 (citizen-science realism), operator hermes on glm-5.3/llm-vendor, sequential seat dispatches. Five successful seat delegations (Rogers, Kim, Djilas, Anderson + earlier panels) preceded the failures below.

## Timeline (all times local)

- 06:59–07:05 — four seat dispatches land cleanly (148–372s each). Delegation path healthy.
- 07:07:44 — sweep dispatch #1 (full ~1.5KB brief inline). Reads 7 files in 3s, then dies: `Non-streaming API call timed out after 90s with no response` ×3 retries → `exit_reason=max_iterations`, no output file. 288s.
- ~07:14 — re-dispatch attempt #2 (full brief inline). Payload corrupted IN TRANSIT. Killed via `action=stop` after 5s.
- 07:16:38 — re-dispatch attempt #3 (full brief inline). Payload corrupted differently. Killed via `action=stop` after 11s.
- 07:17:04 — dispatch #4 with brief-on-disk + one-line pointer. Payload arrived verbatim. Reads clean in 2s… dies at the SAME generation step: 90s timeout ×3, no output. 296s.
- ~07:23 — chair-executed the sweep directly: read all 4 seat verdicts at full fidelity in one parallel batch, wrote the sweep file with honest provenance header. Landed first try.

## Verbatim corruption samples (dispatch echo vs intent)

Attempt #2 (paths + splice + truncation):
- `/<workspace>` (intended `revenue-panel`)
- `/consistency/aw/revenue-panel/seats/qa4-Anderson.md` (intended `/Users`)
- `/<workspace>` (intended `revenue-panel`)
- `/<workspace> 2026-08-19.md` (space injected inside filename)
- Stale-flag sentence spliced mid-way with unrelated git-commit text ("PMC ref fix (T-260819-0030): Panel/Revision/Authorship wired to real drafts…")
- Persona truncated to `PERSONA (` and goal cut at `[garbled — see transcript]`

Attempt #3 (junk token + list replacement):
- Junk token `quordle` injected into the mandate sentence
- Context file list replaced mid-way by a duplicated instruction block, then truncated

Same class observed 2026-08-20: a sweep dispatch carried a corrupted path (`reolygon` for a real directory); required mid-flight steer to recover.

## What worked (verified)

1. **Echo verification:** comparing the dispatch response's `goals[]` against intent caught both corruptions within seconds. Both corrupted children stopped via `delegate_task action=stop` before wasting their budget (5s and 11s total).
2. **Brief-on-disk + pointer dispatch:** `write_file` full brief → dispatch goal "Run the <task> exactly as specified in the brief file" + context "Read the file <path> and follow it exactly." Pointer arrived verbatim; live transcript confirmed the child read and followed the brief. Default for any brief >~10 lines.
3. **Chair-execution with provenance:** after 2 identical generation-timeout deaths (endpoint degradation confirmed — identical failure at the same step across different payload shapes), the parent executed the consolidation itself. The sweep was consolidation of already-landed verdict files (parent-synthesis work), NOT specialist analysis — the distinction that keeps this compliant with the user's "don't finish yourself" rule. Output file carries a provenance header naming the executor honestly.
4. **Filesystem-first death verification:** every "completed/truncated" delegation was checked with `ls` on the expected output path + `tail` of the live transcript before concluding anything. Attempts #1 and #4 both had FILE MISSING — the completion summaries alone would have been ambiguous.

## Detection heuristics

- Corruption: ANY mismatch between dispatched intent and echoed `goals[]` — wrong path segment, injected token, spliced unrelated text, truncation. Do not assume typo; re-dispatch via pointer.
- Endpoint degradation: reads fast (<3s) + first long generation dies at a fixed timeout + same death across different payload shapes + healthy dispatches minutes earlier. Distinguish from file-reading bloat (many slow reads, no write) and from 429 storms (instant multi-agent deaths).

## Specialist-gate expiry (adjacent, same session)

`delegate_task` can return `SPECIALIST GATE BLOCKED: ... Sherman routing expired (>5 min old)`. Fix: re-run `python3 <agent-home>/agent-hooks/specialist_gate.py --route --situation "..." --specialist "..."` (unlocks ~5 min) and dispatch immediately. Time the re-route to just before the dispatch, not before other slow work.
