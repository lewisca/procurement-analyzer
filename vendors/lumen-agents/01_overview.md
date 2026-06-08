# Lumen Agents — Product Overview

## What we do

Lumen Agents is an agentic AI platform for **customer support automation**.
Our agents handle Tier-1 support tickets end-to-end: ticket triage,
information lookup, refund processing, account modification, and
escalation. We're production-deployed at 47 mid-market and enterprise
customers (as of Q1 2026), processing ~2.1M agent runs per month.

## What we do not do

- We do **not** make creative, judgment-heavy decisions (e.g. legal
  advice, medical triage, hiring decisions).
- We do **not** operate without a buyer-defined tool allowlist.
- We do **not** take destructive actions (refunds > $X, account deletion,
  data export) without an explicit human approval gate.

## Agent loop

Our agent loop is a bounded ReAct variant:

1. **Plan** — Given a ticket and the buyer's tool allowlist, the agent
   produces a 1–8 step plan with predicted tool calls.
2. **Validate plan** — Static checker rejects plans that include
   disallowed tools, exceed step limits, or skip required approval gates.
3. **Execute step** — For each step the agent: (a) restates known facts,
   (b) selects a tool, (c) validates parameters against typed schema,
   (d) executes (or dry-runs), (e) checkpoints state.
4. **Consistency check** — Each step's outputs are compared against the
   state checkpoint; contradictions trigger a replan or escalation.
5. **Terminate** — On success, error budget, step budget, cost budget,
   loop detection, or contradiction-irresolvable signal.

## Model policy

- Default model: Claude Sonnet 4.6 via the Anthropic API.
- Buyer-configurable per use case.
- **30-day notice** before any default-model change, with side-by-side
  eval results published on our status page.

## Customers and maturity

- 47 production customers (range: Series A SaaS to Fortune 500 retail).
- Series B, $42M raised, 38 employees.
- SOC 2 Type II since 2024-09; ISO 27001 in progress (audit Q3 2026).
- Status page: status.lumenagents.com (99.95% trailing 90-day uptime).

## Target use cases

| Use case                    | Avg. agent run  | Tool calls / run | Step ceiling |
|-----------------------------|----------------|------------------|--------------|
| Order status lookup         | 1.4 steps      | 2                | 5            |
| Refund (under $100)         | 3.2 steps      | 4                | 8            |
| Refund (over $100)          | 4.8 steps      | 5 + approval     | 12           |
| Account modification        | 5.1 steps      | 6 + approval     | 15           |
| Escalation hand-off         | 2.3 steps      | 3                | 5            |

All ceilings are configurable per use case but enforced at runtime.

## Long-horizon strategy

For workflows >5 steps we use **stateful checkpointing** (see
`05_security_privacy.md` for retention) plus **rolling summary memory**.
The agent's "facts known" state is explicit JSON, not implicit in the
context window. See `03_sample_trace.json` for a 7-step trace.
