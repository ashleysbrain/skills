# Regulatory Language Audit Pattern

**When to Use:** Before any external-facing content (marketing, positioning, thesis, LinkedIn, investor decks) ships.

**Core Rule:** Replace "constrained" → "grounded" everywhere. No medical claims. No diagnostic language. Decision-support framing only.

## Problem Words → Replacement

| Problem | Replacement | Why |
|---------|-------------|-----|
| "constrained by physics" | "grounded in physics" | "Constrained" implies restriction/limitation. "Grounded" implies foundation/stability. |
| "physically constrained outputs" | "physically grounded outputs" | Same — positive framing |
| "physics-constrained AI" | "physics-grounded AI" | Same |
| "constrained AI" (glossary) | "grounded AI" | Same |
| "unconstrained models" (technical) | KEEP | Legitimate technical comparison: standard ML without physics constraints |

## Red Flag Phrases (Remove or Rewrite)

| Red Flag | Safe Alternative |
|----------|------------------|
| "diagnose" / "diagnosis" | "read patterns" / "identify patterns" |
| "medical advice" / "health advice" | "decision-support" / "coaching" / "insight" |
| "treatment" / "therapy" | "protocol" / "plan" / "approach" |
| "prescribe" | "recommend" / "suggest" |
| "clinical" (unless citing actual clinical study) | "evidence-based" / "science-backed" |
| "patient" | "user" / "person" / "coachee" |

## Required Framing (Always Include)

> "The engine is a decision-support tool. It doesn't diagnose. It reads patterns and coaches action."

## Audit Checklist

- [ ] Search for "constrain" (all forms) → replace with "ground" (except "unconstrained models")
- [ ] Search for "diagnos" → remove
- [ ] Search for "medical" / "clinical" / "treatment" / "therapy" / "prescribe" → remove or reframe
- [ ] Search for "patient" → replace with "user" / "coachee"
- [ ] Verify "decision-support tool" framing appears in credibility section
- [ ] No em dashes in any external content
- [ ] No AI telltales ("reaching out", "leverage", "cutting-edge", "revolutionary")

## Example: Before → After

**Before:** "Our AI is physics-constrained. The models are constrained by real equations. The scoring engine produces physically constrained outputs. We don't diagnose — we provide health advice."

**After:** "Our AI is physics-grounded. The models are grounded in real equations. The scoring engine produces physically grounded outputs. The engine is a decision-support tool. It doesn't diagnose. It reads patterns and coaches action."

## Automation

```bash
# Quick audit
grep -rin "constrain" /path/to/content/ --exclude="*unconstrained*"
grep -rin "diagnos\|medical\|clinical\|treatment\|therapy\|prescribe" /path/to/content/
grep -rin "patient" /path/to/content/
```

**Files audited this session:** PIML-MARKETING-BRANDING-BRIEF.md (6 replacements). Thesis already clean.