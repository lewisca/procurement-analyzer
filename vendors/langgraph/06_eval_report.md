# LangGraph / LangSmith — Evaluation Approach

_Sourced from the LangSmith evaluation-concepts documentation
(docs.langchain.com/langsmith). This describes the methodology
LangChain ships for evaluating agents built on LangGraph — not a
report of LangGraph's own benchmark performance, which the OSS
project does not publish in a single quantitative document._

## What LangSmith evaluation provides

LangSmith offers an evaluation framework — datasets, evaluators,
experiments — for measuring the quality of agents built on LangGraph
(or any LLM application). It is **a methodology, not a benchmark
score**. There is no published number like "LangGraph agents score N%
on benchmark X."

The framework is built around two evaluation modes:

- **Offline evaluation** — run against a curated dataset with
  reference outputs. Used for regression testing, version comparison,
  pre-deployment quality gates.
- **Online evaluation** — applied to live production traces; no
  reference outputs required. Used for monitoring quality drift and
  anomaly detection.

## Evaluators supported

1. **Human evaluation** — annotation queues with single-run or
   pairwise comparison.
2. **Code evaluators** — deterministic, rule-based functions for
   structure / format / contract checks.
3. **LLM-as-judge** — language model scoring outputs; can be
   reference-free (rubric-only) or reference-based (compared against
   ground truth).
4. **Pairwise** — two versions compared head-to-head, scored by
   heuristic, LLM, or human.

## Dataset structure

Examples contain:

- **inputs** — the variables passed to the agent
- **reference outputs** (optional) — expected results
- **metadata** (optional) — additional context

An **experiment** captures the results of evaluating one application
version against one dataset, supporting side-by-side comparison
across versions.

## Reference-required vs. reference-free

- **Reference-free** — works online and offline. Examples: safety
  checks, format validation, quality heuristics, rubric-based
  LLM-as-judge scoring.
- **Reference-based** — offline only. Examples: correctness checks,
  factual accuracy, exact match, comparison LLM-as-judge.

## What is NOT in the public methodology

The LangSmith evaluation docs available at fetch time do not
reference standard agent benchmarks (SWE-bench, GAIA, τ-bench,
WebArena, etc.) by name or publish performance numbers. The framework
is intended to support evaluation; it does not itself publish a
quantitative score for LangGraph agents.

This is a gap for a procurement buyer: there is no equivalent of a
"model card" with LangGraph-specific quantitative claims. Buyers
evaluating an integrator's LangGraph-based product should ask for:

- The integrator's own eval results on their use case.
- A description of their evaluation methodology — which evaluators,
  which datasets, how often they run.
- Adversarial / red-team results, which are not part of the LangSmith
  evaluation framework's documented scope.

## Cost of evaluation usage

Evaluation runs against datasets are billed via the standard
LangSmith trace pricing (per the pricing page): $2.50 / 1,000 base
traces or $5.00 / 1,000 extended traces. There is no separate
evaluation SKU.
