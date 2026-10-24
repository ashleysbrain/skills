# Deep Audit Methodology for Assessment Scoring Engines

After building the scoring engine and before declaring it done, run this
systematic audit. Each test catches a different class of bug.

## 1. Item Bank Completeness

```python
item_ids = [i['id'] for i in ITEM_BANK]
assert len(item_ids) == 120                          # expected count
assert len(set(item_ids)) == len(item_ids)           # no duplicates
expected = {f'I{i:03d}' for i in range(1, 121)}
assert set(item_ids) == expected                     # no missing/extra IDs
```

## 2. Facet Coverage

```python
facets_in_bank = set(i['facet'] for i in ITEM_BANK)
assert facets_in_bank == set(FACETS.keys())          # all facets represented
from collections import Counter
items_per_facet = Counter(i['facet'] for i in ITEM_BANK)
assert all(v == 4 for v in items_per_facet.values()) # each facet has exactly 4
```

## 3. Domain Coverage

```python
assert len(set(i['domain'] for i in ITEM_BANK)) == 5  # 5 domains
items_per_domain = Counter(i['domain'] for i in ITEM_BANK)
assert all(v == 24 for v in items_per_domain.values()) # 24 items per domain
```

## 4. Key Distribution

```python
keys = Counter(i['key'] for i in ITEM_BANK)
assert all(k in ('+', '-') for k in keys)             # no invalid keys
# For IPIP-NEO-120: expect ~65 forward, ~55 reverse
```

## 5. Scoring Math Verification

### Forward scoring
```python
item_plus = [i for i in ITEM_BANK if i['key'] == '+'][0]
assert score_item(item_plus, 5) == 5.0   # response 5 -> score 5
assert score_item(item_plus, 1) == 1.0   # response 1 -> score 1
```

### Reverse scoring
```python
item_minus = [i for i in ITEM_BANK if i['key'] == '-'][0]
assert score_item(item_minus, 5) == 1.0  # response 5 -> score 1 (6-5)
assert score_item(item_minus, 1) == 5.0  # response 1 -> score 5 (6-1)
```

### Out of range rejection
```python
try:
    score_item(item_plus, 6)
    assert False, "Should have raised"
except ValueError:
    pass
```

## 6. Perturbation Test (Most Important)

Change ONE item response and verify its facet score changes. This catches
disconnected items — a bug where an item exists in the bank but doesn't
actually influence scoring.

```python
responses_base = {i['id']: 3 for i in ITEM_BANK}
base = score_all(responses_base)

test_item = ITEM_BANK[0]
responses_perturbed = responses_base.copy()
responses_perturbed[test_item['id']] = 5
perturbed = score_all(responses_perturbed)

base_facet = [f for f in base['facets'] if f['facet_code'] == test_item['facet']][0]
pert_facet = [f for f in perturbed['facets'] if f['facet_code'] == test_item['facet']][0]

assert abs(pert_facet['mean'] - base_facet['mean']) > 0, "Item disconnected!"
```

## 7. Boundary Profiles

### All-5s (maximum agreement)
Score with all responses = 5. Each domain should produce expected scores
(accounting for reverse keying — reverse-keyed items scored as 6-5=1).

### All-1s (minimum agreement)
Score with all responses = 1. Should produce inverse of all-5s.

### All-3s (neutral)
Should produce all domain means = 3.0, all percentiles = 50%.

## 8. Domain Aggregation Cross-Check

Manually compute domain means from facet means and compare to API output:

```python
for dcode in ['N', 'E', 'O', 'A', 'C']:
    facet_means = [f['mean'] for f in base['facets'] if f['domain'] == dcode]
    manual = sum(facet_means) / len(facet_means)
    api = [d for d in base['domains'] if d['domain_code'] == dcode][0]['mean']
    assert abs(manual - api) < 0.001
```

## 9. Facet-Domain Mapping Consistency

Verify each item's domain field matches the facet's domain in FACETS:

```python
for item in ITEM_BANK:
    assert FACETS[item['facet']]['domain'] == item['domain']
```

## 10. Suspicious Item Verification

Items where the key direction seems to contradict the wording are NOT bugs.
The construct defines the direction:

- **Neuroticism forward items** measure distress: "Worry about things" [+] is
  correct because worry IS high neuroticism. The negative wording is the
  construct, not a sign of reverse keying.
- **Agreeableness reverse items** measure antagonism: "Love a good fight" [-]
  is correct because fighting is LOW agreeableness.
- **Extraversion reverse items** measure passivity: "Like to take it easy" [-]
  is correct because passivity is LOW extraversion.

Never auto-detect key direction from text. Use the published scoring key.
A negation heuristic will mislabel these correctly-keyed items as errors.

## 11. Percentile Mapping Verification

```python
assert score_to_percentile(3.0) == 50.0   # midpoint
assert score_to_percentile(5.0) > 95.0    # high
assert score_to_percentile(1.0) < 5.0     # low
```

## 12. Scoring Method Verification (sum vs mean)

The most commonly skipped check. Verify your scoring METHOD against the
primary source, not just the keying direction.

1. Fetch the official scoring instructions from the source site.
2. Document whether the source says SUM or MEAN.
3. If using MEAN (for percentile norms), also report SUM in the explanation.
4. Add a percentile approximation disclaimer.
5. Include the verbatim official instruction text in the explanation endpoint.

See `references/scoring-methodology-verification.md` for the full protocol.

```python
# Verify both scoring methods produce consistent personality readings
facet_sum = sum(item_scores)
facet_mean = facet_sum / len(item_scores)
# These are linear transforms: mean = sum / n_items
# Both should produce the same percentile if norms are on the right scale
```

## Audit Output Template

```
======================================================================
DEEP AUDIT: <Tool Name>
======================================================================

1. ITEM BANK COMPLETENESS      : PASS (120 items, 0 duplicates, 0 missing)
2. FACET COVERAGE              : PASS (30 facets, all have 4 items)
3. DOMAIN COVERAGE             : PASS (5 domains, 24 items each)
4. SCORING KEY DISTRIBUTION    : PASS (65 forward, 55 reverse)
5. SCORING MATH                : PASS (forward/reverse/out-of-range)
6. ITEM INFLUENCE (perturb)    : PASS (delta = 0.5)
7. BOUNDARY PROFILES           : PASS (all-5s, all-1s, all-3s verified)
8. DOMAIN AGGREGATION          : PASS (manual == API for all 5 domains)
9. FACET-DOMAIN CONSISTENCY    : PASS (0 inconsistencies)
10. SUSPICIOUS ITEMS           : 9 flagged, ALL verified correct by design
11. PERCENTILE MAPPING         : PASS (sensible across 1.0-5.0 range)
======================================================================
```

## Verified Audit Run

Full audit executed 2026-08-06 against IPIP-NEO-120 scoring engine.
All 11 checks passed. The 9 suspicious items were verified correct against
the IPIP standard (Neuroticism forward items measure distress, which is
the high-N end of the construct).
