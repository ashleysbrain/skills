---
name: marketing-metabolism-production
description: >-
  Operate the the operator agent organism's marketing metabolism: content production,
  distribution, feedback, and product DNA injection. Uses body-part analogs.
version: 1.0.0
author: the operator agent Agent
license: MIT
metadata:
  hermes.tags:
    - marketing
    - the operator agent
    - organism
    - creative-production
    - body-analogs
  hermes.category: operations
  hermes.related_skills:
    - the operator agent-creative-production-spine
    - ds-genome-transcription
    - social-content-pipeline
    - verdent-pm-discipline
---

# Marketing Metabolism Production Skill

Operate the the operator agent organism's **Expressive Phenotype** — the marketing
metabolism that produces branded content, distributes it across platforms,
collects feedback, and injects marketing DNA into products produced by the operator agent.

Full architecture: `docs/MARKETING-METABOLISM-ARCHITECTURE.md`

## When to Use

- Producing marketing content batches (social posts, newsletters, decks)
- Operating the marketing cron ecosystem (daily/weekly/monthly rhythms)
- Reviewing brand genome integrity (BAP/MAP panels)
- Injecting marketing DNA when a product births from the operator agent
- Monitoring distribution organ health and engagement feedback
- Detecting critical slowing down in marketing performance

## Prerequisites

- Creative Faculty engines alive: Goethe (:port), Wernicke (:port),
  Bell (:port), Luria (:port), Da Vinci (:port), Tawara (:port)
- Wave engine alive: :port (for panel orchestration + resonance)
- Harvey alive: :port (for content circulation routing)
- BAP + MAP panel configs present in workspace

## The Process Flow (8-Stage Flow)

NOTE: This was previously called "The Production Spine (8-Stage Flow)" — that
name was corrected on 2026-06-29. The spine (vertebral column) is a real
anatomical structure; using it as a metaphor for a pipeline violates the
structural isomorphism principle. Use "process flow" instead.

1. **BAP** (Wave) — Set brand homeostasis, define the zag
2. **Genesis** (Wernicke → Goethe → Tawara → Da Vinci) — Produce content molecules
3. **Rendering** (Bell → Luria) — Multi-format render + quality gate
4. **Circulation** (Harvey) — Route to distribution organs via MAP prescription
5. **Distribution** (Gershon routing → Heidenhain exocrine secretion) — Platform delivery
6. **Feedback** (Helmholtz) — Sense audience response, normalize signals
7. **Learning** (Burnet/Hippocampus) — Convert feedback to hypotheses
8. **Protection** (Allostasis/BBB) — IP protection + brand integrity

## Physics Checklist (Every Production Run)

- [ ] **Superposition:** Held 2-3 creative directions before collapsing at quality gate
- [ ] **Entanglement:** Brand genome contract propagated to all organs simultaneously
- [ ] **Free Energy:** F = cost - T*info_gain ≤ 0 for each content piece
- [ ] **Critical Slowing Down:** Checked recovery time + variance trends before push
- [ ] **Adiabatic:** No mid-cycle brand identity shifts (except crisis wound-healing)

## Body-Part Analog Quick Reference

| Marketing Function | Body Analog | Engine |
|---|---|---|
| Brand voice | Broca's area | the specialist engine (8124) |
| Visual narrative | Visual cortex | the specialist engine (8120) |
| Creative rhythm | Cardiac conduction | the specialist engine (8128) |
| Design production | Somatomotor cortex | the specialist engine (8116) |
| Multi-format render | Motor cortex | the specialist engine (8121) |
| Quality gate | Cerebellum | the specialist engine (8122) |
| Content routing | Circulatory system | the specialist engine (8092) |
| Distribution routing | Enteric nervous system | the specialist engine (8144) — routing control (WHEN, HOW FAST, WHICH platform) |
| Content Distribution | Exocrine gland (epithelial secretion) | the specialist engine (8145) — platform adaptation + secretion via ductal modes |
| Audience feedback | Somatosensory cortex | the specialist engine (8107) |
| Marketing memory | Immune memory | the specialist engine (8100) |
| Brand defense | Immune system | the specialist engine (8091) |

## Product DNA Injection (When a Product Is Output)

When the specialist engine (8090) produces a product from the operator agent:

1. Copy the 6 marketing chromosomes (voice, visual, positioning, platform, coupling, IP)
2. Apply epigenetic markers based on product type
3. Set mutation rates (voice=0.01, visual=0.02, positioning=0.05, platform=0.15, coupling=0.20, IP=0.00)
4. Initialize content metabolism (first content molecules produced)
5. Activate platform adaptation genes (which distribution organs develop)

## Extended Phenotype Mapping

Marketing organs are **extended phenotype** structures — biological
communication/display mechanisms that extend beyond the 11 standard Gray's
anatomy systems. The user explicitly endorsed this (2026-06-26): analogs
that map to real biology even for functions outside standard anatomy.

