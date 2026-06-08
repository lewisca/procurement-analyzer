# Procurement Evaluation — anthropic-claude

_Analyzed 2026-06-04T14:07:04+00:00 · Rubric: Agentic AI Vendor Evaluation — Horizontal Rubric v2 · Model: claude-sonnet-4-6_

## Verdict

**Weighted overall: 3.27 / 5.0**  ·  <span class="exec-verdict exec-verdict-concerns">Material concerns</span>

**Material concerns.** The vendor has significant gaps across multiple risk categories. Proceeding without remediation is not advised.

**Recommended next step.** Use the *Top concerns* list below as a discussion agenda with the vendor. Consider parallel evaluation of an alternative vendor. If proceeding, structure the engagement as a time-boxed pilot with explicit exit terms.

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

- **LT3 · 2/5 — Major gap.** RED FLAG: The configuration reference explicitly states 'Semantic loop detection — step counting only' under 'What is NOT in the SDK configuration.' This directly confirms there is no loop detection logic — only a step counter that serves as an indirect bound.
- **LT5 · 2/5 — Major gap.** RED FLAG: Both the pricing doc and configuration reference explicitly state there is no per-run cost cap primitive.
- **SC2 · 2/5 — Major gap.** RED FLAG: The failure modes document explicitly states 'No explicit contradiction detector or fact-citation requirement at the SDK level' and the configuration reference lists 'Contradiction detection — developer's responsibility.' There is no automated detection mechanism, no examples of contradictions being caught, and no resolution mechanism built into the SDK.

### Top strengths (highest scores)

- **TC5 · 5/5 — Fully implemented.** Plan mode (`permission_mode='plan'`) is a first-class, documented capability that generates the full execution plan with predicted tool calls without executing them.
- **TC4 · 4/5 — Strong.** Anthropic has among the deepest public adversarial testing records in the industry, including the Frontier Red Team, published Constitutional Classifiers research, quantitative jailbreak resistance data, and sleeper-agent research.
- **TC3 · 4/5 — Strong.** The trace format is structured JSON/JSONL, includes timestamps, tool name, input parameters, reasoning (thinking blocks), hook decisions, and result.

## Artifact coverage

**11 of 13 expected artifact slots filled.**

Optional artifacts not provided: `Sample audit log entries`, `Agent state export`.

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
| Tool implementation (code) | ✓ provided | `11_tool_implementation.py` |
| Agent loop / orchestrator | ✓ provided | `10_agent_loop.py` |
| Pricing, SLA, contract terms | ✓ provided | `07_pricing_sla.md` |

## Scorecard by category

Each row is a category from the rubric. The score is the average across the 5 questions in that category.

| Category | What it measures | Avg score |
|----------|------------------|-----------|
| **Tool-Call Correctness** | Does the agent invoke the right tools, the right way? | <span class="score-chip score-chip-4">4.0</span> |
| **Loop Termination / Step Budgets** | Can the agent get stuck or burn through money? | <span class="score-chip score-chip-3">2.8</span> |
| **Multi-Step State Coherence** | Does the agent stay consistent across a long run? | <span class="score-chip score-chip-3">3.0</span> |
| **Weighted overall** | — | <span class="score-chip score-chip-3">3.3</span> |

## Overall observations

Anthropic's Claude Agent SDK presents a technically credible agentic platform with several genuine differentiators: strict decode-time schema validation (`strict: true`) that makes schema-invalid tool calls structurally impossible, a first-class `permission_mode="plan"` dry-run capability that generates full execution plans without running tools, a fine-grained lifecycle hook system (PreToolUse / PostToolUse / UserPromptSubmit / Stop) that provides per-tool-name control over approval and denial, and buyer-controlled JSONL session persistence with fork/resume enabling reproducible post-mortems. The artifacts are notably transparent about gaps, which increases trust in the accuracy of the positive claims.

