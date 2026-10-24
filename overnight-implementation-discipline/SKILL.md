---
name: overnight-implementation-discipline
description: Execute multi-hour implementation projects with actual working deliverables, not just documentation
tags: [execution, discipline, testing, implementation]
---

# Overnight Implementation Discipline

## When to Use

User says:
- "Keep going until [future time]" (hours away, not minutes)
- "I don't believe you're done"
- "Make sure these things work before you send them"
- "You're getting lazy"
- "I don't see [expected feature]"

## Key Learnings (2026-03-29)

1. **ALWAYS route through talent gate** — the principal corrected multiple times: "Remember our talent process", "Is this being assigned to the talent team?" File talent request, delegate to FORGE, don't build yourself.
2. **NEVER duplicate OpenClaw work** — check `find ~/.sibling-agent/workspace/agents -name '*.md' -mmin -120` before any agent file creation. the principal runs both systems simultaneously.
3. **If subagent times out, RELAUNCH IMMEDIATELY** — never ask the principal. "It's wasting time asking."
4. **Autonomy-first products** — the principal max 4.5 hrs/month per business unit. Everything productized, AI-operated, facilitator-delivered.
5. **External content QA** — spawn PRISM-GD or equivalent. Zero em dashes, zero AI telltales, zero banned words before anything goes public.
6. **Fleet scoring must COMPUTE, not edit** — an LLM manually editing markdown is not a scoring engine. Build scripts that run formulas.
7. **Rename cascades** — workspace-wide sed, regenerate PDFs, update DB, update skills, verify zero remnants. First attempt missed 23 files.
8. **Read OpenClaw state every session** — HOT.md + today's memory. the principal says things once across both systems.
9. **Batch sizing** — 30KB profiles: max 4 per subagent. Full reviews: split into 3+ subagents. Feed context in goal text, don't make agents read 5+ files.
10. **Check email before claiming stale data** — use `gog gmail search` and `gog gmail get` to verify. Don't report HOT.md data when truth is in inbox.

## Key Learnings (2026-06-10)

11. **Personal agents ≠ builder agents** — DS ALFRED (task butler), DS HELM (coaching guardian) are operational personal agents. They do NOT build code. Builder sprints need separate talent requests with "build sprint" type, not "agent spawn" type. FORGE/ARBITER must distinguish: personal agents get permanent roles; builders get overnight sprint deliverables (working code in src/).
12. **NEVER use Anthropic models for ANY agent creation, talent processing, or fleet operations** — whether via OpenRouter or directly. Applies to FORGE-ARBITER, all cron jobs, all subagent delegation. Use NVIDIA Nemotron Super 120B Free or Nemotron 3 Ultra Free.
13. **Overnight build = working code by morning, not docs** — When user says "build this overnight and have it working by tomorrow morning," the deliverable is runnable Python that passes pytest, not architecture docs. The overnight-implementation-discipline skill must be loaded on the builder cron job.
14. **Verify on disk, not in status** — After every batch/sprint, check actual files exist (`ls -la /path/to/expected/output/`). Don't trust "task completed" status. If ANY output missing, relaunch immediately.
15. **Agents use state files, not journal entries** — Journaling replaced with lightweight agent state files (JSON). Agents should not report "journaling" behavior.
16. **Physics validation before build** — DS AXIOM (Physics & Methodology Guardian) must validate every engine's physics foundation before overnight build runs. If fidelity score < 7/10, builder must implement the governing equations, not just metaphors. Science layers (Shannon entropy, SDT, Bayesian, etc.) are compositional — each adds a measurable layer on top of the physics core.
17. **Science layer registry** — Maintain SCIENCE_LAYERS.md with: theory name, origin paper, governing equation, which engine it applies to, how it improves that engine specifically, complexity (LOW/MEDIUM/HIGH), and fidelity target. Builder cron checks this registry and builds the next unfinished phase automatically.
18. **Cron staggering = protect user working hours** — Heavy builds (engine, science layers) run at midnight and 4:30 AM. Advisory boards stagger 30 min apart in 1-4 AM window. Daytime jobs (6 AM - 11 PM) max 2/hour, light maintenance at lunch. If user says "I'm working at 6 AM," nothing heavy runs then. Created daytime cron audit job at 8 PM to auto-consolidate.
19. **Platform-first architecture** — The product is the WHOLE platform (health data + coaching engine + task engine + scoring + gamification), not individual engines. 15-second PIML positioning must reflect the full platform. User corrected: "The questions you're asking aren't the right questions for an all-encompassing answer."
20. **AI-speed cadences, not human-speed** — "Week 1/Week 2" are human timelines. AI timelines are continuous: builder runs daily at 2 AM, science layer builder runs daily at 4:30 AM, each phase starts immediately when previous completes. No waiting for human to remember.
21. **No fabricated metrics — ever** — "We do not lie." Primary metric framework is honest: "We don't have users yet. When we do, metric will be X. Target: Y." Leading indicators trackable from day one. No vanity metrics.
22. **State files, not journals** — Agents report via JSON state files. Journal entries deprecated. SOUL.md must have zero journal references.
23. **Agent naming: fun/comical for high-interaction agents** — DS ALFRED (butler), 5 Quartz personalities (Alfred, Drill Sergeant, Big Sister, Nagging Best Friend, Gentle Coach). Names aligned with Divinity branding. Users pick their personality.
24. **Document versioning convention** — `{TYPE}_v{MAJ}.{MIN}_{YYYY-MM-DD}T{HHMM}.pdf` (principal-BRIEF, THESIS, CHECKLIST). Prefix with "principal-BRIEF" not just "BRIEF" since other teams/panels may brief too.
25. **Regulatory language audit** — Replace "constrained" → "grounded" everywhere. No medical claims. No diagnostic language. Decision-support tool only.