See `references/extended-phenotype-mapping.md` for the full methodology,
including four biological analog patterns (spider web, birdsong, peacock
tail, pheromone trail) and the reconciliation rule between internal organs
and extended phenotype.

The parent methodology is the `body-part-tackle-workflow` skill.

## Port Assignment Pitfall

When registering new marketing engines in the ECS registry, ALWAYS check
existing port assignments first. During this skill's creation (2026-06-26),
ports 8125-8130 were initially assigned to the 5 distribution organs but
collided with existing creative engines (MacLean:port, Ito:port,
Gazzaniga:port, Tawara:port). Fixed to 8140-8144.

Verification command:
```bash
python3 -c "
import yaml
with open('ds-engine-registry/REGISTRY.yaml') as f:
    data = yaml.safe_load(f)
all_ports = [e['port'] for e in data.get('engines', []) if 'port' in e]
from collections import Counter
dupes = {p: c for p, c in Counter(all_ports).items() if c > 1}
print('CONFLICTS:', dupes if dupes else 'none')
"
```

## Synergy with Opencode

- the operator agent: operates crons, produces content, collects feedback, injects DNA
- Opencode: builds distribution organ engines, writes process flow code, refines physics
- Handoff: the operator agent writes spec → Opencode builds engine → the operator agent operates it

## Related Skills

- `marketing-consortium-blueprint` — The generalizable blueprint for creating
  agent consortiums for ANY domain (not just marketing). Covers selection math,
  decision sequence, pathology system, engine /process endpoint contract.
  While THIS skill covers the organs themselves, that skill covers what drives
  tasks THROUGH the organs and how to replicate the pattern for new domains.
- `the operator agent-creative-production-spine` — NOTE: this skill name contains "spine"
  which is an anatomical misnomer (per 2026-06-29 correction). Flagged for
  curator consolidation.

## The Marketing Consortium (Ephemeral Task Swarm)

A **Consortium** is a task-swarmed collective of specialist agents that forms
per marketing idea and disbands on artifact output. Biological isomorphism:
**microbial consortium** (different specialists in symbiotic metabolism of
one substrate — each species performs a different metabolic stage, output of
one feeds the next).

**Naming convention (locked 2026-06-29):** Consortium = ephemeral task swarm
(forms per idea, disbands on birth). Consilium = permanent operator brain-suite
(you boot wearing it every session). Different lifecycle, different purpose.

The Consortium Carriage Controller (`src/consortium_carriage.py`) is the\n**motor planning pathway** that sequences organs into one executable pipeline.\nBiological isomorphism: **premotor cortex → motor cortex → corticospinal tract**.\nIt PLANS and SEQUENCES motor actions. It is NOT the cardiac conduction system\n(that is the specialist engine :port). Corrected 2026-06-29 after isomorphism audit caught\nthe identity theft — software was claiming to be a biological pacemaker.

See `references/consortium-selection-math.md` for the deterministic selection
engine that agents use to choose marketing philosophies — NOT heuristics but
actual math (8D human wellness gate + DNA alignment + free energy ratio gate).

See `references/quantitative-marketing-math.md` for the 44 quantitative formulas
(measurement, prediction, valuation) that drive agent thresholds — Bass diffusion,
prospect theory, Thompson sampling, ROMI, Shapley attribution, LTV:CAC, and more.

## The 8D HUMAN Wellness Gate (Critical Definition)

When screening marketing philosophies, strategies, or content for wellness
alignment, the gate measures **HUMAN consumer wellness** — what the marketing
content DOES TO THE HUMAN who consumes it. NOT whether it's healthy for the
AI to produce. NOT system health. The question is: does this marketing
approach harm or support the HUMAN consumer across all 8 dimensions?

**ALL EIGHT dimensions are protected (Hippocratic oath, corrected 2026-06-29):**
Physical, Psychological, Intellectual, Social, Spiritual, Vocational, Financial,
Environmental. Any marketing philosophy scoring negative on ANY dimension =
automatic REJECT. No hierarchy of harm. Every dimension called out individually.

| Dimension | Protected Against |
|-----------|-------------------|
| Physical | Harm to human bodies (health, sleep, movement, nutrition) |
| Psychological | Harm to human minds (manipulation, anxiety, exploitation) |
| Intellectual | Harm to human intellects (misinformation, dumbing down, confusion) |
| Social | Harm to human connections (division, loneliness exploitation, outrage) |
| Spiritual | Harm to human spirits (cynical co-opting of meaning, fake guru) |
| Vocational | Harm to human work (undermining professional integrity, exploitation) |
| Financial | Harm to human finances (predatory pricing, deceptive billing) |
| Environmental | Harm to human environments (wasteful consumption, destruction) |

The mission: heal humanity across all 8 dimensions. Use POSITIVE healing language only.

User correction (2026-06-29): "Is it wellness for AI or is this wellness for
humans? Because there's a very big difference here when we're considering
marketing content." Followed by: "make sure all eight dimensions are protected.
Call them out individually."

