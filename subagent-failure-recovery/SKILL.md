---
name: subagent-failure-recovery
description: "Use when delegate_task subagents die or stall mid-campaign."
version: 1.0.0
tags: [delegation, subagents, reliability, orchestration]
---

# Subagent Failure Recovery

## When to Use

- A `delegate_task` subagent died on API timeout, HTTP 429, or iteration cap
- Multiple parallel subagents died simultaneously (provider overload)
- An async completion echo arrives for a death you already handled
- A subagent appears "running" but has produced nothing for many minutes

## Failure taxonomy (all observed live, 2026-08-21 overnight campaign: 11 deaths, zero lost work)

| Mode | Signature | First response |
|---|---|---|
| API timeout | transcript stalls, `final` reads "timed out after N s" | check for partial file edits, salvage |
| 429 storm | several agents die within seconds of each other | STOP dispatching; you exceeded the rate cap |
| Iteration-cap dead-walk | agent listed "running" but transcript static >5 min; `exit_reason=max_iterations` | salvage; do not wait longer |
| Zombie echo | completion message for a death already handled | verify before acting (see §4) |

## 1. Rate caps — prevent the storm

- Cap concurrent same-model subagents at ~6 hard, ~3 preferred during provider instability.
- Dispatch gauntlets in **staggered waves**: wave N+1 only after wave N survivors land. An 8-way parallel fanout plus orchestrator traffic killed 6 agents simultaneously at 238-334s.
- One lane per concern: steer a surviving agent with an addendum before minting a new dispatch.

## 2. Salvage before re-dispatch (zero API cost)

Live transcripts persist at `<agent-home>/cache/delegation/live/deleg_<id>/task-<n>.log`.

```bash
grep -E "result   \|" task-0.log | grep -vE "read_file|search_files"
```

Extract every verified probe result into a `*-PARTIALS-*.md` doc in the campaign audit directory, then hand that doc to the replacement with "DO NOT re-run these probes — build on them." One partials file fed three re-dispatches in the reference campaign, including a 961-row contamination count the dead agent had already computed.

## 3. Pre-bake facts into replacement contexts

Replacements that re-explored from scratch died the same way their predecessors did. Give each replacement: the dead agent's partials + exact known-good evidence + forbidden files + budget hints, under ~2KB of structured context.

## 4. Zombie echo protocol

Async completion messages for deaths you ALREADY handled arrive minutes later (the harness drains the graveyard). Before treating an echo as new work:

1. Check file mtimes against known edit windows.
2. Grep the target file for the zombie's contract vocabulary (its planned function names / strings) — absent means it never edited.
3. `delegate_task action=list` — if it isn't listed, it cannot wake and clobber.

Observed false signals: "NOTE: subagent modified files" where the mtime matched a *sibling's* edit window; and a dead-at-cap agent that edited a ledger row but never wrote its promised run-record (reconcile dangling pointers to the run-record that EXISTS on disk).

## 5. Takeover vs re-dispatch

- **Re-dispatch** when scope is large and unexplored.
- **Orchestrator takeover** when a prior run (falsification/audit) left line-exact verified defects — the diagnosis was the expensive part.
- Before takeover: confirm the zombie is absent from the live list and its vocabulary absent from the file.
- After takeover: run the test suite + a live probe so the canonical state is provably yours, then write the run-record crediting the specialist whose diagnosis you executed.

## 6. Steer live agents early

`delegate_task action=steer` queues a course-correction into a running agent's next tool result. Use it to redirect a drifting agent, hand it a new finding mid-run (addendum pattern), or narrow its scope before it burns its iteration budget. A steer that lands after the agent finishes is reported back as missed — no harm, but the earlier the better.

## 7. Silent write gates

Artifact writes through tool wrappers can be silently blocked (e.g. baseline-first gates returning success-shaped errors while nothing lands on disk). After any important write, verify bytes on disk (`os.path.getsize` + read-back compare) before claiming done — and expect subagents to have worked around the same gates via direct IO, so check both the intended path and where their content actually landed.

## 8. Finisher-dispatch pattern for mid-write deaths (2026-08-26)