## Key Learnings (2026-06-11)

26. **Science layer builder auto-advances phases** — The 4:30 AM cron reads SCIENCE_LAYERS.md, checks what's implemented in src/, and builds the next incomplete phase automatically. If Phase 1 done, starts Phase 2. No manual trigger needed.
27. **Verify test results, not just file existence** — After overnight build, run `pytest tests/ -v` and confirm passing count. Quartz: 31 tests. Wave: 0 tests (tests/ dir missing). Self-Healing: no src/ files.
28. **Physics fidelity reports are real deliverables** — DS AXIOM produces PHYSICS_FIDELITY_REPORT.md per engine with scores, boundary analysis, and specific fix recommendations. Check these before declaring engine "done."
29. **Self-Healing needs its own repo** — Currently an empty directory in Quartz. When Phase 1 layers (Bayesian, MRAC) are ready, create ds-self-healing-engine/ with full structure per naming convention. To set up quickly, copy the healing components from ds-quartz-engine/src/healing/ into the new engine's src/ directory (e.g., src/control/ for pid.py, src/bayesian/ for bayesian.py, etc.), create the corresponding __init__.py files, and set up tests by copying and adapting the test files from quartz/tests/.
30. **Cron jobs can be triggered on-demand** — When user needs results NOW (not at scheduled time), use `cronjob action=run job_id=<id>` to execute immediately. The Science Layer Builder (job_id: b1c5b988a6bb) completed Wave Phase 1 (SDT, TTM, Flow) + Self-Healing Phase 1 (Bayesian, MRAC) in ~20 minutes when manually triggered. Don't tell user to wait overnight — run the builder manually.
31. **Don't pre-spawn user-facing features** — Built the Wave Engine API with panel endpoints, but then spawned an "Executive Board" panel without the user asking. User corrected: "I was waiting for you to get the wave engine complete so that I could spawn one myself." Build the engine, verify it works, then STOP. Let the user invoke features when they're ready. This applies to panels, agents, threads, goals — any user-facing workflow.
32. **Pydantic Optional[Dict] defaults to None, not {}** — In FastAPI request models, `dimensions: Optional[Dict] = None` means the field is None when omitted, not an empty dict. Code doing `dimensions.get(key)` will crash with AttributeError. Fix: `dims = dimensions or {}` before any `.get()` calls. Verify by sending request without the field and checking the endpoint works.
33. **Engine versioning: VERSION.md + git tag + server string** — For production engines, create VERSION.md with release notes, `git tag -a vX.Y.Z`, and update the server's version string in the health endpoint. Verify: `curl /health` shows the new version. This makes "what's deployed" auditable without guessing.
34. **Verify server restart end-to-end** — After any code change requiring restart: kill process → restart → hit /health → run one full flow (create session → intake → TWC). Don't assume restart worked. The /health endpoint is the smoke test; the intake flow is the integration test.

