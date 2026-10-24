---
name: hermes-agent
description: "Configure, extend, or contribute to the operator agent Agent."
version: 2.1.0
author: the operator agent Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, setup, configuration, multi-agent, spawning, cli, gateway, development]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [claude-code, codex, sibling-agent]
---

# the operator agent Agent

the operator agent Agent is an open-source AI agent framework by Nous Research that runs in your terminal, messaging platforms, and IDEs. It belongs to the same category as Claude Code (Anthropic), Codex (OpenAI), and OpenClaw — autonomous coding and task-execution agents that use tool calling to interact with your system. the operator agent works with any LLM provider (OpenRouter, Anthropic, OpenAI, DeepSeek, local models, and 15+ others) and runs on Linux, macOS, and WSL.

What makes the operator agent different:

- **Self-improving through skills** — the operator agent learns from experience by saving reusable procedures as skills. When it solves a complex problem, discovers a workflow, or gets corrected, it can persist that knowledge as a skill document that loads into future sessions. Skills accumulate over time, making the agent better at your specific tasks and environment.
- **Skill authoring and curation** — write class-level umbrella skills with concise SKILL.md guidance and push session-specific detail into `references/`, `templates/`, and `scripts/`. Use this when refining, merging, or maintaining the skill library itself.
- **Persistent memory across sessions** — remembers who you are, your preferences, environment details, and lessons learned. Pluggable memory backends (built-in, Honcho, Mem0, and more) let you choose how memory works.
- **Multi-platform gateway** — the same agent runs on Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, and 10+ other platforms with full tool access, not just chat.
- **Provider-agnostic** — swap models and providers mid-workflow without changing anything else. Credential pools rotate across multiple API keys automatically.
- **Profiles** — run multiple independent the operator agent instances with isolated configs, sessions, skills, and memory.
- **Extensible** — plugins, MCP servers, custom tools, webhook triggers, cron scheduling, and the full Python ecosystem.

People use the operator agent for software development, research, system administration, data analysis, content creation, home automation, and anything else that benefits from an AI agent with persistent context and full system access.

**This skill helps you work with the operator agent Agent effectively** — setting it up, configuring features, spawning additional agent instances, troubleshooting issues, finding the right commands and settings, and understanding how the system works when you need to extend or contribute to it.

**Memory layering note:** For engine-specific memory, use a shared baseline plus per-engine overlays, then render the final view with a merge step instead of trying to make memory files recursively include each other. See `references/layered-memory-stacks.md`.

## Troubleshooting JavaScript in HTML Files

When working with HTML prototypes that contain embedded JavaScript (especially in script tags), you may encounter syntax errors related to template literals (backticks).

**Common Issue**: "Unexpected token" errors when JavaScript engine encounters template literals in certain contexts.

**Workaround**: Replace template literals with string concatenation:
- Instead of: `` `text ${variable} text` ``
- Use: `'text ' + variable + ' text'`

**Why this works**: Some JavaScript parsers in embedded contexts (like when extracting script content from HTML) may not properly handle ES6 template literals, even when the target environment supports them.

**Verification**: After making this change, test that the JavaScript executes correctly and produces the same output.

**Honcho/OpenRouter triage:** when a memory or deriver service has an OpenAI-style missing-key error but the machine has OpenRouter credentials, inspect the resolved config and proxy base URL instead of only the raw env file. See `references/honcho-openrouter-memory-dialectic.md`.

**Model Provider Switching:** when the operator agent routes through the wrong provider (e.g., OpenRouter instead of a configured Z.ai LLM), use `hermes config set` to update `model.provider`, `model.default`, and `model.base_url`. See `references/model-provider-switching.md`.

**Telegram + Kanban Integration:** principal-interface profile as single Patient 0 entry point with kanban-orchestrator. See `references/telegram-kanban-integration.md`.

**Clinical Engine Identity Hardening:** the specialist engine (Bernard) explicit AI identity on every endpoint. See `references/clinical-engine-identity-hardening.md`.

**Body Engine Fleet Setup:** 7-engine + registry profile architecture. See `references/body-engine-fleet-setup.md`.

**the principal Interface Deployment:** Patient 0 single Telegram entry point with kanban-orchestrator. See `references/principal-interface-deployment.md`.

**Gateway Lifecycle Management:** macOS launchd quirks and clean restart patterns. See `references/gateway-lifecycle-management.md`.

**Engine Registry Patterns:** Morphogen registry registration and heartbeat patterns. See `references/engine-registry-patterns.md`.

**Kanban Auto-Creation Pattern:** SOUL.md instruction approach for auto-creating Kanban tasks from gateway messages. See `references/kanban-auto-creation-pattern.md`.

**Docs:** https://hermes-agent.nousresearch.com/docs/

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Interactive chat (default)
hermes

# Single query
hermes chat -q "What is the capital of France?"

# Setup wizard
hermes setup

# Change model/provider
hermes model

# Check health
hermes doctor
```

---

## CLI Reference

### Global Flags

```
hermes [flags] [command]

  --version, -V             Show version
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --pass-session-id         Include session ID in system prompt
```

No subcommand defaults to `chat`.

### Chat

```
hermes chat [flags]
  -q, --query TEXT          Single query, non-interactive
  -m, --model MODEL         Model (e.g. anthropic/claude-sonnet-4)
  -t, --toolsets LIST       Comma-separated toolsets
  --provider PROVIDER       Force provider (openrouter, anthropic, nous, etc.)
  -v, --verbose             Verbose output
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --source TAG              Session source tag (default: cli)
```

### Configuration

```
hermes setup [section]      Interactive wizard (model|terminal|gateway|tools|agent)
hermes model                Interactive model/provider picker
hermes config               View current config
hermes config edit          Open config.yaml in $EDITOR
hermes config set KEY VAL   Set a config value
hermes config path          Print config.yaml path
hermes config env-path      Print .env path
hermes config check         Check for missing/outdated config
hermes config migrate       Update config with new options
hermes auth                 Interactive credential manager
hermes auth add PROVIDER    Add OAuth or API-key credential (e.g. nous, openai-codex, qwen-oauth)
hermes auth list            List stored credentials
hermes auth remove PROVIDER Remove a stored credential
hermes doctor [--fix]       Check dependencies and config
hermes status [--all]       Show component status
```

### Tools & Skills

```
hermes tools                Interactive tool enable/disable (curses UI)
hermes tools list           Show all tools and status
hermes tools enable NAME    Enable a toolset
hermes tools disable NAME   Disable a toolset