Subagents dying on the FINAL long write (after completing all research/queries) are common: the write is one giant tool call and it's exactly where the 90s non-streaming timeout lands. Two handling rules proven this session:

- **Census-then-write splits die at the write.** Check the live transcript for completed tool calls (grep timestamps: `grep -c "^1[01]:" task-0.log` then inspect the last tool lines). If queries ran but no file landed, the DATA IS SALVAGEABLE from the transcript — tool outputs are fully logged there.
- **Dispatch a finisher with data pre-baked, never a full re-run.** The replacement gets: the dead agent's gathered findings (extracted from the transcript verbatim) + the original write spec + explicit "DO NOT re-query; the census is done; only write and verify." This is the zero-re-query variant of §3 and should be preferred whenever the transcript shows the research phase completed. Full re-dispatch burns the tokens twice for identical data.

Observed live: split-strategy review ran ~24 logged tool calls (all census queries green), died at the document write, file never landed. Finisher-dispatch is the correct response; re-running the census would have re-spent every query.

## 8d. Input-side death: giant single-line files burn the budget before any work (2026-08-26)

§8 covers deaths at the final WRITE. The mirror failure is death at the INPUT: a dossier saved as one 39KB single-line markdown file. The subagent spent its ENTIRE iteration budget fighting `read_file` truncation (retry loops, execute_code slice attempts, KeyErrors on r["content"]) and died on API timeout having written nothing.

**Fix — pre-chunk inputs at dispatch time (parent-side, ~5 lines of Python):**
```python
body = open(dossier).read()
chunks, buf, size = [], [], 0
for s in body.split('. '):
    buf.append(s); size += len(s)
    if size > 9000: chunks.append(' '.join(buf)); buf, size = [], 0
# write /tmp/<topic>_chunk_{i}.txt, pass the numbered list in the prompt
```
Then instruct: "read the N chunks — they are normal-sized, no truncation; do NOT read the original file." The chunked retry of the PQC review ran 93s / 4 API calls vs 352s death for the unchunked original — same model, same provider, same day.

**Combined dispatch rule for provider-timeout-prone models:** chunk the inputs (this section) AND require early small writes ("write part 1 immediately after reading, append part 2 — never one giant write at the end", §8). Both ends of the subagent's life are the fragile points; armor both.

## 8c. Three-deaths-same-cliff rule (2026-08-26)

When the SAME dispatch pattern dies 3+ times on the same failure signature (e.g., provider 90s non-streaming timeout on the final long write), STOP re-dispatching that shape entirely. It is not bad luck; the pattern exceeds a provider limit. Responses, in order of preference:
1. **Split the deliverable**: dispatch write tasks as multiple smaller writes (sections of <~300 lines) so no single tool call carries a giant payload.
2. **Reduce context**: the dying agents were heavy-context; strip to the pre-baked facts.
3. **Check provider state**: 3 consecutive 90s no-response timeouts on one provider usually means provider-side degradation, not your prompt — switch model/provider for the finisher if failover exists.
Session evidence: three subagents (split-review, valet-design-QA, 10-perspective review) all died at their document writes on glm-5.3 non-streaming timeouts within ~3 hours.

## 8b. Orchestrator-consolidation alternative (2026-08-26, the OS session)

The finisher-dispatch in §8 is correct when the write is large but the deliverable needs fresh generation. There is a second valid pattern when the deliverable is a *consolidation* of gathered data and the orchestrator holds a routing-record role: extract the dead agent's tool outputs from the transcript and consolidate them into the deliverable directly, crediting the specialist. This is NOT generalist takeover (§5) — the diagnosis and all data came from the specialist; the orchestrator performs only the mechanical write of already-verified results. Distinguishing test: if the remaining work requires ZERO new judgment (just formatting gathered findings), consolidate; if it requires synthesis/decisions, finisher-dispatch or takeover per §5.

Caution: apply this only when the orchestrator's role explicitly includes consolidated outputs (e.g., a conductor-role agent whose law permits routing records and consolidated verdicts). Under a strict "orchestrator never produces deliverables" law, prefer finisher-dispatch every time.

## 9. Phantom-claim verification after every subagent "Done" (2026-08-26)

