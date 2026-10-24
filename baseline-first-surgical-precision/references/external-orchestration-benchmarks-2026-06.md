# External Orchestration Benchmarks — 2026-06-08 (rev 4)

Condensed research from COO/V3 combined audit + horizon scans. Sources named; no claims fabricated. Rev 4 updates: Claude Code MCP hook hijack vulnerability (June 8 2026), LangGraph 1.2 DeltaChannel + production hardening, OpenAI AgentKit deprecation (June 3 2026).

## B1. Microsoft Conductor — Deterministic YAML Orchestration

**Source:** `github.com/microsoft/conductor` (MIT, v0.1.1), blog May 14 2026

Multi-agent workflows defined in YAML. Routing between agents is deterministic — Jinja2 templates handle conditions and branching. Orchestration layer consumes zero tokens because routing is fixed at definition time, not LLM-decided.

**Relevance to the operator agent/OpenClaw surgical edits:**
- the operator agent delegations currently use the LLM to decide routing. Conductor's pattern — pre-defined routing tables — would prevent routing failures in multi-part requests.
- **Adoption path:** Not a full migration. The pattern of task-type → agent → tool-set → constraints as a static routing table maps onto the missing "mode system" in the operator agent #29652.

## B2. Claude Code — Hooks Architecture (27 lifecycle events as of v2.1.141+)

**Sources:** `code.claude.com/docs/en/hooks`, `code.claude.com/docs/en/agent-sdk/hooks`, community guides (Morph, Blake Crosley, claudefa.st, thepromptshelf.dev, agentpatterns.ai, disler/claude-code-hooks-mastery)

**Major expansion May 2026.** Claude Code went from 12 lifecycle events to 27 distinct events. The full event surface now includes:

Session lifecycle: `SessionStart`, `Setup`, `SessionEnd`
Main loop: `UserPromptSubmit`, `UserPromptExpansion`
Tool execution: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`
Permission: `PermissionRequest`, `PermissionDenied`
Subagent/team: `SubagentStart`, `SubagentStop`, `TeammateIdle`
Task lifecycle: `TaskCreated`, `TaskCompleted`
System events: `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`
Compression: `PreCompact`, `PostCompact`
User interaction: `Notification`, `Elicitation`, `ElicitationResult`
Flow control: `Stop`, `StopFailure`

### PreCompact hooks (now with blocking support)
Fire before compressing context. **Can now block compaction entirely** by exiting with code 2 or returning `{"decision":"block"}`. Hooks can also: (a) customize summary strategy, (b) persist important context before condensation. Community pattern: hook pulls last 30 messages and re-injects them, making the summary richer.

**Maps to compression amnesia (FM-3):** The #1 failure mode in local surgical-edit sessions. Claude Code now has a structural solution. the operator agent has NO equivalent — no `pre_compact` or `post_compact` hook exists.

### PostCompact hooks (NEW)
Fire after context compression completes. Allows verification that critical state survived compaction. the operator agent has no equivalent.

### SubagentStart / SubagentStop hooks (NEW)
Track subagent lifecycle events. the operator agent has no equivalent hook. The local `workflow_enforcement` plugin cannot monitor subagent state transitions.

### Runtime environment hooks (NEW)
`ConfigChange`, `CwdChanged`, `FileChanged`, `InstructionsLoaded` — fire when the runtime environment changes. the operator agent has none of these. Could be used to detect when baseline artifacts are modified externally.

### PreToolUse hooks (unchanged)
Hooks that run before tool execution. Can block actions by exiting with code 2. Example: block `rm -rf` patterns.

**Correction (rev 2, unchanged):** the operator agent DOES have `pre_tool_call` plugin hooks that can block tool calls (return `{"action": "block", "message": "..."}`). The `workflow_enforcement` plugin uses this mechanism. The gap is that these hooks fire in the parent session but NOT in worker/subagent contexts (see B7).

### MCP Hook Hijack Vulnerability (June 8 2026)
**Source:** Mitiga security research, `cybersecuritynews.com/claude-code-mcp-traffic-hijack/`, `letsdatascience.com` writeup

Mitiga demonstrated that npm packages can register lifecycle hooks at install time that rewrite `~/.claude.json`, redirecting OAuth token refresh to an attacker-controlled proxy. The attack vector is hook auto-accept: if a user or agent has auto-accept enabled for hooks, a malicious package can inject a hook that persists across sessions.

**Relevance to the operator agent/OpenClaw surgical edits:** the operator agent's hook system has the same trust model: hooks registered during `on_session_start` or via npm/pip packages are trusted if auto-accept is enabled. The local config has `hooks_auto_accept: true`, which is the exact attack vector Mitiga demonstrated. While no the operator agent-specific exploit has been documented, the vulnerability validates a security concern about the current hook infrastructure.

**Remediation pattern (from Mitiga):** Remove untrusted hooks, clean config files, rotate credentials, disable auto-accept for production sessions.

### Known bug: Claude Code #24327
PreToolUse hook exit code 2 sometimes causes Claude to stop entirely instead of just blocking the individual tool call. User must manually type "continue." This is relevant because any the operator agent equivalent faces the same agent-loop design tension — blocking a tool should not kill the entire conversation loop.

## B3. Azure AI Agent Orchestration Patterns

**Source:** `learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns` (updated Feb 12 2026)

Five core patterns:
1. **Sequential** — agents in defined order, each receives previous output
2. **Concurrent** — parallel agents, results merged
3. **Group chat** — round-robin discussion
4. **Handoff** — one agent transfers control to another with explicit context
5. **Magentic-One** — orchestrator directs specialized workers

**Key takeaway for delegation:** The handoff pattern with explicit state transfer (not just prompt inheritance) prevents compression amnesia and artifact proliferation across delegation boundaries. A structured handoff payload should include: `{baseline_artifact, constraints, pending_edits, scope_boundary}`.

## B4. LangGraph — State Graph + Checkpointing

**Source:** `langchain-oss/langgraph` docs, v1.2.0 stable API (2026), eastondev.com guide, tech-insider.org tutorial

- **State schema with reducers:** Define what state flows between nodes and how concurrent updates merge.
- **Checkpointing after every node execution:** Auto-saves graph state, enables pause/resume.
- **Thread-scoped state:** Each workflow run gets a `thread_id` with its own state history.

**Relevance:** Artifact proliferation would be structurally prevented by a state schema tracking `{canonical_artifact_path, version}`. the operator agent's checkpoint system is file-snapshot-based, not state-schema-based. The `workflow_enforcement` plugin's `.session-state.json` is effectively a hand-built state schema but lives outside the operator agent's checkpoint system.

**v1.2.0 (2026):** API stabilized. PostgreSQL checkpointing backend for production. Amazon Bedrock AgentCore provides enterprise alternative with persistent memory, runtime isolation, and gateway patterns at cloud scale. Token cost reduction of ~40% vs naive multi-agent in production reports.

**DeltaChannel (beta):** Instead of writing full state snapshots on every node transition, DeltaChannel streams only the diff. Addresses checkpoint storage bloat (long agent sessions consuming gigabytes of checkpoint data). Relevant to the operator agent's `.session-state.json` and `workflow-enforcement-events.jsonl` which grow unbounded across sessions.

## B5. the operator agent Agent #29652 — Mode System Proposal

**Source:** `github.com/NousResearch/hermes-agent/issues/29652` (May 21 2026)

Most directly relevant to this skill's enforcement gap. Proposes a "Mode" system that simultaneously changes persona, restricts tools, and modifies behavioral guidance. Roadmap:
- **Short-term:** Mode dataclass — single highest-value architectural change
- **Medium-term:** PreToolUse-style hooks + skill guard functions
- **Long-term:** Subagent review gate + learning loop for self-improving constraints

**Status:** Still open. the operator agent v0.16.0 (2026-06-05, "Surface Release") shipped 874 commits and 399 issue closures but did NOT implement the mode system. Core agent infrastructure is unchanged.

## B6. OpenClaw Cron ACL/Quota Pattern

**Source:** `github.com/Ricky-Hao/sibling-agent-agent-cron`

Cron plugin includes ACL checks (non-admin agents operate only on their own jobs) and quota enforcement (per-agent limits, minimum intervals). Validation happens in code before LLM invocation, not after.

**Relevance:** Model for what the operator agent's enforcement layer should look like — code-level validation gates, not advisory context.

## B7. the operator agent Hook Infrastructure — Active Gaps (confirmed in v0.16.0)

v0.16.0 (2026-06-05) shipped without addressing any of these. The release focused on the desktop app and UI layer. The only relevant change: uncapped `max_spawn_depth` (floor 1, no ceiling), enabling deeper delegation trees but not fixing subagent enforcement propagation. Three issues constrain what enforcement plugins can do:

### #25204 — Shell hooks don't fire in workers
Filed May 13 2026. Shell hooks for `pre_tool_call` and `on_session_finalize` do not fire in worker/subagent contexts. Python plugin hooks work; shell hooks do not.

**Impact on enforcement:** `delegate_task` subagents run without enforcement unless the plugin is explicitly loaded in the child context. The `workflow_enforcement` plugin uses Python plugin hooks, so it is unaffected in the parent session, but delegated children inherit neither the plugin nor its state.

### #39939 — Hook payloads lack transcript access
Filed ~June 5 2026. `pre_tool_call` and `post_tool_call` hook payloads do not include conversation history or a reference to it.

**Impact:** Enforcement hooks cannot inspect what the model said it was about to do — they only see the tool name and args. This limits the ability to catch cases where the model's stated intent contradicts its tool call.

### #18988 — pre_tool_call cannot rewrite, only block
Filed May 2 2026. `pre_tool_call` can block a tool call (return `{"action": "block"}`) but cannot rewrite the args (e.g., redirect a write from a variant path to the canonical path). The model must re-attempt with corrected args.

**Impact:** When a variant-path write is blocked, the model must generate a new tool call with the correct path. This costs an extra turn and may not always succeed on the first retry.

## B8. Microsoft Agent Framework (MAF) v1.0 GA + BUILD 2026 (updated rev 3)

**Source:** `github.com/microsoft/agent-framework`, `devblogs.microsoft.com/agent-framework/`, BUILD 2026 announcements (June 3 2026)

MAF v1.0 declared production-ready April 2026. BUILD 2026 (June 3) expanded significantly:
- **Agent Harness** — standardized wrapper enforcing guardrails, logging, state management around any agent
- **Hosted Agents** — cloud-hosted agent runtime with built-in observability
- **CodeAct** — code-as-action execution pattern
- **Graph-based workflows** — sequential, concurrent, handoff, group collaboration. Includes **checkpointing**, streaming, human-in-the-loop, and **time-travel debugging**
- **Declarative agents/workflows in YAML** — define instructions, tools, memory config, orchestration topology in version-controlled YAML files
- **Same concepts and APIs** across .NET and Python

**Relevance:** The Harness + checkpointing + time-travel trio addresses all four local gaps: structured enforcement (harness), state preservation across compression (checkpointing), and debugging of state transitions (time-travel). The local system has none of these natively. The `workflow_enforcement` plugin's `.session-state.json` is a hand-built approximation of MAF's checkpointing.

## B9. OpenAI Agents SDK — Three-Layer Guardrails + Harness (updated rev 3)

**Source:** `openai.github.io/openai-agents-python/guardrails/`, `openai.github.io/openai-agents-js/guides/guardrails/`, awesomeagents.ai/news/openai-agents-sdk-sandboxing-guardrails/

April 2026 update expanded from two-layer to **three-layer guardrails** + harness:
- **Input guardrails:** Validate user input before the agent processes it
- **Output guardrails:** Validate agent output before it reaches the user
- **Tool-level guardrails (NEW April 2026):** Run on every custom function-tool invocation. Input guardrails before execution, output guardrails after execution. This is the exact structural primitive the `workflow_enforcement` plugin's `pre_tool_call` handler replicates, but as a first-class SDK feature.
- **Harness abstraction (NEW April 2026):** Wraps the model with the rest of the agent's components (guardrails, tools, memory) for long-horizon tasks. Architecturally similar to the local three-layer model (plugin/skill/config).
- Can invoke a lightweight model for pre-validation before invoking an expensive model (same pattern as the operator agent's `auxiliary.approval` model)

**Relevance:** OpenAI's three-layer guardrail (input/output/tool) + harness pattern is a direct external validation of the local three-layer enforcement model. The gap: the operator agent treats tool-level enforcement as a plugin add-on, not a first-class primitive. The local `pre_tool_call` can only block (not rewrite args per #18988), which is a subset of what OpenAI's tool guardrails support.

### OpenAI AgentKit / Agent Builder Deprecation (June 3, 2026)
**Source:** `openai.com/index/introducing-agentkit/` (updated June 3), `codex.danielvaughan.com` deprecation roundup

On June 3, 2026, OpenAI announced the deprecation of three platform services:
- **Agent Builder** (visual agent canvas)
- **Evals** (evaluation dashboard)
- **Prompts API** (`v1/prompts`)

All three scheduled for shutdown on November 30, 2026. Evals enters read-only mode October 31.

**Migration path:** OpenAI recommends the Agents SDK for code-based workflows, and Workspace Agents in ChatGPT for natural-language workflows.

**Relevance to the operator agent/OpenClaw surgical edits:** The low-code visual builder approach lost. Code-first SDK with structural guardrails (the Agents SDK pattern) is the winning direction. This reinforces the local system's plugin + skill approach (code-first, composable, version-controllable) as architecturally aligned with the market direction. No action needed for local rails beyond noting the validation.

---

## Practical Takeaways for Surgical Edit Discipline

1. **Compression settings matter.** `target_ratio ≥ 0.35`, `protect_last_n ≥ 35` dramatically reduce artifact identity loss in long sessions.
2. **Pre-flight gates are advisory until the operator agent ships #29652.** v0.16.0 did not ship it. Mitigate by re-verifying baseline on disk after any compaction.
3. **One canonical path per deliverable** is the single most effective anti-proliferation rule. Enforce in memory and skills; track upstream for infrastructure support.
4. **Structured handoff payloads** for delegations should include artifact path, constraints, and scope boundary — not just inherited prompts.
5. **Deterministic routing** (Conductor pattern) is the long-term fix for multi-part request ordering failures. Short-term: mandatory decompose-before-execute step in skills.
6. **Plugin hooks do not propagate to subagents** (#25204, confirmed still open in v0.16.0). Delegate with explicit context or accept enforcement gap in children. Uncapped `max_spawn_depth` in v0.16.0 makes deeper trees possible but amplifies this gap.
7. **pre_tool_call cannot rewrite args** (#18988, still open). Blocking costs an extra turn. Design enforcement to give clear redirect messages so the model corrects on retry.
8. **No pre_compact hook exists** — the single biggest gap for compression amnesia. Claude Code now has both PreCompact (with blocking) and PostCompact hooks. The gap is widening. Mitigate with generous compression settings and post-compaction baseline re-verification.
9. **Tool-level guardrails are now a first-class SDK primitive** in OpenAI Agents SDK (April 2026). the operator agent's `pre_tool_call` plugin mechanism is a subset of this capability. Watch for the operator agent #18988 (rewrite action) to close part of this gap.

*Compiled from COSMOS COO combined audit (2026-06-06) and HYDRA horizon scan crons (2026-06-06, 2026-06-07). Rev 3 updates: Claude Code hooks 12→27 with PreCompact blocking, the operator agent v0.16.0 Surface Release (no hook fixes), OpenAI tool-level guardrails + harness, MAF v1.0 GA + BUILD 2026, LangGraph v1.2.0.*
