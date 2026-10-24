# SOS Crisis Protocol

This file is the standalone crisis-handling reference for the public 8D brief.
It documents the staged decision rules so the main skill can stay compact.

## Purpose
If the input suggests imminent harm, emergency, or crisis, stop normal 8D interpretation and switch to SOS mode.

## Stage 1 rollout rule
If the user can still interact safely, ask one manual check first:

> “Are you in immediate danger or do you need emergency help right now?”

In stage 1:
- do **not** auto-route from observed hard-emergency signs alone
- present the closest safe help path
- wait for explicit confirmation before any action that would route, dispatch, or connect externally

## Stage 2 rollout rule
Once the manual check and help-path presentation work reliably:
- prepare the best local number, resource, or handoff text
- still require user confirmation before anything is sent or dialed

## Stage 3 rollout rule
Fully automated routing is a future option only after shadow or pilot validation and explicit opt-in.

## Trigger classes
Treat the following as SOS candidates:
- suicidal thoughts, intent, plan, or inability to stay safe
- overdose, poisoning, medication misuse
- chest pain, breathing trouble, stroke signs, seizure, fainting, severe bleeding, severe allergic reaction
- psychosis, mania, severe confusion, or inability to follow instructions safely
- domestic violence, stalking, assault, coercive control, or immediate physical threat
- fire, gas leak, carbon monoxide exposure, flood, earthquake, or other environmental danger
- child, elder, or vulnerable-adult safety risk

## Crisis-verification gate
The engine must not label ordinary distress language as a crisis unless the crisis gate passes.

### Step 1: Emergency veto
Before anything else, test for hard emergency flags.

Set `E = 1` if any of the following are present:
- trouble breathing
- chest pain
- stroke signs
- seizure
- fainting / unresponsive
- severe bleeding
- severe allergic reaction
- fire, gas leak, or carbon monoxide danger
- active physical assault or immediate bodily threat

If `E = 1`, classify and route as emergency immediately. Do not run crisis math to justify the branch.

### Step 2: Crisis evidence families
If `E = 0`, score six families. Let each family score `x_i` be in `[0, 1]`:
- `I` = explicit self-harm / harm intent
- `P` = concrete plan or preparation
- `M` = means access or acquisition
- `H` = imminence / near-term time horizon
- `K` = inability to stay safe or maintain control
- `R` = corroboration from history, repetition, or another source

Let `c_i` be reliability in `[0, 1]`, and `s_i = x_i * c_i` be signal strength.
A family counts as active only when `s_i >= 0.5`.
Treat lexical wording alone, such as “crisis” or “emergency,” as a weak cue only.

### Step 3: Weighted posterior
Compute weighted evidence mass:

`M_crisis = 0.30s_I + 0.20s_P + 0.15s_M + 0.15s_H + 0.10s_K + 0.10s_R`

Compute a support factor:

`Q = 0.5 + 0.5 * N`

where `N` is the average reliability of active families, or `0` if there are none. If there are no active families, set `Q = 0`.

Compute contradiction strength `X` in `[0, 1]`:
- `X = 0` when nothing contradicts the crisis
- `X = 1` when the input is better explained by ordinary stress, slang, or a non-crisis meaning

Adjusted crisis certainty:

`C_crisis = M_crisis * Q * (1 - X)`

### Step 4: Branch decision table
Use the first matching branch.

1. **Emergency branch**
   - Condition: `E = 1`
   - Action: route as *emergency*

2. **Crisis override branch**
   - Condition: any of the following while `E = 0`:
     - `I >= 0.85`, `c_I >= 0.75`, and `X < 0.35`
     - `P >= 0.70` and `M >= 0.70` and `H >= 0.70` and `X < 0.35`
     - `K >= 0.80` and at least one of `I`, `P`, `M`, or `H` is active
   - Action: route as *crisis*

3. **Posterior crisis branch**
   - Condition: `C_crisis >= 0.55` and at least **2 active families**
   - Action: route as *crisis*

4. **Possible-crisis branch**
   - Condition: `0.25 <= C_crisis < 0.55` or exactly **1 active family**
   - Action: label as *possible crisis*
   - Do not route yet; ask one essential question or provide low-risk support.

5. **Normal 8D branch**
   - Condition: `C_crisis < 0.25` and no override fired
   - Action: stay in normal 8D mode

### Invariants
- Emergency and crisis are distinct branches.
- Crisis language alone does not activate a branch.
- A branch must be supported by the emergency veto, a crisis override, or the posterior threshold.
- If there are no active families and no override, the output cannot be *crisis*.
- High contradiction can only suppress routing; it cannot create routing.

## Response rules
- Do not guess the user’s country if it matters.
- If life is in immediate danger, do not delay for clarification.
- Do not give unsafe home remedies.
- Do not over-question.
- Do not continue normal 8D interpretation until the crisis is routed.

## Common regional emergency numbers
These are examples, not substitutes for local confirmation.

### United States / Canada
- Emergency: 911
- Suicide & Crisis Lifeline: 988
- Poison Control (US): 1-800-222-1222
- Domestic violence (US): 1-800-799-SAFE (7233)
- Sexual assault (US): 1-800-656-HOPE (4673)

### United Kingdom / Ireland
- Emergency: 999 or 112
- Samaritans: 116 123
- NHS non-emergency: 111 (UK)

### European Union
- Emergency: 112

## Location resolver rules
If the country is unknown, ask one direct question: “What country are you in?” If the user is in immediate danger, do not delay the emergency instruction while waiting. If the country is known, use the best local emergency, crisis, toxicology, or victim-support resource available and prefer official or health-service resources.

## Response snippets
- Immediate danger: “This may be an emergency. Call local emergency services now. If you can, unlock the door and keep your phone with you.”
- Crisis support: “I’m treating this as urgent. Please contact your local crisis line or emergency services now, and if possible have a trusted person stay with you.”
- Poisoning / overdose: “This could be poisoning or overdose. Call poison control or emergency services now. Keep the package nearby and tell them what was taken and when.”
- Violence / assault: “Get to a safer place if you can and call emergency services if safe to do so. If you’re able, contact a trusted person or local advocate now.”

## Output shape
- brief crisis label
- best next step
- 1 to 3 immediate actions
- one essential question only if needed
- local resource or best fallback
- escalation note
