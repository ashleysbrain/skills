# The Corpus Cron Schedule & Collision-Check Methodology

**Last verified:** 2026-06-19

## The three absorption crons

| # | Name | Job ID | Schedule | Provider | Deliver | What |
|---|------|--------|----------|----------|---------|------|
| 1 | The Corpus — Nightly Absorption (2 courses) | `339ad22522e9` | `0 1 * * *` (daily 1 AM CT) | glm-4.6 / Z.AI | local (silent) | Absorbs 2 pending courses from `absorption_queue` into canon.db |
| 2 | The Corpus — Weekly Course Discovery (MIT/Stanford/Yale) | `aa75c79a6dbc` | `0 2 * * 0` (Sunday 2 AM CT) | glm-4.6 / Z.AI | local (silent) | Finds new courses via browser, adds to queue (does NOT absorb) |
| 3 | Science Canon Auto-Update (Weekly) | `fe4aa67d3210` | `0 6 * * 1` (Monday 6 AM CT) | no_agent (script) | local (silent) | Runs `science_engine.py` arXiv scan + `sync_canon.py` |

All three use `workdir: /<workspace>`.

## Why these don't collide

1. **Time slots are separated:** 1 AM → 2 AM (Sun) → 6 AM (Mon). The nightly
   absorption finishes well before the Sunday discovery fires. Monday's science
   sync is 4+ hours after the last absorption run.
2. **Different provider pools:** Absorption crons use Z.AI (glm-4.6). The
   advisory board fleet uses OpenRouter free models (nemotron, deepseek-r1).
   No rate-limit contention between concurrent runs.
3. **Silent delivery:** All three deliver `local` — they do not send messages
   to the user during off-hours.
4. **Queue-gated:** Absorption only fires if `absorption_queue` has pending
   items. Empty queue = cron runs and exits cleanly.

## Collision-check methodology (run before creating new organism crons)

```bash
# 1. List all ACTIVE crons and their schedules
# (via cronjob action=list — filter to enabled=true, state=scheduled)

# 2. Map the schedule to a timeline. Flag any two crons in the same
#    15-minute window. If both are LLM-driven (no_agent=false), that's a
#    collision risk.

# 3. Check provider overlap: if two concurrent crons use the same provider
#    (e.g. both OpenRouter free tier), shift one by 30+ minutes or switch
#    to a different provider (Z.AI for absorption, OpenRouter for advisory).

# 4. Off-hours rule: absorption crons fire 1-6 AM CT only. Never schedule
#    absorption during active work hours (7 AM - 11 PM CT).
```

## Staggering template for new crons

When adding a new organism cron, pick a time slot that is NOT occupied:

| Time slot | Currently occupied by |
|-----------|----------------------|
| 12:00-12:30 AM | (open) |
| 1:00 AM | Nightly Absorption |
| 2:00 AM (Sun) | Weekly Discovery |
| 3:00-3:45 AM | OpenRouter model sync, V1 skill cycle |
| 5:00-5:15 AM | Executive Task Manager, principal AM Advisory |
| 6:00 AM (Mon) | Science Canon Auto-Update |
| 6:00-7:15 AM | principal/COO/CRO advisory boards |
| 7:00-7:30 AM | the operator agent Daily Research Scan, AISHA-MD scoring |
| 8:00-8:25 AM | CTO Advisory, the specialist engine Builder |
| 9:00-9:15 AM | Model compliance, Design Advisory |
| 10:00-10:15 AM | Sentinel, VERITAS Dogfood, various panels |
| 11:00 AM-12:35 PM | TWC algorithm, audit cycles, 8D360 review |
| 1:00-10:00 PM | Advisory panels (staggered), Popper, Diviq |
| 11:00-11:50 PM | Fleet wellness, NEXUS auto-remediation |

**Open windows for new absorption-related crons:** 12:00-12:30 AM (before
nightly absorption) or 4:00-4:30 AM (after absorption, before sync).

## Verification commands

```bash
cd /<workspace>

# Queue depth by faculty
sqlite3 canon.db "SELECT faculty, status, COUNT(*) FROM absorption_queue GROUP BY faculty, status;"

# Next courses to absorb (tonight's batch)
sqlite3 canon.db "SELECT title, faculty, priority FROM absorption_queue WHERE status='pending' ORDER BY priority DESC, id ASC LIMIT 2;"

# Total memory
sqlite3 canon.db "SELECT 'principles: ' || COUNT(*) FROM principles UNION ALL SELECT 'findings: ' || COUNT(*) FROM findings UNION ALL SELECT 'techniques: ' || COUNT(*) FROM techniques UNION ALL SELECT 'ai_tells: ' || COUNT(*) FROM ai_tells;"

# Bloodstream alive check (must return results for multi-word query)
python3 canon_query.py "design principles visual composition beauty" --limit 3
```
