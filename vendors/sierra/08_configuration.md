# Sierra — Configuration Surface

_Sierra is a managed platform; configuration is exposed through the
Sierra console, the Agent SDK, and (for some enterprise items)
through implementation services. There is no public per-tenant
configuration YAML the way an OSS framework would publish._

_Sources: sierra.ai/product/develop-your-agent (Agent SDK);
sierra.ai/blog/agent-studio-2-0._

## What customers configure

### Agent composition (via Agent SDK / Agent Studio)

- **Skills** — composable units (triage, respond, confirm, execute);
  selected and stacked per workflow.
- **Policies / guardrails** — rules the supervisor agent enforces.
- **Tone** — brand voice settings.
- **Flexibility / determinism dial** — Sierra documents this
  explicitly: *"Define the degree of flexibility your agent should
  exhibit for each workflow, allowing for varying levels of creativity
  and determinism."*
- **Routing / channel deployment** — which channels (chat, SMS,
  email, voice, WhatsApp, ChatGPT) the agent serves.

### Integrations (deployment / implementation)

- **Systems of record** — CRM (Salesforce, HubSpot), payment gateway,
  internal APIs.
- **Data sources** — Snowflake, Databricks, Redis, Google Cloud, AWS.
- **Communication channels** — twilio, voice infra, email, etc.

### Operational settings

- **Topic / keyword filters** — off-limits content per company policy.
- **Live Assist routing** — when/how to escalate to a human agent.
- **A/B test plans** — variants of agent behavior to test in
  production.

## What Sierra controls (not customer-configurable)

This is what a managed-platform buyer trades off vs. building on a
framework like LangGraph:

- **Model selection within the constellation** — Sierra picks which
  of the 15+ models handle which sub-task. Customer can request
  changes but doesn't choose per-task.
- **Failover policy** — Sierra's automated routing decides when to
  fail over between LLM providers.
- **Eval cadence and methodology** — Sierra runs continuous
  evaluation; customer sees Insights output, not the underlying
  scoring code.
- **Supervisor / validator rule language** — public material doesn't
  describe a customer-editable policy DSL. Policies appear to be
  defined collaboratively during implementation.

## What is NOT in Sierra's documented configuration

Compared to a typical enterprise SaaS admin console, the following
items are **not visible in public material** and would need to be
confirmed during procurement:

- Per-run token / cost budgets — not exposed (outcome-based pricing
  makes this less relevant for buyer, but still worth confirming for
  observability).
- Per-conversation step limits — not exposed.
- Recursion / loop ceilings — not exposed publicly.
- Custom alert routes / SIEM integration for runtime events.
- Custom retention windows for traces (Insights data).
- BYOK encryption keys — not documented as customer-controllable.

## Sierra Insights (the observability surface)

| Component         | What customer can do |
|-------------------|----------------------|
| Insights Explorer | Browse and analyze interactions to diagnose issues |
| Expert Answers    | Curate knowledge that grounds agent responses |
| Trace inspection  | "inspecting API calls, logic traces, and more" via Agent Studio |
| A/B testing       | Define variants, route traffic, measure outcomes |

## Procurement-relevant questions

For a managed-platform buyer, the configuration questions matter less
than they would for a framework — Sierra is responsible for the
runtime. But for governance and ongoing operations:

1. **Who at Sierra can change agent policy in production**, and is
   that change logged in an admin audit log we can see?
2. **What retention can we set on Insights traces**, and can we
   export to our SIEM in real time?
3. **How do we override a supervisor decision** in case of a false
   positive (legitimate transaction blocked)?
4. **What's the runbook** when the constellation routing produces a
   degraded customer experience?
