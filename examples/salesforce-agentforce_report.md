# Procurement Evaluation — salesforce-agentforce

_Analyzed 2026-06-04T14:07:43+00:00 · Rubric: Agentic AI Vendor Evaluation — Horizontal Rubric v2 · Model: claude-sonnet-4-6_

## Verdict

**Weighted overall: 2.27 / 5.0**  ·  <span class="exec-verdict exec-verdict-no">Not recommended</span>

**Not recommended.** Critical capabilities are missing or undisclosed. The risk of deploying this vendor in any consequential workflow is high.

**Recommended next step.** Do not proceed without fundamental remediation. Look at alternative vendors who can answer the questions in this rubric.

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

## At a glance

The three most pressing concerns and the three strongest signals from this evaluation. Use these as the agenda for your next vendor conversation.

### Top concerns (lowest scores)

- **SC2 · 1/5 — Critical gap.** Red flag: The artifacts explicitly state that Salesforce does not document contradiction detection at the Atlas level, and that state coherence relies on the LLM's own consistency plus hallucination flagging — not a dedicated contradiction detector.
- **LT1 · 2/5 — Major gap.** Red flag: The step/iteration ceiling is explicitly not publicly documented and not buyer-configurable.
- **LT2 · 2/5 — Major gap.** No per-execution token budget exists.

### Top strengths (highest scores)

- **TC3 · 4/5 — Strong.** Chain-of-thought traces per conversation are visible to admins in Command Center, including action names, reasoning, and decision rationales.
- **TC1 · 3/5 — Acceptable, with mitigations.** Agentforce provides strong structural pre-execution validation through Topic-bounded action sets — an agent cannot invoke an Action outside its Topic's allowed_actions.
- **SC1 · 3/5 — Acceptable, with mitigations.** The sample trace demonstrates coherent state across 2 iterations (facts established in observe phase of iteration 1 are correctly referenced in reason phase of iteration 2).

## Artifact coverage

**10 of 13 expected artifact slots filled.**

Optional artifacts not provided: `Sample audit log entries`, `Agent state export`, `Tool implementation (code)`.

| Slot | Status | File |
|------|--------|------|
| Product overview | ✓ provided | `01_overview.md` |
| Tool / function schemas | ✓ provided | `02_tool_schema.json` |
| Sample execution trace | ✓ provided | `03_sample_trace.json` |
| Failure-mode / red-team report | ✓ provided | `04_failure_modes.md` |
| Security & privacy | ✓ provided | `05_security_privacy.md` |
| Sample audit log entries | ○ optional, missing | — |
| Agent state export | ○ optional, missing | — |
| Configuration documentation | ✓ provided | `08_configuration.md` |
| Evaluation report | ✓ provided | `06_eval_report.md` |
| Architecture diagram | ✓ provided | `09_architecture.mmd` |
| Tool implementation (code) | ○ optional, missing | — |
| Agent loop / orchestrator | ✓ provided | `10_agent_loop.md` |
| Pricing, SLA, contract terms | ✓ provided | `07_pricing_sla.md` |

## Scorecard by category

Each row is a category from the rubric. The score is the average across the 5 questions in that category.

| Category | What it measures | Avg score |
|----------|------------------|-----------|
| **Tool-Call Correctness** | Does the agent invoke the right tools, the right way? | <span class="score-chip score-chip-3">2.6</span> |
| **Loop Termination / Step Budgets** | Can the agent get stuck or burn through money? | <span class="score-chip score-chip-2">2.2</span> |
| **Multi-Step State Coherence** | Does the agent stay consistent across a long run? | <span class="score-chip score-chip-2">2.0</span> |
| **Weighted overall** | — | <span class="score-chip score-chip-2">2.3</span> |

## Overall observations

