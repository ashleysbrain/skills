# Overnight Execution Failures — Evidence Chains (2026-08-30)

Four failure classes reached the principal in one morning ('what did you even

do????'). Each diagnosis below is fully measured — copy the query patterns.

## 1. FIFO Starvation by R2 Volley Treadmill

**Symptom:** overnight execution order (#7335, posted 23:35) never ran;
interface builds unclaimed 13h; principal: 'why aren't the systems working through
the task list properly???'

**Diagnosis pattern:**
1. `SELECT COUNT(*) FROM messages WHERE status='pending' AND to_op='sibling-agent'`
   → ~120 pending, range 7069..7662.
2. Count overnight run_starts in sibling-agent-autonomic.log per UTC hour bucket →
   63 runs 00:00–10:00, 84 messages completed. Daemon ALIVE and grinding.
3. `SELECT id, subject FROM messages WHERE status='pending' AND to_op='sibling-agent' AND id < <order-id>`
   → 26 ahead of the order; each message takes ~5–8 min (one per headless
   run, 45-min wall cap).
4. Arrival rate ≈ drain rate: R2 countersign loops spawn a new 'R2: Re:
   DONE bus #N...' handoff for every completed volley — the queue never
   drains to the build orders.

**Laws:** posting ≠ dispatching ≠ executing (three gates, each needs its own
receipt). Priority-classed dispatch: build_request/design_request jump the
volley queue; volley loops batch N-countersigns per run; starvation alarm
when any ACTIONABLE ages >4h behind lower-value items. R2 loops need a hard
loop-depth cap (auto-close as latched after N countersigns).

## 2. Morning Brief: Claim-Then-Drop (wake-digest limb)

**Symptom:** principal got no Telegram morning brief; watch condition in
T-260828-0103 explicitly said re-open if no organic digest by 07:00 CDT.

**Diagnosis chain (all stages measured):**
- circadian-state.json transitions: NIGHT 06:31Z (watch part 1 MET), STIR
  12:47:06Z (07:47 CDT — 107min late, stale median-stir entries).
- morning-digest-payload.json regenerated; desktop_notify_ok=true;
  wake_digest --check rc=0; latch deliveries count +1.
- Bus 7649 + 7651 posted 'WAKE-DIGEST ready for the specialist engine delivery' → both
  CLAIMED by hermes-autonomic-bridge at 12:47:33Z, never completed, result
  empty. The bridge flags non-autoack handoffs for an 'R2 responder cron'
  that does not exist. Claim-then-drop = silent death.
- Harvey engine :port /health OK — engine fine, wiring dead.
  Built≠Wired≠Running again.
- Bonus: double-fire (two digests 5s apart) — stir-edge double-tick.

**Laws:** cross-harness handoffs need completion receipts, not claims.
Engine-health and limb-wiring are separate checks. Watch conditions written
at fix-time are immune memory — this one self-declared its breach.

## 3. One-Model Pool Starvation (320 owned, 1 driven)

**Symptom:** principal: 'are we working with grok and the other models or are you
only on glm? this feels really slow for having multiple models.'

**Diagnosis:** dispatch.db `SELECT model, COUNT(*) FROM dispatches GROUP BY
model` → 65 of 68 GO = nvidia/nemotron-3.5-lightning:free, 1 glm-5.3, 2
empty. Grok/GPT-5.6/Claude/DeepSeek/Kimi: zero, ever.

**Root cause chain:**
- Selector pool = technology-registry/prices.json → 10 models (4 glm + 6
  nemotron). Grok/gpt-5.6/claude/deepseek/kimi never added despite being
  connected (provider_models_cache.json: 10 providers/320 endpoints) and
  priced (atlas research).
- capability.store.json = 0 entries — FLW-REGISTRY probe pipeline stalled
  since 08-26; its sensor never alerted on the empty OUTPUT store.
- dispatch.db is the truth table for model usage — query it, don't ask.

**Fix shape (T-260830-0042):** widen pool from atlas live prices; probe all
new members per profile; tier mapping ULTRA=grok-4.6-high/fable-5/sol,
STANDARD=glm-5.3/sonnet-5, FLASH=nemotron/deepseek; acceptance = ≥15
measured models ≥4 providers + live cross-model dispatches in dispatch.db.

## 4. Effort Dial: Lazy Work Was Config, Not Intent

**Symptom:** principal: 'ensure you run heavily on glm 5.3 ultra and not flash.
you are doing lazy work under flash.'

**Diagnosis:** config.yaml line 49 = main session reasoning_effort: medium;
line 397 = DELEGATION reasoning_effort: low. Every dispatched child seat ran
low-effort regardless of orchestrator intent. Model NAME was glm-5.3;
EFFORT was the lazy dial. Patched delegation block low→high, verified by
YAML re-parse. Bandwidth daemon held the ceiling (auto-restore glm-5.3);
nothing held the floor — enforce BOTH ends of any tier.

## 5. Session Hygiene: Client-Stream Errors Masquerade as Model Errors

**Symptom:** principal: 'what is happening with your models??? I keep getting an
error.'

**Diagnosis:** live probe of llm-vendor lane = 2.6s OK (provider healthy). Gateway
log at principal's message time: stream_error_cleanup, TCP force-closed — session
at 841 messages. Auxiliary compression calls to llm-vendor timing out repeatedly
(7–13 min attempts aborting, commit_fence_cancelled) → context can't shrink
→ stream errors. Separately: Copilot credential_pool degraded to RAW token
(models 400 model_not_available_for_integrator).

**Pattern:** before diagnosing provider outage, (1) probe the lane directly
with a minimal chat call, (2) check session size + compression health in
agent.log, (3) grep errors.log for credential_pool degradation. A healthy
provider delivers a broken experience when session hygiene fails. Long principal
sessions should rotate at a context threshold with pinned state handoff.

## Cross-Cutting Laws (all principal-ordered 2026-08-29/30)

- DEBRIEF LAW v2: ≥5 wells, ALL failures, ≥10 learnings, ≥1 triangle
  question — every task, seat, and chain. Omission = half-done work.
- VERIFIED IS A STAGE: verified items must mint downstream action or close
  in the same cycle; dwell clocks + failure-only age alerts (24h sev-1/2,
  72h sev-3/4). kern-878 class.
- Methodology pins go to DS O'Keefe hippocampus (memory_bridge.py,
  positional content arg — probe --help first), NEVER hermes memory tool.
- Triangle verification waves (V1 adversarial → V2 QA ratification → V3
  synthesis) should be minted chain stages, not principal-doubt-triggered.
- DEPLOYMENT-STATE (spec|partial|shipped + artifacts) is a mandatory
  grep-auditable handoff field — docs outpacing wiring was this week's
  recurring failure class.