# Vendor Comparison — Anthropic Claude Agent SDK vs Salesforce Agentforce

_Anthropic Claude Agent SDK analyzed 2026-06-04T14:07:04+00:00  ·  Salesforce Agentforce analyzed 2026-06-04T14:07:43+00:00_
_Rubric: Agentic AI Vendor Evaluation — Horizontal Rubric v2_

## Verdict

**Weighted overall: Anthropic Claude Agent SDK 3.27 / 5.0 · Salesforce Agentforce 2.27 / 5.0**

**Anthropic Claude Agent SDK scores higher overall** (+1.00). On the strength of this evaluation alone, prefer Anthropic Claude Agent SDK — but read the *Biggest differences* section below to confirm the gap is in areas you care about.

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

Category averages and the difference (positive = Anthropic Claude Agent SDK ahead).

| Category | What it measures | Anthropic Claude Agent SDK | Salesforce Agentforce | Δ |
|----------|------------------|----|----|---|
| **Tool-Call Correctness** | Does the agent invoke the right tools, the right way? | <span class="score-chip score-chip-4">4.0</span> | <span class="score-chip score-chip-3">2.6</span> | +1.4 |
| **Loop Termination / Step Budgets** | Can the agent get stuck or burn through money? | <span class="score-chip score-chip-3">2.8</span> | <span class="score-chip score-chip-2">2.2</span> | +0.6 |
| **Multi-Step State Coherence** | Does the agent stay consistent across a long run? | <span class="score-chip score-chip-3">3.0</span> | <span class="score-chip score-chip-2">2.0</span> | +1.0 |
| **Weighted overall** | — | <span class="score-chip score-chip-3">3.3</span> | <span class="score-chip score-chip-2">2.3</span> | **+1.00** |

## Biggest differences (per question)

Where the two vendors diverge most. Start here when comparing — these are the questions a procurement conversation should focus on.

### TC5: Is there a 'dry-run' or simulation mode before real execution?

**Anthropic Claude Agent SDK leads by 3 points.** Anthropic Claude Agent SDK: 5/5  ·  Salesforce Agentforce: 2/5

**Anthropic Claude Agent SDK (Fully implemented).** Plan mode (`permission_mode='plan'`) is a first-class, documented capability that generates the full execution plan with predicted tool calls without executing them. It is available for any workload including high-risk operations (the refund example shows exactly this use case). The architecture diagram, configuration reference, code examples, and failure modes document all confirm this consistently. Buyer can inspect planned actions before execution. Works for complex multi-step workflows since it operates at the agent-loop level.

**Salesforce Agentforce (Major gap).** Red flag: There is no per-run dry-run or simulation mode. Dry-run is environment-based (a separate sandbox org), not an in-product per-execution feature. This means a buyer cannot inspect planned actions for a specific live query before execution — they must set up a parallel sandbox environment with simulated data and test there. This is categorically different from a plan/dry-run mode (like Anthropic's permission_mode='plan') that shows what the agent would do for a given input without executing. For high-risk operations (finance, healthcare), the sandbox approach is cumbersome and not available at runtime.

### TC4: Have you tested against adversarial inputs that could trick tool selection?

**Anthropic Claude Agent SDK leads by 2 points.** Anthropic Claude Agent SDK: 4/5  ·  Salesforce Agentforce: 2/5

**Anthropic Claude Agent SDK (Strong).** Anthropic has among the deepest public adversarial testing records in the industry, including the Frontier Red Team, published Constitutional Classifiers research, quantitative jailbreak resistance data, and sleeper-agent research. Concrete attack categories are described (prompt injection, universal jailbreaks, sabotage, deceptive alignment). SDK-level hooks provide mitigation via UserPromptSubmit scanning. The gap is that specific per-tool adversarial test cases for tool-selection manipulation are not individually documented, and transparency about attacks that still work is limited to high-level statements.

**Salesforce Agentforce (Major gap).** Red flag: Salesforce does not publish quantitative red-team results for adversarial inputs, unlike OpenAI or Anthropic. The Einstein Trust Layer includes prompt-injection defense and a bug bounty program, but no concrete adversarial attack scenarios are described, no known failure modes specific to adversarial tool manipulation are disclosed, and no transparency about attacks that still work is offered. The Trust Layer is described architecturally only. The bug bounty and annual pentest provide some assurance but do not address agentic-AI-specific adversarial evaluation.

### SC5: Can you export the full execution state for debugging?

**Anthropic Claude Agent SDK leads by 2 points.** Anthropic Claude Agent SDK: 4/5  ·  Salesforce Agentforce: 2/5

**Anthropic Claude Agent SDK (Strong).** Full execution state is exported as JSONL on the buyer's own filesystem (buyer-controlled, not locked in vendor's system). The format is structured and machine-parseable. Sessions support resume and fork, meaning execution can be replayed or branched from any point — useful for post-mortem debugging. The trace includes reasoning, tool calls, parameters, results, hook decisions, and token counts. The main gap is that the JSONL export does not include a separate structured 'facts known' or 'decisions made' summary — debugging requires parsing the full message stream rather than querying a structured state object.

