# agents.db Schema Reference

## agents Table

The primary table for fleet registration. Schema discovered via `.schema agents`.

### Key Columns

| Column | Type | Notes |
|--------|------|-------|
| `code` | TEXT UNIQUE | Full code: `DOMAIN-FAMILY-SPECIALTY-LEVEL-CREDENTIAL_TIER-PERSONALITY_CODE-TRAINING_TIER-SEQUENCE` |
| `short_code` | TEXT | Short reference: `FAMILY-SPECIALTY-SEQUENCE` |
| `display_name` | TEXT | Codename only (e.g., "DS ORGANIZER"). NEVER use "Dr." prefix. |
| `cosmic_name` | TEXT | Poetic/phenomenon name (e.g., "The Event Horizon of Execution") |
| `emoji` | TEXT | Single emoji identifier |
| `domain` | TEXT NOT NULL | RES, ENG, MKT, OPS, FIN, LEG, CRE, PGM, EXE, BD, PER, GD, DS, EMP |
| `family` | TEXT NOT NULL | RSR, REV, ANL, WRT, DEV, DSN, MGR, SPC, LED, DIR, CHF, AST, DSP, QA, ORG, HOR |
| `specialty` | TEXT | NEU, CON, PSY, 8DA, 8DH, EF, ARC, GEN, OPS, etc. |
| `level` | INTEGER 1-7 | Agent seniority/complexity tier |
| `credential_tier` | INTEGER 0-5 | Depth of credential stack |
| `personality_code` | TEXT | P01, P02, etc. |
| `training_tier` | INTEGER 1-5 | Training investment level |
| `sequence` | INTEGER | Unique ID within specialty |
| `role` | TEXT | Job title (e.g., "principal Task & Time Management Guardian") |
| `world` | TEXT | CHECK constraint: 'Empire', 'DS', 'GD', 'Personal', 'your-org', 'qubit-health', 'goddess-divinity', 'principal-personal', 'empire' |
| `primary_model` | TEXT | e.g., 'anthropic/claude-sonnet-4-6' |
| `status` | TEXT | 'active', 'inactive', 'archived', 'suspended' |
| `reports_to` | TEXT | display_name of supervisor agent |
| `bio` | TEXT | Agent description |

### Code Format Construction

The `code` column follows this pattern:
```
DOMAIN-FAMILY-SPECIALTY-LEVEL-CREDENTIAL_TIER-PERSONALITY_CODE-TRAINING_TIER-SEQUENCE
```

Example: `EXE-ORG-EF-L6-C5-P1-T4-001`
- Domain: EXE (Executive)
- Family: ORG (Organizer)
- Specialty: EF (Executive Function)
- Level: 6
- Credential Tier: 5
- Personality Code: P1
- Training Tier: 4
- Sequence: 001

### Existing Agent Examples

| Code | Display Name | Domain | Family | Specialty | Level |
|------|-------------|--------|--------|-----------|-------|
| EXE-LED-OPS-L7-C5-P3-T5-001 | DS NEBULA | EXE | LED | OPS | 7 |
| ENG-LED-ARC-L7-C4-P3-T4-001 | DS FORGE | ENG | LED | ARC | 7 |
| EMP-HOR-GEN-L4-C3-P3-T3-001 | DS HORIZON | EMP | HOR | GEN | 4 |

### Registration Command (Simple)

For inserts with no JSON array columns:

```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db \
  "INSERT INTO agents (code, short_code, display_name, cosmic_name, emoji, domain, family, specialty, level, credential_tier, personality_code, training_tier, sequence, role, department, world, bio, primary_model, reports_to, status, hire_date) VALUES ('CODE', 'SHORT', 'NAME', 'Cosmic Name', 'emoji', 'DOMAIN', 'FAMILY', 'SPEC', LEVEL, CTIER, 'PCODE', TTIER, SEQ, 'Role', 'dept', 'world', 'Bio text', 'model', 'REPORTS_TO', 'active', 'YYYY-MM-DD');"
```

### Registration Command (With JSON Arrays)

When the `skills`, `constraints`, or `specializations` columns contain JSON arrays, the direct `sqlite3` command fails due to shell quoting conflicts with `[]` and `""`. Use an intermediate SQL file:

```bash
cat > /tmp/insert_agent.sql << 'SQLEOF'
INSERT INTO agents (code, short_code, display_name, emoji, domain, family, specialty,
  level, credential_tier, personality_code, training_tier, sequence, display_name,
  role, department, world, bio, skills, constraints, specializations,
  primary_model, fallback_model, temperature, max_tokens, reports_to,
  direct_reports, status, hire_date)
VALUES (
    'OPS-COM-COM-L7-C5-P3-T5-001',
    'COM-001',
    'DS ISING',
    '',
    'OPS',
    'COM',
    'COM',
    7, 5, 'P3', 5, 001,
    'DS ISING',
    'Community Management Agent',
    'empire',
    'your-org',
    '',
    'Bio text here.',
    '["community-management", "member-engagement"]',
    '[]',
    '[]',
    'anthropic/claude-sonnet-4-6',
    'anthropic/claude-haiku-4-5',
    0.7, 4096,
    'EXE-CHF-ALL-L7-C5-P3-T5-001',
    '[]',
    'active',
    '2026-06-10'
);
SQLEOF
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db < /tmp/insert_agent.sql
rm /tmp/insert_agent.sql
```

**Why the intermediate file:** The `<< 'SQLEOF'` heredoc prevents shell expansion of `$` and backticks inside the SQL, while the file redirect avoids quoting the entire SQL as a single string argument. This is the only reliable pattern for JSON arrays in VALUES clauses.

### Verify Registration

```bash
sqlite3 ~/.sibling-agent/workspace/intel/agents/database/agents.db \
  "SELECT code, display_name, role, specialty, status, primary_model FROM agents WHERE display_name='NAME'"
```

### Common Pitfalls

- **No `codename` column.** Use `display_name` for the agent name, `code` for the structured identifier.
- **`world` column has CHECK constraint.** Only these values are valid: 'Empire', 'DS', 'GD', 'Personal', 'your-org', 'qubit-health', 'goddess-divinity', 'principal-personal', 'empire'. Using anything else causes a constraint failure.
- **New specialties need a new `specialty` value.** Check existing values with: `SELECT DISTINCT specialty FROM agents WHERE specialty IS NOT NULL`
