# Salesforce Agentforce — Configuration Reference

_Sourced from the Atlas Reasoning Engine writeup, Agentforce Studio
documentation, and Salesforce's published Agentforce material._

## Configuration philosophy

Agentforce configuration is **admin-driven, not developer-driven** —
the unit of configuration is the Topic, configured via the
Agentforce Studio admin console. Developer code (Apex, Flows) is
written as Actions that Topics bind to, but the agent definition
itself is declarative.

This is structurally different from OpenAI / Anthropic / LangGraph,
where the agent is a code object. In Agentforce, the agent is a
Salesforce metadata object.

## Topic configuration

A Topic is the primary configuration unit. Each Topic includes:

| Field | Purpose |
|-------|---------|
| **Topic ID** | Unique identifier |
| **Instructions** | Natural-language description of when to use this Topic |
| **Policies** | Natural-language business rules (e.g., "refunds > $200 require approval") |
| **Allowed Actions** | List of Actions the agent can invoke when on this Topic |
| **Escalation triggers** | Conditions that trigger 'transfer to human' |
| **Knowledge sources** | Data Cloud sources to ground responses |

Topics are configured in the Agentforce Studio admin console.
Changes typically require admin permissions and may flow through
Salesforce's standard change management (sandbox → UAT → production).

## Action configuration

Actions are the agent's tools. They map to Salesforce primitives:

| Action type | Configured by |
|-------------|---------------|
| **Flow** | Salesforce admin / declarative developer |
| **Apex** | Salesforce developer |
| **API** | Integration developer |
| **MCP** (Spring '26) | Connect MCP-compatible external systems |
| **Slack / Email** | Standard Salesforce config |

Each Action has:

- Input schema (typed parameters)
- Topic bindings (which Topics can invoke this Action)
- Permission requirements (which user profiles can trigger)
- Sandbox / production scoping

## Einstein Trust Layer configuration

The Trust Layer is configurable per-tenant:

- **PII detection rules** (which fields are PII; what masking pattern)
- **Toxicity thresholds** (configurable severity)
- **Prompt-injection rules** (custom + default)
- **Topic-level audit requirements** (full vs summary)
- **Region pinning** (where the LLM call routes geographically)

Trust Layer config is typically scoped to the Salesforce org and
applies to all Agentforce deployments in that org.

## Multi-LLM routing

Atlas's constellation-of-models is **not directly buyer-configurable**.
Salesforce decides which LLM handles which sub-task based on
performance, cost, and capability. Buyers can:

- Approve / reject sub-processor changes via the sub-processor
  notification mechanism
- Negotiate model-pinning for sensitive workloads (enterprise tier)
- Specify region constraints (which limit available models)

This is **less buyer control than OpenAI/Anthropic** (where you pick
the model explicitly) but **more abstraction** (Salesforce manages
the routing complexity).

## Observability configuration

| Surface | What it shows |
|---------|---------------|
| **Command Center** | Per-conversation agent activity, decisions, failure states |
| **Event Monitoring** (add-on) | Detailed audit logs at the platform level |
| **Salesforce Reports** | Build custom reports on Agentforce activity |
| **Einstein Studio** | Manage models, prompts, fine-tuning |
| **Data Cloud Activations** | How Agentforce reads / writes data |

## What is NOT in the configuration surface

Compared to a developer-built agent (OpenAI Agents SDK, Anthropic
Agent SDK):

- **No per-run cost cap** (use per-conversation pricing or Flex
  Credit org caps)
- **No per-execution step ceiling** visible to admins (Atlas manages
  internally)
- **No "plan" / dry-run mode** for arbitrary runs (sandbox orgs are
  the dry-run mechanism)
- **No buyer access to the underlying agent loop source** — Atlas is
  proprietary
- **No first-class hook lifecycle** (Anthropic-style PreToolUse) —
  approval flows are Salesforce Approval Process, which is mature but
  shaped differently

## Configuration vs developer-friendly platforms

| Concern | Agentforce (admin-config) | Anthropic / OpenAI (developer-built) |
|---------|---------------------------|--------------------------------------|
| Who configures the agent? | Salesforce admin via Studio | Developer in code |
| How are guardrails set? | Topic policies + Trust Layer config | Hooks / guardrails in code |
| How is approval gating done? | Salesforce Approval Process | Code-level (PreToolUse, InputGuardrail) |
| How is observability configured? | Command Center settings + Event Monitoring | Tracing exporters + logging code |
| How are tools defined? | Actions in Flow / Apex / API | Function decorators + JSON Schema |
| Iteration speed | Slower (change management, sandboxes) | Faster (code, deploy) |

The implication: **Agentforce is best when the buyer has
significant Salesforce admin maturity already.** A team without
Salesforce admin / developer skills will struggle to configure
Agentforce well even though the product itself is well-designed.

## Procurement-relevant takeaways

- Agentforce assumes a deep Salesforce-admin capability on the
  buyer side. This is "free" if the buyer is already a Salesforce
  shop; it's a significant capability requirement otherwise.
- The Topic + Action model is one of the strongest "configuration as
  guardrail" patterns in the agent vendor landscape. Topic-scoped
  Action sets are structurally enforceable in a way that depends
  on the buyer's admin discipline.
- Change management for agent configuration follows Salesforce's
  standard sandbox → UAT → production model. Slower than
  developer-built agents but more audit-friendly for regulated
  industries.
