# BetterSleep ResearchKit Integration — Architecture & Advisory Panel

## Session Context (2026-06-12)
Built the research integration layer for BetterSleep 8D Clone app.

## Advisory Panel Structure (3 Coaches)
1. **AI ResearchKit Integration Strategist** — Technical architecture, IRB, FHIR pipeline
2. **the specialist engine-Science Methodologist** — Study design, statistical validation, publication strategy
3. **AI University Partnership Architect** — Stanford/Harvard/Penn partnerships, IP, honorary degree pathway

## Panel Files
- `/<workspace>`
- `/<workspace>`
- `/<workspace>`
- `/<workspace>`
- `/<workspace>`

## Key Architecture Decisions

### FHIR Bridge Libraries (Verified)
- `StanfordBDHG/ResearchKitOnFHIR` — Stanford's bridge from ResearchKit to FHIR
- `microsoft/healthkit-on-fhir` — Microsoft's HealthKit → FHIR export
- `C3-PRO` — ResearchKit → i2b2 via FHIR (published in PLOS ONE)

### Data Pipeline
```
BetterSleep App → HealthKit (local) → ResearchKit (study data)
  → Firebase (encrypted sync) → FHIR Server → University REDCap/i2b2
```

### IRB Pathway
- Phase 1: Quality improvement (no IRB needed)
- Phase 2: Expedited Category 7 at partner university (6-8 weeks)
- Phase 3: Full IRB for RCT (12-16 weeks)
- Precedent: Apple Heart Study (2017) — 400K+ participants, NEJM

### Validation Study (Minimum Viable)
- n=30, 2-week passive collection
- Compare 8D Physical vs. actigraphy, 8D Psychological vs. PSQI/ISI
- Target journals: JMIR mHealth, NPJ Digital Medicine, SLEEP

### ClinicalTrials.gov Integration
- Scrape API for "sleep" + "mobile" + "wearable" currently recruiting studies
- In-app "Match Me" button with eligibility criteria matching
- Marketing: "First sleep app to auto-match you with university sleep studies"

## Rome Conference Prep
- User accepted to speak at neuroscience/math conference in Rome
- Topic: TWC (Theoretical Wellness Composite) calculation
- Weekly writing schedule set (Fridays 9 AM, cron job 4b83f63e69ca)
