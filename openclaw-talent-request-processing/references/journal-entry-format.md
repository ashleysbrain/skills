# Journal Entry Format for Talent Request Processing

Each cron run should add a new dated section header to the flat journal files (FORGE-journal.md, ARBITER-journal.md) using the following format:

## YYYY-MM-DDTHH:MM:SS - FORGE Talent Request Sweep (Automated)
- Requests processed: <count>
- Agents spawned: <count>
- Dispatch decisions made: <count>
- Fleet analytics sync: <summary>
- Status: <brief status>

And similarly for ARBITER:

## YYYY-MM-DDTHH:MM:SS - ARBITER Talent Request Sweep (Automated)
- Requests processed: <count>
- Agents spawned: <count>
- Dispatch decisions made: <count>
- Fleet analytics sync: <summary>
- Status: <brief status>

These sections are appended chronologically; the newest section appears at the bottom of the file.

**Example entry:**
## 2026-06-07T16:07:01 - FORGE Talent Request Sweep (Automated)
- Requests processed: 0
- Agents spawned: 0
- Dispatch decisions made: 0
- Fleet analytics sync: completed successfully (77 active agents, 124 cron jobs synced)
- Status: No new talent requests; fleet at operational capacity.
