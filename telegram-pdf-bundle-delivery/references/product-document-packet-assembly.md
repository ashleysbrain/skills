# Product Document Packet Assembly Pattern

## When to use
The user needs to assemble a packet of product/engine documents for a technical partner (CTO, investor, advisor) and send it via Telegram. They usually say something like "I need to gather my documents" or "what do I give [person] for product?"

## Workflow

### 1. Find scattered product docs
Search the workspace for key documents using multiple keyword passes:
```
search_files: "three emotion|emotions.*evoke|product thesis|manifesto|vision"
search_files: "perplexity|integration.*engine|engine.*integration"  
search_files: "PIML|physics.informed|strategic pivot"
```
Common locations in DS workspace:
- `ds-wave-elite-conclave-private/` — PRODUCT_THESIS, INTEGRATION, ARCHITECTURE
- `ds-wave-design-advisory-panel-private/` — THREE-EMOTION-CREATIVE-BRIEF
- `ds-wave-*-advisory-panel-private/` — PIML-STRATEGIC-PIVOT, PIML-MARKETING-BRANDING
- `ds-wave-coaching-engine/` — README, ARCHITECTURE
- `ds-wave-shared/` — cross-panel docs, integration guides

### 2. Update positioning if needed
Check if canonical docs reflect current positioning. Common updates:
- Product thesis version bump
- Category positioning (e.g., "AI Life Coach, not health coach")
- New science scope (e.g., PIML naming)

### 3. Create bridge document if needed
If the audience is a technical partner already building, create an **integration guide** (not a tutorial):
- Architecture overview (layers, how they connect)
- API endpoints with request/response examples
- Data flow diagrams
- Frontend integration checklist (what buttons connect to which endpoints)
- Build order (what to wire up first, second, third)
- Key constraints and what's already working

Rule: assume competence. Show "how my stuff plugs into your stuff" not "what is this thing."

### 4. Batch convert to PDF
```bash
cd /tmp/packet
for f in *.md; do
  md-to-pdf "$f" --pdf-options '{"format":"Letter","margin":{"top":"20mm","bottom":"20mm","left":"15mm","right":"15mm"}}'
done
```

### 5. Deliver with organized reading order
Send a single Telegram message with:
- Brief intro ("X documents ready")
- "Start here" pointing to the most important doc
- Numbered list with emoji (1️⃣ 2️⃣ ...) grouping by purpose
- Each item includes `MEDIA:/path/to/file.pdf`

## Pitfalls
- Don't create ground-up tutorials for partners who already have a working build
- Don't make the user hunt for which doc to read first — always designate a "start here"
- Don't forget to update the canonical docs before packaging (version bump, positioning)
- Don't bundle into one PDF when each doc serves a different purpose and the recipient will reference them individually
