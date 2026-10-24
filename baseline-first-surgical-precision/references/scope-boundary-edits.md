# Scope Boundary Edits

## Lesson from the Qubit/QUBIT rename session
When the user specifies that a change applies only to the **product surface** (e.g. v1/v2 launch docs) and **not** to the broader fleet, treat that as a hard boundary.

## Procedure
1. Identify the exact scope before editing.
2. Prefer path-limited edits over global search/replace.
3. After edits, inspect the working tree by scope and restore anything outside the approved surface.
4. Keep a clear separation between product docs and fleet / ops / archive / intel docs.

## Verification
- Product-scoped files changed only where intended.
- Broader fleet artifacts remain untouched.
- If accidental spillover happened, restore it immediately and re-check scope before finishing.
