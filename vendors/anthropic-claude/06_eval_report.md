# Anthropic Claude — Evaluation and Safety Research

_Anthropic publishes among the deepest agentic-AI safety research in
the industry. This document compiles the relevant material for
procurement evaluation._

_Sources: anthropic.com/research; per-model system cards
(Sonnet 4.x, Opus 4.x); Anthropic Responsible Scaling Policy;
Frontier Red Team publications._

## Per-model system cards

Anthropic publishes a system card for each Claude model release.
Each card includes:

- **Capability evaluations** across reasoning, coding, science,
  multimodal tasks
- **Safety evaluations** covering refusal rates, jailbreak
  susceptibility, harmful-content rates
- **Agentic safety evaluations** — increasingly important as Claude
  becomes the primary engine for agentic systems
- **Dangerous-capability evaluations** required by the Responsible
  Scaling Policy (CBRN uplift, autonomous replication, cyber
  capabilities)

These have been published with each major model release through 2026.

## Responsible Scaling Policy (RSP)

Anthropic's RSP is the published deployment-gating policy. Key
elements:

- **AI Safety Levels (ASL-1 through ASL-4+)** — capability thresholds
  requiring specific safety mitigations
- **Required evaluations** before deployment at each ASL
- **Deployment safeguards** scaled to capability level
- **Public reporting** of significant safety-relevant capabilities

Like OpenAI's Preparedness Framework, the RSP is a verifiable
gating policy. Procurement-relevant differences:

- Anthropic's RSP has been iterated longer (multiple public revisions
  since 2023)
- Specifies concrete safety mitigations per ASL (e.g., model weights
  security at ASL-3+)
- Includes a model-weight-exfiltration risk model

## Frontier Red Team

Anthropic publishes red-team research with quantitative methodology.
Recent topics include:

- **Sabotage capability evaluations** — can a model deceive an
  overseer about its work?
- **Sleeper agent / deceptive alignment** — can backdoored behavior
  persist through safety training?
- **Constitutional Classifiers** — input/output safety classifiers
  trained with Constitutional AI methods
- **Universal jailbreak evaluations** — published benchmarks against
  jailbreak attempts
- **Agentic misuse** — evaluations of agentic harms specifically

This is published research with reproducible methodology — not
marketing material.

## Agent-specific evaluation methodology

Anthropic's recommended approach for evaluating an agent built on
Claude (from the engineering blog):

> "Agents that can check and improve their own output are
> fundamentally more reliable."

Recommended verification approaches:

1. **Rules-based feedback** (linting, schema validation, etc.)
2. **Visual feedback** for UI-touching agents
3. **LLM-as-judge** for subjective evaluation

This is methodology, not benchmark scores — same shape as
LangSmith's evaluation framework but with more explicit guidance.

## Public benchmarks

Anthropic regularly publishes Claude's performance on:

- **SWE-bench Verified** — software engineering tasks
- **GPQA Diamond** — graduate-level questions
- **MMLU** — multi-task language understanding
- **HumanEval** — code generation
- **TAU-bench** — agent task evaluation
- **Browser-use benchmarks** — for computer-use models
- **Constitutional Classifiers eval** — for safety mitigations

Claude Opus models have been at or near SOTA on agentic benchmarks
through 2026, particularly SWE-bench (where Claude Code is the
reference application).

## Adversarial-robustness data

The Constitutional Classifiers paper and subsequent system cards
publish quantitative jailbreak resistance data. Key claims:

- **Universal jailbreaks blocked** in deployment with Constitutional
  Classifiers
- **Hours-of-attack data** showing classifier robustness against
  sustained red-team campaigns

Specific numbers are in the system cards; methodology is
reproducible.

## What's NOT in public material

- A composite "Claude Agent score" against a fixed procurement
  benchmark — none exists.
- Per-customer agent performance distributions — these belong to the
  developer who builds on the SDK.
- Aggregate hallucination rate in agentic flows — published per-task
  in benchmarks but not as a single number.

## Comparison to peer evaluation transparency

| Vendor | Per-model system card | Deployment gating policy | Public red-team data | Multi-cloud eval |
|--------|-----------------------|--------------------------|----------------------|------------------|
| Anthropic | ✅ Per major release | ✅ RSP (multiple iterations) | ✅ Frontier Red Team publications | ✅ via Bedrock / Vertex / Azure |
| OpenAI | ✅ Per major release | ✅ Preparedness Framework v2 | ✅ 5000+ hours / 400+ testers | Primarily Azure |
| Sierra | — | — | Partial (research benchmarks) | — |
| LangGraph | — | — | — | — |

**Anthropic and OpenAI are in roughly the same tier on public
evaluation depth.** Both materially ahead of agent-product vendors
(Sierra) and OSS frameworks (LangGraph).

## Procurement-relevant questions to ask

1. **Which Claude model is best for our agent workload?** Request the
   relevant section of the system card.
2. **What ASL is the model currently deployed at?**
3. **For agentic-misuse evaluation specifically** — what's tested,
   and what are the residual risks?
4. **For our use case** — is Constitutional Classifiers running, and
   what's the false-positive rate?
5. **Which cloud should we use** (Bedrock vs Vertex vs Azure vs
   direct) given our compliance constraints?
