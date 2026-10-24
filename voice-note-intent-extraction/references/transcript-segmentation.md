# Transcript Segmentation Rubric

Use this when a voice note mixes the actual ask with background, implementation ideas, and product vision.

## Buckets

- **Request**: the concrete deliverable the user wants now
- **Context**: background facts that explain why the request matters
- **Constraints**: hard rules, exclusions, naming rules, scope limits
- **Operating mode**: whether the user wants a one-time answer, a long-term coach, background monitoring, or regular updates
- **Noise**: repetition, side stories, engine-building talk, or details that do not change the ask

## Extraction rule

When the user says to ignore the engine or focus on the ask, treat that as the active scope boundary.

When a voice note says both:
- "answer this now"
- and "also keep it going over time"

capture both as distinct requirements:
- immediate response behavior
- persistent support behavior

## Example shape

- **Request**: update the coaching flow
- **Context**: the user wants coaching across many domains, not just one-off answers
- **Constraints**: do not assume principal, do not use real public names for advisors
- **Operating mode**: persistent / always-on support with regular refreshes
- **Noise**: engine-building tangents that do not change the request
