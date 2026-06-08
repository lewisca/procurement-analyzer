# Sierra — Product Overview

_Sourced from sierra.ai, sierra.ai/about, sierra.ai/blog/agent-os-2-0,
and the sierra.ai/blog/constellation-of-models architecture post._

## What Sierra is

Sierra is a managed, enterprise AI agent platform purpose-built for
customer experience. Its positioning is **"AI Agent OS"** — a complete
managed product (not a framework) for building, deploying, and
optimizing customer-facing AI agents at Fortune 500 scale.

Headline numbers (May 2026):

- $15.8B valuation; $950M Series E
- $150M+ ARR
- 40%+ of the Fortune 50 as customers
- Co-founded by Bret Taylor (former Co-CEO Salesforce, ex-CTO Facebook,
  OpenAI board) and Clay Bavor (18-year Google veteran, led Project
  Starline)

## What it does

- **Multi-channel customer agents** — one agent deployed across chat,
  SMS, WhatsApp, email, voice, and ChatGPT.
- **Outcome-oriented execution** — agents not just answer but take
  actions (update CRM, manage orders, process subscriptions).
- **Personalization at runtime** — agents pull from customer's
  structured data (Snowflake, Databricks, Redis, Google Cloud, AWS) to
  contextualize each interaction.
- **Live Assist** — agents hand off to humans on demand.
- **A/B testing and optimization** — built-in experimentation
  on agent behavior.

## What it does not do (explicit positioning)

- Sierra is **not a framework**. There's no "use it for any agent
  workflow" pitch. It is scoped to customer experience and the
  systems that power it.
- Sierra is **not self-serve**. Implementation is a managed
  deployment, typically 4–10 weeks, with professional services.
- Sierra **does not replace human agents** — explicit company
  commitment that AI is augmentation, not elimination. "If a member
  wants to speak to a human, that's always an option."

## How agents are built

Customers don't write monolithic agent code. Agents are composed via
the **Agent SDK** as a stack of skills (triage, respond, confirm,
execute) plus policies, retrievers, and tone settings. Sierra also
offers **Ghostwriter** — agents are scaffolded from SOPs, transcripts,
or plain-English descriptions.

Implementation flow:

1. Sierra solution engineers (or partner consultants) work with the
   customer to define the agent's scope, policies, and integrations.
2. Skills are composed via the Agent SDK.
3. Simulations test against a curated dataset and adversarial scenarios.
4. Phased production rollout with continuous A/B testing.

## Customer logos (public)

Financial services: Rocket Mortgage, SoFi, Brex.
Telecom: SiriusXM, Singtel.
Healthcare: Sutter Health, R1 RCM.
Retail / consumer: Gap Inc., Wayfair, ASOS, Rivian, Redfin, CLEAR.
Other: Discord, Docusign, WeightWatchers.

## Model policy

Sierra's defining technical choice is a **constellation of 15+ models**
— frontier, open-weight, and proprietary — orchestrated for different
sub-tasks. Examples documented by Sierra:

- Low-latency models for quick tool-calling (e.g. order management).
- High-precision classification models for nuanced behavior (e.g.
  fraud detection).
- Long-context reasoning models for dense information processing.
- Tone-optimization models for warm, on-brand conversational responses.

Automatic failover between LLM providers when one degrades. Buyer is
abstracted from any single-vendor risk.
