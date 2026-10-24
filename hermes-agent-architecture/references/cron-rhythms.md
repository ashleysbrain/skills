# Cron Rhythms as Biological Clocks

Each body system profile runs on its own biological timescale. Cron jobs are the circadian/ultradian clocks.

## Per-Profile Cron Configuration

### CNS (Wave Engine) — Event-Driven (Sensory)
```bash
# No recurring cron. Triggered by:
# - Telegram messages (via orchestrator → Kanban)
# - User-initiated sessions
# - Kanban task assignment
```
**Rationale:** Brain/CNS reacts to stimuli. Continuous polling wastes energy.

### Autonomic (Quartz Engine) — Ultradian (5 min)
```bash
# PID control loop, lattice maintenance, task regulation
hermes -p autonomic cron create "*/5 * * * *" \
  --prompt "Run Quartz lattice PID control cycle. Check task queue, regulate active tasks, maintain homeostasis. Report anomalies." \
  --skills kanban-worker \
  --name "Autonomic Ultradian Cycle"
```
**Rationale:** Autonomic nervous system runs continuous regulatory loops (heart rate, digestion, homeostasis). 5-min ultradian rhythm matches PID control needs.

### Endocrine (Seed Engine) — Circadian Daily (03:00)
```bash
# Growth, evolution, Avrami JMAK phase transitions, SOC, CPM
hermes -p endocrine-immune cron create "0 3 * * *" \
  --prompt "Run Endocrine daily growth cycle. Execute Avrami JMAK phase transition checks, Landau free energy minimization, SOC criticality assessment, CPM pattern formation. Update growth trajectories. Report developmental milestones." \
  --skills aisha-md-health-scoring-cron-execution \
  --name "Endocrine Circadian Growth"
```
**Rationale:** Endocrine system (growth hormone, cortisol, melatonin) peaks at night. 3 AM aligns with human growth hormone secretion.

### Immune (Allostasis Engine) — Circadian Hourly
```bash
# Surveillance, diagnosis, intervention
hermes -p endocrine-immune cron create "0 * * * *" \
  --prompt "Run Immune hourly surveillance cycle. Scan fleet for TWC < 5.5, error rates > 3, journal decay, cron failures. Diagnose root causes. Spawn intervention agents via talent gate. Log all activity." \
  --skills sentinel-compliance-sweep \
  --name "Immune Hourly Surveillance"
```
**Rationale:** Immune surveillance runs continuously but intensifies during rest phases. Hourly balances responsiveness with resource use.

### Circulatory (Harvey Engine) — Continuous (15 min)
```bash
# Transport, registry sync, fabric maintenance
hermes -p circulatory-skeletal cron create "*/15 * * * *" \
  --prompt "Run Circulatory transport cycle. Sync fleet analytics from OpenClaw, update Harvey fabric registry, verify transport routes, check Morphogen genotype registry health. Report connectivity issues." \
  --skills sibling-agent-fleet-analytics-sync \
  --name "Circulatory Transport Sync"
```
**Rationale:** Circulatory system runs continuously. 15-min intervals balance freshness with API rate limits.

### Orchestrator (Hypothalamus) — Event-Driven + Daily Summary
```bash
# Receives Telegram → Kanban dispatch (event-driven)
# Daily fleet summary at 06:00
hermes -p orchestrator cron create "0 6 * * *" \
  --prompt "Generate daily fleet status summary for principal. Include: Kanban board status, talent gate activity, body system health (from Morphogen), cron compliance, intervention actions taken. Deliver via Telegram." \
  --skills kanban-orchestrator \
  --name "Orchestrator Daily Summary"
```
**Rationale:** Hypothalamus integrates signals and reports to higher centers. 6 AM aligns with cortisol awakening response.

## Cron Job Creation Commands (All at Once)

```bash
# Run from a shell with hermes CLI available
# Assumes profiles: cns, autonomic, endocrine-immune, circulatory-skeletal, orchestrator

# Autonomic - Ultradian 5 min
hermes -p autonomic cron create "*/5 * * * *" \
  --prompt "Run Quartz lattice PID control cycle. Check task queue, regulate active tasks, maintain homeostasis. Report anomalies." \
  --skills kanban-worker \
  --name "Autonomic Ultradian Cycle"

# Endocrine - Circadian daily 03:00
hermes -p endocrine-immune cron create "0 3 * * *" \
  --prompt "Run Endocrine daily growth cycle. Execute Avrami JMAK phase transition checks, Landau free energy minimization, SOC criticality assessment, CPM pattern formation. Update growth trajectories. Report developmental milestones." \
  --skills aisha-md-health-scoring-cron-execution \
  --name "Endocrine Circadian Growth"

# Immune - Circadian hourly
hermes -p endocrine-immune cron create "0 * * * *" \
  --prompt "Run Immune hourly surveillance cycle. Scan fleet for TWC < 5.5, error rates > 3, journal decay, cron failures. Diagnose root causes. Spawn intervention agents via talent gate. Log all activity." \
  --skills sentinel-compliance-sweep \
  --name "Immune Hourly Surveillance"

# Circulatory - Continuous 15 min
hermes -p circulatory-skeletal cron create "*/15 * * * *" \
  --prompt "Run Circulatory transport cycle. Sync fleet analytics from OpenClaw, update Harvey fabric registry, verify transport routes, check Morphogen genotype registry health. Report connectivity issues." \
  --skills sibling-agent-fleet-analytics-sync \
  --name "Circulatory Transport Sync"

# Orchestrator - Daily summary 06:00
hermes -p orchestrator cron create "0 6 * * *" \
  --prompt "Generate daily fleet status summary for principal. Include: Kanban board status, talent gate activity, body system health (from Morphogen), cron compliance, intervention actions taken. Deliver via Telegram." \
  --skills kanban-orchestrator \
  --name "Orchestrator Daily Summary"
```

## Verification

```bash
# List all cron jobs across profiles
for profile in cns autonomic endocrine-immune circulatory-skeletal orchestrator; do
  echo "=== $profile ==="
  hermes -p $profile cron list
done
```

## Pitfalls

| Pitfall | Consequence | Fix |
|---|---|---|
| Same cron schedule for all profiles | Wrong timescale, resource contention | Use biological rhythms table above |
| No cron for Immune | Surveillance gaps, undetected failures | Hourly cron mandatory |
| Endocrine cron at wrong time | Misses growth hormone window | 03:00 local time |
| Autonomic cron too slow | PID oscillation, instability | 5 min maximum |
| Orchestrator no daily summary | principal blind to fleet status | 06:00 summary mandatory |