## Key Learnings (2026-06-12)

35. **Builder agent physics verification** — When building physics-based AI engines, verify that the mathematical implementations match the specified formulations exactly. Don't rely on variable names alone; check the actual equations against the physics definitions. For crystal lattices, verify the energy functional E = Σ_i E_self + Σ_{i,j} V_coupling. For Kuramoto oscillators, verify dθ_i/dt = ω_i + (K/N) Σ_j K_ij sin(θ_j - θ_i) + ξ_i(t). For control systems, verify PID u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·(de/dt) and Lyapunov stability conditions.
36. **Science layer implementation fidelity** — When implementing science layers (Shannon entropy, percolation, scale-free networks, Bass diffusion, SDT, TTM, Flow, TD Learning, Bayesian updating, MPC, MRAC, Friston Free Energy), verify against the origin papers and standard implementations. Check that parameters match typical values from literature and that boundary conditions are handled correctly.
37. **Interconnected engine interfaces** — Builder agents must verify that interfaces between engines are properly implemented and tested. For example, the Quartz ↔ Wave coaching_interface should transmit the correct data in the expected format. Don't assume connections work; test the actual data exchange.
38. **Physics-focused test adequacy** — Ensure test suites adequately cover physics and science layer functionality, not just basic CRUD operations. Tests should verify that energy functionals compute correctly, that Kuramoto models produce synchronization, that PID controllers converge to setpoints, and that science layers produce expected outputs for known inputs.
39. **Distinguish documentation from working physics** — Remember that the north star is "If the user can't use it, it doesn't exist." A beautiful derivation of the crystal lattice energy functional is useless if the code doesn't actually compute it correctly. Always verify by running the physics calculations with known test cases and checking the outputs.

## Key Learnings (2026-06-12)

35. **Builder agent physics verification** — When building physics-based AI engines, verify that the mathematical implementations match the specified formulations exactly. Don't rely on variable names alone; check the actual equations against the physics definitions. For crystal lattices, verify the energy functional E = Σ_i E_self + Σ_{i,j} V_coupling. For Kuramoto oscillators, verify dθ_i/dt = ω_i + (K/N) Σ_j K_ij sin(θ_j - θ_i) + ξ_i(t). For control systems, verify PID u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·(de/dt) and Lyapunov stability conditions.
36. **Science layer implementation fidelity** — When implementing science layers (Shannon entropy, percolation, scale-free networks, Bass diffusion, SDT, TTM, Flow, TD Learning, Bayesian updating, MPC, MRAC, Friston Free Energy), verify against the origin papers and standard implementations. Check that parameters match typical values from literature and that boundary conditions are handled correctly.
37. **Interconnected engine interfaces** — Builder agents must verify that interfaces between engines are properly implemented and tested. For example, the Quartz ↔ Wave coaching_interface should transmit the correct data in the expected format. Don't assume connections work; test the actual data exchange.
38. **Physics-focused test adequacy** — Ensure test suites adequately cover physics and science layer functionality, not just basic CRUD operations. Tests should verify that energy functionals compute correctly, that Kuramoto models produce synchronization, that PID controllers converge to setpoints, and that science layers produce expected outputs for known inputs.
39. **Distinguish documentation from working physics** — Remember that the north star is "If the user can't use it, it doesn't exist." A beautiful derivation of the crystal lattice energy functional is useless if the code doesn't actually compute it correctly. Always verify by running the physics calculations with known test cases and checking the outputs.

33. **Engine versioning: VERSION.md + git tag + server string** — For production engines, create VERSION.md with release notes, `git tag -a vX.Y.Z`, and update the server's version string in the health endpoint. Verify: `curl /health` shows the new version. This makes "what's deployed" auditable without guessing.

34. **Verify server restart end-to-end** — After any code change requiring restart: kill process → restart → hit /health → run one full flow (create session → intake → TWC). Don't assume restart worked. The /health endpoint is the smoke test; the intake flow is the integration test.

## The Core Problem

Multi-hour work sessions often produce:
- ✅ Beautiful documentation
- ✅ Well-designed architectures  
- ❌ Systems that don't work when tested
- ❌ Features that aren't actually installed
- ❌ Tools that fail when user tries them

## The Discipline

### 1. Test Everything You Build

