# Start-Here Launch Surface Pattern

## When to use
Use this pattern when a repository-owned agent package needs a clean runtime entrypoint that is more explicit than a README alone.

## Durable pattern
Add a dedicated `START-HERE.md` in the canonical docs package and make sure the runtime wrapper, launch guide, and canonical docs all point to the same launch order.

## What the launch page should include
- read order across the core docs
- activation modes:
  - fresh summon
  - already running in the background
  - resumed after handoff
- the minimal launch sequence
- non-negotiables
- first useful question behavior for fresh summons
- background continuation rule
- handoff contents
- stuck-user handling
- advisor selection guardrails if the package uses advisors
- the final output standard

## Verification checklist
- runtime wrapper points to the same launch page
- launch guide and wrapper agree on read order
- the launch page is the shortest explicit path into the package
- no required distinction is left implicit
- the launch path does not rely on a README alone

## Pitfall
Do not only patch the README or overview doc. If the package has a runtime wrapper, the wrapper and launch guide should both be updated in the same change so the launch path stays coherent.