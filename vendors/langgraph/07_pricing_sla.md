# LangGraph / LangSmith — Pricing and SLA

_LangGraph (the library) is open source, MIT-licensed, **$0**. The
pricing below covers the **LangSmith Platform** — the paid managed
offering for observability, evaluation, and deployment. Sourced from
langchain.com/pricing._

## Tiers

| Tier        | Price                       | Seats           | Base traces / month                |
|-------------|-----------------------------|-----------------|------------------------------------|
| Developer   | $0 / month (free)           | 1 seat          | 5,000 included, then pay-as-you-go |
| Plus        | $39 / seat / month          | Unlimited       | 10,000 included, then pay-as-you-go |
| Enterprise  | Custom                      | Custom          | Custom                              |

## Usage-based pricing (all tiers)

- **Base traces:** $2.50 per 1,000 (14-day retention)
- **Extended traces:** $5.00 per 1,000 (400-day retention)
- **Engine (LangGraph deployments):** $1.50 per LCU (LangChain
  Compute Unit)
- **Deployment runs (Plus, beyond included):** $0.005 per run
- **Deployment uptime:** $0.0036/minute (Production); $0.0007/minute
  (Development)
- **Sandboxes:** $0.0576/vCPU-hr; $0.0185/GiB-hr memory;
  $0.000123/GiB-hr storage

## What's in each tier

| Feature                            | Developer | Plus    | Enterprise           |
|------------------------------------|-----------|---------|----------------------|
| Seats                              | 1         | Unlimited at $39 ea | Unlimited |
| Workspaces                         | 1         | Up to 3 | Custom               |
| Fleet agents (managed runs)        | 1 × 50/mo | Unlimited × 500 included | Custom |
| Self-hosted / hybrid / VPC option  | —         | —       | ✅ "data doesn't leave your VPC" |
| Custom SSO + RBAC                  | —         | —       | ✅                   |
| Dedicated engineering support      | —         | —       | ✅                   |
| Architectural guidance / training  | —         | —       | ✅                   |
| Support                            | Community | Email   | Dedicated + SLA      |

## SLA

| Tier        | SLA                                                |
|-------------|---------------------------------------------------|
| Developer   | None                                              |
| Plus        | None published                                    |
| Enterprise  | "Dedicated engineering support and SLAs" — terms set per contract |

Public SLA numbers (uptime, response time) are not posted on the
pricing page. For non-Enterprise tiers, this is best-effort. For
Enterprise, the SLA is negotiated.

## Notable terms

- **DPA.** Pre-signed Data Processing Addendum available via DocuSign
  for self-serve customers; bespoke for Enterprise.
- **Model-change notice.** LangSmith does not run the model — buyer
  brings their own LLM provider — so model-change risk lives with the
  LLM vendor (OpenAI, Anthropic, etc.), not LangChain.
- **Self-hosted exit.** For Enterprise customers using self-hosted
  LangSmith, exit is straightforward — the deployment lives in the
  buyer's infrastructure already.
- **Trace export.** Traces are exportable in standard JSON via the
  LangSmith SDK and REST API.

## Budget controls

The OSS library exposes a `recursion_limit` (default 25) on every
graph invocation. There is **no built-in cost cap or token budget at
the LangGraph runtime level** — token and cost accounting are the
responsibility of the underlying LLM provider's SDK and any wrappers
the buyer adds. LangSmith billing is tracked per-trace, but does not
back-enforce per-execution caps.

This is a gap relative to mature managed agentic platforms that
expose both per-run cost caps and tenant-wide spend ceilings as
enforced runtime properties.

## Procurement-relevant questions to ask

- What's the **uptime SLA** on the Plus tier (if any) and the
  Enterprise tier (specific numbers)?
- Is the **base-trace usage cap** hard (auto-stop) or soft
  (overage-billed)? What alerts fire as the cap approaches?
- For Enterprise — what does the **DPA exception schedule** look
  like? Are sub-processors a closed list or can they expand without
  notice?
- For self-hosted Enterprise — what's the **support model** for
  upgrades / CVE patches?