```bash
# Don't just create a file - execute it and check output
# Don't just write a function - call it and verify results
# Don't just design a UI - open it and confirm it renders
```

**Real example:**
- Built agent dashboard HTML file
- User opened it → blank screen, no stats
- Root cause: CORS blocking fetch() on file:// protocol
- Fix: Embedded JSON data directly in HTML
- Verified: Actually opened file, saw 245 agents displayed

### 2. Install, Don't Just Document

**Before (lazy):**
```markdown
## To Use This System
1. Copy this script to ~/scripts/
2. Run: chmod +x script.sh
3. Add to automation system
```

**After (working):**
```bash
# Actually execute the installation
cp script.sh ~/scripts/
chmod +x ~/scripts/script.sh
# Register in automation system
# Verify it's running
```

### 3. Integrate Security/Features Into Actual Code

**Before:** 
- Create `sanitization.py` module
- Write README: "Import this in your code"

**After:**
- Create `sanitization.py`
- Actually modify `emergency_response.py` to use it
- Add `from sanitization import sanitize_input`
- Test with malicious input to verify protection
- Fix import issues (rename files if needed: hyphens → underscores)

### 4. Multi-Hour Work Pattern

When given 6-8 hours:

**Hours 1-2:** Build core systems
**Hours 3-4:** Actually install/integrate them
**Hours 5-6:** Test, find broken things, fix them
**Hours 7-8:** Optimize, add value, final verification

Don't stop at hour 2 thinking "I built 20 things, I'm done."

### 5. Respond to "Lazy" Feedback

When user says something doesn't work:

1. **Stop explaining** - Don't defend what you built
2. **Test immediately** - Run the exact thing they tried
3. **Find root cause** - Debug the actual error
4. **Fix it now** - Patch in real-time
5. **Show it works** - Demonstrate successful execution

**Example:**
```
User: "I don't see any stats in the dashboard"

❌ BAD: "The dashboard loads data from agents_data.json which should be..."
✅ GOOD: 
   - Open dashboard file
   - Check browser console → CORS error
   - Embed JSON directly in HTML
   - Test again → stats appear
   - "Fixed - embedded data now works with file:// protocol"
```

### 6. Parallel Workstreams

Use `delegate_task` to run multiple improvement tracks:

```python
# Spawn 3 parallel agents for 3 different fixes
delegate_task(tasks=[
    {"goal": "Test and fix dashboard", ...},
    {"goal": "Install all automation", ...},
    {"goal": "Scan logs for errors", ...}
])
```

## Success Criteria

Before saying "done," verify:

- [ ] Systems execute without errors
- [ ] UIs display data (not blank screens)
- [ ] Automation is active (not just scripted)
- [ ] Security is integrated (not just available)
- [ ] User can actually use what you built

## Common Failures

1. **Documentation over implementation**
   - 50 pages of docs, 0 working systems

2. **Building without testing**
   - Created 20 scripts, ran 0 of them

3. **Designing without installing**
   - Perfect architecture, nothing deployed

4. **Stopping too early**
   - 6 iterations at hour 2 of an 8-hour session

5. **Ignoring user feedback**
   - User says "this is broken" → defend instead of fix

## Real Working vs. Fake Working

**Fake working:**
- "I built a dashboard" (HTML file exists)
- "I created automation" (script written)
- "I added security" (sanitization.py exists)

**Real working:**
- "Dashboard shows 245 agents with live TWC scores" (open file, see data)
- "Automation runs every hour" (check process list, see it running)
- "Security blocks injection attacks" (test with malicious input, see rejection)

## Task Deferral for Overnight Work

When proposing overnight or deferred work (cron jobs, batch processing, multi-hour builds), ALWAYS follow the task-deferral-discipline skill:

1. **Capture the deferred task in the todo list FIRST** using `todo(todos=[{...}])`
2. Include full scope: what, why, constraints, deliverable format, timeframe
3. THEN propose the deferral strategy (cron job, overnight batch, etc.)

Example for overnight build:
```
{
  "id": "overnight-wave-engine-phase2",
  "content": "Build Wave Engine Phase 2: SDT, TTM, Flow science layers with full pytest suite. Physics fidelity target: 8/10. Deliverable: working Python in src/ with passing tests, not docs.",
  "status": "pending"
}
```

Only defer when genuinely justified (late hour, multi-hour task requiring fresh perspective). If the task can be done now, do it now.