Salesforce Agentforce's strongest agentic-AI control is its Topic-bounded Action architecture — the structural constraint that an agent cannot invoke any Action outside its configured Topic's allowed set. This is a genuinely differentiated guardrail enforced at configuration level rather than in developer code, and it directly limits tool misuse risk. The Einstein Trust Layer adds meaningful PII masking pre-LLM, prompt-injection defense, toxicity detection, and output-side hallucination flagging, all backed by an enterprise-grade compliance portfolio (FedRAMP, HIPAA BAA, ISO 27018, SOC 2 Type II). Command Center provides per-conversation chain-of-thought trace visibility with SIEM export capability. For organizations already deeply invested in the Salesforce platform, these are real advantages.

The most significant gaps cluster around loop control, cost governance, and state coherence. The Atlas ReAct loop's step/iteration ceiling is explicitly not publicly documented and is not buyer-configurable — a direct red flag for runaway agent risk. Loop detection beyond an undocumented step count is acknowledged as absent. Under the Flex Credits pricing model (the primary usage-based option), there is no per-execution cost cap, exposing buyers to uncapped per-execution spend from misconfigured or looping agents; only the per-conversation pricing tier provides structural cost bounding. On state coherence, the artifacts explicitly acknowledge that contradiction detection does not exist at the Atlas layer, relying entirely on the underlying LLM's intrinsic consistency. Mid-execution hallucination detection (as opposed to output-side flagging) is also absent. There is no per-run dry-run or plan-inspection mode — only a sandbox-environment approach. Quantitative adversarial evaluation of the Atlas + Trust Layer composition is not published.

Procurement teams should weight these findings carefully by use case. For high-stakes, multi-step workflows in regulated industries (where the FedRAMP posture and Trust Layer PII architecture are decisive), Agentforce may still be the right choice — but buyers must press Salesforce under NDA for the step-ceiling defaults, per-Topic cost alerting capabilities, and any adversarial red-team results on the Atlas composition. For use cases requiring fine-grained runtime control (per-run cost caps, step budgets, dry-run inspection, contradiction detection), Agentforce's closed managed-platform architecture is a material limitation relative to developer-built alternatives.

## Tool-Call Correctness

**What this category measures.** Does the agent invoke the right tools, the right way?

**Why it matters.** Agent misinterprets what a tool does and invokes it incorrectly. In healthcare, wrong tool = wrong medication. In finance, wrong tool = wire to wrong account. Real action + wrong tool = catastrophic.

### TC1: Walk me through how you prevent tool misinterpretation. Show me your validation layer.

