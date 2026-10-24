# Three-Tier Partnership Flow Design

**Source:** Session 2026-07-07 — user asked for complete the operator agent → B2B → B2C → Products process flow.
**Spec file:** `~/your-workspace/ds-wave-gamification-advisory-panel-private/THREE-TIER-PARTNERSHIP-FLOW.md` (297 lines, 9 sections)

## Key Design Decisions Captured

### Near-instant B2C birth via pre-birth template pool
Full gestation takes hours, but users expect <30s latency when clicking "Enable the specialist engine" in a partner app. Solution: the operator agent maintains a warm pool of pre-gestated B2C template organisms per partner (at Fetus stage, APGAR pending). On user enablement, the operator agent pulls a template, specializes it (stamp URN, verify ECS identity, write birth record, APGAR spot-check), and returns it live. This is the only background-cost operation — pool replenishment triggers when depth drops below threshold (~50).

### B2B organisms are reproductively PARTIAL
B2B organisms can birth products (PARTIAL potency) but CANNOT birth B2C organisms. When a partner user needs a B2C organism, the B2B submits a request to the operator agent, which births the B2C from its template pool. This preserves the reproductive hierarchy: only the operator agent births organisms.

### Data flow directionality
- UP: Product → B2C (raw usage) → B2B (anonymized outcomes + 8D scores) → the operator agent (aggregate coupling matrices, no user/partner identity)
- DOWN: the operator agent engine updates cascade through evolution push protocol, gated by developmental stage at every tier boundary
- the operator agent uses population-scale coupling data (the specialist engine) to update physics models (Landau, Kuramoto, nucleation thresholds), which flow back DOWN as evolution pushes

### Partnership termination reparenting
When a partner relationship ends, all B2C organisms under that B2B reparent from `ds://partner-b2b/` to `ds://gg-direct/`. Users never lose their coaching. Products survive — their parent (B2C) simply gets a new grandparent. B2B organism deprecated after 90-day hospice.

### Revenue model
Product revenue split: DS/the operator agent 40%, Partner/B2B 35%, the operator agent Infrastructure 10%, B2C user benefit 15% (credited as coaching credits). Partnership tiers: S ($500K+, all engines, white-label), A ($150-500K, 8D+coaching+gamification, co-branded), B ($50-150K, 8D+health data pipeline).

### Consent boundary enforcement
Each B2C organism carries `consent_flags` (share_with_partner, share_aggregate_with_gg, retain_after_partner_exit). User controls these. B2B cannot override. the operator agent never sees anything flagged false.

## API Surface (15 endpoints)

Three groups: B2C lifecycle (birth request, template pool, user enablement, namespace management), data flow UP (b2c→b2b, b2b→gg aggregate pushes), evolution push DOWN (gg→b2b→b2c cascade), governance (reparent, hospice).

## How This Extends the Locked Potency Hierarchy

The `locked-potency-hierarchy.md` reference defines the cryptographic potency system (FULL/PARTIAL/NONE). This partnership flow spec operationalizes that hierarchy for commercial deployment:
- the operator agent (FULL) births B2B organisms with PARTIAL tokens
- B2B (PARTIAL) requests B2C births from the operator agent (cannot self-birth organisms)
- B2C (PARTIAL) births products with NONE tokens
- Products (NONE) are terminal — sterile, no reproductive organs

The template pool pattern is the key innovation that makes commercial viability possible without violating the locked architecture.
