# Artios Pattern — Bursty Scale-to-Zero Reference Architecture

Reference architecture extracted from Artios de novo enzyme design
(T-261021-0043; referral lineage sr-c77fa76503; numbers are
Artios-reported, VERITAS CONDITIONAL PASS 75% 2026-10-21). Artios runs
100k-1M design campaigns on Modal with a ~3000-GPU burst ceiling and drove
per-campaign cost from ~$10,000 to ~$500 by declaring hardware PER STAGE
and scaling to zero between campaigns.

## The law this encodes

Idle compute is pure free-energy cost (cost > 0, info gain = 0, F > 0 ->
SKIP). Scale-to-zero makes SKIP the default state; bursts are lawful,
idle is not. Any bursty GPU workload runs as a STAGE LADDER: every stage
declares its own hardware class, concurrency shrinks monotonically down
the ladder, and the whole app costs $0 between campaigns.

## Stage ladder (generalized from enzyme design)

| Stage | Shape | Hardware | Scale |
|---|---|---|---|
| S0 generate | per-item independent | mid GPU (T4/L4) | fan-out to burst ceiling |
| S1 screen | cheap filters | CPU or T4 | widest fan-out, shortest jobs |
| S2 rank | aggregation | small CPU | one container |
| S3 fine model | few survivors, heavy | H100/A100 | narrow fan-out |
| S4 validate | human/wet-lab/adversarial | no GPU | plate-sized fixed batch |

## Runnable skeleton

```python
import modal

app = modal.App("bursty-ladder")

screen_image = modal.Image.debian_slim(python_version="3.11").pip_install("numpy")
fine_image = modal.Image.debian_slim(python_version="3.11").pip_install("torch")

# S1 SCREEN — cheap and widest. CPU-only by declaration, NOT inherited GPU.
@app.function(image=screen_image, cpu=2, timeout=300)
def screen(design: dict) -> float:
    ...  # cheap physics/heuristic score
    return score

# S3 FINE MODEL — narrow and heavy. Big iron only for ranked survivors.
@app.function(
    image=fine_image,
    gpu="H100",
    timeout=3600,
    max_containers=8,            # narrow fan-out, declared as a decision
)
def fine_model(design: dict) -> dict:
    ...  # expensive model on a survivor
    return result

@app.local_entrypoint()
def campaign(designs_json: str = "designs.json"):
    import json
    designs = json.load(open(designs_json))

    # Funnel: S1 at full width (100k-1M items), cheap per item.
    scores = list(screen.map(designs, order_outputs=False))

    # S2 RANK on cheap CPU, then S3 only on the survivors.
    ranked = sorted(zip(scores, designs), key=lambda t: t[0], reverse=True)
    survivors = [d for _, d in ranked[:96]]   # plate-sized batch by construction

    results = list(fine_model.map(survivors))
    return results
```

## Design rules

1. **Per-stage hardware declaration.** `gpu=` (and `cpu=`/`memory=`) chosen
   per stage by measured need. Never inherit the heaviest stage's class.
2. **Scale-to-zero default.** No `min_containers` on bursty functions;
   `container_idle_timeout=60-300` only where latency matters. Between
   campaigns the app costs nothing.
3. **Burst ceiling is a budget decision.** `max_containers` /
   `concurrency_limit` declared per stage, with the burst's dollar cost
   estimated in the campaign spec BEFORE launch (3000 GPUs is a decision,
   not an accident).
4. **Monotone funnel.** Concurrency must shrink down the ladder; if S3 wants
   more containers than S1, the ladder is misdeclared.
5. **Report per campaign, not per hour.** Budget one campaign = one plate /
   one benchmark / one sweep. (Artios: $10k -> $500 per campaign.)
6. **Expensive truth is plate-sized.** The final validation batch is a fixed
   small batch (96 wells), not "whatever fits the budget" — the width ratio
   between cheap screen and expensive test should be 3-4 orders of magnitude.

## Organism tie-ins

- QA fleets: the funnel is clonal selection with an explicit ratio — see
  QA-FLEET-ARCHITECTURE.md section 12a (T-261021-0043).
- Scaffold-then-personalize: backbone-first, sequence-after is the same
  commit-structure-before-parameters rule the organism uses for platform
  scaffolds vs instance personalization.

## Provenance

Ledger T-261021-0043 (kind=build, lane=conduction); principal referral
gpJh3DRJ+gRs8fT4d; playbook:
your-stack/ARTIOS-SCALING-PLAYBOOK-BUILD-T-261021-0043.md. Follow-ups:
GH repo capture (T-261021-0051), cost blog capture (T-261021-0052) —
upgrade numbers to source-grade when they land.
