# Coaching in Plain English — Pattern for Advisory Board Synthesis

## When to Use
Every board synthesis (Stage 3) that escalates decisions or recommendations to the user. Also applies to any board output the user will read directly.

## The Problem
Board advisors (especially red team) speak in domain jargon. The user is a principal who needs to make business decisions, not an engineer who already knows the terminology. A synthesis that lists "HRTF: build or license?" without explaining what HRTF is has failed.

## User Correction (2026-06-11)
> "you're not giving me much information... you're not really telling me what those mean... you're not helping me here. you're not giving me any coaching."

## The Pattern

For every technical term or decision in a board synthesis:

### 1. Define the Term (1-2 sentences, plain English)
- **HRTF** = Head-Related Transfer Function. The math that makes sound feel like it's coming from a specific direction in 3D space.
- **CAC** = Customer Acquisition Cost. How much you spend to get ONE person to download your app.
- **Unit economics** = Whether you make more money per customer than you spend acquiring them.

### 2. Use a Real-World Analogy
- Unit economics negative = "like spending $2 to make a cup of lemonade you sell for $1.50 — you lose 50¢ on every cup"
- SOC cascade = "like a row of dominos — if the first one falls (audio_mixer breaks), 5 others fall with it"
- Avrami nucleation = "like sugar crystallizing in rock candy — the idea has fully formed"

### 3. For Decisions, Explain Each Option Like You're Pitching a Friend
- **"Build"** means: Write all that 3D audio math yourself. More control, takes longer, harder.
- **"License"** means: Use someone else's ready-made system. Faster, less control.
- **Recommendation:** License for MVP. Use Apple's built-in spatial audio. Free, fast, works. Build your own later if needed.

### 4. For Risk Claims, Add "What This Means For You"
Don't just say "75-85% rejection probability." Say:
> "Apple will probably reject your first submission. This is normal for health-adjacent apps. Plan for 1-2 rejections (2 weeks extra). If we get the compliance docs right and spatial audio is the first screen, probably 30-40% on first submission."

### 5. Never Escalate Without Coaching
Every "DECISION NEEDED" must include:
- WHAT it means (plain English)
- WHY it matters (business impact)
- WHAT HAPPENS if they choose each option
- YOUR RECOMMENDATION (with reasoning)
- DEFAULT if they don't answer (so work proceeds)

## Anti-Patterns
- Listing "HRTF: build or license?" with no explanation
- Saying "unit economics negative" without the lemonade analogy
- Citing patent numbers without explaining what the patent actually covers
- Using severity labels (CRITICAL, HIGH) without saying what the real-world consequence is
- Presenting 4 decisions without saying which ones are urgent vs. can wait
- Defending a red team claim when the user pushes back, instead of verifying independently

## Example (BetterSleep Coaching Session 2026-06-11)
See: `/<workspace>`

This session took a jargon-heavy Stage 3 synthesis and rewrote every section with plain English definitions, analogies, and actionable coaching. The user went from "you're not helping me" to having clear answers on all 4 decisions.
