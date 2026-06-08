"""OpenAI Agents SDK — tool and guardrail implementation examples.

Reference patterns for defining tools and guardrails in the openai-agents
SDK. The @function_tool decorator (from src/agents/tool.py) infers a JSON
Schema from Python type hints and applies strict mode by default for
OpenAI models via the Responses API.

The InputGuardrail / OutputGuardrail patterns shown match the verbatim
class signatures in src/agents/guardrail.py.
"""
from __future__ import annotations

from typing import Literal
from dataclasses import dataclass

from agents import (
    Agent,
    Runner,
    function_tool,
    input_guardrail,
    output_guardrail,
    GuardrailFunctionOutput,
    RunContextWrapper,
)


# --- Pattern 1: A function tool with strict schema ---------------------------
# The @function_tool decorator generates a JSON Schema from the type hints.
# Under strict mode (default for Responses API), the model is constrained at
# decode time to emit only schema-valid arguments — schema violations are
# structurally impossible.

REASON_CODES = Literal[
    "duplicate_charge",
    "item_not_received",
    "defective_item",
    "customer_request",
    "other",
]


@function_tool
def issue_refund(
    order_id: str,
    amount_cents: int,
    reason_code: REASON_CODES,
    idempotency_key: str,
) -> dict:
    """Issue a refund against an order.

    Args:
        order_id: The order ID, format ORD-XXXXXX.
        amount_cents: Refund amount in cents. Must not exceed the order total.
        reason_code: One of the allowed reasons.
        idempotency_key: UUID v4 to dedupe retries within 24 hours.
    """
    # Application-layer validation — NOT framework-provided.
    # Strict mode catches schema errors; foreign keys and business rules
    # must be checked here.
    order = orders_repo.get(order_id)
    if order is None:
        return {"error": "order_not_found", "order_id": order_id}
    if amount_cents > order.amount_cents:
        return {
            "error": "refund_exceeds_order",
            "max_allowed_cents": order.amount_cents,
        }

    # Idempotency — also developer-implemented.
    if existing := idempotency_store.lookup(idempotency_key):
        return existing

    refund_id = refunds_repo.create(
        order_id=order_id,
        amount_cents=amount_cents,
        reason_code=reason_code,
        idempotency_key=idempotency_key,
    )
    idempotency_store.put(idempotency_key, {"refund_id": refund_id, "status": "settled"})
    return {"refund_id": refund_id, "status": "settled"}


# --- Pattern 2: Input guardrail with tripwire ------------------------------
# Input guardrails run IN PARALLEL with the agent's first model call.
# A tripwire_triggered=True result halts the run before any tool executes.


@input_guardrail
async def block_off_topic_input(
    ctx: RunContextWrapper,
    agent: Agent,
    user_input: str,
) -> GuardrailFunctionOutput:
    """Halt if the input is off-topic for this support agent."""
    is_off_topic = classify_off_topic(user_input)
    return GuardrailFunctionOutput(
        tripwire_triggered=is_off_topic,
        output_info={"reason": "input outside support scope"} if is_off_topic else None,
    )


# --- Pattern 3: Output guardrail enforcing destructive-action approval -----
# Output guardrails inspect the model's planned final output (or planned
# tool call) AFTER the model has generated it but BEFORE it's emitted.
# Tripwire halts and returns the partial RunResult to the caller for human
# review.


@output_guardrail
async def require_human_approval_for_large_refunds(
    ctx: RunContextWrapper,
    agent: Agent,
    output,
) -> GuardrailFunctionOutput:
    """Trip if the agent is about to issue a refund > $200 without approval."""
    planned_refund_cents = extract_planned_refund_amount(output)
    needs_approval = (
        planned_refund_cents is not None
        and planned_refund_cents > 20_000
        and not ctx.context.human_approval_token
    )
    return GuardrailFunctionOutput(
        tripwire_triggered=needs_approval,
        output_info={
            "reason": "refund > $200 requires human approval",
            "planned_amount_cents": planned_refund_cents,
        } if needs_approval else None,
    )


# --- Pattern 4: Wiring it all together -------------------------------------

@dataclass
class SupportContext:
    customer_id: str
    human_approval_token: str | None = None


support_agent = Agent[SupportContext](
    name="support_agent",
    instructions=(
        "You are a customer support agent. Use tools to look up orders and "
        "issue refunds only when policy permits."
    ),
    model="gpt-5.5",
    tools=[issue_refund, lookup_order, lookup_customer],
    input_guardrails=[block_off_topic_input],
    output_guardrails=[require_human_approval_for_large_refunds],
)


# Running the agent
result = Runner.run_sync(
    starting_agent=support_agent,
    input="My order ORD-77129834 never arrived; I'd like a refund.",
    context=SupportContext(customer_id="CUST-447712"),
    max_turns=10,
)

# If a guardrail tripwire fired, result.interruptions contains the planned
# action. The caller can present it to a human for approval, then resume.


# --- What this pattern enforces vs. what it doesn't ------------------------
#
# ENFORCED (by the SDK / Responses API):
#   - Strict JSON Schema on tool arguments (decode-time, structural).
#   - max_turns runtime cap.
#   - Tripwire-halting guardrails with parallel execution.
#   - Built-in tracing spans for every step.
#
# NOT ENFORCED (developer must implement):
#   - Foreign-key / business-rule validation in tool bodies.
#   - Idempotency dedup.
#   - Per-tool destructiveness metadata (no first-class field).
#   - Semantic loop detection.
#   - Bounded retry on tool errors.
#   - Cost cap per run (set via dashboard org-level budget).
#
# This is the SAME pattern as LangGraph's: framework provides hooks,
# developer wires policy. The differences from LangGraph:
#
#   1. Strict JSON Schema is decode-time structural, not post-hoc Pydantic.
#   2. Guardrails are a first-class SDK primitive with explicit tripwires.
#   3. Tracing is built in, not bolt-on.
#   4. max_turns has a graceful-handler escape, not just an exception.
