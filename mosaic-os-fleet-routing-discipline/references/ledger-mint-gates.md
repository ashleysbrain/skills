# Task-ledger mint gates (verified live 2026-09-02)

Minting tasks into `/<workspace>`:

1. **Raw INSERT is blocked** (IntegrityError: 'raw INSERT INTO tasks blocked (bus #3623 single-write-path)'). Use the gate module:
   ```python
   import sys; sys.path.insert(0,'/<workspace>')
   import task_ledger as tl
   c = tl.connect()
   tid = tl.mint(c)          # reserves the ID
   tl.submit(c, title=..., kind=..., lane=..., origin=..., created_by=..., task_id=tid, detail=..., flow=..., deadline=...)
   ```
   Direct `UPDATE` for closures/field fixes DOES work — only INSERT is gated.

2. **GENOME block required for kind=build** (kind='execute' does not exist; valid kinds: build, defect, gap, improvement, verify, probe, decision, question, maintenance, research). The gate at `/<workspace>` enforces this grammar:
   - `body=` must be a SINGLE TOKEN from canonical systems (circulatory, connective, creative_visual, digestive, endocrine, immune, integumentary, lymphatic, memory, metabolic, muscular, nervous, network, nucleus, regulatory, reproductive, respiratory, sensory, skeletal, urinary)
   - `scientist=DS <Name>`
   - `physics="<quoted principle>"` — quotes REQUIRED
   - `8d=` must be a canonical dimension — AI: accuracy, adaptability, alignment, coherence, consensus, coordination, efficiency, latency, load_balance; human: environmental, financial, intellectual, physical, psychological, social, spiritual, vocational
   - `metrics="<what does this emit?>"` — required at birth (soft mode env DS_GENOME_METRICS_SOFT exists but default OFF)
   - Template: `GENOME: body=nervous scientist=the specialist engine physics="direct pathway minimizes relay latency" 8d=latency metrics="delivery latency, write-through rate"`
   - actor_class constraint: only 'ai','human','ai-or-human' (NOT 'group').

3. **Bus posts**: `python3 /<workspace> post --from X --to Y --type Z --subject ... --content ...`; intake gates subject ≤160 / content ≤2000 chars; empty stdout echoes happen — ALWAYS verify by direct sqlite read-back of message-bus.db before claiming a post landed (read-back may show a different sender's message at the same max(id); check from_op too).
