# Personality Variation Sets — Index

**Rule:** Before creating any new profile, search the existing library first.

## Existing Profile Library

### Domain Templates (100 profiles)
Location: `~/your-workspace/docs/personality-variations/`

| File | Domains | Profiles |
|------|---------|----------|
| `research-science-domains.md` | Neuroscience, Histology, Cardiovascular | 30 (V1-V10 each) |
| `creative-design-domains.md` | Creative/Design, Marketing, Product/UX | 30 |
| `operational-domains.md` | Engineering/DevOps, Medical/Clinical, PM, Organism Architecture | 40 |

### Agent-Specific Profiles (280 files)
Location: `~/your-workspace/hydra-os/intel/agents/codes/*-10-variations.md`

Categories include:
- C-Suite (NEBULA, BINARY, COSMOS, HERA, etc.)
- GD agents (CALISTA, SABLE, ATHENA, MUSE, etc.)
- Dr. agents (Dr.-Alexander-Petrov, Dr.-Amanda-Foster, etc.)
- Technical (FORGE, ARBITER, PARALLAX, SENTINEL, etc. — note: some of these agents are retired but their variation files remain for reference)
- Medical (AISHA, AISHA-MD, VITALS, etc.)
- Each with DS-prefixed and non-prefixed versions

### Registry
`~/your-workspace/docs/personality-variations/README.md` — lookup procedure and inventory

## Lookup Procedure

Before building ANY new specialist profile:

1. Check domain templates — does the specialist domain match one of the 10 existing templates?
2. Check agent-specific files:
   ```bash
   ls ~/your-workspace/hydra-os/intel/agents/codes/ | grep -i "[keyword]"
   ```
3. If a profile exists — USE IT. Do not create a new one.
4. If no profile exists — create one using the domain template as the base, save to `docs/personality-variations/`.

## Profile Code Format

`[MBTI]-[Enneagram]-[Domain]-[V#]`

Example: `INTJ-5w6-NEURO-V3` = INTJ, Enneagram 5 wing 6, Neuroscience domain, V3 Analyst variation

## OCEAN Code Format

`O#C#E#A#N#` (each 0-10)
O = Openness, C = Conscientiousness, E = Extraversion, A = Agreeableness, N = Neuroticism

## Domain-Specific Variation Templates

### Research/Science
V1 Scanner | V2 Reviewer | V3 Analyst | V4 Methodologist | V5 Historian | V6 Skeptic | V7 Synthesist | V8 Forecaster | V9 Explainer | V10 Lead

### Creative/Design
V1 Visionary | V2 Explorer | V3 Designer | V4 Craftsman | V5 Aesthete | V6 Maverick | V7 Storyteller | V8 Innovator | V9 Performer | V10 Creative Director

### Engineering/DevOps
V1 Architect | V2 Reviewer | V3 Debugger | V4 Security Auditor | V5 Historian | V6 Tester | V7 Integrator | V8 Release Manager | V9 Documenter | V10 Lead Engineer

### Medical/Clinical
V1 Diagnostician | V2 Researcher | V3 Analyst | V4 Treatment Planner | V5 Historian | V6 Skeptic | V7 Synthesist | V8 Forecaster | V9 Communicator | V10 Lead Clinician

For custom domains that don't fit a template, the prefrontal cortex (Luria) designs a custom 10-variation set before dispatch. Structure is always 10 variations with MBTI/Enneagram/OCEAN.
