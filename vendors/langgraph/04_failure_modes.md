# LangGraph — Known Failure Modes

_LangGraph is an open-source orchestration framework, not a managed
vendor product. There is no formal failure-mode catalog with observed
production rates. This file documents the failure modes the framework
itself acknowledges in its documentation and source code, plus the
mitigations it ships with._

## 1. Runaway / non-terminating loop

**The framework's primary guard against runaway loops is a
`recursion_limit` on the compiled graph.** From the LangGraph source
(`chat_agent_executor.py`), the prebuilt `create_react_agent` factory
includes a `_are_more_steps_needed(state, response)` check that
inspects `remaining_steps` in state. When the budget is low, the agent
emits a sentinel message — `"Sorry, need more steps to process this
request."` — and terminates rather than continuing to loop.

- **Detection mechanism.** Hard step counter on the compiled graph.
- **Default ceiling.** The default `recursion_limit` is 25 (per the
  LangGraph reference docs).
- **Configurability.** Set via the runtime config, e.g.
  `graph.invoke(input, {"recursion_limit": 50})`.
- **What happens at the limit.** A `GraphRecursionError` is raised, OR
  for the prebuilt agent, a sentinel message is emitted.

**Gaps relative to a mature failure-mode story.**

- No semantic loop detection (e.g. same tool called repeatedly with
  same args, or repeated reasoning content). The framework relies on
  the step counter alone.
- No first-class "circuit breaker" on tool errors — repeated tool
  failures count against the step budget but are not detected as a
  loop signal.

## 2. Tool-call failure

When a tool function raises, the `ToolNode` catches the exception and
returns it to the LLM as a `ToolMessage` containing the error text.
The LLM then decides whether to retry, try a different tool, or give
up.

- **Detection mechanism.** Standard Python exception in the tool
  function body.
- **Mitigation.** The LLM sees the error in the next step and can
  replan. Whether this works depends entirely on the model's
  capability — the framework does not impose a bounded-retry policy.
- **Gaps.** No built-in retry count; no escalation path; no
  distinction between transient errors (worth retrying) and permanent
  errors (don't retry).

## 3. Hallucinated tool name or parameters

If the LLM emits a tool call for a tool that doesn't exist, or with
parameters that fail Pydantic validation:

- **Tool name miss.** `ToolNode` returns an error message naming the
  unknown tool; the LLM gets another turn.
- **Param schema miss.** Pydantic raises a `ValidationError` from the
  `@tool`-decorated function; the error is returned as a `ToolMessage`.
- **Gaps.** **Validation happens INSIDE the tool call, not before
  it.** There is no pre-execution gate that intercepts the tool call,
  validates parameters, and rejects without invoking the function.
  For destructive tools, users must add validation as the first
  statement of the function body or use approval gates.

## 4. State contradiction / hallucinated facts

**Not addressed by the framework.** LangGraph manages state via the
StateGraph abstraction (TypedDict / Pydantic), and provides reducers
that combine updates from nodes. The framework does not:

- Detect contradictions between facts established in different steps.
- Require source-step citations on facts added to state.
- Provide a hallucination-detection layer.

Users who need these guarantees must implement them as additional
nodes or post-model hooks. This is a known gap relative to enterprise
agentic platforms.

## 5. State / checkpoint corruption

LangGraph's checkpointers (InMemorySaver, SqliteSaver, PostgresSaver,
CosmosDBSaver) persist state at each step.

- **Recovery.** If a graph crashes mid-run, the most recent checkpoint
  survives and `graph.invoke(None, config)` resumes from there. This
  is the framework's primary failure-recovery mechanism.
- **Durability modes.** Three options trading off performance and
  consistency:
  - `"exit"` — persists only on completion / error (lowest durability)
  - `"async"` — persists asynchronously during next step (balanced)
  - `"sync"` — synchronous persist before next step (highest)
- **Encryption.** Optional via `EncryptedSerializer` (AES, requires
  the `LANGGRAPH_AES_KEY` env var). Off by default.

## 6. Destructive tool executed without human review

The framework provides `interrupt_before=['tools']` to pause before
tool execution; a human can then review and resume or modify. **This
is opt-in** — the default agent does not gate destructive actions.

- **Mitigation.** Users wire `interrupt_before` or
  `interrupt_after` on the appropriate node(s) and integrate with their
  own approval UI.
- **Gaps.** No tool-level destructiveness classification in the
  framework. The user is responsible for marking which tools require
  human approval, and the framework provides no metadata field for
  this.

## 7. Adversarial input / prompt injection

**Not addressed by the framework directly.** Prompt injection
mitigations are the responsibility of the model provider and the
application author. LangGraph provides no:

- Adversarial test suite
- Prompt-injection detector
- Input sanitization layer

There are community-shared examples but no shipped defenses.

## Summary

LangGraph is **strong on recovery** (checkpointing, replay, durability
modes) and **weak on prevention** (no built-in loop detector beyond
step counting, no contradiction detection, no pre-execution tool
validation gate, no adversarial testing). Procurement buyers
evaluating a LangGraph-based product should ask the **integrator**
how they have layered these defenses on top of the framework, since
LangGraph itself does not provide them.
