# Two-Silo Architecture — Engine Fleet + Patient 0 Health Tracking

## Overview

When the user is both building the AI organism AND the first patient (Patient 0), use a **dual-silo architecture** with complete isolation. This pattern emerged from the June 13, 2026 session where both the engine fleet (7 engines) and patient interface (principal-interface) were deployed and verified.

## Silo 1: Engine Fleet (The AI Organism Body)

**7 profiles, 7 engines, self-healing 24/7**

| Profile | Engine | Port | Body System | Purpose |
|---|---|---|---|---|
| `wave` | Wave | 8000 | Brain/CNS | Coaching, Mastermind, Resonance |
| `quartz` | Crystal | 8089 | Autonomic NS | PID Control, Lattice, Tasks |
| `seed` | Seed | 8090 | Endocrine/Growth | Avrami JMAK, Landau, Product Dev |
| `allostasis` | Allostasis | 8091 | Immune/Homeostatic | Surveillance, Allostatic Load, Intervention |
| `harvey` | Harvey | 8092 | Circulatory | Fabric, Transport, Registry |
| `morphogen` | Morphogen | 8093 | Skeletal/Registry | Genotype Registry, BMP Gradients |
| `bernard` | Bernard (AI Clinical) | 8094 | Clinical Diagnostic | SOAP Rounds, Differential Dx, Vitals, AI-Equivalent Credentials, Evidence Synthesis, 12 Non-US Health System Methodology |

**Self-Healing Loop (Autonomic, every 4h):**
```
Allostasis scans → detects anomaly → alerts Bernard
Bernard diagnoses → writes SOAP note → prescribes fix
Fix deployed by the specialist engine (cron c890b270b920)
the specialist engine (Allostasis) verifies fix → clears alert
Morphogen updates organism map → all healthy
```

**Cron Jobs (Engine Fleet):**
- Bernard Auto-Heal — every 4h (c890b270b920)
- principal/CTO/Design/Legal/Research Advisory — daily (via Wave)
- SENTINEL Compliance — daily (FORGE/ARBITER)
- TWC Algorithm Audit — every 12h (the specialist engine)
- Model Compliance — daily (No-Anthropic enforcement)

## Silo 2: Patient 0 Health Tracking (Your Personal Health)

**1 profile, your single Telegram entry point**

| Component | Purpose |
|---|---|
| `principal-interface` | Single Telegram entry point → routes to engine APIs |
| `AISHA-MD` | 8D Wellness: Physical, Emotional, Intellectual, Social, Spiritual, Vocational, Financial, Environmental |
| Daily TWC/SOS scoring | Health trends, recovery tracking, coaching delivery |

**Routing Logic (in principal-interface SOUL.md):**
- `"health"`, `"vitals"`, `"diagnose"`, `"rounds"` → **Bernard (8094)** `/patient/vitals`, `/rounds`
- `"coach"`, `"strategy"`, `"decide"` → **Wave (8000)** advisory panels
- `"tasks"`, `"plan"`, `"schedule"` → **Quartz (8089)** `/v1/tasks`, `/v1/lattice/state`
- `"build"`, `"product"`, `"feature"` → **Seed (8090)** `/v1/engines`, `/landau`
- `"monitor"`, `"stress"`, `"immune"` → **Allostasis (8091)** `/organism`
- `"registry"`, `"fleet"`, `"status"` → **Morphogen (8093)** `/organism/map`
- `"flow"`, `"messages"` → **Harvey (8092)** `/fabric/vitals`

**Cron Jobs (Patient 0):**
- Health Scoring Daily Pipeline — 8D/TWC scoring
- Obsidian Health Vault Sync — daily
- Fleet Analytics Sync — daily at 23:15
- FORGE-ARBITER Talent Review — daily at 22:45
- FORGE-ARBITER Talent Processor — daily at 21:00

## Key Separation Guarantees

| Guarantee | Engine Fleet (Silo 1) | Patient 0 (Silo 2) |
|---|---|---|
| **Scoring** | TWC (organizational), allostatic load, engine health % | 8D wellness, SOS, TWC (personal), clinical vitals |
| **Agents** | the specialist engine, the specialist engine, the specialist engine (AI Physician), FORGE, ARBITER | AISHA-MD, Advisory Panels (principal, CTO, etc.) |
| **Memory** | Separate Honcho workspaces, builder context | Isolated patient context, health history |
| **Telegram** | Internal comms only (never user-facing) | User-facing via principal-interface |
| **Cron** | Auto-heal, advisory, compliance | Health scoring, coaching, sync |

## Implementation Checklist

- [ ] 7 engine profiles created (`wave`, `quartz`, `seed`, `allostasis`, `harvey`, `morphogen`, `bernard`)
- [ ] 1 patient interface profile created (`principal-interface`)
- [ ] Telegram `default_profile` set to `principal-interface`
- [ ] Engine services running on localhost:port-8094
- [ ] All 7 engines registered in Morphogen (port 8093)
- [ ] Bernard cron (c890b270b920) running every 4h
- [ ] Patient 0 cron jobs scheduled
- [ ] Zero cross-silo memory leakage verified
- [ ] Clinical engine returns identity + disclaimer on every endpoint

## Session Reference

- **Date**: June 13, 2026
- **Blueprint**: `/<workspace>`
- **All 7 engines verified UP**: Wave(8000), Crystal(8089), Seed(8090), Allostasis(8091), Harvey(8092), Morphogen(8093), Bernard(8094)
- **Morphogen Registry**: 7 engines, 7 systems — all `healthy`
- **Telegram gateway**: Running in `default` profile, routing to `principal-interface`