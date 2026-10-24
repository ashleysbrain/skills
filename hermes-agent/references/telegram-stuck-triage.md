# Telegram stuck / not responding triage

Use when the user says the Telegram chat is "stuck", "not working", or the agent seems frozen in Telegram.

## First interpret the symptom
A Telegram report can mean different things:
- **Gateway/session issue:** the platform session is disconnected, misrouted, or the bot is not receiving messages.
- **Conversation state issue:** the bot is waiting on approval, tool output, or a follow-up and the user expects a response.
- **Topic/thread issue:** the user is in the wrong Telegram topic, DM topic, or chat mapping.

## Triage sequence
1. Check whether the user is asking about the **current chat** or a different Telegram chat/topic.
2. Ask for the **exact symptom** if it is ambiguous:
   - no replies at all
   - replies go to the wrong chat/thread
   - responses appear delayed or missing
   - the assistant says it is waiting/stuck
3. If you are sending a live test, prefer `send_message(action="list")` first when there is any possibility of multiple Telegram targets. Then send to the explicit target that matches the user-visible DM/group/thread instead of assuming the bare platform name will land where the user is looking.
4. If the user means the assistant is waiting, explain the immediate blocker rather than claiming the platform is broken.
5. If the user means routing is wrong, verify the target chat/topic mapping before changing anything.

## Delivery verification
When the user says "I don't see a message" after you reported a successful Telegram send:
- do **not** assume the delivery failed just because the outbound API call returned success
- check whether the user may be viewing a different Telegram account, chat, thread, or topic
- resend to the explicit DM/group target from `send_message(action="list")`
- confirm the exact message ID / target that was used so the user can compare against their Telegram UI
5. If Telegram looks healthy but the assistant still feels stuck, check the upstream backend logs for a model/provider exception before blaming the platform. A local worker crash can make Telegram look frozen even when delivery is fine.

## Reply guidance
- Do **not** answer with a vague "I'm stuck" explanation unless the user explicitly asked for internal state.
- Prefer a concrete statement of what is blocking progress:
  - missing task/instruction
  - wrong chat/topic context
  - pending approval
  - platform/session mismatch

## Useful follow-up questions
- "Do you mean the Telegram bot is not replying at all, or it is replying in the wrong chat/topic?"
- "Is this in the main chat, a DM topic, or a group/thread?"
- "What was the last message you sent before it stopped behaving correctly?"