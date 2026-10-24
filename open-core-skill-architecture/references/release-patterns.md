# Open-Core Release Patterns

## Patterns that work

### 1. Public utility + premium intelligence
Ship a public skill that is genuinely useful on its own, then make the premium layer the place where calibration, memory, automation, or deeper synthesis lives.

### 2. Family of skills, not a monolith
Split a large domain into a small umbrella plus support skills when the jobs are distinct:
- intake / normalization
- interpretation / summarization
- safety / escalation
- premium bridge / upsell path

### 3. Make the upgrade path obvious but not coercive
The public skill should naturally prompt:
- "That was useful"
- "I want this to remember me"
- "I want the calibrated version"
- "I want hosted automation"

### 4. Release the standard, not the secret sauce
Publish the workflow, schema, and safe outputs. Keep the weights, calibration logic, and proprietary decision rules private.

## Anti-patterns
- Shipping a generic assistant with no clear job
- Revealing the moat in the public skill body
- Putting session-specific details in the umbrella SKILL.md
- Making the public skill feel like a stub instead of a real tool

## Checklist before release
- [ ] Public layer solves one real problem end-to-end
- [ ] Premium layer is clearly better, not just larger
- [ ] Public skill is understandable in under a minute
- [ ] The skill family has clear boundaries
- [ ] Launch copy matches the actual behavior of the skill
