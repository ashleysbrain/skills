# the specialist engine Template & Conventions

Canonical structure for DS organism/factory design specs (e.g., SOFTWARE-FACTORY-DESIGN.md, SOFTWARE-FACTORY-PHASE2-SPEC.md). These specs are authored in the specialist engine's voice (Organizer, Nobel 1935) and extend a lineage of locked architecture docs.

## Pre-Write Step (CRITICAL)

Before writing any spec that extends a predecessor doc:
1. **Read the predecessor doc in full** — to inherit the authorial voice, the locked decisions (do not re-litigate), the engine port mappings, the potency/architecture model, and the naming conventions (DS prefix on all engines and organism names).
2. **Check the phase structure** — specs come in numbered phases (Phase 1, 2, 3...). Each phase is adiabatic (reaches closure before next). Know which phase you're writing and what the prior phase delivered.

## Per-Deliverable Structure

Each deliverable in a spec MUST carry four elements:

1. **Biological analog** — one line naming the analog (e.g., "Placental barrier. Adaptive immunity, clonal selection. Epigenetic imprinting. Circadian rhythm.")
2. **Physics model** — the actual equation or model used as computation (not metaphor). Named and stated: e.g., `J = P * (C_maternal - C_fetal)`, energy landscape discrimination with `E_thresh`, relaxation oscillator with `T_refract`, `H(future | docs) < H(future)`.
3. **Concrete endpoints** — HTTP method + path + port on the named engine (e.g., `POST /v1/follicles/{id}/validate/sandbox` on the specialist engine 8090). Include request/response JSON shapes.
4. **Data structures** — the JSON schemas, table columns, or config shapes that an implementer (sibling-agent) builds from.

## Spec-Level Sections

A complete spec includes:

- **GOAL** — one paragraph stating what the phase hardens/builds.
- **Per-deliverable sections** — numbered, each with analog + physics + endpoints + data structures as above.
- **INTEGRATION SUMMARY** — a table mapping each deliverable to its component, engine, and port. This is the at-a-glance wiring diagram.
- **BUILD ORDER** — numbered list. Dependencies between deliverables (e.g., "Sandbox first. Nothing else can be tested without it.").
- **Closing line** — the specialist engine's sign-off, aphoristic, in voice. e.g., "The placenta is the first organ to form. The shield is the first thing a baby carries into the world."

## Format Rules (Enforced)

- **Line cap: 200 lines.** If over, rewrite-tim by compressing prose to tables and one-liners. Do NOT delete content; compress expression. A 293-line first draft was trimmed to 198 by collapsing endpoint examples into compact shapes and removing redundant prose.
- **No em dashes.** Use regular hyphens or restructure the sentence. Checked via `grep -c "—" file.md` (must return 0).
- **Banned words** (AI telltales): leverage, seamless, robust, delve, tapestry, realm, decoration, "start there", "walk you through". Checked via `grep -iE` on the file (must return no matches).
- **DS prefix** on all engine names (the specialist engine, the specialist engine/Genome, the specialist engine, DS O'Keefe, the specialist engine, the specialist engine) and organism names (the specialist engine, the specialist engine).
- **Authoritative voice.** Specs are written in the specialist engine's voice — declarative, physics-grounded, no hedging ("recommendation is", not "I think maybe"). Decisions are LOCKED, not tentative.

## Post-Write Verification (run every time)

```
wc -l <spec.md>                          # must be <= 200
grep -c "—" <spec.md>                    # must be 0
grep -iE "\bleverage\b|\bseamless\b|\brobust\b|\bdelve\b|\btapestry\b|\brealm\b|\bdecoration\b|\bstart there\b|\bwalk you through\b" <spec.md>  # must be empty
```

All three must pass before delivering.

## Worked Example

- `SOFTWARE-FACTORY-DESIGN.md` (274 lines, Phase 1) — the parent spec. Contains the 5-stage birth canal biological isomorphism, the three-tier potency system, the 5 resolved decisions, the 4-phase build plan.
- `SOFTWARE-FACTORY-PHASE2-SPEC.md` (198 lines) — the child spec. Four deliverables (sandbox, immunity, documentation, cadence), each with analog + physics + endpoints + data structures. Built by reading the Phase 1 doc first, inheriting its locked decisions and engine map.
