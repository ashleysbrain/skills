# Session Discovery Pattern — August 2026

## Observed Behavior

When searching for the latest Divinity Health V1 Skill Product Review session (job `c37a1090869d`), multiple sessions exist for the same day with different naming conventions:

- `cron_c37a1090869d_20260807_032550` — review job session with actual output
- `cron_31e90033684f_20260807_024534` — watchdog session that references the review
- `cron_31e90033684f_20260806_204333` — previous watchdog run

## Recommended Search Strategy

To reliably find the **latest review job output** (not the watchdog sessions):

1. **Search for the review job ID pattern** (not the watchdog job ID):
   ```python
   session_search(
       query="Divinity Health V1 Skill Product Review",
       limit=5,
       sort="newest"
   )
   ```

2. **Alternatively, search for the cron session with review job ID prefix**:
   ```python
   session_search(
       query="cron_c37a1090869d_20260807",
       sort="newest",
       limit=3
   )
   ```

3. **Check the session title** — review sessions are titled "Divinity Health V1 Skill Product Review · YYYY-MM-DD HH:MM", while watchdog sessions are titled "V1 Skill Cycle Watchdog · YYYY-MM-DD HH:MM"

## Pitfall: Searching for Watchdog Sessions

Searching for the watchdog job ID (`cron_31e90033684f_`) will return watchdog sessions, not the actual review output. These watchdog sessions only contain gap summaries and do not contain the full §13.1 engine report with actual counts.

## Evidence

Observed 2026-08-07 during watchdog execution:
- Review job session: `cron_c37a1090869d_20260807_032550` — contains full engine report with JSON block
- Watchdog session: `cron_31e90033684f_20260807_024534` — contains only watchdog alert summary
- Both sessions exist in the database; querying for the wrong job ID returns the wrong session

## Corrective Action

Always search for the review job ID (`c37a1090869d`) or the review job session title pattern. Never search for the watchdog job ID when attempting to validate review job output.