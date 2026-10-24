# Absorption Races and Agent-Class Protection (2026-08-21 session)

Session detail for the daemon-cadence-architecture skill: the reload/resume
race, the D1 agent-class severance defect, content-level live/stale DB
proof, and the panel posthumous-sweep pattern.

## 1. Config-change ordering race (bit twice in one morning)

Symptom: `hermes cron resume <id>` prints "Resumed job... Next run: 08:00",
a state check minutes later shows the job `enabled: False / paused`. Looks
like a CLI persistence bug. It is not.

Mechanism: the reconciler daemon keeps running the OLD config until it is
reloaded. `retire_green_crons` in the old config still lists the job in
ABSORB_MAP, so the next pass re-pauses it — usually within the minute. The
resume ack was real; the state was transient.

Correct sequence (binding):
1. Edit the reconciler config (ABSORB_MAP / LANES).
2. `launchctl kickstart -k gui/$(id -u)/com.your-org.cadence-reconciler`
3. Confirm single new PID (`ps aux | grep '[c]adence_reconciler'` — expect
   exactly one; a transient double-start settles within a pass).
4. THEN `hermes cron resume <id>`.
5. Verify ONLY after a full lane pass has elapsed (worst lane interval, not
   seconds). Trust survival-across-a-pass, never the resume ack.

## 2. D1 CRITICAL — agent-class crons retired on foreign greens

`retire_green_crons` pauses any cron whose ABSORB_MAP lane job shows a
3-green streak. If the mapped lane job is a deterministic script but the
CRON is an LLM agent window, retirement severs the agent's routing brain
while the evidence board stays green. Observed 2026-08-21:
- e2bcad9b634c Self-Evolving QA Organ — paused 12:11:56Z by a 45m-lane
  green streak earned by a wrapper script.
- 6bf3256ff89c Conductor Pulse — same class.
- be1535732caa (engagement-return-path) and b18364f94c37 (world-model-radar)
  were queued for the same fate that night.

Fix applied: all four removed from ABSORB_MAP. Rule: agent-class conversion
path is `monitor_script` (hash-compare gate, silent no_change ticks), NEVER
ABSORB_MAP. Post-edit verification must be programmatic — grep the map
against the agent-job census (tmp-verify-absorbmap.py pattern). In this
session the first patch itself shipped 3 fabricated tokens (glm-5.3
calibrated-failure mode); the verifier caught what the visual diff would
not. Never visual-diff a config edit.

Related open finding (D3): `rc in (0,1)` counts WARN exits as green for
streak retirement; retirement should require a per-lane warn-as-green
declaration.

## 3. Content-level live/stale DB proof (mtime lies under WAL)

During verification, main-file mtimes INVERTED the live/stale verdict:
`<agent-home>/message-bus.db` showed Aug 20 13:05 (newer) vs
`your-workspace/message-bus.db` Aug 18 10:32 (older). Verdict from mtime
would have been wrong. What is actually true:

- LIVE: `/<workspace>` — max(id) tracks
  today's traffic (2823), WAL active, row content current.
- STALE: `<agent-home>/message-bus.db` — frozen at 30,375 storm rows
  (Aug-18 alert storm), WAL 0 bytes since Aug 20 22:14, zero writers,
  zero lsof handles. Its `-shm` showed TODAY's timestamp — shm is touched
  by mere READERS (the delegation harness, my own probes), a false-live
  signal.
- Fossils: every underscore variant (`operator_bus.db` under
  your-workspace/, organism/, organism/logs/) is dead since Aug 17-18;
  one has a different schema (no messages table). A structured glob for
  "operator_bus*" misses the hyphen pair that matters.

Probe recipe: `sqlite3 <db> "SELECT count(*), max(id) FROM messages;"` on
each candidate + `ls -la <db>*` for WAL size/mtime + `lsof <db>` for
writers. Judge by content, then WAL file, never the main-file mtime.

## 4. Posthumous transcript sweep (late-echo evidence mining)

A subagent that died at synthesis still gathered evidence. When its async
completion echo arrives after you chair-executed the mandate, sweep the
corpse's transcript (<agent-home>/cache/delegation/live/deleg_<id>/task-N.log)
for tool calls covering threads your own record never touched. In this
session the corpse's bus-naming glob surfaced the underscore-fossil DBs the
chair's own sweep had missed — one net-new finding, chased to ground, zero
re-dispatch. Cost: one read_file + two probes.

## 5. Panel arithmetic that mattered

Seat model: 4 seats (Popper r1, Tanenbaum, Cannon, Deming). Deming died 3x
on the 90s non-streaming llm-vendor timeout; chair-executed on the third. Brief-
on-disk protected the payload, not the lane — the third dispatch loaded its
brief perfectly and still died. After two identical-signature deaths, stop
spending dispatches; execute directly and credit the specialist.
