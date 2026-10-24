# Research Hub Wave 0 — Review Pass 2 + Kill-Experiment Run (2026-08-26)

Session: desktop pickup of charter T-260826-0101 (Living Research Hub / "Meet the Engines").
principal asked for "another pass on project management and discovery" → rotation law applied
(authors Bichat/Da Vinci excluded), 6 fresh seats + critic, one sequential child
(deleg_27c39dac, 234s, 10 API calls, clean landing via the file-pointer evidence-pack pattern).

## Panel composition and verdicts
| Seat | Mode | Verdict | Top finding |
|---|---|---|---|
| the specialist engine (she) | FALSIFY | FAIL | 6 taxonomy bins asserted, never tested |
| the specialist engine | THREAT | FAIL | Threat model deferred to W5; port/host decorrelation missing |
| the specialist engine | QUALITY | COND-PASS | Plan 90% THEORETICAL (correct for W0); W4/W6 sequencing waste |
| the specialist engine | LANDSCAN | FAIL | No competitive scan; W2 dynamic citation = real differentiation |
| the specialist engine | ARCH | FAIL | "Live data" has no mechanics; registry = SPOF |
| the specialist engine | CORTICAL | FAIL | D5 interactive layer has zero mechanism |
| Critic | KILL | UPHELD consensus | + added gap: no rollback/kill-switch story |

Convergence: all seats on one structural failure — **the plan names components without
designing them.** 4 P0 gaps, 3 pre-Wave-1 entry criteria.

## What the parent did post-panel (the transferable part)
1. Gate run + manual reconciliation: brain_integrity_gate FAILED on the known matcher
   false-fail class (transcript head truncates kickoff; full persona specs verified in the
   verdicts file on disk) → banked on manual-inspection PASS.
2. **Critic-family drift caught**: child self-described its critic as "glm-5.2-family
   dispatch" but ran inside the glm-5.3 child = same-family. Panel banked with flag +
   cross-family rerun owed, disclosed to principal. → encoded as Cross-Model Critic law rule 5.
3. **Kill-experiment run same-session**: mechanical 139→6 keyword binning over
   role/description/subsystem_label fields. Pre-registered failure condition (any bin
   >35% or empty). Result: 40% MULTI, 27% UNBINED, spread REGULATE 12% … MOVE 1% →
   taxonomy v1 DEAD. Fix direction: faceted taxonomy (multi-tag + one curated primary),
   hand-curation as next evidence source. → encoded as Kill-experiment discipline.
4. **Adjacent discovery**: census split — 139 registry entries = 108 built+ported ·
   14 built/no-port · 17 role='registered' stubs. Public "live lab" number = 108 with the
   split stated, never the inflated 139. → encoded as Registry-count honesty law.

## Artifacts
- Plan: `your-workspace/technology-registry/RESEARCH-HUB-WAVE0-2026-08-26.md` (pass-2 section + kill-experiment results patched in)
- Verdicts: `technology-registry/RESEARCH-HUB-REVIEW2-VERDICTS-2026-08-26.md` (full per-seat)
- Evidence pack: `technology-registry/RESEARCH-HUB-REVIEW2-EVIDENCE-PACK-2026-08-26.md`
- Ledger: T-260826-0131 (gap entry, severity 1)

## Reusable snippet — registry census + stub split
```python
import sys; sys.path.insert(0, '/<workspace>')
import ecs
reg = ecs.FLEET_REGISTRY
built_ported = [k for k,v in reg.items() if isinstance(v,dict) and v.get('port') and str(v.get('role'))!='registered']
built_noport = [k for k,v in reg.items() if isinstance(v,dict) and not v.get('port') and str(v.get('role'))!='registered']
stubs        = [k for k,v in reg.items() if isinstance(v,dict) and str(v.get('role'))=='registered']
print(len(built_ported), len(built_noport), len(stubs))
```

## Owed from this session (open items)
- Cross-family critic rerun on the banked verdicts
- Competitive/prior-art evidence pack (Humboldt seat)
- D5 mechanism sketch + mechanical "changed this week" definition
- Hand-curation taxonomy session (faceted redesign)