hermes skills list          List installed skills
hermes skills search QUERY  Search the skills hub
hermes skills install ID    Install a skill (ID can be a hub identifier OR a direct https://…/SKILL.md URL; pass --name to override when frontmatter has no name)
hermes skills inspect ID    Preview without installing
hermes skills config        Enable/disable skills per platform
hermes skills check         Check for updates
hermes skills update        Update outdated skills
hermes skills uninstall N   Remove a hub skill
hermes skills publish PATH  Publish to registry
hermes skills browse        Browse all available skills
hermes skills tap add REPO  Add a GitHub repo as skill source
```

### MCP Servers

```
hermes mcp serve            Run the operator agent as an MCP server
hermes mcp add NAME         Add an MCP server (--url or --command)
hermes mcp remove NAME      Remove an MCP server
hermes mcp list             List configured servers
hermes mcp test NAME        Test connection
hermes mcp configure NAME   Toggle tool selection
```

### Gateway (Messaging Platforms)

```
hermes gateway run          Start gateway foreground
hermes gateway install      Install as background service
hermes gateway start/stop   Control the service
hermes gateway restart      Restart the service
hermes gateway status       Check status
hermes gateway setup        Configure platforms
```

Supported platforms: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Home Assistant, DingTalk, Feishu, WeCom, BlueBubbles (iMessage), Weixin (WeChat), API Server, Webhooks. Open WebUI connects via the API Server adapter.

Platform docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

### Sessions

```
hermes sessions list        List recent sessions
hermes sessions browse      Interactive picker
hermes sessions export OUT  Export to JSONL
hermes sessions rename ID T Rename a session
hermes sessions delete ID   Delete a session
hermes sessions prune       Clean up old sessions (--older-than N days)
hermes sessions stats       Session store statistics
```

### Cron Jobs

```bash
hermes cron list            List jobs (--all for disabled)
hermes cron create SCHED    Create: '30m', 'every 2h', '0 9 * * *'
hermes cron edit ID         Edit schedule, prompt, delivery
hermes cron pause/resume ID Control job state
hermes cron run ID          Trigger on next tick
hermes cron remove ID       Delete a job
hermes cron status          Scheduler status
```

*Note: When managing OpenClaw cron jobs, verify job existence in live system before editing (see references/sibling-agent-cron-verification.md)*

**Note:** For OpenClaw cron job management, see the verification guide in `references/sibling-agent-cron-verification.md` to avoid editing non-existent jobs.

### Webhooks

```
hermes webhook subscribe N  Create route at /webhooks/<name>
hermes webhook list         List subscriptions
hermes webhook remove NAME  Remove a subscription
hermes webhook test NAME    Send a test POST
```

### Profiles

```
hermes profile list         List all profiles
hermes profile create NAME  Create (--clone, --clone-all, --clone-from)
hermes profile use NAME     Set sticky default
hermes profile delete NAME  Delete a profile
hermes profile show NAME    Show details
hermes profile alias NAME   Manage wrapper scripts
hermes profile rename A B   Rename a profile
hermes profile export NAME  Export to tar.gz
hermes profile import FILE  Import from archive
```

### Credential Pools

```
hermes auth add             Interactive credential wizard
hermes auth list [PROVIDER] List pooled credentials
hermes auth remove P INDEX  Remove by provider + index
hermes auth reset PROVIDER  Clear exhaustion status
```

### Other

```
hermes insights [--days N]  Usage analytics
hermes update               Update to latest version
hermes pairing list/approve/revoke  DM authorization
hermes plugins list/install/remove  Plugin management
hermes honcho setup/status  Honcho memory integration (requires honcho plugin)
hermes memory setup/status/off  Memory provider config
hermes completion bash|zsh  Shell completions
hermes acp                  ACP server (IDE integration)
hermes claw migrate         Migrate from OpenClaw
hermes uninstall            Uninstall the operator agent
```

---

## Slash Commands (In-Session)

Type these during an interactive chat session. New commands land fairly
often; if something below looks stale, run `/help` in-session for the
authoritative list or see the [live slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands).
The registry of record is `hermes_cli/commands.py` — every consumer
(autocomplete, Telegram menu, Slack mapping, `/help`) derives from it.

### Session Control
```
/new (/reset)        Fresh session
/clear               Clear screen + new session (CLI)
/retry               Resend last message
/undo                Remove last exchange
/title [name]        Name the session
/compress            Manually compress context
/stop                Kill background processes
/rollback [N]        Restore filesystem checkpoint
/snapshot [sub]      Create or restore state snapshots of the operator agent config/state (CLI)
/background <prompt> Run prompt in background
/queue <prompt>      Queue for next turn
/steer <prompt>      Inject a message after the next tool call without interrupting
/agents (/tasks)     Show active agents and running tasks
/resume [name]       Resume a named session
/goal [text|sub]     Set a standing goal the operator agent works on across turns until achieved
                     (subcommands: status, pause, resume, clear)
/redraw              Force a full UI repaint (CLI)
```

### Configuration
```
/config              Show config (CLI)
/model [name]        Show or change model
/personality [name]  Set personality
/reasoning [level]   Set reasoning (none|minimal|low|medium|high|xhigh|show|hide)
/verbose             Cycle: off → new → all → verbose
/voice [on|off|tts]  Voice mode
/yolo                Toggle approval bypass
/busy [sub]          Control what Enter does while the operator agent is working (CLI)
                     (subcommands: queue, steer, interrupt, status)
/indicator [style]   Pick the TUI busy-indicator style (CLI)
                     (styles: kaomoji, emoji, unicode, ascii)
/footer [on|off]     Toggle gateway runtime-metadata footer on final replies
/skin [name]         Change theme (CLI)
/statusbar           Toggle status bar (CLI)
```

### Tools & Skills
```
/tools               Manage tools (CLI)
/toolsets            List toolsets (CLI)
/skills              Search/install skills (CLI)
/skill <name>        Load a skill into session
/reload-skills       Re-scan skills-library/ for added/removed skills
/reload              Reload .env variables into the running session (CLI)
/reload-mcp          Reload MCP servers
/cron                Manage cron jobs (CLI)
/curator [sub]       Background skill maintenance (status, run, pin, archive, …)
/kanban [sub]        Multi-profile collaboration board (tasks, links, comments)
/plugins             List plugins (CLI)
```

### Gateway
```
/approve             Approve a pending command (gateway)
/deny                Deny a pending command (gateway)
/restart             Restart gateway (gateway)
/sethome             Set current chat as home channel (gateway)
/update              Update the operator agent to latest (gateway)
/topic [sub]         Enable or inspect Telegram DM topic sessions (gateway)
/platforms (/gateway) Show platform connection status (gateway)
```

### Utility
```
/branch (/fork)      Branch the current session
/fast                Toggle priority/fast processing
/browser             Open CDP browser connection
/history             Show conversation history (CLI)
/save                Save conversation to file (CLI)
/copy [N]            Copy the last assistant response to clipboard (CLI)
/paste               Attach clipboard image (CLI)
/image               Attach local image file (CLI)
```

### Info
```
/help                Show commands
/commands [page]     Browse all commands (gateway)
/usage               Token usage
/insights [days]     Usage analytics
/gquota              Show Google Gemini Code Assist quota usage (CLI)
/status              Session info (gateway)
/profile             Active profile info
/debug               Upload debug report (system info + logs) and get shareable links
```

### Exit
```
/quit (/exit, /q)    Exit CLI
```

---

## Key Paths & Config

```
<agent-home>/config.yaml       Main configuration
<agent-home>/.env              API keys and secrets
$HERMES_HOME/skills/        Installed skills
<agent-home>/sessions/         Gateway routing index, request dumps, *.jsonl transcripts (and optional per-session JSON snapshots when sessions.write_json_snapshots: true)
<agent-home>/state.db          Canonical session store (SQLite + FTS5)
<agent-home>/logs/             Gateway and error logs
<agent-home>/auth.json         OAuth tokens and credential pools
<agent-home>/hermes-agent/     Source code (if git-installed)
```

Profiles use `<agent-home>/profiles/<name>/` with the same layout.

### Config Sections

Edit with `hermes config edit` or `hermes config set section.key value`.

| Section | Key options |
|---------|-------------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement` |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral) |
| `tts` | `provider` (edge/elevenlabs/openai/minimax/mistral/neutts) |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` |
| `security` | `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort` |
| `checkpoints` | `enabled`, `max_snapshots` (50) |\n\nFull config reference: https://hermes-agent.nousresearch.com/docs/user-guide/configuration\n\n## Communication Best Practices\n\nEffective communication is key to productive sessions. Follow these guidelines to ensure clarity and efficiency:\n\n### Acknowledge and Move Forward\n- When the user indicates understanding (e.g., "I got it now," "That makes sense," "OK"), acknowledge briefly and move on to the next topic or action\n- Avoid repeating information that has already been acknowledged unless specifically asked for clarification or reinforcement\n- This respects the user's time and keeps the conversation focused on progress\n\n### Match Communication Style to User Preferences\n- The user prefers visual diagrams over text for system architecture (consider using the `architecture-diagram` skill)\n- Pay attention to cues about preferred detail level and format\n- Stop repeating acknowledged information\n\n### Evidence-Based Guidance\n- When providing health, wellness, or scientific guidance, emphasize evidence-based, non-diagnostic information\n- Frame advice in terms of general wellness principles rather than medical diagnoses\n- Use metaphors like "principal as metaphor for life leadership" when appropriate to make concepts relatable\n\n### Context-Aware Explanations\n- Tailor explanations to the user's role and context (e.g., CTO vs. end-user vs. researcher)\n- For personal life situations, focus on practical, actionable advice\n- For business contexts, emphasize ROI, scalability, and implementation considerations\n\n### Memory Isolation Awareness\n- Be aware that different life domains (personal, business, etc.) may require different approaches and panel architectures\n- Respect memory isolation between domains when relevant to the task

### Providers

20+ providers supported. Set via `hermes model` or `hermes setup`.

| Provider | Auth | Key env var |
|----------|------|-------------|
| OpenRouter | API key | `OPENROUTER_API_KEY` |
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes auth` |
| OpenAI Codex | OAuth | `hermes auth` |
| GitHub Copilot | Token | `COPILOT_GITHUB_TOKEN` |
| Google Gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| xAI / Grok | API key | `XAI_API_KEY` |
| Hugging Face | Token | `HF_TOKEN` |
| Z.AI / LLM | API key | `GLM_API_KEY` |
| MiniMax | API key | `MINIMAX_API_KEY` |
| MiniMax CN | API key | `MINIMAX_CN_API_KEY` |
| Kimi / Moonshot | API key | `KIMI_API_KEY` |
| Alibaba / DashScope | API key | `DASHSCOPE_API_KEY` |
| Xiaomi MiMo | API key | `XIAOMI_API_KEY` |
| Kilo Code | API key | `KILOCODE_API_KEY` |
| OpenCode Zen | API key | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | API key | `OPENCODE_GO_API_KEY` |
| Qwen OAuth | OAuth | `hermes auth add qwen-oauth` |
| Custom endpoint | Config | `model.base_url` + `model.api_key` in config.yaml |
| GitHub Copilot ACP | External | `COPILOT_CLI_PATH` or Copilot CLI |

