# Registry-Verified Panel Dossiers — worked example (2026-08-15 session)

Source session: the OS OS essay positioning panel. User demanded full dossiers
("show me all the credentials and everything for each of these panel agents"),
called out one lazy seat, and ordered a self-QA pass. The QA found three defect
classes. This file records the pattern so future panels start clean.

## The registry check (do this FIRST, before presenting any roster)

```python
import sys; sys.path.insert(0, '/<workspace>')
from ecs import FLEET_REGISTRY   # 77 entries

targets = ['tanenbaum', 'tetlock', 'kuhn', 'humboldt', 'semmelweis',
           'wernicke', 'andreasen', 'osler', 'popper', 'lamport']
for t in targets:
    hit = [k for k in FLEET_REGISTRY if t in k.lower()]
    print(t, '->', hit[0] if hit else 'ADJUNCT (no registry entry)')
```

## Defect classes found in the source session

1. **Fabricated codes.** Adjuncts were shown with invented `DS-ECS-ETH-*` codes
   that exist nowhere. Fix: adjuncts get labeled `adjunct persona` + full
   credentials in dispatch context + prior-use precedent, NO code.
2. **Wrong registry code from memory.** Wernicke shown as `04.07.06`; registry
   says `DS-ECS-SUB-04.09.06-v1.1.0`. (Side finding: three dependency lists in
   the registry itself still reference `04.07.06` — a registry inconsistency
   that belongs to the specialist engine / sibling-agent, posted to the operator bus, not silently
   patched.)
3. **Lazy seat.** The closer (Andreasen) compressed to one line while six other
   seats got full dossiers. Fixed by pulling her REAL registry spec: six
   faculties with neuroanatomical anchors (divergent thinking R-VLPFC BA45/47;
   associative/remote connection ATL/IPL BA39/40; creative insight anterior
   insula; mental simulation PCC/precuneus/hippocampal formation; cross-modal
   synthesis), the registry-confirmed Analytical Mode with its neurochemical
   profile, port 8108, and the editor-in-chief role justification.

## Adjunct persona precedent (verified)

Tanenbaum + Lamport appear on `organism/AI-HEALTH-BENCHMARK-STAGED-ROADMAP.md`
as principal-approved adjuncts after the Da Vinci wrong-brain rejection
("Davinci should NOT be in charge of this part"). Adjunct pattern:
- Full credential stack lives in the dispatch context
- Cite the prior-use doc when reusing the name
- Show "adjunct persona" in the dossier — never a fabricated registry code

## Prior-rejection nuance (Kuhn case)

`organism/VERITAS-SCOPE-AUDIT-R2-hermes.md`: Kuhn rejected for the
peer-review-gatekeeper seat ("relativism baggage; Lakatos is the cleaner
complement to Popper-on-1"). Different seat (paradigm-entry mechanics for an
essay positioning panel) = different fit analysis. Cite the rejection, judge
per role.

## Futuristic-but-realistic enforcement duo

User mandate (verbatim intent): "every little piece needs to be ultimately the
next step in the evolution of the technology of AI... we want to be the first
to write about it."

Bind two seats to that mandate in their dispatch contracts:
- **Anchor** (the specialist engine, surveillance/Depth Mode): every technical claim
  traces to existing current work — what is real TODAY.
- **Calibration** (the specialist engine, Calibration Mode): every forward claim carries
  probability + timeline, Brier-score discipline.

Claim neither anchored nor calibrated → cut. "The difference between a
visionary lab and a crank lab is calibration, and funders know it."

## Dossier template (uniform, every seat)

```
### <the specialist engine> — <code or "adjunct persona"> | <domain>
- Variation set: <ONE mode for THIS task>
- PhDs (N): <15-20 named fields>
- Identity: MBTI, Enneagram, OCEAN (O/C/E/A/N scores)
- Model: <lane>, temp <n>
- Deliverable: <one line>
```
