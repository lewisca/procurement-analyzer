# Anthropic — Security, Privacy, and Compliance

_Sourced from trust.anthropic.com (gated portal), privacy.claude.com,
anthropic.com/legal/, and third-party compliance summaries
(trustlists.org, claudeimplementation.com)._

## Certifications

| Standard | Status |
|----------|--------|
| SOC 2 Type II | ✅ Active |
| SOC 2 Type I | ✅ |
| ISO 27001:2022 | ✅ Certified (Information Security Management) |
| **ISO/IEC 42001:2023** | ✅ Certified (AI Management Systems — unusually held) |
| HIPAA | ✅ HIPAA-ready configuration; BAA available |
| GDPR | ✅ Compliant; DPA available |
| CCPA | ✅ Compliant |

Reports are gated behind trust.anthropic.com (NDA-protected
SafeBase portal).

ISO 42001 is the AI-specific management system standard. Anthropic
holds it; OpenAI also holds it; LangChain (for LangSmith) also holds
it. Sierra also claims it. **Among the four enterprise vendors in
this comparison, all hold ISO 42001 — a reasonable bar for an
agentic AI vendor in 2026.**

## Important shared-responsibility caveat

From the third-party Anthropic implementation guide:

> "It's important to note that Anthropic holds SOC 2 Type II and ISO
> 27001 certifications — but their scope covers Anthropic's
> infrastructure, not your application. When you build an application
> on the Claude API, your application layer, your data pipelines,
> your user authentication, your logging infrastructure, and your
> output validation controls are all outside the scope of Anthropic's
> certifications."

This is the **shared responsibility model** familiar from cloud
security. Buyer's procurement should not assume Anthropic's
certifications cover an application built on top — the developer's
own controls need their own audit.

## Data handling

### Training-data policy (CRITICAL)

Anthropic's policy is clear: **API customer data is not used to train
Claude models by default.** This is contractually backed for
enterprise plans and documented in the privacy policy.

Opt-in flows for data usage in research are explicit and time-limited.

### Encryption

- **In transit:** TLS (specific minimum version not in public docs;
  confirm via trust portal).
- **At rest:** Encrypted.
- **For ZDR-eligible workloads:** Zero data retention available on
  certain enterprise plans.

### Retention

Default API conversation retention is 30 days. Customers can opt into
zero-retention for sensitive workloads on appropriate plans.

### Regional data residency

- **Direct Anthropic API:** US-based by default.
- **Amazon Bedrock:** Regional residency follows AWS regions (US, EU,
  AP).
- **Google Vertex AI:** Regional residency follows GCP regions.
- **Microsoft Azure AI Foundry:** Regional residency follows Azure
  regions (including dedicated US gov clouds).

Multi-cloud distribution gives **better regional residency options**
than OpenAI's primarily-Azure path. EU customers in particular have
more sourcing flexibility.

## Access controls

- **SSO / SAML** available on enterprise plans
- **SCIM provisioning** on enterprise
- **API key scoping** by workspace
- **Audit logs** for admin actions on enterprise plans
- **MFA** standard

## Sub-processors

Anthropic publishes a sub-processor list on the trust portal.
Major sub-processors typically include:

- Amazon Web Services (infrastructure)
- Google Cloud (some workloads)
- Various email, support, and analytics tooling

Notification policy: advance notice of new sub-processors;
customers can subscribe to updates.

## Pentest and bug bounty

- Annual third-party penetration testing (documented in SOC 2 scope).
- Public bug bounty program at anthropic.com/security (HackerOne).
- Vulnerability disclosure policy is public.

## Incident response

- 24/7 incident response team.
- Status page at status.anthropic.com with public incident history.
- Customer notification SLAs are contract-defined.

## Contractual terms

- **Standard DPA** available via Anthropic legal team.
- **Standard Contractual Clauses (SCCs)** for EU/UK transfers.
- **BAA** for HIPAA-covered entities on appropriate plans.
- **Mutual indemnification** for IP claims (standard for enterprise
  tier).
- **Model deprecation policy** with public schedule; recent cycles
  have been 6+ months notice.

## Zero data retention (ZDR)

Available on enterprise plans for sensitive workloads. Tradeoff:

- Conversation persistence disabled (no Sessions resume across days)
- Some safety / monitoring features limited

## What procurement should verify under NDA

1. **SOC 2 Type II report** — scope and exceptions.
2. **ISO 42001 scope statement** — what's covered under the AI
   management system.
3. **Sub-processor list** — current snapshot.
4. **Multi-cloud option pricing and terms** — Bedrock vs Vertex vs
   Azure vs direct.
5. **ZDR availability and trade-offs** for your specific workload.
6. **BAA scope** for HIPAA workloads.
7. **Audit log export** — schema, retention, SIEM format.

## Summary

Anthropic's security posture is **comparable in depth to OpenAI's**
with two notable advantages:

1. **Multi-cloud distribution** — buyers can run Claude via Bedrock,
   Vertex, or Azure Foundry, giving better regional residency and
   sourcing leverage.
2. **Tighter default training-data policy** — the no-training default
   is firmer than some peers in 2026.

The principal **gaps** vs an ideal posture:

- The trust portal is gated (you can't browse policies without
  credentials).
- Specific encryption-version pinning and audit-log schema are not
  publicly documented (require NDA).
