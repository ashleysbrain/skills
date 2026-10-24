# QA Fleet Seat Build — 2026-08-24 session (Nedergaard, Ford, Thompson, Saltzer)

Four elite seats minted + wired in one session. Working pattern and the
laws that bit, for any future seat build.

## The repeatable seat-mint sequence (proven 4x)

1. **Name first, collision-check always**: 4-category naming (scientist /
   law / principle / concept); verify the name is unclaimed with
   `rg -l "DS <Name>" ~/your-org ~/your-workspace` BEFORE
   writing anything. Names used this session: the specialist engine (glymphatic
   clearance, Iliff 2012), the specialist engine (Ford-Fulkerson max-flow/min-cut),
   the specialist engine (D'Arcy Thompson transformation grids, *On Growth and
   Form* 1917), the specialist engine (Saltzer-Schroeder 8 principles + end-to-end
   argument). Each name's physics MUST provide the governing equation
   that drives the seat's actual behavior.

2. **Register the FLOW before the ledger mint.** The task_ledger genome
   gate rejects unknown flow codes (`ValueError unknown flow code`) —
   mint the flow in `stores/flow-registry.json` FIRST. New flows are born
   with `owner` + `sensor` + `verified` from day one (all 31 legacy flows
   shipped without them — that omission is why the specialist engine exists).

3. **Mint script pattern** (idempotent, mirrors `mint_qa_fleet.py`):
   `your-stack/scripts/mint_<name>.py` — ORGANS.json append (additive,
   bump organ_count, verify count == len) + task_ledger.submit with
   GENOME block (`kind=build` requires it). Stage vocabulary warning
   ('minted' is legacy; use the flow's own stage list) is accepted.

4. **Methodology file**: `your-stack/methodology/DS-<NAME>-METHOD
   OLOGY.md` — lineage, the governing physics AS BEHAVIOR, operating
   loop, standing laws, interfaces, verification hooks (what proves the
   seat is alive).

5. **Organ script** in `organism/`: deterministic detectors → reversible
   action → manifest/telemetry log → route (bus / ledger mint).
   Exit-code contract: 0 clean, 1 findings (healthy), 2 broke.

6. **Wire into `autonomous_iteration.one_pass()`** as a new pass function
   (e.g. `security_pass()`), add its result to the LOG dict. NEVER a new
   cron. Compile, then kill-test: `kill <pid>; sleep 15; launchctl list |
   grep autonomous-iteration` — new pid under KeepAlive proves
   supervision; the daemon picks up the new lane on restart.

## Pitfalls that bit live this session

### Dedupe key MUST be a literal prefix of the minted title (hit TWICE)
`flow_lint.py` minted 90 duplicates on its second run because the dedupe
key was prose-shaped, not a title prefix. The S8 lesson in
improvement_scan.py says exactly this and I still re-hit it — then
re-hit it AGAIN with a weak `or` guard in the assert. FINAL LAW:
construct `key = "EVOLVE: <subject> <check>"`, `title = key + " — " +
prose`, `assert title.startswith(key)`, dedupe with
`SELECT COUNT(*) FROM tasks WHERE title LIKE key||'%'` (all states, not
just open). Test = run twice; second run MUST mint 0.

### The ledger is append-only (birth certificates)
`DELETE FROM tasks` is blocked by trigger (error 19). Duplicates are
closed, never deleted: `UPDATE tasks SET state='cancelled', outcome=
'duplicate...' WHERE id NOT IN (SELECT MAX(id) ... GROUP BY
substr(title,1,60))`. Note the CHECK constraint allows only
open/claimed/done/blocked/cancelled — no 'closed' state.

### Whitelisting a decoy as live (the Nedergaard self-catch)
I whitelisted `<agent-home>/cron/cron.db` as "live" without probing it.
The QA pass found it 0-byte with NO schema — the LIVE cron store is
`jobs.json` (JSON, not a DB at all). LAW: a live-whitelist entry must be
proven by schema + rows + (ideally) open-file/process evidence, never by
name plausibility. The cleanup seat then quarantined its own author's
mistake — exactly the design intent.

### tasks.db is NOT the ledger
`your-stack/tasks.db` exists but has no `tasks` table in the expected
shape — the real ledger is `your-stack/stores/task-ledger.db`
(schema: id/title/kind/lane/.../state/flow/stage...). Use
`gates/task_ledger.py`'s connect() like the mint scripts do.

### bus INSERT is 7 columns
`messages (timestamp, from_op, to_op, msg_type, subject, content,
status)` — count them; '6 values for 7 columns' on first try.

### Kill-test from inside the gateway shell can SIGTERM yourself
`kill $OLD` in the same terminal sometimes takes the shell down
(exit -15). Survive it: just re-run `launchctl list` + `ps` in a fresh
call to confirm the new pid.

## The four seats (what they own)

| Seat | Code | Organ | Law |
|---|---|---|---|
| the specialist engine | IMM-13.09.01 | organism/glymphatic_sweep.py | W'=P−K·W: route overproduction to producers; move never delete; liveness (lsof) before clearance |
| the specialist engine | IMM-13.10.01 | organism/flow_lint.py | max-flow=min-cut: only the bottleneck is worth improving; flows need owner+sensor+verified |
| the specialist engine | NPR-04.11.01 | organism/isomorphism_lint.py + telegram_ask.py + stores/isomorphism-register.json | isomorphism = falsifiable deformation or retract; principal questions ADHD-friendly w/ 24h default |
| the specialist engine | IMM-13.11.01 | organism/security_audit.py + FLW-SECURITY + SECURITY-ARCHITECTURE.md | every verdict names the mechanism; CRITICAL pages principal; fleet stages (Denning/Shamir/Schneier) gated on the principal-review checkpoints |

## principal telegram_ask format (ADHD law, live-tested)
One question per message; BUILD context line; options as lettered
pickable rows; explicit "DEFAULT if no answer in 24h". Token+chat read
from <agent-home>/.env (TELEGRAM_BOT_TOKEN / TELEGRAM_ALLOWED_USERS) —
same pattern as telegram_liveness_watchdog.py. Every ask logged to
telemetry/thompson-questions.jsonl.
