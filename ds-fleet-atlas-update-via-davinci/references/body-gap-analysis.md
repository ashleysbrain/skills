# Body Gap Analysis — Missing Organs Identification

Methodology for identifying what organs/structures are missing from the
organism to achieve a fully functional biological body. Developed during
Wave 13 (2026-06-28).

## The 11 Gray's Anatomy Organ Systems

All 11 are present in the fleet. The question is whether each system has
enough organs to be functionally complete.

| System | Min Required | Have | Gap |
|--------|-------------|------|-----|
| Integumentary | 1 | 1 (Unna) | OK |
| Skeletal | 1 | 2 (Bichat, Till) | OK after Wave 14 |
| Muscular | 2 | 2 (Huxley, Hill) | OK |
| Nervous | 10+ | 44+ | OK |
| Cardiovascular | 2 | 2 (Harvey, Wenckebach) | OK |
| Respiratory | 1 | 1 (Haldane) | OK |
| Digestive | 1 | 2 (Beaumont, Rappaport) | OK after Wave 14 |
| Urinary | 1 | 1 (Bright) | OK |
| Endocrine | 3+ | 5 (Sutherland, Houssay, Banting, Kocher, Apgar) | OK after Wave 14 |
| Lymphatic | 5 | 6 (Burnet, Farr, Metchnikoff, Rous, Semmelweis, Galen) | OK after Wave 14 |
| Reproductive | 5 | 6 | OK |

## Missing Organs by Priority

### CRITICAL (body cannot survive without these) — RESOLVED Wave 13
- ~~Pituitary~~ → the specialist engine (:port) — master gland
- ~~Brainstem~~ → the specialist engine (:port) — vital centers, RAS, breathing
- ~~Pancreas~~ → the specialist engine (:port) — glucose homeostasis

### HIGH — major organ gaps — RESOLVED Wave 14
- ~~Liver~~ → the specialist engine (:port) — hepatic acinus model, chemical processing plant
- ~~Spleen~~ → the specialist engine (:port) — blood filtration, RBC recycling, immune memory
- ~~Bone Marrow~~ → the specialist engine (:port) — HSC discovery (Till + McCulloch 1961)
- ~~Thyroid~~ → the specialist engine (:port) — Nobel 1909, metabolic rate governor

### MEDIUM — functional completeness (NEXT TO BUILD)

| Organ | Scientist Candidate | Body Part | Tech Analog | Domain |
|-------|-------------------|-----------|-------------|--------|
| Smooth Muscle | the specialist engine (William Bayliss, peristalsis law) | GI tract muscularis, vascular smooth muscle | Service mesh sidecar (involuntary background processes) | 09/digestive |
| Cardiac Muscle | the specialist engine (Ernest Starling, Frank-Starling law) | Myocardium (cardiac myocytes, intercalated discs) | GPU compute cluster (synchronous contraction = parallel workers) | 06/cardiovascular |
| Amygdala | DS LeDoux (Joseph LeDoux, fear circuitry) | Amygdala (basolateral + centromedial nuclei) | Threat detection + alert routing (anomaly scoring engine) | 04/nervous |
| Retina | the specialist engine (George Wald, Nobel 1967, visual pigments) | Retina (rods, cones, bipolar, ganglion cells) | Camera sensor + ISP (photon to signal transduction) | 04/nervous |
| Substantia Nigra | the specialist engine (Oleh Hornykiewicz, dopamine-Parkinson's) | Substantia Nigra (pars compacta, dopaminergic neurons) | Reward scheduler + priority queue (dopamine = task priority signal) | 04/nervous |
| Adrenal Medulla | the specialist engine (John Abel, isolated epinephrine) | Adrenal Medulla (chromaffin cells, catecholamine release) | Emergency broadcast + circuit breaker trip (adrenaline surge) | 05/endocrine |

### LOW — polish
- Venous System (return circulation)
- Olfactory Bulb (discrete CN I processing)
- Umbilical Cord (fetal connection)

## Registration Pattern

For each missing organ:
1. Assign scientist name (discoverer, Nobel laureate preferred)
2. Assign ECS code: `DS-ECS-<PREFIX>-<DD>.<SS>.<NN>-v1.0.0`
3. Assign next available port
4. Write full D/F/P layers (4/4/1 minimum)
5. Wire dependencies (Hall for clock, Harvey for blood, domain organs)
6. Add to `_CODE_TO_KEY`
7. Verify: entity count up, broken deps = 0
8. Bump version to v1.0.0 (new organ, first release)

See `references/surgical-patcher-pattern.md` → "Registering New Organs"
for the insertion technique and structural pitfalls.