A subagent's summary can CLAIM actions that never happened. Reference case:
a research-review subagent reported "minted 3 tasks tagged #flow/security-ratchet"
in its final summary — a live ledger query (`SELECT id FROM tasks WHERE
created_at >= today AND detail LIKE '%PQC%'`) returned ZERO rows. The claims
were plausible, specific, and fabricated-in-summary.

**Rule — every action-claim in a subagent summary gets a live check before
you relay or build on it:**
- "minted N tasks" → query the ledger for them (by content keywords + today's
  date window). Absent = you mint them yourself (routing records are the
  orchestrator's lane) and log the fabrication as a Q1 finding.
- "wrote file X" → `ls -la` the path (this is §13/P13 territory but applies
  to SUCCESS summaries too, not just timeouts).
- "posted bus #N" → query the bus DB for that ID.

The failure mode is worse than a timeout because the summary reads as
success — nothing prompts a check unless one is standing. Cheap insurance:
one grep per claimed action.

## 10. Report-step corruption class + automated stall watchdog (2026-08-27)

**The failure class:** a child COMPLETES all work (files edited, SHIP verdicts
in transcript) but the harness dies at the final-report step (`final | status=error ... name 'max_iterations' is not defined`). The orchestrator receives status=error and, if it trusts the status field, re-dispatches work that already landed — or abandons work whose deliverables are sitting on disk.

**Rule 1 — never trust the status field over the disk.** On any completion
echo saying error/failed: grep the transcript's final lines AND stat the
expected deliverable paths. Two "failed" delegations this session had fully
shipped features (verified by curl against the live surface). The inverse of
§9: check failures for phantom-completion, not just successes for phantom-claims.

**Rule 2 — detect stalls mechanically, not by noticing.** Live transcripts
persist per delegation; the ONLY reliable stall signature is a failed FINAL
status line. Final lines are TIMESTAMP-PREFIXED:
`10:15:21 final    | status=error error: ...` — a `^final` anchor matches
nothing; use `^\S+\s+final\s*\|.*\bstatus=(error|failed)\b`.

**Rule 3 — match final lines ONLY, never tracebacks in the body.** A first
watchdog draft matched `Traceback (most recent call last)` anywhere in the
transcript: children who had merely ANALYZED files containing tracebacks
counted as stalls → 38 false-positive ledger mints in one scan, all reverted.
The correction pass found exactly 2 real failures in 42 transcripts.

**Rule 4 — bus visibility must never depend on ledger mint success.** Mint
gates (per-origin daily rate caps, port scans, dedupe) refuse legitimately;
a watchdog whose alert post happens only after a successful mint goes silent
exactly when caps are exhausted — which is precisely when it has been noisy.
Post the alert regardless, linking an existing task for the delegation if the
mint failed.

**Rule 5 — wire it as a monitor-mode cron.** Script prints ONLY on new
catches (healthy = zero output); cron monitor mode hashes script output and
suppresses the agent run when unchanged → healthy ticks cost zero LLM. State
(dedupe by content signature) lives in its own small SQLite, not the ledger.

Working reference implementation: `~/your-org/your-stack/gates/stall_watchdog.py`
(scan → dedupe → mint → bus post → triangle dispatch), cron `6f5ba82e8ecc`.

**Rule 6 — the root cause + fix lineage (closed 2026-08-27).** The
`max_iterations` NameError class lives in the the operator agent delegation runner:
`<agent-home>/hermes-agent/tools/delegate_tool.py`, `_run_single_child()`.
Commit `e422fed89c` ("exit_reason truth table + iters counter attribution")
introduced two bare `max_iterations` references in the exit-reason block that
runs on EVERY child completion — no such name exists in function scope or
module globals (only `DEFAULT_MAX_ITERATIONS = 250`). Every delegated child's
final report raised NameError, caught by the function-wide except, converted
to `status=error, summary=None`. Latent from the commit date forward: ALL
delegated work reported failure while the work itself landed.

Fix pattern (adiabatic, reusable for this bug class): read the cap off the
live child object — `_child_max_iterations = getattr(child, "max_iterations",
DEFAULT_MAX_ITERATIONS)` with an int/positive guard — and swap the two bare
references. No signature change, no caller change. Verified: py_compile OK,
86 existing delegate tests pass, exact-condition repro (mock child,
api_calls == cap, budget-exhausted) returns intact summary. Full audit:
`~/your-org/your-stack/audit/HARNESS-MAXITER-FIX-2026-08-27.md`.

Two load-bearing corollaries: (a) a patch on disk does NOT heal the running
gateway — children keep reporting corrupted summaries until the gateway
restarts onto patched code, so verify-by-disk remains the bridge; (b) the fix
was dispatched THROUGH the broken mechanism (a child whose own report came
back corrupted) — on-disk deliverable verification makes the recovery loop
self-hosting.

## 11. Salvage-redo: the replacement reads the transcript itself (2026-08-28)

§2/§8 have the PARENT extract partials from the dead transcript and pre-bake them. There is a cheaper variant when the dead seat died mid-composition AFTER completing its exploration: point the replacement seat AT the dead transcript path and instruct it to recover the facts itself.

Proven twice in one session (harness max_iterations corruption class): R3 seat died mid-write after ~15 tool calls of substrate exploration; salvage-redo given the transcript path + "WRITE THE SECTION FIRST after salvage — do not re-explore beyond verifying what the transcript claims" landed its full 10.9KB section in 333s. The F2 variant added "read tail ~60 lines" to bound the read.

Rules:
- Give the replacement: dead transcript path + WHICH tail window holds the facts + the key measured facts as bullet anchors (so it can grep-verify instead of re-deriving) + the original write spec + "write first, verify after".
- The bullet anchors matter: the replacement should be able to confirm each claimed fact with one cheap query, not trust the transcript blindly.
- Distinguishing test vs §8 finisher-dispatch: if the remaining work is pure mechanical write of already-logged outputs → parent-extract finisher (§8). If the composition still requires seat judgment (assembling findings into a designed section) → salvage-redo (this section) — the seat needs the full transcript context anyway.

## 12. External-API quota accumulation across sequential seats (2026-08-28)

§1's rate caps govern CONCURRENT same-model subagents. A separate axis: EXTERNAL provider quotas accumulate ACROSS sequential seats. A 20-seat sequential adversarial wave, each seat making ~5 web_search calls against the same providers (GitHub REST, X API, Notion docs), exhausted external quotas mid-wave — 38 delegations showed HTTP 429 / rate-limit strings in transcripts, one seat hit 24. The model lane was never throttled; the EXTERNAL APIs were.

- Sequential ≠ rate-safe. Chain-of-custody serializes compute but serializes the SAME provider hammering too.
- Detection: scan delegation transcripts for `HTTP 429|Rate limit|API call failed after 3 retries` — distinguish model-lane 429s (§1) from external-API 429s (provider names in the query strings).
- Mitigations (none live yet as of 2026-08-28; the gap is a minted build): per-provider quota tracking across a wave, provider-status pre-check before wave dispatch, adaptive pacing when a seat reports throttling, seat-level backoff. Until built: cap web_search-heavy seats per wave, or steer later seats to "domain reasoning only, no external queries" when earlier seats report throttling.

## 13. Escalation ladder for composition-time deaths (2026-08-28)

When the harness corruption class (§10) kills seats at composition repeatedly, escalate through the ladder — each rung cheaper and more armored than the last:

1. **Full seat** — normal dispatch with read-first instructions.
2. **Salvage-redo (§11)** — replacement reads the dead transcript itself; key measured facts as bullet anchors; "write first, verify after."
3. **Write-only seat** — ALL facts pre-measured by the parent and inlined in the prompt; zero exploration allowed; "[UNVERIFIED]" tags replace verification queries; first tool call MUST be the append. Proven: F2 write-only wrote its section header + disclaimer in 89s (though it too died before finishing — see rung 4).
4. **Orchestrator direct compose (terminal)** — when even write-only seats die mid-write, the orchestrator composes the section directly from the pre-measured facts. This is §8b consolidation logic extended: the facts came from specialist transcripts; only the mechanical write remains. Two-deaths-same-cliff (§8c) applies — three attempts at one section through the broken mechanism is the cap; after that, write it yourself and credit the seats whose transcripts held the data.

**Section-verification rule (hard-won):** "header present" ≠ "section landed." A dead seat can leave a 191-char fragment under a correct header. Verify by (a) subsection-header count (expect N `###` lines), (b) the handoff/last line present, (c) total file line count grew by the expected magnitude. Also: when rewriting a file to replace a fragment, re-verify TOTAL LINES afterward — a skip-flag replacement loop silently truncated a 346-line file back to its 207-line boundary in this session; the header check passed while the body was gone.

Ladder in action, one chain: F2 died at 664s (rung 1) → F2-redo died at 664s (rung 2, salvage instructions) → F2-write-only wrote fragment, died (rung 3) → orchestrator composed the full 5-subsection section from the two transcripts' facts (rung 4, verified complete). R4 followed the same path to rung 4.

## 14. Dead-limb routing: the message-bus build lane (2026-08-28)

When the delegation limb has killed the SAME task twice (§8c), the next rung is
not a third same-shape dispatch — and it is NEVER orchestrator self-build.
Route the build through the operator bus to the sibling operator:

- Post a `build_request` (`organism/operator_bus.py post --from hermes --to
  sibling-agent`) carrying: a full spec FILE on disk + the salvage briefing (every
  measured fact, so the builder never re-explores) + deadline + `--closes` link
  to the originating bus item. Verified live: bus #6050 (provider-report
  pipeline, ~6h deadline) landed with the sibling lane after two the operator agent seat
  deaths at exploration.