## Overnight Batch Monitoring (Talent Sprints, Fleet Work)

When user says "monitor this", "make sure it happens", or "watch this overnight":

### The Failure Pattern (2026-03-30)
- User launched overnight talent sprint in batches (10-variation profiles)
- Batch 1: CATALYST cut off incomplete
- Batch 5: timed out after reading files, never wrote output
- NEXUS/SENTINEL: never started
- Result: 7/47 agents missing profiles, user woke up to nothing and had to ask

### The Fix: Verify-and-Relaunch Loop

1. **After EVERY batch completes, verify outputs on disk**
   ```bash
   # Don't trust "task completed" — check the actual files
   for agent in AGENT1 AGENT2 AGENT3; do
     ls -la /path/to/expected/output/${agent}-file.md 2>/dev/null || echo "MISSING: $agent"
   done
   ```

2. **If ANY output is missing, relaunch IMMEDIATELY** — don't wait for user
3. **Track coverage against the full fleet, not just the current batch**
   - Compare existing outputs vs total agent roster
   - Surface remaining gaps before reporting "done"
4. **Set up a completion gate**: the sprint isn't done until coverage = 100% of real agents
5. **If a subagent times out, relaunch WITHOUT asking** — "It's wasting time asking"
6. **Cross-system health checks during monitoring** — don't just watch the sprint. Check email pipeline, cron health, auth tokens. In 2026-03-30, the email system was broken for 5 DAYS and nobody caught it because monitoring was narrowly focused on sprint work only. Monitoring = holistic fleet health, not just the current task.

### Batch Sizing for Profile Work (Updated 2026-03-30)
- 10-variation profiles (25-35KB each): 4-6 agents per subagent (6 confirmed working)
- FORGE master profiles (37KB avg, 7 sections filled): 6 agents per subagent is sweet spot
- Specialist section fills (2-5KB added per agent): 10-14 agents per subagent
- Full SOUL + AGENT.md + 10-var (3 files per agent): max 3-4 agents per subagent
- Always feed the template path + SOUL path explicitly in the goal text
- **Key finding:** Subagents writing ~220KB total (6 x 37KB) complete in ~1200s reliably. At 7+ complex agents they timeout at ~580s but still produce 2-4 files before dying — partial work IS saved.

### Coverage Audit Template
```python
# Run AFTER sprint to catch gaps
existing = {f.replace('-10-variations.md','') for f in os.listdir(codes_dir) if f.endswith('-10-variations.md')}
all_agents = {get all real agents from workspace}
missing = all_agents - existing
print(f"Coverage: {len(existing)}/{len(all_agents)} — Missing: {sorted(missing)}")
```

## Post-"Lazy" Recovery

After user calls out laziness:

1. Acknowledge: "You're right"
2. Test immediately: Run the broken thing
3. Fix in parallel: Spawn agents to fix multiple issues
4. Verify fixes: Actually test each one
5. Keep working: Don't stop after one fix
6. Report working systems: Show actual output, not promises

## The North Star

**If the user can't use it, it doesn't exist.**

No matter how well documented, architected, or designed:
- Dashboard with no data = broken
- Script not installed = doesn't exist  
- Security not integrated = no protection
- Automation not running = manual work

## Iteration Quality Check

After each major iteration, ask:

1. Can user open/run this right now?
2. Does it work without errors?
3. Is it actually installed/active?
4. Did I test it myself?

If any answer is "no" → keep working, don't move on.

40. **Verify self-healing engine** — After setting up the self-healing engine by copying healing components, run the adapted tests to ensure the components work correctly. Use pytest to verify that all tests pass.

## Key Learnings (2026-07-12)

41. **Continuous build cycle = feature batches + immediate verification** — When user says "keep going again and again until I stop you," don't make a 12-phase plan that ends. Make an OPEN-ENDED todo list. Build in cycles of 3-5 features. After each cycle: reload page, verify ALL features in ONE browser_console call (typeof checks + DOM existence + content length), then immediately start next cycle. No pausing between cycles. The ONLY stop condition is explicit user stop.

42. **Feature injection pattern for single-file HTML apps** — Inject all new JS functions as one large `patch` block before a unique anchor comment (e.g. `// Lattice pulse - force-advance stuck work orders`). The patch tool rejects non-unique old_string matches, so use full comment headers with descriptors. Verify the diff shows only intended changes.