The platform has three significant weaknesses that procurement should weigh carefully against use-case risk. First, loop and cost control are materially underdeveloped: there is no semantic loop detection (only a step counter with an undisclosed default), no per-execution cost cap primitive, and no real-time budget alerting — the artifacts explicitly acknowledge "Buyer bears cost-runaway risk." Second, state coherence safeguards for high-stakes domains are absent at the SDK level: contradiction detection, hallucination detection mid-execution, and fact-citation requirements are all listed as "developer's responsibility" with no built-in mechanism. Automatic context compaction is acknowledged as a heuristic that can lose important early-session facts. Third, wrong-tool retry and circuit-breaker logic are also developer responsibilities, with no bounded retry counter shipped in the SDK.

Overall, the Claude Agent SDK is strongest for developer-facing agentic workloads (where Claude Code is the proven reference application) and for organizations willing to build custom safety layers on top of the hook framework. Buyers considering high-stakes autonomous operations in healthcare or finance should plan for substantial custom development to cover the loop-control, cost-cap, contradiction-detection, and hallucination-detection gaps before going to production.

## Tool-Call Correctness

**What this category measures.** Does the agent invoke the right tools, the right way?

**Why it matters.** Agent misinterprets what a tool does and invokes it incorrectly. In healthcare, wrong tool = wrong medication. In finance, wrong tool = wire to wrong account. Real action + wrong tool = catastrophic.

### TC1: Walk me through how you prevent tool misinterpretation. Show me your validation layer.

<span class="score-chip score-chip-4">4 / 5</span> **Strong** &nbsp;·&nbsp; _high confidence_

**What the analyzer found.** Strict tool use is a genuine decode-time constraint, meaning schema validation happens before execution, not after. The artifacts show typed schemas with patterns, enums, required fields, and min/max constraints. A concrete trace confirms `strict_validated: true` on every tool call. The PreToolUse hook layer adds a second gate for business-rule validation. The artifacts are also honest about what strict mode does NOT protect against (semantic correctness, business rules). The gap is the absence of a concrete example of a rejected invalid parameter in a trace (the trace only shows valid calls); hallucinated-parameter failure-mode examples are described conceptually but not illustrated in an actual trace.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `02_tool_schema.json` — "Add `strict: true` to your tool definitions to ensure Claude's tool calls always match your schema exactly."
  - `02_tool_schema.json` — "Strict tool use constrains Claude's decoding to schema-conforming JSON. Schema-invalid output is structurally impossible."
  - `02_tool_schema.json` — "what_this_protects_against: ["Hallucinated parameter types", "Missing required fields", "Out-of-enum values"]"
  - `03_sample_trace.json` — ""strict_validated": true"
  - `04_failure_modes.md` — "This is structurally equivalent to OpenAI's strict mode — schema violations are impossible for the model to emit when strict is enabled."
  - `02_tool_schema.json` — "what_this_does_NOT_protect_against: ["Semantically wrong but schema-valid arguments", "Business-rule violations", "Foreign-key non-existence", "Idempotency violations"]"

**Gaps for buyer to verify.** No trace example showing a schema-invalid argument actually being rejected at decode time. No illustration of what the model/SDK returns to the developer when strict validation fires.

### TC2: What happens when the agent selects the wrong tool? Is there retry / correction logic?

<span class="score-chip score-chip-3">3 / 5</span> **Acceptable, with mitigations** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** The PreToolUse hook can deny a wrong-tool call and the agent can replan, which is the first step of correction logic. However, bounded retries and circuit-breaker logic are explicitly called out as developer responsibilities, not SDK-enforced. There is no documented automatic replanning mechanism, no bounded retry counter built in, no circuit breaker after N failures, and no real trace example showing wrong-tool selection being detected and corrected. The artifacts are honest about this gap.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "PreToolUse — runs before a tool executes; can deny, allow, modify args, or surface to a user"
  - `10_agent_loop.py` — "Returning a "deny" decision halts the tool call without raising an exception."
  - `10_agent_loop.py` — "# NOT ENFORCED (developer's responsibility): #   - Bounded retry counter on tool errors."
  - `08_configuration.md` — "Bounded retry on tool errors — developer's responsibility"
  - `10_agent_loop.py` — "The agent will see a denied tool result and can replan or ask the user."

**Gaps for buyer to verify.** No SDK-native bounded retry limit. No circuit-breaker after N repeated failures. No trace example showing wrong-tool detection and replanning. Replanning is left to the model's own behavior after receiving a deny result.

