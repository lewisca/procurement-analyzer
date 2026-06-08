# LangGraph — Configuration Reference

_Sourced from the LangGraph persistence and overview docs at
docs.langchain.com/oss/python/langgraph. This summarizes the
configuration surface a buyer would need to know about when adopting
LangGraph. As an OSS library, configuration is code-level (Python),
not a managed-platform admin console._

## Per-graph invocation config

Passed via the `config` kwarg on `graph.invoke()` / `graph.stream()`:

```python
config = {
    "configurable": {
        "thread_id": "user_42_session_3",     # ties checkpoints together
        "checkpoint_ns": "",                  # subgraph namespace
        "checkpoint_id": "1ef-step-5",        # for replay from a specific checkpoint
        # any custom keys your nodes read via RunnableConfig
    },
    "recursion_limit": 25,    # hard step limit; default 25
    "callbacks": [...],       # observability hooks (LangSmith, custom)
    "tags": ["agent_v3", "tenant_acme"],
    "metadata": {"user_id": "u_42"},
}

graph.invoke(input, config)
```

### `recursion_limit`

- Default: 25
- Hard ceiling on the number of super-steps in a single graph run.
- When exceeded: `GraphRecursionError` is raised (or, for the
  prebuilt `create_react_agent`, the agent emits the sentinel
  "need more steps to process this request" message and terminates
  cleanly).

### `thread_id`

- Required when a checkpointer is attached.
- Groups all checkpoints for one conversation / agent run.

### `durability`

- `"exit"` — persist only on graph completion or error
- `"async"` — persist asynchronously during next step (default)
- `"sync"` — synchronous persist before next step

## Compile-time config

Set on `graph.compile()`:

```python
graph.compile(
    checkpointer=PostgresSaver(conn),      # required for persistence
    store=PostgresStore(conn),             # cross-thread memory
    interrupt_before=["tools"],            # human-in-the-loop gate
    interrupt_after=[],                    # post-node interrupts
    debug=False,                           # extra debug logging
)
```

### Checkpointer backends supported

- **`InMemorySaver`** — dev/testing only; lost on restart.
- **`SqliteSaver` / `AsyncSqliteSaver`** — local single-node workflows.
- **`PostgresSaver` / `AsyncPostgresSaver`** — production
  recommended. Supports both sync and async drivers.
- **`CosmosDBSaver`** — Azure Cosmos DB with Microsoft Entra auth.

All implement the `BaseCheckpointSaver` interface: `.put()`,
`.put_writes()`, `.get_tuple()`, `.list()`.

### Encryption at the checkpoint layer

Optional. Off by default. Enabled by wrapping the checkpointer's
serializer:

```python
from langgraph.checkpoint.serde.encrypted import EncryptedSerializer

serde = EncryptedSerializer.from_pycryptodome_aes()   # reads LANGGRAPH_AES_KEY env var
checkpointer = PostgresSaver(conn, serde=serde)
```

## Stream / observability modes

Passed via `stream_mode` on `graph.stream()`:

| Mode          | What you get |
|---------------|--------------|
| `values`      | Full state after each step |
| `updates`     | State updates per step (changed keys only) |
| `messages`    | LLM token-by-token output with node metadata |
| `custom`      | User-emitted data via `get_stream_writer()` |
| `checkpoints` | Checkpoint events (requires checkpointer) |
| `tasks`       | Task start/finish with results and errors |
| `debug`       | Combines checkpoints + tasks + metadata (most verbose) |

For audit-trail purposes, `debug` mode is the closest equivalent to
a structured per-step log.

## What configuration is NOT in LangGraph

LangGraph does **not** provide configuration for:

- Cost or token budgets per run (use the LLM client's controls
  instead).
- Tool allowlists at the runtime level (compile-time — the tools
  passed to `create_react_agent` are the allowlist).
- Approval thresholds based on tool destructiveness (must be coded
  in the graph topology with `interrupt_before`).
- Tenant isolation / multi-tenancy at the framework level (runs in
  the buyer's process; tenant separation is a deployment concern).
- RBAC / SSO at the framework level (these live in LangSmith or your
  own auth layer).
- Alert routes / notification channels.

These are deployment-layer or LangSmith-layer concerns, not OSS
runtime concerns. A buyer evaluating a LangGraph-based product should
ask the integrator how each is wired in their stack.
