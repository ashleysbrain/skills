# Live Chat Thread Mirror Pattern

Use this pattern when a scheduled job or downstream synthesis needs the *current* chat state, but cannot read the live thread directly.

## Why it exists
- Cron jobs usually run without direct access to the interactive thread context.
- A local mirror gives the scheduler a stable, readable source of truth.
- It preserves the latest operating preferences, decisions, and open questions without relying on memory alone.

## Recommended shape
- Keep the mirror as a short, factual markdown file.
- Update it after meaningful steering exchanges.
- Include only durable items:
  - operating requirements
  - cadence / timing
  - sources to ingest
  - recent decisions
  - current open questions
- Keep it readable for both humans and automated synthesis jobs.

## Practical use
- Nightly synthesis reads the mirror alongside transcripts, tasks, logs, and workspace artifacts.
- Morning check-ins can also read the same mirror for continuity.
- If the live thread is part of the work system, mirror it locally rather than trying to reconstruct it from memory later.

## Pitfalls
- Do not turn the mirror into a full transcript dump.
- Do not store ephemeral chatter or task progress that will age out quickly.
- Do not rely on the mirror alone if other workspace artifacts are available; use it as the thread-specific anchor.
