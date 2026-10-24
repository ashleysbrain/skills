# Cross-Repo Intelligence Map for COO Reviews

The COO advisory board repo (`ds-wave-coo-advisory-panel-private/`) contains stable
context, coach files, and process docs. But it does NOT contain the live operational
state. To produce a substantive review instead of generic advice, pull from these
sources every run.

## Primary Sources (check every run)

### principal Advisory Panel
- **Path**: `/<workspace>`
- **What to look for**: Today's priority stack (ranked), decisions needed from the principal,
  commitment completion status, deferred items and their deadlines
- **Why it matters**: The principal task lattice is the source of truth for what the principal is
  actually working on. If a COO recommendation conflicts with the principal priority stack,
  flag it.

### CTO Advisory Panel
- **Path**: `/<workspace>[date].md`
- **What to look for**: Build blockers (especially stale ones), API contract status,
  CI/CD readiness, infrastructure gaps, engine fleet status
- **Why it matters**: CTO blockers are usually COO coordination problems. A 9-day-stale
  approval is a coordination failure, not just a technical one.

### Fleet Journals (FORGE / ARBITER)
- **Paths**: `hydra-os/intel/agents/journals/FORGE/journal-[date].md`
            `hydra-os/intel/agents/journals/ARBITER/journal-[date].md`
- **What to look for**: Active agent count, top erroring cron jobs (name + error count),
  capability gaps, model assignment issues
- **Why it matters**: Cron jobs with high error counts are zombie commitments. Agent
  fleet bloat is a resource discipline finding (Ruth Porat lane).

### Marketing Content
- **Path**: `hydra-os/intel/marketing/`
- **What to look for**: What launch content has been drafted recently. Check file mod times
  with `ls -lt`.
- **Why it matters**: If marketing has drafted ProductHunt/HackerNews/blog posts but the
  product has no approved build direction or CI/CD, that content is premature. Flag it
  as a sequencing problem (Sheryl Sandberg + Angela Ahrendts lane).

## Secondary Sources (check as relevant)

### Product Project Docs
- **Path**: `/<workspace>`
- **What to look for**: Product specs (e.g., `8D-SLEEP-PROJECT.md`), engine docs,
  architecture overviews
- **Why it matters**: Grounds launch ops recommendations in what actually exists.

### Coaching Engine
- **Path**: `/<workspace>`
- **How to check**: `cd ... && git log --oneline -5`
- **Why it matters**: Confirms what has actually shipped vs what is planned. The git log
  is ground truth for engineering progress.

### Other Advisory Panel Repos
- **Paths**: `ds-wave-product-advisory-panel-private/`, `ds-wave-marketing-advisory-panel-private/`,
  `ds-wave-research-advisory-panel-private/`, `ds-wave-legal-advisory-panel-private/`,
  `ds-wave-design-advisory-panel-private/`, etc.
- **How to check**: `git log --oneline -3` in each to see recent activity
- **Why it matters**: Identifies which boards are active vs stale. A board with no recent
  commits may have gone silent.

## Verification Commands

### Find what changed since last run
```bash
find /<workspace>* -name "*.md" -newer /tmp/coo-review-[previous-date].md \
  2>/dev/null | grep -v ".git/" | head -40
```

### Ground-truth engine count
```bash
ls -d /<workspace>*-engine 2>/dev/null | wc -l
```
Compare against whatever number appears in the CTO report and principal task table.

### Recent git activity across all the specialist engine repos
```bash
for d in /<workspace>*/; do
  echo "--- $(basename $d) ---"
  cd "$d" && git log --oneline -3 2>/dev/null
done
```

### Check engine version stamps
```bash
for f in /<workspace>*-engine/VERSION.md; do
  echo "$(dirname $f | xargs basename): $(head -1 $f)"
done
```

## Common Findings This Methodology Surfaces

1. **Stale blockers**: A P0 item flagged yesterday still unaddressed today. Escalate.
2. **Engine count discrepancies**: 25 vs 28 vs 36 across sources. Reconciliation needed.
3. **Zombie cron jobs**: High error count, still running. Kill recommendation.
4. **Premature marketing content**: Launch posts drafted before product is shippable.
5. **Source-of-truth ambiguity**: Same item marked "completed" in one log, "pending" in another.
6. **Fleet bloat**: Agent count far exceeds productive output. Ruth Porat: cut.
