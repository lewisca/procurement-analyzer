# Lumen Agents — Pricing, SLAs & Contract Terms

## Pricing tiers

| Tier        | Pricing model               | Step budget cap | Cost cap / run | SSO | Audit log retention |
|-------------|----------------------------|------------------|----------------|-----|---------------------|
| Starter     | $0.04 / agent run + tokens | 10 steps         | $0.10          | —   | 30 days             |
| Pro         | $0.025 / run + tokens      | 25 steps (configurable) | $1.00 (configurable) | SAML/OIDC | 365 days |
| Enterprise  | Annual contract            | Custom           | Custom         | SAML/OIDC + custom IdP | 365d online / 7y cold |

Step, token, and cost caps are buyer-configurable within tier ceilings.
Real-time spend dashboards are included on all tiers.

## Budgets & alerts

- **Token budget per run:** default 20K, configurable. Alerts at 80%.
  Hard stop at 100%.
- **Cost cap per run:** see table above. Alerts at 80% by default
  (configurable). Hard stop at 100%.
- **Tenant-wide monthly cap:** Available on Pro and Enterprise.
- **Step limit:** see table. Enforced at runtime — agent cannot
  request a step extension.
- **Alerts:** Email, webhook, PagerDuty, and Slack.

## Service-level agreement

| Metric              | Pro                  | Enterprise           |
|---------------------|----------------------|----------------------|
| Uptime              | 99.9% monthly        | 99.95% monthly       |
| Response time p95   | < 8 s                | < 5 s (with regional shard) |
| Support response    | Business hours, 8h   | 24/7, 30 min for P1  |
| Incident notification | <24h               | <2h for P1 / <24h for others |
| Credits             | 10% per 0.1% miss   | 25% per 0.1% miss    |

Status page: status.lumenagents.com. 99.95% trailing-90-day uptime as
of 2026-04-30.

## Contractual terms (standard MSA, buyer-friendly defaults)

- **DPA:** Standard DPA available pre-signature; supports SCCs.
- **IP indemnification:** Lumen indemnifies for IP-infringement claims
  arising from our agent outputs (with standard exclusions for buyer
  misuse).
- **Output liability:** Mutual liability cap = annual fees paid.
  Carve-outs for confidentiality, IP, gross negligence.
- **Sub-processors:** Listed publicly; 30 days' advance notice on
  changes; buyer right to object.
- **Model-change notice:** 30 days' advance notice on any default-model
  change; buyer can pin to N-1 for the notice period; we publish
  side-by-side eval results before any rollout.
- **Data export:** Available at any time during contract. On exit,
  buyer has 90 days to export traces, logs, and configurations.
  Deletion verification certificate provided.
- **Account closure:** Self-serve via admin console; data deleted
  within 30 days; export window guaranteed.
- **Termination for convenience:** 30 days' notice on Pro; per
  Enterprise contract.
- **Audit rights:** Buyer may audit (or have an auditor audit) Lumen's
  controls once per year, with 30 days' notice. SOC 2 report
  ordinarily satisfies this.

## Custom contracts

Anything in this document can be negotiated on Enterprise. Notable
items frequently customized: data residency, retention, BYOK, custom
RBAC roles, single-tenant deployment, named-incident notification SLAs.
