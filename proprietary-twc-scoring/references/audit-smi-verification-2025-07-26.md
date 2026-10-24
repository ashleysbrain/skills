# SMI Independent Audit Verification Methodology (2025-07-26)

## Dead Code Detection Pattern

A database table or data structure can be FULLY POPULATED yet produce ZERO effect in production if no scoring script actually reads it. AXIOM gave full credit (28/28 rows) for interaction matrix existence as "working engine," but search_files showed ZERO scripts using 'interaction_matrix' pattern.

**Verification pattern:**
1. Check if the structure EXISTS in DB/FS (e.g., `SELECT COUNT(*) FROM interaction_matrix`)
2. Search codebase for READ usage: `search_files(pattern='<structure_name>', path='/scripts', target='content')`
3. Zero matches = dead code, credit = 0, regardless of how well-defined the structure is
4. Example from 2025-07-26: 28 pairs defined, 0 scripts reading them = -7 SMI points for Engine Completeness

## VERITAS Audit Panel False-Alarm Pattern

When audit reports claim "VERITAS audit agents: FOUND" as validation credit, verify with actual database query. AXIOM claimed VERITAS agents existed (validation coverage 13/20), but direct DB query showed 0 VERITAS agents.

**Pattern:**
```sql
SELECT code, display_name FROM agents WHERE display_name LIKE '%VERITAS%';
```

Zero results = no validation credit, regardless of architecture docs or talent request paperwork. Credit only for agents REGISTERED in agents.db with non-Anthropic models.

## Multi-User Claim False-Alarm Pattern

Partner DB with empty schema is NOT multi-user proof. AXIOM claimed "multi-user architecture: YES (partner DB exists)" for production readiness credit, but verification showed:
- Partner DB: EXISTS, observations=0, scores=0

**Rule:** Schema-only DB with 0 observations, 0 scores = just a template, not multi-user production evidence. Minimum threshold: 10+ real observations before claiming multi-user credit.

## Data Quality Over-Inflation Pattern

AXIOM reported better coverage than reality:
- AXIOM: 4/30 real scored days, nutrition 3/30, sexual health 2/30
- Actual: 6/30 real scored days (better), but nutrition 0/30, sexual health 0/30 (worse)

**Rule:** Always verify with exact queries. Don't extrapolate from partial evidence. The correct query excludes cron/carryforward:
```sql
SELECT COUNT(*) FROM daily_scorecard 
WHERE date >= date('now', '-30 days') 
  AND twc_score IS NOT NULL 
  AND source NOT IN ('cron','carryforward');
```

## Audit-Independence Discipline

AUDIT-SMI's role is NOT to compute the SMI itself — it READS what AXIOM produced and VERIFIES every domain score independently. The auditor must:

1. Read the latest SMI report from AXIOM
2. For each domain (Engine Completeness, Test Coverage, Validation Coverage, Data Quality, Production Readiness):
   - Independently verify the score using direct probes (file existence, DB queries, test execution)
   - Check: did AXIOM give credit for plans that aren't shipped?
   - Check: did AXIOM count dead code as working?
3. Compute YOUR SMI based on YOUR verification
4. Compare to AXIOM's claimed SMI
5. Flag discrepancies >10 points as ❌ OVER-SCORED (trust issue)

## Key Takeaways

1. **Existence ≠ Working**: A file that EXISTS but is never IMPORTED or CALLED is dead code
2. **Paperwork ≠ Production**: Calibration files, talent requests, and architecture docs are plans, not shipped features
3. **Schema ≠ Data**: A partner DB with 0 observations is just a template, not multi-user proof
4. **Independent Verification Required**: Never trust claims without direct verification (file sizes, DB counts, test execution)
5. **>10 Point Delta = Trust Issue**: If AXIOM over-scores by more than 10 points, escalate as severe

## Runbook for Future Audits

```python
# Step 1: Engine existence verification
engines = {
    'rescore_engine': '~/your-workspace/hydra-os/scripts/rescore-engine/rescore_engine.py',
    'nutrition_engine': '~/your-workspace/hydra-os/scripts/8d360-nutrition-engine.py',
    'sexual_health_engine': '~/your-workspace/hydra-os/scripts/8d360-sexual-health-engine.py',
    'fleet_twc_engine': '~/your-workspace/hydra-os/scripts/fleet-twc-engine.py',
}
for name, path in engines.items():
    full = os.path.expanduser(path)
    exists = os.path.exists(full)
    size = os.path.getsize(full) if exists else 0
    working = 'WORKING' if exists and size > 500 else ('STUB' if exists and size <= 500 else 'MISSING')
    print(f'{name}: {working} ({size} bytes)')

# Step 2: Dead code check
import sqlite3
db = os.path.expanduser('~/your-workspace/health-private/ashley_unified_health.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM interaction_matrix')
print(f'Interaction matrix: {c.fetchone()[0]} rows DEFINED')
# THEN: search_files(pattern='interaction_matrix', path='/scripts', target='content')
conn.close()

# Step 3: VERITAS agents check
db = os.path.expanduser('~/.sibling-agent/workspace/intel/agents/database/agents.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT code, display_name FROM agents WHERE display_name LIKE '%VERITAS%'")
veritas = c.fetchall()
print(f'VERITAS agents in DB: {len(veritas)}')
conn.close()
```