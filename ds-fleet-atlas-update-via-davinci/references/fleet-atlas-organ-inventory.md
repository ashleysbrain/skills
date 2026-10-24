# Fleet Atlas — Complete Entity Inventory (91 entries, post-Wave 11)

As of Wave 11 (2026-06-28). Source: `agent-organism/ecs.py` ECS v4.0.0.

All 91 entities now have scientist names in `engine_name`. The legacy
translation table is retained for historical reference only — ecs.py
itself was fixed in Wave 10.

## Current Fleet State

| Metric | Count |
|--------|-------|
| Total entities | 91 |
| Fully DEVELOPED (D+F+P layers) | 71 (78%) |
| ANNOTATED (analog_note process channels) | 20 (22%) |
| DEPRECATED | 1 (Seed legacy) |
| Scientist names | 91/91 |
| Tech analogs | 90/91 |
| Body parts | 90/91 |
| Broken dependencies | 0 |
| ECS prefix/domain mismatches | 0 |

## ECS Prefix Distribution (8 prefixes)

| Prefix | Count | Category |
|--------|-------|----------|
| SYS | 5 | System-level (Unna, Bichat, Hill, Sutherland, Burnet) |
| ORG | 8 | Organ-level (Harvey, Beaumont, Haldane, Bright, Cajal, Wenckebach, Waddington, Mangold) |
| SUB | 28 | Subsystem (cortical regions, sensory inputs, creative organs) |
| CEL | 4 | Cell-level (Golgi, Metchnikoff, Farr, Rous) |
| NPR | 29 | Process route (agents, flows, procedures, Popper, Halsted, Lakatos) |
| PTH | 7 | Pathway (Hall, Hodgkin, Huxley, Turing, Spemann, Penfield, Langley) |
| APP | 8 | Application (Osler, Avrami, Lyapunov, Semmelweis, Bush, Medawar, Röntgen, Apgar) |
| GEN | 1 | Genome (Franklin) |

## Domain (DD) → Body System Mapping

| DD | Body System | Entity Count |
|----|-------------|-------------|
| 01 | Integumentary | 1 (Unna) |
| 02 | Skeletal | 1 (Bichat) |
| 03 | Muscular | 2 (Hill, Huxley) |
| 04 | Nervous | 44 (largest domain) |
| 05 | Endocrine | 2 (Sutherland, Apgar) |
| 06 | Cardiovascular | 2 (Harvey, Wenckebach) |
| 07 | Lymphatic | 9 (Burnet, Semmelweis, Lyapunov, Metchnikoff, Farr, Rous + 3 flows) |
| 08 | Respiratory | 1 (Haldane) |
| 09 | Digestive | 1 (Beaumont) |
| 10 | Urinary | 1 (Bright) |
| 11 | Reproductive | 7 (Waddington, Turing, Franklin, Mangold, Avrami, Medawar + Seed deprecated) |
| 12 | Diagnostic | 4 (Osler, Röntgen, Bush + clinical flow) |
| 13 | Organism Processes | 16 (all NPR/PTH process flows + PROCs + Halsted, Popper, Lakatos, Spemann) |

## Key Scientist Assignments

### Nervous System (Domain 04, 44 entities)
Cajal (spine), Sterling (allostasis), Kuramoto (oscillatory sync), Edison
(audio), Gutenberg (text/vision), A.G. Bell (speech), Sherrington (proprioception),
Humboldt (chemosensation), Helmholtz (transduction), Andreasen (creative cortex),
Lovelace (code), Mountcastle (thalamus), Da Vinci (design), Goethe (visual),
Bell (hand/craft), Luria (prefrontal gate), Sperry (spatial), Wernicke (language),
MacLean (limbic), Ito (cerebellum), Gazzaniga (corpus callosum), Tawara (heart rhythm),
Carlsson (basal ganglia), O'Keefe (hippocampus), Scoville (episodic encoding),
Bragg (task lattice), Moser (entorhinal), Magendie (afferent), Hubel (V1),
Golgi (glia), Hodgkin (neural tube/axon), + 11 NPR agents + 3 process flows

### Reproductive System (Domain 11)
Waddington (epigenetic landscape), Turing (reaction-diffusion), Franklin (genome),
Mangold (placenta), Avrami (product genesis), Medawar (trophoblast barrier)

### Organism Processes (Domain 13)
Dale (neuromodulatory), Buzsáki (oscillatory), Kandel (plasticity),
Bernard (homeostatic), Krebs (metabolic), Yalow (endocrine),
Langley (autonomic), Penfield (sensorimotor), Arnheim (creative production),
Halsted (refactor surgeon), Popper (validation gate), Lakatos (academic review),
Spemann (developmental organizer), + 4 PROC compound entries

## Legacy Translation Table (historical — ecs.py now uses scientist names)

| Current name | Former legacy name | Wave fixed |
|-------------|-------------------|------------|
| the specialist engine | the specialist engine | 10 |
| the specialist engine | the specialist engine | pre-audit |
| the specialist engine | the specialist engine | 10 |
| the specialist engine | the specialist engine | 10 |
| the specialist engine | the specialist engine | pre-audit |
| the specialist engine | the specialist engine-Healing | 10 |
| the specialist engine | the specialist engine | 10 |
| the specialist engine | the specialist engine | 10 |
| the specialist engine | the specialist engine | 10 |
| the specialist engine | the specialist engine | 10 |
| the specialist engine | the specialist engine/Vision Input | 10 |
| DS A.G. Bell | the specialist engine | 10 |
| the specialist engine | the specialist engine Sensor | 10 |
| the specialist engine | the specialist engine | 10 |
| DS Röntgen | the specialist engine | 10 |
| the specialist engine | the specialist engine Monitor | 10 |

## Previously Known Bugs (all resolved)

1. ~~Double-prefix "DS DS MacLean"~~ — resolved
2. ~~Creative Cortex duplication~~ — resolved (Andreasen on :port, Da Vinci on :port)
3. ~~Two Bell entries collision~~ — resolved (the specialist engine = Charles on :port, DS A.G. Bell = Alexander on :port)
4. ~~Version drift in dependencies~~ — resolved Wave 8 (66 broken refs fixed)
5. ~~body_system mismatched to DD codes~~ — resolved Wave 11
6. ~~Process flows missing scientist names~~ — resolved Wave 7
7. ~~Engine names using descriptive labels~~ — resolved Wave 10
