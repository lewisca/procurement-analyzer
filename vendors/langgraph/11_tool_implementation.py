"""LangGraph — canonical tool definition example.

This shows how tools are typically defined for a LangGraph agent.
Tools come from LangChain (`langchain_core.tools`); LangGraph just
calls them via `ToolNode`. The pattern below is what users adopt; it
is not framework-enforced.

This is illustrative of the LangGraph + LangChain tool-definition
convention, not extracted from a specific repo file.
"""
from __future__ import annotations

from typing import Annotated
from pydantic import BaseModel, Field, field_validator
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode


# --- Pattern 1: @tool decorator with Pydantic args_schema --------------------
# This is the recommended pattern. The decorator infers the args schema from
# the function signature + Pydantic type hints. Validation happens via
# Pydantic when the tool is invoked.


class IssueRefundInput(BaseModel):
    """Arguments for the refund tool. Pydantic validates these before
    the tool function body executes."""
    order_id: str = Field(..., pattern=r"^ORD-[0-9]{5,10}$")
    amount_cents: int = Field(..., ge=0, le=100_000_000)
    reason_code: str = Field(..., description="One of: duplicate_charge, item_not_received, defective_item, customer_request, other")

    @field_validator("reason_code")
    @classmethod
    def _validate_reason(cls, v: str) -> str:
        allowed = {"duplicate_charge", "item_not_received", "defective_item", "customer_request", "other"}
        if v not in allowed:
            raise ValueError(f"reason_code must be one of {allowed}")
        return v


@tool("issue_refund", args_schema=IssueRefundInput)
def issue_refund(order_id: str, amount_cents: int, reason_code: str) -> dict:
    """Issue a refund against an order.

    Notes for the buyer / integrator:
      - LangGraph + LangChain do NOT add framework-level checks for:
          * Foreign-key existence (does ORD-12345 actually exist?)
          * Business rules (refund <= order total?)
          * Idempotency (was this same refund already issued?)
          * Approval / destructiveness gating
      - The integrator must add those checks inside the function body
        (as below) OR wire interrupt_before=['tools'] for human approval.
    """
    # ---- Application-layer validation (NOT framework-provided) ----
    order = orders_repo.get(order_id)
    if order is None:
        return {"error": "order_not_found", "order_id": order_id}
    if amount_cents > order.amount_cents:
        return {
            "error": "refund_exceeds_order",
            "max_allowed_cents": order.amount_cents,
            "requested_cents": amount_cents,
        }

    # ---- Idempotency (NOT framework-provided; must be DIY) ----
    # In LangGraph, the recommended pattern is a stable tool_call_id from
    # the LLM combined with a buyer-managed dedup store. The framework
    # does not handle this.

    # ---- Side effect ----
    refund_id = refunds_repo.create(
        order_id=order_id,
        amount_cents=amount_cents,
        reason_code=reason_code,
    )
    return {"refund_id": refund_id, "status": "settled"}


# --- Pattern 2: Register tools with ToolNode --------------------------------

tool_node = ToolNode([issue_refund, get_order, search_kb])


# --- Pattern 3: Human-in-the-loop approval gate for destructive tools ------
# LangGraph's mechanism for "don't call this tool without approval" is
# interrupt_before=['tools'] at compile time:

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import InMemorySaver

workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

graph = workflow.compile(
    checkpointer=InMemorySaver(),
    interrupt_before=["tools"],   # <-- pauses BEFORE tool execution
)

# Usage:
# 1. Invoke; graph runs to the tools node and stops.
# 2. graph.get_state(config) returns the planned tool calls.
# 3. Human reviews. To approve: graph.invoke(None, config).
# 4. To modify: graph.update_state(config, {...}) then graph.invoke(None, config).
# 5. To deny: simply do not resume.


# --- What this pattern does NOT enforce -------------------------------------
#
# The above is the BEST PATTERN in LangGraph. It still does NOT enforce:
#
#   - Per-tool destructiveness classification (interrupt_before is binary —
#     either ALL tools get reviewed, or none do).
#   - A pre-execution validation layer separate from the function body.
#     If you forget to add the checks in the function body, nothing else
#     catches it.
#   - Tool-call audit logging beyond the standard streaming trace.
#   - Cost / token caps per tool call.
#
# Integrators building on LangGraph generally implement these in a
# middleware-style wrapper around their tools or as a custom node placed
# between `agent` and `tools`.
