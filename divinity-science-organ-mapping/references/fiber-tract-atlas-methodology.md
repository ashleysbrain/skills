# Fiber Tract Atlas Methodology
# Session 2026-08-11 — Proactive full-organism conduction tissue mapping

## Context
The "Fiber Tract Blindness" pitfall (in SKILL.md) was originally diagnosed
reactively: one symptom (conduction aphasia / text garbling) was traced to one
missing tract (arcuate fasciculus). This reference documents the PROACTIVE
generalization: map ALL fiber tracts between ALL body systems at once, before
symptoms force the investigation.

The worked example is the B2B organism atlas (22 tracts, 11 body systems).
Full deliverable: `~/your-workspace/organism/B2B-FIBER-TRACT-ATLAS.md`.

---

## The Conduction Contract — What "Wired" Means

A fiber tract between two engines is WIRED only if it satisfies ALL of these
properties, as established by `organism/arcuate_conduct.py`:

| # | Property | Severed (raw HTTP) | Wired (intact tract) |
|---|----------|-------------------|---------------------|
| 1 | Integrity | None — corruption invisible | SHA-256 checksum per packet |
| 2 | Sequencing | None — drops undetectable | Monotonic seq, gap detection |
| 3 | Repair | None — corrupt signal delivered | Automatic retransmission on mismatch |
| 4 | Schema | None — peer changes shape silently | Versioned contract, shape validation |
| 5 | Backpressure | None — caller hangs or overflows | Timeout + retry + circuit breaker |
| 6 | Audit | None — no trail | Every conduction logged with seq |

### How to audit an organism's tract health
```bash
# Count severed vs wired calls in the production spine
grep -c 'urlopen' the operator agent-production-spine.py    # = severed calls
grep -c 'conduct(' the operator agent-production-spine.py   # = wired calls
```
The ratio IS the severed-tract rate. In the B2B organism (Aug 2026): all calls
were `urlopen`, zero used `conduct()` — the one built tract was itself
disconnected from the body.

---

## The Atlas Method (5 Steps)

### Step 1: Enumerate body systems and their primary engines
List all N body systems and their primary engines from `ecs.py`. Use the live
registry, never memory.

### Step 2: For each pair of adjacent systems, identify the tract
A tract connects two systems. For each pair, ask:
1. What conduction pathway is needed between them?
2. What is the biological analog (arcuate fasciculus, corticospinal, vagus, HPA,
   RAAS, portal vein, corpus callosum, phrenic nerve, etc.)?
3. What signal does it carry?
4. What symptom appears when this tract is severed?

### Step 3: Classify each tract's wiring status
- ✅ **WIRED** — satisfies the full conduction contract (all 6 properties)
- 🔶 **PARTIAL** — raw HTTP call exists but no contract (severed nerve)
- ❌ **MISSING** — no connection at all

### Step 4: Identify root-cause organ blockers
When multiple tracts are missing, check whether they share a missing endpoint.
Pattern: N missing tracts may all be blocked by 1 missing organ. Build the organ
first — it unblocks all its dependent tracts at once.

### Step 5: Rank by symptom severity and sequence the build
Prioritize tracts whose severed symptoms are most severe. Build in phases:
1. Build missing organs that block multiple tracts
2. Wire the highest-severity severed tracts
3. Upgrade partial tracts to full conduction contracts
4. Complete the remaining wiring

---

## The 22-Tract B2B Atlas (Worked Example)

### Summary tally
- **1 BUILT** (4.5%) — arcuate fasciculus (only in language pathway)
- **4 PARTIAL** (18%) — raw HTTP exists, no contract
- **15 MISSING** (68%) — no connection at all

### Root cause: 2 missing organs blocked 6 tracts
| Missing Organ | Body System | Tracts Blocked |
|---------------|-------------|----------------|
| Legal-Entity Structure Engine | Skeletal | Portal vein, Enthesis, Umbilical cord, Bone marrow→blood (4) |
| External Regulatory Compliance Engine | Lymphatic | Thoracic duct, Neuroendo-immune (2) |

