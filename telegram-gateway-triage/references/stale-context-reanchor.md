# Stale context re-anchor note

Observed failure pattern:
- User reported Telegram was stuck / not working correctly.
- Assistant answered a different ongoing repo/task thread instead of the Telegram complaint.

Recovery pattern:
1. Treat the latest user complaint as the only active task.
2. Discard unrelated repo progress or prior task state from the reply.
3. Acknowledge the mismatch briefly.
4. Re-anchor on the Telegram issue and ask for the last successful message or exact symptom if needed.

Good first response shape:
- "Got it — let's ignore the prior thread and focus on the Telegram issue. Tell me the last message that went through, and I’ll separate delivery vs. reply drift."
