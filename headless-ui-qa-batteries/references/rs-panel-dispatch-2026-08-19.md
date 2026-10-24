# Fresh-Brain Panel Dispatch Pattern + Census-Prep Pitfalls (2026-08-19)

PENDING SKILL.md INTEGRATION (background curator guard refuses SKILL.md edits in
no-user-present sessions; merge the one-line pointers below into SKILL.md in a
foreground session). Companion to `references/cdp-census-battery.md` (census probes)
and `references/localhost-server-wedge.md` (sync-thread wedge).

## Fresh-brain rotation for adversarial review panels

When the principal asks for reviewers "unlike any that have reviewed the work so far":

1. **Census prior reviewers mechanically before selecting seats.** Grep all audit docs
   for `\bDS [A-Z][a-z]+` and count (Counter). This session: 76 audit docs → 25 prior
   brains (Popper 30x, Codd 28x, Tanenbaum 26x, ...). The census IS the exclusion list.
2. **Pick never-used lenses matched to the failure classes you expect**, not famous-name
   generalists. Product/ui work → the specialist engine (heuristics + cognitive walkthrough,
   3 personas), the specialist engine (evidence encoding, data-ink, hidden-capability verdicts),
   the specialist engine (team design's 5 conditions, permission matrices, tool↔workflow audit).
3. **Feed reviewers a verified mechanical digest; forbid them to read prior audits**
   (one-line instruction: "do NOT read prior audit/*.md files except <the digest>").
   Freshness = no anchoring on prior verdicts. The digest must carry the principal-taste
   constraints (palette, plain words, every-input-operates) so recommendations are
   buildable, not generic.
4. **Exclusive resource lanes per concurrent reviewer** (one owns the CDP port; others
   static-file + curl only; third DB/statistics only). Shared browser profiles produce
   phantom defects from interleaved probes.
5. **Verify before trusting — including refutations.** A reviewer's "digest correction"
   claiming functions were missing was itself wrong: they grepped for
   `fn = function` but the file used `window.fn = function`. Resolution rule: check the
   LIVE surface (curl the served file), not just disk, when siblings/guardian
   auto-restore may have changed the file mid-session. Record verdicts as
   KEPT / REFUTED with evidence in the consolidated plan.
6. **Persist every deliverable to a stable audit path immediately** — subagent summaries
   live in <agent-home>/cache and the full text is often trimmed in transit; read back from
   the saved subagent-summary-*.txt and archive to audit/ before citing.
7. **Consolidation shape that worked:** rotation-record header (who reviewed, fresh or
   not) → master findings index (deduped, severity, source reviewer, owning lane) →
   phases ordered truth-first (kill fabricated data before features) → market steals
   ranked by impact × 1/effort → permanent methodology amendments → metric-of-done per
   phase → open principal decisions list.

## Sherman gate cadence with parallel subagents

The specialist gate expires after 5 minutes and blocks `delegate_task` AND
`execute_code` alike. With a 15-minute panel in flight: re-route
(`specialist_gate.py --route --situation ... --specialist "DS <Name>"`) immediately
before EACH dispatch or code-execution batch; one gate call unblocks both tools for
that window. Keep situations named by task class so routing stays stable.

## the OS ledger integration for review passes

- Mint per-pass tasks: `task_ledger.py --submit --title "<pass>" --kind verify --lane
  deck --origin ceo --by hermes --actor-class ai` (lanes/kinds are taxonomy-constrained;
  there is no ui lane — deck fits product surfaces).
- Claim via module API (CLI has no claim flags): `import task_ledger; tl.claim(c,
  actor, "ai", task_id=tid)` — mind the (actor, actor_kind) order.
- Close with outcome strings that cite the artifact path — method names are only
  citable with execution records attached (anti-decoration law).

## Server-restart port race (new wedge class)

`launchctl kickstart -k` on a KeepAlive service can return while the OLD process still
holds the port: the replacement dies with `[Errno 48] address already in use` in the
service log, the old instance keeps serving, and a battery run right after scores
against stale-but-alive code. Before trusting a restart: check the service log tail for
the bind error, curl the health endpoint, and if you see the race, either kill the PID
holding the port first or accept that the old instance is the runtime target.

## Artifacts from the session that seeded this

- audit/rs-digest-2026-08-19.md (mechanical digest)
- audit/nielsen-r0/rs-nielsen-report-2026-08-19.md, audit/rs-tufte-2026-08-19.md,
  audit/rs-hackman-2026-08-19.md (three fresh-brain reports)
- audit/rs-market-deep-dive-2026-08-19.md (19 competitors + 12 adjacent flows)
- audit/RS-WORLD-PLAN-2026-08-19.md (consolidation, phase model, principal decisions)
