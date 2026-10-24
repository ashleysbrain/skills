# principal Rejection of a Running Cron: Pause First, Plan Second (2026-08-17)

## Trigger

The principal rejects the OUTPUT of a running cron ("these crons aren't what we
need", "stop sending me this") without specifying a replacement. Observed:
AISHA-MD Daily Unified Scorecard (job 4181f7195527, 7:30 AM daily, deliver to
principal Telegram) — rejected 2026-08-17, same day she commissioned the elite B2C
health organism under the GG3 tier to replace the whole pipeline.

## Rule (order matters)

1. PAUSE FIRST. `cronjob(action="pause", job_id=...)` before any analysis.
   Every further fire before the pause is another unwanted user-facing
   message landing in her chat. Pausing is reversible; unwanted deliveries
   are not.
2. Only after the pause: replacement planning (what the principal actually asked
   for — in this case a full organism-level redesign, plan-only).
3. Never delete the job — pause with the date and the principal-quote reason so
   the consolidation trail is traceable.

## Cross-fleet census (the hermes pause is NOT the whole fix)

the operator agent crons and sibling-agent crons are two separate systems. Pausing the hermes
job does not stop sibling-agent-lane siblings doing the same work:

- the operator agent: `cronjob action=list`
- Openclaw: parse `~/.sibling-agent/cron/jobs.json` (dict, key "jobs"; each job has
  id/name/enabled/schedule.kind/expr) and grep the serialized JSON for the
  function-class keywords (health, wellness, scorecard, standup, 8d, aisha).

Found 2026-08-17: 9 still-active sibling-agent-lane AISHA/8D360 health crons
(AISHA Daily Standup Processor, 8D360 Daily Wellness Check-In, 8D360 HealthKit
Daily Pull, Post-Standup Transcript Analysis, AISHA the operator agent Brief x3/day,
8D360 Sunday Full Check-In, AISHA Medical Intelligence Weekly Scan, AISHA
Weekly Goal Review). Lane rule: sibling-agent's fleet is sibling-agent's — enumerate
them in the consolidation plan and hand off via the operator bus
(sqlite insert into /<workspace>; the
organism/operator_bus.py CLI misinvocations are documented elsewhere); do not
modify another fleet's jobs directly.

## Why pause beats "fix the pipeline"

The principal's rejection was architectural (organism-level rethink), not a defect
report. Improving the scorecard's content would have kept delivering a thing
she said she does not want. When the rejection is architectural, no
output-level fix is responsive — pause, then design the replacement.
