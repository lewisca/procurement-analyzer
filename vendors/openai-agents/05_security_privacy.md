# OpenAI — Security, Privacy, and Compliance

_Sourced from trust.openai.com (SafeBase trust portal),
openai.com/enterprise-privacy/, openai.com/security-and-privacy/,
openai.com/business-data/, and the OpenAI Help Center compliance
articles._

## Certifications

| Standard | Status | Scope |
|----------|--------|-------|
| SOC 2 Type 2 | ✅ Active | API Platform, ChatGPT Enterprise, ChatGPT Edu, ChatGPT Team. Most recent report: 2025-01-01 → 2025-06-30. |
| ISO 27001 | ✅ Certified | Information security management |
| ISO 27017 | ✅ Certified | Cloud security |
| ISO 27018 | ✅ Certified | Cloud privacy |
| ISO 27701 | ✅ Certified | Privacy information management |
| **ISO 42001** | ✅ Certified | AI management system — the AI-specific standard published in late 2023 |
| HIPAA | ✅ Compliant (with BAA) | ChatGPT for Healthcare and API on appropriate plans |
| GDPR | ✅ Compliant | DPA executable via DocuSign or sales |
| CCPA | ✅ Compliant | Standard for US enterprise |

The SOC 2 Type 2 report covers the four trust criteria: **Security,
Availability, Confidentiality, and Privacy.** This is broader than
the typical Security-only SOC 2.

Reports and certificates are available on the OpenAI Trust Portal at
trust.openai.com (requires NDA / authenticated access).

## Data handling

### Training-data policy (THE KEY ENTERPRISE QUESTION)

> "Organization data remains confidential, secure, and entirely owned
> by the customer across ChatGPT Enterprise, ChatGPT Business, ChatGPT
> Edu, ChatGPT for Healthcare, ChatGPT for Teachers, and the API
> platform. By default, OpenAI does not use data from these services
> for training or improving models."

This is explicit and contractually backed. For consumer ChatGPT
products, the default is different — but the enterprise / API surface
is clear.

### Encryption

- **In transit:** TLS (specific minimum version not published; confirm
  via trust portal).
- **At rest:** Encrypted (standard claim).
- **Cached schemas note:** "Cached schemas don't qualify for zero data
  retention" — buyers under zero-retention contracts should confirm
  caching implications with their account team.

### Retention

Default API retention is 30 days (subject to zero-data-retention
agreements available on appropriate plans). For ChatGPT Enterprise,
retention is admin-configurable.

### Data residency

OpenAI does not currently offer a buyer-selectable regional cloud the
way Sierra does (US/EU). US deployment is default. EU customers
typically rely on the DPA + SCCs for cross-border transfer. For
strict EU residency, Azure OpenAI Service (run by Microsoft on Azure
EU infrastructure) is the standard path.

## Access controls

- **SSO / SAML:** Available on ChatGPT Enterprise.
- **SCIM provisioning:** Available on ChatGPT Enterprise.
- **MFA:** Standard.
- **Role-based access:** Admin / Member / Owner roles in the workspace
  console.
- **Audit log:** Compliance API for ChatGPT Enterprise; raw export to
  customer SIEM.

## Sub-processors

OpenAI publishes a sub-processor list (accessible via the trust
portal). The list is updated when sub-processors change; customers
can subscribe to notifications.

Major sub-processors typically include:
- Microsoft Azure (infrastructure)
- Snowflake (analytics)
- Various payment, email, and support tooling

The full current list is on the trust portal; verify before signing.

## Bug bounty and pentest

OpenAI runs a public bug bounty program. Pentest cadence is
documented in the SOC 2 report scope. Recent penetration testing has
been performed by named third parties (e.g. ControlPlane published a
case study of red-teaming GPT-4o, Operator, o3-mini, and Deep Research
for OpenAI).

## Incident response

OpenAI maintains 24/7 incident response. Status page at
status.openai.com is public and well-maintained. Recent major
incidents have been transparently disclosed with post-mortems.

## Contracts and DPA

- **Standard DPA** available via DocuSign for self-serve sign.
- **Custom MSA** for Enterprise customers.
- **Standard Contractual Clauses (SCCs)** for EU/UK transfers.
- **BAA** for HIPAA-covered entities on appropriate plans.

## Zero data retention (ZDR)

For sensitive workloads, ZDR is available on the API platform — no
data persists after the response is delivered. Trade-off: schema
caching and some safety features are limited under ZDR.

## What procurement should verify under NDA

1. **SOC 2 Type 2 report** — current period scope and any exceptions.
2. **Sub-processor list** — current snapshot + notification policy.
3. **ZDR availability** for your workload — and what it disables.
4. **Compliance API** — audit log export schema, retention, and SIEM
   format.
5. **Regional residency requirements** — if EU, get specifics on
   Azure OpenAI path.
6. **BAA scope** — what services it covers (not all OpenAI products
   are HIPAA-covered).

## Summary

OpenAI's compliance and security posture is **as deep as any
foundation-model vendor's**. SOC 2 Type 2 + ISO 27001 + ISO 27017 +
ISO 27018 + ISO 27701 + **ISO 42001** + HIPAA + GDPR is a complete
enterprise stack.

The training-data policy is contractually clear: enterprise / API
customer data does not train OpenAI's models by default.

The principal **gap** vs. Sierra is buyer-selectable regional
residency — for that, the recommended path is Azure OpenAI Service
rather than the direct OpenAI cloud.
