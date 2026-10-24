# Rolling mirror helper notes

Session-derived guidance for maintaining the the specialist engine chat-thread mirror.

## Why the helper exists
- The mirror should stay short, factual, and readable for cron synthesis.
- Manual hand-editing tends to create drift and inconsistent timestamps.
- A tiny append-only helper makes it easy to record new steering signals without rewriting the whole file.

## Recommended pattern
- Keep a `## Rolling updates` section near the bottom of the mirror.
- Append timestamped bullets only.
- Include a compact source label when useful.
- Cap the section size so old notes do not dominate the mirror.

## Verification
- Test the helper on a temporary copy of the mirror before wiring it into cron.
- Confirm the new bullet lands under the correct heading and spacing remains clean.