Full provider docs: https://hermes-agent.nousresearch.com/docs/integrations/providers

### Toolsets

Enable/disable via `hermes tools` (interactive) or `hermes tools enable/disable NAME`.

| Toolset | What it provides |
|---------|-----------------|
| `web` | Web search and content extraction |
| `search` | Web search only (subset of `web`) |
| `browser` | Browser automation (Browserbase, Camofox, or local Chromium) |
| `terminal` | Shell commands and process management |
| `file` | File read/write/search/patch |
| `code_execution` | Sandboxed Python execution |
| `vision` | Image analysis |
| `image_gen` | AI image generation |
| `video` | Video analysis and generation |
| `tts` | Text-to-speech |
| `skills` | Skill browsing and management |
| `memory` | Persistent cross-session memory |
| `session_search` | Search past conversations |
| `delegation` | Subagent task delegation |
| `cronjob` | Scheduled task management |
| `clarify` | Ask user clarifying questions |
| `messaging` | Cross-platform message sending |
| `todo` | In-session task planning and tracking |
| `kanban` | Multi-agent work-queue tools (gated to workers) |
| `debugging` | Extra introspection/debug tools (off by default) |
| `safe` | Minimal, low-risk toolset for locked-down sessions |
| `spotify` | Spotify playback and playlist control |
| `homeassistant` | Smart home control (off by default) |
| `discord` | Discord integration tools |
| `discord_admin` | Discord admin/moderation tools |
| `feishu_doc` | Feishu (Lark) document tools |
| `feishu_drive` | Feishu (Lark) drive tools |
| `yuanbao` | Yuanbao integration tools |
| `rl` | Reinforcement learning tools (off by default) |
| `moa` | Mixture of Agents (off by default) |

Full enumeration lives in `toolsets.py` as the `TOOLSETS` dict; `_HERMES_CORE_TOOLS` is the default bundle most platforms inherit from.

Tool changes take effect on `/reset` (new session). They do NOT apply mid-conversation to preserve prompt caching.

---

## Security & Privacy Toggles

Common "why is the operator agent doing X to my output / tool calls / commands?" toggles — and the exact commands to change them. Most of these need a fresh session (`/reset` in chat, or start a new `hermes` invocation) because they're read once at startup.

### Secret redaction in tool output

Secret redaction is **on by default** — tool output (terminal stdout, `read_file`, web content, subagent summaries, etc.) is scanned for strings that look like API keys, tokens, and secrets before it enters the conversation context and logs. Leave it enabled for normal use:

```bash
hermes config set security.redact_secrets true       # keep enabled globally
```

**Restart required.** `security.redact_secrets` is snapshotted at import time — toggling it mid-session (e.g. via `export HERMES_REDACT_SECRETS=false` from a tool call) will NOT take effect for the running process. Tell the user to change it in config from a terminal, then start a new session. This is deliberate — it prevents an LLM from flipping the toggle on itself mid-task.

Disable only when you deliberately need raw credential-like strings for debugging or redactor development:
```bash
hermes config set security.redact_secrets false
```

### PII redaction in gateway messages

Separate from secret redaction. When enabled, the gateway hashes user IDs and strips phone numbers from the session context before it reaches the model:

```bash
hermes config set privacy.redact_pii true    # enable
hermes config set privacy.redact_pii false   # disable (default)
```

### Command approval prompts

By default (`approvals.mode: manual`), the operator agent prompts the user before running shell commands flagged as destructive (`rm -rf`, `git reset --hard`, etc.). The modes are:

- `manual` — always prompt (default)
- `smart` — use an auxiliary LLM to auto-approve low-risk commands, prompt on high-risk
- `off` — skip all approval prompts (equivalent to `--yolo`)

```bash
hermes config set approvals.mode smart       # recommended middle ground
hermes config set approvals.mode off         # bypass everything (not recommended)
```

Per-invocation bypass without changing config:
- `hermes --yolo …`
- `export HERMES_YOLO_MODE=1`

Note: YOLO / `approvals.mode: off` does NOT turn off secret redaction. They are independent.

### Shell hooks allowlist

Some shell-hook integrations require explicit allowlisting before they fire. Managed via `<agent-home>/shell-hooks-allowlist.json` — prompted interactively the first time a hook wants to run.

### Disabling the web/browser/image-gen tools

To keep the model away from network or media tools entirely, open `hermes tools` and toggle per-platform. Takes effect on next session (`/reset`). See the Tools & Skills section above.

---

## Voice & Transcription

### STT (Voice → Text)

Voice messages from messaging platforms are auto-transcribed.

Provider priority (auto-detected):
1. **Local faster-whisper** — free, no API key: `pip install faster-whisper`
2. **Groq Whisper** — free tier: set `GROQ_API_KEY`
3. **OpenAI Whisper** — paid: set `VOICE_TOOLS_OPENAI_KEY`
4. **Mistral Voxtral** — set `MISTRAL_API_KEY`

