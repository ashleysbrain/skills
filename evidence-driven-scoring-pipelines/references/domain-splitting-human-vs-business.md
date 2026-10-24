# Domain splitting: human 8D vs business 8D

## When to split
Split the spec when the same scoring concept is being used for two domains with different semantics, clocks, or baselines.

Typical split signal:
- person-level adaptive scoring uses a sleep-linked wake session
- organization-level scoring uses a reporting window or operating cycle
- the same math can be shared, but the domain meaning is different

## Recommended structure
Use three files:
- `ADAPTIVE-EVIDENCE-LEDGER-PRODUCT-SPEC.md` — human 8D / Patient 0
- `ADAPTIVE-EVIDENCE-LEDGER-BUSINESS-SPEC.md` — business 8D / your-org
- `ADAPTIVE-EVIDENCE-LEDGER-SHARED-PRIMITIVES.md` — canonical shared mechanics

## What belongs in the shared primitives doc
Keep only the cross-domain mechanics there:
- accumulation window shape
- evidence event shape
- field update shape
- confidence state shape
- coverage / recency / corroboration / reliability math
- append-only provenance and replay rules
- shared state transitions

## What belongs in the domain specs
Keep domain-specific meaning in the domain docs:
- boundary condition for the window
- source set and examples
- dimension vocabulary
- UX language
- seal trigger
- acceptance criteria
- any domain-specific overrides to shared defaults

## Duplication rule
If a formula or threshold is identical in both domains, define it once in the shared primitives doc and reference it from both domain specs.

If a formula differs by domain meaning, keep the difference explicit in the relevant domain spec and do not hide it behind a generic alias.