**Salesforce Agentforce (Major gap).** Trace export is supported via Salesforce Events Layer / Data Cloud / SIEM connector, which is positive. However: the per-step trace schema is not publicly documented (gated to logged-in customers via Trailhead); the sample trace in the artifacts is explicitly 'reconstructed' not a real export; there is no documentation of the export format being standard JSON with all facts, decisions, and intermediate states; and replayability from exported state is not described anywhere. The platform lock-in note further suggests that state export for post-mortem debugging outside Salesforce tooling is non-trivial.

### TC1: Walk me through how you prevent tool misinterpretation. Show me your validation layer.

**Anthropic Claude Agent SDK leads by 1 points.** Anthropic Claude Agent SDK: 4/5  ·  Salesforce Agentforce: 3/5

**Anthropic Claude Agent SDK (Strong).** Strict tool use is a genuine decode-time constraint, meaning schema validation happens before execution, not after. The artifacts show typed schemas with patterns, enums, required fields, and min/max constraints. A concrete trace confirms `strict_validated: true` on every tool call. The PreToolUse hook layer adds a second gate for business-rule validation. The artifacts are also honest about what strict mode does NOT protect against (semantic correctness, business rules). The gap is the absence of a concrete example of a rejected invalid parameter in a trace (the trace only shows valid calls); hallucinated-parameter failure-mode examples are described conceptually but not illustrated in an actual trace.

**Salesforce Agentforce (Acceptable, with mitigations).** Agentforce provides strong structural pre-execution validation through Topic-bounded action sets — an agent cannot invoke an Action outside its Topic's allowed_actions. Typed input schemas exist on Actions (e.g. order_id: string, amount_cents: integer with min/max, reason_code: enum). The Einstein Trust Layer also adds PII/toxicity/injection checks before and after execution. However, the validation layer has significant gaps: semantically wrong but schema-valid parameter values are not caught by the framework; business-rule validation is fully developer-delegated to Apex/Flow; and no concrete example of a hallucinated parameter being caught and rejected is provided. The iterative refinement ('self-reflection or built-in verification') is vague about exactly when and how bad parameters are intercepted. The artifacts also explicitly disclaim: 'what_it_does_NOT_protect_against_natively' — semantically wrong values. Pre-execution validation exists but is partial, with reliance on developer-written Apex for the harder cases.

### TC2: What happens when the agent selects the wrong tool? Is there retry / correction logic?

**Anthropic Claude Agent SDK leads by 1 points.** Anthropic Claude Agent SDK: 3/5  ·  Salesforce Agentforce: 2/5

**Anthropic Claude Agent SDK (Acceptable, with mitigations).** The PreToolUse hook can deny a wrong-tool call and the agent can replan, which is the first step of correction logic. However, bounded retries and circuit-breaker logic are explicitly called out as developer responsibilities, not SDK-enforced. There is no documented automatic replanning mechanism, no bounded retry counter built in, no circuit breaker after N failures, and no real trace example showing wrong-tool selection being detected and corrected. The artifacts are honest about this gap.

**Salesforce Agentforce (Major gap).** Red flag: there is no documented automatic tool-selection failure detection, no explicit replanning mechanism described, no bounded retry count, and no trace example of wrong-tool selection being caught and corrected. The closest mechanism is 'iterative refinement' with self-reflection and a fallback escalation to human on confidence drops — but these are vague and do not specifically address wrong tool selection. The step ceiling is explicitly stated to be internal and not publicly documented, so the circuit-breaker behavior is a black box. No trace example of wrong-tool correction exists in the artifacts.

## Tool-Call Correctness

**What this category measures.** Does the agent invoke the right tools, the right way?

