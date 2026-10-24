# B2B Organism — Body Systems → Business Function Mapping

**Purpose:** The canonical translation layer from biological body systems to B2B organism business functions. Load this whenever mapping a body system to a business/organism role, auditing per-system B2B coverage, or deciding what to build next for B2B organisms.

**Source:** Grounded in `ecs.py` FLEET_REGISTRY (76 engines), `organism-redesign/PHYSIOLOGY-COMPLETE-BODY-SYSTEMS.md`, `docs/reproductive-system/B2B-ORGANISM-CONFIG.md`, and the organism-biological-isomorphism-verification rules (esp. Rule 16: B2B↔B2C is *mycorrhizal*, not anatomical).
**Established:** August 11, 2026.

---

## The 6 Core Systems → B2B Business Function

| # | Body System | B2B Business Function | One-line meaning |
|---|---|---|---|
| 1 | Nervous | **Decision / Routing** | Task intake, prioritization, routing to specialists, scheduling, go/no-go gates |
| 2 | Cardiovascular | **Financial Flow** | Revenue circulation, budget perfusion to units, cash-pressure regulation, payment uptime |
| 3 | Respiratory | **External Communications** | Marketing outbreath (content/brand), sales/intake inbreath (leads/signals), PR, market voice |
| 4 | Digestive | **Customer Intake & Product Delivery** | Onboarding (ingestion), requirements breakdown (digestion), value absorption, product delivery |
| 5 | Urinary | **Waste / Cleanup** | Dead processes, stale data, failed experiments, tech debt, cost cleanup, the "what to kill" function |
| 6 | Endocrine | **Culture / Motivation** | Slow org-wide broadcast: tone, values, drive, urgency — the hormonal background modulating every engine |

## Per-System: Engines, Gaps, Business Document

