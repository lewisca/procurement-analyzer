# Sierra — Skill Implementation Approach (Public Description)

_Sierra's Agent SDK source code is not public. This document
describes the skill-implementation pattern that Sierra publicly
documents at sierra.ai/product/develop-your-agent and on
sierra.ai/blog/meet-the-ai-agent-engineer._

## The role: Agent Engineer

Sierra has formalized a discipline they call **"Agent Engineer"** —
the customer-side or Sierra-side engineer responsible for designing,
composing, and operating agents on the platform. This is one of
Sierra's distinguishing positions: they treat agent development as a
specialized engineering practice with its own SDK, simulation tools,
and observability.

## Skills as the unit of composition

From Sierra's public documentation:

> "Compose AI agents by mixing and matching skills—like triage,
> respond, and confirm—into complex workflows that agents can execute
> for a specific use case."

Skills are:

- **Typed.** Inputs and outputs are typed; the LLM selects skills
  and provides typed args, not raw API calls.
- **Composable.** Skills stack into workflows. Customers don't write
  monolithic agent code.
- **Policy-bound.** Each skill carries policy metadata that the
  validator agent enforces.
- **Deterministic in execution.** The skill's underlying API call is
  pre-defined and reviewed; the LLM cannot alter the call shape.

## What a skill typically contains (inferred from public material)

Sierra has not published a skill schema reference. The pattern,
inferred from the public Agent SDK page, is approximately:

```
Skill: update_subscription
├── name: human-readable identifier
├── description: when the agent should select this skill
├── inputs: typed parameters with allowed values
├── policy_bindings: rules the validator agent evaluates
├── underlying_action: deterministic API call (CRM endpoint)
├── side_effects: classification (read-only, write, destructive)
├── escalation_triggers: conditions that route to Live Assist
└── observability_tags: how this skill shows up in Insights traces
```

This is the **buyer's contract surface**: the agent's behavior is
constrained to the skills the customer enables and configures.

## Testing skills

Sierra's documented testing workflow:

1. **Simulations** — pre-deployment, "verify your agent performs as
   expected across a wide range of scenarios and avoid regressions."
   Simulations run against curated datasets.
2. **A/B testing** — post-deployment, compare skill or policy
   variants on live traffic with outcome metrics.
3. **Insights Explorer** — trace inspection at the skill-call level
   to diagnose specific bad interactions.
4. **Continuous evaluation** — Sierra's research-grade benchmark
   approach (τ-series, μ-Bench) is run internally against the
   constellation; aggregate results inform model selection per task.

## What's not in public material

- A **published skill schema reference** (open-source or in their
  docs). Customers see this once they have access to the SDK.
- A **complete code example** of a skill definition. The product
  pages describe the pattern; they don't show source.
- A **policy DSL** for the validator agent. Public material says
  policies exist; the language isn't shown.

## How this compares to a framework like LangGraph

LangGraph's `@tool` decorator + `ToolNode` is conceptually similar
but operates at a lower level:

| Concern | LangGraph (framework) | Sierra (managed) |
|---------|------------------------|------------------|
| Skill / tool definition | `@tool` Python decorator; you write the function | Sierra Agent SDK; you compose from templates |
| Validation | Pydantic inside function; you add business rules | Validator agent + policy bindings |
| Idempotency | You implement | Sierra documents "deterministic" execution; implementation under NDA |
| Approval gates | `interrupt_before=['tools']` you wire up | Validator agent + Live Assist routing |
| Destructiveness | No framework concept | Policy bindings; payment-isolation architectural |
| Observability | You write to LangSmith yourself | Insights 2.0 shipped |

The Sierra abstraction is **higher-level and more opinionated**.
That's exactly the buyer-vs-builder trade-off: less flexibility,
more guarantees out of the box.

## Procurement-relevant questions to ask

1. **Can we see a real skill definition under NDA?** Schema, code,
   policy syntax.
2. **What's the validator's policy expressiveness?** Can it reference
   prior turn content? Customer attributes? Time-windowed signals?
3. **What happens when the LLM passes schema-valid but semantically
   wrong args** (e.g. valid customer_id, wrong customer)? Is that a
   validator job?
4. **How does the simulation framework compare to LangSmith / our
   in-house eval?** Can we import our own test set?
5. **What's the development experience** like for a customer-side
   Agent Engineer? Cycle time from "modify a skill" to "see it live"?
