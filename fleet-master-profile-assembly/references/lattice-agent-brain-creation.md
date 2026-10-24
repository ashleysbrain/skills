# LATTICE Agent-Brain Creation Notes

Session-specific notes from the LATTICE build.

## What was built
- New DB-backed agent brain: `LATTICE`
- Role: `Chief Agent Architect — OpenClaw / the operator agent Skill Engineering`
- Job code: `PER-LED-AGT-L6-C5-P31-T5-130`
- Personality code: `P31`
- Profile path: `/<workspace>`

## Useful verification queries
```sql
SELECT code, display_name, personality_code, training_tier, sequence
FROM agents
WHERE code='PER-LED-AGT-L6-C5-P31-T5-130';

SELECT code, name, decision_speed, risk_tolerance
FROM personalities
WHERE code='P31';

SELECT persona_code, persona_name, mbti, enneagram, domain_focus
FROM agent_personas
WHERE agent_id=(SELECT id FROM agents WHERE code='PER-LED-AGT-L6-C5-P31-T5-130')
ORDER BY persona_code;
```

## Pitfall discovered
- SQLite rejected one attempted personality insert because `decision_speed` must be one of the schema-allowed enum values.
- Lesson: before inserting a new personality, confirm allowed enum values from the live schema rather than assuming a nearby value will pass.

## Verification standard
- Always verify both:
  1. DB rows exist and match the expected code/persona linkage
  2. The generated `-profile.md` file exists and reflects the same identity fields
- For single-agent brain creation, a short terminal-based DB probe is enough; no fleet batch orchestration is needed.