### 1. Nervous → Decision / Routing
- **Existing engines (body_system=`nervous`, 45 engines):** the specialist engine (:port, timing root/master clock), the specialist engine/Wave (:port, cadence/sync), the specialist engine/Allostasis (:port, SLA/KPI setpoints + deviation detection), the specialist engine (routing/failover, RAS dynamic routing), the specialist engine/the specialist engine (decision thresholds/go-no-go gates), the specialist engine (cellular-respiration task prioritization: rapid/core/deep tiers), the specialist engine (6 flows — routing protocol reference), the specialist engine/MacLean/Carlsson (prefrontal decision + dopaminergic reward).
- **Missing:** External business-request → engine dispatch loop (Krebs models engine-internal tasks, not external business requests); cranial-nerve analog for inbound channel routing (Rule 35 mandates this methodology); arcuate fasciculus wiring verification (Rule 36 — check engines are *wired*, not just registered); RAS root-cause discipline (Rule 23 — fix the fingerprint/receptor root, don't just reroute).
- **Business document produced:** Daily Task Routing Manifest (Krebs-tiered dispatch list with allostatic setpoint status); Decision Threshold Policy (go/no-go criteria for auto vs human-approval actions).

### 2. Cardiovascular → Financial Flow
- **Existing engines (body_system=`cardiovascular`, 2 engines):** the specialist engine (:port, perfusion modeling, V/Q matching), the specialist engine/the specialist engine (cardiac conduction = 3-tier failover: SA=the operator agent/AV=sibling-agent/Purkinje=sibling-agent via overdrive suppression). Cross-system: the specialist engine (urinary) couples via RAAS for pressure/volume = liquidity regulation.
- **Missing:** B2B revenue-perfusion model (Harvey models physiological perfusion, not budget/revenue flow to business units — no `business_perfusion` process flow registered); payment-processing throughput/fee/chargeback engine; financial RAAS coupling (Bright↔Harvey business liquidity axis); Haldane coupling for "oxygenated" vs "deoxygenated" capital (recurring vs one-time revenue).
- **Business document produced:** Cash Flow Perfusion Report (funded vs ischemic departments, liquidity pressure status); Financial Heartbeat/Conduction SLA (3-tier billing/payment failover guarantee).

### 3. Respiratory → External Communications
- **Existing engines (body_system=`respiratory`, 1 engine):** the specialist engine (:port, gas exchange, V/Q matching). Cross-system: the specialist engine/the specialist engine (sensory intake = environmental signal), the specialist engine/the specialist engine mode (:port, content generation = exhalation), the specialist engine (publishing = distribution channel).
- **Missing:** B2B comms exchange flow (inbound market signal ↔ outbound message gas-exchange model not registered); brand-voice "oxygenation" quality-loading model (O₂-Hb dissociation analog for brand-consistency of outbound content); respiratory-rate ↔ market-cadence coupling; pH/Henderson-Hasselbalch business analog (fast market-sentiment correction / PR crisis response); V/Q matching for channel efficiency (content produced vs audience reached).
- **Business document produced:** Communications Exchange Cadence (intake rate, emission rate, channel V/Q efficiency, market-sentiment "blood gas" reading); Brand-Oxygenation Report (per-message saturation curve before emission).

### 4. Digestive → Customer Intake & Product Delivery
- **Existing engines (body_system=`digestive`, 1 engine):** the specialist engine (:port, digestive modeling, gut-brain axis). Cross-system: the specialist engine (:port, reproductive/product birth = downstream of digestion), the specialist engine/the specialist engine (product delivery), the specialist engine/bone-marrow (customer-specific model training per B2B-ORGANISM-CONFIG §8).
- **Missing:** Customer-onboarding ingestion flow (Beaumont exists but B2B intake → requirements breakdown → delivery pipeline is not a registered digestive process flow; gut-brain axis Beaumont↔Wave is a top-5 missing cross-system interaction per PHYSIOLOGY doc §6); product-delivery absorption model (how much value the customer absorbs vs "excretes"/churns — adoption efficiency); B2B-specific onboarding consuming the 12 registration fields from B2B-ORGANISM-CONFIG; bone-marrow training intake wired to Beaumont.
- **Business document produced:** Customer Intake & Onboarding Pipeline (ingestion→breakdown→absorption→delivery stages with adoption/absorption metric); Product Delivery Manifest (what was digested from customer, what nutrient/product delivered back).

### 5. Urinary → Waste / Cleanup
- **Existing engines (body_system=`urinary`, 1 engine):** the specialist engine (:port, filtration/excretion, slow pH control, RAAS). Cross-system allies: the specialist engine (skeletal/repair = tech-debt remediation), the specialist engine (lymphatic/repair-stability), the specialist engine-Healing (:port, repair cascades = automated cleanup), glymphatic clearance pattern (stale-state reset for cron pipelines).
- **Missing:** B2B waste-stream classification (dead features, zombie crons, stale leads, sunk-cost projects, orphaned SaaS spend — not mapped as a urinary process flow); cleanup process_flows are the fleet's biggest gap (2026-07-07 audit: immune/repair engines have ZERO process_flows; Bright's business-cleanup flows equally thin — Rule 13 mandates canonical flow categories); cost-excretion/budget-drain filter (glomerular filtrate = all spend, reabsorption = justified, excretion = cut); electrolyte/feedback balance for resource allocation.
- **Business document produced:** Waste Stream & Cleanup Report (filtered/killed, reabsorbed/justified, excreted/deprecated); Technical-Debt Clearance Cadence (scheduled cleanup with accumulation alerts — rising "creatinine" = debt piling up).

### 6. Endocrine → Culture / Motivation
- **Existing engines (body_system=`endocrine`, 2 engines):** the specialist engine (:port, second-messenger/cAMP signaling, HPA/HPT/HPG axes, negative-feedback broadcast), the specialist engine (endocrine, pituitary/master-gland coordination = executive culture-setting). Cross-system: the specialist engine (allostasis — *correctly reclassified endocrine* per immune-separation note: HPA/cortisol is endocrine not nervous), the specialist engine (nervous, RPE/dopamine = motivation/reward signal).
- **Missing:** Culture-as-hormone broadcast model (organism-wide culture broadcast as hormonal signal with second-messenger amplification — not a registered process flow); motivation axis wiring (Schultz RPE ↔ Sutherland broadcast coupling); stress/urgency HPA business analog (Sterling models physiological allostasis, not business-stress → culture modulation; Rule 31 — no graceful degradation, the cortisol signal must drive real action); values-alignment broadcast (oxytocin analog for fleet cohesion); long-horizon vision signal (GH analog).
- **Business document produced:** Culture & Motivation Broadcast (urgency/cortisol, drive/dopamine, cohesion/oxytocin, direction/GH — periodic "hormonal panel" of org culture); Values & Operating Principles Document (the slow endocrine setpoint — cf. `CULTURE-AND-OPERATING-PRINCIPLES.md`); Motivation Cadence Policy (how urgency shifts task prioritization and routing).

