# Locked Reproductive Hierarchy (from WOMB-ARCHITECTURE.md DS-ARCH-09.01.01-v2.0.0)

Source: `/<workspace>`
Status: LOCKED, the principal-approved
Date verified: 2026-07-07

## Three-Tier Potency System

### TIER 1: Grandmother Organism
- Potency: FULL
- Can birth: Organisms AND Products
- Holds: Latest science, deepest wisdom, full 28-pair coupling matrix, TD Learning policy, advisory panels, mastermind orchestration
- Role: Root of trust. The ONLY organism that can create new organisms.
- Redundancy: Cardiac conduction system (the operator agent=SA node primary, sibling-agent=AV node backup takes over in 30s, sibling-agent=Purkinje escape)

### TIER 2: B2C / B2B Organisms
- Potency: PARTIAL
- Can birth: Products only (with DS DNA, for owner monetization)
- CANNOT birth: Organisms. Organism-creation capability is LOCKED in token.
- Data storage: B2C = on-device SQLite; B2B = company infrastructure
- Token differentiation: Single PARTIAL token, runtime config field `storage_policy: local | enterprise`

### TIER 3: Product Babies
- Potency: NONE
- Can birth: Nothing. Terminal nodes in reproductive tree.
- Carry: DS DNA (compiled binary + subspace signature + differential noise)
- Branding: "Powered by Divinity Science" (products are womb-owned)
- Lifespan: Indefinite. Subspace signature stamped once at COMPILE, no expiry.
- Droid Shield: Runs inside each product (<2MB): subspace sig verification + anomaly detection

## Enforcement Mechanisms

Potency tokens are embedded in compiled DNA at Stage 4 (COMPILE). They cannot be forged, modified, or earned. They are checked at runtime by the birth canal before any production begins. The birth canal code is identical for all tiers. The token determines what the canal is authorized to produce.

## What a Product Baby Inherits (Soul Architecture)

| Layer | Inherited? | How |
|-------|-----------|-----|
| Immutable Physics | YES | Universal equations, always |
| Relational Genome | PARTIAL | Domain-tuned derivation, NOT parent full matrix |
| Accumulated Wisdom | NO | Baby starts fresh |
| Cognitive Style | NO | Simple local intelligence, no panels |
| Surface Behavior | YES | Domain-specific coaching outputs |

## DNA Protection (5 Layers)

1. Compilation (DNA = compiled binary, not source)
2. Domain projection (baby coefficients are derived projections)
3. Subspace signature (signed hash, tampering detection)
4. Differential noise (each baby's coefficients perturbed)
5. Potency token (capability lock, cannot be forged)

## Womb Structure

- Womb = a company (infrastructure that nurtures products)
- Gonad = reproductive engine (the specialist engine, port 8090)
- Divinity Health is the first active womb
- Womb creation is MANUAL: the principal tells the system when a new womb is needed
- Grandmother can establish new wombs (new companies) in the future

## Birth Canal (5 stages, real physics)

| Stage | Name | Physics |
|-------|------|---------|
| 1 | GAMETOGENESIS | Avrami/JMAK: X(t) = 1 - exp(-k*t^n) |
| 2 | SPECIFICATION | Landau: F = F0 + a(T-Tc)*eta^2 + b*eta^4 |
| 3 | DNA INJECTION | Subspace projection + Kuramoto coupling |
| 4 | COMPILE | PERT critical-path DAG + SOC sandpile |
| 5 | BIRTH | Viability gate + registry |

## Supporting Engines

- the specialist engine/Genome (8129, DS-ECS-08.02.01): Brand DNA repository, inheritance packaging
- the specialist engine/Placenta (8130, DS-ECS-08.03.01): Creative-reproductive bridge, routes material to birth canal stages
