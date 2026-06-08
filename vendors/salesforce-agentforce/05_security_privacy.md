# Salesforce — Security, Privacy, and Compliance

_Salesforce has one of the broadest enterprise compliance portfolios
in the SaaS industry, accumulated over 25+ years of selling to
financial services, healthcare, and government. Agentforce inherits
that posture._

_Sourced from compliance.salesforce.com (the Salesforce Compliance
Site), the Einstein Trust Layer documentation, and third-party
compliance summaries._

## Certifications

This is Salesforce's distinguishing strength. The certification
portfolio is broader than any other vendor in the comparison:

| Standard | Status |
|----------|--------|
| SOC 2 Type II | ✅ Active |
| SOC 1 Type II | ✅ Active |
| ISO 27001 | ✅ Certified |
| ISO 27018 | ✅ Certified (cloud privacy) |
| PCI-DSS | ✅ Compliant |
| HIPAA | ✅ BAA available |
| **FedRAMP** | ✅ **Authorized** (Government Cloud Plus) |
| GDPR | ✅ Compliant; DPA available |
| CCPA | ✅ Compliant |
| **DoD IL4 / IL5** | ✅ Available on Government Cloud |

**FedRAMP authorization is the differentiator.** None of OpenAI,
Anthropic, Sierra, or LangGraph have a comparable federal authority.
For US federal government, state/local agencies on FedRAMP-aligned
procurement, or any contractor needing FedRAMP-flow-down, Salesforce
is often the only viable AI-agent vendor.

Documents are available at compliance.salesforce.com:

- SOC 2 Type II reports (multiple, per service)
- ISO certificates
- FedRAMP Security Package (requires .gov / .mil email or partner
  request)
- DPA template
- Sub-processor list

## Einstein Trust Layer (the security architecture)

The Trust Layer is **structurally stronger than peer offerings**
because Salesforce designed it specifically for the regulated /
enterprise use case:

### PII masking

> "PII shared with the agent is automatically encrypted and masked"

Specifically: PII is **masked BEFORE the prompt reaches the LLM** and
**unmasked when the response returns to the user**. The LLM never
sees the raw PII. This is a structurally stronger position than
"the LLM provider promises not to log."

### Zero data retention (ZDR) with LLM providers

> "Einstein Trust Layer sits across all of this, enforcing zero data
> retention with third-party LLM providers"

Salesforce has contractual ZDR with OpenAI, Anthropic, and the other
foundation-model partners. The LLM provider never persists customer
data even temporarily.

This is **uniquely strong**: most buyers using OpenAI or Anthropic
directly have to negotiate ZDR themselves and accept feature
trade-offs. Salesforce has done this negotiation at scale, on the
buyer's behalf.

### Toxicity detection + prompt-injection defense

Output classifier + input classifier. Configurable guardrails for
regulated use cases.

### Configurable per-tenant rules

Each Salesforce customer can configure their own:

- PII detection rules
- Toxicity thresholds
- Topic-level audit requirements
- Approval gates per Action

## Data Cloud architecture

The "Zero-Copy" architecture is Salesforce's data philosophy:

> "Data is retrieved, never duplicated — maintaining security via the
> Einstein Trust Layer"

When the agent needs customer data, it queries the source system
(e.g., the customer's Snowflake / BigQuery / Databricks) at query
time, not from a Salesforce-copied snapshot. This means:

- No duplicate copies of sensitive data in Salesforce-managed storage
- Customer data lifecycle controlled by source system
- Deletion in source system propagates immediately

## Regional data residency

Available regions:

- **US** (multiple regions including Government Cloud Plus)
- **EU** (multiple regions for GDPR)
- **UK** (post-Brexit residency)
- **Australia**
- **Japan**
- **Canada**
- **DoD-specific clouds**

This is the broadest residency footprint of any vendor in this
comparison.

## Access controls

Salesforce inherits the Salesforce Platform's mature access
controls:

- **SSO / SAML** standard
- **SCIM provisioning**
- **MFA** standard
- **Role-based access** with Salesforce's well-developed
  Profiles + Permission Sets model
- **Field-level security** — granular PII access controls
- **Audit logs** (Event Monitoring add-on for detailed audit)

## Sub-processors

Public sub-processor list at compliance.salesforce.com.

Notable: OpenAI and Anthropic appear as sub-processors for
LLM-backed Agentforce features. The contractual ZDR posture
prevents either from retaining data.

## Incident response

- 24/7 incident response
- Public status page at status.salesforce.com (industry-standard,
  long history)
- Customer notification SLAs are tier-dependent

## Bug bounty and pentest

- Public bug bounty program at trust.salesforce.com
- Annual third-party pentest documented in SOC 2 scope
- Vulnerability disclosure policy is mature

## Contractual terms

- **Standard DPA** available via legal
- **SCCs** for EU/UK transfers
- **BAA** for HIPAA workloads
- **MSA** with significant negotiation room at enterprise scale
- **Multi-year discounts** of 20-40% available for 3-year commits
  with volume guarantees

## Procurement-relevant strengths and gaps

**Strengths:**

1. FedRAMP authorization — unique among AI-agent vendors
2. ZDR with LLM providers contractually enforced
3. PII masking pre-LLM (the LLM never sees raw PII)
4. Field-level security inheritable from Salesforce Platform
5. Broadest regional residency footprint
6. Most mature audit / compliance tooling

**Gaps:**

1. Salesforce Platform lock-in — leaving Salesforce means leaving
   Agentforce; data portability requires planning
2. Trust Layer audit-log granularity for AI-specific events is less
   publicly documented than the rest of Salesforce's audit story
3. Sub-processor changes (LLM provider swaps in Atlas's
   constellation) are abstracted from the buyer — visibility into
   when/why the underlying LLM changes is unclear

## Procurement questions to ask

1. Which Salesforce edition supports our use case (Unlimited may be
   required for full Trust Layer features)?
2. ZDR scope — does it cover everything in Atlas's constellation, or
   only certain models?
3. Government Cloud Plus pricing and feature parity with commercial
   if FedRAMP is needed
4. Event Monitoring license — needed for AI-specific audit detail?
5. Data Cloud licensing — required for Agentforce; ~$108K/year
   minimum (often a surprise line item)
