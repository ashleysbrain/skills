# the principal handoff checklist additions (2026-08-02 final review)

Use with the main adversarial panel steps.

## First-boot docs
- [ ] `START_HERE.md` exists and is first pointer in README
- [ ] First command is `./start.sh` (never `./update.sh` for fresh clone)
- [ ] `./update.sh` documented as later-only pull path
- [ ] Every path cited in ONBOARDING/QUICK_START exists in tree
- [ ] No `cyber-gg-blueprint`, `/<home>`, or author-only paths in primary docs
- [ ] Phenotype/docs say `gg_core` if full the operator agent (not locked b2bu)

## Remote / push
- [ ] `git remote -v` → org `Divinity-Science-Research-Lab/Cyber-the operator agent` (or intended org)
- [ ] After push: `git ls-remote origin HEAD` matches `git rev-parse HEAD`
- [ ] Working tree clean of intended source; runtime dbs/logs unstaged

## Fresh clone
```bash
rm -rf /tmp/Cyber-the operator agent-handoff && git clone --depth 1 <ORG_URL> /tmp/Cyber-the operator agent-handoff
cd /tmp/Cyber-the operator agent-handoff && ./start.sh
```

## Smoke (expect 200 + payload)
- /api/health → type gg_core when full the operator agent
- /you, /setup, /integrations-adaptive, /ops
- /gg-styles.css
- POST /api/user/health-check → recorded true, twc_100, engine

## Templates (not theater)
- BRANDON_TECH_STACK.yaml (+ config copy if docs cite it)
- workspace templates under templates/workspace/
- persona yaml, onboarding checklist, daily workflow

Do not report ready until this list is green.
