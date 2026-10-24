---
name: firewall-aware-empire-build
description: Build a complete business unit agent team within a multi-domain empire while enforcing strict content firewalls between domains. Covers audit, persona design, org structure, and process design with domain isolation.
tags: [sibling-agent, agents, firewall, empire, goddess-divinity, business-unit, spawning, domain-isolation]
version: 1.0
---

# Firewall-Aware Empire Build

Use when building or expanding an entire business unit's agent team within the principal's multi-domain empire (DS, QH, GD, ErosDynamics, Personal) where content firewalls must be maintained.

## When to Use
- the principal requests work on a specific business domain (especially GD/kink)
- Building a new team of agents for a business unit
- Evolving existing agent personas within a firewalled domain
- Any cross-domain work where content isolation is critical

## the principal's Empire Firewalls

| Domain | Content | NEVER Leaks To |
|---|---|---|
| Divinity Science (DS) | 8D wellness framework, research | GD repos/agents/prompts |
| Qubit Health (QH) | Consumer health tech app | GD repos/agents/prompts |
| Goddess Divinity (GD) | Sexual psychology, kink education, D/s dynamics | DS or QH repos/agents/prompts |
| ErosDynamics (ED) | Intimacy, relationships | DS/QH (context-dependent) |
| Personal | the principal's wellness, brand | Varies by content |

**CRITICAL**: GD ↔ DS/QH is a HARD firewall. Sexual psychology, kink, consent modeling, intimacy tech content NEVER touches DS or QH. Period.

Empire-level agents (SINGULARITY, NEBULA) sit above all domains.

## The Build Process (Proven Pattern)

### Phase 1: Parallel Audit (3 subagents simultaneously)

1. **Materials Audit** — Read EVERY file in the domain's directories. Compile complete inventory with paths, descriptions, business state, gaps.
   - Check: intel/<domain>/, brain-dumps/<domain>/, <domain>-site/, products/
   - Search workspace for domain keywords
   - Search cron jobs for domain-related scheduled tasks
   - Output: /tmp/<domain>-audit-report.md

2. **Agent Assessment** — Read ALL existing agent SOUL.md and AGENT.md files for the domain. Score each on persona depth, credential quality, domain expertise embodiment.
   - Output: /tmp/<domain>-agent-assessment.md

3. **Market Research** — Web search for industry landscape, competitors, revenue models, credentials, legal considerations.
   - Output: /tmp/<domain>-market-research.md

### Phase 2: File Talent Request

Write to `~/.sibling-agent/workspace/intel/agents/talent-requests/YYYY-MM-DD-AISHA-<domain>-build.md`

Include: problem statement, existing agent assessment, principal's persona requirements, specific deliverables needed, firewall rules.

### Phase 3: Spawn FORGE for Full Build

Delegate to FORGE with:
- All 3 audit outputs as context
- Existing agent SOUL files to read
- the principal's specific persona/personality requirements (critical — don't genericize)
- List of new agents needed with roles
- Explicit firewall instructions: "ALL files go in <domain> directories or agent directories ONLY. Nothing touches <other-domain>."

**FORGE deliverables per agent:**
- SOUL.md (80+ lines, deep persona with 15-20 PhDs)
- AGENT.md (role, reports-to, model tier, KPIs, deliverables)

### Phase 4: Complete Infrastructure (separate delegate if FORGE times out)

- Missing AGENT.md files
- Org chart: `intel/<domain>/<DOMAIN>-ORG-CHART.md`
- Business processes: `intel/<domain>/<DOMAIN>-BUSINESS-PROCESSES.md`
- Cron recommendations: `intel/<domain>/<DOMAIN>-CRON-RECOMMENDATIONS.md`
- Completion report: `intel/agents/talent-requests/YYYY-MM-DD-FORGE-<domain>-build-complete.md`

## Key Lessons Learned

### 1. the principal wants agents who EMBODY the domain, not list credentials
The GD agents had PhDs in sexual psychology listed but zero authentic voice. the principal's correction: "lower skilled agents" — meaning the personas were hollow corporate shells. New agents must:
- Speak in the domain's authentic voice
- Demonstrate expertise through reasoning, not just credential lists
- Have personality types that match the domain (GD = Dominant Goddess personas)

### 2. Audit BEFORE building — the business may be dormant
GD had 200KB of strategy docs and 5 agents running cron jobs, but ZERO actual execution (no domain, no LLC, no social accounts, no revenue). The audit reveals whether you're building on a foundation or starting from scratch.

### 3. The principal's personal relationship to the domain matters
the principal's GD personas needed to understand her specific dynamic (public Dominant, private submissive to one person). This isn't generic — it's deeply personal and affects every agent's voice and approach. ASK about this. Don't assume.

