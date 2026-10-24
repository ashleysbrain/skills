# Voice Note Context Extraction

Use this when a user sends a long voice memo that mixes product context with implementation details and asks for *only the specific request*.

## Extraction rule

Separate the transcript into three buckets:
- **Target need**: what the user actually wants
- **Background/context**: supporting architecture, rationale, or examples
- **Non-goals / exclusions**: what the user said to leave out

## Practical filter

If the user later says something like:
- "only find the context related to the type of principal I want"
- "not the engine itself"

then keep only phrases that describe the desired role, outcome, constraints, and scope. Drop engine-building talk unless it changes the meaning of the request.

## Example from this session

The memo was about a QBIT health engine and explicitly asked for:
- more than 10 agents
- split maintenance/build coverage
- a renamed research agent tied to Dr. Gill the external advisor's research
- day-to-day monitoring alongside build work

It did **not** contain principal-specific context.
