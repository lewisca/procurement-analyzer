"""Lumen Agents — reference implementation of a destructive tool.

This is the actual production handler for `issue_refund`. We share it
with buyers under NDA so they can audit validation, idempotency,
approval gating, and trace emission against our claims.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Literal

from lumen.runtime import (
    ToolContext,
    ToolError,
    ApprovalRequired,
    schema_validator,
    record_trace_event,
    write_audit_log,
)
from lumen.persistence import idempotency_store, refunds_repo, orders_repo


REASON_CODES = Literal[
    "duplicate_charge",
    "item_not_received",
    "defective_item",
    "wrong_item_shipped",
    "customer_request",
    "fraud_chargeback",
    "other",
]


@dataclass
class IssueRefundInput:
    order_id: str
    amount_cents: int
    reason_code: REASON_CODES
    idempotency_key: str


# ---------- Validation: typed schema + business rules + FK existence ----------

INPUT_SCHEMA = {
    "type": "object",
    "required": ["order_id", "amount_cents", "reason_code", "idempotency_key"],
    "properties": {
        "order_id": {"type": "string", "pattern": r"^ORD-[0-9]{5,10}$"},
        "amount_cents": {"type": "integer", "minimum": 0, "maximum": 100_000_000},
        "reason_code": {"type": "string", "enum": list(REASON_CODES.__args__)},
        "idempotency_key": {"type": "string", "pattern": r"^[a-f0-9-]{36}$"},
    },
    "additionalProperties": False,
}


def _validate(raw: dict) -> IssueRefundInput:
    # 1. JSON Schema 2020-12 validation — runs BEFORE any side effect.
    schema_validator.validate(raw, INPUT_SCHEMA)
    parsed = IssueRefundInput(**raw)

    # 2. Foreign-key existence check — catches hallucinated order IDs
    #    (FM-TC-002 in the failure-mode doc).
    if not orders_repo.exists(parsed.order_id):
        raise ToolError(
            code="order_not_found",
            human_msg=f"order_id {parsed.order_id} does not exist",
            agent_msg="The order_id you provided does not exist in the CRM. Verify the ID from the original ticket and retry.",
        )

    # 3. Business-rule validator — amount cannot exceed order total.
    order = orders_repo.get(parsed.order_id)
    if parsed.amount_cents > order.amount_cents:
        raise ToolError(
            code="refund_exceeds_order",
            human_msg=f"refund amount {parsed.amount_cents} exceeds order total {order.amount_cents}",
            agent_msg="The refund amount exceeds the order total. Either reduce the refund or escalate.",
        )

    # 4. Idempotency key format already validated by schema; uniqueness
    #    handled by the idempotency_store below.
    return parsed


# ---------- Approval gate ------------------------------------------------------

AUTO_APPROVE_THRESHOLD_CENTS = 10_000


def _needs_human_approval(ctx: ToolContext, parsed: IssueRefundInput) -> bool:
    customer = ctx.state.get_required("customer")
    # Mirrors `tool_schema.json#issue_refund.approval_gate.auto_approve_if`.
    return not (parsed.amount_cents <= AUTO_APPROVE_THRESHOLD_CENTS
                and customer.risk_score < 0.3)


# ---------- Handler ------------------------------------------------------------

def issue_refund(ctx: ToolContext, raw_input: dict, *, mode: Literal["dry_run", "live"] = "live") -> dict:
    """Issue a refund. The agent calls this; the runtime invokes the handler.

    Contract:
      - All validation happens before any side effect.
      - In dry_run mode no external call is made; the response shows
        what would have happened.
      - Live execution is dedup'd by idempotency_key for 24h.
      - Every outcome (success, validation error, approval required) is
        recorded to the per-run trace AND the immutable audit log.
    """
    parsed = _validate(raw_input)

    # Approval gate. We surface this as a separate ApprovalRequired
    # exception so the orchestrator can pause the run, record a trace
    # event, and wait for a typed approval token.
    if _needs_human_approval(ctx, parsed) and not ctx.approval_token_present():
        record_trace_event(ctx, "approval_requested", parsed.__dict__)
        raise ApprovalRequired(
            tool="issue_refund",
            reason="amount_or_risk_above_auto_approve",
            payload=parsed.__dict__,
        )

    if mode == "dry_run":
        record_trace_event(ctx, "tool.dry_run", {"tool": "issue_refund", "input": parsed.__dict__})
        return {
            "would_execute": True,
            "would_amount_cents": parsed.amount_cents,
            "approval_required": _needs_human_approval(ctx, parsed),
        }

    # Idempotency check — ensures retries within 24h do not double-refund.
    if existing := idempotency_store.lookup(parsed.idempotency_key):
        record_trace_event(ctx, "tool.idempotency_replay", existing)
        return existing

    # Side effect: actually issue the refund.
    refund_id = f"RFND-{ctx.year_now()}-{uuid.uuid4().hex[:6].upper()}"
    refund = refunds_repo.create(
        refund_id=refund_id,
        order_id=parsed.order_id,
        amount_cents=parsed.amount_cents,
        reason_code=parsed.reason_code,
        idempotency_key=parsed.idempotency_key,
        approver_id=ctx.approval_token().approver_id,
        agent_trace_id=ctx.trace_id,
    )
    idempotency_store.put(parsed.idempotency_key, {"refund_id": refund_id, "status": "settled"})

    record_trace_event(ctx, "tool.execute", {"tool": "issue_refund", "refund_id": refund_id})
    write_audit_log(
        ctx,
        action="tool.execute",
        resource="issue_refund",
        outcome="settled",
        approver_id=ctx.approval_token().approver_id,
    )

    return {"refund_id": refund_id, "status": "settled", "settled_at": refund.settled_at.isoformat()}