**Performance Note**: For faster transcription (especially on CPU), use the `tiny` model. Trade-off: slightly lower accuracy but significantly faster processing. For critical transcription accuracy, use `base` or higher.

Config:
```yaml
stt:
  enabled: true
  provider: local        # local, groq, openai, mistral
  local:
    model: tiny          # Use 'tiny' for fastest CPU performance, 'base' for better accuracy
```
```
### TTS (Text → Voice)

| Provider | Env var | Free? |
|----------|---------|-------|
| Edge TTS | None | Yes (default) |
| ElevenLabs | `ELEVENLABS_API_KEY` | Free tier |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | Paid |
| MiniMax | `MINIMAX_API_KEY` | Paid |
| Mistral (Voxtral) | `MISTRAL_API_KEY` | Paid |
| NeuTTS (local) | None (`pip install neutts[all]` + `espeak-ng`) | Free |

Voice commands: `/voice on` (voice-to-voice), `/voice tts` (always voice), `/voice off`.

---\n\n## Communication Best Practices\n\nEffective communication is key to productive sessions. Follow these guidelines to ensure clarity and efficiency:\n\n### Acknowledge and Move Forward\n- When the user indicates understanding (e.g., \"I got it now,\" \"That makes sense,\" \"OK\"), acknowledge briefly and move on to the next topic or action\n- Avoid repeating information that has already been acknowledged unless specifically asked for clarification or reinforcement\n- This respects the user's time and keeps the conversation focused on progress\n\n### Match Communication Style to User Preferences\n- Some users prefer visual diagrams over text for system architecture (consider using the `architecture-diagram` skill)\n- Others may prefer concise bullet points over detailed paragraphs\n- Pay attention to cues about preferred detail level and format\n\n### Evidence-Based Guidance\n- When providing health, wellness, or scientific guidance, emphasize evidence-based, non-diagnostic information\n- Frame advice in terms of general wellness principles rather than medical diagnoses\n- Use metaphors like \"principal as metaphor for life leadership\" when appropriate to make concepts relatable\n\n### Context-Aware Explanations\n- Tailor explanations to the user's role and context (e.g., CTO vs. end-user vs. researcher)\n- For personal life situations, focus on practical, actionable advice\n- For business contexts, emphasize ROI, scalability, and implementation considerations\n\n### Memory Isolation Awareness\n- Be aware that different life domains (personal, business, etc.) may require different approaches and panel architectures\n- Respect memory isolation between domains when relevant to the task\n\n## Specialized Work and Profiles\n\nFor engine builds, rebuilds, audits, and significant code work:\n\n- Always work under elite specialist profiles — never the general assistant\n- Switch personas to cover all angles (systems architect, physicist, distributed systems engineer, QA architect)\n- Use different models for different specialties\n- The general assistant orchestrates and delivers results, but the actual build/review work goes through the right architectural brain\n\n## Revolutionary Features and P0 Items\n\nAction items for advancing the DS organism:\n\n### Revolutionary Features\n- **Metabolic economy**: Organism manages computational resources like a body manages energy - triages when scarce, grows when abundant (Harvey engine's deeper purpose)\n- **Dreaming / offline consolidation**: During low-activity periods, consolidate memory, optimize coupling, and rehearse scenarios (TD Learning + offline replay loop)\n- **Symbiotic relationships**: Multiple organisms share anonymized learnings through the Grandmother (like immune systems sharing antibody information)\n- **Evolutionary pressure**: Product babies that perform well feed evolutionary information back to the Grandmother to adjust coupling matrix for future births\n\n### P0 Items (Action Required)\n- **TD Learning wiring**: Wire the self-improving coaching policy into the Wave engine loop (organism's neuroplasticity)\n- **Persistence layer**: Replace in-memory dicts with fleet-wide store (SQLite local, PostgreSQL cloud) for cross-restart memory\n- **Birth canal**: Build the actual birth pipeline from 'idea in brain' to 'product baby with DS DNA' (idea → spec → DNA injection → compiled product)\n\n---\n\n## Spawning Additional the operator agent Instances

Run additional the operator agent processes as fully independent subprocesses — separate sessions, tools, and environments.

## the specialist engine Maintenance

When working with the Divinity Science (DS) engine fleet, particularly for fixing Layer 4 methodology endpoints that return empty `{}`:

### Core Principles
- **Always work in small batches** - never attempt to fix all engines at once
- **Always verify you finish everything** - track what's been fixed and what remains
- **Never break the system** - backup first, test changes incrementally
- **Working prototypes over docs** - prioritize getting endpoints returning live data in the browser

### Layer 4 Methodology Fix Procedure
When engines return empty `{}` on `/v1/layers` endpoint:

1. **Backup first**: Copy `src/api/server.py` to `src/api/server.py.bak` for each engine
2. **Diagnose the issue**: Check if `mount_methodology_endpoints(app, ...)` is called BEFORE `app = FastAPI(`
3. **Apply the fix**: Move the mount call to AFTER app creation:
   ```python
   # WRONG (too early):
   app = FastAPI(
       from methodology_api import mount_methodology_endpoints  # SYNTAX ERROR
       mount_methodology_endpoints(app, "engine-name", "module")  # SYNTAX ERROR
   )
   
   # CORRECT (after app creation):
   app = FastAPI(
       title="the specialist engine",
       version="1.0.0",
       description="Engine description",
   )
   
   # Layer 4: Methodology API
   from methodology_api import mount_methodology_endpoints
   mount_methodology_endpoints(app, "engine-name", "module")
   ```
4. **Verify syntax**: `python3 -c "compile(open('server.py').read(), 'server.py', 'exec')"`
5. **Restart engine**: Kill existing process, start fresh instance
6. **Verify fix**: `curl -s http://127.0.0.1:<port>/v1/layers` should return populated JSON with institutions > 0

### Engine Fleet Work Patterns
- **Delegation limitations**: For mechanical fixes involving many similar files, consider writing a verification script yourself rather than delegating - delegation often times out on volume work
- **Directory structure awareness**: Not all engines follow the same naming pattern; verify actual directory names before attempting restarts
- **Process management**: Use `lsof -ti :<port>` to find and kill existing processes before restarting
- **Import path correctness**: Some engines import from `engine.core` while others use `core.engine` - match the working engines' pattern

### Building New the specialist engine
When creating new Divinity Science engines (like the specialist engine, the specialist engine, the specialist engine), follow these patterns:

**Naming Convention**: 
- Refer to engines by scientist names only (the specialist engine, the specialist engine, the specialist engine) as a "tip of the hat" to their contributions
- Avoid appending functional descriptions in verbal/written references (e.g., not "the specialist engine (Genome)")
- Functional roles are encoded in the ECS registry and engine metadata

**Engine Building Pattern** (follow the Goethe engine template exactly):
1. Create directory structure: `ds-<engine-name>-engine/` with:
   - `run_server.py` (uvicorn launcher on specific port)
   - `requirements.txt` (fastapi, uvicorn, pydantic, numpy<2)
   - `src/__init__.py`, `src/api/__init__.py`, `src/<engine>/__init__.py` (empty package markers)
   - `src/<engine>/core/__init__.py` (exports from engine.py)
   - `src/<engine>/core/engine.py` (core science with Engine dataclass and `_engine` singleton)
   - `src/<engine>/core/methodology.py` (Layer 4 with institutions, methodologies, model routes, personalities)
   - `src/api/server.py` (FastAPI with /health, /v1/vitals, and domain-specific endpoints)
   - `VERSION.md`
   - `~/Library/LaunchAgents/com.divinityscience.<engine>.plist` (launchd agent)
   - `logs/` directory

**ECS Registry Fix** (critical for clean imports):
When adding a new engine to `/<workspace>`:
- Add entry to `FLEET_REGISTRY` using `_entry()` pattern
- **Crucially**: Also add the engine key to the `_C` dict using `_code()` to prevent `KeyError` on import
- Example: 
  ```python
  _C = {
      # ... existing entries
      "genome": _code(2, 10, 1),      # the specialist engine
      "placenta": _code(2, 10, 2),    # the specialist engine  
      "maturation": _code(2, 10, 3),  # the specialist engine
      # ... other entries
  }
  
  FLEET_REGISTRY = {
      # ... existing entries
      "ds-genome-engine": _entry(
          key="genome",
          directory="ds-genome-engine",
          name="the specialist engine",
          port=8129,
          scientist="Rosalind Franklin",
          # ... other params
      ),
      # ... other entries
  }
  ```
- Verification: `python3 -c "import sys; sys.path.insert(0, '/path/to/ds-engine-registry'); from ecs import FLEET_REGISTRY; print(f'Total engines: {len([k for k,v in FLEET_REGISTRY.items() if not v.get(\"renamed_to\")])}')"` should show clean import and correct count

### Verification Checklist
After fixing an engine:
- [ ] Server.py has correct syntax (no indentation errors)
- [ ] Mount method call appears AFTER `app = FastAPI(...)`
- [ ] Engine process is running on the correct port
- [ ] `/v1/layers` returns populated JSON (institutions > 0)
- [ ] Other layers (1, 2, 3) still return data
## Specialized Work and Profiles

For engine builds, rebuilds, audits, and significant code work:

- Always work under elite specialist profiles — never the general assistant
- Switch personas to cover all angles (systems architect, physicist, distributed systems engineer, QA architect)
- Use different models for different specialties
- The general assistant orchestrates and delivers results, but the actual build/review work goes through the right architectural brain

### Conducting Methodology Audits (the specialist engine)

When performing methodology quality and research integrity audits (similar to the the specialist engine role):

1. **Canonical System Verification**: Always check that all components adhere to the canonical tier system:
   - Labels: Thriving / Flourishing / Stable / Developing / Strained / Distressed / Crisis
   - Verify threshold mappings in calculators, reporters, and display layers
   - Ensure proportional scaling is consistent (0-100 vs 0-1 scales)

2. **Mathematical Rigor Checks**:
   - Verify RNG seeding practices (avoid fixed seeds that remove stochasticity)
   - Check coupling mathematics and parameter values for correctness
   - Validate entropy calculations and statistical tests (e.g., KS tests for scale-free networks)
   - Examine rescore engines for inflation, double-counting, and tier consistency issues

3. **Evidence-Based Validation**:
   - Any claim of "N citations" must list N citations with author, year, journal, DOI/URL
   - Verify citation counts match actual references (severity-1 violation if not)
   - Check for ghost citations or unverified claims in marketing materials

4. **Component-Specific Audits**:
   - **Wave Engine (Kuramoto)**: Check RNG seeding, coupling math, parameter values
   - **Crystal Engine (Lattice)**: Validate scale_free.py KS test, entropy calculations
   - **Rescore Engine**: Check for inflation, double-counting, tier consistency
   - **Calculator/Reporting**: Verify tier labels match canonical system
   - **VERITAS Process**: Confirm calibration gates are documented
   - **Marketing Docs**: Scan for ghost citations, unverified claims, inflated citation counts

5. **Communication of Findings**:
   - Use the exact audit report format specified in the specialist engine protocols
   - Be specific: file path, line numbers, exact code, exact fix instructions
   - Mark severity levels clearly (1=critical, 2=major, 3=minor)
   - Include status tracking (OPEN/FIXED) for findings across audit runs

### When to Use This vs delegate_task

| | `delegate_task` | Spawning `hermes` process |
|-|-----------------|--------------------------|
| Isolation | Separate conversation, shared process | Fully independent process |
| Duration | Minutes (bounded by parent loop) | Hours/days |
| Tool access | Subset of parent's tools | Full tool access |
| Interactive | No | Yes (PTY mode) |
| Use case | Quick parallel subtasks | Long autonomous missions |

### One-Shot Mode

```
terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)

# Background for long tasks:
terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)
```

### Interactive PTY Mode (via tmux)

the operator agent uses prompt_toolkit, which requires a real terminal. Use tmux for interactive spawning:

```
# Start
terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)

# Wait for startup, then send a message
terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)

# Read output
terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)

# Send follow-up
terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)

# Exit
terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)
```

### Multi-Agent Coordination

```
# Agent A: backend
terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)

# Agent B: frontend
terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)

# Check progress, relay context between them
terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)
terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)
```

### Session Resume

```
# Resume most recent session
terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)

# Resume specific session
terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)
```

### Tips
### Tips
- **Prefer `delegate_task` for quick subtasks** — less overhead than spawning a full process
- **Use `-w` (worktree mode)** when spawning agents that edit code — prevents git conflicts
- **Set timeouts** for one-shot mode — complex tasks can take 5-10 minutes
- **Use `hermes chat -q` for fire-and-forget** — no PTY needed
- **Use tmux for interactive sessions** — raw PTY mode has `\\r` vs `\\n` issues with prompt_toolkit
- **For scheduled tasks**, use the `cronjob` tool instead of spawning — handles delivery and retry
- **For volume mechanical work** (fixing many similar files), consider writing a verification script yourself rather than delegating - delegation often times out
- **For engine builds, rebuilds, audits, and significant code work**: always work under elite specialist profiles — never the general assistant

---

## Durable & Background Systems

Four systems run alongside the main conversation loop. Quick reference
here; full developer notes live in `AGENTS.md`, user-facing docs under
`website/docs/user-guide/features/`.

### Gateway startup hooks

Use gateway startup hooks for deterministic boot actions that must run on
process start. Keep them *mechanical*, not agent-interpreted.

- If the boot action is a fixed command or file render, call the command
  directly from the hook rather than spawning a reasoning agent to read a
  checklist and decide what to do.
- Always verify the intended artifact exists after the hook runs.
- For hydra-os memory bootstrapping, see `references/gateway-startup-hook-boot-render.md`.

### Delegation (`delegate_task`)

Synchronous subagent spawn — the parent waits for the child's summary
before continuing its own loop. Isolated context + terminal session.

- **Single:** `delegate_task(goal, context, toolsets)`.
- **Batch:** `delegate_task(tasks=[{goal, ...}, ...])` runs children in
  parallel, capped by `delegation.max_concurrent_children` (default 3).
- **Roles:** `leaf` (default; cannot re-delegate) vs `orchestrator`
  (can spawn its own workers, bounded by `delegation.max_spawn_depth`).
- **Not durable.** If the parent is interrupted, the child is
  cancelled. For work that must outlive the turn, use `cronjob` or
  `terminal(background=True, notify_on_complete=True)`.

Config: `delegation.*` in `config.yaml`.

### Cron (scheduled jobs)

Durable scheduler — `cron/jobs.py` + `cron/scheduler.py`. Drive it via
the `cronjob` tool, the `hermes cron` CLI (`list`, `add`, `edit`,
`pause`, `resume`, `run`, `remove`), or the `/cron` slash command.

- **Schedules:** duration (`"30m"`, `"2h"`), "every" phrase
  (`"every monday 9am"`), 5-field cron (`"0 9 * * *"`), or ISO timestamp.
- **Per-job knobs:** `skills`, `model`/`provider` override, `script`
  (pre-run data collection; `no_agent=True` makes the script the whole
  job), `context_from` (chain job A's output into job B), `workdir`
  (run in a specific dir with its `AGENTS.md` / `CLAUDE.md` loaded),
  multi-platform delivery.
- **Invariants:** 3-minute hard interrupt per run, `.tick.lock` file
  prevents duplicate ticks across processes, cron sessions pass
  `skip_memory=True` by default, and cron deliveries are framed with a
  header/footer instead of being mirrored into the target gateway
  session (keeps role alternation intact).

User docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron

### Curator (skill lifecycle)

Background maintenance for agent-created skills. Tracks usage, marks
idle skills stale, archives stale ones, keeps a pre-run tar.gz backup
so nothing is lost.

- **CLI:** `hermes curator <verb>` — `status`, `run`, `pause`, `resume`,
  `pin`, `unpin`, `archive`, `restore`, `prune`, `backup`, `rollback`.
- **Slash:** `/curator <subcommand>` mirrors the CLI.
- **Scope:** only touches skills with `created_by: "agent"` provenance.
  Bundled + hub-installed skills are off-limits. **Never deletes** —
  max destructive action is archive. Pinned skills are exempt from
  every auto-transition and every LLM review pass.
- **Telemetry:** sidecar at `skills-library/.usage.json` holds
  per-skill `use_count`, `view_count`, `patch_count`,
  `last_activity_at`, `state`, `pinned`.

Config: `curator.*` (`enabled`, `interval_hours`, `min_idle_hours`,
`stale_after_days`, `archive_after_days`, `backup.*`).
User docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/curator

### Kanban (multi-agent work queue)

Durable SQLite board for multi-profile / multi-worker collaboration.
Users drive it via `hermes kanban <verb>`; dispatcher-spawned workers
see a focused `kanban_*` toolset gated by `HERMES_KANBAN_TASK`, and
orchestrator profiles can opt into the broader `kanban` toolset. Normal
sessions still have zero `kanban_*` schema footprint unless configured.

- **CLI verbs (common):** `init`, `create`, `list` (alias `ls`),
  `show`, `assign`, `link`, `unlink`, `comment`, `complete`, `block`,
  `unblock`, `archive`, `tail`. Less common: `watch`, `stats`, `runs`,
  `log`, `dispatch`, `daemon`, `gc`.
- **Worker/orchestrator toolset:** `kanban_show`, `kanban_complete`,
  `kanban_block`, `kanban_heartbeat`, `kanban_comment`, `kanban_create`,
  `kanban_link`; profiles that explicitly enable the `kanban` toolset
  outside a dispatcher-spawned task also get `kanban_list` and
  `kanban_unblock` for board routing.
- **Dispatcher** runs inside the gateway by default
  (`kanban.dispatch_in_gateway: true`) — reclaims stale claims,
  promotes ready tasks, atomically claims, spawns assigned profiles.
  Auto-blocks a task after `failure_limit` consecutive spawn failures
  (default 2; configurable via `kanban.failure_limit` or per-task
  `max_retries`).
- **Isolation:** board is the hard boundary (workers get
  `HERMES_KANBAN_BOARD` pinned in env); tenant is a soft namespace
  within a board for workspace-path + memory-key isolation.

User docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban

---

## Windows-Specific Quirks

the operator agent runs natively on Windows (PowerShell, cmd, Windows Terminal, git-bash
mintty, VS Code integrated terminal). Most of it just works, but a handful
of differences between Win32 and POSIX have bitten us — document new ones
here as you hit them so the next person (or the next session) doesn't
rediscover them from scratch.

### Input / Keybindings

**Alt+Enter doesn't insert a newline.** Windows Terminal intercepts Alt+Enter
at the terminal layer to toggle fullscreen — the keystroke never reaches
prompt_toolkit. Use **Ctrl+Enter** instead. Windows Terminal delivers
Ctrl+Enter as LF (`c-j`), distinct from plain Enter (`c-m` / CR), and the
CLI binds `c-j` to newline insertion on `win32` only (see
`_bind_prompt_submit_keys` + the Windows-only `c-j` binding in `cli.py`).
Side effect: the raw Ctrl+J keystroke also inserts a newline on Windows —
unavoidable, because Windows Terminal collapses Ctrl+Enter and Ctrl+J to
the same keycode at the Win32 console API layer. No conflicting binding
existed for Ctrl+J on Windows, so this is a harmless side effect.

mintty / git-bash behaves the same (fullscreen on Alt+Enter) unless you
disable Alt+Fn shortcuts in Options → Keys. Easier to just use Ctrl+Enter.

**Diagnosing keybindings.** Run `python scripts/keystroke_diagnostic.py`
(repo root) to see exactly how prompt_toolkit identifies each keystroke
in the current terminal. Answers questions like "does Shift+Enter come
through as a distinct key?" (almost never — most terminals collapse it
to plain Enter) or "what byte sequence is my terminal sending for
Ctrl+Enter?" This is how the Ctrl+Enter = c-j fact was established.

### Config / Files

**HTTP 400 "No models provided" on first run.** `config.yaml` was saved
with a UTF-8 BOM (common when Windows apps write it). Re-save as UTF-8
without BOM. `hermes config edit` writes without BOM; manual edits in
Notepad are the usual culprit.

### `execute_code` / Sandbox

**WinError 10106** ("The requested service provider could not be loaded
or initialized") from the sandbox child process — it can't create an
`AF_INET` socket, so the loopback-TCP RPC fallback fails before
`connect()`. Root cause is usually **not** a broken Winsock LSP; it's
the operator agent's own env scrubber dropping `SYSTEMROOT` / `WINDIR` / `COMSPEC`
from the child env. Python's `socket` module needs `SYSTEMROOT` to locate
`mswsock.dll`. Fixed via the `_WINDOWS_ESSENTIAL_ENV_VARS` allowlist in
`tools/code_execution_tool.py`. If you still hit it, echo `os.environ`
inside an `execute_code` block to confirm `SYSTEMROOT` is set. Full
diagnostic recipe in `references/execute-code-sandbox-env-windows.md`.

### Testing / Contributing

**`scripts/run_tests.sh` doesn't work as-is on Windows** — it looks for
POSIX venv layouts (`.venv/bin/activate`). The the operator agent-installed venv at
`venv/Scripts/` has no pip or pytest either (stripped for install size).
Workaround: install `pytest + pytest-xdist + pyyaml` into a system Python
3.11 user site, then invoke pytest directly with `PYTHONPATH` set:

```bash
"/c/Program Files/Python311/python" -m pip install --user pytest pytest-xdist pyyaml
export PYTHONPATH="$(pwd)"
"/c/Program Files/Python311/python" -m pytest tests/foo/test_bar.py -v --tb=short -n 0
```

Use `-n 0`, not `-n 4` — `pyproject.toml`'s default `addopts` already
includes `-n`, and the wrapper's CI-parity guarantees don't apply off POSIX.

**POSIX-only tests need skip guards.** Common markers already in the codebase:
- Symlinks — elevated privileges on Windows
- `0o600` file modes — POSIX mode bits not enforced on NTFS by default
- `signal.SIGALRM` — Unix-only (see `tests/conftest.py::_enforce_test_timeout`)
- Winsock / Windows-specific regressions — `@pytest.mark.skipif(sys.platform != "win32", ...)`

Use the existing skip-pattern style (`sys.platform == "win32"` or
`sys.platform.startswith("win")`) to stay consistent with the rest of the
suite.

### Path / Filesystem

**Line endings.** Git may warn `LF will be replaced by CRLF the next time
Git touches it`. Cosmetic — the repo's `.gitattributes` normalizes. Don't
let editors auto-convert committed POSIX-newline files to CRLF.

**Forward slashes work almost everywhere.** `C:/Users/...` is accepted by
every the operator agent tool and most Windows APIs. Prefer forward slashes in code
and logs — avoids shell-escaping backslashes in bash.

---

### Troubleshooting

### Cron Job Delivery Channel Errors

**Symptom:** Errors containing `Unsupported channel: heartbeat` or `Channel is required (no configured channels detected)` in lastDiagnostics or delivery previews.

**Solution:** Ensure the job has a valid delivery channel configured. Use `hermes cron edit <job_id> --channel <channel-id>` or `--channel last` to route to the last active session. Verify channel exists in gateway platform configuration.
Example:
```bash
hermes cron edit <job_id> --channel last
```

### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify provider: `pip install faster-whisper` or set API key
3. In gateway: `/restart`. In CLI: exit and relaunch.

### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

### Model/provider issues
1. `hermes doctor` — check config and dependencies
2. `hermes auth` — re-authenticate OAuth providers (or `hermes auth add <provider>`)
3. Check `.env` has the right API key
4. **Copilot 403**: `gh auth token` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.
5. **Honcho local setup**: if `uv sync` fails on `lancedb` wheel selection on Intel macOS, keep going with the pgvector backend via `uv sync --no-install-package lancedb`, then run migrations and start API + deriver. See `references/honcho-local-self-hosting.md`.
6. **Provider/transport mismatch**: if a worker says `Missing API key for openai model config`, inspect the *resolved* model config, not just the env file. Make sure the transport, proxy `base_url`, and secret source line up. See `references/provider-mismatch-triage.md`.
7. **Honcho/OpenRouter memory path:** if memory embeddings or chat still fail after env edits, verify the OpenRouter base URL and per-feature API-key mapping, restart API + deriver, then run one embedding probe and one chat probe. See `references/honcho-openrouter-memory-dialectic.md`.

### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
- **Code changes:** Restart the CLI or gateway process

### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `/skill name` or `hermes -s name`

### Gateway issues
Check logs first:
```bash
grep -i "failed to send\|error" <agent-home>/logs/gateway.log | tail -20
```

Common gateway problems:
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`
- **Inbound messages silently ignored (Telegram/Discord/Slack/etc.)**: No user allowlist configured. Gateway denies all inbound messages by default. See `references/gateway-allowlist-config.md` for the fix — add `TELEGRAM_ALLOWED_USERS=your_id` to `<agent-home>/.env` and run `hermes gateway restart`.
+**Multiple gateway instances / port conflicts**: If you see errors about another gateway instance already running, list processes with `ps aux | grep -v grep | grep -E 'hermes.*gateway|gateway.*hermes'`, kill the conflicting PIDs (e.g., `kill -9 <PID>`), then run `hermes gateway stop` to ensure clean state, finally start with `hermes gateway run --replace`.
- **Telegram bot token already in use**: If you see errors like "Telegram bot token already in use (PID XXXXX)" in the gateway logs, it means the bot token is being used by another process. This often occurs when a previous the operator agent gateway didn't shut down cleanly. To fix:
  1. Check gateway logs for confirmation: `tail -n 20 <agent-home>/logs/gateway-stderr.log`
  2. Identify the conflicting process: `ps aux | grep -v grep | grep -E 'hermes.*gateway|gateway.*hermes|telegram'` 
  3. Stop the conflicting process: `kill -9 <PID>` (if it's a gateway process, use `hermes gateway stop` instead)
  4. Ensure clean gateway state: `hermes gateway stop`
  5. Verify state: `cat <agent-home>/gateway_state.json` (should show "gateway_state":"stopped")
  6. Start fresh: `hermes gateway run --replace`
 
 ### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
### Platform-specific issues
- **Telegram feels "stuck" or "not working"**: first distinguish *platform/session failure* from *conversation-state waiting* or *wrong topic/thread mapping*. See `references/telegram-stuck-triage.md` for the short triage sequence and wording rules.
- **Telegram delivery verification pitfall**: a `send_message(..., target="telegram")` success only proves the bot sent to the current home channel. If the user says they do not see the message, call `send_message(action="list")` and resend to the explicit DM/group target that matches the live account/thread before concluding routing is broken.
- **Telegram home channel/configuration issues**: If Telegram messages aren't arriving as expected, verify:
  1. Home channel is set correctly: `hermes config get TELEGRAM_HOME_CHANNEL` (should match your Telegram user/chat ID)
  2. Gateway allowlist includes your ID: Check `<agent-home>/.env` for `TELEGRAM_ALLOWED_USERS=<your_id>`
  3. Your Telegram ID can be found in gateway logs: look for `inbound message: platform=telegram user=YourName chat=<your_id>`
  4. After correcting config, restart gateway: `hermes gateway restart`
  See `references/gateway-allowlist-config.md` and `references/telegram-stuck-triage.md` for details.
- **Telegram startup docs should be label-clean**: when adding or editing runtime launch docs, use the engine/system name in document titles and labels, keep the agent name for runtime/controller docs, and include a short `START-HERE` page if there is a dedicated launch path. Verify the read order so the launch wrapper points to the canonical engine docs rather than a descriptive alias. See `references/runtime-launch-labels.md`.
- **Launch-path verification**: if a wrapper points to a checklist or launch doc, verify the file exists and the order is linear before calling the path complete. See `references/launch-path-verification.md`.
- **Windows-specific issues** (`Alt+Enter` newline, WinError 10106, UTF-8 BOM config, test suite, line endings): see the dedicated **Windows-Specific Quirks** section above.

## Where to Find Things

| Looking for... | Location |
|----------------|----------|
| Config options | `hermes config edit` or [Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) |
| Available tools | `hermes tools list` or [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) |
| Slash commands | `/help` in session or [Slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands) |
| Skills catalog | `hermes skills browse` or [Skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) |
| Provider setup | `hermes model` or [Providers guide](https://hermes-agent.nousresearch.com/docs/integrations/providers) |
| Platform setup | `hermes gateway setup` or [Messaging docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) |
| MCP servers | `hermes mcp list` or [MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) |
| Profiles | `hermes profile list` or [Profiles docs](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) |
| Cron jobs | `hermes cron list` or [Cron docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) |
| Memory | `hermes memory status` or [Memory docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) |
| Env variables | `hermes config env-path` or [Env vars reference](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) |
| CLI commands | `hermes --help` or [CLI reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) |
| Gateway logs | `<agent-home>/logs/gateway.log` |
| Session files | `hermes sessions browse` (reads state.db) |
| OpenClaw Fleet Analytics Sync Details (hermes-agent skill) | `references/fleet_analytics_sync_details.md` |
| OpenClaw Database Schema Reference | `references/sibling-agent-database-schema.md` |
| Baseline-First Gate and File Write Guidelines | `references/baseline-first-gate-and-file-writes.md` |
| **the specialist engine and Building Patterns** | `references/ds-engine-fleet-maintenance/naming-and-building-patterns.md` |
| Source code | `<agent-home>/hermes-agent/` |
| **the operator agent Agent Import Troubleshooting Guide** | `references/hermes-agent-import-troubleshooting.md` |

---

## Contributor Quick Reference

For occasional contributors and PR authors. Full developer docs: https://hermes-agent.nousresearch.com/docs/developer-guide/

### Project Layout

```
hermes-agent/
├── run_agent.py          # AIAgent — core conversation loop
├── model_tools.py        # Tool discovery and dispatch
├── toolsets.py           # Toolset definitions
├── cli.py                # Interactive CLI (HermesCLI)
├── hermes_state.py       # SQLite session store
├── agent/                # Prompt builder, context compression, memory, model routing, credential pooling, skill dispatch
├── hermes_cli/           # CLI subcommands, config, setup, commands
│   ├── commands.py       # Slash command registry (CommandDef)
│   ├── config.py         # DEFAULT_CONFIG, env var definitions
│   └── main.py           # CLI entry point and argparse
├── tools/                # One file per tool
│   └── registry.py       # Central tool registry
├── gateway/              # Messaging gateway
│   └── platforms/        # Platform adapters (telegram, discord, etc.)
├── cron/                 # Job scheduler
├── tests/                # ~3000 pytest tests
└── website/              # Docusaurus docs site
```

Config: `<agent-home>/config.yaml` (settings), `<agent-home>/.env` (API keys).

### Adding a Tool (3 files)

**1. Create `tools/your_tool.py`:**
```python
import json, os
from tools.registry import registry

def check_requirements() -> bool:
    return bool(os.getenv("EXAMPLE_API_KEY"))

def example_tool(param: str, task_id: str = None) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="example_tool",
    toolset="example",
    schema={"name": "example_tool", "description": "...", "parameters": {...}},
    handler=lambda args, **kw: example_tool(
        param=args.get("param", ""), task_id=kw.get("task_id")),
    check_fn=check_requirements,
    requires_env=["EXAMPLE_API_KEY"],
)
```

**2. Add to `toolsets.py`** → `_HERMES_CORE_TOOLS` list.

Auto-discovery: any `tools/*.py` file with a top-level `registry.register()` call is imported automatically — no manual list needed.

All handlers must return JSON strings. Use `get_hermes_home()` for paths, never hardcode `<agent-home>`.

### Adding a Slash Command

1. Add `CommandDef` to `COMMAND_REGISTRY` in `hermes_cli/commands.py`
2. Add handler in `cli.py` → `process_command()`
3. (Optional) Add gateway handler in `gateway/run.py`

All consumers (help text, autocomplete, Telegram menu, Slack mapping) derive from the central registry automatically.

### Agent Loop (High Level)

```
run_conversation():
  1. Build system prompt
  2. Loop while iterations < max:
     a. Call LLM (OpenAI-format messages + tool schemas)
     b. If tool_calls → dispatch each via handle_function_call() → append results → continue
     c. If text response → return
  3. Context compression triggers automatically near token limit
```

### Testing

```bash
python -m pytest tests/ -o 'addopts=' -q   # Full suite
python -m pytest tests/tools/ -q            # Specific area
```

- Tests auto-redirect `HERMES_HOME` to temp dirs — never touch real `<agent-home>/`
- Run full suite before pushing any change
- Use `-o 'addopts='` to clear any baked-in pytest flags

**Windows contributors:** `scripts/run_tests.sh` currently looks for POSIX venvs (`.venv/bin/activate` / `venv/bin/activate`) and will error out on Windows where the layout is `venv/Scripts/activate` + `python.exe`. The the operator agent-installed venv at `venv/Scripts/` also has no `pip` or `pytest` — it's stripped for end-user install size. Workaround: install pytest + pytest-xdist + pyyaml into a system Python 3.11 user site (`/c/Program Files/Python311/python -m pip install --user pytest pytest-xdist pyyaml`), then run tests directly:

```bash
export PYTHONPATH="$(pwd)"
"/c/Program Files/Python311/python" -m pytest tests/tools/test_foo.py -v --tb=short -n 0
```

Use `-n 0` (not `-n 4`) because `pyproject.toml`'s default `addopts` already includes `-n`, and the wrapper's CI-parity story doesn't apply off-POSIX.

**Cross-platform test guards:** tests that use POSIX-only syscalls need a skip marker. Common ones already in the codebase:
- Symlink creation → `@pytest.mark.skipif(sys.platform == "win32", reason="Symlinks require elevated privileges on Windows")` (see `tests/cron/test_cron_script.py`)
- POSIX file modes (0o600, etc.) → `@pytest.mark.skipif(sys.platform.startswith("win"), reason="POSIX mode bits not enforced on Windows")` (see `tests/hermes_cli/test_auth_toctou_file_modes.py`)
- `signal.SIGALRM` → Unix-only (see `tests/conftest.py::_enforce_test_timeout`)
- Live Winsock / Windows-specific regression tests → `@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific regression")`

**Monkeypatching `sys.platform` is not enough** when the code under test also calls `platform.system()` / `platform.release()` / `platform.mac_ver()`. Those functions re-read the real OS independently, so a test that sets `sys.platform = "linux"` on a Windows runner will still see `platform.system() == "Windows"` and route through the Windows branch. Patch all three together:

```python
monkeypatch.setattr(sys, "platform", "linux")
monkeypatch.setattr(platform, "system", lambda: "Linux")
monkeypatch.setattr(platform, "release", lambda: "6.8.0-generic")
```

See `tests/agent/test_prompt_builder.py::TestEnvironmentHints` for a worked example.

### Extending the system prompt's execution-environment block

Factual guidance about the host OS, user home, cwd, terminal backend, and shell (bash vs. PowerShell on Windows) is emitted from `agent/prompt_builder.py::build_environment_hints()`. This is also where the WSL hint and per-backend probe logic live. The convention:

- **Local terminal backend** → emit host info (OS, `$HOME`, cwd) + Windows-specific notes (hostname ≠ username, `terminal` uses bash not PowerShell).
- **Remote terminal backend** (anything in `_REMOTE_TERMINAL_BACKENDS`: `docker, singularity, modal, daytona, ssh, managed_modal`) → **suppress** host info entirely and describe only the backend. A live `uname`/`whoami`/`pwd` probe runs inside the backend via `tools.environments.get_environment(...).execute(...)`, cached per process in `_BACKEND_PROBE_CACHE`, with a static fallback if the probe times out.
- **Key fact for prompt authoring:** when `TERMINAL_ENV != "local"`, *every* file tool (`read_file`, `write_file`, `patch`, `search_files`) runs inside the backend container, not on the host. The system prompt must never describe the host in that case — the agent can't touch it.

Full design notes, the exact emitted strings, and testing pitfalls:
`references/prompt-builder-environment-hints.md`.

**Refactor-safety pattern (POSIX-equivalence guard):** when you extract inline logic into a helper that adds Windows/platform-specific behavior, keep a `_legacy_<name>` oracle function in the test file that's a verbatim copy of the old code, then parametrize-diff against it. Example: `tests/tools/test_code_execution_windows_env.py::TestPosixEquivalence`. This locks in the invariant that POSIX behavior is bit-for-bit identical and makes any future drift fail loudly with a clear diff.

### Commit Conventions

```
type: concise subject line

Optional body.
```

Types: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`

### Key Rules

- **Never break prompt caching** — don't change context, tools, or system prompt mid-conversation
- **Message role alternation** — never two assistant or two user messages in a row
- Use `get_hermes_home()` from `hermes_constants` for all paths (profile-safe)
- Config values go in `config.yaml`, secrets go in `.env`
- New tools need a `check_fn` so they only appear when requirements are met
