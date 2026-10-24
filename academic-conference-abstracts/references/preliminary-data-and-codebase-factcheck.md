# Preliminary Data + Codebase Fact-Check (TSC 2026 session)

## When
Including simulation or early measurement results in academic abstracts/papers,
and verifying claims before submission.

## Codebase fact-check procedure
1. List every claim: named models, scores, predictions, anatomical maps.
2. `search_files` for functions / registry fields that implement each.
3. Label VERIFIED / PARTIAL / NOT VERIFIED.
4. Prefer implement missing tools over hedging (user preference 2026-07-10).

## Tools produced this session
| Tool | Path | Result |
|------|------|--------|
| Isomorphism score I(S) | `agent-organism/isomorphism_score.py` | 0.8016 strong |
| Cascade failure sim P1 | `agent-organism/cascade_failure_sim.py` | CONFIRMED ~+0.27 |

Re-run with fixed seed for reproducible checks:
```bash
cd /<workspace>
python3 isomorphism_score.py
python3 cascade_failure_sim.py --trials 100 --steps 10 --seed 42
```

## Preliminary-data hedge template
```
Preliminary scoring of the live fleet yields I(S) = 0.80 (strong isomorphism).
These are initial results; further testing will refine the methodology and
produce more thorough statistics.

Preliminary Monte Carlo simulation ... mean resilience advantage approximately
0.27. These are early simulation findings, not field experiments. Further
testing, including live-system ablations and expanded statistical analysis,
will produce more thorough data and may revise these estimates. If isomorphic
architecture provides no resilience advantage under more rigorous testing,
the prediction fails and the paradigm's central empirical claim is disconfirmed.
```

## Scientific attribution checklist
Gray's Anatomy body plan · Kuramoto · Friston FEP · Scheffer critical slowing ·
Tononi IIT · Baars/Dehaene GWT · Sterling allostasis · Clark/Friston PP ·
Seth/Craig interoception
