# Unclaimed-Dwell Escalation, Pull-Through, and Taxonomy Evolution — 2026-09-03

Session: principal co-working on the essay; two verdict tasks (5WH falsification
T-260903-0045, outline adversarial T-260903-0047) sat unclaimed at tri:review
while the principal was actively blocked. principal: "how long is it going to sit in there
before it's actioned? Don't do this yourself."

## 1. Escalate-without-executing pattern (lane-law compliant)

When principal-blocked work stalls at a station, the operator NEVER does the work.
Measured response, in order:

1. **Measure, don't estimate**: query ledger state/claimed_by/stage +
   task_events for the tickets; count active claims in the lane
   (`SELECT COUNT(*) FROM tasks WHERE state='claimed' AND lane=...`).
   This session: both unclaimed 26/18 min, research lane had ZERO claims —
   honest projection was ~10h/station dwell (bus #13216 velocity data).
2. **Attach deadlines directly** (the deadline kwarg does not persist —
   known trap): `UPDATE tasks SET deadline=... WHERE id=?` + read-back.
3. **Post an escalation alert** on the bus with: claim-now order, deadline,
   fallback instruction (dispatcher reroutes to any idle volley seat;
   epithelial research first-pass is sufficient to start, adversarial
   follows), and honest root-cause note if the standing mechanism
   (principal-priority lane) is still unshipped — the manual escalation stands
   in for it and says so.
4. **Report flat**: measured dwell, action taken, and what happens if the
   deadline passes (reroute already moving). No vows.

## 2. Pull-through root cause (debrief pattern)

principal follow-up: "if all these things are sitting unclaimed there's a problem
in our process flow — identify and fix it."

Root cause named in debrief
(`stores/session-debriefs/debrief-2026-09-03-unclaimed-tri-dwell.json`):
**claims are voluntary-pull only; no force-route/escalate/reroute exists; and
fix-tasks die in the same unclaimed queue they were minted to cure** — four
ordered fixes (principal lane, station TTLs, dwell fork, re-date) all sat unclaimed
together. Pattern law: *detection without pull-through = alarm theatre; every
ordered fix must carry its own claim-enforcement or it joins the backlog it
was minted to kill.*

Remedy shape (T-260903-0051, consolidated build order to the engine lane):
one order, four mechanisms, each with a FILE-LEVEL target
(glia_conduction.py force-reroute wave; dispatcher principal-preempt queue;
task_ledger.py deadline re-attach at mint; analytics_scout.py slope alarm),
each closing only with LIVE-RUN evidence (a task actually rerouted, a principal
task actually preempted), glial QA verifies — never the builder. The blocked
principal tasks are named in the order as the live integration test: the fix ships
by healing the block it was minted under.

## 3. Taxonomy evolution via mint refusal

Minting the v3-revision gate task failed twice on validation:
- `unknown kind 'writing'` — kinds are a closed set in
  stores/task-taxonomy.json (build/defect/gap/improvement/verify/probe/
  decision/question/maintenance/research).
- `unknown lane 'writing'` — lanes equally closed (scheduler/registry/
  interop/stores/bus/deck/report/gg/fleet/security/legal/connectivity/
  immune/nervous/research).

Correct source fix when the CLASS of work is real and missing: back up
`stores/task-taxonomy.json` (`.bak-<topic>-<date>`), add the kind/lane as
DATA (the registries are data, never code), then re-lane the already-minted
task with a direct UPDATE + read-back. An essay pipeline with no legal
writing task type is exactly the outdated-flow class the principal flags — the
mint refusal is curriculum, fix it at the source rather than shoehorning
into `research`.

## 4. Gated sequencing in the ledger, not in operator memory

principal order "do X once the flows are fixed, don't rush the flows" is encoded
as a task whose detail carries a HARD GATE list (each blocking ticket + its
required outcome, e.g. verdict vocabularies FIT/PARTIAL-FIT/NO-FIT and
ABOVE/PARTIAL/STILL-HARNESS), plus the execution contract for what runs when
the gate opens (first full FLW-WRITING v0.2 pass; verdicts rewrite or kill
spine sections — never orchestrator judgment). GENOME metrics clause tracks
gate pre-conditions; any pre-condition failing >24h alarms. This converts a
sequencing promise into a mechanical trigger instead of the operator
eyeballing readiness.
