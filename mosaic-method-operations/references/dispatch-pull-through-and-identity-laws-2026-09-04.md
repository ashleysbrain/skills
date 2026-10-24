# Dispatch pull-through, width-first dispatch, and identity laws — 2026-09-04

Session born from principal distrust escalation: "bus numbering still not corrected…
gone into a black box for days… This is not mosaic methodology."

## 1. MINT-AND-WALK-AWAY (the orchestrator's own posting≠executing violation)

Measured: 15 tasks minted 09-03, escalations posted, ALL 15 still unclaimed
next morning; fleet meanwhile closed 52 tasks and made 138 claims in 24h.
Bus-post verification verifies DELIVERY, not ACTION. A dispatch is not
complete when the message posts — it is complete when the CLAIM lands.

Countermeasure (until T-260903-0051 mechanizes it): every dispatch gets
claim-state checks at +1h/+4h/+24h with alarm on silence. Dispatcher
authority includes force-claim: `claim(c, 'sibling-agent', 'ai', tid)` — claim-and-
assign is routing, not doing the work (lane law holds).

## 2. WIDTH-FIRST CONCURRENT DISPATCH (principal order 07:35)

"Are we only working one task at a time even though we have multiple
harnesses and models? We must optimize and this is way too slow."
Measured: 421 open dep-free tasks, only 2 actors carrying claimed work
(sibling-agent 69, hermes 15). Serial dispatch of independent tasks pays full
latency N times — bad physics. Policy stored in
`stores/dispatch-policy.json`: independent tasks fan out as concurrent
waves across harnesses/models; single-seat dispatch of independent work =
protocol violation unless sole-capable (recorded).

Proof of concept: two verdict seats force-dispatched in parallel returned
in 2 minutes what starved 20 hours in the queue.

## 3. FORCE-DISPATCH VIA DELEGATE SEATS (the working fallback)

When a station starves a principal-blocked task past its deadline:
1. `delegate_task` with isolated contexts, one per verdict, reading claims
   from the LEDGER themselves (not from orchestrator summary).
2. SPECIALIST GATE: delegate_task is blocked if Sherman routing is >5 min
   old — re-run first:
   `python3 <agent-home>/agent-hooks/specialist_gate.py --route --situation "…"
   --specialist "DS <name>"` → unlocks for 5 minutes.
3. Record verdict in ledger with FULL PROVENANCE (seat id, model, duration,
summary-file path).

## 4. SAME-MODEL VERIFICATION IS WEAK VERIFICATION

principal: "I don't trust this work… feels like it could be the operator agent again." Correct
in a precise way: verdict seats were isolated contexts but same model family
as the orchestrator. Law now written: judgment outputs from same-model seats
are CANDIDATE until cross-verified on a DIFFERENT harness; same-model
self-verification of judgments = protocol violation (in FLW-STACK-MATCH and
qa gate). Demote in ledger with explicit CANDIDATE stamp + distrust provenance.

## 5. DEAD-INBOX ROUTING (bus lint catch)

Cross-verify request posted to glia bounced lint: `to_op='glia' last consumed
90h ago (outside 48h window)` — dead consumers named in the lint's consumer
list. Reroute within seconds to a live consumer (qa-fleet). Always read the
lint output on bus posts; it is a delivery-rot early warning, not noise.

## 6. IDENTITY LAW v3 + ANTI-IMPERSONATION (principal 07:47 + 07:49)

ANY principal conversation is with the OS, never a harness. AND the converse:
no harness may claim to BE the OS — identity is granted by the ring model,
never self-declared; runtimes are dispatched SEATS with provenance, never the
OS. Self-naming as the OS = identity usurpation, same severity as fabricated
done-claims. Stored: `stores/identity-law.json` + harness memory identity law.

## 7. principal-GATE BATCHING (principal 08:03 "why am I a bottleneck?")

Audit: 0 tasks owned by principal, but 13 open tasks named a principal gate with no
cadence — gates as one-off interruptions = manufactured bottleneck.
`dispatch-policy.json` ceo_gate_policy: gates batch into ONE decision packet
(consolidated digest, recommended default per item, buttons); safe-default
items proceed unless overridden; only true ratifications (schema cutover,
publication) hard-block; gate misuse = detector finding.

## 8. FLOW-REGISTRY EDIT TRAP: new flow without `code` breaks the ledger

Appending a flow dict lacking `code` to stores/flow-registry.json makes
`gates/task_ledger.py` fail at import: `FLOW_CODES = {f["code"]: …}` →
KeyError 'code' — EVERY subsequent mint dies until fixed. New flows need at
least `code` + `id`. The gate refusal was loud (correct behavior); fix and
re-verify with `import task_ledger` before re-minting.

## 9. FLW-STACK-MATCH (principal methodology as flow, 09-04 07:45)

Census found ZERO stack-matching flows of 59; 13 hard-named a single
harness. Registered FLW-STACK-MATCH (60th): profile → rate (live ratings,
stale >7d below fresh) → physics gate per candidate tuple → select with
recorded basis → width-first dispatch → different-harness verify → learn
loop (outcome vs predicted info_gain adjusts ratings). Build order minted
severity-1; 13 flows marked stack_match_evolution=PENDING (propagate the
class). Mint gates hit in sequence this session: GENOME 8d comma-list
rejected (single dimension only), FLOW-TAG gate requires flow= kwarg —
both already documented in SKILL.md traps; the NEW one is the missing
`code` field (§8).
