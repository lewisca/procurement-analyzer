# Salesforce Agentforce — Product Overview

_Sourced from salesforce.com/agentforce (gated), cirra.ai's Atlas
technical writeup, salesforce.com/agentforce/pricing/,
compliance.salesforce.com, and multiple third-party 2026 implementation
guides._

## What it is

Agentforce is Salesforce's enterprise AI agent platform — a managed,
closed-source product layered on top of the Salesforce CRM platform.
It's a complete agent product (not a framework, not an SDK), and the
core selling point is **deep integration with Salesforce data and
workflows** rather than agent capabilities in isolation.

## Architecture (three layers, per Salesforce)

| Layer | What it does |
|-------|-------------|
| **Atlas Reasoning Engine** | The agent loop. ReAct-style: Reason → Act → Observe. Processes user intent, builds an execution plan, selects and invokes Actions, validates outputs. |
| **Data Cloud Grounding** | Connects the agent to live CRM data via zero-copy architecture — data is retrieved, never duplicated. Agent answers ground in real customer records. |
| **Einstein Trust Layer** | Security wrapper enforcing PII masking, toxicity detection, hallucination mitigation, zero data retention with LLM providers, prompt-injection defense, audit logging. |

## What Atlas Reasoning Engine does

From the Atlas technical writeup:

> "Atlas begins by mapping user inputs to predefined 'Topics' representing
> specific intents. Each topic includes relevant natural-language
> instructions, business policies, and an allowed set of Actions. This
> scoping mechanism constrains the reasoning problem and embeds
> guardrails directly into the agent's decision-making framework."

**Topics as built-in guardrails.** Each agent operates within a Topic
(e.g., "process refund," "schedule appointment," "lookup order
status"). The Topic limits which Actions the agent can perform — so
the universe of possible actions is bounded by configuration, not
discovered at runtime.

### The ReAct loop

```
Reason: LLM generates step-by-step thinking about the problem
Act:    Agent executes chosen actions (DB queries, API calls, workflow triggers)
Observe: Results feed back into reasoning, allowing dynamic adaptation
```

The loop "incorporates new context or clarifications from the user
mid-task" rather than executing a fixed plan rigidly.

### Multi-model ensemble

Atlas routes sub-tasks to different LLMs:

> "Salesforce deepened partnerships with OpenAI and Anthropic to
> incorporate latest LLMs including GPT-5 and Claude variants. Atlas
> acts as an intelligent controller that can route sub-tasks to
> different models or knowledge sources, optimizing for both quality
> and cost-effectiveness."

This is structurally similar to Sierra's "constellation of models"
approach, but specifically with named partnerships to OpenAI and
Anthropic.

## Action types (the agent's "tools")

Actions available depend on the active Topic and may include:

- **Salesforce Flow** automations
- **Apex** code or **API** calls
- **Slack** / chatbot messages
- **Email** dispatch
- **Integrated service** invocations
- **MCP-compatible external systems** (added in Spring '26)

The MCP integration in Spring 2026 was important — Agentforce can
now connect to any MCP server without custom API development. This
narrows a key historical gap vs OpenAI / Anthropic agent platforms.

## Customers and maturity

Salesforce had a public "$2 per conversation" launch in 2024,
restructured to Flex Credits at $0.10/action in May 2025, and then
added per-user licensing at $125/user/month. Three concurrent pricing
models in 2026 — sign of a product still finding product-market fit
on the commercial side, even though the technical platform is
production-deployed.

Customer adoption is broad — Salesforce's existing enterprise base
(150K+ companies on the platform) is the deployment surface. Notable
public claims: 85% AI resolution rates for some customer support
deployments.

## What it does

- **Customer-facing agents** (support, sales, service)
- **Employee-facing agents** (internal productivity, ops)
- **Agentforce Voice** (voice channel)
- **Branded multi-channel deployment** — chat, voice, email, SMS, in-app

## What it does not do (out of scope by design)

- **Not a general-purpose agent framework.** Agentforce only works in
  the Salesforce ecosystem. If your systems of record live outside
  Salesforce, integration cost is significant (Data Cloud licensing
  alone is $108K/year minimum).
- **Not self-serve or low-code-friendly outside Salesforce's admin
  paradigm.** Production deployment typically requires Salesforce
  partner / consulting services. Year-1 pilot budgets run $150K–$200K.
- **Not multi-cloud-portable.** Bound to Salesforce-managed
  infrastructure.

## Procurement-relevant positioning

Agentforce is the **enterprise-platform extreme** of the agent vendor
landscape. Compared to OpenAI Agents SDK (developer-built),
Anthropic Claude Agent SDK (developer-built with safety primitives),
Sierra (managed-CX vertical), and LangGraph (OSS framework):

- Agentforce ships **the most enterprise compliance** (SOC 2 + ISO
  27001 + ISO 27018 + PCI-DSS + HIPAA + **FedRAMP** + GDPR)
- Agentforce has **the deepest integration** with existing Salesforce
  data and workflows
- Agentforce has **the highest implementation cost** and platform
  lock-in
- Agentforce uses other vendors' LLMs (OpenAI, Anthropic) under the
  hood — it's not a foundation model company

The model-policy implication: Salesforce's LLM strategy is **fully
delegated** to OpenAI and Anthropic. Buyers concerned about
foundation-model lock-in get distance from that risk — Atlas can in
principle swap models.
