# Release Triage for Candidate Skills

Use this checklist when deciding which existing skill should be released, promoted, or refactored into a public umbrella.

## Rank candidates by four questions

1. **Is it immediately useful?**
   - Can another user use it without hidden context, private repos, or special setup?

2. **Is it a class-level umbrella?**
   - Does it describe a reusable workflow family rather than one session, one project, or one internal codename?

3. **Is the boundary safe?**
   - Does the public layer avoid PHI, proprietary calibration, internal fleet details, or private infrastructure paths?

4. **Does it create a natural upgrade path?**
   - Can the open layer stand on its own while the premium layer adds intelligence, automation, or personalization?

## Simple scoring rubric

Score each candidate 0–5 on each axis:
- Utility
- Self-containedness
- Safety / privacy boundary
- Reusability as a class-level umbrella
- Clarity of public promise

High scores usually mean the skill is ready to ship.
Low scores usually mean it should be rewritten as an umbrella with details pushed into `references/`.

## Overlap handling

If two skills cover the same territory:
- pick the broader umbrella for release
- move session-specific detail into references
- note the overlap in the handoff or review
- let the curator handle long-term consolidation

## Red flags

- depends on private health data or calibration
- requires internal DBs, cron jobs, or fleet-specific paths
- only makes sense for the current project or day
- is mostly a wrapper around proprietary logic
- can only be used by people who already know the backstory

## What “good” looks like

A good public skill:
- explains the workflow clearly
- is useful with minimal setup
- preserves the moat by keeping private logic out of the public layer
- uses references for the details that would otherwise bloat the main SKILL.md
- reads like a standard other people could adopt
