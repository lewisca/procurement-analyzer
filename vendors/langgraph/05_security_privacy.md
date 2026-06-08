# LangGraph / LangChain — Security, Privacy & Compliance

_LangGraph (the OSS library) runs entirely in the customer's
environment — there is no SaaS surface to evaluate. This document
covers the **LangSmith Platform** (the paid managed offering by
LangChain), which is what a buyer would be evaluating if they're
considering hosted observability, evaluation, and deployment._

_Sourced from the LangChain Trust Center (trust.langchain.com), the
LangSmith SOC 2 announcement (changelog.langchain.com, 2024-07-15),
the LangChain Privacy Policy (langchain.com/privacy-policy), and
public regions FAQ documentation._

## OSS vs. managed posture

| Surface | What's evaluated | Where data lives |
|---------|-------------------|-------------------|
| LangGraph (Python / TS library) | Code in your repo | Buyer's environment only |
| Self-hosted LangSmith | Application running in buyer's VPC | Buyer's environment only |
| LangSmith Cloud (US) | Managed SaaS | LangChain-managed, US-only |
| LangSmith Cloud (EU) | Managed SaaS, EU residency | LangChain-managed, EU |

If you're evaluating the **library**, security/privacy is mostly a
question about your own deployment posture, not LangChain's. If you're
evaluating the **managed platform**, everything below applies.

## Certifications

| Standard | Status | Notes |
|----------|--------|-------|
| SOC 2 Type II | ✅ Compliant since 2024-07-15 | "After a rigorous audit process, LangSmith has been certified to conform to industry best-practices for the protection of data and for security procedures." |
| GDPR | ✅ Compliant | Per LangChain changelog announcement |
| HIPAA | ✅ Compliant | Per support.langchain.com |
| ISO 27001 | Not announced | — |

The auditor was not named in the public announcement. Trust center
resources at trust.langchain.com/resources are available under NDA.

## Data handling

From the LangChain Privacy Policy:

- **Data collected.** Account information (email, password,
  registration details), payment info (third-party processed), usage
  data, device/online activity data, feedback and correspondence.
- **Training use.** The policy "does not explicitly state whether
  customer data is used to train models. It mentions creating
  'aggregated, de-identified, or other anonymous data' for 'research
  and development purposes' but does not specify AI model training."
  This is a gap worth flagging in contract review.
- **Retention.** No specific retention timeframes published. The
  policy notes retention is based on "the nature and sensitivity of
  such information, the potential risk of harm from unauthorized use
  or disclosure, the purposes for which we process it, and the
  applicable legal requirements."
- **Deletion.** Customers can submit Data Subject Access Requests via
  an online form. The policy notes: "we may not be able to fully
  comply with your request" due to legal retention obligations.

## Encryption

- **In transit:** TLS (standard for the SaaS).
- **At rest:** Not explicitly described in the public Privacy Policy.
  Caveat from the policy itself: "we cannot guarantee the security of
  personal information."
- **In LangGraph (OSS):** Optional via `EncryptedSerializer` for
  checkpoint encryption (AES, requires `LANGGRAPH_AES_KEY` env var).
  Off by default — buyer must opt in.

## Regional data residency

LangSmith offers **EU data residency** as a distinct cloud (announced
on the LangChain changelog). Per the regions FAQ, customers can
provision in either US or EU; data does not cross regions.

For HIPAA workloads, contact LangChain support to enable the HIPAA
posture (requires BAA execution).

## Access control

- **SSO:** Custom SSO is **Enterprise tier only** (per LangSmith
  pricing page). Plus and Developer tiers use email/password +
  password manager.
- **RBAC:** Custom RBAC is also Enterprise tier only.
- **MFA:** Not detailed on the public trust pages.

## Sub-processors

Per the Privacy Policy, sub-processors include "lawyers, bankers,
auditors, insurers, and providers that assist with hosting, analytics,
email delivery, marketing, and database management." A specific named
list (e.g. AWS, Stripe, Segment) was not present at fetch time;
contact support@langchain.dev for the current sub-processor list.

## Data Processing Addendum

- Pre-signed DPA available via DocuSign (per support.langchain.com).
- Standard Contractual Clauses are available for EU/UK customers.

## Audit logs (the managed platform)

LangSmith provides traces (the agent execution logs) and admin
actions to authenticated users in the platform UI. The depth and
queryability of admin audit logs at the **tenant** level (vs.
per-trace) is not publicly documented; contact sales for specifics.

## Buyer-side gaps to verify

If you are buying LangSmith (the managed offering), procurement
should ask for:

1. The **SOC 2 Type II report** under NDA — confirm scope and
   exceptions.
2. **Sub-processor list** as it stands today (not the privacy
   policy's category-level statement).
3. **Explicit training-use policy** — does buyer telemetry train any
   LangChain or partner model? Get this in writing in the DPA.
4. **Retention defaults and configurability** — what's the default,
   what's the floor, what's the ceiling, can it be changed
   contractually?
5. **Admin audit log export** — schema, retention, programmatic
   access.

These are standard enterprise questions that the public-facing trust
materials don't fully answer.
