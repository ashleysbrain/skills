# GENOME Gate Canonical Values (verified live 2026-08-28)

Source of truth: `/<workspace>`
(GENOME_RE + parse_genome). Regex:

```
GENOME:\s*body=(\S+)\s+scientist=(.+?)\s+physics=(["'])([^"']*)\3\s+8d=(\S+)
```

## Canonical body systems (single token, no spaces)
circulatory, connective, creative_visual, digestive, endocrine, immune,
integumentary, lymphatic, memory, metabolic, muscular, nervous, network,
nucleus, regulatory, reproductive, respiratory, sensory, skeletal, urinary

## Canonical 8d dimensions

**AI:** accuracy, adaptability, alignment, coherence, consensus,
coordination, efficiency, latency, load_balance

**Human:** environmental, financial, intellectual, physical,
psychological, social, spiritual, vocational

## Rejection examples (observed 2026-08-27/28)
- `body=clinical guardian` → space breaks `(\S+)`
- `body=placenta` → not canonical (use `reproductive`)
- `8d=privacy` → not canonical (use `accuracy` etc.)
- lane `clinical` → must exist in task-taxonomy.json
- port `:port` in title/detail → premint scan rejects (registry-owned)

## Other mint quirks
- `actor_class` CHECK constraint allows only `ai|human|ai-or-human` —
  cannot use `fleet` to auto-ack tasks; set `state='done'` with an
  ACK-AT-MINT note instead.
- `UPDATE ... WHERE id IN (?)` fails — build placeholders dynamically.
- Bus schema: `from_op`/`to_op` (not `from`/`to`); no `type` column —
  filter on `subject`.
- Conductor :port endpoints: `/health`, `/api/immune` (serves
  `rulings_pending`), `/api/calendar`, `/api/bus` — no `/needs-you`,
  `/api/decisions`, `/api/rulings`.
- principal decision cards render context only when `ceo_brief` fields
  (what/why_you/if_approved/if_rejected) are non-empty — patched fallback
  lives in conduction_daemon.py (~line 760); backup at
  conduction_daemon.py.bak-contextfix.