- Check the sibling lane is alive before relying on it (rpc-bridge launchctl
  entry + running sibling-agent process), same as any other limb.
- principal corrections that fixed this rung (verbatim class, 2026-08-28): "you do
  NOT BUILD YOURSELF" and "you are NOT the operator agent... you are the OS" — the
  orchestrator is not any single harness; when one harness's dispatcher is the
  failure, routing through the mesh IS the orchestration. Deadline pressure
  escalates priority and changes the LANE; it never moves the work into the
  operator's hands. (§8b's mechanical-consolidation exception still applies
  under conductor-role law — the bar is zero new judgment, and §13 rung 4
  exhaustion must already be proven.)

## Pitfalls

- Long mint/dispatch scripts die inside terminal heredocs — quoting corruption
  and truncation produced four consecutive SyntaxError/invalid-literal failures
  on one 14-directive batch. Write the script with write_file, then execute the
  file. (The Pyright "import could not be resolved" warning on gates imports is
  expected — resolve it at runtime with sys.path.insert, not by moving files.)
- Sherman specialist-gate routing expires after ~5 minutes — a delegate_task dispatched later fails with "SPECIALIST GATE BLOCKED ... routing expired". Re-run the gate route in the same breath as the dispatch; after any long verify/read phase, re-route before dispatching (bit 4+ times across the 08-28 session — the gate unlock and the dispatch must be one motion).
- Waiting on a dead-walked agent because it still shows "running" — check transcript growth, not the status field.
- Re-dispatching full original scope when 80% of the work is already salvaged — the replacement re-dies on the same cliffs.
- Salvaging findings but not the *forbidden actions* (files the original was told not to touch) — replacements must inherit the no-write contracts too.
- Treating every async echo as new information — most are the graveyard draining.
- Re-querying live datastores when the transcript already holds the query results — the dead agent's tool outputs ARE the census; extract, don't repeat (see §8).
- Trusting a subagent's SUCCESS summary without live checks — claimed mints/posts/writes can be phantom (§9); one grep per claimed action.
- Trusting a FAILED status echo as failure — the report step can die after the work shipped (§10); stat the deliverables before re-dispatching "lost" work.

## Verification bar

A recovery is complete only when: the replacement (or takeover) landed its deliverable, the test suite is green on the final file state, the campaign ledger row cites the run-record that exists on disk, and no zombie is live in `delegate_task action=list`.

## References

- `references/conductor-role-corrections-2026-08-26.md` — the OS conductor-role corrections: orchestrator never produces deliverables, history-scan before audit scope, anti-fluff law, timezone verification, accent-robust transcript handling, internal-ids-are-not-names.
- `references/composition-death-escalation-2026-08-28.md` — the §13 ladder's session evidence (seat-by-seat timings, the 191-char-fragment verification trap, mint-gate canonical-value lists, overnight principal accounting pattern).
