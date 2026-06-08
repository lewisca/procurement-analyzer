# Salesforce Agentforce — Evaluation Approach

_Sourced from Salesforce's published Agentforce material and the
Atlas Reasoning Engine technical writeup. Salesforce publishes
limited quantitative evaluation data publicly; this document compiles
what's available and explicitly notes the gaps._

## What Salesforce publishes

### Aggregate outcome metrics

The headline claim from public 2026 material:

> "Salesforce Agentforce 360: 85% AI Resolution"

This is an aggregate outcome metric — what percent of customer
interactions reach a successful resolution without human escalation.
It's not a benchmark score; it's a customer-deployment KPI.

### Continuous in-production evaluation

The Atlas writeup describes:

> "The feedback loop captures user signals (thumbs-up/down ratings,
> success metrics) and applies these insights through reinforcement
> learning or fine-tuning, creating what Salesforce describes as a
> 'flywheel' that strengthens performance over time as agents
> accumulate usage experience."

Mechanism: user feedback signals → RL / fine-tuning → improved agents.
This is implementation methodology, not a public benchmark.

### Command Center observability

Per the Atlas writeup:

> "The system provides extensive transparency through the Command
> Center dashboard, which displays agent activities, failure states,
> and decision rationales. Administrators can examine chain-of-thought
> traces from any conversation, enabling audits of the agent's
> reasoning."

This is the evaluation surface available to Salesforce customers
internally. Not a public benchmark either.

## What Salesforce does NOT publish

Salesforce notably **lacks** the kinds of evaluation transparency
that OpenAI and Anthropic publish:

| Evaluation artifact | OpenAI | Anthropic | Salesforce |
|---------------------|--------|-----------|------------|
| Per-model system card | ✅ | ✅ | ❌ (uses partner models) |
| Quantitative red-team data | ✅ (5000 hrs / 400 testers for GPT-5) | ✅ (Frontier Red Team publications) | ❌ Not published |
| Public benchmark scores | ✅ (SWE-bench, GAIA, etc.) | ✅ (TAU-bench, SWE-bench, etc.) | ❌ |
| Deployment-gating policy | ✅ Preparedness Framework | ✅ Responsible Scaling Policy | ❌ |
| Reproducible eval methodology | ✅ openai/evals | ✅ Open methodology | ❌ |

This is partly because **Salesforce uses OpenAI's and Anthropic's
models under the hood** — the model-level safety story is delegated
to those partners. But Salesforce also does not publish evaluation
of the *Agentforce composition* (Atlas + Trust Layer + Topics) the
way Sierra publishes research benchmarks (τ-knowledge, τ-voice).

## The gap that matters for procurement

A procurement buyer evaluating Agentforce gets:

- **Outcome metrics** ("85% AI resolution") — aggregate, customer-side
- **Architectural assurances** (Trust Layer, Topic scoping, ZDR)
- **Compliance certifications** (SOC 2, ISO, FedRAMP, etc.)

A procurement buyer does **not** get from Salesforce:

- Quantitative adversarial-robustness measurements
- Per-task accuracy benchmarks
- Hallucination rate measurements
- Comparison data against alternative agent platforms

The procurement-relevant question becomes: **do the partner LLM
vendors' (OpenAI, Anthropic) published evaluations apply to your
Agentforce deployment?**

The answer is partially yes — model-level capabilities transfer —
but the Atlas + Trust Layer + Topic composition has emergent
behaviors not covered by the underlying models' system cards.

## Comparison to peer evaluation transparency

| Vendor | Public quantitative eval | Why |
|--------|-------------------------|-----|
| OpenAI | Deepest (system cards, Preparedness Framework, 5000-hr red-team data) | Foundation model company; eval IS their product |
| Anthropic | Deep (RSP, Frontier Red Team, system cards per model) | Same |
| Sierra | Moderate (research benchmarks: τ-knowledge, τ-voice, μ-Bench) | Vendor-published research as differentiation |
| **Salesforce Agentforce** | **Limited** (aggregate outcome metrics; Command Center observability) | Platform vendor; eval delegated to partner models |
| LangGraph | Minimal (no central eval program; OSS framework) | OSS framework, no shipping vendor to do evaluations |

## Procurement-relevant questions to ask

1. **For your specific use case** — request Agentforce deployment
   case studies in your industry (Salesforce has many publicly named
   customers — pick relevant ones)
2. **What's the actual "85% resolution" definition** — what's
   counted as a resolution vs an escalation?
3. **Adversarial / red-team evaluation** — has Salesforce or a
   contracted third party performed adversarial testing of the Atlas
   + Trust Layer composition (not just the underlying LLMs)?
4. **Model swap evaluation** — when Atlas's constellation routes a
   sub-task to a different LLM, what's the change-management
   process? Is the new model re-evaluated against your Topics before
   it goes live?
5. **Per-Topic accuracy reporting** — can the Command Center surface
   accuracy / failure rates per Topic over time?