**Why it matters.** Agent misinterprets what a tool does and invokes it incorrectly. In healthcare, wrong tool = wrong medication. In finance, wrong tool = wire to wrong account. Real action + wrong tool = catastrophic.

_Category average — Anthropic Claude Agent SDK: **4.0**, Salesforce Agentforce: **2.6**, Δ +1.4._

### TC1: Walk me through how you prevent tool misinterpretation. Show me your validation layer.

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-4">4 / 5</span> | Strong |
| Salesforce Agentforce | <span class="score-chip score-chip-3">3 / 5</span> | Acceptable, with mitigations |

**Anthropic Claude Agent SDK — what the analyzer found.** Strict tool use is a genuine decode-time constraint, meaning schema validation happens before execution, not after. The artifacts show typed schemas with patterns, enums, required fields, and min/max constraints. A concrete trace confirms `strict_validated: true` on every tool call. The PreToolUse hook layer adds a second gate for business-rule validation. The artifacts are also honest about what strict mode does NOT protect against (semantic correctness, business rules). The gap is the absence of a concrete example of a rejected invalid parameter in a trace (the trace only shows valid calls); hallucinated-parameter failure-mode examples are described conceptually but not illustrated in an actual trace.

_Gaps to verify with Anthropic Claude Agent SDK._ No trace example showing a schema-invalid argument actually being rejected at decode time. No illustration of what the model/SDK returns to the developer when strict validation fires.

**Salesforce Agentforce — what the analyzer found.** Agentforce provides strong structural pre-execution validation through Topic-bounded action sets — an agent cannot invoke an Action outside its Topic's allowed_actions. Typed input schemas exist on Actions (e.g. order_id: string, amount_cents: integer with min/max, reason_code: enum). The Einstein Trust Layer also adds PII/toxicity/injection checks before and after execution. However, the validation layer has significant gaps: semantically wrong but schema-valid parameter values are not caught by the framework; business-rule validation is fully developer-delegated to Apex/Flow; and no concrete example of a hallucinated parameter being caught and rejected is provided. The iterative refinement ('self-reflection or built-in verification') is vague about exactly when and how bad parameters are intercepted. The artifacts also explicitly disclaim: 'what_it_does_NOT_protect_against_natively' — semantically wrong values. Pre-execution validation exists but is partial, with reliance on developer-written Apex for the harder cases.

_Gaps to verify with Salesforce Agentforce._ No concrete example of an LLM-hallucinated parameter being rejected pre-execution. No published schema for how Atlas validates parameter values against the Action schema before invoking. The iterative-refinement self-reflection mechanism is not described precisely enough to confirm pre-execution interception.

### TC2: What happens when the agent selects the wrong tool? Is there retry / correction logic?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-3">3 / 5</span> | Acceptable, with mitigations |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** The PreToolUse hook can deny a wrong-tool call and the agent can replan, which is the first step of correction logic. However, bounded retries and circuit-breaker logic are explicitly called out as developer responsibilities, not SDK-enforced. There is no documented automatic replanning mechanism, no bounded retry counter built in, no circuit breaker after N failures, and no real trace example showing wrong-tool selection being detected and corrected. The artifacts are honest about this gap.

_Gaps to verify with Anthropic Claude Agent SDK._ No SDK-native bounded retry limit. No circuit-breaker after N repeated failures. No trace example showing wrong-tool detection and replanning. Replanning is left to the model's own behavior after receiving a deny result.

**Salesforce Agentforce — what the analyzer found.** Red flag: there is no documented automatic tool-selection failure detection, no explicit replanning mechanism described, no bounded retry count, and no trace example of wrong-tool selection being caught and corrected. The closest mechanism is 'iterative refinement' with self-reflection and a fallback escalation to human on confidence drops — but these are vague and do not specifically address wrong tool selection. The step ceiling is explicitly stated to be internal and not publicly documented, so the circuit-breaker behavior is a black box. No trace example of wrong-tool correction exists in the artifacts.

_Gaps to verify with Salesforce Agentforce._ No published description of retry logic, max retry count, or how Atlas detects it selected the wrong Action. No trace example showing wrong-tool correction. Step ceiling not documented. Buyer cannot verify replanning logic.

### TC3: Do you log which tool was called and with what parameters? Can the decision be audited?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-4">4 / 5</span> | Strong |
| Salesforce Agentforce | <span class="score-chip score-chip-4">4 / 5</span> | Strong |

