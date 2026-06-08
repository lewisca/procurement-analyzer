# Anthropic Claude — Agent SDK and Platform Overview

_Sourced from code.claude.com/docs/en/agent-sdk/overview,
platform.claude.com/docs/en/agents-and-tools/tool-use/overview,
claude.com/blog/building-agents-with-the-claude-agent-sdk, and
github.com/anthropics/claude-agent-sdk-python._

## What it is

Anthropic's agent platform is a stack similar in shape to OpenAI's
but with a distinctly different design philosophy. Components:

| Layer | What it is | Open / Closed |
|-------|-----------|---------------|
| **Models** | Claude Opus 4.8, Opus 4.7, Sonnet 4.6, Haiku 4.5, and earlier | Closed; accessed via API |
| **Messages API** | Standard chat completion with tool use | Closed API; SDKs open |
| **Tool use** | Client tools (run in your app) + server tools (run on Anthropic's infra: web_search, code_execution, web_fetch, tool_search) | Closed |
| **Agent SDK** | Python + TypeScript libraries that give you "the same tools, agent loop, and context management that power Claude Code" | **Open source (MIT)** at github.com/anthropics/claude-agent-sdk-{python,typescript} |
| **Managed Agents** | Hosted REST API where Anthropic runs the agent + sandbox; you send events | Closed |
| **Claude Code** | The CLI / IDE coding agent (which the Agent SDK is the library version of) | Closed binary; SDK exposes the same engine |

This is **a different shape than OpenAI**. OpenAI's Agents SDK is a
thin wrapper around the Responses API; Anthropic's Agent SDK is the
library form of a production agent (Claude Code) that's been running
real workloads for months. The agent loop, tool registry, and context
management are battle-tested at scale.

## Core design philosophy

From Anthropic's engineering blog (claude.com/blog/building-agents-with-the-claude-agent-sdk):

> "Give Claude a computer." — Claude needs the same tools that
> programmers use every day, including file access, execution
> capabilities, and iterative debugging.

The agent loop follows: **gather context → take action → verify
work → repeat.**

Notable design choices:

- **Agentic search over RAG.** Rather than loading retrieved chunks
  into context, Claude uses `grep` / `tail` / file reads to find
  what it needs. Slower but more transparent.
- **Code as a tool of choice.** "Code is precise, composable, and
  infinitely reusable" — Claude is encouraged to write code as a
  primary action mechanism.
- **Self-verification.** Anthropic recommends building rules-based,
  visual, or LLM-as-judge feedback into every agent — agents that
  check their own output "are fundamentally more reliable."

## Core abstractions (Agent SDK)

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)
```

| Primitive | What it does |
|-----------|--------------|
| `query()` | Run an agent with a prompt and yield messages |
| `ClaudeAgentOptions` | Configure the run (tools, permissions, hooks, etc.) |
| `allowed_tools` | Whitelist of tools the agent can use |
| `disallowed_tools` | Explicit deny list |
| `permission_mode` | `default`, `acceptEdits`, `bypassPermissions`, `plan` — controls when the SDK asks for user approval |
| `hooks` | Lifecycle callbacks: PreToolUse, PostToolUse, Stop, SessionStart, SessionEnd, UserPromptSubmit |
| `agents` | Subagent definitions for delegation |
| `mcp_servers` | MCP server connections |
| `resume` | Resume a prior session by ID |

## Built-in tools (shipped with the SDK)

| Tool | What it does |
|------|--------------|
| Read | Read any file in working directory |
| Write | Create new files |
| Edit | Make precise edits to existing files |
| Bash | Run terminal commands, scripts, git |
| Monitor | Watch a background script and react to each output line |
| Glob | Find files by pattern (`**/*.ts`) |
| Grep | Search file contents with regex |
| WebSearch | Search web for current information |
| WebFetch | Fetch and parse web page content |
| **AskUserQuestion** | First-class clarifying-question tool with multiple-choice options |

The **AskUserQuestion tool is unusual** — it's a built-in mechanism
for the agent to pause and ask the user a structured question, with
multiple-choice options. Most agent SDKs don't formalize this as a
tool; Anthropic treats it as a first-class capability.

## Distinguishing differentiators

- **Hooks** — lifecycle callbacks (PreToolUse, PostToolUse, Stop,
  SessionStart, etc.) let developers validate, log, block, or
  transform agent behavior at specific points. This is a finer-grained
  control surface than OpenAI's guardrails or Sierra's validator
  agents.
- **Permission modes** as a first-class concept — `default` prompts
  for risky tool use; `acceptEdits` auto-approves file edits;
  `bypassPermissions` runs unsupervised; `plan` shows what it would
  do without executing.
- **Sessions with fork/resume** — sessions are persistable JSONL on
  the developer's filesystem, with first-class fork and resume.
- **Subagents** — formal delegation with `parent_tool_use_id` linking
  in traces.
- **Compaction** — automatic context summarization as limits approach
  for long-running agents.

## What it does not do

- Anthropic Agent SDK does not include a hosted runtime — you run it
  in your own process. For that, Anthropic offers the separate
  **Managed Agents** product (REST API with Anthropic-managed
  sandboxes).
- The SDK is opinionated toward developer agents (Claude Code is the
  reference application). Customer-facing agents are doable but the
  SDK's defaults assume a single developer user rather than thousands
  of customer turns.

## Customer and maturity signals

Anthropic is the second-largest commercial LLM provider by API volume.
Claude Code itself has hundreds of thousands of developer users; the
Agent SDK gives those developers the same library Claude Code runs on.

Claude is offered via direct API and via three third-party clouds:
**Amazon Bedrock, Google Vertex AI, Microsoft Azure AI Foundry, and
Claude Platform on AWS.** Multi-cloud distribution gives buyers more
sourcing options than OpenAI's primarily-Azure path.

Subscription plans: as of June 15, 2026, Agent SDK and `claude -p`
usage on subscription plans draws from a new monthly Agent SDK credit
separate from interactive usage limits.

## Model policy

Models are versioned with explicit deprecation paths. As of mid-2026:

| Model | Status |
|-------|--------|
| Claude Opus 4.8 | Latest flagship |
| Claude Opus 4.7 / 4.6 / 4.5 / 4.1 | Available; varied release dates |
| Claude Opus 4 | Deprecated |
| Claude Sonnet 4.6 / 4.5 | Available |
| Claude Sonnet 4 | Deprecated |
| Claude Haiku 4.5 | Available |
| Claude Haiku 3.5 | Retired except on Bedrock and Vertex AI |

Customers can pin to specific versions or use rolling aliases.
Deprecation announcements come with a public schedule.
