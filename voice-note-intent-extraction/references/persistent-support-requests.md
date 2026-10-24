# Persistent Support Requests

## Session note

This reference captures a recurring pattern in voice-note extraction:
users may describe a coaching system that must operate as a long-term background assistant, not just a one-time responder.

## What to extract

When the user says the coach should be:
- active 24/7
- in the background
- continuously helping
- constantly updating
- researching the latest information
- keeping the user on track over time

extract the requirement as a *persistent support mode*.

## What not to collapse

Do not flatten these into a generic "help the user" request.
Keep the distinction between:
- one-time answer mode
- ongoing coach mode

## Useful labels

These phrases are safe shorthand for extracted requirements:
- persistent mode
- background continuity
- freshness-aware coaching
- proactive update loop
- warm session state

## Pitfall

If the note contains both engine-building chatter and the user's real ask, separate them cleanly.
The persistent-coach requirement belongs in the request, not the background.