**Anthropic Claude Agent SDK — what the analyzer found.** The trace format is structured JSON/JSONL, includes timestamps, tool name, input parameters, reasoning (thinking blocks), hook decisions, and result. Sessions are stored on the developer's filesystem (buyer-controlled), enabling export and integration with external systems. Reasoning traces (thinking blocks) are captured. Subagent traces are linked via `parent_tool_use_id`. The main gap is that audit-log JSONL to external SIEM format/schema is not publicly documented; structured log export schema requires NDA verification.

_Gaps to verify with Anthropic Claude Agent SDK._ Audit log export schema and SIEM integration format not publicly documented (flagged as requiring NDA review in security_privacy.md). Retention policy for Managed Agents hosted logs not clearly stated.

**Salesforce Agentforce — what the analyzer found.** Chain-of-thought traces per conversation are visible to admins in Command Center, including action names, reasoning, and decision rationales. The sample trace illustrates iteration number, phase (reason/act/observe), LLM used, inputs to each action, topic_allowed_check, and facts added — covering the key elements. Logs are exportable via Salesforce Events Layer / Data Cloud / SIEM connector, enabling integration with buyer systems. PII masking is applied in logs. However, the underlying per-step event schema is not publicly documented, Event Monitoring for detailed AI-specific logs requires an add-on license, and the trace file is explicitly 'reconstructed from Salesforce's published descriptions' rather than a real export. Token-level detail per step is not shown.

_Gaps to verify with Salesforce Agentforce._ Per-step event schema not publicly documented. Token/cost breakdown per step not shown in trace. Event Monitoring add-on required for full audit detail (cost unclear). Log retention defaults not specified.

### TC4: Have you tested against adversarial inputs that could trick tool selection?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-4">4 / 5</span> | Strong |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** Anthropic has among the deepest public adversarial testing records in the industry, including the Frontier Red Team, published Constitutional Classifiers research, quantitative jailbreak resistance data, and sleeper-agent research. Concrete attack categories are described (prompt injection, universal jailbreaks, sabotage, deceptive alignment). SDK-level hooks provide mitigation via UserPromptSubmit scanning. The gap is that specific per-tool adversarial test cases for tool-selection manipulation are not individually documented, and transparency about attacks that still work is limited to high-level statements.

_Gaps to verify with Anthropic Claude Agent SDK._ No specific examples of adversarial inputs that trick tool selection (vs. general jailbreak/injection research). Quantitative failure rates for remaining adversarial patterns not fully public. System cards require NDA access for full detail.

**Salesforce Agentforce — what the analyzer found.** Red flag: Salesforce does not publish quantitative red-team results for adversarial inputs, unlike OpenAI or Anthropic. The Einstein Trust Layer includes prompt-injection defense and a bug bounty program, but no concrete adversarial attack scenarios are described, no known failure modes specific to adversarial tool manipulation are disclosed, and no transparency about attacks that still work is offered. The Trust Layer is described architecturally only. The bug bounty and annual pentest provide some assurance but do not address agentic-AI-specific adversarial evaluation.

_Gaps to verify with Salesforce Agentforce._ No published red-team or adversarial evaluation of Atlas + Trust Layer composition. No documented failure modes for adversarial tool selection manipulation. No specifics on prompt injection test cases or outcomes. Buyer cannot assess robustness without requesting NDA materials.

### TC5: Is there a 'dry-run' or simulation mode before real execution?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-5">5 / 5</span> | Fully implemented |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** Plan mode (`permission_mode='plan'`) is a first-class, documented capability that generates the full execution plan with predicted tool calls without executing them. It is available for any workload including high-risk operations (the refund example shows exactly this use case). The architecture diagram, configuration reference, code examples, and failure modes document all confirm this consistently. Buyer can inspect planned actions before execution. Works for complex multi-step workflows since it operates at the agent-loop level.

