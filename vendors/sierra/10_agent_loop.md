# Sierra — Agent Orchestration Flow (Public Description)

_Sierra does not publish source code for its agent loop or
orchestrator — this is closed-source proprietary IP. The flow
described below is reconstructed from Sierra's published architecture
posts and product pages:_

- _sierra.ai/blog/constellation-of-models_
- _sierra.ai/blog/agent-os-2-0_
- _sierra.ai/product/trust-and-reliability_
- _sierra.ai/product/develop-your-agent_

_This file documents the orchestration model conceptually. For
implementation details, procurement should request an architecture
briefing under NDA._

## High-level loop

For each customer interaction, the Sierra Agent OS executes roughly
the following flow (paraphrased from Sierra's published architecture):

```
1. INGEST
   - Channel adapter normalizes input (chat / voice transcription /
     email / SMS / WhatsApp / ChatGPT) into a unified turn.
   - PII masking layer encrypts and masks identifiers before they
     enter the LLM context.
   - Topic / keyword filter scans for off-limits content (per-tenant
     policy). Violations route to Live Assist instead of the agent.

2. CONTEXT ASSEMBLY
   - Agent Data Platform (ADP) joins this interaction with the
     customer's historical conversations AND structured customer data
     (CRM, billing, inventory, policy documents).
   - Retriever model pulls relevant policy and knowledge snippets
     (Linnaeus / Darwin search models).

3. PLAN
   - Planner agent interprets the user's intent and decomposes it
     into structured steps with predicted skill invocations.
   - The plan respects the customer's configured guardrails and
     channel constraints.

4. CLASSIFY
   - Classifier model confirms the intent category (e.g. order
     change, refund request, fraud signal, escalation request) —
     this drives downstream skill routing.

5. EXECUTE (per step)
   - Executor agent selects from the customer's enabled skills.
   - The Agent SDK enforces "deterministic API Interactions" — the
     LLM does not write raw API calls; it picks a typed skill.
   - For payment-sensitive operations, execution routes through the
     dedicated PCI-certified infrastructure; payment data never
     enters the LLM context.

6. VALIDATE (before commit)
   - Validator agent reviews the executor's proposed action against
     the tenant's policy rules.
   - On policy violation, the validator blocks the action and routes
     to Live Assist (human handoff with context).
   - On approval, the action commits.

7. RESPOND
   - Tone model composes the customer-facing response with brand
     voice settings applied.
   - Output written back to the channel adapter and delivered to the
     customer.

8. OBSERVE
   - Every step writes to the per-interaction trace.
   - Insights 2.0 surfaces traces in Explorer for diagnosis and A/B
     testing.
   - Continuous evaluation runs against production conversations
     (the "Golden articles" methodology).

CONTINUOUS THROUGHOUT:
   - Provider health monitor watches latency / error rate / timeout
     for each model in the constellation. On degradation, automated
     failover routes traffic to a healthier peer model — no run-time
     interruption.
```

## What's notable from a procurement risk lens

**Strengths (vs. a bare framework like LangGraph):**

1. **Validator-agent-before-commit** is a real shipped safety layer.
   The buyer does not have to build it.
2. **Deterministic API interactions** mean the LLM cannot emit raw
   API calls — only enumerated skills with typed args. Eliminates a
   class of tool-call-correctness risk.
3. **Payment isolation** removes the LLM from a PCI attack surface
   entirely.
4. **Live Assist routing** is a first-class escape valve, not an
   afterthought.
5. **Constellation-of-models with failover** means no single LLM
   outage breaks the platform.

**Gaps in public material:**

1. The actual **validator policy language** isn't published. Customers
   can presumably define policies via Sierra's UI/SDK, but the
   syntax and expressiveness isn't visible publicly.
2. **Loop / recursion ceiling** is not documented. Outcome-based
   pricing absorbs the cost, but a buyer cannot configure a
   per-conversation step limit explicitly from public material.
3. **Contradiction detection** between facts established across a
   long conversation is not explicitly described. Sierra claims
   "memory and continuity" but does not publish a contradiction
   detector or fact-citation requirement.
4. **The orchestrator's source is closed.** Procurement should be
   comfortable trusting Sierra's claims architecturally; code-level
   verification is not available.

## Compare to a framework approach

| Concern | Bare framework (e.g. LangGraph) | Sierra |
|--------|-------------------------------|--------|
| Validation before tool execution | You build it | Shipped (validator agent) |
| Per-tool destructiveness gating | You wire it up | Shipped (payment isolation + supervisor) |
| Failover on LLM outage | You implement | Shipped (constellation routing) |
| PII masking | You implement | Shipped |
| Topic / keyword filters | You implement | Shipped |
| Observability UI | You buy LangSmith | Shipped (Insights 2.0) |
| Code-level inspection | Full source available | Closed source, NDA architecture briefings |
| Per-customer model selection | Full control | Sierra picks per task |
