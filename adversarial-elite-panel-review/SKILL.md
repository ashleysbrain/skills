---
name: adversarial-elite-panel-review
description: Elite panel review before end-user testing finds gaps.
triggers:
  - Before end user the principal or customer touches code
  - After major feature complete but before deployment
  - When user says don't cut corners or prove it works
  - Post adversarial review gap analysis
pitfalls:
  - CLAIMING readiness without running actual code - Result embarrassment
  - TRUSTING git state equals what is RUNNING - Container can have stale code, verify via hash or direct inspection
  - SKIPPING CSS resource checks - Pages render unstyled and look broken
  - LEAVING hardcoded paths like /<home> or /home/user - Breaks portability
  - FORGETTING to gitignore runtime artifacts like dbs, logs, pids - Commits bloat plus privacy risk
  - IGNORING import name collisions like record_interaction from two modules - Runtime errors
  - NOT doing fresh clone test - the principal first run path is not developer state
  - FIRST-BOOT DOCS SAY update.sh - Fresh users must run start.sh; update.sh is pull-later only
  - PRIMARY DOCS CITE MISSING PATHS - tech stack/templates must exist at every cited path
  - AUTHOR PATHS IN HANDOFF DOCS - cyber-gg-blueprint or /<home> in ONBOARDING/QUICK_START
  - WRONG GIT REMOTE - personal fork vs org Cyber-the operator agent; verify remote URL plus matching SHAs
  - TEMPLATE THEATER - guides without copyable in-repo templates
  - TRUSTING tool success without read-back - see tool-output-verification-discipline
steps:
  - RESTATE ask R1 - what must NOT fail for end user
  - CONFIRM git remote is the intended org organism repo (not personal)
  - AUDIT first-boot docs - START_HERE; step1 is start.sh not update.sh; cited paths exist
  - VERIFY git HEAD matches what is RUNNING in container or service
    - Compare file hashes or direct inspection via docker exec
    - Restart if stale because live mounts help but verify
  - SMOKE all end user URLs
    - Main health, /you, /setup, /integrations-adaptive, /ops, key APIs
    - Expect 200 and required fields (recorded, twc_100, engine on health-check)
  - CHECK resource dependencies
    - All CSS and JS referenced in HTML exist and load HTTP 200
    - No hardcoded localhost ports that will not work for others
  - AUDIT hardcoded paths
    - grep -r "/Users/|/home/" in Python files and primary docs
    - Fix with relative paths or environment variables
  - VERIFY identity and persona isolation
    - No the principal or Aisha remnants in configs, HTML, or defaults
    - Phenotype type matches product (gg_core vs locked b2bu)
  - VERIFY templates exist and are non-empty
  - TEST the UPDATE PIPELINE
    - Make a trivial fix, push to org remote, then simulate user ./update.sh
    - Verify fix applies without full rebuild unless Dockerfile or requirements changed
  - FRESH CLONE with ./start.sh (not update.sh)
  - REPORT gaps BEFORE user sees them
    - Critical shows full error, URL, expected versus actual
    - Fix immediately or note as open gap with severity
  - PUSH and confirm HEAD moves on the correct remote
examples:
  - Found missing gg-styles.css caused page unstyled - created file, verified HTTP 200
  - task_engine.py had /<workspace> - removed as the principal personal tool
  - Import collision of record_interaction in user_learning_engine and adaptive_communication - renamed to record_tech_profile_feedback
  - Container code hash not equal git hash - restarted to load live mounted changes
  - Docs said update.sh first - fixed to start.sh plus START_HERE; fresh clone verified
  - ONBOARDING cited missing tech stack path - dual-located file plus fixed docs
  - User push to Cyber-the operator agent not mine - confirmed org remote plus ls-remote HEAD match
validation:
  - After all fixes, fresh clone test (cd /tmp && git clone ... && ./start.sh)
  - Smoke test suite passes all core endpoints plus CSS plus health-check API
  - No hardcoded paths in core Python files or primary docs
  - No the principal or Aisha in configs
  - All resources load, no 404 on CSS or JS
  - git remote is org; local HEAD equals origin HEAD
  - Templates present
references:
  - See references/cyber-gg-adversarial-r4.md for full transcript of R4 review and gaps found.
  - See references/principal-handoff-checklist-2026-08-02.md for first-boot/doc/remote checklist.
  - organism-deployment/references/principal-first-boot-path.md for canonical the principal commands.

scripts:
  - scripts/smoke-test.sh — Automated 8+ endpoint check suite. Run after fixes to verify all core paths work.

---

Use the specialist engine (falsification), the specialist engine (cognitive bias), the specialist engine (stress/allostatic load), the specialist engine (message circulation), the specialist engine (thalamic routing), the specialist engine (brand voice) to find and fix issues NO generalist would catch.

## Triangle offense tri-group routing (principal law 2026-08-26/27, BINDING)

The operator NEVER self-verifies shipped work and NEVER builds after
delegating. Three vertices volley at every process layer: BUILD (glial
fleet, lead-agent-planned) -> ATTACK (adversarial cell, Ravine-routed,
orthogonal lineage) -> VERIFY (QA engine seats). principal never routes traffic.
Pass-count law: first passes cannot be trusted; stop rule = 2 consecutive
CLEAN passes with rotated substrate/profile (typically 4-5 total; engine-
first method measured p_eff ~ 0.79). Verification-discipline laws: every
write-claim needs a read-back of the actual row; use the organism's own
engines (Ravine/Nullius/Ring-1) instead of ad-hoc panels — ad-hoc panels
had reviewer=builder and no evidence gate, and missed defects the engines
caught. Full detail: references/triangle-offense-routing-2026-08-27.md
