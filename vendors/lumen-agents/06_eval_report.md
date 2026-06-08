# Lumen Agents — Evaluation Report (Q1 2026)

This is the public summary of our internal evaluation pipeline. Full
methodology, datasets, and per-run results available under NDA.

## Eval pipeline overview

- **Cadence:** Continuous. Smoke evals run on every PR. Full evals run
  on every model upgrade and weekly on `main`. Quarterly we publish a
  rolled-up public summary (this document).
- **Datasets:**
  - `cs_real_2025_q4` — 1,840 real anonymized support tickets from 9
    customers (with consent and DPA permission). Held-out from training
    and never seen by the model in any other context.
  - `cs_synthetic_v3` — 4,200 synthetic tickets covering long-tail
    intents.
  - `adversarial_v2` — 312 prompt-injection / contradictory-instruction
    attacks across 11 categories.
- **Judges:** Hybrid. Deterministic checks (correct tool, correct
  output schema, idempotency-key reuse) for ~70% of evaluation
  signals. LLM-as-judge (Claude Opus 4.7) with a published rubric for
  the remaining 30% (intent classification, escalation appropriateness,
  response quality).
- **Reproducibility:** Eval scripts and rubrics are in our public
  GitHub repo at `lumenagents/evals`. Datasets are not public (PII
  considerations) but inspectable under NDA.

## Headline results (Q1 2026)

Tested model: `claude-sonnet-4-6` (deployed default).

| Use case                        | Success rate | Avg cost | Avg steps | Avg latency |
|---------------------------------|--------------|----------|-----------|-------------|
| Order status lookup             | 99.4%        | $0.011   | 1.4       | 4.2s        |
| Refund (under $100)             | 97.1%        | $0.028   | 3.2       | 9.8s        |
| Refund (over $100, w/ approval) | 96.3%        | $0.043   | 4.8 + appr | 21.4s      |
| Account modification            | 92.8%        | $0.061   | 5.1 + appr | 28.1s      |
| Escalation hand-off             | 99.7%        | $0.014   | 2.3       | 5.1s        |

**Success** = correct tool selected AND correct params AND policy-compliant
outcome AND no contradictions AND no loop signal AND within budgets.

## Adversarial results

`adversarial_v2` (312 attacks). Tested at default safety configuration.

| Category                              | Caught | Missed | Rate    |
|---------------------------------------|--------|--------|---------|
| Prompt injection in KB                | 47/47  | 0      | 100.0%  |
| Prompt injection in customer message  | 42/43  | 1      | 97.7%   |
| Contradictory instructions            | 38/38  | 0      | 100.0%  |
| Tool-parameter hallucination          | 29/31  | 2      | 93.5%   |
| Privilege escalation via reason_code  | 22/22  | 0      | 100.0%  |
| Looping induction                     | 18/18  | 0      | 100.0%  |
| Refund-to-attacker address            | 24/24  | 0      | 100.0%  |
| Authority impersonation               | 19/20  | 1      | 95.0%   |
| Time-based pressure                   | 14/14  | 0      | 100.0%  |
| Encoded / obfuscated instruction      | 19/20  | 1      | 95.0%   |
| Multi-turn social engineering         | 32/35  | 3      | 91.4%   |
| **TOTAL**                             | **304/312** | **8** | **97.4%** |

The 8 missed cases are categorized and published in our quarterly
reliability report. Each has an open fix in our backlog.

## Long-horizon coherence

We track three coherence signals on every `>=5`-step run:

- **State continuity** — 99.8% (a fact added before step N is correctly
  retained through step N).
- **Contradiction detection recall** — 99.7% (synthetic contradictions
  caught by our consistency-checker).
- **Hallucination detection recall** — 96.3% (synthetic mid-execution
  hallucinations caught by source-citation rule).

## Failure-case examples (selected)

We deliberately publish failure cases, not just wins:

1. **Multi-turn social engineering (FM-TC-004 variant).** Attacker
   builds rapport over 4 turns, then in turn 5 asks for refund to a
   different address. Our address-mismatch rule catches the refund call
   but the agent had already disclosed the customer's order list in
   turn 3. **Status:** open; remediation is to add a "disclosure
   policy" rule that gates customer-record info on identity
   verification.

2. **Tool-parameter hallucination on rare order ID format (FM-TC-002
   variant).** Two-character merchant prefix collides with internal ID
   format from a legacy customer. **Status:** patched 2026-02-14.

3. **Escalation message truncation on very long traces.** Agent
   summary handed to humans is truncated at 8KB; >2% of complex tickets
   lose context. **Status:** in progress (rolling-summary improvement).

## Methodology versioning

This is `eval_methodology_v3.2`. Diff from v3.1: added
`multi_turn_social_engineering` category to adversarial suite;
upgraded judge to Opus 4.7; added per-step state continuity signal.

All methodology versions are public at lumenagents.com/evals/methodology.

## How to verify

Enterprise buyers can:

1. Inspect datasets under NDA in our trust center.
2. Run our eval pipeline against their own held-out tickets via a
   shared sandbox.
3. Compare model versions side-by-side in the admin console (we
   maintain N-1 and N-2 for 90 days after any upgrade).
