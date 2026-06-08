# OpenAI — Evaluation and Safety Research

_OpenAI publishes substantially more evaluation and safety research
than any agent vendor in the buyer's set. This document compiles the
relevant material for procurement evaluation._

_Sources: GPT-5 System Card (PDF, Aug 2025); Operator System Card;
o1 System Card; OpenAI Preparedness Framework v2 (April 2025);
ControlPlane red-team case study; openai.com/security-and-privacy/._

## Published per-model system cards

OpenAI publishes a system card for each major model release. Each
card includes:

- **Evaluation results** across the Preparedness Framework risk
  categories (cybersecurity, CBRN, persuasion, model autonomy).
- **External red-teaming methodology** and aggregate results.
- **Mitigation summaries** with before/after measurements.
- **Known limitations** and residual risk.

| Model | System Card | Date |
|-------|------------|------|
| GPT-5 | gpt-5-system-card.pdf | August 13, 2025 |
| o1 | openai.com/index/openai-o1-system-card/ | 2024 |
| Operator (computer-use agent) | openai.com/index/operator-system-card/ | 2025 |
| Deep Research | (separate write-up) | 2025 |

These are the closest agentic equivalents to a "Lumen-style"
quantitative reliability report.

## Red-team scale

From the GPT-5 System Card:

> "Red teaming work for GPT-5 comprised more than 5,000 hours of work
> from over 400 external testers and experts."

For comparison, this is roughly an order of magnitude more red-team
investment than typically reported by managed agent vendors.

Each campaign aimed to:
1. Contribute to a specific hypothesis related to safety
2. Measure the sufficiency of safeguards in adversarial scenarios
3. Provide strong quantitative comparisons to previous models

External red-teaming is supplemented by **internal red-team testing,
automated evaluations, and alignment audits.**

## Preparedness Framework

The Preparedness Framework v2 (April 2025) is OpenAI's published
deployment-gating policy. It defines:

- **Risk thresholds** per category (cybersecurity, CBRN, persuasion,
  model autonomy) — Low / Medium / High / Critical.
- **Required evaluations** before crossing a threshold.
- **Allowed deployment conditions** per threshold.
- **Continuous evaluation** as model capabilities evolve.

Procurement-relevant: this is one of very few publicly documented
*deployment-gating policies* in the AI industry. It provides a
verifiable framework for asking: "what risk threshold has this model
been certified to?"

**Independent critique exists.** A September 2025 academic analysis
(arxiv 2509.24394) argues that the v2 framework requests evaluation
of "a small minority of AI risks" and permits deployment of "Medium"
capabilities that could "unintentionally enable severe harm." This
critique is worth reading alongside OpenAI's own framing.

## Public benchmarks and evaluations

Beyond the system cards, OpenAI publishes:

- Capability evaluations (MMLU, HumanEval, GPQA, etc.) at model
  launch.
- Function-calling reliability metrics under strict mode.
- Long-context performance curves.
- Safety refusal benchmarks (jailbreak rates, etc.).

Specific to agentic workloads:
- **SWE-bench** results for coding agents.
- **τ-bench** (originally developed externally; OpenAI publishes
  comparable agent-task performance).
- **Operator** browser-task success rates.

## LangSmith-equivalent: OpenAI Evals

OpenAI ships an open-source evals framework (github.com/openai/evals)
plus integrated evals tooling in the OpenAI dashboard. The Agents SDK
includes tracing that feeds into eval workflows automatically.

This is parallel to LangSmith — provides a methodology, not a
managed-service benchmark score.

## What's NOT in the public material

- Per-customer agent-product success rates (these belong to the
  developer who builds on top of the SDK, not to OpenAI).
- Adversarial-robustness scores at the AGENT level (system cards
  evaluate the model; how the agent SDK + guardrails composition
  performs is the developer's eval responsibility).
- A composite "OpenAI Agents safety score" against a fixed
  procurement benchmark — none exists.

## Comparison to peer evaluation transparency

| Vendor | Quantitative public red-team data | Per-model system card | Deployment-gating policy |
|--------|-----------------------------------|----------------------|--------------------------|
| OpenAI | ✅ 5,000+ hours / 400+ external testers | ✅ Per major model | ✅ Preparedness Framework v2 |
| Sierra | Partial (research benchmarks, no red-team scale data) | — | — |
| LangGraph | — (OSS framework, no central red-team budget) | — | — |

## Procurement-relevant questions to ask

1. **For your specific agent use case**, has OpenAI evaluated the
   model on similar tasks? Request relevant section(s) of the system
   card.
2. **What Preparedness Framework level** is the model deployed at?
3. **Is the Agents SDK guardrail framework** something we should rely
   on, or layer additional checks on top?
4. **What's the eval cadence** when a new model snapshot replaces the
   one we're pinned to?
5. **Are agent-level evals** (full SDK + guardrails composition)
   available, or only model-level evals?
