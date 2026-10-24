# Ledger mint gotchas: GENOME gate + assignee (observed live 2026-08-21)

Session: financial-research thread, T-260821-0088..0092. Every item below
was hit live and resolved in-session.

## assignee rules (task_ledger.submit)
- `assignee` must be a people.json `P-*` id (P-ASHLEY, P-BRANDON,
  P-NANDITA, P-PARAG, P-ANGELA as of 2026-08-21) or OMITTED from the call
  entirely.
- Invalid id -> `ValueError: unknown assignee 'P-HERMES' — add them to
  stores/people.json`. Operators are NOT people; there is no P-HERMES.
- Passing `assignee=None` -> `IntegrityError: NOT NULL constraint failed:
  tasks.assignee`. Omit the kwarg, never pass None.

## GENOME gate (kind=build only)
`submit(..., kind='build')` requires a GENOME block inside `detail`,
parsed by `organism/genome_gate.py` (NOT gates/genome_gate.py — the gates/
path does not exist; checking it wastes a search). Regex at :113:

    GENOME: body=(\S+) scientist=(DS \S+) physics="([^"]+)" 8d=(\S+)

- body: canonical Gray's systems + organism bodies (circulatory,
  digestive, lymphatic, immune, ...) validated against organism_config.
- scientist: must start with `DS ` (e.g. `the specialist engine`).
- physics: quoted one-liner, non-empty.
- 8d: HUMAN_DIMENSIONS = environmental, financial, intellectual,
  physical, psychological, social, spiritual, vocational; or
  AI_DIMENSIONS = accuracy, adaptability, alignment, coherence, consensus,
  coordination, efficiency, latency, load_balance. `financial` IS a valid
  human dimension.
- Worked example (accepted live):
  `GENOME: body=digestive scientist=the specialist engine physics="digestive
  catabolism: external financial sources broken into absorbable evidence
  units at the single ingest path" 8d=financial`
- A newline after the block inside `detail` is fine.

## Query the vocab live before minting (saves a failed submit)
    python3 -c "import sys; sys.path.insert(0,'/<workspace>'); import genome_gate as g; print(sorted(g._vocab()['bodies'])); print(sorted(g._vocab()['human_dims']))"

## Other submit facts re-confirmed this session
- kinds: build, decision, defect, gap, improvement, maintenance, probe,
  question, verify. `research` is NOT a kind — research foundations mint
  as kind=gap or verify with flow=FLW-RESEARCH.
- flow is validated against stores/flow-registry.json; unknown code ->
  ValueError naming the file to edit (data, never code).
- claim(c, actor, actor_kind, task_id=...) — actor THEN actor_kind; wrong
  order raises "actor_kind must be 'ai' or 'human'".
