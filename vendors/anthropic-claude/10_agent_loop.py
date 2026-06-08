"""Claude Agent SDK — agent loop pattern.

Reference excerpts from the claude-agent-sdk-python repo. The Python
SDK exposes a `query()` async generator that yields messages as the
agent runs. The actual loop is delegated to the Claude Code binary
under the hood, with the SDK providing typed message types and hook
dispatch.

Source: github.com/anthropics/claude-agent-sdk-python
"""
from __future__ import annotations

import asyncio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    HookMatcher,
    AgentDefinition,
    SystemMessage,
    AssistantMessage,
    ResultMessage,
)


# --- Pattern 1: Basic agent loop ---------------------------------------------
# The query() function is an async generator. Each yielded message represents
# a step in the agent's execution. The loop is managed by the SDK; the
# developer consumes messages.

async def basic_agent():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        # message is one of: SystemMessage, AssistantMessage,
        # ToolResultMessage, ResultMessage, UserMessage
        if isinstance(message, SystemMessage) and message.subtype == "init":
            print(f"Session: {message.data['session_id']}")
        if isinstance(message, ResultMessage):
            print(f"Final: {message.result}")


# --- Pattern 2: Hook-driven safety -----------------------------------------
# Hooks fire at well-defined lifecycle points. Returning a deny decision
# halts the tool call without raising an exception.

async def log_file_change(input_data, tool_use_id, context):
    """PostToolUse hook for audit logging."""
    file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
    with open("./audit.log", "a") as f:
        f.write(f"modified {file_path} (tool_use_id={tool_use_id})\n")
    return {}


async def gate_destructive_writes(input_data, tool_use_id, context):
    """PreToolUse hook that requires explicit approval for writes outside /workspace."""
    tool_name = input_data.get("tool_name")
    file_path = input_data.get("tool_input", {}).get("file_path", "")
    if tool_name in ("Edit", "Write") and not file_path.startswith("/workspace/"):
        # Returning a "deny" decision halts the tool call. The agent will
        # see a denied tool result and can replan or ask the user.
        return {
            "decision": "deny",
            "reason": f"Write outside /workspace blocked: {file_path}",
        }
    return {}


async def safety_gated_agent():
    async for message in query(
        prompt="Refactor utils.py to improve readability",
        options=ClaudeAgentOptions(
            permission_mode="default",  # prompts on risky actions
            allowed_tools=["Read", "Edit", "Write", "Bash"],
            hooks={
                "PreToolUse":  [HookMatcher(matcher="Edit|Write", hooks=[gate_destructive_writes])],
                "PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[log_file_change])],
            },
        ),
    ):
        if isinstance(message, ResultMessage):
            print(message.result)


# --- Pattern 3: Plan mode (dry-run) ----------------------------------------
# permission_mode="plan" produces the execution plan without running tools.
# Useful for high-risk evaluation: the agent shows what it WOULD do.

async def dry_run_agent():
    async for message in query(
        prompt="Update all subscriptions in the database to tier=premium",
        options=ClaudeAgentOptions(
            permission_mode="plan",   # dry-run: shows plan, no execution
            allowed_tools=["Read", "Bash"],
        ),
    ):
        # In plan mode, Claude produces a plan message rather than executing
        if isinstance(message, AssistantMessage):
            print(message.content)


# --- Pattern 4: Subagent delegation ----------------------------------------

async def code_review_with_subagent():
    async for message in query(
        prompt="Use the code-reviewer agent to review this codebase",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Agent"],   # Agent tool enables subagent invocation
            agents={
                "code-reviewer": AgentDefinition(
                    description="Expert code reviewer for quality and security reviews.",
                    prompt="Analyze code quality and suggest improvements. Flag security issues.",
                    tools=["Read", "Glob", "Grep"],
                )
            },
        ),
    ):
        # Messages from inside the subagent's context have parent_tool_use_id
        # linking back to the parent invocation
        if isinstance(message, AssistantMessage) and message.parent_tool_use_id:
            print(f"[subagent reply] {message.content}")
        elif isinstance(message, ResultMessage):
            print(f"[main result] {message.result}")


# --- Pattern 5: Session resume / fork --------------------------------------

async def resume_pattern():
    from claude_agent_sdk import fork_session

    # First query — capture session ID
    session_id = None
    async for message in query(
        prompt="Read the authentication module and summarize",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"]),
    ):
        if isinstance(message, SystemMessage) and message.subtype == "init":
            session_id = message.data["session_id"]

    # Resume — Claude remembers context from prior query
    async for message in query(
        prompt="Now find all places that call it",  # 'it' = auth module
        options=ClaudeAgentOptions(resume=session_id),
    ):
        if isinstance(message, ResultMessage):
            print(message.result)

    # Fork — branch the session to explore an alternative
    new_session_id = fork_session(session_id)


# --- What's enforced by the SDK vs developer responsibility ----------------
#
# ENFORCED (shipped):
#   - Strict JSON Schema on tool arguments via strict tool use.
#   - Lifecycle hooks (PreToolUse / PostToolUse / Stop / SessionStart /
#     SessionEnd / UserPromptSubmit) with deny / modify / prompt decisions.
#   - Permission modes (default / acceptEdits / bypassPermissions / plan).
#   - Tool allowlist / denylist.
#   - Session persistence with fork / resume / tag.
#   - Automatic context compaction for long runs.
#   - Built-in observability (each step yields a typed message).
#
# NOT ENFORCED (developer's responsibility):
#   - Per-tool destructiveness classification (use hook matchers).
#   - Bounded retry counter on tool errors.
#   - Foreign-key / business-rule validation in tool bodies.
#   - Contradiction detection across turns.
#   - Per-run cost cap (use max_tokens + org-level dashboard cap).
"""