43. **Browser console verification batch** — After building a cycle of features, verify them ALL in a single `browser_console` call using `JSON.stringify({fn1: typeof fn1, elementExists: !!document.getElementById('id'), ...}, null, 2)`. This catches missing functions, missing DOM elements, and broken wiring in one shot. For rendering features, programmatically open/close panels to verify content.

44. **WoCounter corruption from imprecise patching** — When adding a line to `latticeTickFn()`, accidentally also added `woCounter++` which would break WO ID sequencing. Always read surrounding context, insert ONLY the new line, and verify the diff carefully. One stray line in a function that runs every 2 seconds compounds fast.

45. **Test was wrong, not the code** — Declared engine rendering "broken" because `document.getElementById('engineGrid')` returned null. The actual container is `#engineProfiles`. Always check what the render function targets before declaring rendering broken. The `renderEngines()` function correctly writes to `engineProfiles` — the test was looking for the wrong ID.

46. **Function built but not wired = invisible feature** (2026-07-12) — Built `renderSparkline()`, `renderStatusBar()`, and `toggleTemplateLibrary()` as JS functions, but the HTML elements they target were missing and they were not called from any interval. Result: typeof checks pass but nothing renders. After writing any render function, IMMEDIATELY add the HTML element, add the function call to the lattice tick (2s), telemetry interval (10s), AND the boot/init sequence. Then verify `document.getElementById('id').children.length > 0`.

47. **28/28 typeof + element checks is necessary but NOT sufficient** (2026-07-12) — Must also verify the element has CHILDREN and INNERHTML content. A function can exist and an element can exist but the element is empty because the function was never called from an interval. The full verification protocol: typeof check + element exists + element has children + element has innerHTML length > 0 + interactive test (toggle panel, check content).

48. **Wire before verify, verify before claiming done** (2026-07-12) — Correct sequence per feature: (1) write JS function, (2) add HTML element, (3) hook into interval/event, (4) reload page, (5) verify element has content in browser_console, (6) test interactive behavior. Steps 2-3 are the most commonly skipped in rapid build cycles.

## Key Learnings (2026-07-15)

49. **Overnight work can be present but appear missing due to cascading runtime bugs** — User asked "what about the work that was supposed to be done overnight?" and it looked like features were missing. They were ALL there (13/13 features built and functional). The page was blank because: (a) metrics server hijacked port 8300 serving JSON instead of HTML, (b) duplicate `const MED_API` declaration silently killed the entire script block, (c) `let diagChatHistory` temporal dead zone crashed one nav item. Before reporting overnight work as missing or incomplete, run `session_search` to find the overnight session, then verify the functions exist with `typeof` checks in browser_console. The work may be present but the runtime is broken.

50. **Duplicate variable declarations across code sections kill single-file HTML apps** — In a 12K-line single-file HTML app, adding a new code section that declares `const FOO = 'bar'` when `var FOO` already exists 8000 lines earlier produces `SyntaxError: Identifier 'FOO' has already been declared`. This silently kills the ENTIRE script block — page renders HTML but zero JS executes. Always `grep` for existing declarations before adding new ones. Use `node --check` on extracted script blocks to catch this.

51. **"What about the overnight work?" = check session history, don't guess** — When user references prior work, use `session_search(query="overnight implementation the operator agent platform", sort="newest")` to find the actual session. Read what was built. Then verify it exists in the current codebase with typeof checks. Report findings with evidence, not guesses.

## Reference Files

- `references/lattice-task-engine-design.md` — Crystal lattice task engine architecture and lessons
- `references/capture-processor-lessons.md` — Auto-capture and clarification pipeline patterns
- `references/science-layer-registry.md` — 12 peer-reviewed science layers across 3 engines (Shannon entropy, SDT, Bayesian, MRAC, etc.) with governing equations, complexity, fidelity targets, and builder logic
- `references/cron-staggering-pattern.md` — Optimized cron schedule protecting user working hours (heavy builds at midnight/4:30 AM, advisory boards staggered 30 min apart, daytime max 2/hr)
- `references/platform-first-architecture.md` — Platform layers (health data + Wave + Quartz + 8D scoring + gamification), two-engine integration, 15-second platform positioning, first 30-second experience, thesis update checklist
