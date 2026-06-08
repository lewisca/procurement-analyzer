"""Claude Agent SDK — tool definition and hook patterns.

Reference patterns for defining tools and safety hooks in the
claude-agent-sdk-python package. Tools are defined as Python functions
that conform to the MCP tool protocol (Anthropic uses MCP as the
canonical tool definition format under the hood).

Source: github.com/anthropics/claude-agent-sdk-python and the docs
at code.claude.com/docs/en/agent-sdk.
"""
from __future__ import annotations

from typing import Literal
from dataclasses import dataclass

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    HookMatcher,
    SystemMessage,
    ResultMessage,
)
from mcp.types import ToolAnnotations


# --- Pattern 1: User-defined tool via MCP protocol --------------------------
# Anthropic tools follow the MCP spec. The input_schema is a JSON Schema;
# under strict mode (default in Agent SDK), Claude's decoding is constrained
# to schema-conforming JSON.

ISSUE_REFUND_TOOL = {
    "name": "issue_refund",
    "description": "Issue a refund against an order. Use only when policy permits.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {"type": "string", "pattern": "^ORD-[0-9]{5,10}$"},
            "amount_cents": {"type": "integer", "minimum": 0, "maximum": 100_000_000},
            "reason_code": {
                "type": "string",
                "enum": ["duplicate_charge", "item_not_received", "defective_item", "customer_request", "other"],
            },
            "idempotency_key": {"type": "string", "pattern": "^[a-f0-9-]{36}$"},
        },
        "required": ["order_id", "amount_cents", "reason_code", "idempotency_key"],
    },
    "strict": True,
}


def issue_refund_impl(order_id: str, amount_cents: int, reason_code: str, idempotency_key: str) -> dict:
    """Application-layer implementation.

    Note: the SDK + strict mode enforce schema validity. Application-layer
    checks (foreign keys, business rules, idempotency) are the developer's
    responsibility.
    """
    order = orders_repo.get(order_id)
    if order is None:
        return {"error": "order_not_found", "order_id": order_id}
    if amount_cents > order.amount_cents:
        return {"error": "refund_exceeds_order", "max_allowed_cents": order.amount_cents}

    if existing := idempotency_store.lookup(idempotency_key):
        return existing

    refund_id = refunds_repo.create(
        order_id=order_id, amount_cents=amount_cents, reason_code=reason_code,
    )
    idempotency_store.put(idempotency_key, {"refund_id": refund_id, "status": "settled"})
    return {"refund_id": refund_id, "status": "settled"}


# --- Pattern 2: Hook-based destructive-action gating ------------------------
# Anthropic's distinguishing safety primitive. PreToolUse hooks can deny,
# modify, or surface to the user — finer-grained than guardrails-in-parallel.

async def require_approval_for_large_refunds(input_data, tool_use_id, context):
    """PreToolUse hook: any refund > $200 requires human approval."""
    if input_data.get("tool_name") != "issue_refund":
        return {}

    amount = input_data.get("tool_input", {}).get("amount_cents", 0)
    if amount <= 20_000:
        return {}  # auto-approve small refunds

    # Approval needed. Return a "prompt user" decision and the SDK will
    # surface to the caller / AskUserQuestion mechanism.
    return {
        "decision": "prompt_user",
        "prompt": f"Refund of ${amount/100:.2f} requires approval. Approve?",
        "options": ["approve", "deny", "escalate to supervisor"],
    }


# --- Pattern 3: PreToolUse hook for prompt-injection scanning --------------

async def scan_prompt_injection(input_data, tool_use_id, context):
    """UserPromptSubmit hook: block obvious injection attempts."""
    prompt = input_data.get("prompt", "")
    if detect_injection_signal(prompt):
        return {
            "decision": "deny",
            "reason": "Potential prompt injection detected",
        }
    return {}


# --- Pattern 4: Audit-log hook ---------------------------------------------

async def audit_refund_tool_call(input_data, tool_use_id, context):
    """PostToolUse hook: log every refund tool call to an audit file."""
    if input_data.get("tool_name") != "issue_refund":
        return {}

    with open("/var/log/refund_audit.jsonl", "a") as f:
        f.write(json.dumps({
            "ts": datetime.utcnow().isoformat(),
            "tool_use_id": tool_use_id,
            "args": input_data.get("tool_input"),
            "result": input_data.get("tool_result"),
        }) + "\n")
    return {}


# --- Pattern 5: Wiring it all together -------------------------------------

options = ClaudeAgentOptions(
    permission_mode="default",   # prompts for risky actions per SDK defaults
    allowed_tools=["Read", "Glob", "Grep", "issue_refund", "lookup_order", "escalate_to_human"],
    hooks={
        "UserPromptSubmit": [
            HookMatcher(hooks=[scan_prompt_injection]),
        ],
        "PreToolUse": [
            HookMatcher(matcher="issue_refund", hooks=[require_approval_for_large_refunds]),
        ],
        "PostToolUse": [
            HookMatcher(matcher="issue_refund", hooks=[audit_refund_tool_call]),
        ],
    },
)


# --- What this enforces vs leaves to developer ----------------------------
#
# ENFORCED by SDK + strict tool use:
#   - JSON Schema validity on tool arguments (decode-time, structural).
#   - Pre/post hook lifecycle.
#   - Permission-mode gating.
#   - Tool allowlist.
#
# DEVELOPER responsibility (typical pattern shown above):
#   - Foreign-key / business-rule validation INSIDE the tool implementation.
#   - Idempotency dedup INSIDE the tool implementation.
#   - Destructive-action approval gating via PreToolUse hooks.
#   - Audit logging via PostToolUse hooks.
#   - Prompt-injection scanning via UserPromptSubmit hooks.
#
# DIFFERENCE vs OpenAI Agents SDK:
#   - OpenAI: InputGuardrail / OutputGuardrail with `tripwire_triggered: bool`,
#     runs in PARALLEL with the agent and halts on tripwire.
#   - Anthropic: Pre/PostToolUse hooks with `decision`-style returns (allow,
#     deny, modify, prompt_user), run AT specific lifecycle points.
#   - Anthropic's hooks are more granular (matched per tool name / regex).
#   - OpenAI's guardrails are more parallel-safe by design.
#   - For tool-call risk: Anthropic's PreToolUse provides finer per-tool control.
#   - For input safety: similar coverage; OpenAI's parallel input guardrails
#     are faster (don't wait for the agent), Anthropic's UserPromptSubmit
#     runs before the model sees the input.
"""
