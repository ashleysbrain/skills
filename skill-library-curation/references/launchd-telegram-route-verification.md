# Launchd + Telegram route verification notes

Session lesson: when a user says the Telegram session is "stuck" or "not working," do not jump straight to a transport failure. First compare the latest user message with the assistant's last turn to detect drift or a wrong-task response.

Then verify the route in layers:
- app/service health: confirm the local service is loaded and running under launchd
- direct endpoint: hit the local `/health` endpoint or equivalent, not just a wrapper status command
- gateway health: confirm the the operator agent gateway is loaded and active
- routing state: inspect whether the setup is using standard DM routing or topic-mode routing before assuming a missing mapping

Useful log/command landmarks from the session:
- `launchctl print gui/$(id -u)/<label>` to confirm a service is loaded and see the executable, args, and working directory
- `curl http://127.0.0.1:port/health` to verify the API directly
- `hermes gateway status` to confirm the gateway service is live
- local state inspection may reveal that topic-mode tables are absent, which means the system is operating in standard DM mode rather than a broken topic map

Do not encode the environment-specific failure itself as a rule; the durable lesson is the layered verification sequence and the "latest user turn first" drift check.