<span class="score-chip score-chip-3">3 / 5</span> **Acceptable, with mitigations** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Agentforce provides strong structural pre-execution validation through Topic-bounded action sets — an agent cannot invoke an Action outside its Topic's allowed_actions. Typed input schemas exist on Actions (e.g. order_id: string, amount_cents: integer with min/max, reason_code: enum). The Einstein Trust Layer also adds PII/toxicity/injection checks before and after execution. However, the validation layer has significant gaps: semantically wrong but schema-valid parameter values are not caught by the framework; business-rule validation is fully developer-delegated to Apex/Flow; and no concrete example of a hallucinated parameter being caught and rejected is provided. The iterative refinement ('self-reflection or built-in verification') is vague about exactly when and how bad parameters are intercepted. The artifacts also explicitly disclaim: 'what_it_does_NOT_protect_against_natively' — semantically wrong values. Pre-execution validation exists but is partial, with reliance on developer-written Apex for the harder cases.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `02_tool_schema.json` — "strategy_1_topic_scoping: The Topic configuration restricts which Actions the agent can invoke. An agent assigned to topic_id='schedule_appointment' literally cannot select 'process_refund_under_threshold' — it's not in the topic's allowed_actions."
  - `02_tool_schema.json` — "strategy_2_einstein_trust_layer: Output of each Action's input/output passes through the Einstein Trust Layer: PII masking, toxicity check, prompt-injection detection, hallucination mitigation."
  - `02_tool_schema.json` — "what_it_does_NOT_protect_against_natively: ["Semantically-wrong-but-policy-allowed argument values (developer-implemented Apex / Flow logic)", "Foreign-key existence (typically handled by Salesforce data model)", "Business-rule violations (developer encodes in Topic policies o…"
  - `03_sample_trace.json` — ""topic_allowed_check": "passed (action in topic.allowed_actions)""
  - `11_tool_implementation.md` — "Note: developer responsibility for: - Foreign-key existence (Salesforce SOQL already does this, but   developer must write the query) - Business-rule validation (refund amount ≤ order amount, etc.) - Idempotency"

**Gaps for buyer to verify.** No concrete example of an LLM-hallucinated parameter being rejected pre-execution. No published schema for how Atlas validates parameter values against the Action schema before invoking. The iterative-refinement self-reflection mechanism is not described precisely enough to confirm pre-execution interception.

### TC2: What happens when the agent selects the wrong tool? Is there retry / correction logic?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _low confidence_

**What the analyzer found.** Red flag: there is no documented automatic tool-selection failure detection, no explicit replanning mechanism described, no bounded retry count, and no trace example of wrong-tool selection being caught and corrected. The closest mechanism is 'iterative refinement' with self-reflection and a fallback escalation to human on confidence drops — but these are vague and do not specifically address wrong tool selection. The step ceiling is explicitly stated to be internal and not publicly documented, so the circuit-breaker behavior is a black box. No trace example of wrong-tool correction exists in the artifacts.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `10_agent_loop.md` — "d. ITERATIVE REFINEMENT       - Atlas evaluates LLM-generated plans through "self-reflection         or built-in verification, fine-tuning solutions until valid         outputs emerge"       - On confidence drop or policy violation: ESCALATE"
  - `04_failure_modes.md` — "Atlas's ReAct loop has internal step bounds, but Salesforce does not publicly document the default or how to configure them."
  - `10_agent_loop.md` — "Step / iteration ceiling — Atlas's hard upper bound on ReAct   iterations is not publicly documented. Implied by "iterative   refinement... until valid outputs emerge" but not specified."
  - `04_failure_modes.md` — "The system includes automatic 'transfer to human' fallback actions when confidence drops or policy violations threaten."

**Gaps for buyer to verify.** No published description of retry logic, max retry count, or how Atlas detects it selected the wrong Action. No trace example showing wrong-tool correction. Step ceiling not documented. Buyer cannot verify replanning logic.

### TC3: Do you log which tool was called and with what parameters? Can the decision be audited?

<span class="score-chip score-chip-4">4 / 5</span> **Strong** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Chain-of-thought traces per conversation are visible to admins in Command Center, including action names, reasoning, and decision rationales. The sample trace illustrates iteration number, phase (reason/act/observe), LLM used, inputs to each action, topic_allowed_check, and facts added — covering the key elements. Logs are exportable via Salesforce Events Layer / Data Cloud / SIEM connector, enabling integration with buyer systems. PII masking is applied in logs. However, the underlying per-step event schema is not publicly documented, Event Monitoring for detailed AI-specific logs requires an add-on license, and the trace file is explicitly 'reconstructed from Salesforce's published descriptions' rather than a real export. Token-level detail per step is not shown.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""_documented_observability_features": [     "Command Center dashboard displays agent activities, failure states, and decision rationales",     "Administrators can examine chain-of-thought traces from any conversation, enabling audits of the agent's reasoning",     "Feedback lo…"
  - `03_sample_trace.json` — ""exportable_via": "Salesforce Events Layer / Data Cloud / SIEM connector""
  - `03_sample_trace.json` — ""audit_log_written_to_command_center": true"
  - `03_sample_trace.json` — ""chain_of_thought_visible_to_admins": true"
  - `10_agent_loop.md` — "Per-step trace schema — Command Center shows traces but the   underlying event schema is not publicly documented."
  - `08_configuration.md` — "Command Center | Per-conversation agent activity, decisions, failure states Event Monitoring (add-on) | Detailed audit logs at the platform level"

**Gaps for buyer to verify.** Per-step event schema not publicly documented. Token/cost breakdown per step not shown in trace. Event Monitoring add-on required for full audit detail (cost unclear). Log retention defaults not specified.

### TC4: Have you tested against adversarial inputs that could trick tool selection?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Red flag: Salesforce does not publish quantitative red-team results for adversarial inputs, unlike OpenAI or Anthropic. The Einstein Trust Layer includes prompt-injection defense and a bug bounty program, but no concrete adversarial attack scenarios are described, no known failure modes specific to adversarial tool manipulation are disclosed, and no transparency about attacks that still work is offered. The Trust Layer is described architecturally only. The bug bounty and annual pentest provide some assurance but do not address agentic-AI-specific adversarial evaluation.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "Einstein Trust Layer mitigation (this is Salesforce's strongest documented layer):  - PII masking before LLM call — sensitive data is encrypted and   masked before it reaches the LLM - Toxicity detection — output classifier flags toxic content - Prompt-injection defense — expl…"
  - `04_failure_modes.md` — "Gap: Salesforce does not publish quantitative red-team results (unlike OpenAI's "5,000 hours / 400 testers" or Anthropic's Frontier Red Team publications). The Trust Layer is described architecturally, not quantitatively."
  - `06_eval_report.md` — "Quantitative red-team data | ✅ (5000 hrs / 400 testers for GPT-5) | ✅ (Frontier Red Team publications) | ❌ Not published"
  - `05_security_privacy.md` — "Bug bounty and pentest - Public bug bounty program at trust.salesforce.com - Annual third-party pentest documented in SOC 2 scope - Vulnerability disclosure policy is mature"

**Gaps for buyer to verify.** No published red-team or adversarial evaluation of Atlas + Trust Layer composition. No documented failure modes for adversarial tool selection manipulation. No specifics on prompt injection test cases or outcomes. Buyer cannot assess robustness without requesting NDA materials.

### TC5: Is there a 'dry-run' or simulation mode before real execution?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Red flag: There is no per-run dry-run or simulation mode. Dry-run is environment-based (a separate sandbox org), not an in-product per-execution feature. This means a buyer cannot inspect planned actions for a specific live query before execution — they must set up a parallel sandbox environment with simulated data and test there. This is categorically different from a plan/dry-run mode (like Anthropic's permission_mode='plan') that shows what the agent would do for a given input without executing. For high-risk operations (finance, healthcare), the sandbox approach is cumbersome and not available at runtime.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `02_tool_schema.json` — "dry_run_mode: {     "supported": "via Salesforce Sandbox environments",     "mechanism": "Salesforce admins typically configure Agentforce in a sandbox org with simulated data before promoting to production. Built-in 'preview' for many Actions, but per-run dry-run for arbitrar…"
  - `08_configuration.md` — "No per-run cost cap (use per-conversation pricing or Flex   Credit org caps) No per-execution step ceiling visible to admins (Atlas manages   internally) No "plan" / dry-run mode for arbitrary runs (sandbox orgs are   the dry-run mechanism)"
  - `08_configuration.md` — "Change management for agent configuration follows Salesforce's standard sandbox → UAT → production model. Slower than developer-built agents but more audit-friendly for regulated industries."

**Gaps for buyer to verify.** No per-run simulation mode. Cannot inspect planned actions before execution in production. Sandbox approach requires separate environment setup and does not address runtime pre-execution inspection of specific queries.


## Loop Termination / Step Budgets

**What this category measures.** Can the agent get stuck or burn through money?

**Why it matters.** Agent gets stuck in a reasoning or burn-through loop, exhausting tokens / API calls / dollars. Costs explode, SLAs miss, resources drain. Without hard limits and detection, agents can spiral.

### LT1: What is the maximum step / iteration limit? How is it enforced?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Red flag: The step/iteration ceiling is explicitly not publicly documented and not buyer-configurable. Multiple artifacts confirm this gap. The per-conversation pricing tier ($2/conversation) provides an outcome-based structural bound that partially compensates — runaway under that model is the vendor's cost problem. However, the Flex Credits model ($0.10/action) places the cost risk squarely on the buyer with no documented per-conversation step cap. Since the vendor offers three concurrent pricing models and the per-conversation bound only applies to one of them, this cannot be credited as a full structural protection. The partial credit for the per-conversation tier saves this from a score of 1.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "Atlas's ReAct loop has internal step bounds, but Salesforce does not publicly document the default or how to configure them. The Atlas writeup describes "iterative refinement" which implies a loop ceiling, but specifics are not public."
  - `10_agent_loop.md` — "Step / iteration ceiling — Atlas's hard upper bound on ReAct   iterations is not publicly documented. Implied by "iterative   refinement... until valid outputs emerge" but not specified."
  - `04_failure_modes.md` — "Gap: Less explicit than OpenAI's max_turns or LangGraph's recursion_limit. Buyer-side configurability is unclear from public material."
  - `08_configuration.md` — "No per-execution step ceiling visible to admins (Atlas manages   internally)"
  - `04_failure_modes.md` — "Flex Credits pricing means each Action has a known cost ($0.10 per standard action, $0.15 per voice action). A runaway agent costs the buyer real money (20 credits × $0.005 per action × N actions). Per-conversation tier has a per-conversation cap ($2/conversation)."

**Gaps for buyer to verify.** Step ceiling value not published. Not buyer-configurable. Graceful stop behavior at limit not described. Only partially mitigated by per-conversation pricing (not applicable under Flex Credits or per-user licensing).

### LT2: Can you set token budgets? What happens when they're hit?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** No per-execution token budget exists. There is no real-time token tracking, no alerts as a limit approaches, and no hard stop per execution on token spend. The per-conversation pricing tier provides a structural cost bound ($2/conversation), but: (a) it only applies to one of three pricing models; (b) under Flex Credits the buyer is exposed to uncapped per-execution cost (only org-level monthly caps exist); (c) token-level granularity (per step, per tool call) is not documented anywhere. The artifacts explicitly note 'No per-run cost cap' as a documented gap in configuration.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `08_configuration.md` — "No per-run cost cap (use per-conversation pricing or Flex   Credit org caps)"
  - `07_pricing_sla.md` — "Flex Credits: NOT bounded — agent action count drives cost.   Buyer should set:   - Org-level monthly Flex Credit cap   - Topic-level action budgets where supported   - Alerting on burn rate"
  - `07_pricing_sla.md` — "Per-conversation ($2): predictable per-interaction cost.   Bounded by conversation count, not by agent action count.   Best for: high-action-count workflows where a single conversation   involves many tool calls."
  - `10_agent_loop.md` — "Token / cost budget per run — Flex Credits pricing makes per-   Action cost visible, but per-conversation step cap is not   documented."

**Gaps for buyer to verify.** No token budget per execution. No real-time spend tracking at execution level. No per-step token breakdown visible. Org-level monthly cap only (coarse granularity). Alerting mechanism for approaching limits not described.

### LT3: How do you prevent infinite loops? Is there loop detection?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _low confidence_

**What the analyzer found.** Red flag: Loop detection is explicitly 'not documented; presumably relies on iteration count' per the artifacts. There is no description of semantic loop detection (same tool called with same inputs multiple times), no automatic intervention mechanism beyond the undocumented step ceiling, and no real log examples of loops being caught. The iterative refinement / self-reflection mechanism is vague and does not describe loop-specific detection. This is a meaningful gap — step limits are not loop detection.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "Atlas's ReAct loop has internal step bounds, but Salesforce does not publicly document the default or how to configure them."
  - `10_agent_loop.md` — "Loop / semantic loop detection — not documented; presumably   relies on iteration count."
  - `10_agent_loop.md` — "d. ITERATIVE REFINEMENT       - Atlas evaluates LLM-generated plans through "self-reflection         or built-in verification, fine-tuning solutions until valid         outputs emerge""

**Gaps for buyer to verify.** No documented loop detection logic. No semantic equivalence checking (same action + same inputs = loop). No example of a loop being caught. Step limit ceiling not even documented. Mechanism is a black box.

### LT4: Do you provide detailed logging of every step? Can I see tokens / cost spent?

<span class="score-chip score-chip-3">3 / 5</span> **Acceptable, with mitigations** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Per-conversation chain-of-thought traces are available in Command Center, showing action names, reasoning, inputs/outputs, and decision rationales. The sample trace demonstrates multi-field structured logging per step including iteration number, phase, LLM used, inputs, results, and facts added. Export via Salesforce Events Layer / SIEM connector is supported. However: per-step token counts are not shown anywhere in the trace; cost breakdown per step is not documented; the underlying event schema is not publicly documented; full detail requires an Event Monitoring add-on; and the trace in the artifacts is explicitly 'reconstructed' rather than a real export. The logging story is moderately strong on structure and reasoning visibility but weak on token/cost granularity.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""_documented_observability_features": [     "Command Center dashboard displays agent activities, failure states, and decision rationales",     "Administrators can examine chain-of-thought traces from any conversation, enabling audits of the agent's reasoning""
  - `03_sample_trace.json` — ""exportable_via": "Salesforce Events Layer / Data Cloud / SIEM connector""
  - `08_configuration.md` — "Command Center | Per-conversation agent activity, decisions, failure states Event Monitoring (add-on) | Detailed audit logs at the platform level Salesforce Reports | Build custom reports on Agentforce activity"
  - `10_agent_loop.md` — "Per-step trace schema — Command Center shows traces but the   underlying event schema is not publicly documented."
  - `03_sample_trace.json` — ""pii_masking_applied_in_logs": true"

**Gaps for buyer to verify.** Token count per step not in trace. Cost per step not shown. Event schema not publicly documented. Full audit detail requires add-on license (Event Monitoring). Log retention defaults not specified.

### LT5: Can you set cost caps per execution? Are you alerted?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Red flag: There is no per-execution cost cap feature. Explicit statement in configuration docs: 'No per-run cost cap.' Under Flex Credits (the primary usage-based pricing model), a runaway agent directly increases buyer cost with no per-execution hard stop. The artifacts explicitly warn buyers about this risk. The per-conversation pricing tier ($2/conversation) provides an outcome-based structural bound for that pricing model only — but since Flex Credits is the primary scalable model and 'Salesforce does not publish per-conversation hard caps under Flex Credits,' buyers on Flex Credits have no protection. Org-level monthly caps exist but are coarse and post-hoc relative to individual execution runaway. No real-time alerting mechanism is described.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `08_configuration.md` — "No per-run cost cap (use per-conversation pricing or Flex   Credit org caps)"
  - `07_pricing_sla.md` — "Flex Credits: NOT bounded — agent action count drives cost.   Buyer should set:   - Org-level monthly Flex Credit cap   - Topic-level action budgets where supported   - Alerting on burn rate"
  - `04_failure_modes.md` — "Buyers should be aware: under Flex Credits, a misconfigured agent that loops can run up significant cost. Salesforce does not publish per-conversation hard caps under Flex Credits."
  - `07_pricing_sla.md` — "Per-conversation ($2): predictable per-interaction cost.   Bounded by conversation count, not by agent action count."

**Gaps for buyer to verify.** No per-execution dollar cap. No 80% budget alert mechanism. Flex Credits model fully exposes buyer to runaway cost. Org-level monthly cap only. Per-conversation pricing provides partial structural protection but only for that pricing tier.


## Multi-Step State Coherence

**What this category measures.** Does the agent stay consistent across a long run?

**Why it matters.** Agent forgets facts established early on, or hallucinates facts mid-execution and bases later steps on them. State drifts. Contradictions cascade. Agent decides "user is high-risk" in step 2, then processes their transaction in step 7.

### SC1: How do you maintain context across 5+ steps? Show me a long execution trace.

<span class="score-chip score-chip-3">3 / 5</span> **Acceptable, with mitigations** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** The sample trace demonstrates coherent state across 2 iterations (facts established in observe phase of iteration 1 are correctly referenced in reason phase of iteration 2). Data Cloud provides cross-session persistent context. However, the trace only shows 2 iterations — well below the 5+ step threshold required by the rubric for optimal scoring. No long-horizon trace (5-10 steps) is provided. No documentation of how context window management handles very long sequences. State coherence for complex multi-step tasks remains undemonstrated in the artifacts.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""facts_added": ["order_exists=true", "amount=24500", "within_refund_window=true"],       "policy_check": "amount_cents (24500) > $200 threshold → requires human approval""
  - `03_sample_trace.json` — ""reasoning": "Refund amount $245.00 exceeds the $200 auto-approve threshold. Per Topic policy, must escalate for human approval. Will use the escalate_to_supervisor action.""
  - `04_failure_modes.md` — "Atlas maintains conversational context within a session. Data Cloud provides cross-session persistent context (the customer's full history is available on every interaction)."
  - `01_overview.md` — "The loop "incorporates new context or clarifications from the user mid-task" rather than executing a fixed plan rigidly."

**Gaps for buyer to verify.** No 5+ step execution trace provided. Context window management strategy for long tasks not documented. Summarization / windowing strategy not described. Quality of state coherence at step 8+ cannot be assessed.

### SC2: How do you detect contradictions? (Agent decides X in step 2, contradicts it in step 7)

<span class="score-chip score-chip-1">1 / 5</span> **Critical gap** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Red flag: The artifacts explicitly state that Salesforce does not document contradiction detection at the Atlas level, and that state coherence relies on the LLM's own consistency plus hallucination flagging — not a dedicated contradiction detector. No automated detection of intra-session contradictions is described, no examples of caught contradictions are shown, and no resolution mechanism specific to contradictions exists. This is the lowest-scoring area because the artifacts actively acknowledge the absence of this capability rather than leaving it ambiguous.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "Gap: Salesforce does not document contradiction detection or fact-citation requirements at the Atlas level. Per the published material, state coherence relies on the LLM's own consistency plus Trust Layer hallucination flagging — not a separate contradiction detector."
  - `10_agent_loop.md` — "Loop / semantic loop detection — not documented; presumably   relies on iteration count."

**Gaps for buyer to verify.** No contradiction detection logic documented. No example of a contradiction being caught. Resolution mechanism absent. Full reliance on LLM's intrinsic consistency is explicitly acknowledged as the only mechanism.

### SC3: Is there state validation / checkpointing at each step?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** The sample trace shows implicit state tracking via 'facts_added' in the observe phase of each iteration, which represents the closest thing to checkpointing shown. However, there is no explicit checkpoint mechanism described — no saved state object at each step, no state validation rules checking logical consistency, and no replayability from an intermediate checkpoint. Atlas is closed-source so the actual state management mechanism is opaque. The Command Center traces show some intermediate state, but the underlying schema is undocumented and the state is not described as queryable or resumable.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""facts_added": ["order_exists=true", "amount=24500", "within_refund_window=true"]"
  - `10_agent_loop.md` — "Source code visibility — Atlas is proprietary; buyer cannot   audit the loop implementation."
  - `08_configuration.md` — "No "plan" / dry-run mode for arbitrary runs (sandbox orgs are   the dry-run mechanism)"
  - `10_agent_loop.md` — "Per-step trace schema — Command Center shows traces but the   underlying event schema is not publicly documented."

**Gaps for buyer to verify.** No explicit checkpoint mechanism documented. No state validation rules at each step. Cannot inspect intermediate agent state at an arbitrary step. Not described as replayable from a checkpoint. State lives in the LLM context window (implicitly), not in an explicit queryable store.

### SC4: What happens if the agent hallucinates a fact mid-execution and bases later steps on it?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Einstein Trust Layer includes hallucination detection that flags outputs not grounded in retrieved data — this provides some protection against hallucinated facts at output time. However, this is an egress check on the final response, not a mid-execution check that catches a hallucinated fact in step 3 before it cascades into decisions in steps 5-7. No intra-execution fact-citation requirement is described. No examples of caught mid-execution hallucinations are shown. Quantitative hallucination rates are explicitly not published. The mechanism is architecturally described but undemonstrated, and the critical gap (cascading hallucination mid-execution) is not addressed.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "Einstein Trust Layer hallucination detection — flags outputs   that don't ground in retrieved data"
  - `04_failure_modes.md` — "Iterative refinement in Atlas — "Atlas evaluates LLM-generated   plans through self-reflection or built-in verification, fine-tuning   solutions until valid outputs emerge""
  - `04_failure_modes.md` — "Gap in public evidence: Salesforce does not publish quantitative hallucination rate measurements."
  - `09_architecture.mmd` — "HallucinationCheck[Hallucination detection<br/>flag ungrounded claims]"
  - `04_failure_modes.md` — "Salesforce does not document contradiction detection or fact-citation requirements at the Atlas level."

**Gaps for buyer to verify.** No mid-execution hallucination detection (only output-side). No fact-citation requirement for agent reasoning. No examples of caught hallucinations. No quantitative hallucination rate data. Cascading hallucination risk during multi-step execution not addressed.

### SC5: Can you export the full execution state for debugging?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _low confidence_

**What the analyzer found.** Trace export is supported via Salesforce Events Layer / Data Cloud / SIEM connector, which is positive. However: the per-step trace schema is not publicly documented (gated to logged-in customers via Trailhead); the sample trace in the artifacts is explicitly 'reconstructed' not a real export; there is no documentation of the export format being standard JSON with all facts, decisions, and intermediate states; and replayability from exported state is not described anywhere. The platform lock-in note further suggests that state export for post-mortem debugging outside Salesforce tooling is non-trivial.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""exportable_via": "Salesforce Events Layer / Data Cloud / SIEM connector""
  - `03_sample_trace.json` — ""_caveats_for_procurement": [     "Trace SHAPE is reconstructed from Salesforce's published descriptions; Salesforce does not publish per-customer sample traces.",     "Specific Action / Topic / model names are illustrative.",     "Real implementation: Salesforce customers see…"
  - `10_agent_loop.md` — "Per-step trace schema — Command Center shows traces but the   underlying event schema is not publicly documented."
  - `05_security_privacy.md` — "Salesforce Platform lock-in — leaving Salesforce means leaving    Agentforce; data portability requires planning"

**Gaps for buyer to verify.** Export schema not publicly documented. No confirmation that full intermediate state (facts known at each step, reasoning at each step) is included in exports. Replayability from exported state not documented. Export format and completeness unverifiable without Salesforce login.


## What to do next

This vendor is not ready. The asks below are a baseline; do not commit until they're answered.

### Three concrete things to take back to the vendor

1. **Ask about SC2.** Original question: "_How do you detect contradictions? (Agent decides X in step 2, contradicts it in step 7)_". What you're missing: No contradiction detection logic documented. No example of a contradiction being caught. Resolution mechanism absent. Full reliance on LLM's intrinsic consistency is explicitly acknowledged as the only mechanism.
2. **Ask about LT1.** Original question: "_What is the maximum step / iteration limit? How is it enforced?_". What you're missing: Step ceiling value not published. Not buyer-configurable. Graceful stop behavior at limit not described. Only partially mitigated by per-conversation pricing (not applicable under Flex Credits or per-user licensing).
3. **Ask about LT2.** Original question: "_Can you set token budgets? What happens when they're hit?_". What you're missing: No token budget per execution. No real-time spend tracking at execution level. No per-step token breakdown visible. Org-level monthly cap only (coarse granularity). Alerting mechanism for approaching limits not described.

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

### Artifacts analyzed

- `01_overview.md`
- `02_tool_schema.json`
- `03_sample_trace.json`
- `04_failure_modes.md`
- `05_security_privacy.md`
- `06_eval_report.md`
- `07_pricing_sla.md`
- `08_configuration.md`
- `09_architecture.mmd`
- `10_agent_loop.md`
- `11_tool_implementation.md`

### About this report

Generated by the Procurement Analyzer. Scores are produced by a large language model against a structured rubric and are intended to accelerate, not replace, a buyer's due-diligence judgement. Always verify cited evidence against the source artifacts before acting on the verdict.