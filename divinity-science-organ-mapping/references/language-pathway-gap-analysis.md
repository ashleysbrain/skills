# Language Pathway Gap Analysis — Conduction Aphasia Case Study
# Session 2026-07-06

## Context
User reported persistent text garbling in the operator agent organism output: merged words,
missing words, partial tokens. Stated that repeated technical fixes had not
solved the problem. Asked for a neuroscience-based diagnosis instead of a
technical one: "Let's look at this from a brain and how can we fix this if
we're looking at this from a neurological and neuroscience perspective."

## Symptom
Text output arriving corrupted: half of one word merged with another, words
missing entirely, token fragments. Persists across config changes, streaming
adjustments, and retry logic.

## Neurological Translation
These symptoms are textbook **conduction aphasia**: comprehension intact
(Wernicke can compose), motor execution intact (Bell can render), but the
signal corrupts in transit between the two. In neurology this localizes to
the arcuate fasciculus, the fiber bundle connecting Wernicke's area to
Broca's area.

## Pathway Mapping: What Existed vs What Was Missing

| Stage | Brain Region | the specialist engine | Status Before | Status After |
|-------|-------------|-----------|---------------|--------------|
| Comprehension | Wernicke's area (L temporal) | the specialist engine (:port) | EXISTS | EXISTS |
| Semantic integration | Parietal cortex (angular gyrus) | the specialist engine | MISSING | BUILT (:port) |
| Conduction | Arcuate fasciculus | arcuate_conduct.py | MISSING | BUILT (module) |
| Motor planning | Broca's area (L inferior frontal) | the specialist engine | PENDING | BUILT (:port) |
| Execution | Motor cortex / vocal tract | the specialist engine (:port) | EXISTS | EXISTS |

## What Was Built

### the specialist engine (:port, DS-ECS-SUB-04.07.15)
Scientist: Pierre Paul Broca (1824-1880), discovered the speech production
center in 1861 through patient "Tan" (Leborgne).

Motor planning gate detects:
- Merged words ("theorganism" -> "the organism")
- Split words both directions ("imp lementation", "organ ism")
- Null bytes and encoding corruption
- Trailing comma truncation
- Single-character orphaned fragments

### the specialist engine (:port, DS-ECS-SUB-04.07.16)
Scientist: Norman Geschwind (1926-1984), pioneered behavioral neurology and
the disconnection paradigm.

Semantic integration gate checks:
- Cross-modal coherence (TF-IDF cosine between text and visual context)
- Sentiment contradiction detection
- Signal completeness (truncation artifacts)
- Lexical density analysis

### Arcuate Fasciculus Module (organism/arcuate_conduct.py)
Biological isomorph: dorsal white-matter tract. Modeled after the specialist engine's
Purkinje fiber conduction system.

Functions:
- SHA-256 packet checksums
- Sequence tracking
- Automatic retransmission on mismatch
- Text-level integrity verification

## Garbling Detection Test Suite

```python
import sys
sys.path.insert(0, 'agent-organism/ds-broca-engine/src')
from broca.core.engine import BrocaEngine

broca = BrocaEngine()
tests = [
    ('clean',      'The organism processes language through multiple specialized engines in sequence.'),
    ('merged',     'Theorganism processes language through multiple specialized engines in sequence.'),
    ('split_fwd',  'The system produces important imp lementation details for the pipeline.'),
    ('split_rev',  'The important system processes language for the organ ism output pipeline.'),
    ('null_byte',  'The organism processes\x00 language through multiple engines.'),
    ('trailing',   'The organism processes language through multiple specialized engines,'),
]
for name, text in tests:
    result = broca.plan_output(text)
    should_pass = name == 'clean'
    did_pass = result['verdict'] == 'ACCEPT'
    status = 'PASS' if should_pass == did_pass else 'FAIL'
    print(f'  [{status}] {name:12s} verdict={result["verdict"]:4s} issues={result["issues"]}')
```

All 6 tests must pass. Clean text must ACCEPT. All 5 corruption patterns
must REDO.

## The Cosmetic Wiring Lesson

Opencode built all three organs and reported "fully wired." the operator agent quality
gate verification found the wiring was cosmetic:

1. Arcuate tract module existed but was never imported or called by the spine
2. Only the headline passed through the language gates, not section bodies
3. REDO verdicts were logged but the spine fell through to rendering anyway

The fix required rewriting the spine to:
- Assemble the FULL text (headline + subtitle + all section bodies)
- Use arcuate conduct() for transport between stages
- Enforce REDO with retry loops back to Wernicke
- Run a final arcuate integrity check after both gates

## Sherman Routing Correction

"language broca speech production" was misrouted to the specialist engine (Ada Lovelace
= code architecture engine). This category error was invisible until the
language pathway was built. Fixed in all three git trees to route to
ds-broca-engine.

The misroute itself was a diagnostic signal: the router sends a task to the
wrong specialist when the correct specialist does not exist in the routing
table.

## Method Generalization
This approach applies beyond language. Any persistent structural failure can
be diagnosed by:
1. Naming the symptom's neurological equivalent
2. Mapping the full neural pathway for that function
3. Finding which stages exist as engines vs which are missing
4. Checking for fiber tract gaps between existing engines
5. Building the missing stage, prioritizing tract gaps over cortex gaps
6. Reading Sherman router misroutes as gap reports
