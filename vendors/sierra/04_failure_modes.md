# Sierra — Trust & Reliability Approach (Failure-Mode Posture)

_Sierra does not publish a formal failure-mode catalog with observed
production rates the way a Lumen-style reference vendor might. What
they DO publish is their architectural approach to mitigating each
class of failure. This document compiles those documented mitigations
and explicitly notes where evidence is absent._

_Sources: sierra.ai/product/trust-and-reliability;
sierra.ai/blog/constellation-of-models; sierra.ai/blog/agent-os-2-0._

## 1. Hallucination (LLM produces wrong / fabricated content)

**Sierra's documented mitigation:**

> "To mitigate risks inherent in the non-deterministic nature of LLMs,
> Sierra wraps LLMs in supervisory layers to reduce hallucinations,
> ensure security, and prevent abuse." — sierra.ai

- Multi-stage architecture: planner → executor → **validator** agent
  reviews outputs before commit.
- Retrieval-grounded generation (the Linnaeus / Darwin search models
  are claimed to improve resolution rates by "up to 16 percentage
  points").
- Continuous A/B testing in production catches behavior drift.

**Gap in public evidence:** Sierra does not publish a quantitative
hallucination rate or a representative failure example. Procurement
should ask under NDA: *what's your measured hallucination rate on a
representative customer workflow, and how was it measured?*

## 2. Wrong tool / wrong API call

**Sierra's documented mitigation:**

> "When your AI agent accesses your systems of record, those
> interactions are deterministic and controlled to ensure your
> policies and security procedures are always followed."

- The Agent SDK enforces "deterministic API Interactions" — LLMs
  select pre-defined skills with typed inputs, not raw API calls.
- Validator agents review the executor's chosen action before commit.

**Gap:** Sierra's public material doesn't describe what happens when
the LLM passes a schema-valid but semantically wrong argument (e.g.
valid customer_id but the wrong customer). Ask Sierra under NDA.

## 3. Adversarial input / prompt injection / abuse

**Sierra's documented mitigation:**

- Customer-disclosed adversarial testing. WeightWatchers VP Maureen
  Martin (quoted on the trust page): *"Our technology team has been
  playing the part of Devil's Advocate, writing in questions to trip
  the AI agent up. And it is great to look at those examples and
  recognize that the AI has understood, identified, and caught the
  misuse."*
- "Built-in filters and monitors for topics and keywords that are
  off-limits based on your company policies." — sierra.ai

**Gap:** Sierra does not publish a structured red-team report. They
have published research benchmarks (τ-knowledge, τ-voice, τ³-Bench)
focused on capability evaluation; whether these include adversarial
robustness scoring is unclear from public material.

## 4. Single-model degradation / outage

**Sierra's documented mitigation:**

> "Sierra automatically switches between LLM providers to optimise
> your agent's performance and maintain service continuity in case
> one provider experiences an outage."

- The constellation-of-models architecture means no single LLM is a
  single point of failure.
- Continuous monitoring tracks "latency, error rates, and timeouts"
  per model; automated routing fails over to "healthier, equivalent
  models."

**This is unusual in the agentic AI space.** Most vendors are pinned
to one LLM provider. Sierra's documented failover capability is a
real differentiator against single-LLM products.

## 5. PII / sensitive data exposure

**Sierra's documented mitigation:**

- *"Personally identifiable information (PII) shared with the agent
  is automatically encrypted and masked."*
- Payment data routes through a **dedicated PCI-certified
  infrastructure** and *"never touches Sierra's core platform, LLMs,
  or persistent storage."*

The payment-data isolation claim is architecturally strong —
sensitive payment data never enters the LLM context. Procurement
should request the architecture diagram showing this isolation under
NDA.

## 6. Cost / token runaway

**Not publicly addressed.** Sierra's outcome-based pricing model
shifts the cost-runaway risk from buyer to vendor — buyers only pay
on successful resolution — but how Sierra protects ITSELF from
runaway costs (and whether they pass on per-interaction caps to the
buyer's agent design) is not in public material.

For buyers, the implicit guarantee is that "if the agent loops, you
don't pay." But that does not protect against a degraded customer
experience.

## 7. State drift / contradiction across long interactions

**Sierra's documented mitigation:**

- Agent Data Platform (ADP) provides unified context across
  conversations and structured customer data.
- "Memory and continuity to move from conversations to relationships."

**Gap:** Sierra's public material does not describe a contradiction
detector or fact-citation requirement. They claim "true agency: the
ability to connect dots across time" — which is the positive framing
of the same capability — but they don't publish a quantitative
miss rate or a fail-safe mechanism for when state drifts.

## 8. Failover during human escalation

**Documented:** Live Assist hands off to humans on demand, with
context. Sierra explicitly positions human escalation as a
first-class capability rather than a fallback for failure: *"if a
member wants to speak to a human, that's always an option."*

## Summary for procurement

Sierra's failure-mode posture is **architectural and policy-driven**
rather than quantitative. They tell you HOW their architecture
prevents each class of failure but rarely publish numbers. The
strongest signals are:

- The validator-agent layer (real structural mitigation)
- Multi-provider failover (real differentiator)
- PCI infrastructure isolation for payments (real architectural choice)

The weakest signals are:

- No published quantitative failure rates
- No representative failure-trace examples
- No structured red-team report (though they invite customer-side
  Devil's Advocate testing)

These gaps are normal for an enterprise vendor at Sierra's stage —
detail lives under NDA. Procurement should request the relevant
artifacts in the security review phase before signing.
