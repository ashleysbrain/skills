# principal action surface — where ready deliverables go

Class: filing a finished artifact (comment, post, kit) so the principal can act on it.

## Rule

The `/comments` board (b-comments) is the principal's visible action surface. Any paste-ready deliverable — comments, principal-feed posts, correction kits — files there with explicit `id`, next `seq`, status `ready`; tap-to-copy buttons render from that board's kind/status.

Organizational boards (b-posts, b-art, b-comments itself as an archive) hold inventory; they are NOT principal action surfaces and some have no tab at all. Filing a deliverable on its topical board hides it — move or mirror it to b-comments.

## Pitfall

Inserting a card without explicit id/seq can land a NULL-key row (insert helpers raise TypeError on None only after the write); always set both, computed from `MAX(seq)` on the target board first.
