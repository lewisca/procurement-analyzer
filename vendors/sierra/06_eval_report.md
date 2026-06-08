# Sierra — Evaluation and Research

_Sourced from sierra.ai/blog/research and the research blog posts
linked from there. Sierra runs an unusually deep public research
program — multiple benchmarks have been published in 2026 alone with
quantitative methodology._

## Published benchmarks (2026)

| Benchmark | Date | Scope | Key claim |
|-----------|------|-------|-----------|
| **τ-knowledge** | 2026-05-13 | Multi-step tasks with evolving knowledge bases | Finding: "models still struggle to reliably use this information in practice" |
| **τ-voice** | 2026-05-01 | 278 grounded customer-service tasks across retail, airline, telecom | Real-time voice agent evaluation with diverse personas and environmental noise |
| **μ-Bench** | 2026-04-20 | Open multilingual transcription benchmark | Built from customer-service calls across five locales; measures "whether they preserve the speaker's intent" |
| **τ³-Bench** | 2026-03-18 | Extension of τ-bench to knowledge retrieval and voice | Combined benchmark covering tool-use + retrieval + voice |
| **Golden articles** | 2026-04-14 | Daily search quality measurement | Continuous feedback loop on production conversations |
| **Linnaeus / Darwin** | 2026-04-03 | Search models | "Up to 16 percentage point improvements in resolution rates" |
| **Voice transcription routing** | 2026-05-18 | 70+ languages | Dynamic provider routing claim of improved agent effectiveness |

This is **substantially more public research than most managed-agent
vendors publish**. The benchmarks (τ-knowledge, τ-voice, μ-Bench,
τ³-Bench) are open and reproducible.

## Methodology Sierra describes publicly

- **Daily measurement** against live production conversations
  ("Golden articles" approach).
- **Continuous A/B testing** for in-production behavior changes.
- **Adversarial testing** is invited from customers (the WeightWatchers
  Devil's Advocate quote) but Sierra does not publish a structured
  adversarial benchmark of its own.
- **Outcome-based evaluation** is implicitly built into the pricing
  model — Sierra is paid only on successful resolution, so the
  evaluation signal is real money.

## What Sierra publishes vs. what they don't

**Published:**
- Benchmark definitions and high-level findings (τ-* series and μ-Bench)
- Quantitative improvement claims tied to specific releases (Linnaeus
  / Darwin 16 percentage points)
- The fact that they continuously evaluate in production

**Not published:**
- A composite "how well does the Sierra Agent OS perform" score on
  these benchmarks
- Per-customer performance distributions
- Adversarial / red-team results
- A model card equivalent for the Sierra constellation

## Comparison to LangSmith eval

LangSmith provides an evaluation framework — a methodology and tools
— but does not publish performance numbers. Sierra **does both**:
they ship the evaluation framework internally AND publish research
benchmarks that allow third parties to validate the field's general
direction (without revealing per-customer Sierra performance).

This is unusual and is a real signal of evaluation maturity.

## Procurement-relevant questions to ask

1. **How does YOUR proposed agent score on τ³-Bench?** This is the
   most relevant single number Sierra could give a buyer.
2. **What's the production resolution rate** on a similar workload to
   ours? (Most enterprise buyers can get a tiered answer here.)
3. **How is "successful resolution" defined** in the outcome-based
   pricing contract, and is that the same definition used in the
   resolution-rate metric?
4. **Adversarial robustness** — can you share a structured
   adversarial test result, even at an aggregate level?
5. **How often is the eval re-run** when an underlying LLM provider
   in the constellation is updated?
