# Mycorrhizal Network Composition Reference

Condensed domain knowledge from the the specialist engine deep dive (MYCORRHIZAL-NETWORK-DEEP-DIVE.md). For the full document, see the worked example path.

## The 15 Dimensions of the Fungal Medium

### 8 Human Wellness Dimensions

| Dim | Code | Carbon (raw data) | Nitrogen (derived insight) | Phosphorus (physics model) |
|---|---|---|---|---|
| Physical | PHY | sleep, HRV, HR, steps, glucose | recovery, readiness, training load | Landau order parameter |
| Psychological | PSY | mood, stress surveys, therapy notes | resilience, regulation indices | Kuramoto PSY-PHY coupling |
| Intellectual | INT | learning hours, books, courses | knowledge graph depth | Shannon entropy H |
| Social | SOC | interaction frequency, event attendance | connection quality scores | Network centrality |
| Spiritual | SPI | meditation, journaling, nature time | meaning coherence scores | Spiritual order parameter |
| Vocational | VOC | work hours, tasks, milestones | career trajectory metrics | Vocational Landau potential |
| Financial | FIN | income, spending, savings rate | financial health scores | Phase transition (accumulation vs drawdown) |
| Environmental | ENV | location, air quality, home sensors | environmental health indices | Spatial wellness gradients |

### 7 AI Health Dimensions

| Dim | Code | Carbon (raw data) | Nitrogen (derived insight) | Phosphorus (physics model) |
|---|---|---|---|---|
| Computational | CMP | latency, throughput, errors, uptime | performance benchmarks | Computational phase model |
| Data | DAT | ingestion volume, freshness, validation | data quality scores | Shannon entropy of streams |
| Model | MDL | accuracy, calibration, drift | confidence intervals, feature stability | Model phase space (converged vs drifting) |
| Security | SEC | vulnerability counts, patch status, access logs | threat surface assessments | Security order parameter |
| Coupling | CPL | cross-dimensional correlations, cascade times | coherence scores | K_ij matrix itself (reflexive) |
| Evolutionary | EVO | adaptation rate, mutation counts | fitness landscape coverage | Evolutionary regime (exploit vs explore) |
| Resource | RES | memory, compute, storage, energy | efficiency scores | Resource phase state |

## Key Architectural Decisions

### Kin Affinity Weighting
The kin_affinity factor is added to the ensemble weight formula from B2C-RECEPTOR-MODEL.md:
```
w_r proportional to source_trust_r * recency_r * mutual_information_r * kin_affinity_r
```
- kin_affinity = 1.0 for originating B2B
- kin_affinity = 0.3-0.7 for non-kin B2Bs (tunable)
- Decays when originating B2B stops delivering value

### Source-Sink Roles
- the operator agent: ultimate source (physics models, engine updates, immune patches flow DOWN)
- B2B: source AND sink (produces domain intelligence, consumes user outcomes)
- B2C: sink-downward, source-upward (receives intelligence, produces wellness data)
- Products: terminal sink (consume from parent B2C, produce telemetry only)

### Network Topology Evolution
- Phase 1 (0-10 B2Bs): hub-and-spoke, all through the operator agent
- Phase 2 (10-50 B2Bs): mesh formation, lateral B2B exchange
- Phase 3 (50+ B2Bs): mature forest, dense mesh, hub-loss rerouting

### Missing Engine: the specialist engine
No existing engine builds the inter-organism network layer. The gap was identified and a proposed engine (the specialist engine, `ds://gg/engines/mycelia`) was specified. the specialist engine would: build edges, prune edges, route preferentially (kin affinity), monitor CPL dimension fleet-wide, grow toward nutrients (chemotactic), and thicken with maturity (active Metcalfe's law).

Existing engines that are NOT the network layer:
- the specialist engine: placenta (point-to-point, not a network)
- the specialist engine: root hairs (B2C side only, not inter-organism)
- the specialist engine: nutrient extraction (flows THROUGH network, not the network)
- the specialist engine: immune patrol (flows THROUGH network, not the network)

## Four Cargo Classes

| Cargo | Biology | the specialist engine |
|---|---|---|
| Sugars (carbon) | Photosynthate | Validated wellness data points |
| Amino acids (nitrogen) | Protein building blocks | Derived insights and coaching signals |
| Phosphates (phosphorus) | ATP, DNA | Physics model updates (Landau coefficients, coupling constants) |
| VOCs | Airborne signals | Real-time status broadcasts |

## Source Document
`~/your-workspace/ds-wave-gamification-advisory-panel-private/MYCORRHIZAL-NETWORK-DEEP-DIVE.md` (347 lines, authored as the specialist engine)
