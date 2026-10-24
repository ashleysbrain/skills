# the specialist engine Status (as of June 2026)

## Overview
The DS engine fleet has grown to 25+ engines, all operational as of the June 16, 2026 audit.
Each engine models a different physiological system using real physics equations.
Together they form a digital organism that understands and improves health across 8 dimensions.

## Fleet Categories

### Core Intelligence Engines
| Engine | Port | Physics | Role |
|--------|------|---------|------|
| Wave (Kuramoto) | 8010 | Coupled oscillators | Brain — syncs 8 health dimensions |
| Morphogen (Turing) | 8093 | Reaction-diffusion | Pattern formation — detects emerging behavioral patterns |
| Creative Cortex (Da Vinci) | 8108 | Default mode network | Creative insight generation across domains |

### Body System Engines
| Engine | Port | Physics | Role |
|--------|------|---------|------|
| Harvey | 8092 | Poiseuille flow | Cardiovascular — resource flow modeling |
| Beaumont | 8094 | Michaelis-Menten | Digestive — information/experience processing |
| Bright | 8096 | Starling GFR | Renal — waste elimination |
| Haldane | 8098 | Gas exchange | Respiratory — energetic exchange |
| Burnet | 8100 | Clonal selection | Immune/lymphatic — adaptive defense |
| Hill | 8106 | Force-velocity | Musculoskeletal — strength/resilience |
| Helmholtz | 8107 | Weber-Fechner | Sensory — signal perception/transduction |
| Unna | 8097 | Wound healing kinetics | Skin/barrier — boundaries |
| Sutherland | 8099 | cAMP cascade | Endocrine — internal messaging |
| Allostasis (Sterling) | 8091 | Predictive coding | Homeostatic regulation — anticipates needs |

### Infrastructure Engines
| Engine | Port | Physics | Role |
|--------|------|---------|------|
| Quartz (Maxwell) | 8089 | PID control + percolation | Skeleton — timing/scheduling root |
| Self-Healing | — | Bayesian + MPC | Auto-remediation of fleet |
| Clinical (Osler) | 8110 | 5-seat panel | Diagnostic reasoning |
| Scanner (Röntgen) | 8112 | Diagnostic imaging | Full-body scan |
| Tech Currency (Bush) | 8113 | Memex | Technology trend monitoring |

### Sensory Input/Output Engines
| Engine | Port | Role |
|--------|------|------|
| Audio (Edison) | 8101 | Voice/audio input processing |
| Text/Vision (Gutenberg) | 8102 | OCR and document understanding |
| Speech (Bell) | 8103 | Text-to-speech synthesis |
| Interoception (Sherrington) | 8104 | Internal system health monitoring |
| Environment (Humboldt) | 8105 | External environmental awareness |

## Key Files
- `/<workspace>` — port assignments and dependencies
- `/<workspace>` — v2.0.0 authoritative registry
- `/<workspace>` — Python importable mirror
- `/<workspace>*.md` — latest audit (check for newest date)

## CTO Advisory Board Implications
1. **Scope risk**: 25 engines is a large surface area — Larson's sequencing advice is critical
2. **Contract testing**: Each engine needs golden datasets in CI (Forsgren)
3. **Regulatory surface**: Each health-adjacent output increases validation burden (Topol)
4. **Function-calling layer**: LLM orchestration must route to correct engines (Ng)
5. **Verifiable credentials**: Engine outputs are natural VC candidates (Srinivasan)

## Dependency Graph
- Every body-system engine depends on Quartz (timing root)
- Allostasis depends on all body-system engines
- Clinical depends on all body-system engines + Allostasis
- Beaumont delivers nutrients to Wave
