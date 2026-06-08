"""OpenAI Agents SDK — Runner loop excerpts.

Verbatim excerpts (with light condensing) from
github.com/openai/openai-agents-python (MIT licensed, src/agents/run.py).
The full file is ~1879 lines; what follows is the canonical agent loop
showing: turn-budget enforcement, guardrail tripwire integration, and
the cycle between agent → tools → agent.

Source: src/agents/run.py (Runner / AgentRunner classes).
"""

# --- Entry point (Runner.run docstring, verbatim) ----------------------------

async def run(
    starting_agent,
    input,
    *,
    context=None,
    max_turns=DEFAULT_MAX_TURNS,    # default = 10
    hooks=None,
    run_config=None,
    error_handlers=None,
    previous_response_id=None,
    auto_previous_response_id=False,
    conversation_id=None,
    session=None,
):
    """
    Run a workflow starting at the given agent.

    The agent will run in a loop until a final output is generated. The loop runs like so:

      1. The agent is invoked with the given input.
      2. If there is a final output (i.e. the agent produces something of type
         `agent.output_type`), the loop terminates.
      3. If there's a handoff, we run the loop again, with the new agent.
      4. Else, we run tool calls (if any), and re-run the loop.

    In two cases, the agent may raise an exception:

      1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.
      2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered
         exception is raised.
    """
    ...


# --- The hard step-budget enforcement (verbatim, line ~1057-1081) -----------

#                     current_turn += 1
#                     if max_turns is not None and current_turn > max_turns:
#                         _error_tracing.attach_error_to_span(
#                             current_span,
#                             SpanError(
#                                 message="Max turns exceeded",
#                                 data={"max_turns": max_turns},
#                             ),
#                         )
#                         max_turns_error = MaxTurnsExceeded(f"Max turns ({max_turns}) exceeded")
#                         run_error_data = build_run_error_data(
#                             input=original_input,
#                             new_items=session_items,
#                             raw_responses=model_responses,
#                             last_agent=current_agent,
#                             reasoning_item_id_policy=resolved_reasoning_item_id_policy,
#                         )
#                         handler_result = await resolve_run_error_handler_result(
#                             error_handlers=error_handlers,
#                             error=max_turns_error,
#                             context_wrapper=context_wrapper,
#                             run_data=run_error_data,
#                         )
#                         if handler_result is None:
#                             raise max_turns_error
#
#                         # If a handler intercepts the error, synthesize a graceful final output.
#                         validated_output = validate_handler_final_output(
#                             current_agent, handler_result.final_output
#                         )
#                         output_text = format_final_output_text(current_agent, validated_output)
#                         synthesized_item = create_message_output_item(current_agent, output_text)
#                         ...


# --- The guardrail tripwire (verbatim from src/agents/guardrail.py) ---------

# class GuardrailFunctionOutput:
#     tripwire_triggered: bool
#     """Whether the tripwire was triggered. If triggered, the agent's
#     execution will be halted."""
#
# class InputGuardrail(Generic[TContext]):
#     """Input guardrails run in parallel with the agent's invocation,
#     enabling early validation and fail-fast behavior. Guardrails return a
#     `GuardrailResult`. If `result.tripwire_triggered` is `True`, the agent
#     run is halted."""


# --- What this code captures vs. what it doesn't ----------------------------
#
# CAPTURED (shipped in the SDK):
#   - Hard max_turns enforcement (default 10, configurable, runtime-checked).
#   - Graceful error_handlers escape for max_turns exhaustion.
#   - Input and output guardrails with tripwire halting.
#   - Built-in tracing spans for every model call, tool call, guardrail.
#   - Handoffs as a first-class delegation primitive.
#   - Session / Responses API state for cross-turn memory.
#
# NOT CAPTURED (developer's responsibility):
#   - Semantic loop detection (same tool, same args, repeated). Only step
#     counter is enforced.
#   - Bounded retry counter on tool errors.
#   - Foreign-key / business-rule validation. Schema validation is decode-time
#     strict mode; business rules belong in tool function bodies or guardrails.
#   - Contradiction detection across turns.
#   - Per-tool destructiveness classification.
#   - Cost cap per run. Token-based pricing means cost is bounded by
#     max_turns × max_output_tokens × model rate, but there's no dollar-cap
#     primitive in the SDK itself. Org-level spend caps live in the OpenAI
#     dashboard.
