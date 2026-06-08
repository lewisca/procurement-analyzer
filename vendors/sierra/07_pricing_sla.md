# Sierra — Pricing, SLA, Contract Terms

_Sourced from sierra.ai/blog/outcome-based-pricing-for-ai-agents and
multiple third-party guides published in 2026 (Lorikeet, Quiq, eesel,
Featurebase, Nurix, Ringg). Sierra does not publish a public pricing
page._

## Pricing model

**Outcome-based.** Sierra is paid when an agent achieves a
**successful resolution**. Unresolved queries or escalations to human
agents typically do not trigger a charge.

This is structurally different from token-based or seat-based
pricing — and it shifts the incentive: the vendor wins only when the
agent actually works.

## Typical contract structure

Per third-party reports, contracts combine:

| Component                  | Notes |
|----------------------------|-------|
| Base platform fee          | Annual; covers Agent OS access, baseline observability, model orchestration |
| Per-successful-outcome fee | Per resolved conversation; rate varies by complexity and channel |
| Professional services      | Implementation (4–10 weeks typical), agent design, integration |

## Estimated annual cost (third-party, not Sierra-confirmed)

| Deployment size       | Year-one budget (estimated) |
|------------------------|------------------------------|
| Standard (single channel, moderate volume) | $150K — $350K |
| Multi-channel scaled  | $350K — $750K |
| Large enterprise multi-channel | $750K — $1.5M+ |
| Setup / implementation | $50K — $200K one-time |

These figures are from public third-party analyses; they are not
quoted from Sierra. Treat as order-of-magnitude.

## Implementation timeline

**4–10 weeks** for a managed deployment, per published case studies.
Sierra operates as a managed-deployment vendor, not self-serve SaaS.

## What's bundled (everything tier)

Sierra does not appear to gate features by tier the way LangSmith
does. The product is single-tier (enterprise) with deployment scope
and volume as the cost variables. Per public material, every customer
gets:

- The Agent OS with constellation-of-models orchestration
- Multi-channel deployment (chat, SMS, WhatsApp, email, voice, ChatGPT)
- Insights 2.0 observability
- Simulations / Agent SDK
- Live Assist (human handoff)
- Standard certifications (SOC 2, ISO 27001, ISO 42001, HIPAA, GDPR,
  PCI, CCPA)

EU data residency is documented as an "enterprise plan" feature —
though given Sierra is enterprise-only, this likely means it requires
explicit selection rather than being a tier gate.

## SLA

**Not publicly published.** Standard for enterprise managed AI
vendors at this stage. SLAs are negotiated per contract.

Procurement should establish:
- Uptime guarantee (target ≥99.9% for production agents)
- Response-time guarantee (e.g., p95 latency for the customer agent)
- Incident notification SLA
- SLA credits for misses
- Outage handling for the constellation failover

## Notable terms / model policy

- **Outcome-based pricing protects the buyer from token-cost
  runaway.** If the LLM loops, Sierra eats the cost, not the buyer.
- **Sierra is model-agnostic** (constellation). This means:
  - No single-LLM-provider lock-in for the buyer.
  - But also: when an underlying provider changes its pricing or
    deprecates a model, Sierra absorbs that — buyer should ask how
    that's reflected in renewal pricing.
- **Standard DPA available** (implied by GDPR / SOC 2 posture, not
  explicitly published).

## Budget controls in the runtime

The runtime has no documented buyer-facing token / cost cap because
outcome-based pricing means the buyer isn't billed per token. Sierra
themselves manage cost-runaway risk internally.

## Procurement-relevant questions to ask

1. **Precise definition of "successful resolution"** for billing.
   This is the single most important term.
2. **What counts as a "no-charge" interaction** — escalations,
   abandons, repeats from the same customer?
3. **Volume commitments and minimums** — is there a floor?
4. **Price-protection clauses** when underlying LLM costs rise.
5. **Termination terms** — what happens to your data, your agent
   configuration, your traces?
6. **SLA specifics** — uptime, latency, credit structure.
7. **Year-2 escalation** — typical % annual increase.
