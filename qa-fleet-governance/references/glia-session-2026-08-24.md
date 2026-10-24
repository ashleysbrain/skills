# Glia QA Fleet — session learnings 2026-08-24 (passes 7-12, voice notes, reframe)

Source: full-day principal Telegram session on the QA fleet ("The Glia").

## 1. Opportunity reframe (principal ruling, evening)
- No errors/issues/tickets — only OPPORTUNITIES. Glia help desk = opportunity desk.
- Aliases NOT renames (machine fields stable): severity -> OPPORTUNITY_WEIGHT,
  blocked -> GROWING_EDGE, audit pass -> opportunity harvest pass.
- opportunity_weight drives queue priority.
- principal killed pre/post measurement baseline ("system changes every 10 min").
  Final ruling (10-brain pass #12): bottleneck-first (dwell/WIP telemetry,
  one week, MINT FREEZE) + descriptive macros only + Kuhn 30-day readout
  (voluntary adoption of opportunity language in self-authored text,
  anomaly-resolution rate, bilingual-class census). Goodhart demotion clause:
  any metric promoted to target auto-demotes to diagnostic. NO causal
  mindset claims possible in a self-modifying fleet (Kahneman).
- Felleman catch: static weight->priority = weight-chasing not excitement.
  Fix: priority = weight x novelty-RPE (deviation from band rolling median)
  + top-band scarcity cap (habituation in ~2 weeks without variance).
  claim-latency-vs-expectation = the fleet's actual excitement signal.

## 2. Fleet laws minted today
- ENGINES-VS-AGENTS LAW: engine = one hyper-specific task, own pinned model,
  own harness, machine-checkable DONE, kill criteria, harness-into-able.
  Graduation at >=20 runs + 95% held-out + stable spec.
- POLARIZATION: engine variation = named signal-selected states
  (AUDIT/REPAIR/STANDBY) with MANDATORY exit criteria (glial scarring = a
  state without exit scleroses into an accidental mode). Not "modes" (ECS
  collision) not "plasticity" (too vague to gate).
- PROVEN-flows-only needs a GENESIS clause (new engines run under
  proven-parent sponsorship) or the law outlaws the fleet's own newborns
  (Leibniz HIGH collision, caught same day).
- 2:1 fleet cap REQUIRES mint-time cap-check or it is decoration — violated
  3x within one day of being written.
- Precedence axiom: F>0 terminates regardless of weight.
- GROWING_EDGE must inherit polarization exit predicate (escape hatch fix).

## 3. Isomorphism adjudication pattern (pass #10)
When principal proposes a biology metaphor for a system component, run CONCURRENT-
BLIND seats each defending a DIFFERENT isomorphism + a sweep seat + critic.
Result this time: composite ruling (glial fleet org + polarization engine
variation + immune pre-mint selection + stem-cell bank recruitment layer).
Killed: the 10:1 glia:neuron myth (~1:1, Azevedo 2009) — the workload claim
survived the number dying. Borrowed: skin wound-healing stages -> incident
response flow template.

## 4. Per-technology SME engines (SUBSTRATE-SME class)
- One engine per connected technology, RETROACTIVELY (census everything
  already connected INCLUDING hermes itself, not just future techs).
- Duties: version currency (canary-gated), connection health scan,
  approval-gated optimizations, bounded-context SME answering (its tech ONLY
  — critic amendment: otherwise SMEs sprawl into generalists).
- Mint gate per tech: connection live + >=2 consumers + recurring events.
- First instance: the specialist engine (sibling-agent).

## 5. Handshake contracts (principal: "factual, not claims")
Both sides must FUNCTIONALLY demonstrate capability (live-run record), typed
terms, per-function protocols. A handshake is proven by execution, never by
documentation. When a harness ships 300 features, its SME scans them and the
ecosystem adjusts immediately.

## 6. Stress-opportunity doctrine
- Obstacles: work around, evolve around, BUILD the missing variables (never
  surrender to non-ideal variables — change the circumstances).
- Bounded persistence: F = cost - T*info_gain, stop when F>0 across N>=3
  consecutive iterations; stopping = park-with-knowledge (passive research
  continues). Neither 3-tries nor infinite.
- Open-market math/science/world problems as research-studio stretch targets.

## 7. 24/7 total-goal operation (principal evening rulings)
- QA fleet = TOTAL GOAL running 24/7 (self-review + flow/strategy revision
  loop) as event-driven launchd KeepAlive daemons + event bus. NO CRONS —
  crons = failure-only alerts, healthy = zero output.
- Never depend on principal pushing bus checks — daemons read bus+ledger directly,
  escalate only on lease-expiry/starvation.
- AM briefs: minimal, organized asks as BUTTONS (ADHD law), never walls.

## 8. ADHD principal voice-note handling (proven pattern)
- Digest EVERY ask as numbered items (P1..PN); nothing dropped.
- Accent normalization at intake: principal country accent renders Glia as
  "glier/gleal/gleeya" in transcripts — normalize to canonical terms via
  glossary BEFORE anything downstream reads it; never propagate mishearings
  into naming/docs (principal corrected this directly).
- Gateway drops: voice notes silently lost across gateway restarts. Recovery
  path: ls -lt <agent-home>/cache/audio/ -> newest .ogg -> whisper tiny model
  (local transcription can take 5-10 min on long notes; use background
  process + wait). 6 notes recovered this way in one day.

## 9. Wave architecture for thorough reviews (principal-specified, proven)
Two waves, 10 different brains: Wave A = 5 CONCURRENT-BLIND seats (no
cross-reading); Wave B = 5 DIFFERENT sequential seats that cross-examine A.
Critic consolidates across all 10: verdicts + deduped severity-ranked gap
list + measurement ruling + delta-only micro-tasks. Caught 13 gaps incl 4
HIGH in the day's own work. Rotate critic seat too (capture risk).
