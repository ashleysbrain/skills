---
name: product-immune-system
description: >-
  Enforce quality gates at product birth (build passes, tests pass, CI configured,
  no secrets leaked) and run continuous immune surveillance throughout product
  life. Maps to the specialist engine engine (port 8131). Every DS product is born with
  immunity — no product ships without passing these gates.
category: devops
---

## The Product Immune System

Biological mapping: The human immune system protects the body from infection and disease. The product immune system protects software products from bugs, regressions, broken builds, security vulnerabilities, and dependency decay. Every bug caught becomes a regression test — immune memory that prevents reinfection.

| Immune Layer | Human Body | Product |
|---|---|---|
| Skin & barriers | Skin, mucosal membranes | Branch protection, .gitignore, secret scanning |
| Innate immunity | Complement, macrophages — fast, automatic | CI pipeline (build + test on every push) |
| Adaptive immunity | T-cells, B-cells — slow, intelligent | Code review, architecture review |
| Immune memory | Antibodies | Regression tests (each bug becomes a test) |
| Self/non-self recognition | MHC markers | Architectural fit review (is this change "self" or "non-self"?) |

## Birth Quality Gates (Mandatory)

Every DS product MUST pass ALL of these before being declared "born":

1. **Version controlled** — git repo exists, remote configured, .gitignore present
2. **Build passes** — `npm run build` / equivalent exits 0
3. **Tests exist and pass** — at least 1 test file, all green
4. **CI configured** — `.github/workflows/ci.yml` runs build + test on push/PR
5. **No secrets leaked** — scan staged files for API keys, tokens, passwords
6. **README exists** — documents what the product is and how to run it
7. **Dependencies clean** — no dev dependencies in production, lockfile committed
8. **Reimplementation fidelity** (conditional — product IS a rewrite of a
   reference implementation): differential-verification certificate with
   per-stage pass counts, zero unverified stages (see reimplementation birth
   gate below)

Verification commands:
```bash
git remote -v                              # version control
npm run build                              # build
npm test                                   # tests
test -f .github/workflows/ci.yml           # CI
git diff --cached | grep -iE '(api_key|secret|token|password).*='  # secret scan
test -f README.md                          # README
```

## Continuous Surveillance Protocol

After birth, the product immune system runs on a schedule:

### Daily (innate immunity — automatic, fast)
- CI runs on every commit (already handled by GitHub Actions)
- Dependency vulnerability scan: `npm audit --audit-level=moderate`

### Weekly (immune patrol)
- Check all product repos: are they building? Any failing CI?
- Review test coverage trends — is it growing or shrinking?
- Dependency update check: `npm outdated`

### On incident (adaptive response)
- When a bug is found, add a regression test BEFORE fixing it
- Run architectural fit review on the fix
- Tag the commit with the bug class to build immune memory

## The Semmelweis Engine

This skill is the operational procedure for the specialist engine (port 8131), the organism's Product Immune Surveillance engine. When a cron job triggers, it:
1. Enumerates all product repos in the your-org org
2. Checks each repo's CI status via `gh run list`
3. Runs `npm audit` on each
4. Alerts on: failing CI, known vulnerabilities, stale dependencies (>30 days)
5. Logs results to the fleet journal

## Operationalizing: Registering Products with the Semmelweis API

The engine existing on :port is NOT the same as the immune system being
operational. A live Semmelweis with `products_tracked: 0` means the organism
has immune infrastructure but no products enrolled in surveillance. Every DS
product must be explicitly registered.

### Diagnostic: is immunity actually operational?

Check the health endpoint — `products_tracked` tells you immediately:
```bash
curl -s localhost:port/health | grep products_tracked
```
If `products_tracked: 0`, immunity exists but is not enforced on any product.
Register products before declaring the immune system "live."

### Registration flow

```
POST /v1/register          {product_id, name, version}     -> newborn, health=100
POST /v1/milestone         {product_id, milestone_name,    -> +2 health per milestone
                             category, evidence}
GET  /v1/check-readiness/{product_id}                       -> maturation gate
GET  /v1/health-report/{product_id}                         -> full immune chart
GET  /v1/products                                           -> all tracked products
POST /v1/feedback          {product_id, feedback_text,      -> adjusts health ±5
                             sentiment (-1.0..+1.0)}            triggers immune alert if <50
```

### Birth-canal milestone categories

When recording birth milestones, use these immune-mapped categories:

| Category | Immune analog | Example milestone |
|---|---|---|
| `innate_immunity` | Complement, macrophages | `ci_pipeline_active`, `build_passes_clean` |
| `immune_memory` | Antibodies | `test_suite_present` |
| `passive_immunity` | Maternal antibodies at birth | `birth_canal_quality_gate_passed` |
| `reimplementation_fidelity` | Self/non-self discrimination at birth | `differential_verification_certificate` (see below) |
| `barrier_defense` | Skin, mucosal barriers | `branch_protection_soft_gate` |
| `hygiene_protocol` | Antiseptic procedure | `cruft_removed`, `secrets_scanned` |
| `post_birth_documentation` | Birth certificate | `readme_documented` |

### Reimplementation birth gate (differential-verification certificate)

Any product that IS a reimplementation of a reference implementation
(MATLAB→Python port, framework escape, cross-language rewrite — the Spynach
pattern, T-261021-0049) must present a **differential-verification
certificate** before birth: every stage of the rewrite executed against the
reference oracle on identical inputs, per-stage verify/pass counts reported,
ZERO unverified stages shipped. Harness + protocol:
`software-development/engine-stability-audit/scripts/differential_verification.py`
and `references/differential-verification-protocol.md`.

Immune logic (the specialist engine GENOME): the reimplementation's own tests are
self-antigens — the agent that misread the reference also writes the tests.
Only the reference implementation is a trustworthy oracle. A `passive_immunity`
milestone recording the certificate + counts satisfies this gate; every
divergence caught during verification becomes a permanent manifest regression
case (antibody production — manifests grow monotonically like the
immune-memory test suite).

### Maturation gate

`check-readiness/{product_id}` evaluates three thresholds:
- `milestones_sufficient` (enough birth milestones recorded)
- `health_adequate` (health score ≥ threshold)
- `feedback_sufficient` (real user feedback received)

A product is `ready_for_v2` only when ALL three pass. A product with
milestones and health but zero feedback correctly returns `ready: false` —
the immune system requires real-world exposure (feedback) before declaring
maturation complete.

### API interaction note

The the operator agent security scanner blocks `curl | python3` pipes (rightfully).
When interacting with the Semmelweis API programmatically, use `execute_code`
with `urllib.request` instead of piping curl to an interpreter:

```python
import json, urllib.request
BASE = "http://127.0.0.1:port"
def post(path, payload):
    req = urllib.request.Request(BASE+path, data=json.dumps(payload).encode(),
                                  headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)
```

Full API reference and worked example: `references/semmelweis-api-product-registration.md`

## Registry Reference

Engine: the specialist engine
DS-ECS Code: DS-ECS-07.04.01-v3.0.0
Port: 8131
Domain: Lymphatic (Domain 07, Immune System)
Role: Product Immune Surveillance
Dependencies: reproductive, genome, ecs_compliance, clinical

## Templates
- `templates/ci-nodejs.yml` — copy to `.github/workflows/ci.yml` in any Node.js product repo. Runs build + test on every push/PR. Use Node 22+ (Node 20 is deprecated on GitHub Actions runners).

## First Product Born With Immunity
8D Sleep (2026-06-19) was the first DS product to pass all birth quality gates:
repo at `your-org/8d-sleep`, CI green (build + 10/10 tests), README,
.gitignore, no secrets. This is the reference implementation.

## Organ Integration (Immune Response Chain)

When a product degrades, the immune system activates a coordinated response:

1. **the specialist engine** (:port) detects degradation (CI red, vulnerability found)
2. **the specialist engine** (:port) checks for identity drift (ECS code violations)
3. **the specialist engine** (:port) analyzes the threat pattern (adaptive defense)
4. If compromised: **the specialist engine** (:port) verifies all claims against filesystem/reality
5. If broken references: **the specialist engine** (:port) repairs connective tissue
6. Fix becomes a regression test (immune memory)
7. **the specialist engine** clears alert when CI passes green again

Upstream signaling:
- **the specialist engine** (:port, Reproductive): notified when product passes all birth gates (viable for birth/version bump)
- **the specialist engine** (:port, Genome): notified when brand-DNA drift detected
- **the specialist engine** (:port, Clinical): called for deep diagnostic review when multiple products degrade

## Immune Memory Protocol

Every bug found and fixed MUST produce a regression test:

1. Reproduce the bug in a test (it should fail)
2. Fix the code (test should now pass)
3. Document what was wrong and why the test prevents recurrence
4. The test suite grows monotonically — tests are never deleted, only refactored

This is antibody production. The same class of bug can never reintroduce itself.

## Pitfalls

### Branch protection requires GitHub Pro on private repos
GitHub's free plan does NOT support branch protection rules on private
repositories. The `your-org` org is on the free plan. Options:
1. **Make the repo public** (free branch protection — some DS repos are
   already public: `health-intelligence-platform`, `8d-pattern-awareness`)
2. **Upgrade org to a paid plan** ($4/user/month enables branch protection
   on all private repos)
3. **Use CI as a soft gate** (current state for `8d-sleep`: CI runs on
   every push but direct pushes to main are not blocked)

When the user wants to harden a private product repo, surface this
constraint proactively — do not attempt the API call and fail.

### Dev server success does NOT mean the build works
Vite's hot-reload dev server (`npm run dev`) tolerates TypeScript type
errors that `npm run build` (which runs `tsc && vite build`) will catch.
The 8D Sleep build was broken for days while the dev server ran fine.
**Always run the production build, not just the dev server, when verifying
product health.**

### The 11 organ systems (for organism mapping)
The product immune system maps to the **Lymphatic** system in Gray's
Anatomy — NOT "Immune System" as a separate category. The lymphatic
system IS the immune system. the specialist engine (port 8131) lives in the
Lymphatic system alongside the specialist engine, the specialist engine, the specialist engine, and the specialist engine.

## Service Deployment & Management

The Semmelweis engine runs as a persistent service managed by launchd on macOS.
Proper deployment and management ensures continuous immune surveillance.

### Launchd Job Configuration
The engine uses a launchd plist located at:
`~/Library/LaunchAgents/com.divinityscience.semmelweis.plist`

Key configuration elements:
- **WorkingDirectory**: Must point to the engine's root directory (e.g., `/<workspace>`)
- **ProgramArguments**: Should specify the full path to the venv Python and `run_server.py`
- **EnvironmentVariables**: Set `PORT=8131` (or whatever port the engine uses)
- **StandardOutPath/StandardErrorPath**: Direct logs to the engine's `logs/` directory
- **RunAtLoad** and **KeepAlive**: Ensure the service starts on boot and restarts on failure

### Deployment Workflow
1. **Create/update the engine code** in `/<workspace>`
2. **Set up the Python venv** (if not existing):
   ```bash
   cd /<workspace>
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Install/launchd plist**:
   ```bash
   # Copy plist to ~/Library/LaunchAgents/
   cp deploy/com.divinityscience.semmelweis.plist ~/Library/LaunchAgents/
   # Load the job
   launchctl load ~/Library/LaunchAgents/com.divinityscience.semmelweis.plist
   ```
4. **Verify deployment**:
   ```bash
   # Check it's loaded
   launchctl list | grep semmelweis
   # Wait for startup, then health check
   curl -s http://127.0.0.1:port/health | python3 -m json.tool
   # Confirm correct ECS code and body_system
   ```

### Updating a Running Engine
When code changes are made:
1. **Unload the existing job**:
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.divinityscience.semmelweis.plist
   ```
2. **Reload to pick up changes**:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.divinityscience.semmelweis.plist
   ```
3. **Verify the update** took effect via the health endpoint (check uptime is reset)

### Common Pitfalls to Avoid
- **Pointing to wrong directory**: Ensure launchd WorkingDirectory points to the *actual* engine code, not old/dead directories like `ds-maturation-engine`
- **Forgetting venv path**: ProgramArguments must use the venv's Python binary, not system Python
- **Missing environment variables**: PORT must be set if the engine expects it
- **Not verifying after update**: Always check the health endpoint to confirm new code is running (look at uptime_seconds)
- **Logs filling disk**: Monitor log files in the engine's `logs/` directory and rotate as needed

### Health Verification
Always verify the engine is reporting correct information:
```bash
curl -s http://127.0.0.1:port/health | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'ECS Code: {d.get(\"ds_ecs_code\")}')
print(f'Body System: {d.get(\"body_system\")}')
print(f'Port: {d.get(\"port\")}')
print(f'Uptime: {d.get(\"uptime_seconds\",0):.1f}s')
"
```
Correct values for Semmelweis:
- ECS Code: `DS-ECS-07.04.01-v3.0.0`
- Body System: `lymphatic`
- Port: `8131`