## Selection Math (Agents Need MATH Not Heuristics)

User correction (2026-06-29): "There's got to be some sort of a math behind
their decision making... it's not just based on legistics."

The selection function is DNA-encoded. Every spin-out inherits it:

```
Score(P, T) = 0.30·DNA(P) + 0.25·EIGHT_D(P) + 0.20·FIT(P,T)
              + 0.15·EVIDENCE(P) + 0.10·CONTRARIAN(P)
```

Hard gates: 8D < 0 -> REJECT. DNA < 0.5 -> REJECT. Protected dimension
harmed -> REJECT. Free energy ratio F = COST / [Score * (1 + INFO_GAIN)] >= 1.0
-> SKIP.

See `references/consortium-selection-math.md` for the full math spec.
See `src/selection_engine.py` for the executable engine.

## Consortium System (Autonomous Carriage Layer)

Above the marketing metabolism sits the **consortium carriage** — an autonomous
controller that drives a marketing idea through the organism from intake to output.
The marketing consortium is the FIRST instance of a generalizable blueprint
that works for any domain (health, legal, education, etc.).

Full system at `~/your-workspace/marketing-consortium/`:
- **Curriculum** (03): 14 modules, 3-layer architecture (knowledge + process + audit)
- **Selection math** (05 + src/selection_engine.py): deterministic scoring with
  8D human wellness gate (ALL 8 dimensions protected), DS DNA alignment, free
  energy gate, superposition (top 3 candidates held)
- **Decision sequence** (07): 9-phase formula ordering — agents know WHICH formula
  runs WHEN (selection before content exists, measurement after)
- **Pathology system** (04): 6 pathology types for reporting missing/broken body parts
- **Blueprint** (08): generalizable template for creating consortiums in any domain
- **Endpoint contract** (09): /process spec for sibling-agent to wire engines

Key rules learned during build (2026-06-29):
- It is a PROCESS FLOW, not a "spine". Never use anatomical terms as metaphors.
- It is OUTPUT, not "birth". Not every artifact is birthed.
- ALL 8 dimensions of HUMAN consumer wellness are protected. No exceptions.
- Build the system COMPLETELY before testing. Do not ask for test ideas until
  engines are wired and organs are built.
- The 8D gate measures HUMAN consumer wellness (what the marketing DOES TO the
  human who sees it), NOT whether it is healthy for the AI to produce.
- The goal is to heal humanity across all 8 dimensions. Positive framing only.

See `references/consortium-carriage-system.md` for full architecture details.

## Pitfalls

- **Never high-drive a low-energy audience** (impedance mismatch = wasted energy)
- **Never skip the quality gate** (Luria checks brand genome compliance)
- **Never distribute without MAP prescription** (wrong platform = wrong dosage)
- **Never change brand identity mid-cycle** (adiabatic violation = chaos)
- **Never let r_brand drop below 0.8** (brand incoherence = audience confusion)
- **Never expose coupling coefficients externally** (IP violation = BBB breach)
- **Never use anatomical terms as metaphors for processes** — "spine" means the vertebral column, "birth" means reproductive output. Use "process flow" and "output" unless referencing the actual anatomy. This is a structural isomorphism, not a metaphor system.
- **Never protect fewer than ALL 8 dimensions** — every dimension is protected. No hierarchy of harm. Any negative score on ANY dimension = automatic REJECT.
- **Never test before the system is fully built** — build completely (engines wired, organs built, endpoints connected), THEN test. Asking for test ideas before the build is complete is a physics violation (adiabatic).
- **Never use heuristics when MATH exists** — agent decisions need deterministic
  scoring (selection engine), not vibes. User is physics-informed and demands
  real quantitative frameworks (conjoint analysis, Bass model, prospect theory,
  etc.) behind every threshold decision.
- **Never confuse 8D human wellness with system health** — the 8D gate in
  marketing measures what content does TO THE HUMAN consumer, not whether the
  AI system is healthy.
- **Never test before building completely (2026-06-29 correction).** "You
  haven't even built and connected the engines yet... you need to build it all
  the way before that." Build every layer completely, connect everything
  end-to-end, THEN test. Pushing for a test run while engines are unwired and
  body parts are missing is an adiabatic violation.
- **Never put project state in the 2,200-char the operator agent memory buffer (2026-06-29
  correction).** Project state lives in files, git, and the operator bus. The
  memory buffer holds ONLY: user identity, communication style, standing rules,
  current priority. "It's a process flow, I don't know why that needs to go to
  memory." Destructive memory deletes to make room for project state are
  FORBIDDEN — route to DS O'Keefe (T2) or files instead.
- **Never force the number of framework categories to match the 8D dimensions
  (2026-06-29 correction).** "I feel like there's going to be more [than 8].
  Are you trying to fit only eight because I have eight dimensions?" Let
  research surface whatever number of categories naturally emerges.
