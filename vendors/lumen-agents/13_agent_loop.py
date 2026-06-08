"""Lumen Agents — orchestrator / agent-loop pseudocode (simplified).

The real implementation has more telemetry, retry windows, and tenant
isolation. This is the buyer-NDA reference that shows the planner /
validator / executor / checkpoint / loop-detector wiring matches what
the security and failure-mode docs claim.
"""
from __future__ import annotations

from lumen.runtime import (
    LLM,
    BudgetMeter,
    LoopDetector,
    StateStore,
    Checkpointer,
    ConsistencyChecker,
    PlanValidator,
    ToolDispatcher,
    Trace,
    ApprovalRequired,
    ToolError,
)


def run(ticket, tenant_config) -> Trace:
    trace = Trace.open(tenant_id=tenant_config.tenant_id, ticket=ticket)
    state = StateStore.new(trace_id=trace.id)
    budget = BudgetMeter.from_config(tenant_config.budgets)
    loop = LoopDetector(signals=("repeated_tool_call", "embedding_similarity", "state_hash_unchanged"))
    consistency = ConsistencyChecker.from_use_case(tenant_config.use_case)
    checkpointer = Checkpointer(state_store=state)

    state.add_fact("ticket.id", ticket.id, source_step=1)
    state.add_fact("ticket.customer_email", ticket.customer_email, source_step=1)

    plan = LLM.plan(ticket=ticket, allowlist=tenant_config.tool_allowlist, state=state.snapshot())
    PlanValidator.validate(plan, tenant_config)  # raises on disallowed tools, missing approval gates
    trace.record_plan(plan)

    step_num = 2  # step 1 was the plan
    while not plan.is_complete() and step_num <= budget.step_limit:
        budget.assert_within_limits()  # raises BudgetExceeded → graceful escalate

        next_action = plan.next_action(state.snapshot())
        if next_action.type == "tool_call":
            try:
                # Validation runs INSIDE the tool dispatcher, before any side effect.
                # See tool_implementation.py for the contract.
                result = ToolDispatcher.invoke(
                    tool=next_action.tool,
                    params=next_action.params,
                    mode="dry_run" if next_action.is_destructive_and_unapproved() else "live",
                    trace_ctx=trace.step_ctx(step_num),
                )
            except ApprovalRequired as ar:
                trace.record_approval_request(step_num, ar)
                decision = await_human_approval(ar, timeout_s=tenant_config.approvals.approval_timeout_seconds)
                if decision.denied:
                    return escalate(trace, reason="destructive_action_blocked", notes=decision.notes)
                # Re-attempt live with approval token.
                result = ToolDispatcher.invoke(
                    tool=next_action.tool,
                    params=next_action.params,
                    mode="live",
                    approval_token=decision.token,
                    trace_ctx=trace.step_ctx(step_num),
                )
            except ToolError as te:
                # Bounded retries (max 3 per step), then circuit-break.
                if plan.retry_count(step_num) < 3:
                    plan.note_error(step_num, te)
                    continue
                return escalate(trace, reason="agent_low_confidence", notes=str(te))

            state.absorb(result, source_step=step_num)
        elif next_action.type == "reasoning":
            LLM.reason(state=state.snapshot(), goal=plan.goal, trace=trace.step_ctx(step_num))

        # Per-step coherence + loop checks. Failures here trigger replan or escalate.
        if violation := consistency.check(state):
            trace.record_consistency_flag(violation)
            if not consistency.resolvable(violation, tenant_config):
                return escalate(trace, reason="contradiction_detected", notes=violation.summary)

        if loop.signal_fires(state, plan, step_num):
            trace.record_loop_signal(loop.last_signal)
            return escalate(trace, reason="loop_detected", notes=loop.last_signal.description)

        checkpointer.checkpoint(step_num)
        step_num += 1

    if step_num > budget.step_limit:
        return escalate(trace, reason="budget_exceeded", notes=f"step_limit={budget.step_limit} hit")

    trace.close(outcome="completed")
    return trace


def escalate(trace: Trace, *, reason: str, notes: str) -> Trace:
    """Graceful escalation. Records the reason, posts to the human queue,
    and returns the trace so the caller (and the buyer) can audit."""
    trace.record_escalation(reason=reason, notes=notes)
    trace.close(outcome="escalated")
    HumanHandoffQueue.post(trace, reason=reason, notes=notes)
    return trace
