# Progressive Confidence v1 Source Set Notes

Session-specific notes from the Adaptive Evidence Ledger spec review.

## v1 source set
Use the smallest source set that can visibly move score and confidence during a wake session:

- structured user check-ins
- explicit sleep or wake confirmation
- quest and task completion events
- calendar context when available

Optional for later phases:

- wearable data
- direct sensor or device logs
- stronger cross-source corroboration layers

## Implementation order reminder
Freeze the v1 source set before building the session object and confidence engine. The confidence model should then rise with:

- breadth of evidence
- recency of evidence
- corroboration across sources

## Product behavior
- Session opens on wake.
- Session seals on sleep.
- Confidence should grow through the day as more evidence accumulates.
- If evidence conflicts, keep history and reduce confidence instead of forcing certainty.