### TC3: Do you log which tool was called and with what parameters? Can the decision be audited?

<span class="score-chip score-chip-4">4 / 5</span> **Strong** &nbsp;·&nbsp; _high confidence_

**What the analyzer found.** The trace format is structured JSON/JSONL, includes timestamps, tool name, input parameters, reasoning (thinking blocks), hook decisions, and result. Sessions are stored on the developer's filesystem (buyer-controlled), enabling export and integration with external systems. Reasoning traces (thinking blocks) are captured. Subagent traces are linked via `parent_tool_use_id`. The main gap is that audit-log JSONL to external SIEM format/schema is not publicly documented; structured log export schema requires NDA verification.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""type": "assistant", "subtype": "thinking", "content": "I need to look up the order first, verify the customer's claim, then issue the refund if policy permits.""
  - `03_sample_trace.json` — ""type": "hook_pretooluse", "matcher": "issue_refund", "decision": "deny_and_prompt_user", "elapsed_ms": 8, "reason": "Refund amount $245.00 > $200 auto-approve threshold""
  - `03_sample_trace.json` — ""format": "JSONL on developer's filesystem", "location": "~/.claude/sessions/<session_id>.jsonl or developer-specified", "supports_resume": true, "supports_fork": true"
  - `11_tool_implementation.py` — "f.write(json.dumps({             "ts": datetime.utcnow().isoformat(),             "tool_use_id": tool_use_id,             "args": input_data.get("tool_input"),             "result": input_data.get("tool_result"),         }) + "\n")"
  - `08_configuration.md` — "Subagents are invoked via the `Agent` tool. Messages from inside a subagent's context include `parent_tool_use_id` linking back to the parent invocation — making subagent traces auditable."

**Gaps for buyer to verify.** Audit log export schema and SIEM integration format not publicly documented (flagged as requiring NDA review in security_privacy.md). Retention policy for Managed Agents hosted logs not clearly stated.

### TC4: Have you tested against adversarial inputs that could trick tool selection?

<span class="score-chip score-chip-4">4 / 5</span> **Strong** &nbsp;·&nbsp; _high confidence_

**What the analyzer found.** Anthropic has among the deepest public adversarial testing records in the industry, including the Frontier Red Team, published Constitutional Classifiers research, quantitative jailbreak resistance data, and sleeper-agent research. Concrete attack categories are described (prompt injection, universal jailbreaks, sabotage, deceptive alignment). SDK-level hooks provide mitigation via UserPromptSubmit scanning. The gap is that specific per-tool adversarial test cases for tool-selection manipulation are not individually documented, and transparency about attacks that still work is limited to high-level statements.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "Anthropic operates an internal Frontier Red Team that publishes research on: Sabotage capability evaluations, Sleeper-agent / deceptive-alignment research, Constitutional AI and Constitutional Classifiers, Universal jailbreak evaluations, Agentic misuse — evaluations of agenti…"
  - `06_eval_report.md` — "Universal jailbreaks blocked in deployment with Constitutional Classifiers"
  - `06_eval_report.md` — "Hours-of-attack data showing classifier robustness against sustained red-team campaigns"
  - `04_failure_modes.md` — "async def block_prompt_injection(input_data, ...):     if detect_injection_attempt(input_data["prompt"]):         return {"decision": "deny", "reason": "potential injection"}"
  - `06_eval_report.md` — "Sleeper agent / deceptive alignment — can backdoored behavior persist through safety training?"

**Gaps for buyer to verify.** No specific examples of adversarial inputs that trick tool selection (vs. general jailbreak/injection research). Quantitative failure rates for remaining adversarial patterns not fully public. System cards require NDA access for full detail.

### TC5: Is there a 'dry-run' or simulation mode before real execution?

<span class="score-chip score-chip-5">5 / 5</span> **Fully implemented** &nbsp;·&nbsp; _high confidence_

