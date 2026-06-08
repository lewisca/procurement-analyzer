# OpenAI Agents — Pricing and SLA

_Sourced from openai.com/api/pricing/ (gated via bot-block on
WebFetch; figures verified via developers.openai.com/api/docs/pricing
and third-party reports). All figures USD as of mid-2026._

## Pricing model

**Token-based.** Pay per input/output token consumed across model
calls. This is the opposite of Sierra's outcome-based model — runaway
agents cost the buyer real money. Token budgets and per-execution
limits are the buyer's tools to bound this exposure.

## Per-million-token pricing (2026)

| Model | Input | Output | Notes |
|-------|------:|-------:|-------|
| GPT-5.5 | $5.00 | $30.00 | Flagship |
| GPT-5.4 | $2.50 | $15.00 | Cost-efficient flagship |
| GPT-5 | $1.25 | $10.00 | Aug 2025 release; lower-cost option |
| GPT-4o (legacy) | varies | varies | Maintained for backward compat |
| o-series (reasoning) | varies | varies | Premium for extended deliberation |

**Cached input** is discounted 90% across GPT-5.x. E.g., GPT-5.5
cached input drops from $5.00 to $0.50 per million tokens. This makes
multi-turn agents substantially cheaper than the headline number
suggests.

**Batch API** and **Flex** processing cut the standard short-context
GPT-5.5 from $5/$30 to $2.50/$15 per million input/output — a 50%
discount for workloads that tolerate latency.

## Built-in tool pricing

| Tool | Pricing |
|------|---------|
| Function calling | Free (you pay for the tokens) |
| File search | Per call (Responses API only) |
| Web search | Fixed 8,000 input-token block per call (on gpt-4o-mini and gpt-4.1-mini non-preview) |
| Code Interpreter | Per session — billed at full 20-minute session rate, includes hosted shell |
| Computer use | Per call + token cost |
| MCP servers | Free (per-call cost goes to the MCP server provider, not OpenAI) |

## Per-tier pricing for ChatGPT (managed product)

The Agents SDK and Responses API are usage-priced (above). For the
**managed ChatGPT Enterprise / Business / Edu / Healthcare** SKUs,
pricing is per-seat:

| Tier | Approximate per-seat (annual contract) |
|------|----------------------------------------|
| ChatGPT Team | ~$25–30 / month / user |
| ChatGPT Business | Negotiated |
| ChatGPT Enterprise | Negotiated (custom) |
| ChatGPT Edu | Educational pricing |
| ChatGPT for Healthcare | Custom (BAA-required) |

For most "build an agent" use cases relevant to this rubric, the API
pricing is what applies. ChatGPT Enterprise is for end-user-facing
chat deployments rather than custom-built agents.

## SLA

**API platform SLA:**
- Standard API has best-effort availability; specific SLA commitments
  depend on commercial tier.
- Enterprise customers can negotiate availability SLAs with credits.
- Public status page at status.openai.com with detailed incident
  history.

**ChatGPT Enterprise SLA:**
- Negotiated per contract.
- Includes priority support and named account team.

## Budget controls

OpenAI provides several **token / cost runaway controls** for the
buyer:

- **Org-level monthly spend cap** — set in the dashboard; hard stop
  when reached.
- **Project-level budget limits** — segment spend by use case.
- **Per-request `max_output_tokens`** — caps output per call.
- **Agents SDK `max_turns`** — caps turns per agent run (default 10).
- **Tier rate limits** — TPM and RPM ceilings per model and tier.
- **Usage alerts** — email/webhook when approaching budget.

This is **more comprehensive cost-runaway tooling than LangGraph**
(which only offers `recursion_limit`) and operates at a different
layer than Sierra (which uses outcome-based pricing).

For a procurement buyer evaluating runaway risk on a token-pricing
vendor: OpenAI offers explicit per-org, per-project, per-request,
and per-agent-run caps. Buyer must set them.

## DPA and contract terms

- Standard DPA available via DocuSign self-serve.
- SCCs for EU/UK transfers.
- BAA for HIPAA-covered workloads (on appropriate plans).
- Sub-processor notification policy with subscription.
- Zero data retention available on the API platform for sensitive
  workloads.

## Model change policy

OpenAI provides **dated model snapshots** (e.g. `gpt-5-2025-08-13`)
that customers can pin to for stability. Rolling aliases (`gpt-5.5`)
auto-upgrade to the latest within that family.

When OpenAI deprecates a snapshot, they publish a deprecation
schedule with advance notice. Recent deprecation cycles have been
12+ months.

## Procurement-relevant questions to ask

1. **Org-level monthly spend cap** — set this BEFORE any agent goes
   to production. It is the single most important budget control.
2. **Zero data retention** — does your workload qualify, and what
   features (schema caching, audit logs) does it disable?
3. **Model snapshot strategy** — will you pin or roll? Pinning gives
   stability at the cost of staying behind on capability.
4. **Tier negotiation** — at sufficient volume, custom pricing and
   capacity guarantees become available.
5. **Sub-processor list** — get the current snapshot in your security
   review.