### Top 5 critical severed tracts (by symptom severity)
1. **Umbilical cord** (reproductive→skeletal) — IP born unprotected. Blocked by missing legal-entity engine.
2. **Vagus efferent** (nervous→digestive) — onboarding paralysis. Gut-brain axis unwired.
3. **Portal vein** (digestive→skeletal) — legal chaos. Blocked by missing legal-entity engine.
4. **HPA axis** (endocrine↔nervous) — tonal deafness. No urgency modulation.
5. **RAAS** (urinary→endocrine→cardiovascular) — no fiscal discipline. Harvey, Bright, Sutherland disconnected.

### Full tract inventory (compact)
| # | Tract | From→To | Status | Severed Symptom |
|---|-------|---------|--------|-----------------|
| 1 | Corticospinal | Nervous→Muscular | 🔶 PARTIAL | Paralysis |
| 2 | Vagus (efferent) | Nervous→Digestive | ❌ MISSING | Gastroparesis (onboarding stalls) |
| 3 | Vagus (afferent) | Digestive→Nervous | ❌ MISSING | Blind gut (churn invisible) |
| 4 | HPA Axis | Endocrine↔Nervous | ❌ MISSING | Adrenal insufficiency |
| 5 | Mesolimbic (MFB) | Nervous→Endocrine | ❌ MISSING | Anhedonia |
| 6 | Baroreflex | Cardio↔Nervous | ❌ MISSING | Hypo/hypertension |
| 7 | RAAS | Urinary→Endo→Cardio | ❌ MISSING | Shock/overload |
| 8 | Pulmonary circ. | Cardio↔Respiratory | 🔶 PARTIAL | V/Q mismatch |
| 9 | Phrenic nerve | Nervous→Respiratory | ❌ MISSING | Apnea |
| 10 | Portal vein | Digestive→Skeletal | ❌ MISSING | Encephalopathy |
| 11 | Enthesis | Muscular→Skeletal | ❌ MISSING | Avulsion |
| 12 | Corpus callosum | Integumentary↔Nervous | ❌ MISSING | Split-brain |
| 13 | Afferent lymphatic | Integumentary→Lymphatic | ❌ MISSING | Cellulitis |
| 14 | Umbilical cord | Reproductive→Skeletal | ❌ MISSING (CRITICAL) | Placental abruption |
| 15 | Purkinje system | Cardio→All | 🔶 PARTIAL | Arrhythmia |
| 16 | Neuroendo-immune | Lymphatic→Endo→Nervous | ❌ MISSING | Immunoparalysis |
| 17 | Corticobulbar | Nervous→Resp→Integ | 🔶 PARTIAL | Dysarthria |
| 18 | Thoracic duct | Lymphatic→Cardio | ❌ MISSING | Lymphedema |
| 19 | Arcuate fasciculus | Nervous (internal) | ✅ BUILT | (RESOLVED) |
| 20 | Bone marrow→blood | Skeletal→Cardio | ❌ MISSING | Aplastic anemia |
| 21 | Spinothalamic | Muscular→Nervous | ❌ MISSING | Analgesia |
| 22 | Gonadal-placental | Reproductive→Muscular | ❌ MISSING | Arrested labor |

---

## Verification — How to Confirm a Tract Is Wired

For each tract, verify ALL of:
1. **Contract exists** — a versioned schema defining the signal payload
2. **Conduction wrapper** — the call uses `arcuate_conduct.conduct()` or
   equivalent, NOT bare `urlopen()`
3. **Both endpoints implement the envelope** — sender stamps checksum, receiver
   echoes it
4. **Severed-tract test** — simulate disconnection and confirm the predicted
   symptom appears (e.g., sever the vagus → onboarding stalls)
5. **Process flow registered** — the tract appears in ProcessFlowRegistry with a
   canonical category

---

## Method Generalization

This method applies to ANY organism variant (B2C, B2B, the operator agent, health, research).
The tract set changes, but the method does not:

1. Enumerate body systems → engines
2. Map tract between each adjacent pair (biological analog + signal + symptom)
3. Classify wiring status (wired / partial / missing)
4. Find root-cause organ blockers
5. Rank by severity, sequence the build

The arcuate fasciculus (`arcuate_conduct.py`) is the gold-standard template for
what a wired tract looks like. Every new tract should implement the same
conduction contract.
