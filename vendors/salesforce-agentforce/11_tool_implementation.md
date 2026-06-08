# Salesforce Agentforce — Action Implementation Patterns

_Salesforce Actions (the Agentforce equivalent of "tools") are built
using Salesforce's existing developer primitives — Flow, Apex, and
external APIs. This document describes the patterns publicly. Real
implementations live in customer Salesforce orgs and Trailhead
modules accessible to logged-in users._

_Sources: Salesforce Agentforce documentation, Trailhead modules
(referenced), and the Atlas Reasoning Engine writeup._

## How Actions get defined

Actions in Agentforce map to one of five Salesforce primitives:

| Primitive | Built by | When to use |
|-----------|----------|-------------|
| **Flow** | Salesforce admin (declarative) | Standard CRUD operations, multi-step business processes |
| **Apex class** | Salesforce developer (code) | Complex logic, integration with external systems |
| **External API** | Integration developer | Calling out to non-Salesforce systems |
| **Slack / Email** | Standard Salesforce config | Communication actions |
| **MCP server** (Spring 2026) | Any MCP-compatible service | External tool integration via standardized protocol |

The pattern is **familiar to Salesforce-skilled teams** and unfamiliar
to teams without Salesforce admin / developer maturity.

## Conceptual Action structure

While exact schema details require Salesforce login, the public
material describes:

```yaml
# Conceptual Action (declarative representation)
action_name: process_refund_under_threshold
description: Issue a refund up to $200 against a customer order
action_type: apex   # could also be: flow, api, slack, email, mcp

# Input schema — typed parameters
inputs:
  order_id:
    type: string
    description: The order to refund
    required: true
  amount_cents:
    type: integer
    minimum: 0
    maximum: 20000
    description: Refund amount in cents
    required: true
  reason_code:
    type: enum
    values: [duplicate_charge, item_not_received, defective_item, customer_request]
    required: true

# Topic binding — which Topics can invoke this Action
topic_bindings:
  - process_refund
  - issue_customer_credit

# Permission requirements — which user profiles can trigger
permission_requirement: agentforce_refund_action_user

# Sandbox / production scoping
deployable_to: [sandbox, uat, production]

# Audit
audit_to_command_center: full
```

The actual implementation (the Apex class or Flow) is separate from
the metadata above — Agentforce binds to the implementation by name.

## Apex action implementation pattern

A typical Apex Action class for `process_refund_under_threshold` would
include:

```apex
// Conceptual Apex pattern - illustrative
public with sharing class ProcessRefundAction {
    @InvocableMethod(label='Process Refund Under Threshold')
    public static List<Result> execute(List<Request> requests) {
        List<Result> results = new List<Result>();
        for (Request req : requests) {
            // Application-layer validation (NOT framework-provided)
            Order__c order = [SELECT Id, Amount__c FROM Order__c
                              WHERE Order_Id__c = :req.order_id LIMIT 1];
            if (order == null) {
                results.add(new Result('order_not_found'));
                continue;
            }
            if (req.amount_cents > order.Amount__c * 100) {
                results.add(new Result('refund_exceeds_order'));
                continue;
            }

            // Side effect: issue the refund (idempotency, audit, etc.
            // handled here in the developer's Apex code)
            String refundId = RefundService.issue(order, req);
            results.add(new Result('settled', refundId));
        }
        return results;
    }
    // ... Request / Result inner classes
}
```

**Note: developer responsibility for:**
- Foreign-key existence (Salesforce SOQL already does this, but
  developer must write the query)
- Business-rule validation (refund amount ≤ order amount, etc.)
- Idempotency (Salesforce DML naturally handles some cases; developer
  must add idempotency keys for stronger guarantees)

## What Salesforce + Trust Layer enforces vs developer

| Concern | Enforced by Salesforce | Developer responsibility |
|---------|------------------------|---------------------------|
| Schema validity (typed args) | ✅ Flow / Apex parameter types | — |
| Topic-action binding | ✅ Topic metadata | — |
| PII masking before LLM | ✅ Trust Layer | — |
| Toxicity / prompt injection | ✅ Trust Layer | — |
| Output hallucination detection | ✅ Trust Layer | — |
| Foreign-key existence | Partial (SOQL) | Developer writes the query |
| Business rules | ❌ | Developer / admin (in Apex or Flow) |
| Idempotency | ❌ | Developer (in Apex) |
| Audit log to Command Center | ✅ Automatic | — |

## Comparison to peer SDK tool patterns

| Vendor | Tool definition |
|--------|----------------|
| Anthropic Agent SDK | Python decorator `@function_tool` + JSON Schema |
| OpenAI Agents SDK | Python decorator `@function_tool` + JSON Schema |
| LangGraph | Python `@tool` decorator + Pydantic schema |
| Sierra | Composable "skills" via Sierra Agent SDK (closed) |
| **Agentforce** | **Salesforce metadata + Flow / Apex / API binding** |

The pattern is structurally different:

- **SDK vendors**: tool definition IS the implementation; tightly
  coupled
- **Agentforce**: tool definition (Action metadata) is SEPARATE from
  the implementation (Apex / Flow); admin-managed binding

This separation has trade-offs:

- **Pro for Agentforce**: admins can rebind an Action to a different
  implementation without code changes; mature change-management
- **Con for Agentforce**: requires Salesforce admin maturity;
  iteration is slower

## What is NOT publicly visible

- Specific Action schema reference (gated to Salesforce customers)
- Topic metadata format examples (gated to Trailhead users)
- Trust Layer internal classifier weights / thresholds
- Constellation router decision logic

## Procurement-relevant questions

1. **Request a real Topic + Action configuration example** under NDA
   — what does a production agent's metadata look like?
2. **Action authoring**: which of our use cases are achievable in
   Flow vs require Apex development?
3. **Action lifecycle**: how is change management handled between
   sandbox and production? Typical timeline for an Action change?
4. **MCP server support**: which auth models are supported; can we
   connect external tools without exposing internal credentials to
   Salesforce-managed infrastructure?
5. **Performance**: per-Action latency budgets in Agentforce
   conversations?
