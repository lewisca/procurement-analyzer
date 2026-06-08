# OpenAI Agents — Configuration Reference

_Sourced from the Agents SDK docs (openai.github.io/openai-agents-python),
Responses API reference, and the openai-agents-python repo source._

## Per-run config

Passed to `Runner.run()` / `Runner.run_sync()` / `Runner.run_streamed()`:

```python
from agents import Agent, Runner, RunConfig

result = Runner.run_sync(
    starting_agent=agent,
    input="...",
    max_turns=10,                    # default; hard runtime cap
    context=my_context,              # passed to tools / guardrails
    session=my_session,              # cross-turn persistent memory
    run_config=RunConfig(
        model_settings=...,          # temperature, max_tokens, etc.
        input_guardrails=[...],      # parallel input validators
        output_guardrails=[...],     # parallel output validators
        handoffs=[...],
        tracing_disabled=False,      # default: tracing enabled
        trace_metadata={...},        # custom span tags
    ),
    error_handlers=[...],            # intercept MaxTurnsExceeded, etc.
)
```

### `max_turns`

- **Default:** 10 (from `DEFAULT_MAX_TURNS` in run.py).
- **Enforcement:** Runtime, in the agent runner loop. Increments
  `current_turn` after each model call; raises `MaxTurnsExceeded`
  when `current_turn > max_turns`.
- **Graceful handling:** `error_handlers` can intercept the exception
  and synthesize a final output, so a max-turns hit doesn't crash
  the application.

### Per-request limits (Responses API level)

- `max_output_tokens` — caps output tokens per LLM call.
- `parallel_tool_calls: false` — restricts to single tool per turn.
- `tool_choice` — restricts tool selection (`auto`, `required`,
  specific function, or `allowed_tools` subset).

## Agent definition

```python
from agents import Agent, function_tool, InputGuardrail, OutputGuardrail

@function_tool
def get_order(order_id: str) -> dict:
    """Look up an order by ID."""
    ...

agent = Agent(
    name="support_agent",
    instructions="You are a customer support agent...",
    model="gpt-5.5",
    tools=[get_order, ...],
    input_guardrails=[my_input_guardrail],
    output_guardrails=[my_output_guardrail],
    handoffs=[other_agent],
)
```

Note that **guardrails are first-class** in the agent definition —
not bolted on at runtime. The same agent always has the same
guardrails, which is good for auditability.

## Session / memory configuration

```python
from agents import Agent, Session

session = Session(persist=True)
# Cross-turn memory survives between Runner.run() calls
# using the same session
```

Under the hood, Sessions can use the Responses API's server-side
state (via `previous_response_id`) or local message-array passing.

## Tool configuration

Tool decorators infer the JSON Schema from function signatures and
type hints:

```python
@function_tool
def issue_refund(
    order_id: str,
    amount_cents: int,
    reason_code: str,
    idempotency_key: str,
) -> dict:
    """Issue a refund. Use only when policy permits."""
    ...
```

The SDK auto-generates a strict JSON Schema; the model is constrained
at decode time to produce only schema-valid arguments.

## Guardrail configuration

```python
from agents import input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def pii_filter(ctx, agent, user_input):
    has_pii = detect_pii(user_input)
    return GuardrailFunctionOutput(
        tripwire_triggered=has_pii,
        output_info={"reason": "PII detected"} if has_pii else None,
    )

agent = Agent(
    name="...",
    input_guardrails=[pii_filter],
    ...
)
```

When `tripwire_triggered=True`, the SDK halts the run and the caller
receives the partial result for human review.

## Tracing configuration

Tracing is **on by default.** Every agent run produces a hierarchical
span tree visible in the OpenAI dashboard:

- Per-LLM-call spans (timing, tokens, model)
- Per-tool-call spans (input, output, errors)
- Per-guardrail spans (tripwire status, elapsed time)
- Per-handoff spans

Custom exporters can route traces to external systems (Datadog,
Honeycomb, etc.) via the SDK's `set_tracing_export_api_key()` and
`add_trace_processor()` hooks.

## What is NOT in the SDK configuration

- **Per-tool destructiveness classification** — not a first-class
  field. Developers encode it in guardrails or tool naming
  conventions.
- **Cost cap per execution** — must be enforced via
  `max_output_tokens` per call + `max_turns` per run; there's no
  single dollar cap at the runtime layer.
- **Loop detection (semantic)** — only step-counter (max_turns).
- **Bounded retry** on tool errors — developer's responsibility.

## Org-level / dashboard configuration

In the OpenAI dashboard (platform.openai.com):

- **Monthly spend cap** (org-wide hard stop).
- **Project budgets** (segment by use case).
- **Rate limits** (per model, per tier).
- **API key scoping** (per project, per role).
- **Audit logs** (compliance API for Enterprise).
- **SSO / SCIM** (Enterprise).

## Procurement-relevant takeaways

OpenAI's Agents SDK gives the developer **explicit configuration
control** at every layer — turn budget, token cap, tool restrictions,
guardrails, tracing. The default is sensible (max_turns=10, tracing
on).

The buyer's main task is to *use* the controls — set the dashboard
spend cap, configure appropriate guardrails per agent, pin model
snapshots if stability is required. These are not defaults; they're
developer responsibilities.
