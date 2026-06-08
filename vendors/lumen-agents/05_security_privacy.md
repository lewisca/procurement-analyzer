# Lumen Agents — Security, Privacy & Audit

## Certifications

| Standard         | Status           | Auditor     | Last report  |
|------------------|------------------|-------------|--------------|
| SOC 2 Type II    | Active           | Schellman   | 2025-09-30   |
| ISO 27001        | In progress      | Schellman   | Target Q3 2026 |
| GDPR / UK GDPR   | Compliant; DPA available | — | — |
| CCPA             | Compliant        | —           | —            |
| HIPAA            | BAA available on Enterprise tier | — | — |

Trust center: trust.lumenagents.com (all reports gated by NDA).

## Data handling

- **Encryption in transit:** TLS 1.3 minimum.
- **Encryption at rest:** AES-256-GCM, customer-managed keys (BYOK)
  available on Enterprise tier.
- **Data residency:** US (default), EU (Frankfurt), UK (London),
  Australia (Sydney). Selected per-tenant at provisioning.
- **Training use:** Buyer data is **never** used to train Lumen's
  models or any third-party model. This is contractual, not just a
  policy statement; see Section 4 of the standard DPA.
- **Retention defaults:**
  - Agent traces: 365 days (buyer-configurable down to 30).
  - Tool-call logs: 365 days.
  - Buyer-uploaded KB content: retained until buyer deletes.
- **Deletion:** Buyer-triggered deletion completes within 30 days
  (immediate from primary; up to 30 days for backups). Verification
  certificate provided on request.
- **Data subject requests:** Self-serve in admin console; SLA: 14 days.

## Access control

- **SSO:** SAML 2.0 and OIDC on Pro and Enterprise tiers.
- **MFA:** Required for all admin accounts; configurable for end users.
- **RBAC:** Five built-in roles (Owner, Admin, Auditor, Operator,
  Viewer); custom roles on Enterprise.
- **Least privilege defaults:** New users are Viewer; explicit
  promotion required.
- **Admin action audit log:** All admin actions (config changes, user
  changes, key rotations, data exports) logged immutably. Exportable to
  buyer SIEM via SCIM-compatible endpoint.
- **Session management:** 12-hour default; configurable. Sessions
  invalidated on password change, MFA reset, or role downgrade.

## Audit logs (agent execution)

- **Per-run trace** — full reasoning chain, tool calls (inputs, outputs),
  per-step token / cost / time, contradictions, loop signals,
  approvals. See `03_sample_trace.json` for the schema.
- **Format:** Structured JSON; also queryable in admin console.
- **Immutability:** Logs are append-only; signed with a per-tenant key
  so tampering is detectable.
- **Buyer export:** REST API and webhooks; CSV / JSON / NDJSON. Logs can
  also be streamed to S3, GCS, or Splunk.
- **Retention:** 365 days online; 7 years cold storage available
  (Enterprise tier).

## Network security

- **Tenant isolation:** Logical isolation at the application and
  database layers. Single-tenant deployments available on Enterprise.
- **Egress:** Agent tool calls are scoped to the buyer's tool allowlist;
  outbound network egress goes through a tenant-specific egress proxy.
- **Penetration testing:** Annual third-party pentest (NCC Group);
  summary report available under NDA.
- **Vulnerability disclosure:** security@lumenagents.com; 90-day
  coordinated disclosure; bug bounty via HackerOne (active since 2024).

## Incident response

- **24/7 on-call:** Rotation across SRE and security teams.
- **Notification SLAs:** Customer notification within 24h of confirmed
  incident affecting their data; preliminary RCA within 5 business days;
  full RCA within 30 days.
- **Public status page:** status.lumenagents.com.
- **History:** Quarterly reliability reports published; most recent
  major incident was 2025-08-14 (CRM-integration outage; 47 min
  partial degradation; no data exposure).

## Sub-processors

Listed publicly at lumenagents.com/subprocessors. We provide 30 days'
advance notice of any new sub-processor. Current list (as of
2026-03-31): AWS, Anthropic, OpenAI (optional model only), Stripe
(billing), Snowflake (analytics), Sumo Logic (logging).

## Contractual terms

Standard DPA, MSA, and SCCs available pre-signature. Buyer-friendly
defaults: see `07_pricing_sla.md` for indemnification, exit, and
model-change notice terms.