**What the analyzer found.** Plan mode (`permission_mode='plan'`) is a first-class, documented capability that generates the full execution plan with predicted tool calls without executing them. It is available for any workload including high-risk operations (the refund example shows exactly this use case). The architecture diagram, configuration reference, code examples, and failure modes document all confirm this consistently. Buyer can inspect planned actions before execution. Works for complex multi-step workflows since it operates at the agent-loop level.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `08_configuration.md` — "`plan` | Shows what the agent would do without executing — equivalent to dry-run mode in other SDKs"
  - `08_configuration.md` — "The `plan` mode is **Anthropic's documented dry-run capability** — the agent produces a plan with predicted tool calls but does not execute them. This is materially stronger than OpenAI's `tool_choice` controls because it generates the full execution plan, not just a restriction."
  - `10_agent_loop.py` — "# --- Pattern 3: Plan mode (dry-run) ---------------------------------------- # permission_mode="plan" produces the execution plan without running tools. # Useful for high-risk evaluation: the agent shows what it WOULD do."
  - `02_tool_schema.json` — ""plan": "Shows what the agent would do without executing; equivalent to dry-run""
  - `04_failure_modes.md` — "The SDK's `permission_mode="plan"` is a dry-run mode where the agent shows what it would do without executing — useful for high-risk operations."


## Loop Termination / Step Budgets

**What this category measures.** Can the agent get stuck or burn through money?

**Why it matters.** Agent gets stuck in a reasoning or burn-through loop, exhausting tokens / API calls / dollars. Costs explode, SLAs miss, resources drain. Without hard limits and detection, agents can spiral.

### LT1: What is the maximum step / iteration limit? How is it enforced?

<span class="score-chip score-chip-3">3 / 5</span> **Acceptable, with mitigations** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** The SDK has an internal turn counter that enforces step limits, which is better than no limit. However, the artifacts explicitly acknowledge that the default max_turns value is not publicly specified, and the mechanism for overriding it is not documented in the provided materials. No conservative default value is given, no 'graceful stop' behavior is described, and no example of a limit being hit is shown. The pricing model is token-based (not outcome-based), so the structural alternative credit does not apply. This is a meaningful gap for a procurement buyer.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "The Agent SDK enforces step / iteration limits via the SDK's internal turn counter."
  - `04_failure_modes.md` — "Gaps vs OpenAI / LangGraph: Public material doesn't specify a default max_turns or how to override it in the same explicit way as the OpenAI Agents SDK. Developer should consult the SDK reference or session docs."
  - `03_sample_trace.json` — ""total_turns": 7"

**Gaps for buyer to verify.** Default max_turns value not publicly documented. Configuration parameter to override step limit not shown. No example of graceful stop behavior when limit is hit. No documented ceiling on the limit.

### LT2: Can you set token budgets? What happens when they're hit?

<span class="score-chip score-chip-3">3 / 5</span> **Acceptable, with mitigations** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Token totals are captured in ResultMessage (observable post-hoc), and per-request `max_tokens` provides per-call output caps. Org-level console caps provide a coarse budget. However, there is no per-execution token budget with real-time tracking, no alerts as limits approach mid-execution, and the pricing model is token-based so buyers are exposed to runaway cost. The artifacts honestly flag this gap. Compaction reduces context growth but does not bound spend.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""total_input_tokens": 4421, "total_output_tokens": 612"
  - `07_pricing_sla.md` — "**Per-request max_tokens** caps output per call"
  - `07_pricing_sla.md` — "Gap relative to ideal: no documented per-run cost cap primitive in the SDK itself."
  - `04_failure_modes.md` — "Compaction limits the context-token cost on long runs"
  - `07_pricing_sla.md` — "**Org-level usage caps** in the Anthropic Console"

**Gaps for buyer to verify.** No per-execution token budget with real-time tracking. No alerting at X% of budget. No per-step granular token breakdown in the trace. Org-level caps are coarse and not per-run.

