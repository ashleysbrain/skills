# PENDING PATCH — timeout-recovery section (parked 2026-08-18, blocked by background _read_before_write guard)

Apply in a foreground session via `hermes curator` or skill_manage patch. Exact find/replace pair:

## FIND (old_string)
```
- Genuinely mid-work (recent think line, substantial calls) → re-dispatch same scope.
Subagents without web access
```

## REPLACE (new_string)
```
- Genuinely mid-work (recent think line, substantial calls) → re-dispatch same scope.
- Verification COMPLETE but deliverable died at generation (all reads/greps landed, exit_reason=max_iterations, "API call failed after 3 retries") → transcript autopsy + WRITE-ONLY re-dispatch (proven 2026-08-18 falsification seat): (1) extract the dying think-line — the finding truncated mid-sentence is often the seat's strongest (dying line read "ledger has **no exter…" → parent verified: no external_id column, no UNIQUE constraint); (2) parent-verify each salvaged claim mechanically; never forward a truncated thought unverified; (3) re-dispatch write-only with facts pre-digested as numbered F1..Fn labeled "parent-verified, do NOT re-check", deliverable structure spelled out, hard tool budget (≤6 calls). Failed run: 1166s/6 calls, zero deliverable. Salvage: complete 13K-char verdict in 99s/2 calls.
Subagents without web access
```

## SECOND PENDING PATCH — after "Dispatch corruption is visible in the ECHO" paragraph, append:

```
**Corruption in your OWN dispatch: steer the live child.** When the PARENT's long-context generation corrupts the goal text itself (mangled paths `/Urs/aw/`, shifted dates, fragmenting section numbers — observed 2026-08-18 seat-4 dispatch), fire `delegate_task(action='steer', subagent_id, message=...)` immediately with: (1) authoritative corrected paths labeled "copy exactly", (2) the real requirement list restated cleanly, (3) "IGNORE the corrupted numbering in the original goal". The steer queues into the child's next tool result and lands before its read budget is spent. Capable children may partially self-heal first (one ran search_files to recover real paths) — steer anyway, then verify the final output against the corrected instruction set, not the corrupted one.
```

## THIRD PENDING PATCH — Phase 4 (Consolidation), append after the paragraph:

```
Consolidation-seat timeout fallback (proven 2026-08-18): when the closer brain's reads all land but the synthesis dies at generation, parent assembly is legitimate ONLY IF the parent (a) holds all banked artifacts in context already, and (b) performs original consolidation work — cross-verifying seat-vs-seat citations (caught: kill-test citation drift in two phases), converting implicitly-covered tests into explicit work items, and restoring requirements dropped between seats (caught: version migration vanished from the build plan). Assembly without original cross-checks is generalist drift; the cross-checks ARE the seat. Gate the assembled document as usual. Full run: references/notion-loop-qa-panel-2026-08-18.md.
```

## FOURTH PENDING PATCH — Pitfalls, append:

```
- **As-of-stamp every volatile count in an evidence pack** (ledger rows, workspace objects, live process counts): panels run long enough for live stores to drift mid-run (observed 180→185 mid-panel; the drift itself became evidence for the dedupe blocker). Static numbers go stale while seats run — stamp `as-of <timestamp>` or seats inherit wrong facts.
- **Marker-scan your own long generations** (tail corruption hits the parent too): after any >10KB execute_code write, scan for duplicated words, stray tokens in table rules, and hyphenation drift; fix via auditable (old,new) replace-pairs and re-scan to zero. An 11-defect generation was caught this way before it reached the principal (2026-08-18).
```

Full session record with all techniques: `references/notion-loop-qa-panel-2026-08-18.md` (landed).
