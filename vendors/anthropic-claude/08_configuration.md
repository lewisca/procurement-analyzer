# Anthropic Claude Agent SDK — Configuration Reference

_Sourced from code.claude.com/docs/en/agent-sdk and the
claude-agent-sdk-python repo._

## ClaudeAgentOptions — the primary configuration object

```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher, AgentDefinition

options = ClaudeAgentOptions(
    # ---- Tool registry ----
    allowed_tools=["Read", "Glob", "Grep"],     # whitelist
    disallowed_tools=["Bash"],                   # explicit deny
    mcp_servers={
        "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
    },

    # ---- Permission control ----
    permission_mode="default",   # default | acceptEdits | bypassPermissions | plan

    # ---- Lifecycle hooks ----
    hooks={
        "PreToolUse":  [HookMatcher(matcher="Edit|Write", hooks=[validate_path])],
        "PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[log_change])],
        "Stop":        [HookMatcher(hooks=[audit_final_state])],
        "SessionStart": [...],
        "SessionEnd":   [...],
        "UserPromptSubmit": [HookMatcher(hooks=[scan_for_injection])],
    },

    # ---- Subagents ----
    agents={
        "code-reviewer": AgentDefinition(
            description="Expert code reviewer.",
            prompt="Analyze code quality and suggest improvements.",
            tools=["Read", "Glob", "Grep"],
        )
    },

    # ---- Session ----
    resume=prior_session_id,   # resume a session

    # ---- Plugins / settings ----
    plugins=[my_plugin],
    setting_sources=["~/.claude", ".claude"],  # restrict where settings load from
)
```

## Permission modes (key differentiator)

| Mode | Behavior |
|------|----------|
| `default` | Prompts user (or hook) for approval on risky tool use |
| `acceptEdits` | Auto-approves file edits — useful for trusted CI |
| `bypassPermissions` | No prompts — only for fully trusted automation |
| `plan` | Shows what the agent would do without executing — equivalent to dry-run mode in other SDKs |

The `plan` mode is **Anthropic's documented dry-run capability** —
the agent produces a plan with predicted tool calls but does not
execute them. This is materially stronger than OpenAI's `tool_choice`
controls because it generates the full execution plan, not just a
restriction.

## Hook lifecycle events

Hooks are the central safety / observability primitive in the
Anthropic Agent SDK. From the docs:

| Event | When it fires | Common uses |
|-------|---------------|-------------|
| `PreToolUse` | Before tool execution | Validate args, deny dangerous calls, request approval |
| `PostToolUse` | After tool execution | Audit logs, output validation, transform results |
| `Stop` | When agent stops | Final-state audit |
| `SessionStart` | New session begins | Initialize state, log identity |
| `SessionEnd` | Session terminates | Cleanup, audit |
| `UserPromptSubmit` | Before user prompt is added to context | Prompt-injection scanning, intent classification |

Hooks return a dict that can:
- **Allow** the tool call to proceed unchanged
- **Modify** the tool args before execution
- **Deny** the tool call (returning a deny decision)
- **Request user approval** (the SDK surfaces to the caller)

## Subagent configuration

```python
agents={
    "code-reviewer": AgentDefinition(
        description="Expert code reviewer.",
        prompt="Analyze code quality and suggest improvements.",
        tools=["Read", "Glob", "Grep"],
    ),
    "test-runner": AgentDefinition(
        description="Run tests and report results.",
        prompt="Execute test suite and summarize failures.",
        tools=["Bash"],
    ),
}
```

Subagents are invoked via the `Agent` tool. Messages from inside a
subagent's context include `parent_tool_use_id` linking back to the
parent invocation — making subagent traces auditable.

## Filesystem-based configuration

The SDK loads configuration from filesystem locations (similar to
how editors load .editorconfig):

| Location | What's loaded |
|----------|---------------|
| `.claude/skills/*/SKILL.md` | Skills (specialized capabilities) |
| `.claude/commands/*.md` | Legacy custom commands |
| `CLAUDE.md` or `.claude/CLAUDE.md` | Project context and instructions (Memory) |
| `~/.claude/` | User-level defaults |

Per-project `.claude/` directories enable team-shared agent
configurations checked into source control.

## Session management

```python
# Resume
async for message in query(prompt="...", options=ClaudeAgentOptions(resume=session_id)):
    ...

# Fork — branch a session to explore an alternative
from claude_agent_sdk import fork_session
new_session_id = fork_session(parent_session_id)

# Tag, rename, delete sessions
```

Sessions are stored as JSONL on the developer's filesystem (or
Anthropic's event log under Managed Agents).

## What is NOT in the SDK configuration

- **Per-run cost cap** — no dollar-cap primitive; use max_tokens +
  org-level cap
- **Per-tool destructiveness metadata** — not a first-class field
  (developer encodes via hook matchers)
- **Semantic loop detection** — step counting only
- **Bounded retry on tool errors** — developer's responsibility
- **Contradiction detection** — developer's responsibility

## Configuration vs Managed Agents

For the **Managed Agents** product (REST API where Anthropic runs the
sandbox), configuration is similar but state is Anthropic-hosted
rather than filesystem-local. Common transition path: prototype on
Agent SDK, promote to Managed Agents for production.

## Procurement-relevant takeaways

- The hook framework is **more fine-grained** than competitive
  vendors' guardrail systems. Procurement can ask: "show us your
  hook coverage matrix — what fires before/after each tool category?"
- `permission_mode="plan"` is a real dry-run capability — useful for
  high-risk pilot evaluation.
- Subagents with `parent_tool_use_id` linking enable traceable
  delegation.
- Sessions on the developer's filesystem mean the buyer can audit
  every interaction without depending on Anthropic to retain logs.
