# Salesforce Agentforce — Pricing, SLA, Contract Terms

_Sourced from salesforce.com/agentforce/pricing/ (referenced),
multiple third-party 2026 implementation guides
(saastr.com, rizexlabs.com, ekfrazo.com, jitendrazaa.com)._

## Three concurrent pricing models

Salesforce has shipped **three different pricing models** for
Agentforce in 18 months — a sign of commercial experimentation:

| Model | Launched | Cost basis |
|-------|----------|-----------|
| **Per-conversation** | Original launch | $2 per conversation |
| **Flex Credits** | May 2025 | $500 per 100,000 credits ($0.005/credit); standard action = 20 credits ($0.10); voice action = 30 credits ($0.15) |
| **Per-user license** | 2026 | Starting at $125/user/month |

The SaaStr commentary: "Salesforce now has 3+ pricing models for
Agentforce. And maybe right now, that's the way to do it." Buyers
should pick the model that matches their workload shape.

## Per-conversation vs Flex Credits tradeoff

- **Per-conversation** ($2): predictable per-interaction cost.
  Bounded by conversation count, not by agent action count.
  Best for: high-action-count workflows where a single conversation
  involves many tool calls.
- **Flex Credits** ($0.10/action, $0.15 voice): pay-per-action.
  Best for: simple workflows with few actions per conversation.
- **Per-user license** ($125/user/month): predictable per-user
  cost. Best for: employee-facing agents with high per-user usage.

## Enterprise buying structures (Flex Credits)

Three Flex Credits purchasing modes:

| Mode | Description |
|------|------------|
| **Pre-purchase** | Credits bought upfront at contracted rate, drawn down as consumed |
| **Pay-as-you-go** | Billed monthly in arrears based on actual usage; no upfront commitment |
| **PreCommit** | Volume-based with negotiated rates; for large-scale deployments |

## Hidden costs (the procurement gotcha)

Per third-party 2026 reports, the realistic Year-1 budget is
**substantially higher than the headline rate**:

| Line item | Cost |
|-----------|------|
| Data Cloud (required) | $108,000 / year minimum |
| Pilot implementation | $20,000 – $40,000 one-time |
| Usage costs | Variable |
| **Conservative Year 1 (single-use pilot)** | **$150,000 – $200,000** |

For scaled enterprise multi-channel deployments:

- Standard scaled deployment: $350,000 – $750,000 / year
- Large enterprise multi-channel: $750,000 – $1,500,000+ / year

These are third-party estimates, not Salesforce-quoted; treat as
order of magnitude.

## SLA

Salesforce inherits its 25-year-old enterprise SLA framework:

- **Standard uptime**: 99.9% target on Standard tier
- **99.95%+** on higher tiers / Government Cloud
- **Mature credits structure** for misses
- **Public status page** at status.salesforce.com with full history
- **Government Cloud Plus** has dedicated SLAs for federal workloads

Specific numbers are negotiated per contract. Salesforce SLAs are
known to be enterprise-credible — this is one of the company's most
established commercial dimensions.

## Multi-year discounts

Per third-party reports:

> "Multi-year commitments unlock better per-conversation rates and
> platform pricing. Organizations willing to commit to 3-year
> agreements with minimum volume guarantees can often negotiate
> 20–40% reductions in effective cost."

Standard enterprise practice. Worth pursuing.

## Buyer cost-runaway controls

- **Per-conversation tier**: bounded by definition ($2 / conversation
  regardless of action count)
- **Flex Credits**: NOT bounded — agent action count drives cost.
  Buyer should set:
  - Org-level monthly Flex Credit cap
  - Topic-level action budgets where supported
  - Alerting on burn rate
- **Per-user license**: bounded by license count

Comparison to other vendors:

- Sierra (outcome-based pricing): vendor eats cost runaway risk
- OpenAI / Anthropic (token-based): buyer eats cost runaway risk
  with controls (max_tokens, org spend caps)
- **Salesforce Flex Credits**: token-style buyer risk (per-action)
- **Salesforce per-conversation**: outcome-style bounded risk

## Contractual terms

- **Standard MSA** — extensively negotiated at enterprise scale
- **DPA** available; SCCs for EU/UK
- **BAA** for HIPAA
- **Indemnification** — IP and output indemnification standard at
  enterprise tier
- **Termination** — typically 30-60 day notice with data-export
  obligations
- **Data export** — Salesforce provides comprehensive export tools;
  data portability is generally good within Salesforce's
  documentation
- **Model-change notice** — Atlas's underlying LLMs may change
  without buyer notification; the abstraction is sub-processor-list
  managed, not per-deployment
- **FedRAMP** — separate contract path for Government Cloud Plus
  required by federal procurement rules

## Multi-cloud / portability

**Limited.** Agentforce is bound to Salesforce-managed
infrastructure. Government Cloud Plus is a separate dedicated
environment for federal workloads.

Multi-cloud agnosticism (Bedrock / Vertex / Azure) of foundation
model providers does NOT transfer to Salesforce — once the agent
is built on Agentforce, the platform is Salesforce.

## Procurement-relevant questions to ask

1. **Which pricing model fits our workload?** Run the per-conversation
   vs Flex Credits math with realistic action counts before signing.
2. **Multi-year discount terms** — what volume commitment unlocks
   20-40% discount?
3. **Data Cloud requirement** — already licensed? If not, the $108K
   minimum is a real line item.
4. **Implementation services** — Salesforce direct vs partner; what's
   in scope?
5. **Government Cloud Plus pricing** if FedRAMP is required (separate
   negotiation).
6. **Cost controls on Flex Credits** — what spend-cap tooling is
   available?
7. **Year-2 escalation** — typical % annual increase on Salesforce
   contracts; bake into TCO.
