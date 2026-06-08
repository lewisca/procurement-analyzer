# Vendor Comparison — Lumen Agents (mock — mature) vs QuickBot AI (mock — early stage)

_Lumen Agents (mock — mature) analyzed 2026-05-13T20:07:01+00:00  ·  QuickBot AI (mock — early stage) analyzed 2026-05-13T20:05:41+00:00_
_Rubric: Agentic AI Vendor Evaluation — Horizontal Rubric v2_

## Verdict

**Weighted overall: Lumen Agents (mock — mature) 5.00 / 5.0 · QuickBot AI (mock — early stage) 1.00 / 5.0**

**Lumen Agents (mock — mature) scores higher overall** (+4.00). On the strength of this evaluation alone, prefer Lumen Agents (mock — mature) — but read the *Biggest differences* section below to confirm the gap is in areas you care about.

## Scope of this evaluation

This rubric measures **one dimension**: how procurement-ready a vendor's public posture is for an agentic AI deployment. The score is useful, but it is not the whole procurement decision.

### What this rubric measures

- Whether the vendor's documentation describes the technical mechanisms a buyer needs to verify (validation layers, step ceilings, audit logs, evaluation methodology, failure modes).
- Whether evidence is **concrete** (source code, published quantitative results, verbatim policy language) or **abstract** (architectural prose without measurements).
- Where the vendor's public posture has gaps a buyer will need to close under NDA before signing.

### What this rubric does NOT measure

- **Business fit.** Whether this vendor's product category matches the buyer's actual use case.
- **Time-to-value.** A managed product can deploy in weeks; building equivalent on a framework can take 6–12 months.
- **Team capability fit.** Some vendors require Python developers, some require platform admins, some require no-code users.
- **Integration depth.** A vendor that scores well here may fail because it doesn't integrate with the buyer's existing systems.
- **Vendor lock-in / portability.** Frameworks give maximum portability; enterprise platforms can lock in tightly.
- **Total cost of ownership at scale.** Token-based, outcome-based, license-based, and per-action pricing models all have different cost curves.
- **Vertical certifications.** FedRAMP, FDA SaMD, FINRA, and other regulatory bars are not in this rubric.
- **Build-vs-buy economics.** This depends on the buyer's team and budget, not on vendor characteristics.

### How to use this score

A sound procurement decision is three layers:

1. **Business-fit screen** — what's the use case, team capability, integration profile, regulatory bar, time-to-value tolerance?
2. **Category selection** — build with a framework / foundation model + SDK / buy a managed product / extend an enterprise platform / pick a vertical specialist?
3. **Vendor due diligence within the chosen category** — *this is the layer this report addresses*.

This report is the right tool for comparing vendors **within the same category** (e.g., managed customer-experience agents like Sierra vs Decagon vs Cresta; or foundation-model + SDK choices like Anthropic vs OpenAI). It is **not** the right tool for choosing between fundamentally different categories — those decisions belong to Layers 1 and 2.

If you have completed Layers 1–2 and this vendor is a candidate within the right category, the score below is meaningful. If you have not, complete those layers first before relying on this score alone.

**Note on this specific comparison.** Both vendors should be in the same Layer-2 category for the comparison below to be apples-to-apples. If one vendor is a framework and the other is a managed product (or one is a foundation-model SDK and the other an enterprise platform), the score difference reflects category posture more than vendor quality. Use the per-category and per-question detail to spot when this is happening.

## Scorecard side by side

Category averages and the difference (positive = Lumen Agents (mock — mature) ahead).

| Category | What it measures | Lumen Agents (mock — mature) | QuickBot AI (mock — early stage) | Δ |
|----------|------------------|----|----|---|
| **Tool-Call Correctness** | Does the agent invoke the right tools, the right way? | <span class="score-chip score-chip-5">5.0</span> | <span class="score-chip score-chip-1">1.0</span> | +4.0 |
| **Loop Termination / Step Budgets** | Can the agent get stuck or burn through money? | <span class="score-chip score-chip-5">5.0</span> | <span class="score-chip score-chip-1">1.0</span> | +4.0 |
| **Multi-Step State Coherence** | Does the agent stay consistent across a long run? | <span class="score-chip score-chip-5">5.0</span> | <span class="score-chip score-chip-1">1.0</span> | +4.0 |
| **Weighted overall** | — | <span class="score-chip score-chip-5">5.0</span> | <span class="score-chip score-chip-1">1.0</span> | **+4.00** |