---

## Cross-System Axes (the interactions that make the six a working organism)

From PHYSIOLOGY-COMPLETE-BODY-SYSTEMS.md §6 — all directly relevant to systems 1–6:

| Axis | Systems coupled | B2B meaning |
|---|---|---|
| Gut–Brain | Digestive (4) ↔ Nervous (1) | Customer intake signals reshape routing/decisions |
| HPA Axis | Endocrine (6) ↔ Nervous (1) ↔ Allostasis | Culture/urgency modulates decision setpoints |
| RAAS | Urinary (5) ↔ Cardiovascular (2) ↔ Endocrine (6) | Cleanup/liquidity pressure regulates financial flow & culture |
| Haldane coupling | Respiratory (3) ↔ Cardiovascular (2) | Comms cadence ↔ revenue perfusion (oxygenated capital) |

---

## The "Thin Periphery" Finding (Durable Gap Pattern)

The Nervous system (decision/routing) is **over-built** (45 engines) because it was developed first. Systems 2–6 each have only **1–2 dedicated engines** and — critically — **most peripheral engines have zero registered business process_flows**. This was first documented in the 2026-07-07 immune/repair fleet audit (single largest flow gap) and confirmed August 2026 to extend across cardiovascular, respiratory, digestive, urinary, and endocrine.

**Build priority implication:** The priority is NOT new peripheral engines. It is **wiring the existing peripheral engines into B2B business process flows** using the 8 canonical biological flow categories (neuromodulatory, autonomic, oscillatory, metabolic, homeostatic, sensorimotor, structural_plasticity, endocrine). Engines without process_flows are anatomically present but functionally silent.

---

## Programmatic Engine Extraction Technique (Reusable)

When asked to map body systems or audit per-system coverage, **always extract from the live registry** — never rely on memory or skill docs (which drift). The canonical extraction:

```python
import re
from collections import defaultdict

with open('/<workspace>') as f:
    txt = f.read()

# Extract (engine_name, body_system) pairs by scanning entry blocks
entries = re.findall(
    r'engine_name["\']?\s*[:=]\s*["\']?([A-Za-z][\w\- ]+)["\']?[\s\S]{0,400}?body_system["\']?\s*[:=]\s*["\']?([\w_]+)',
    txt
)
by_sys = defaultdict(list)
for name, sys_ in entries:
    by_sys[sys_.strip()].append(name.strip())

for sys_ in sorted(by_sys):
    engines = sorted(set(by_sys[sys_]))
    print(f"[{sys_}] ({len(engines)})")
    for n in engines:
        print(f"  - {n}")
```

**Variants:**
- Count only: `re.findall(r'"body_system"\s*:\s*"([^"]+)"', txt)` → `Counter`.
- Process-flow audit (find engines with zero flows): query `process_flows` key presence per entry.
- Port collision check: extract `port` field per entry and run `Counter`.

**Authoritative registry locations** (check the most recently modified):
- `/<workspace>`
- `/<workspace>`
- `/<workspace>` (the operator agent organism canonical)
- `/<workspace>`

---

## B2B Organism Architecture Notes

- **B2B↔B2C is mycorrhizal (Rule 16).** Each B2B and B2C is an *independent organism* (a tree). the specialist engine is the mycelial network connecting them. Data/capabilities flow through the network; no organism owns another. Do NOT model B2B-B2C as mother-fetus, cell-neuron, or endocrine-axis — all three were rejected.
- **B2B organisms CAN spawn** B2BU organisms (with purchase limits) and B2B products. Genome protection enforces spawn limits.
- **B2B gets bone marrow** (customer-specific model training) and detailed medical/diagnostic sections (no "easy" mode).
- **Firewalls are layered** (B2B→B2BU→B2C information protection; audience-dependent layers).
- See `docs/reproductive-system/B2B-ORGANISM-CONFIG.md` for the full 12-field registration spec.
