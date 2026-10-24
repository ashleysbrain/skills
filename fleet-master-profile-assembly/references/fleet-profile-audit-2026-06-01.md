# Fleet Profile Audit — 2026-06-01

## What was verified
- Profile directory: `/<workspace>`
- Credential/profile DB: `/<workspace>`
- Master template: `/<workspace>`

## Current findings
- `agents.db` contains fleet identity + credential tables, including:
  - `agents`
  - `agent_credentials`
  - `credential_pools`
  - `agent_personas`
- Profile count on disk: **85** `*-profile.md` files
- Full 17-section profiles found: **79** of 85
- A profile is considered complete when it contains all headings `## Section 1` through `## Section 17`

## Practical verification recipe
1. Count profiles:
   - `find .../*-profile.md`
2. Count 17-section files:
   - regex check for headings `^## Section [1-9]$` / `^## Section 1[0-7]$`
3. Query DB schema:
   - `sqlite3 agents.db ".tables"`
   - `PRAGMA table_info(agents);`
   - `PRAGMA table_info(agent_credentials);`
   - `PRAGMA table_info(agent_personas);`

## Notes
- The DB is not just roster data; it also stores credential pools and persona variants.
- When auditing fleet profiles, check both the filesystem and DB schema before concluding a profile is missing or incomplete.
- Don’t assume every `*-profile.md` is part of the 17-section core-op tier; some files may be lighter or transitional.