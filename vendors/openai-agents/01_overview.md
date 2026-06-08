# OpenAI Agents — Product Overview

_OpenAI's agent platform is a stack, not a single product. This
overview covers the layers a procurement buyer is evaluating when
they consider "building on OpenAI for agents."_

_Sources: openai.github.io/openai-agents-python (Agents SDK docs);
developers.openai.com/api/docs/guides/agents; Responses API docs;
openai.com/security-and-privacy/; trust.openai.com (gated)._

## The stack

| Layer | What it is | Open / Closed |
|-------|-----------|---------------|
| **Models** | GPT-5.5, GPT-5.4, GPT-5, GPT-4o, o-series reasoning models, gpt-realtime-2 (voice) | Closed; accessed via API |
| **Responses API** | Unified agentic primitive; replaces split Chat Completions / Assistants APIs. Built-in tools, state persistence, conversation threading. | Closed API; client SDKs open |
| **Built-in tools** | web_search, file_search, computer_use, code_interpreter, MCP servers, function calling | Tools run in OpenAI-managed sandboxes |
| **Agents SDK** | Python/TypeScript SDK on top of Responses. Adds run loop, guardrails, handoffs, tracing, sessions. | **Open source** (MIT, github.com/openai/openai-agents-python) |
| **Enterprise wrapper** | ChatGPT Enterprise, ChatGPT Business, ChatGPT Edu — managed deployments with SSO, DPA, admin controls | Closed |

OpenAI's positioning: bring your own application code (via the Agents
SDK), use OpenAI's models and tools as the substrate, optionally
deploy through ChatGPT Enterprise for managed governance.

## Core abstractions (Agents SDK)

From the official docs:

> The SDK operates on three primary primitives: **Agents** (LLMs with
> instructions and tools), **Handoffs** (agents delegating to other
> agents), and **Guardrails** (validation of inputs/outputs).
> Additional infrastructure includes tracing for visualization and
> sessions for persistent memory.

Hello-world from the docs:

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

## What the platform does

- **Function calling** with strict JSON-Schema validation (the model
  cannot emit a schema-non-conforming tool call when `strict: true`).
- **Built-in tools** — web search, file search, computer use, code
  interpreter — all sandboxed in OpenAI infrastructure.
- **Parallel tool calls** by default; `parallel_tool_calls: false`
  to force single-tool turns.
- **Tool choice control** via `auto`, `required`, `{"type":
  "function", "name": "X"}`, or `allowed_tools`.
- **Handoffs** — first-class delegation between agents.
- **Guardrails** — input and output validators running in parallel
  with the agent, with explicit `tripwire_triggered` halting.
- **Tracing** — built-in span-based traces, viewable in the OpenAI
  dashboard or exported.
- **Sessions** — cross-turn persistent memory (Responses API state).
- **Sandbox agents** — agents that run in isolated workspaces.
- **MCP server integration** with optional `require_approval` for
  human-in-the-loop.

## What it does not do (explicit positioning)

- The Agents SDK does not lock you to OpenAI models — it works with
  any compatible model (Anthropic Claude, open-weights, etc.) but
  uses the Responses API by default for OpenAI.
- It does not include a hosted product runtime. You run the SDK in
  your own environment, against OpenAI's API. (ChatGPT Enterprise is
  a separate offering.)
- It does not impose policy / brand restrictions — those are the
  developer's responsibility via guardrails and instructions.

## Customer and maturity signals

OpenAI is the largest commercial LLM provider by API volume. ChatGPT
has 100M+ weekly active users; ChatGPT Enterprise serves Fortune 500
deployments at scale.

The Agents SDK is **the production-ready upgrade of OpenAI's earlier
Swarm experiment.** From the docs:

> "The OpenAI Agents SDK enables you to build agentic AI apps in a
> lightweight, easy-to-use package with very few abstractions. It's
> a production-ready upgrade of our previous experimentation for
> agents, Swarm."

## Model policy

OpenAI ships a new flagship model approximately quarterly. Recent
generations: GPT-4 (2023) → GPT-4o (2024) → GPT-5 (Aug 2025) → GPT-5.4
/ GPT-5.5 (2026). Customers can pin to specific snapshots (e.g.
`gpt-5-2025-08-13`) for stability or use the rolling alias
(`gpt-5.5`) for the latest.

Reasoning models (o-series) are positioned separately for tasks that
benefit from extended deliberation.