### LT3: How do you prevent infinite loops? Is there loop detection?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** RED FLAG: The configuration reference explicitly states 'Semantic loop detection — step counting only' under 'What is NOT in the SDK configuration.' This directly confirms there is no loop detection logic — only a step counter that serves as an indirect bound. There is no mechanism to detect the same tool being called 3x with the same inputs, no detection of repeated reasoning, and no automatic intervention when a loop pattern is identified. The artifacts are transparent about this gap.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `08_configuration.md` — "Semantic loop detection — step counting only"
  - `04_failure_modes.md` — "The Agent SDK enforces step / iteration limits via the SDK's internal turn counter."
  - `10_agent_loop.py` — "# NOT ENFORCED (developer's responsibility): #   - Bounded retry counter on tool errors."

**Gaps for buyer to verify.** No loop detection logic whatsoever. No example of a loop being caught. No automatic intervention other than eventual step-limit exhaustion. Mechanism is entirely reactive (step counter), not preventive.

### LT4: Do you provide detailed logging of every step? Can I see tokens / cost spent?

<span class="score-chip score-chip-4">4 / 5</span> **Strong** &nbsp;·&nbsp; _high confidence_

**What the analyzer found.** Structured JSONL sessions capture every message type including thinking, tool calls with parameters, hook decisions with elapsed time, tool results, and cumulative token counts. Per-step token usage is present in some messages (individual tool_use messages have usage blocks). Sessions are on the developer's filesystem, making them exportable and queryable. Intermediate states including hook decisions and denials are logged. The main gap is that cost (dollar) breakdown is not directly in the trace — requires multiplying tokens by price externally — and per-step token data is not present on every message type.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""usage": {"input_tokens": 1820, "output_tokens": 88}"
  - `03_sample_trace.json` — ""total_input_tokens": 4421, "total_output_tokens": 612"
  - `03_sample_trace.json` — ""format": "JSONL on developer's filesystem", "location": "~/.claude/sessions/<session_id>.jsonl or developer-specified", "supports_resume": true, "supports_fork": true"
  - `03_sample_trace.json` — ""type": "hook_pretooluse", "matcher": "issue_refund", "decision": "deny_and_prompt_user", "elapsed_ms": 8, "reason": "Refund amount $245.00 > $200 auto-approve threshold""
  - `03_sample_trace.json` — ""type": "assistant", "subtype": "thinking", "content": "I need to look up the order first, verify the customer's claim, then issue the refund if policy permits.""

**Gaps for buyer to verify.** No dollar-cost breakdown in trace (requires external calculation). Per-step token counts not on every message type (only on tool_use messages in the sample). Retention policy for Managed Agents not specified.

### LT5: Can you set cost caps per execution? Are you alerted?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _high confidence_

**What the analyzer found.** RED FLAG: Both the pricing doc and configuration reference explicitly state there is no per-run cost cap primitive. The pricing model is token-based, meaning the buyer bears cost-runaway risk directly. The only controls are per-request max_tokens (caps a single LLM call, not a multi-step execution) and org-level console caps (coarse, not per-run). There are no real-time alerts at 80% of budget, no hard stop per execution, and no transparent cost accounting within a run. The outcome-based pricing alternative does not apply here.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `07_pricing_sla.md` — "Gap relative to ideal: no documented per-run cost cap primitive in the SDK itself."
  - `08_configuration.md` — "Per-run cost cap — no dollar-cap primitive; use max_tokens + org-level cap"
  - `07_pricing_sla.md` — "**Org-level usage caps** in the Anthropic Console"
  - `04_failure_modes.md` — "Pricing model: Token-based, like OpenAI. Buyer bears cost-runaway risk and must use available controls."

**Gaps for buyer to verify.** No per-run cost cap. No real-time spend tracking within an execution. No alerting as cost approaches a threshold. Org-level caps are the only protection and operate at a coarse monthly level.


## Multi-Step State Coherence

**What this category measures.** Does the agent stay consistent across a long run?

**Why it matters.** Agent forgets facts established early on, or hallucinates facts mid-execution and bases later steps on them. State drifts. Contradictions cascade. Agent decides "user is high-risk" in step 2, then processes their transaction in step 7.

### SC1: How do you maintain context across 5+ steps? Show me a long execution trace.

