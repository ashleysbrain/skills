# Spec-vs-Runtime Gap Audit (revival pattern)

**Added:** 2026-07-19 — session where user asked to "get this fully operational" and we discovered the spec docs and runtime had drifted apart.

---

## When to use

When the user says any of:
- "get this fully operational"
- "go back through our prior work"
- "show me the processes"
- "we built this a long time ago"
- "this is more than a cron"

…they are usually pointing at a **spec/runtime desync**: the docs describe the intended system, the runtime implements a subset, and nobody has reconciled them recently.

## The technique (4 moves)

### 1. Digest — survey both layers in parallel
- Spec layer: every `.md` / `.yaml` in the repo's docs + the canonical process docs
- Runtime layer: route registry (`grep -nE '@app\.(get|post|...)' src/.../api.py`), models, state fields, cron jobs, running processes

### 2. Build the gap table
Two columns: **Spec says** vs **Runtime does**. One row per behavior. Examples that consistently surface for this engine:

| Spec says | Runtime does |
|---|---|
| 10-step flow with monitoring state | 4 CRUD modes, no monitoring |
| Consecutive advisor deliberation with synthesis | placeholder endpoint, no real advisor logic |
| Persistent 24/7 loop with research_queue, next_checkin, panel_revision_notes | no background loop |
| 6 question families, one-at-a-time, stop rule | free-text intake, no question routing |
| 6 response types with synthesis rules | generic text response |
| Handoff format with 6 fields | no handoff endpoint |

### 3. Read the gap as a phased revival plan
Sort gaps by dependency, not by glamour. For this engine the adiabatic order is:

- **Phase 1 — State machine into runtime** (everything else depends on session state being real)
- **Phase 2 — Consecutive advisor deliberation** (the product moat; plugs into mastermind + advisor-panel-orchestration skills)
- **Phase 3 — Persistent 24/7 monitoring** (monitoring state, research_queue, panel-revision detection, signal-only interruptions)
- **Phase 4 — Question flow + response type classifier** (UX polish; depends on real state existing)

### 4. Surface the reconciliation, don't bury it
Present the gap table to the user before proposing work. They built the spec — they need to see exactly where the runtime stopped catching up. Do not silently "fix" the spec down to match the runtime; the spec is usually the source of truth.

## Common pitfalls

- **Treating persistent mode as "a longer answer."** It is not. It is an ongoing support loop with a `monitoring` state, `research_queue`, `next_checkin`, and `panel_revision_notes`. A cron that fires a coaching prompt is a *trigger*, not the mode itself. The user's phrase "this is more than a cron" is the tell that you are under-modeling persistence.
- **Skipping the gap table and jumping to "Phase 1."** Without the table the user can't see which behaviors are missing, and you can't defend the phasing.
- **Phasing by glamour instead of dependency.** Advisors are the moat, but they depend on real session state. Don't start with advisors.
- **Forgetting the empty modules.** `learning/`, `resonance/`, `healing/`, `control/`, `coaching_interface/` exist as directories with no implementation. Treat them as "designed, never built" — they are NOT evidence the feature exists.
- **Assuming the running port matches `run_server.py`.** Launchd-managed processes can hold a different port than the file declares. Always `lsof -nP -iTCP:<port> -sTCP:LISTEN` and `ps -p <pid> -o command` to verify the live process matches the file you're reading.
- **Confusing "shim" with "canonical."** `src/api/server.py` may be a re-export shim; the real routes live in `src/server/api.py`. Read both before declaring the route set.

## Verification commands (reuse, don't retype)

```bash
# Route registry (canonical)
grep -nE '@app\.(get|post|put|delete|websocket)' src/server/api.py

# Live process vs declared port
lsof -nP -iTCP:port -sTCP:LISTEN
ps -p $(lsof -nP -iTCP:port -sTCP:LISTEN | awk 'NR==2{print $2}') -o pid,ppid,command

# Empty module detection
for d in learning resonance healing control coaching_interface; do
  count=$(ls src/$d/ 2>/dev/null | wc -l)
  echo "$d: $count files"
done

# Cron jobs referencing the engine
jq -r '.jobs[] | select(.name | test("wave|coach"; "i")) | "\(.id) | \(.name) | \(.schedule)"' <agent-home>/cron/jobs.json
```

## Related

- `references/canonical-process-doc-set.md` — the 10-step spec itself
- Step 7 of the main SKILL.md ("Verify the runtime-facing package") is the seed of this technique; this file extends it into a full revival pattern.
