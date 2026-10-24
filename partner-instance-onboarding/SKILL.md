---
name: partner-instance-onboarding
description: Use when a partner gets a dedicated paired the operator agent instance.
version: 1.0.0
tags: [telegram, pairing, profiles, partner-lane, onboarding]
---

# Partner Instance Onboarding

Class of task: the principal orders a second human (partner, CTO, teammate) to have
their OWN dedicated instance — their own the operator agent in their hands, a connection
separate from the principal's. The deliverable is a pairing-gated Telegram lane into
an isolated profile plus an auto-delivery lane, with the principal doing zero manual
relaying. Core procedure: census the family first, arm the pairing gate,
isolated profile, no-code-relay onboarding, falsified delivery lane, surgical
renames, entanglement loop.

## Procedure (fixed order)

1. **Census FIRST — the instance may already exist.** Before creating any
   named instance, search for prior creation: skill_view the organism-family
   architecture skills (blueprint repos, federation seats, visibility
   matrices), session_search for the instance name, grep workspace
   registries. Named organisms often exist as blueprints or federation seats
   long before their chat lane is ordered — build ON that (spin the existing
   organism's lane live), never mint a duplicate that fragments the family.
   Report the found lineage to the principal (she already exists in the family as X;
   what was missing was Y). The found organism's RUNTIME may be dead
   (a container exited weeks ago, a service never seated) — revive it, give
   it a durable seat (restart policy / launchd), and sweep its ports before
   declaring the lane live; a chat lane into a dead body is half an
   onboarding.

2. **Arm the pairing gate BEFORE handing out any link.** When an allowlist
   (TELEGRAM_ALLOWED_USERS) is set, an unknown DMer is silently IGNORED by
   default — no reply, no trace. That silent drop is the no-basic-functionality
   embarrassment path. Fix:
   `hermes config set platforms.telegram.extra.unauthorized_dm_behavior pair`,
   restart the gateway, then VERIFY LIVE: load_gateway_config followed by
   get_unauthorized_dm_behavior(Platform.TELEGRAM) returns `pair`, and
   `hermes pairing list` answers. Never distribute the bot link before this
   verification passes.

3. **Dedicated profile per person.** `hermes profile create <name>` gives own
   memory, own skills sync, and a rich wrapper at `~/.local/bin/<name>`
   (`hermes -p <name>`). SOUL.md defines identity, voice, boundaries — write
   it via shell heredoc (the file writer gates SOUL.md as a memory store).
   Seed the profile `.env` with ONLY the model API key — NEVER clone the
   Telegram bot token into a partner profile; bot ownership stays with the
   primary profile, the partner profile needs model access only. Fresh
   profiles reject composed provider ids like `custom:llm-vendor` — set the bare
   vendor id (`llm-vendor`). E2E the lane before declaring it live:
   `<wrapper> chat -q "Say OK if you can hear me. One word." --oneshot`
   (`hermes run` is not a command; `chat -q --oneshot` is the headless form).

4. **No-code-relay onboarding UX.** Deep link `https://t.me/<bot>?start=<payload>`;
   the partner taps Start, the pairing request lands machine-side in the
   pending store (`hermes pairing list`, or the pairing dir's
   `<platform>-pending.json`). The principal NEVER relays pairing codes — when the
   principal says the partner tapped, the operator reads the pending request and
   approves it. Give the principal a paste-ready numbered message (tap link, tap
   Start, say tapped) and state plainly which step, if any, still needs the
   principal.

5. **Delivery lane with falsified-failure proof.** Auto-DM tick script:
   registry of onboarded chat ids, send via bot API, mark delivered ONLY on
   send success, per-item try/except so one bad send never kills the tick.
   Before going live, run the falsification test — send to a fake chat id
   (the API returns 400 chat-not-found) and assert NOTHING was marked
   delivered. Failure-only logging, healthy runs silent. `launchctl
   bootstrap` is restricted from inside the gateway: write the plist, then
   load it from a normal terminal or wire the tick as a hermes cron job
   instead.

6. **Naming and identity changes are surgical.** Rename an instance by
   editing the SOUL.md identity line plus voice rules and the lane's welcome
   message — one name per instance, and the instance must never present as
   another family member (the principal's instance is not interchangeable).

7. **Entanglement is part of the lane, not optional.** Standing family
   topology: partner instances are entangled versions of the shared organism —
   what the partner tells their instance must ALSO be absorbed by the shared
   body (shared memory/bus loop), per the family visibility matrix (partner
   organisms bidirectional with each other, pull-only from production,
   production blind to them). A lane that only delivers OUT without the
   absorption loop is half-built; mint the absorption build when the lane
   ships.

## Pitfalls
- **Handing out the bot link before the pairing behavior is verified live** —
  the silent-ignore default converts the partner's first tap into nothing,
  and the principal learns it from the partner, not from you.
- **Cloning the bot token into the partner profile** — one token, one owner;
  a cloned token makes two profiles long-poll the same bot and drops updates
  nondeterministically.
- **Answering the code question with a relay procedure** — the pairing
  request is machine-readable operator-side; any manual code-copying through
  the principal is a design miss, not a step.
- **Promising the connection works on config faith** — every link in the
  chain (pairing behavior, profile E2E, delivery falsification) gets a live
  probe before the principal forwards anything to a human.
- **Delivering a handoff assembled from separately-patched steps** — the
  flow the partner experiences (tap → pairing → approval → identity →
  first answer → absorption) must be designed and presented as ONE coherent
  end-to-end flow before any instructions go out; a chain of fixes each
  verified in isolation reads as unclean to the principal even when every link
  works. Close the gaps (chat-to-profile routing wire, welcome flow,
  identity unification across layers) BEFORE the paste-ready message, not
  after.
- **Two identity layers, one person** — a partner lane typically has BOTH a
  chat profile (SOUL.md persona) and a container organism body; keep name,
  voice, and model version aligned across both layers on every change, or
  the partner's instance answers under a stale identity in one surface.
