# Sierra — Security, Privacy, and Compliance

_Sourced from trust.sierra.ai (referenced; the page itself is
SafeBase-rendered and gates its content behind a CTA, but the
high-level posture is published across sierra.ai's product pages and
in their public statements)._

## Certifications held

Sierra publicly cites the following certifications:

| Standard         | Status      | Source |
|------------------|-------------|--------|
| SOC 2 Type II    | ✅ Held     | sierra.ai trust page; cited in multiple third-party sources |
| ISO 27001        | ✅ Held     | sierra.ai trust page |
| **ISO 42001**    | ✅ Held     | sierra.ai trust page — this is the AI management system standard, notable because few agent platforms have it |
| HIPAA            | ✅ Compliant | sierra.ai trust page; BAA available |
| GDPR             | ✅ Compliant | sierra.ai trust page |
| PCI DSS          | ✅ Compliant for payment flow | "dedicated PCI-certified infrastructure" |
| CCPA             | ✅ Compliant | sierra.ai trust page |
| CSA STAR         | ✅ Cited    | sierra.ai trust page |

**ISO 42001 is the notable one** — it's the AI management system
standard published in late 2023 and uncommonly held by agent vendors
in 2026. Sierra holding it is a real differentiator from peers.

The SOC 2 report itself, the ISO certificates, and the full
penetration-test history are gated behind the SafeBase trust portal
and require a Sierra account or NDA for access.

## Data handling

**Customer data isolation:**

> "Customer data is only used as instructed and is never shared with
> other customers." — sierra.ai

**Training-data policy:**

> "Sierra does not use customer data to train shared models." —
> documented across Sierra trust material.

This is the single most important commitment for an enterprise buyer
in 2026 and Sierra states it explicitly.

**PII handling:**

> "Personally identifiable information (PII) shared with the agent is
> automatically encrypted and masked."

PII masking applies in logs, traces, and the analytics layer.

**Payment data architectural isolation:**

> "Sensitive payment data flows through dedicated PCI-certified
> infrastructure and never touches Sierra's core platform, LLMs, or
> persistent storage."

This is unusual and strong — the LLM context never sees payment
information. Removes the LLM as a class-of-vulnerability for card
data.

**Off-policy content filtering:**

> "Built-in filters and monitors for topics and keywords that are
> off-limits based on your company policies."

## Regional data residency

Sierra runs managed cloud deployments in:

- **US region** (default)
- **EU region** (available on enterprise plans)

EU residency is essential for GDPR-affected European customers.

## Encryption

- **In transit:** TLS (standard, not specifically called out as 1.2
  or 1.3 in public material — confirm under NDA).
- **At rest:** Encrypted (standard claim, key management details
  not in public material).
- **PII in storage:** Encrypted and masked per the above.

## Access controls

Sierra's public material doesn't enumerate SSO / RBAC tier
availability the way LangSmith's pricing page does. Customer reviews
and third-party guides indicate:

- **SSO:** Available, presumed enterprise tier (standard for $150K+
  contracts).
- **RBAC:** Not publicly detailed; confirm with Sierra.
- **MFA:** Standard offering.

## Audit logging

Sierra's Insights 2.0 product provides per-interaction trace and
analytics. Whether tenant-level admin audit logs (e.g. who changed
which policy, who approved which deployment) are separately available
is not documented publicly. Procurement should ask: *what does the
admin audit log look like, what's its retention, and can it be
exported to a customer SIEM?*

## Sub-processors

Sierra does not publish a public sub-processor list. Customers can
request the current list during procurement. Given Sierra's
constellation-of-models architecture, sub-processors will include
multiple LLM providers (OpenAI, Anthropic, Google likely) plus cloud
infrastructure providers — buyer should request the full list.

## Incident response

Sierra has an internal incident response process but does not run a
public status page (in contrast to many enterprise SaaS vendors who
publish status.<vendor>.com). Customer notification SLAs are
contract-defined.

## Procurement-relevant questions to ask

These are the gaps in public material that procurement should close:

1. **SOC 2 report under NDA** — confirm scope and any exceptions.
2. **ISO 42001 scope statement** — what's actually in the AI
   management system's scope?
3. **Full sub-processor list** with notification policy on changes.
4. **Admin audit log capabilities** — schema, retention, SIEM export.
5. **Incident notification SLA** — specific hours to customer
   notification.
6. **Data-deletion verification** — how do you prove buyer data is
   gone after off-boarding?
7. **Encryption-in-transit version pinning** (TLS 1.2 vs 1.3).
8. **Key management** — BYOK supported? At which tier?

## Summary

Sierra's security posture is **enterprise-grade and well-certified**.
The combination of SOC 2 + ISO 27001 + ISO 42001 + HIPAA + GDPR + PCI
is what a Fortune 50 procurement leader expects to see — and it's
unusual to find all of them, especially ISO 42001, in an
agent-platform vendor at any stage.

The gaps are details (audit log schema, key management, sub-processor
list) that are normal to negotiate during contract review, not
deal-breakers.