**Salesforce Agentforce — what the analyzer found.** Red flag: There is no per-run dry-run or simulation mode. Dry-run is environment-based (a separate sandbox org), not an in-product per-execution feature. This means a buyer cannot inspect planned actions for a specific live query before execution — they must set up a parallel sandbox environment with simulated data and test there. This is categorically different from a plan/dry-run mode (like Anthropic's permission_mode='plan') that shows what the agent would do for a given input without executing. For high-risk operations (finance, healthcare), the sandbox approach is cumbersome and not available at runtime.

_Gaps to verify with Salesforce Agentforce._ No per-run simulation mode. Cannot inspect planned actions before execution in production. Sandbox approach requires separate environment setup and does not address runtime pre-execution inspection of specific queries.


## Loop Termination / Step Budgets

**What this category measures.** Can the agent get stuck or burn through money?

**Why it matters.** Agent gets stuck in a reasoning or burn-through loop, exhausting tokens / API calls / dollars. Costs explode, SLAs miss, resources drain. Without hard limits and detection, agents can spiral.

_Category average — Anthropic Claude Agent SDK: **2.8**, Salesforce Agentforce: **2.2**, Δ +0.6._

### LT1: What is the maximum step / iteration limit? How is it enforced?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-3">3 / 5</span> | Acceptable, with mitigations |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** The SDK has an internal turn counter that enforces step limits, which is better than no limit. However, the artifacts explicitly acknowledge that the default max_turns value is not publicly specified, and the mechanism for overriding it is not documented in the provided materials. No conservative default value is given, no 'graceful stop' behavior is described, and no example of a limit being hit is shown. The pricing model is token-based (not outcome-based), so the structural alternative credit does not apply. This is a meaningful gap for a procurement buyer.

_Gaps to verify with Anthropic Claude Agent SDK._ Default max_turns value not publicly documented. Configuration parameter to override step limit not shown. No example of graceful stop behavior when limit is hit. No documented ceiling on the limit.

**Salesforce Agentforce — what the analyzer found.** Red flag: The step/iteration ceiling is explicitly not publicly documented and not buyer-configurable. Multiple artifacts confirm this gap. The per-conversation pricing tier ($2/conversation) provides an outcome-based structural bound that partially compensates — runaway under that model is the vendor's cost problem. However, the Flex Credits model ($0.10/action) places the cost risk squarely on the buyer with no documented per-conversation step cap. Since the vendor offers three concurrent pricing models and the per-conversation bound only applies to one of them, this cannot be credited as a full structural protection. The partial credit for the per-conversation tier saves this from a score of 1.

_Gaps to verify with Salesforce Agentforce._ Step ceiling value not published. Not buyer-configurable. Graceful stop behavior at limit not described. Only partially mitigated by per-conversation pricing (not applicable under Flex Credits or per-user licensing).

### LT2: Can you set token budgets? What happens when they're hit?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-3">3 / 5</span> | Acceptable, with mitigations |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** Token totals are captured in ResultMessage (observable post-hoc), and per-request `max_tokens` provides per-call output caps. Org-level console caps provide a coarse budget. However, there is no per-execution token budget with real-time tracking, no alerts as limits approach mid-execution, and the pricing model is token-based so buyers are exposed to runaway cost. The artifacts honestly flag this gap. Compaction reduces context growth but does not bound spend.

_Gaps to verify with Anthropic Claude Agent SDK._ No per-execution token budget with real-time tracking. No alerting at X% of budget. No per-step granular token breakdown in the trace. Org-level caps are coarse and not per-run.

**Salesforce Agentforce — what the analyzer found.** No per-execution token budget exists. There is no real-time token tracking, no alerts as a limit approaches, and no hard stop per execution on token spend. The per-conversation pricing tier provides a structural cost bound ($2/conversation), but: (a) it only applies to one of three pricing models; (b) under Flex Credits the buyer is exposed to uncapped per-execution cost (only org-level monthly caps exist); (c) token-level granularity (per step, per tool call) is not documented anywhere. The artifacts explicitly note 'No per-run cost cap' as a documented gap in configuration.

_Gaps to verify with Salesforce Agentforce._ No token budget per execution. No real-time spend tracking at execution level. No per-step token breakdown visible. Org-level monthly cap only (coarse granularity). Alerting mechanism for approaching limits not described.

### LT3: How do you prevent infinite loops? Is there loop detection?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** RED FLAG: The configuration reference explicitly states 'Semantic loop detection — step counting only' under 'What is NOT in the SDK configuration.' This directly confirms there is no loop detection logic — only a step counter that serves as an indirect bound. There is no mechanism to detect the same tool being called 3x with the same inputs, no detection of repeated reasoning, and no automatic intervention when a loop pattern is identified. The artifacts are transparent about this gap.

_Gaps to verify with Anthropic Claude Agent SDK._ No loop detection logic whatsoever. No example of a loop being caught. No automatic intervention other than eventual step-limit exhaustion. Mechanism is entirely reactive (step counter), not preventive.

**Salesforce Agentforce — what the analyzer found.** Red flag: Loop detection is explicitly 'not documented; presumably relies on iteration count' per the artifacts. There is no description of semantic loop detection (same tool called with same inputs multiple times), no automatic intervention mechanism beyond the undocumented step ceiling, and no real log examples of loops being caught. The iterative refinement / self-reflection mechanism is vague and does not describe loop-specific detection. This is a meaningful gap — step limits are not loop detection.

_Gaps to verify with Salesforce Agentforce._ No documented loop detection logic. No semantic equivalence checking (same action + same inputs = loop). No example of a loop being caught. Step limit ceiling not even documented. Mechanism is a black box.

### LT4: Do you provide detailed logging of every step? Can I see tokens / cost spent?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-4">4 / 5</span> | Strong |
| Salesforce Agentforce | <span class="score-chip score-chip-3">3 / 5</span> | Acceptable, with mitigations |

**Anthropic Claude Agent SDK — what the analyzer found.** Structured JSONL sessions capture every message type including thinking, tool calls with parameters, hook decisions with elapsed time, tool results, and cumulative token counts. Per-step token usage is present in some messages (individual tool_use messages have usage blocks). Sessions are on the developer's filesystem, making them exportable and queryable. Intermediate states including hook decisions and denials are logged. The main gap is that cost (dollar) breakdown is not directly in the trace — requires multiplying tokens by price externally — and per-step token data is not present on every message type.

_Gaps to verify with Anthropic Claude Agent SDK._ No dollar-cost breakdown in trace (requires external calculation). Per-step token counts not on every message type (only on tool_use messages in the sample). Retention policy for Managed Agents not specified.

**Salesforce Agentforce — what the analyzer found.** Per-conversation chain-of-thought traces are available in Command Center, showing action names, reasoning, inputs/outputs, and decision rationales. The sample trace demonstrates multi-field structured logging per step including iteration number, phase, LLM used, inputs, results, and facts added. Export via Salesforce Events Layer / SIEM connector is supported. However: per-step token counts are not shown anywhere in the trace; cost breakdown per step is not documented; the underlying event schema is not publicly documented; full detail requires an Event Monitoring add-on; and the trace in the artifacts is explicitly 'reconstructed' rather than a real export. The logging story is moderately strong on structure and reasoning visibility but weak on token/cost granularity.

_Gaps to verify with Salesforce Agentforce._ Token count per step not in trace. Cost per step not shown. Event schema not publicly documented. Full audit detail requires add-on license (Event Monitoring). Log retention defaults not specified.

### LT5: Can you set cost caps per execution? Are you alerted?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** RED FLAG: Both the pricing doc and configuration reference explicitly state there is no per-run cost cap primitive. The pricing model is token-based, meaning the buyer bears cost-runaway risk directly. The only controls are per-request max_tokens (caps a single LLM call, not a multi-step execution) and org-level console caps (coarse, not per-run). There are no real-time alerts at 80% of budget, no hard stop per execution, and no transparent cost accounting within a run. The outcome-based pricing alternative does not apply here.

_Gaps to verify with Anthropic Claude Agent SDK._ No per-run cost cap. No real-time spend tracking within an execution. No alerting as cost approaches a threshold. Org-level caps are the only protection and operate at a coarse monthly level.

**Salesforce Agentforce — what the analyzer found.** Red flag: There is no per-execution cost cap feature. Explicit statement in configuration docs: 'No per-run cost cap.' Under Flex Credits (the primary usage-based pricing model), a runaway agent directly increases buyer cost with no per-execution hard stop. The artifacts explicitly warn buyers about this risk. The per-conversation pricing tier ($2/conversation) provides an outcome-based structural bound for that pricing model only — but since Flex Credits is the primary scalable model and 'Salesforce does not publish per-conversation hard caps under Flex Credits,' buyers on Flex Credits have no protection. Org-level monthly caps exist but are coarse and post-hoc relative to individual execution runaway. No real-time alerting mechanism is described.

_Gaps to verify with Salesforce Agentforce._ No per-execution dollar cap. No 80% budget alert mechanism. Flex Credits model fully exposes buyer to runaway cost. Org-level monthly cap only. Per-conversation pricing provides partial structural protection but only for that pricing tier.


## Multi-Step State Coherence

**What this category measures.** Does the agent stay consistent across a long run?

**Why it matters.** Agent forgets facts established early on, or hallucinates facts mid-execution and bases later steps on them. State drifts. Contradictions cascade. Agent decides "user is high-risk" in step 2, then processes their transaction in step 7.

_Category average — Anthropic Claude Agent SDK: **3.0**, Salesforce Agentforce: **2.0**, Δ +1.0._

### SC1: How do you maintain context across 5+ steps? Show me a long execution trace.

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-4">4 / 5</span> | Strong |
| Salesforce Agentforce | <span class="score-chip score-chip-3">3 / 5</span> | Acceptable, with mitigations |

**Anthropic Claude Agent SDK — what the analyzer found.** The session persistence model (JSONL), fork/resume, and compaction provide a solid foundation for long-horizon context maintenance. The resume pattern in the code shows cross-session reference ('it' = auth module from prior session). However, the sample trace is only 7 turns — not a 10+ step coherent trace demonstrating state maintained from step 1 to step 8+. The artifacts honestly acknowledge that compaction is 'a heuristic — important early-session facts can be lost if compaction is too aggressive,' which is a real gap.

_Gaps to verify with Anthropic Claude Agent SDK._ No long (10+ step) coherent execution trace demonstrating context maintained from early to late steps. Compaction acknowledged as potentially lossy for important early facts. No explicit strategy document for long-horizon tasks beyond compaction.

**Salesforce Agentforce — what the analyzer found.** The sample trace demonstrates coherent state across 2 iterations (facts established in observe phase of iteration 1 are correctly referenced in reason phase of iteration 2). Data Cloud provides cross-session persistent context. However, the trace only shows 2 iterations — well below the 5+ step threshold required by the rubric for optimal scoring. No long-horizon trace (5-10 steps) is provided. No documentation of how context window management handles very long sequences. State coherence for complex multi-step tasks remains undemonstrated in the artifacts.

_Gaps to verify with Salesforce Agentforce._ No 5+ step execution trace provided. Context window management strategy for long tasks not documented. Summarization / windowing strategy not described. Quality of state coherence at step 8+ cannot be assessed.

### SC2: How do you detect contradictions? (Agent decides X in step 2, contradicts it in step 7)

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |
| Salesforce Agentforce | <span class="score-chip score-chip-1">1 / 5</span> | Critical gap |

**Anthropic Claude Agent SDK — what the analyzer found.** RED FLAG: The failure modes document explicitly states 'No explicit contradiction detector or fact-citation requirement at the SDK level' and the configuration reference lists 'Contradiction detection — developer's responsibility.' There is no automated detection mechanism, no examples of contradictions being caught, and no resolution mechanism built into the SDK. The only mitigation is the general recommendation to use LLM-as-judge feedback, which is a manual developer-implemented pattern, not an automated system. This is a significant gap for the healthcare/finance risk scenarios described in the rubric.

_Gaps to verify with Anthropic Claude Agent SDK._ No contradiction detection mechanism at any level of the SDK. No examples of contradictions caught. No automated resolution mechanism. Developer must implement entirely from scratch if needed.

**Salesforce Agentforce — what the analyzer found.** Red flag: The artifacts explicitly state that Salesforce does not document contradiction detection at the Atlas level, and that state coherence relies on the LLM's own consistency plus hallucination flagging — not a dedicated contradiction detector. No automated detection of intra-session contradictions is described, no examples of caught contradictions are shown, and no resolution mechanism specific to contradictions exists. This is the lowest-scoring area because the artifacts actively acknowledge the absence of this capability rather than leaving it ambiguous.

_Gaps to verify with Salesforce Agentforce._ No contradiction detection logic documented. No example of a contradiction being caught. Resolution mechanism absent. Full reliance on LLM's intrinsic consistency is explicitly acknowledged as the only mechanism.

### SC3: Is there state validation / checkpointing at each step?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-3">3 / 5</span> | Acceptable, with mitigations |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** Sessions are persisted as JSONL after each interaction, enabling resume from a prior state, which is a form of implicit checkpointing. Fork enables branching from any point. However, there is no explicit per-step checkpoint with state validation rules, no consistency validation built in, and no structured 'what does the agent know right now' query capability. State is implicitly maintained in the context window and JSONL log, not in a separately queryable fact store. The artifacts do not show inspectable intermediate state beyond the message stream.

_Gaps to verify with Anthropic Claude Agent SDK._ No per-step state validation rules. No queryable intermediate state object separate from the message log. No consistency validation at checkpoints. Checkpointing is implicit in JSONL persistence, not an explicit checkpoint primitive with validation.

**Salesforce Agentforce — what the analyzer found.** The sample trace shows implicit state tracking via 'facts_added' in the observe phase of each iteration, which represents the closest thing to checkpointing shown. However, there is no explicit checkpoint mechanism described — no saved state object at each step, no state validation rules checking logical consistency, and no replayability from an intermediate checkpoint. Atlas is closed-source so the actual state management mechanism is opaque. The Command Center traces show some intermediate state, but the underlying schema is undocumented and the state is not described as queryable or resumable.

_Gaps to verify with Salesforce Agentforce._ No explicit checkpoint mechanism documented. No state validation rules at each step. Cannot inspect intermediate agent state at an arbitrary step. Not described as replayable from a checkpoint. State lives in the LLM context window (implicitly), not in an explicit queryable store.

### SC4: What happens if the agent hallucinates a fact mid-execution and bases later steps on it?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** RED FLAG: No hallucination detection mechanism exists at the SDK level. The artifacts explicitly flag the absence of contradiction detection and fact-citation requirements. Compaction is acknowledged as potentially lossy, which could itself introduce hallucination-like behavior (facts from early turns lost). There is no mechanism to detect references to facts not established earlier, no correction mechanism, and no examples of caught hallucinations. Self-verification via LLM-as-judge is recommended but not implemented. This is a significant gap for high-stakes domains.

_Gaps to verify with Anthropic Claude Agent SDK._ No hallucination detection mechanism. No fact-citation requirement. No correction mechanism for mid-execution hallucinations. No logged examples of hallucinations being caught. Compaction may itself introduce fact loss.

**Salesforce Agentforce — what the analyzer found.** Einstein Trust Layer includes hallucination detection that flags outputs not grounded in retrieved data — this provides some protection against hallucinated facts at output time. However, this is an egress check on the final response, not a mid-execution check that catches a hallucinated fact in step 3 before it cascades into decisions in steps 5-7. No intra-execution fact-citation requirement is described. No examples of caught mid-execution hallucinations are shown. Quantitative hallucination rates are explicitly not published. The mechanism is architecturally described but undemonstrated, and the critical gap (cascading hallucination mid-execution) is not addressed.

_Gaps to verify with Salesforce Agentforce._ No mid-execution hallucination detection (only output-side). No fact-citation requirement for agent reasoning. No examples of caught hallucinations. No quantitative hallucination rate data. Cascading hallucination risk during multi-step execution not addressed.

### SC5: Can you export the full execution state for debugging?

| Vendor | Score | Verdict |
|--------|-------|---------|
| Anthropic Claude Agent SDK | <span class="score-chip score-chip-4">4 / 5</span> | Strong |
| Salesforce Agentforce | <span class="score-chip score-chip-2">2 / 5</span> | Major gap |

**Anthropic Claude Agent SDK — what the analyzer found.** Full execution state is exported as JSONL on the buyer's own filesystem (buyer-controlled, not locked in vendor's system). The format is structured and machine-parseable. Sessions support resume and fork, meaning execution can be replayed or branched from any point — useful for post-mortem debugging. The trace includes reasoning, tool calls, parameters, results, hook decisions, and token counts. The main gap is that the JSONL export does not include a separate structured 'facts known' or 'decisions made' summary — debugging requires parsing the full message stream rather than querying a structured state object.

_Gaps to verify with Anthropic Claude Agent SDK._ No structured 'facts known / decisions made' export — requires parsing full message stream. Managed Agents state is hosted by Anthropic, not developer filesystem (different ownership model). JSONL schema not formally documented for SIEM/tooling integration.

**Salesforce Agentforce — what the analyzer found.** Trace export is supported via Salesforce Events Layer / Data Cloud / SIEM connector, which is positive. However: the per-step trace schema is not publicly documented (gated to logged-in customers via Trailhead); the sample trace in the artifacts is explicitly 'reconstructed' not a real export; there is no documentation of the export format being standard JSON with all facts, decisions, and intermediate states; and replayability from exported state is not described anywhere. The platform lock-in note further suggests that state export for post-mortem debugging outside Salesforce tooling is non-trivial.

_Gaps to verify with Salesforce Agentforce._ Export schema not publicly documented. No confirmation that full intermediate state (facts known at each step, reasoning at each step) is included in exports. Replayability from exported state not documented. Export format and completeness unverifiable without Salesforce login.


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