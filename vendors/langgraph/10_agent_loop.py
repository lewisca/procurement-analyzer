"""LangGraph — agent loop excerpt.

This is a verbatim excerpt (with light condensing) of the agent-loop
control flow from LangGraph's prebuilt `create_react_agent` factory at
libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py.

The full file is ~1015 lines; what follows is the canonical loop —
how the agent decides whether to call a tool or terminate, and how
the step-budget guard works.

Source: github.com/langchain-ai/langgraph (main branch, MIT license).
"""

# --- Step-budget guard ------------------------------------------------------

def _are_more_steps_needed(state, response):
    """Returns True if the agent should stop because the step budget
    can't accommodate another round of tool calls.

    `remaining_steps` is a state field maintained by the runtime; the
    `recursion_limit` set on graph.invoke() decrements this counter.
    """
    has_tool_calls = isinstance(response, AIMessage) and response.tool_calls
    all_tools_return_direct = (
        all(call["name"] in should_return_direct for call in response.tool_calls)
        if isinstance(response, AIMessage)
        else False
    )
    remaining_steps = _get_state_value(state, "remaining_steps", None)
    if remaining_steps is not None:
        if remaining_steps < 1 and all_tools_return_direct:
            return True
        elif remaining_steps < 2 and has_tool_calls:
            return True

    return False


# --- The agent node (LLM call) ----------------------------------------------

def call_model(state, runtime, config):
    """Called once per loop iteration. Invokes the LLM, returns the
    AIMessage as a state update. If the step budget is low, emits a
    sentinel response instead of trying another round."""
    model_input = _get_model_input_state(state)

    if is_dynamic_model:
        dynamic_model = _resolve_model(state, runtime)
        response = cast(AIMessage, dynamic_model.invoke(model_input, config))
    else:
        response = cast(AIMessage, static_model.invoke(model_input, config))

    response.name = name

    if _are_more_steps_needed(state, response):
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, need more steps to process this request.",
                )
            ]
        }
    return {"messages": [response]}


# --- The loop's routing function ---------------------------------------------
# This is the agent loop's central decision: continue (call tools) or terminate.

def should_continue(state):
    """Inspects the latest message. If the LLM emitted tool_calls,
    route to the tools node. If not, terminate (END), or route to
    structured-response generation if response_format was specified."""
    messages = _get_state_value(state, "messages")
    last_message = messages[-1]

    # If there is no function call, then we finish
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        if post_model_hook is not None:
            return "post_model_hook"
        elif response_format is not None:
            return "generate_structured_response"
        else:
            return END

    # Otherwise if there is, we continue
    else:
        if version == "v1":
            return "tools"
        elif version == "v2":
            if post_model_hook is not None:
                return "post_model_hook"
            # v2 streams: dispatch every tool_call as a Send for parallel execution
            return [
                Send(
                    "tools",
                    ToolCallWithContext(
                        __type="tool_call_with_context",
                        tool_call=call,
                        state=state,
                    ),
                )
                for call in last_message.tool_calls
            ]


# --- Assembling the StateGraph ----------------------------------------------

workflow = StateGraph(
    state_schema=state_schema or AgentState,
    context_schema=context_schema,
)

# The two nodes the loop cycles between.
workflow.add_node(
    "agent",
    RunnableCallable(call_model, acall_model),
    input_schema=input_schema,
)
workflow.add_node("tools", tool_node)

# Optional hooks (pre/post the agent node).
if pre_model_hook is not None:
    workflow.add_node("pre_model_hook", pre_model_hook)
    workflow.add_edge("pre_model_hook", "agent")
    entrypoint = "pre_model_hook"
else:
    entrypoint = "agent"

workflow.set_entry_point(entrypoint)

# Conditional edges drive the loop: agent decides whether to call tools.
workflow.add_conditional_edges(
    "agent",
    should_continue,
    # ... possible destinations are: "tools", "post_model_hook",
    #     "generate_structured_response", or END
)

# After tools execute, return to the entry point (or pre_model_hook) for
# the next LLM turn. This is the CYCLE that makes it an agent loop.
workflow.add_edge("tools", entrypoint)

graph = workflow.compile(checkpointer=checkpointer, store=store)


# --- What this code does NOT include --------------------------------------
#
# The loop above:
#   - Stops on step-budget exhaustion (via _are_more_steps_needed).
#   - Stops when the LLM produces no tool_calls (a natural finish).
#   - Catches tool exceptions inside ToolNode and returns them to the LLM
#     as ToolMessage content (the LLM gets another shot).
#
# The loop above does NOT include:
#   - Semantic loop detection (same tool, same args, repeated)
#   - Bounded retry counter on tool errors
#   - Contradiction or hallucination detection
#   - Cost / token budget enforcement
#   - Dry-run / simulation mode
#   - Per-tool destructiveness classification with approval gates
#
# Users who need these guarantees layer them on top — typically as
# additional nodes or post_model_hook implementations.
