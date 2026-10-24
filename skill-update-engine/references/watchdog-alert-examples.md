# Watchdog Alert Examples — Concrete Outputs

This file contains real watchdog alert outputs for the Divinity Health V1 Skill Product Review job (`c37a1090869d`), captured during live monitoring. Use these as reference templates when the watchdog cron job (`31e90033684f`) produces its deliverable.

---

## Example 1: Philosophical Shortfall (Informational — Downgraded)
**Date:** 2026-06-23  
**Watchdog session:** `cron_31e90033684f_20260623_131100`  
**Review job run:** 2026-06-23 03:27 UTC (status: ok)  
**Engine report:** Emitted §13.1 JSON block with `pipeline_status: "nominal"`, `shortfall_label: "philosophical"`

### Watchdog Output
```
The Divinity Health V1 Skill Product Review job (`c37a1090869d`) ran successfully on 2026-06-23 at 03:27 UTC. The pipeline status is **nominal**, but the day falls short of the V1 health-review target profile:

| Metric | Target | Actual | Gap |
|--------|--------|--------|-----|
| New skills recommended | 3 | 0 | **−3** |
| Updates generated | 5 | 3 | **−2** |

**Shortfall label:** *philosophical* — the V1 core + support pair (`8d-pattern-awareness` + `8d-snapshot-report`) was assessed as structurally coherent and in maintenance mode, so no new skills were genuinely needed. The 3 patches shipped were manifest/version integrity fixes.

**Corrective action:** The ARBITER should expand the scan radius in the next cycle (per §2 of skill-update-engine) to surface ≥3 candidates. Prioritize the queued PARALLAX item — **8d-pattern-awareness reference consolidation** (22 support files, exceeds 15-file threshold) — as the next medium-confidence structural update to close the update gap.
```

### Classification
- **Template used:** Philosophical shortfall (informational — downgraded, no daily alert) per §13.2
- **Routing:** Downgraded to informational per watchdog routing rule (`shortfall_label == "philosophical"` → suppress daily alert)
- **Escalation trigger:** 3+ consecutive days with same root cause → target-calibration issue (R15)

---

## Example 2: Structural Shortfall (Alert)
**Date:** 2026-06-25  
**Watchdog session:** (this session)  
**Review job run:** **Not run** — no output file in `/<workspace>` for 2026-06-24 or 2026-06-25; no session found for today's execution  
**Scheduled trigger:** 03:25 daily — elapsed without delivery

### Watchdog Output
```
The review job `c37a1090869d` **has not run yet for 2026-06-25** / **ran but failed to produce candidates**.

**Status for 2026-06-25:**
- Review job `c37a1090869d`: **not run**
- No session found for today's execution

**Today's delivery vs. targets:**
| Metric | Target | Delivered | Gap |
|--------|--------|-----------|-----|
| New skill recommendations | 3/day | 0 | **3** |
| Total updates | 5/day | 0 | **5** |

**Next corrective action:** Trigger the review job manually or investigate why the 03:25 cron trigger did not fire.
```

### Classification
- **Template used:** Structural shortfall (alert) per §13.2
- **Routing:** Full alert — job did not execute, structural issue
- **Corrective action:** Manual trigger or cron investigation

---

## Key Observations for Future Watchdog Runs

1. **Philosophical vs. Structural distinction matters** — The June 23 run produced output (3 updates) but missed the new-skill target due to coherent family (philosophical). The June 25 run produced nothing (structural). The watchdog MUST classify correctly to avoid alert fatigue.

2. **JSON block presence enables auto-classification** — The June 23 engine report emitted the §13.1 JSON block, allowing the watchdog to read `shortfall_label: "philosophical"` and downgrade. If the JSON block is missing, the watchdog must use the "JSON block missing" template and reconstruct from state.db.

3. **Cron schedule verification** — The review job runs at 03:25 (cron: `25 3 * * *`). The watchdog runs every 360 minutes (interval). On June 25, the watchdog ran after the review job's scheduled window — this is the correct detection window.

4. **Output file existence = primary signal** — Check `/<workspace>*.md` first. If no file for today, the job didn't run (structural). If file exists but no JSON block, use "JSON block missing" template.

5. **Session search as backup** — When output file exists but content is ambiguous, use `session_search(query="c37a1090869d", sort="newest")` to find the engine session and extract the JSON block or reconstruct metrics.

---

## Template Compliance Checklist

For every watchdog output, verify:
- [ ] Uses exact template from §13.2 (Structural / Philosophical / JSON block missing / Silent)
- [ ] Includes job ID (`c37a1090869d`) and date
- [ ] Shows metric table with Target/Delivered/Gap
- [ ] States shortfall classification (structural/philosophical)
- [ ] Provides specific next corrective action
- [ ] Does NOT add custom commentary beyond template fields

---

*Generated from live watchdog runs on 2026-06-23 and 2026-06-25. Update this file when new alert patterns emerge.*