<span class="score-chip score-chip-4">4 / 5</span> **Strong** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** The session persistence model (JSONL), fork/resume, and compaction provide a solid foundation for long-horizon context maintenance. The resume pattern in the code shows cross-session reference ('it' = auth module from prior session). However, the sample trace is only 7 turns — not a 10+ step coherent trace demonstrating state maintained from step 1 to step 8+. The artifacts honestly acknowledge that compaction is 'a heuristic — important early-session facts can be lost if compaction is too aggressive,' which is a real gap.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""total_turns": 7"
  - `01_overview.md` — "**Compaction** — automatic context summarization as limits approach for long-running agents."
  - `04_failure_modes.md` — "Compaction automatically summarizes earlier messages as the context window fills. This keeps long-running agents coherent without manual intervention but is a heuristic — important early-session facts can be lost if compaction is too aggressive."
  - `10_agent_loop.py` — "# Resume — Claude remembers context from prior query     async for message in query(         prompt="Now find all places that call it",  # 'it' = auth module"
  - `01_overview.md` — "**Sessions with fork/resume** — sessions are persistable JSONL on the developer's filesystem, with first-class fork and resume."

**Gaps for buyer to verify.** No long (10+ step) coherent execution trace demonstrating context maintained from early to late steps. Compaction acknowledged as potentially lossy for important early facts. No explicit strategy document for long-horizon tasks beyond compaction.

### SC2: How do you detect contradictions? (Agent decides X in step 2, contradicts it in step 7)

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _high confidence_

**What the analyzer found.** RED FLAG: The failure modes document explicitly states 'No explicit contradiction detector or fact-citation requirement at the SDK level' and the configuration reference lists 'Contradiction detection — developer's responsibility.' There is no automated detection mechanism, no examples of contradictions being caught, and no resolution mechanism built into the SDK. The only mitigation is the general recommendation to use LLM-as-judge feedback, which is a manual developer-implemented pattern, not an automated system. This is a significant gap for the healthcare/finance risk scenarios described in the rubric.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "Gap: No explicit contradiction detector or fact-citation requirement at the SDK level. Same gap as OpenAI."
  - `08_configuration.md` — "Contradiction detection — developer's responsibility"
  - `01_overview.md` — "**Self-verification.** Anthropic recommends building rules-based, visual, or LLM-as-judge feedback into every agent — agents that check their own output "are fundamentally more reliable.""

**Gaps for buyer to verify.** No contradiction detection mechanism at any level of the SDK. No examples of contradictions caught. No automated resolution mechanism. Developer must implement entirely from scratch if needed.

### SC3: Is there state validation / checkpointing at each step?

<span class="score-chip score-chip-3">3 / 5</span> **Acceptable, with mitigations** &nbsp;·&nbsp; _medium confidence_

**What the analyzer found.** Sessions are persisted as JSONL after each interaction, enabling resume from a prior state, which is a form of implicit checkpointing. Fork enables branching from any point. However, there is no explicit per-step checkpoint with state validation rules, no consistency validation built in, and no structured 'what does the agent know right now' query capability. State is implicitly maintained in the context window and JSONL log, not in a separately queryable fact store. The artifacts do not show inspectable intermediate state beyond the message stream.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""format": "JSONL on developer's filesystem", "location": "~/.claude/sessions/<session_id>.jsonl or developer-specified", "supports_resume": true, "supports_fork": true"
  - `01_overview.md` — "**Sessions with fork/resume** — sessions are persistable JSONL on the developer's filesystem, with first-class fork and resume."
  - `08_configuration.md` — "Contradiction detection — developer's responsibility"
  - `10_agent_loop.py` — "# ENFORCED (shipped): #   - Session persistence with fork / resume / tag. #   - Built-in observability (each step yields a typed message)."

**Gaps for buyer to verify.** No per-step state validation rules. No queryable intermediate state object separate from the message log. No consistency validation at checkpoints. Checkpointing is implicit in JSONL persistence, not an explicit checkpoint primitive with validation.

### SC4: What happens if the agent hallucinates a fact mid-execution and bases later steps on it?

<span class="score-chip score-chip-2">2 / 5</span> **Major gap** &nbsp;·&nbsp; _high confidence_

