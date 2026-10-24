# Progressive Confidence for Attention-Retention UX

Session note: when the goal is to keep a user engaged with a scoring flow, do **not** wait for full intake before producing value.

## Pattern

- Produce an immediate **provisional score** from the evidence already provided.
- Show **confidence** as a separate signal from the score.
- Let confidence rise through the day as more data points arrive, corroborate each other, or fill in missing dimensions.
- Reset the session at a sleep/wake boundary when the domain is tied to daily behavior.
- Present missing fields as **not yet observed**, not as failures.

## Attention hooks

- Show a live completeness indicator: provided vs missing vs still pending.
- Make the score update feel cumulative: each new data point should visibly add to prior context.
- Use a simple explanation of *why* confidence changed so the user sees the system learning.
- Keep the first interaction lightweight so the user gets feedback before the intake is complete.

## Avoid

- Do not require full completion before any score appears.
- Do not mix confidence into the score so the user cannot tell whether the number moved because of evidence or certainty.
- Do not make the day clock monotonic across sleep if the product is organized around wake sessions.
