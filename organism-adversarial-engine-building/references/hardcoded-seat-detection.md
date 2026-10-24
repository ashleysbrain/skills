# Hardcoded-Seat Detection Recipe

Caught 2026-08-12 by three independent QA auditors (Popper, Lyapunov, Eccles)
across ATK-01 and ATK-03. This is a recurring class of defect — a seat that
returns a constant score regardless of input, defeating the adversarial panel.

## Signature

```python
# BAD — hardcoded placeholder that shipped to production
value_chain_seat = SeatVerdict(
    seat=SeatName.VALUE_CHAIN.value,
    assessment="Value chain assessed from primary and support activities",
    score=0.5,  # <-- constant, ignores all input
)
```

The seat *looks* implemented (it has an assessment string, an enum name, a score),
so a surface review passes it. Only an input-differential test catches it.

## Detection (mandatory after every multi-seat engine build)

Send ≥2 inputs that should produce **different** seat scores and assert the
scores differ. Run this from the engine's server:

```python
import requests

# Input A: minimal/empty — should score low
r_a = requests.post("http://localhost:port/v1/analyze",
                    json={"value_chain": {}}).json()
# Input B: rich — all activities strong — should score high
r_b = requests.post("http://localhost:port/v1/analyze",
                    json={"value_chain": {
                        "inbound logistics": 0.9, "operations": 0.9,
                        "outbound logistics": 0.9, "marketing": 0.9,
                        "service": 0.9, "procurement": 0.9,
                        "technology": 0.9, "human resources": 0.9,
                        "infrastructure": 0.9,
                    }}).json()

def seat_score(result, seat_name):
    for s in result["seats"]:
        if s["seat"] == seat_name:
            return s["score"]
    return None

vc_a = seat_score(r_a, "Value Chain Analysis")
vc_b = seat_score(r_b, "Value Chain Analysis")
assert vc_a != vc_b, f"HARDCODED SEAT: Value Chain returns {vc_a} for both inputs"
print(f"PASS: Value Chain varies ({vc_a} -> {vc_b})")
```

If the assertion fails, the seat is hardcoded. The fix is always: derive the
score from the input data (coverage × quality, magnitude × consistency, etc.).

## Where it tends to hide

Seats added late as placeholders ("I'll compute this later") that never get
revisited. In the 2026-08-12 case:

- **ATK-01**: Value Chain + Market Positioning (both returned 0.5) — genuinely hardcoded, later fixed
- **ATK-03**: Munger Lollapalooza (returned constant 0.3) — genuinely hardcoded, fixed in round 4
- **ATK-03**: Lynch Growth Moat — **FALSE POSITIVE** (see "Wrong-Input-Category False Positive" below)

These are the "last two seats" in each engine — the ones added to round out the
5-seat panel after the first three got real implementations.

## Wrong-Input-Category False Positive (caught 2026-08-12, 4th audit)

**Critical pitfall for auditors:** A seat can *appear* hardcoded when you test
it with the wrong category of inputs. ATK-03's Lynch Growth Moat was flagged as
"returns 0.300 regardless of input" in the 3rd audit because the auditor only
varied `brand` and `switching_costs`. But Lynch is a *growth* investor — his
seat responds to `growth_rates`, `earnings_growth`, `revenue_growth`, and
`same_store_sales`, not brand metrics. When tested with actual growth inputs,
the score ranges 0.083→0.952.

**Rule:** Before declaring a seat hardcoded, check the seat's function signature
to identify which parameters it actually reads. Test with inputs that map to
THOSE parameters. A seat that appears static under one input category may vary
correctly under its intended input category.

**Verification pattern:**
1. Read the seat's compute function (e.g. `analyze_lynch_growth_moat`)
2. Identify which parameters it reads (e.g. `growth_rates`, `earnings_growth`)
3. Send two inputs that differ ONLY in those parameters
4. Assert the scores differ
5. If they don't differ, THEN declare it hardcoded

## Prevention rule

A stub seat must crash loudly (`raise NotImplementedError`) or omit the score
field. Never silently return 0.5 — it passes every unit test that doesn't do
input-differential testing, and it looks intentional to a reviewer.
