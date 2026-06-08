# LangGraph — Product Overview

_Sourced from the LangGraph GitHub README and docs.langchain.com._

## What it is

LangGraph is "a low-level orchestration framework and runtime for
building, managing, and deploying long-running, stateful agents." It
is positioned as **infrastructure**, not a complete agent product —
it provides the runtime substrate (state, persistence, observability)
on which agent behaviors are built.

The framework is open source (MIT-licensed) and Python-first, with a
JavaScript/TypeScript port. Inspiration is drawn from Pregel and
Apache Beam (for the runtime), and from NetworkX (for the public
graph-construction interface).

## What it does

- **Durable execution.** Agents persist through failures and resume
  from where they left off.
- **Human-in-the-loop oversight.** Inspect and modify agent state at
  any point during execution.
- **Memory.** Both short-term working memory (per-thread) and
  long-term cross-thread memory (via Stores).
- **Streaming and observability.** Per-step state snapshots, token
  streaming, debug traces.
- **Production deployment.** Used in production at companies cited
  by LangChain including "Klarna, Replit, Elastic, and more."

## What it does not do (explicitly out of scope)

The README explicitly distinguishes LangGraph from higher-level agent
products: "if you're looking to quickly build agents, check Deep Agents,
described as 'a higher-level package built on LangGraph for agents that
can plan, use subagents, and leverage file systems for complex tasks.'"

LangGraph does not:

- Pick the model for you. You bring your own LLM (OpenAI, Anthropic,
  Gemini, etc.); LangGraph orchestrates calls.
- Prescribe tool implementations. Tools are user-defined.
- Provide a UI. LangSmith (paid) supplies the observability UI.

## Core abstractions

LangGraph models agents as a **StateGraph** — a directed graph where:

- **State** is a shared TypedDict (or Pydantic model) representing the
  current snapshot of an agent run.
- **Nodes** are Python functions that take the current state and
  return a state update.
- **Edges** define routing between nodes; conditional edges let the
  agent decide its own next step based on state.
- **Cycles** are first-class — the agent loop is literally a cycle in
  the graph.

A minimal hello-world from the official docs:

```python
from langgraph.graph import StateGraph, MessagesState, START, END

def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}

graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()

graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
```

## Agent loop model

Pre-built agents (the `create_react_agent` factory in the prebuilt
package) implement a standard ReAct-style loop with two nodes:

1. **agent node** — calls the LLM with the current message history.
2. **tools node** — executes any tool calls the LLM emitted.

A `should_continue` function inspects the latest message; if the LLM
emitted tool calls, route to `tools`; otherwise terminate. This is the
literal control flow from
`libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py`.

## Customers and maturity

Per the README: "trusted by companies shaping the future of agents –
including Klarna, Replit, Elastic, and more." Case studies are
collected at langchain.com/built-with-langgraph.

LangGraph itself is OSS. The paid surface — observability, evaluation,
and managed deployment — is **LangSmith Platform** (see pricing doc).
LangSmith has been **SOC 2 Type II compliant since July 2024**, plus
GDPR and HIPAA.

## Model policy

LangGraph does not lock in a model. The agent factory accepts any
chat model that implements LangChain's `BaseChatModel` interface
(OpenAI, Anthropic, Google, open-weight models via LiteLLM, etc.).
The `create_react_agent` signature supports both **static** models
(one model per agent) and **dynamic** models (a callable that selects
a model at runtime based on state).
