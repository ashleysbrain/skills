# the operator agent / OpenClaw — Skill Family & Release Architecture

**Version:** 1.0.0 — 2026-05-31  
**Lens stack:** FORGE · ARBITER · PARALLAX · SENTINEL · NEXUS · Open-Core Product Strategist

---

## 1. Family Map

The the operator agent / OpenClaw ecosystem is split into **three families**, each with its own
current stable core anchor. A family is a grouping of skills that share a domain,
a version lineage, and a coherent upgrade narrative.

| Family | Domain | Current Stable Core Anchor | Open-Core? |
|---|---|---|---|
| **the operator agent Agent** | Agent runtime, tools, gateway, plugins | `v1.0.0` (initial public core) | Yes — repo is open-source |
| **OpenClaw Fleet** | Multi-agent orchestration, spawning, analytics, journals | `v1.0.0` (internal core, not yet public) | Partial — internals private, patterns public |
| **Skill Authoring** | Skill/SOUL authoring, open-core packaging, release discipline | `v1.0.1` (open-core-skill-architecture) | Yes — already public skill |

### Why three families, not one

Merging them would create a single monolithic anchor that can't move independently.
Splitting by domain lets each family ship at its own cadence while still sharing
the release identity format and class taxonomy.

---

## 2. Release Class Taxonomy

Five classes, scoped precisely. Every artifact in any family must carry exactly one.

| Class | Definition | Contains | Does NOT contain | Example |
|---|---|---|---|---|
| **core** | Primary user-facing artifact for a family | Main workflow, public promise, intake → output pipeline, upgrade hooks | Private weights, calibration internals, session-specific config | `hermes-agent` repo, `open-core-skill-architecture` SKILL.md |
| **support** | QA, guides, references, helpers that amplify a core | Boundary maps, release triage rubrics, safety schemas, public-lane routing | Standalone workflows that could be their own core | `release-versioning.md`, `open-core-boundary.md` |
| **bridge** | Migration, compatibility, redaction, or connector between families or versions | Upgrade scripts, schema migrations, lane routing configs, API adapters | New user-facing features | `public-lane-routing.md`, profile-to-topic connector |
| **fork** | Derivative variant of an existing core, targeting a different audience or constraint | Trimmed/rebranded core, domain-specific adaptation | Anything that diverges so far it can't trace lineage | `8d-pattern-awareness` forked from a broader scoring core |
| **ops** | Internal fleet/workflow utility not intended for public consumption | Cron-driven analytics syncs, talent-request processors, journal compliance checks | Anything a public end-user would invoke directly | `sibling-agent-fleet-analytics`, `sibling-agent-talent-request-processing` |

### Class decision rule

1. If it has its own user-facing promise → **core**.
2. If it documents, validates, or guides a core → **support**.
3. If it connects two versions, families, or surfaces → **bridge**.
4. If it adapts a core for a different audience → **fork**.
5. If it runs internally and no end-user invokes it → **ops**.

---

## 3. Current-Anchor Coherence Rule

**Rule:** Every candidate release is ranked against the *current stable core anchor*
for its family, not against the family's first version or a fixed V1.

### Mechanics

1. Each family has exactly one **active core anchor** at any time.
2. When a new core release ships, the anchor advances and all future
   support/bridge/fork/ops releases are scored against the new anchor.
3. Support releases that lag behind the anchor by more than one major version
   enter a **deprecation window** (flagged in release notes, not auto-removed).
