# Anthropic Claude — Pricing and SLA

_Sourced from anthropic.com/api/pricing/, code.claude.com pricing
notes, and platform.claude.com/docs/en/about-claude/models pricing
tables._

## Pricing model

**Token-based**, same as OpenAI. Buyer pays per input/output token
plus server-tool usage. Multi-cloud (Bedrock / Vertex / Azure) follows
respective cloud's billing.

## Per-million-token pricing (USD, mid-2026)

| Model | Input | Output | Notes |
|-------|------:|-------:|-------|
| Claude Opus 4.8 | $15 | $75 | Latest flagship |
| Claude Opus 4.7 | $15 | $75 | Premium reasoning |
| Claude Opus 4.6 | $15 | $75 | Available |
| Claude Sonnet 4.6 | $3 | $15 | Cost-balanced flagship |
| Claude Sonnet 4.5 | $3 | $15 | Available |
| Claude Haiku 4.5 | $1 | $5 | Cost-efficient |

**Tool-use system prompt** consumes additional tokens — these are
documented per-model in the tool use overview (e.g., Opus 4.8 with
tool_choice=auto adds 290 tokens; with any/tool, 410 tokens).

**Prompt caching** is available with up to 90% discount on cached
tokens.

**Batch API** provides 50% discount for asynchronous, non-realtime
workloads.

## Built-in tool pricing

Per the tool use docs:

- **Server-side tools** (web_search, code_execution, web_fetch,
  tool_search) incur **additional usage-based pricing**.
  - Example: web search charges per search performed
- **Client-side tools** (user-defined, bash, text_editor) — same as
  any other Claude API request, no extra fee
- **Tool-use system prompt overhead** counted per-call

## Multi-cloud pricing

Available on:

- **Direct Anthropic API** (anthropic.com)
- **Amazon Bedrock** (AWS native, follows AWS regional pricing)
- **Google Vertex AI** (GCP native)
- **Microsoft Azure AI Foundry** (Azure native)
- **Claude Platform on AWS** (newer, AWS-native deployment)

Buyers can negotiate enterprise contracts on any of these surfaces.
Multi-cloud gives **better procurement leverage** than single-source
vendors.

## Agent SDK credit (subscription plans)

Starting **June 15, 2026**: Agent SDK and `claude -p` usage on
subscription plans (Claude Pro, Team, Enterprise) draws from a
**separate monthly Agent SDK credit**, distinct from interactive
usage limits.

**Procurement implication:** Agent workloads have a separate budget
envelope from interactive Claude.ai usage. Buyers should request
Agent SDK credit allocations explicitly when contracting.

## SLA

**API platform SLA:**

- Standard API: best-effort availability with public status page at
  status.anthropic.com
- Enterprise contracts: negotiated availability SLAs with credits
- Multi-cloud customers benefit from the underlying cloud's SLA
  (AWS / GCP / Azure)

Specific uptime numbers are negotiated per contract; not posted
publicly.

**ChatGPT-equivalent (Claude.ai consumer):** No formal SLA.

## Buyer cost controls

OpenAI parallel: token-based pricing means runaway cost is the
buyer's problem. Available controls:

- **Org-level usage caps** in the Anthropic Console
- **Per-request max_tokens** caps output per call
- **Tool restriction** via `allowed_tools` / `disallowed_tools` —
  prevents agent from invoking expensive tools
- **Permission modes** including `plan` (dry-run only) for high-risk
  testing
- **Compaction** auto-summarizes context for long runs (reduces
  context cost growth)

Gap relative to ideal: no documented per-run cost cap primitive in
the SDK itself.

## Contractual terms

- **Standard DPA** available
- **SCCs** for EU/UK transfers
- **BAA** for HIPAA workloads on appropriate plans
- **Multi-cloud sourcing options** — material procurement leverage
- **Model deprecation**: public schedule with 6+ month notice on
  recent cycles. Deprecated models remain accessible during the
  notice period.
- **Mutual indemnification** for IP claims on enterprise

## Branding terms

Per Anthropic's docs:

> "For partners integrating the Claude Agent SDK, use of Claude
> branding is optional. When referencing Claude in your product:
> Allowed: 'Claude Agent' (preferred), 'Claude' (within an 'Agents'
> menu), '{YourAgentName} Powered by Claude' (if you have an existing
> agent name)."

Procurement implication: agent products built on Claude can be
unbranded as Claude — buyer's product keeps its own identity.

## Procurement-relevant questions to ask

1. **Which cloud** — Bedrock vs Vertex vs Azure Foundry vs direct?
   Pricing, residency, and SLA differ.
2. **Agent SDK credit** allocation if on a subscription plan vs
   API-direct.
3. **Prompt caching** — confirm rates and TTL.
4. **Org-level monthly spend cap** — set before going to production.
5. **Model deprecation schedule** for the model you pin to.
6. **Tool-use overhead** — confirm token cost for your typical
   tool_choice setting (auto vs any).
