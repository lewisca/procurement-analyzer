# Example Reports

Four reference outputs from the analyzer so you can see what it produces
without running it yourself. Each was generated against real public
documentation from the named vendors — methodology and sources are cited
inside each file.

## What's here

| File | Type | Score |
|------|------|-------|
| [`anthropic-claude_report.md`](anthropic-claude_report.md) | Single-vendor | **3.27 / 5** |
| [`salesforce-agentforce_report.md`](salesforce-agentforce_report.md) | Single-vendor | **2.27 / 5** |
| [`anthropic-vs-salesforce_comparison.md`](anthropic-vs-salesforce_comparison.md) | Head-to-head | **Δ +1.00** |
| [`lumen-vs-quickbot_comparison.md`](lumen-vs-quickbot_comparison.md) | Head-to-head (mock vendors) | **Δ +4.00** |

## Suggested reading order

1. **Start with [`anthropic-vs-salesforce_comparison.md`](anthropic-vs-salesforce_comparison.md).**
   This is the most interesting output — two real vendors, dramatically
   different archetypes (foundation-model SDK vs enterprise platform),
   with the counter-intuitive result that the enterprise platform with
   the *deepest compliance footprint* scored lower than the foundation
   model SDK. The "Biggest differences" section walks question by
   question through why.

2. **Then [`anthropic-claude_report.md`](anthropic-claude_report.md).**
   Shows what a high-scoring single-vendor report looks like — verbatim
   evidence quotes from Anthropic's public docs, color-coded score chips,
   and a "what to do next" agenda for the buyer.

3. **Compare with [`salesforce-agentforce_report.md`](salesforce-agentforce_report.md).**
   Same shape; lower scores; honest about where Salesforce's public
   posture has gaps (no quantitative red-team data, no buyer-visible
   step ceiling, closed Atlas source) while still crediting their real
   strengths (FedRAMP, ISO 42001, Topic-bounded action sets).

4. **Finally [`lumen-vs-quickbot_comparison.md`](lumen-vs-quickbot_comparison.md).**
   The mock vendors. Lumen and QuickBot are deliberately constructed —
   one as a mature reference vendor, one as a deliberately bad one — to
   demonstrate the tool's discrimination range. The 4-point spread isn't
   typical of real vendors but shows what perfect implementation vs
   deliberately-bad implementation looks like through the rubric.

## What every report includes

- **Verdict** — weighted overall score (1–5) with a procurement-style
  recommendation ("Strong fit" / "Acceptable with mitigations" / etc.)
- **Scope of this evaluation** — explicit framing of what the rubric
  measures and (importantly) what it doesn't
- **At a glance** — top 3 concerns and top 3 strengths
- **Artifact coverage** — what the vendor sent vs what the rubric
  expects
- **Scorecard by category** — Tool-Call Correctness, Loop Termination,
  Multi-Step State Coherence
- **Per-question detail** — every question with reasoning + verbatim
  evidence quotes from the vendor's documents
- **What to do next** — concrete asks to take back to the vendor
- **Glossary** — agentic-AI terms used throughout

## Why these are reproducible

Every score in every example comes from analyzing files in the
[`vendors/`](../vendors/) folders, which are themselves built from
public vendor material with sources cited inline. You can:

1. Inspect the input data in `vendors/<vendor-name>/`
2. Re-run the analyzer against any vendor folder
3. Get a report that should match these examples within a small
   variance (LLM scoring isn't perfectly deterministic)

See the [main README](../README.md) for how to run.