4. The anchor version is recorded in the family's `ANCHOR` file at the repo root
   (or in the skill's `SKILL.md` frontmatter for skill families).

### Current anchors (as of 2026-05-31)

```
the operator agent Agent    — core — v1.0.0 — (initial public release pending)
OpenClaw Fleet  — ops  — v1.0.0 — (internal, not public-facing)
Skill Authoring — core — v1.0.1 — 2026-05-31
```

---

## 4. Release Identity Format

**Canonical format:**

```
[Family] — [Release Class] — v[SemVer] — [Release Date]
```

**Rules:**
- Family name is title-cased and matches the family map exactly.
- Release class is lowercase and matches the taxonomy exactly.
- SemVer follows strict `MAJOR.MINOR.PATCH`:
  - **MAJOR**: breaking workflow change, new public promise, or anchor advancement
  - **MINOR**: new capability within the existing promise
  - **PATCH**: fix, clarification, reference update, no behavior change
- Release date is ISO 8601 (`YYYY-MM-DD`).
- No "V1" shorthand. No unnamed drafts.

### Examples

```
the operator agent Agent    — core    — v1.0.0 — 2026-06-15
the operator agent Agent    — core    — v1.1.0 — 2026-07-01
the operator agent Agent    — support — v1.0.1 — 2026-06-20
the operator agent Agent    — bridge  — v1.0.0 — 2026-06-18
OpenClaw Fleet  — ops     — v1.1.0 — 2026-06-10
OpenClaw Fleet  — ops     — v1.0.1 — 2026-06-05
Skill Authoring — core    — v1.1.0 — 2026-06-08
Skill Authoring — support — v1.0.2 — 2026-06-03
```

---

## 5. Core vs Support vs Bridge vs Ops — Classification Guide

### What goes in `core`

- The main agent runtime (`run_agent.py`, `cli.py`, `model_tools.py`, `toolsets.py`)
- The gateway and platform adapters (`gateway/`, `gateway/platforms/`)
- The tool registry and built-in tools (`tools/`, `tools/registry.py`)
- The plugin loader and plugin interface (`plugins/` infrastructure, not every plugin)
- The skill loader and slash-command registry
- The profile system and session store
- Public-facing documentation and getting-started guides

### What goes in `support`

- Reference documents (boundary maps, release patterns, persona architecture)
- QA and validation scripts (`scripts/run_tests.sh`, `scripts/validate_soul.py`)
- Safety-guarded recommendation schemas
- Human-language taxonomy guides
- Release triage rubrics

### What goes in `bridge`

- Profile-to-platform routing connectors (`public-lane-routing.md` pattern)
- Schema migrations between major versions
- API adapter layers (ACP adapter, TUI gateway adapter)
- Upgrade/redaction scripts for moving from one core version to the next
- Cross-family connectors (e.g., a bridge that lets OpenClaw agents consume the operator agent skills)

### What goes in `ops`

- Fleet analytics sync engine (`sibling-agent-fleet-analytics`)
- Talent request processing pipelines (`sibling-agent-talent-request-processing`)
- Journal compliance monitoring
- Cron job health checks and error aggregation
- Daily pipeline skills (`health-scoring-daily-pipeline`, `daily-talent-management-review`)
- Internal scoring engines that never face end-users (`proprietary-twc-scoring`)

### What goes in `fork`

- Domain-specific adaptations of a core skill for a different audience
  (e.g., `8d-pattern-awareness` forked from a scoring core)
- Branded or trimmed variants of the agent for specific verticals
- Experimental branches that diverge from the main promise

---

## 6. Recommended Release Ladder

The release ladder defines the *sequence* of releases for each family.
Each rung is a concrete release with its class and estimated scope.

### the operator agent Agent Family

```
Rung 1 — v1.0.0 — core — Initial public release
  Scope: run_agent.py + cli.py + tools/ + gateway/ + plugin loader + profile system
  Open: MIT license, full source
  Moat: hosted inference, managed fleet, premium plugins (memory, observability)

Rung 2 — v1.0.1 — support — Developer reference pack
  Scope: AGENTS.md, boundary map, plugin authoring guide, platform adapter guide
  Depends on: core v1.0.0

Rung 3 — v1.0.0 — bridge — ACP + TUI connector pack
  Scope: acp_adapter/ + tui_gateway/ + ui-tui/ as installable extensions
  Depends on: core v1.0.0

Rung 4 — v1.1.0 — core — Plugin marketplace + skill registry
  Scope: Public skill registry, plugin install/uninstall, optional-skills promotion
  Anchor advances to v1.1.0
  Depends on: core v1.0.0

Rung 5 — v1.1.1 — support — Release triage + QA automation
  Scope: Automated release validation, compatibility matrix, triage checklist
  Depends on: core v1.1.0

Rung 6 — v2.0.0 — core — Multi-agent runtime
  Scope: Built-in subagent orchestration, shared tool budgets, inter-agent messaging
  Anchor advances to v2.0.0
  Depends on: core v1.1.0
```

### OpenClaw Fleet Family

```
Rung 1 — v1.0.0 — ops — Internal fleet sync
  Scope: fleet_analytics.py, talent-request processor, journal compliance
  NOT public — internal utility

Rung 2 — v1.0.1 — ops — Error classification + baseline tracking
  Scope: Error taxonomy, baseline error counts, automated alerting
  Depends on: ops v1.0.0

Rung 3 — v1.1.0 — ops — Agent spawning pipeline
  Scope: FORGE + ARBITER talent evaluation, spawn template, DB registration
  Depends on: ops v1.0.0

Rung 4 — v2.0.0 — core — Public fleet orchestration API
  Scope: REST API for fleet CRUD, agent lifecycle, public dashboard
  Anchor advances to v2.0.0
  Open: API spec + client SDK
  Moat: hosted fleet, proprietary TWC scoring, managed dispatching
```

### Skill Authoring Family

```
Rung 1 — v1.0.1 — core — Open-core skill architecture (SHIPPED)
  Scope: SKILL.md + all references/ + release identity format + class taxonomy
  Anchor: v1.0.1 (current)

Rung 2 — v1.0.2 — support — Release versioning compact spec
  Scope: Expanded versioning examples, deprecation window rules, ANCHOR file spec
  Depends on: core v1.0.1

Rung 3 — v1.1.0 — core — Safety-guarded recommendation engine pattern
  Scope: Public signal logic, confidence scoring, escalation routing, panel workflow
  Anchor advances to v1.1.0
  Moat: Private calibration weights, proprietary thresholds, hosted personalization

Rung 4 — v1.1.0 — support — Persona architecture guide
  Scope: Lens naming rules, panel composition guide, disallowed-language registry
  Depends on: core v1.1.0
```

---

## 7. Naming Convention

### Family names

Use the canonical family map. No abbreviations in release identity lines.

| Family | Short tag (for file/branch names) | Full name (for release identity) |
|---|---|---|
| the operator agent Agent | `hermes` | `the operator agent Agent` |
| OpenClaw Fleet | `sibling-agent` | `OpenClaw Fleet` |
| Skill Authoring | `skill-auth` | `Skill Authoring` |

### Artifact naming

```
<family-tag>-<class>-<short-description>-v<semver>
```

Examples:
```
hermes-core-agent-runtime-v1.0.0
hermes-support-dev-reference-v1.0.1
hermes-bridge-acp-tui-connector-v1.0.0
sibling-agent-ops-fleet-analytics-v1.0.0
skill-auth-core-open-core-architecture-v1.0.1
skill-auth-support-release-versioning-v1.0.2
```

### Branch naming

```
release/<family-tag>/<class>/<semver>
```

Examples:
```
release/hermes/core/1.0.0
release/sibling-agent/ops/1.0.0
release/skill-auth/core/1.1.0
```

### Tag naming

```
<family-tag>-<class>-v<semver>
```

Examples:
```
hermes-core-v1.0.0
sibling-agent-ops-v1.0.0
skill-auth-core-v1.1.0
```

---

## 8. Open-Core Boundary per Family

### the operator agent Agent

**Open (core):**
- Agent runtime, tool orchestration, CLI, gateway, platform adapters
- Plugin interface and plugin discovery mechanism
- Profile system, session store, skill loader
- Built-in skills and optional-skills catalog
- Test suite, build scripts, development guide

**Moat (premium):**
- Hosted inference routing and credential pooling
- Managed fleet orchestration (OpenClaw as a service)
- Premium memory plugins (longitudinal synthesis, cross-session recall)
- Proprietary observability and achievement plugins
- Advanced dashboard and TWC scoring

### OpenClaw Fleet

**Open (when public core ships):**
- Agent lifecycle API spec and client SDK
- Fleet health dashboard schema
- Public agent profile format
- Journal compliance specification

**Moat (stays private):**
- TWC scoring engine and proprietary weights
- Internal spawning heuristics and FORGE/ARBITER decision logic
- Fleet analytics sync internals
- Error classification engine and baseline tracking

### Skill Authoring

**Open (core):**
- Skill architecture pattern, release classes, versioning scheme
- Boundary map, safety-guarded recommendation schema
- Persona architecture (public roles only)
- Release triage checklist

**Moat (premium):**
- Domain-specific calibration packs (health, finance, wellbeing)
- Hosted skill marketplace curation and ranking
- Automated skill quality scoring internals
- Premium bridge packs for regulated domains

---

## 9. Release Discipline Rules

1. **No orphan releases.** Every release belongs to exactly one family and carries exactly one class.
2. **No floating anchors.** The current stable core anchor is recorded explicitly and updated when a new core ships.
3. **No unnamed drafts.** Use the full release identity format, even for internal ops releases.
4. **No cross-family dependencies without a bridge.** If OpenClaw needs a the operator agent artifact, ship a bridge release that makes the dependency explicit.
5. **No moat leakage.** Run the competitor test before every core release: could a competitor reproduce the premium system from the public layer alone? If yes, the boundary is too thin.
6. **No fixed-V1 comparisons.** Always compare candidates against the current anchor, not the family's first release.
7. **Deprecation windows, not silent removals.** When a support release lags the anchor by more than one major version, flag it. Don't delete it silently.

---

## 10. Summary

- **3 families**: the operator agent Agent, OpenClaw Fleet, Skill Authoring
- **5 release classes**: core, support, bridge, fork, ops — each with a precise definition and decision rule
- **Current anchors**: the operator agent Agent `v1.0.0` (pending), OpenClaw Fleet `v1.0.0` (internal), Skill Authoring `v1.0.1` (shipped)
- **Release identity**: `[Family] — [Release Class] — v[SemVer] — [Release Date]`
- **Open-core boundary**: public layer is genuinely useful; premium layer is clearly better, not just larger
- **Naming convention**: `<family-tag>-<class>-<description>-v<semver>` for artifacts, `release/<family>/<class>/<semver>` for branches
- **Release ladder**: 6 rungs for the operator agent Agent, 4 for OpenClaw Fleet, 4 for Skill Authoring — each with explicit scope and dependency