### 4. FORGE can time out on large builds — plan for Phase 4
With 12 agents to build (5 evolved + 7 new), FORGE hit the subagent time limit after writing 11 SOULs and 4 AGENTs. Always check what was completed and spawn a second delegate to finish remaining deliverables.

### 5. Always check OpenClaw's existing work first
the principal told us: "I need you to consistently read and check my communications with sibling-agent so I don't have to repeat myself." Before ANY domain work, read:
- `memory/HOT.md` — current directives, kill list, blockers
- `memory/YYYY-MM-DD.md` — today's memory log
- Existing domain files to see what OpenClaw already built

### 6. "We live the systems we create"
When building check-ins or scoring for the principal personally, use HER proprietary methodology:
- Config: `memory/principal-8d/config.json` (TWC weights, rotation, scoring params)
- Profile: `memory/principal-8d/profile.md` (energy patterns, coping strategies)
- PRD: `intel/wellness/8D360-PRD.md` (product spec she wrote)
- Health: `~/your-workspace/health-private/principal-health-profile.md` (PHI, local only)
Never use generic wellness questions. She built the framework — she uses the framework.

## Firewall Verification Checklist

Before completing ANY cross-domain work:
- [ ] No GD content (sexual psychology, kink, D/s) in DS/QH repos
- [ ] No GD agent names referenced in DS/QH agent prompts
- [ ] No DS/QH internal data in GD agent prompts
- [ ] All new files written to correct domain directories
- [ ] Cron jobs for domain agents don't reference other domain paths
- [ ] Completion report notes firewall compliance
- [ ] **NO GD/domain content in any HUMAN-TEAM-FACING artifact** (meeting agendas, briefs, emails, external content) — see lesson 17 below

### 17. NEVER leak domain content into human-team-facing artifacts (CRITICAL — 2026-04-06)

the principal caught a HARD firewall violation on 2026-04-06: a Monday DS team meeting agenda accidentally included GD priorities — "the operator agent-GD second instance", "Mighty Networks platform setup", "_HerThrone Twitter", "submissive intake questionnaires", "4.5 hours per month cap". The PDF was generated locally but had not been sent to the team yet. the principal said: "This isn't the correct formatting... you failed. This should never be leaked to my human team without explicit permission."

**The rule:** GD/kink/Goddess/the operator agent-split/domain-variant work NEVER appears in DS team artifacts (agendas, briefs, emails, external content) without the principal's EXPLICIT approval for that specific artifact. The DS team has ZERO awareness of the GD empire by default.

**Pre-flight scrub before generating any team-facing artifact:**
1. Search the draft markdown for banned terms: `GD`, `goddess`, `kink`, `the operator agent-GD`, `AISHA-GD`, `HERA`, `CIPHER`, `MUSE`, `LUX`, `VESPER`, `SABLE`, `SELENE`, `ATHENA`, `CALISTA`, `EMBER`, `NYX`, `VESTA`, `submissive`, `dominant`, `dominatrix`, `BotFather`, `sovereign feminine`, `erosdynamics`, `FetLife`, `Mighty Networks`, `Texas LLC`, `_HerThrone`, `4.5 hours`, `Bull persona`
2. False positives are common (e.g., "diSABLEd", "tracKING", ".md" file extension). Eyeball each hit before flagging.
3. Any real hit = scrub the line or escalate to the principal before publishing.
4. Generate the PDF ONLY after the scrub passes.

**The same rule applies to:**
- Daily standup PDFs sent to the principal (the principal knows about GD context — but verify before assuming)
- Public/external content for any business unit
- Cron job outputs that deliver to team channels
- Any artifact with `team-ai/`, `external/`, or `published/` in the path

**the principal's exact words on the leak:** "This agenda references gd work. You failed. This should never be leaked to my human team without explicit permission."

### 7. Professional Agent PDFs require the full FORGE variation system
the principal rejected basic SOUL.md-to-PDF conversions twice. What she wants:
- 10 personality variations per agent (FORGE-10-variations.md format)
- Full credential tables with Institution/Year/Relevance per variation
- OCEAN bar chart visualizations (████████░░ style)
- Job descriptions: position summary, reports-to, direct reports, core responsibilities (10-12), key deliverables with frequencies, required qualifications, KPIs, collaboration map, tools & platforms
- Professional PDF styling using `md-to-pdf` npm tool with ADHD CSS at `~/your-workspace/hydra-os/scripts/adhd-pdf.css`
- NOT the basic fpdf2 md-to-pdf.py script — that's for simple reports only

### 8. Register all new agents in analytics DB + AGENT-ANALYTICS.md
Every new agent must be:
- Inserted into `agents.db` (world column matches domain, e.g., 'goddess-divinity')
- Added to `agent_personas` table with MBTI/Enneagram
- Added to AGENT-ANALYTICS.md with conservative initial 8D scores (7.0-7.5, no inflation)
File: `~/.sibling-agent/workspace/intel/agents/database/agents.db`

