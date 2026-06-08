# QuickBot agent loop.
# We keep this simple. The LLM decides what to do; we run it.

def run_agent(ticket):
    messages = [{"role": "user", "content": ticket.body}]
    while True:
        response = call_llm(messages)
        if response.get("tool_call"):
            tool = response["tool_call"]["name"]
            args = response["tool_call"]["args"]
            result = TOOLS[tool](**args)
            messages.append({"role": "tool", "content": str(result)})
        else:
            # Agent decided it's done.
            return response["text"]
