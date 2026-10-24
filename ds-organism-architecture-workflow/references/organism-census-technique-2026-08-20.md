# Organism Census Technique — live body vs map (2026-08-20 session)

Class: "what are we missing" full-organism audits. Produced the 62-live-ports-vs-20-registered finding; bus build_requests #2565 (MeetingAdapter/Fireflies) and #2566 (registry reconciliation) came out of it.

## The four-source cross-diff

Never trust ONE source of organism truth. Diff all four; the disagreements ARE the findings:

1. **Live body**: `lsof -nP -iTCP -sTCP:LISTEN` → classify into engine span (8000-8200), python services outside span, and OS noise (ssh tunnels, ControlCenter, limactl, Electron).
2. **Map (registry)**: `ds-engine-registry/REGISTRY.yaml` (the operator agent repo canonical) → ports, owners, body_system.
3. **Genome**: `ecs.py` ECS code count (`grep -oE "DS-ECS-[A-Z]+-[0-9.]+-v[0-9.]+" | sort -u | wc -l`).
4. **Paper gap registry**: `MISSING_BODY_COMPONENTS.md` — CHECK STALENESS FIRST (see rules below).

Session numbers for calibration: 62 in-span listeners + ~20 out-of-span python services; REGISTRY.yaml 20 engines (all 20 registered ports live = registry accurate but incomplete); ecs.py 81 codes; ~42 shadow engines. ~19 LaunchAgents plists matched ds/gg/hermes patterns vs 12 live DS services.

## Rules learned

- **Registry gaps answer "why aren't we connected to X" questions.** The organism grew organs without registering them; answer capability questions from the LIVE port census, never from the registry alone.
- **MISSING_BODY_COMPONENTS.md goes stale silently.** The 2026-08-20 copy still said "Quartz" (renamed the specialist engine), "Message Fabric Missing" (mesh 53/53 wired per bus #2298), and pre-tissue-layer entries. Cross-check against bus history + ecs.py before quoting. Bus #2566 tasked sibling-agent with the rewrite to current paradigm.
- **NEVER blind-delete launchd plists.** A plist existing is not evidence it is stale — some are watchdogs with long intervals. Per-plist liveness verification BEFORE any deletion.
- **Auth-gate census is part of the organism census.** External ring check (env key NAMES only, never values): grep <agent-home>/.env, `gws auth status`, `gh auth status`, `which xurl/himalaya/memo`. An unconfigured credential = an amputated sense organ; the fix is always a principal gesture, not code.
- **Compose findings into existing ticks, never new crons** (principal rule 08-19).

## Census output shape (what the principal sees)

1. Headline divergence (map vs body).
2. Missing internal organs table (registry's own MISSING list, staleness-corrected).
3. External ring table: surface / verified state / unblock gesture.
4. Physics-ordered build order: registry sync (F<0, unblocks everything) → auth gestures (principal, minutes each) → multiplying assets (semantic store) → rest.

## Specialist-gate note

`execute_code` is specialist-gated alongside `patch`. When a long batch dies with "Sherman routing expired," chain the route stamp AND the action into ONE terminal command: `python3 <agent-home>/agent-hooks/specialist_gate.py --route --situation "..." --specialist "the specialist engine" && <action>`. Verified posting #2565/#2566 this way.