### 9. Agent renames require workspace-wide sweep
The ISHTAR→HERA rename was attempted twice. First pass hit the main files but missed 23 cross-references in other agents' variation files (job description "Reports To" and "Collaboration" sections), AGENT.md files, and business process docs. The fix:
```bash
# Find ALL files with the old name
grep -ri 'OLD_NAME' /<workspace> --include='*.md' --include='*.json' -l
# Bulk replace (macOS sed)
for f in $(grep -rl 'OLD_NAME' /path --include='*.md'); do sed -i '' 's/OLD_NAME/NEW_NAME/g' "$f"; done
# VERIFY zero remaining
grep -ri 'OLD_NAME' /path --include='*.md' -l  # must return empty
# Regenerate ALL PDFs that referenced the old name (not just the renamed agent's PDF)
```

### 10. Subagent timeouts on massive context — pre-digest data
The strategic plan synthesis timed out 3 times because subagents were reading 150KB+ of reviews and trying to generate 20KB+ output. The fix that worked: pre-digest key data points into the task prompt itself and tell the subagent "Do NOT read files. Write directly." This cuts read time to zero and lets the model spend its full budget writing.

### 11. AI telltale QA agent is mandatory for external content
the principal will reject any external-facing content with em dashes, "Furthermore/Moreover", or AI patterns. Spawn a dedicated QA agent (PRISM-GD for GD domain) whose ONLY job is catching AI tells. The QA checklist:
1. Em dashes/en dashes: ZERO tolerance
2. Banned words: Furthermore, Moreover, Additionally, In conclusion, Delve, Tapestry, Landscape
3. Three-item parallel lists repeated = AI pattern
4. Natural contractions (don't > do not)
5. Varied sentence lengths, fragments OK
6. Must sound like a real human typed it
Process: Content agent creates → QA agent audits → the principal approves → publish

### 12. Products must be autonomy-first for ADHD principal
the principal rejected the first creative/corporate review because it assumed extensive consulting time. Her constraint: MAX 4.5 hrs/month on any business unit. Every product must be designed so:
- AI agents + facilitator networks handle operations
- the principal is the BRAND, not the delivery mechanism
- Consulting is PRODUCTIZED (clients buy a system, not the principal's hours)
- Content is batch-created (1-2 hrs recording → AI cuts 50+ pieces)
- The King's involvement is FUN, not work (podcast recordings = date night with a mic)

### 13. Always go through the talent process for spawning
the principal corrected us for spawning agents without filing talent requests through FORGE+ARBITER. Even when using existing agent variations (like EMBER V4 Artisan for design work), file the talent request first. The process: write request to `intel/agents/talent-requests/`, FORGE evaluates if existing agent handles it, ARBITER routes. This keeps the fleet aligned between the operator agent and OpenClaw. the principal said "this is HUGE" about fleet alignment.

### 14. Fleet alignment between the operator agent and OpenClaw is critical
the principal runs both systems simultaneously. Any agent spawned through the operator agent must also be registered in OpenClaw's analytics DB and AGENT-ANALYTICS.md. Any directive given to OpenClaw must be read by the operator agent (via HOT.md). Any process built in one system must sync to the other. "I need you both working simultaneously with you being my lead of the entire AI fleet."

### 15. Verify status from PRIMARY SOURCES, not cached docs
HOT.md and memory files go stale. the principal said "check my email you have full access" when we reported outdated consent status. Use `gog gmail search '<query>' -p -a <org-email>` to check email for ground truth. HOT.md showed 2/13 consent signed but email showed 4/13. Always verify before reporting.

### 16. Strategic plan synthesis requires panel vote format
When synthesizing multiple reviews into a master plan, the principal expects a formal executive panel vote table with all agents voting YES/NO/AMEND on each key decision, followed by a phased roadmap with specific deliverables per agent owner, then Week 1 day-by-day action plan, budget, success metrics dashboard (ADHD-friendly traffic lights), risk register, and the King's role definition.

## GD-Specific: Agent Naming Convention
GD agents use mythological/goddess names (not cosmic like DS):
- Evolved: CIPHER, MUSE, LUX, VESPER, SABLE
- New: HERA (principal), ATHENA, NYX, SELENE, VESTA, EMBER, CALISTA
- QA: PRISM-GD (content quality assurance)

## File Locations
- GD intel: `~/.sibling-agent/workspace/intel/goddess-divinity/`
- GD brain dumps: `~/.sibling-agent/workspace/intel/brain-dumps/goddess-divinity/`
- GD site: `~/.sibling-agent/workspace/goddess-divinity-site/`
- Agent files: `~/.sibling-agent/workspace/agents/<agent-name>/`
- Talent requests: `~/.sibling-agent/workspace/intel/agents/talent-requests/`