## Biggest differences (per question)

Where the two vendors diverge most. Start here when comparing — these are the questions a procurement conversation should focus on.

### TC1: Walk me through how you prevent tool misinterpretation. Show me your validation layer.

**Lumen Agents (mock — mature) leads by 4 points.** Lumen Agents (mock — mature): 5/5  ·  QuickBot AI (mock — early stage): 1/5

**Lumen Agents (mock — mature) (Fully implemented).** Lumen provides typed JSON Schema 2020-12 validation that runs strictly before execution, a concrete rejection example (string 'fifty dollars' for an integer field), FK existence checks catching hallucinated order IDs, explicit error handling that triggers replanning, and code-level proof via tool_implementation.py. All optimal signals are present with no red flags.

**QuickBot AI (mock — early stage) (Critical gap).** Red flag: The tool implementation explicitly defers error handling to the downstream CRM ('Most errors are handled by the CRM's API anyway'), meaning invalid inputs are sent to real systems before any validation occurs. The agent loop in 11_agent_loop.py calls tools with raw LLM-provided args directly — no type checking, no schema validation, no pre-execution guard. The tool schema in 02_tool_schema.json lists types as plain string annotations (e.g. 'string', 'number') with no enforcement mechanism. There is no validation layer, no rejection of hallucinated parameters, and no pre-execution check anywhere in the artifacts.

### TC2: What happens when the agent selects the wrong tool? Is there retry / correction logic?

**Lumen Agents (mock — mature) leads by 4 points.** Lumen Agents (mock — mature): 5/5  ·  QuickBot AI (mock — early stage): 1/5

**Lumen Agents (mock — mature) (Fully implemented).** Wrong-tool selection is a documented failure mode (FM-TC-003) with a real observed rate (0.34%), dual-layer detection (pre-plan intent classifier and post-execution outcome checker), bounded retries (max 3 per step) enforced in agent_loop.py, and a circuit-breaker that escalates to a human. All optimal signals—including a real example, automatic replanning, bounded retries, and escalation—are present.

**QuickBot AI (mock — early stage) (Critical gap).** Red flag: The agent loop is a bare `while True` with no retry logic, no wrong-tool detection, no bounded retry counter, no circuit breaker, and no escalation path. If the agent selects the wrong tool, the error is returned as a string to `messages` and the loop continues indefinitely — a textbook infinite loop risk. The failure_modes doc confirms the only stop condition is the agent deciding it's done. No examples of self-correction or replanning exist anywhere in the artifacts.

### TC3: Do you log which tool was called and with what parameters? Can the decision be audited?

**Lumen Agents (mock — mature) leads by 4 points.** Lumen Agents (mock — mature): 5/5  ·  QuickBot AI (mock — early stage): 1/5

**Lumen Agents (mock — mature) (Fully implemented).** Every step in the sample trace includes timestamp, tool name, input params, output, validation status, per-step token and cost breakdown, elapsed time, and LLM reasoning. Logs are structured JSON, immutable (append-only, signed), exportable to buyer SIEM, and retained 365 days. The reasoning trace captures the LLM's plan rationale explicitly. All optimal signals present.

**QuickBot AI (mock — early stage) (Critical gap).** Red flags: The sample trace captures only action name and a one-word result ('found', 'ok', 'sent') — no input parameters, no output payloads, no LLM reasoning, no timestamps per step, and no tool-selection rationale. The audit log sample is similarly sparse (no parameters, no agent reasoning). Logs are retained only 7 days — far too short for audit purposes. Export requires emailing support, not a programmatic API. No structured JSON with full parameter capture, no immutability guarantees, and no evidence of replayability.

### TC4: Have you tested against adversarial inputs that could trick tool selection?

**Lumen Agents (mock — mature) leads by 4 points.** Lumen Agents (mock — mature): 5/5  ·  QuickBot AI (mock — early stage): 1/5

**Lumen Agents (mock — mature) (Fully implemented).** Lumen documents a structured adversarial test suite (312 attacks across 11 categories), runs it weekly and on every model upgrade, provides quantitative pass/fail results, names specific attack categories, gives a concrete real example (KB prompt injection), and is transparent about the 8 missed cases with open fixes. They acknowledge attacks that still partially work (multi-turn social engineering at 91.4%). All optimal signals are met.

**QuickBot AI (mock — early stage) (Critical gap).** Red flag: The vendor explicitly admits 'We haven't done specific red-team testing in-house yet.' Adversarial testing is listed as merely 'researching' on the roadmap. The only mitigation cited is delegating to model providers' built-in protections — no in-house testing framework, no documented attack scenarios, no known failure modes from adversarial inputs, and no concrete mitigations for prompt injection or tool-selection manipulation.

### TC5: Is there a 'dry-run' or simulation mode before real execution?

**Lumen Agents (mock — mature) leads by 4 points.** Lumen Agents (mock — mature): 5/5  ·  QuickBot AI (mock — early stage): 1/5

**Lumen Agents (mock — mature) (Fully implemented).** Dry-run mode is fully implemented, enabled by default for all write_high_risk and destructive tools, buyer-configurable, demonstrated in the sample trace for a real refund workflow (7-step multi-step case), and wired into the orchestrator code. Planned actions are shown before execution, including what would execute and why. All optimal signals are present.

**QuickBot AI (mock — early stage) (Critical gap).** No dry-run or simulation mode exists anywhere in the artifacts. The agent loop immediately executes all tool calls against live systems. The only approximation of a safety gate mentioned is CRM-level approval for high-value refunds — which is a downstream CRM feature, not a QuickBot dry-run capability. There is no mechanism for a buyer to inspect planned actions before execution.

## Tool-Call Correctness

**What this category measures.** Does the agent invoke the right tools, the right way?

**Why it matters.** Agent misinterprets what a tool does and invokes it incorrectly. In healthcare, wrong tool = wrong medication. In finance, wrong tool = wire to wrong account. Real action + wrong tool = catastrophic.

_Category average — Lumen Agents (mock — mature): **5.0**, QuickBot AI (mock — early stage): **1.0**, Δ +4.0._

### TC1: Walk me through how you prevent tool misinterpretation. Show me your validation layer.

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Lumen provides typed JSON Schema 2020-12 validation that runs strictly before execution, a concrete rejection example (string 'fifty dollars' for an integer field), FK existence checks catching hallucinated order IDs, explicit error handling that triggers replanning, and code-level proof via tool_implementation.py. All optimal signals are present with no red flags.

_Gaps to verify with Lumen Agents (mock — mature)._ Buyers cannot inspect the full business-rule validator suite without NDA access; schema coverage for every tool parameter edge case is not exhaustively documented publicly, but the pattern and example are convincing.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: The tool implementation explicitly defers error handling to the downstream CRM ('Most errors are handled by the CRM's API anyway'), meaning invalid inputs are sent to real systems before any validation occurs. The agent loop in 11_agent_loop.py calls tools with raw LLM-provided args directly — no type checking, no schema validation, no pre-execution guard. The tool schema in 02_tool_schema.json lists types as plain string annotations (e.g. 'string', 'number') with no enforcement mechanism. There is no validation layer, no rejection of hallucinated parameters, and no pre-execution check anywhere in the artifacts.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: typed schema enforcement code (e.g. Pydantic models), pre-execution validators, examples of rejected invalid parameters, and error-handling paths when the LLM hallucinates a parameter.

### TC2: What happens when the agent selects the wrong tool? Is there retry / correction logic?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Wrong-tool selection is a documented failure mode (FM-TC-003) with a real observed rate (0.34%), dual-layer detection (pre-plan intent classifier and post-execution outcome checker), bounded retries (max 3 per step) enforced in agent_loop.py, and a circuit-breaker that escalates to a human. All optimal signals—including a real example, automatic replanning, bounded retries, and escalation—are present.

_Gaps to verify with Lumen Agents (mock — mature)._ The evaluation report doesn't show a raw trace of a wrong-tool correction; relying on failure-mode doc and pseudocode. But the evidence is otherwise comprehensive.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: The agent loop is a bare `while True` with no retry logic, no wrong-tool detection, no bounded retry counter, no circuit breaker, and no escalation path. If the agent selects the wrong tool, the error is returned as a string to `messages` and the loop continues indefinitely — a textbook infinite loop risk. The failure_modes doc confirms the only stop condition is the agent deciding it's done. No examples of self-correction or replanning exist anywhere in the artifacts.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: tool-selection error detection, bounded retry logic (e.g. max 3 attempts), circuit breaker, escalation path, and a real trace showing correction after wrong-tool selection.

### TC3: Do you log which tool was called and with what parameters? Can the decision be audited?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Every step in the sample trace includes timestamp, tool name, input params, output, validation status, per-step token and cost breakdown, elapsed time, and LLM reasoning. Logs are structured JSON, immutable (append-only, signed), exportable to buyer SIEM, and retained 365 days. The reasoning trace captures the LLM's plan rationale explicitly. All optimal signals present.

_Gaps to verify with Lumen Agents (mock — mature)._ None notable.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flags: The sample trace captures only action name and a one-word result ('found', 'ok', 'sent') — no input parameters, no output payloads, no LLM reasoning, no timestamps per step, and no tool-selection rationale. The audit log sample is similarly sparse (no parameters, no agent reasoning). Logs are retained only 7 days — far too short for audit purposes. Export requires emailing support, not a programmatic API. No structured JSON with full parameter capture, no immutability guarantees, and no evidence of replayability.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: full parameter logging per tool call, LLM reasoning traces, structured exportable logs, longer retention policy, and immutability/tamper-evidence controls.

### TC4: Have you tested against adversarial inputs that could trick tool selection?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Lumen documents a structured adversarial test suite (312 attacks across 11 categories), runs it weekly and on every model upgrade, provides quantitative pass/fail results, names specific attack categories, gives a concrete real example (KB prompt injection), and is transparent about the 8 missed cases with open fixes. They acknowledge attacks that still partially work (multi-turn social engineering at 91.4%). All optimal signals are met.

_Gaps to verify with Lumen Agents (mock — mature)._ Full adversarial dataset is not public (NDA required); multi-turn social engineering at 91.4% is a known open weakness, though transparently disclosed.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: The vendor explicitly admits 'We haven't done specific red-team testing in-house yet.' Adversarial testing is listed as merely 'researching' on the roadmap. The only mitigation cited is delegating to model providers' built-in protections — no in-house testing framework, no documented attack scenarios, no known failure modes from adversarial inputs, and no concrete mitigations for prompt injection or tool-selection manipulation.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: in-house red-team results, documented adversarial attack scenarios and mitigations, known failure modes from adversarial testing, and a timeline for the adversarial testing suite.

### TC5: Is there a 'dry-run' or simulation mode before real execution?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Dry-run mode is fully implemented, enabled by default for all write_high_risk and destructive tools, buyer-configurable, demonstrated in the sample trace for a real refund workflow (7-step multi-step case), and wired into the orchestrator code. Planned actions are shown before execution, including what would execute and why. All optimal signals are present.

_Gaps to verify with Lumen Agents (mock — mature)._ None notable.

**QuickBot AI (mock — early stage) — what the analyzer found.** No dry-run or simulation mode exists anywhere in the artifacts. The agent loop immediately executes all tool calls against live systems. The only approximation of a safety gate mentioned is CRM-level approval for high-value refunds — which is a downstream CRM feature, not a QuickBot dry-run capability. There is no mechanism for a buyer to inspect planned actions before execution.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: a sandbox/simulation mode, dry-run execution path that shows planned actions without executing them, and confirmation it works for multi-step workflows.


## Loop Termination / Step Budgets

**What this category measures.** Can the agent get stuck or burn through money?

**Why it matters.** Agent gets stuck in a reasoning or burn-through loop, exhausting tokens / API calls / dollars. Costs explode, SLAs miss, resources drain. Without hard limits and detection, agents can spiral.

_Category average — Lumen Agents (mock — mature): **5.0**, QuickBot AI (mock — early stage): **1.0**, Δ +4.0._

### LT1: What is the maximum step / iteration limit? How is it enforced?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Hard step limit is runtime-enforced (not advisory, not prompt-based), defaulting to 25 with a max ceiling of 50, configurable per use case, with conservative per-use-case defaults (5 for simple lookups, 12 for complex refunds). The agent loop code shows the hard stop and graceful escalation on limit hit. The 0.21% exhaustion rate is documented with clean escalation in 98% of those cases. All optimal signals are present.

_Gaps to verify with Lumen Agents (mock — mature)._ None notable.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: The pricing/SLA document explicitly states 'No hard step or token limits.' The agent loop is a literal `while True` with no step counter, no ceiling, and no enforcement mechanism. The failure_modes document confirms the only termination condition is the agent's own decision — meaning a malfunctioning agent can loop indefinitely. This is the canonical runaway agent recipe.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: a configurable step limit, runtime enforcement code, graceful termination behavior at the limit, and a conservative default value.

### LT2: Can you set token budgets? What happens when they're hit?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Token budget per run is configurable (default 20K), tracked in real-time, alerts fire at 80%, hard stop at 100%. The sample trace shows per-step token breakdown (input/output) and budget remaining at completion. Cost is also tracked per step. All optimal signals are present.

_Gaps to verify with Lumen Agents (mock — mature)._ None notable.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: The vendor explicitly states there are no token limits. The sample trace contains no token tracking whatsoever. There is no evidence of per-execution token budgets, real-time tracking, warning alerts as limits approach, or hard stops. Cost budgets per execution are also absent. The pricing model bundles cost into the plan ('no surprises'), which means there is no per-execution cost accountability.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: token budget configuration options, real-time token tracking per step, alerting at budget thresholds, hard stop behavior, and per-execution cost breakdowns.

### LT3: How do you prevent infinite loops? Is there loop detection?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Loop detection is multi-signal: hash-based for exact repeats (FM-LT-001), embedding-similarity for semantic repeats (FM-LT-004), and state-hash-unchanged tracking. It fires at step 3 of repeated identical calls, is checked at every step, wired into the orchestrator, and escalates automatically. Concrete examples with observed production rates are documented. All optimal signals present.

_Gaps to verify with Lumen Agents (mock — mature)._ None notable.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: The agent loop has no loop detection of any kind — no repeated-action detection, no state comparison across steps, no cycle detection. The failure_modes response is dismissive ('agents are designed to not get stuck') and reveals the only termination mechanism is the agent deciding it's done. There is no automatic intervention, no escalation, and no real examples of loop detection from logs.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: explicit loop detection logic (e.g. same tool + same args = loop), automatic intervention mechanism, real log examples of detected loops, and escalation paths.

### LT4: Do you provide detailed logging of every step? Can I see tokens / cost spent?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Every step in the sample trace includes step number, action type, tool name, input params, output, validation status, per-step token breakdown (input/output), cost in USD, and elapsed_ms. Aggregate totals and budget remaining are also captured. Logs are structured JSON, immutable, exportable via REST API and streaming to S3/Splunk/GCS. All optimal signals are present.

_Gaps to verify with Lumen Agents (mock — mature)._ None notable.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: The sample trace contains no tokens, no cost, no per-step reasoning, no input parameters, and no intermediate states — just action names and one-word results. The audit log is similarly bare. Retention is only 7 days. Export requires emailing support rather than a programmatic API. There is no token or cost breakdown visible anywhere.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: per-step token counts, cost breakdowns, input/output parameters in logs, LLM reasoning per step, error/retry logging, longer retention, and a queryable export API.

### LT5: Can you set cost caps per execution? Are you alerted?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Dollar cost cap per execution is configurable, tracked in real-time (per-step cost_usd in trace), alerts fire at 80% via Slack/email/PagerDuty, and a hard stop is enforced at 100%. Tenant-wide monthly caps are also available. Cost accounting spans all steps including tool calls and LLM invocations. The audit log shows a live config update of the cost cap. All optimal signals present.

_Gaps to verify with Lumen Agents (mock — mature)._ None notable.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: There is no cost-cap feature per execution. The pricing model absorbs costs into the plan, which actually masks per-execution cost visibility rather than enabling control. No real-time spend tracking, no alerting at 80% of budget, no hard stop on cost, and no per-execution cost accounting exist in any artifact.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: per-execution dollar cap configuration, real-time cost tracking, threshold alerts, hard stop behavior when cap is reached, and transparent cost accounting across tool calls.


## Multi-Step State Coherence

**What this category measures.** Does the agent stay consistent across a long run?

**Why it matters.** Agent forgets facts established early on, or hallucinates facts mid-execution and bases later steps on them. State drifts. Contradictions cascade. Agent decides "user is high-risk" in step 2, then processes their transaction in step 7.

_Category average — Lumen Agents (mock — mature): **5.0**, QuickBot AI (mock — early stage): **1.0**, Δ +4.0._

### SC1: How do you maintain context across 5+ steps? Show me a long execution trace.

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** An 8-step trace is provided showing coherent context retention: facts from step 2 (customer.risk_score) are referenced in step 7 approval, facts from step 3 (tracking POD) are referenced in step 4 reasoning. The explicit JSON facts state (not implicit context window) is the mechanism. State continuity is 99.8% per eval report. Long-horizon strategy is explicitly documented. All optimal signals present.

_Gaps to verify with Lumen Agents (mock — mature)._ None notable.

**QuickBot AI (mock — early stage) — what the analyzer found.** The only execution trace provided is 3 steps with no state detail. Context is maintained only through the raw `messages` list in the agent loop — no explicit memory management, no windowing strategy, no summarization, no long-horizon state handling. There is no 5+ step trace and no discussion of context degradation strategy anywhere in the artifacts.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: a 5–10 step coherent execution trace, explicit long-context strategy (summarization, memory, windowing), evidence that facts from step 1 are correctly used in step 8+.

### SC2: How do you detect contradictions? (Agent decides X in step 2, contradicts it in step 7)

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Contradiction detection is automated (logical predicates over facts-state JSON), runs at every step, catches real inter-step contradictions (item-not-received claim vs. proof-of-delivery fact), 99.7% detection recall in eval, with replan/escalate resolution. The sample trace shows a caught contradiction with verdict and resolution. The 0.3% miss rate for distantly-related facts is transparently disclosed. All optimal signals present.

_Gaps to verify with Lumen Agents (mock — mature)._ The specific predicate rules per use case are not enumerated publicly, but the mechanism and metrics are well documented.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: The vendor's response to contradiction detection is explicitly dismissive — 'Agents are generally good at staying consistent.' There is no consistency-checking logic, no automated detection, no examples of caught contradictions, and no resolution mechanism. The answer relies entirely on the assumption that LLMs don't contradict themselves, which is naive and unsupported.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: consistency-checking implementation, automated detection of inter-step contradictions, real examples of caught contradictions, and a resolution/escalation mechanism.

### SC3: Is there state validation / checkpointing at each step?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** State checkpoints are created at each step with SHA-256 hashes, facts count, and per-fact source citations. The state is explicit JSON (not implicit in context window), inspectable, and fully replayable via a POST /api/v1/replay endpoint that rebuilds state and verifies per-step hashes. All optimal signals present.

_Gaps to verify with Lumen Agents (mock — mature)._ Not every step has a checkpoint in the state_export (steps 4 and 6 are missing from the checkpoint list), though the key steps are covered. This is a minor gap.

**QuickBot AI (mock — early stage) — what the analyzer found.** There is no checkpointing mechanism anywhere in the artifacts. State is entirely implicit in the `messages` list in memory. No intermediate state is saved, validated, or made inspectable. There is no ability to resume from a checkpoint if interrupted, and no state validation rules. The trace does not capture intermediate state at any step.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: checkpoint implementation per step, state validation rules, inspectable intermediate state, replayability from any checkpoint, and explicit queryable state storage.

### SC4: What happens if the agent hallucinates a fact mid-execution and bases later steps on it?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** Hallucination detection is built into the state-validator: every fact must cite a source step and tool. Facts without citations are rejected before they can influence later steps. 96.3% recall on synthetic hallucinations is documented. A concrete example (address confirmed without a confirmation tool call) is given. The correction mechanism (re-verify or escalate) is specified. All optimal signals present.

_Gaps to verify with Lumen Agents (mock — mature)._ The 3.7% miss rate on hallucination detection is not further characterized (what types escape?). Buyers would benefit from knowing what hallucination patterns evade the source-citation rule.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: The vendor's hallucination strategy is entirely delegated to model providers ('We rely on the model provider's improvements here'). There is no in-agent hallucination detection, no mechanism to catch references to unestablished facts, no correction mechanism, no examples of caught hallucinations, and no preventive strategy requiring agents to cite sources. This is a critical gap for any high-stakes deployment.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: hallucination detection logic, source-citation enforcement, examples of caught mid-execution hallucinations, correction/escalation mechanisms, and logs showing hallucination handling.

### SC5: Can you export the full execution state for debugging?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Lumen Agents (mock — mature) | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| QuickBot AI (mock — early stage) | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Lumen Agents (mock — mature) — what the analyzer found.** A complete state export is provided in structured JSON (lumen.state.v2), including all facts with source citations, decisions with rules cited, checkpoints with state hashes, consistency check results, and loop detector status. The export is digitally signed (ed25519), replayable via a documented API endpoint, and compatible with multiple runtime versions. Retained for 365 days online, 7 years cold storage on Enterprise. All optimal signals present.

_Gaps to verify with Lumen Agents (mock — mature)._ The state export does not appear to include per-step LLM reasoning text inline (that's in the trace, not the state export), but the two documents together are comprehensive. This is a very minor gap.

**QuickBot AI (mock — early stage) — what the analyzer found.** Red flag: Full execution state export does not exist. The only export mechanism is emailing support@quickbot.ai — not a programmatic API. The sample trace is severely incomplete (no reasoning, no parameters, no intermediate facts, no per-step state). State is only in the in-memory messages list, which is not persisted beyond 7-day logs. There is no replayability, no post-mortem capability, and no standard format export.

_Gaps to verify with QuickBot AI (mock — early stage)._ Need to see: full state export in JSON including reasoning, facts, decisions, tool call parameters, intermediate states; programmatic export API; replayability from exported state; and post-mortem tooling.


## Glossary

Quick definitions for terms used in this report. Skip if you already know them.

- **Agent** — An AI system that can take actions (call tools, run code, send messages), not just answer questions in chat.
- **Agent loop** — The repeating cycle of: plan → call a tool → read the result → decide the next action. Most production agents are loops, not one-shot calls.
- **Tool / function call** — When the agent calls a piece of code or a service — e.g. "look up an order", "issue a refund", "send an email". Each tool has typed arguments.
- **Tool schema** — The contract that defines each tool: its name, arguments, allowed values, and whether it has real-world side effects (destructive).
- **Hallucination** — When the agent invents a fact or a tool argument that isn't grounded in the evidence — e.g. claims it confirmed an address that was never confirmed.
- **Loop (runaway)** — When the agent gets stuck in a repeating cycle — calling the same tool, or paraphrasing the same question — without making progress. Burns tokens and money.
- **Step budget** — A hard ceiling on how many actions the agent can take in one run. If reached, the agent stops gracefully and (ideally) escalates.
- **Token budget / cost cap** — A hard ceiling on the number of language-model tokens (or dollars) a run can consume. Prevents cost explosions from runaway loops.
- **Checkpoint** — A snapshot of the agent's state (known facts, decisions made, open tasks) saved at each step. Lets you inspect what the agent "knew" mid-run and replay if needed.
- **State coherence** — Whether the agent stays consistent over a long run — remembers facts established earlier, doesn't contradict itself, doesn't act on hallucinated facts.
- **Contradiction detection** — Logic that flags when a decision the agent makes contradicts a fact it established earlier (e.g. step 2: "user is high-risk"; step 7: refund issued anyway).
- **Idempotency** — Property that running the same action twice produces the same result. Prevents double-charges if a network retry happens.
- **Dry-run / simulation mode** — A way to ask "what would the agent do?" without actually doing it. Critical for high-risk operations.
- **Approval gate** — A point in the agent's flow where a human must approve before a destructive action runs (refund, account closure, etc.).
- **Red-team / adversarial testing** — Deliberately trying to break the agent — prompt injection, contradictory instructions, hallucinated tool params — to find vulnerabilities before attackers do.

---

### About this comparison

Generated by the Procurement Analyzer. Both vendors were scored independently against the same rubric; this report compares the scores. As with the single-vendor report, scores are produced by a large language model and should accelerate, not replace, buyer judgement. Verify cited evidence in the source documents before acting.