**What the analyzer found.** RED FLAG: No hallucination detection mechanism exists at the SDK level. The artifacts explicitly flag the absence of contradiction detection and fact-citation requirements. Compaction is acknowledged as potentially lossy, which could itself introduce hallucination-like behavior (facts from early turns lost). There is no mechanism to detect references to facts not established earlier, no correction mechanism, and no examples of caught hallucinations. Self-verification via LLM-as-judge is recommended but not implemented. This is a significant gap for high-stakes domains.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `04_failure_modes.md` — "Gap: No explicit contradiction detector or fact-citation requirement at the SDK level. Same gap as OpenAI."
  - `08_configuration.md` — "Contradiction detection — developer's responsibility"
  - `04_failure_modes.md` — "Compaction automatically summarizes earlier messages as the context window fills. This keeps long-running agents coherent without manual intervention but is a heuristic — important early-session facts can be lost if compaction is too aggressive."
  - `06_eval_report.md` — "Aggregate hallucination rate in agentic flows — published per-task in benchmarks but not as a single number."

**Gaps for buyer to verify.** No hallucination detection mechanism. No fact-citation requirement. No correction mechanism for mid-execution hallucinations. No logged examples of hallucinations being caught. Compaction may itself introduce fact loss.

### SC5: Can you export the full execution state for debugging?

<span class="score-chip score-chip-4">4 / 5</span> **Strong** &nbsp;·&nbsp; _high confidence_

**What the analyzer found.** Full execution state is exported as JSONL on the buyer's own filesystem (buyer-controlled, not locked in vendor's system). The format is structured and machine-parseable. Sessions support resume and fork, meaning execution can be replayed or branched from any point — useful for post-mortem debugging. The trace includes reasoning, tool calls, parameters, results, hook decisions, and token counts. The main gap is that the JSONL export does not include a separate structured 'facts known' or 'decisions made' summary — debugging requires parsing the full message stream rather than querying a structured state object.

**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._
  - `03_sample_trace.json` — ""format": "JSONL on developer's filesystem", "location": "~/.claude/sessions/<session_id>.jsonl or developer-specified", "supports_resume": true, "supports_fork": true"
  - `08_configuration.md` — "Sessions are stored as JSONL on the developer's filesystem (or Anthropic's event log under Managed Agents)."
  - `01_overview.md` — "**Sessions with fork/resume** — sessions are persistable JSONL on the developer's filesystem, with first-class fork and resume."
  - `10_agent_loop.py` — "# Fork — branch the session to explore an alternative     new_session_id = fork_session(session_id)"
  - `03_sample_trace.json` — ""_implication": "Buyer can replay or branch any agent run. Forking is a first-class operation: graph.fork_session() in the SDK.""

**Gaps for buyer to verify.** No structured 'facts known / decisions made' export — requires parsing full message stream. Managed Agents state is hosted by Anthropic, not developer filesystem (different ownership model). JSONL schema not formally documented for SIEM/tooling integration.


## What to do next

This vendor has material gaps. Use the asks below as a structured conversation with them — but actively evaluate alternatives in parallel.

### Three concrete things to take back to the vendor

1. **Ask about LT3.** Original question: "_How do you prevent infinite loops? Is there loop detection?_". What you're missing: No loop detection logic whatsoever. No example of a loop being caught. No automatic intervention other than eventual step-limit exhaustion. Mechanism is entirely reactive (step counter), not preventive.
2. **Ask about LT5.** Original question: "_Can you set cost caps per execution? Are you alerted?_". What you're missing: No per-run cost cap. No real-time spend tracking within an execution. No alerting as cost approaches a threshold. Org-level caps are the only protection and operate at a coarse monthly level.
3. **Ask about SC2.** Original question: "_How do you detect contradictions? (Agent decides X in step 2, contradicts it in step 7)_". What you're missing: No contradiction detection mechanism at any level of the SDK. No examples of contradictions caught. No automated resolution mechanism. Developer must implement entirely from scratch if needed.

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
- `10_agent_loop.py`
- `11_tool_implementation.py`

### About this report

Generated by the Procurement Analyzer. Scores are produced by a large language model against a structured rubric and are intended to accelerate, not replace, a buyer's due-diligence judgement. Always verify cited evidence against the source artifacts before acting on the verdict.