# Salesforce Agentforce — Atlas Reasoning Engine Loop (Public Description)

_The Atlas Reasoning Engine is closed-source proprietary IP. There
is no public source code. This document describes the loop conceptually
from Salesforce's published material._

_Sources: cirra.ai's Atlas Reasoning Engine technical writeup;
Salesforce Agentforce documentation; the Einstein Trust Layer
documentation._

## High-level loop

For each user interaction, Atlas executes (paraphrased from
Salesforce's published descriptions):

```
1. INGRESS through Einstein Trust Layer (input side)
   - PII masking: sensitive fields encrypted + masked BEFORE the LLM sees them
   - Toxicity classifier on input
   - Prompt-injection defense classifier
   - On violation: skip to ESCALATE (transfer to human)

2. TOPIC MAPPING
   - Classify user intent → predefined Topic
   - Topic carries: natural-language instructions + business policies +
     allowed Actions
   - This is a structural guardrail: agent can only invoke Actions in
     topic.allowed_actions

3. REACT LOOP (Atlas core)
   Iterate until completion or escalation:

   a. REASON
      - Constellation router selects an LLM appropriate for this sub-task
        (GPT-5, Claude variants, or specialized models)
      - LLM generates step-by-step thinking about the problem
      - Reasoning is grounded in: Topic instructions + Data Cloud retrieval
        + prior loop iterations

   b. ACT
      - Agent selects an Action from topic.allowed_actions
      - Action types: Salesforce Flow, Apex, API, Slack/Email, MCP
      - Action input/output passes through Trust Layer (more masking,
        more grounding checks)

   c. OBSERVE
      - Result feeds back into reasoning
      - Atlas can incorporate "new context or clarifications from the
        user mid-task" rather than executing a fixed plan rigidly

   d. ITERATIVE REFINEMENT
      - Atlas evaluates LLM-generated plans through "self-reflection
        or built-in verification, fine-tuning solutions until valid
        outputs emerge"
      - On confidence drop or policy violation: ESCALATE

4. EGRESS through Einstein Trust Layer (output side)
   - Hallucination detection: flag claims not grounded in retrieved data
   - Toxicity check on output
   - PII unmasking: restore real values for the legitimate recipient
     (the LLM never saw raw PII; user does see real values)
   - Audit log written to Command Center

5. ESCALATE (when triggered)
   - Automatic "transfer to human" fallback action
   - Salesforce Service Cloud agent receives full context
   - Audit trail preserved
```

## What this loop captures structurally

**Strengths** vs framework-built agents:

1. **Topic-bounded action sets** are the strongest documented
   shipped-by-default guardrail in any agent vendor in this
   comparison. The structural property — *the agent literally cannot
   invoke an Action not in topic.allowed_actions* — is configuration-
   enforced, not code-enforced. This is much harder to bypass than a
   code allowlist a developer might forget to add to.

2. **Multi-model constellation routing** means no single LLM is a
   single point of failure. Atlas can route around a degraded model
   provider similar to Sierra's failover.

3. **PII masking pre-LLM** is architecturally strong. The LLM never
   sees raw sensitive data; the buyer doesn't have to trust the LLM
   provider's logging policy because the data is masked at the
   Salesforce boundary.

4. **Iterative refinement** with self-reflection is built-in, not
   developer-implemented.

5. **'Transfer to human' is a first-class fallback** triggered by
   confidence or policy — not a code path the developer has to
   build.

## What this loop does NOT show

**Gaps** in public material:

- **Step / iteration ceiling** — Atlas's hard upper bound on ReAct
  iterations is not publicly documented. Implied by "iterative
  refinement... until valid outputs emerge" but not specified.
- **Loop / semantic loop detection** — not documented; presumably
  relies on iteration count.
- **Token / cost budget per run** — Flex Credits pricing makes per-
  Action cost visible, but per-conversation step cap is not
  documented.
- **Source code visibility** — Atlas is proprietary; buyer cannot
  audit the loop implementation.
- **Per-step trace schema** — Command Center shows traces but the
  underlying event schema is not publicly documented.

## Where it differs structurally from peers

| Concern | Anthropic SDK | OpenAI SDK | LangGraph | **Atlas (Agentforce)** |
|---------|---------------|------------|-----------|------------------------|
| Tool selection bounded by | Code-level allowed_tools | Code-level tool registry | Code-level tools array | **Configuration-level Topic** |
| Validation before tool call | PreToolUse hook | Input guardrail | Pydantic in tool | **Trust Layer + Topic policy** |
| Step ceiling | Configurable max_turns | max_turns (default 10) | recursion_limit (default 25) | **Internal, not configurable by buyer** |
| Multi-LLM routing | Developer chooses | Developer chooses | Developer chooses | **Atlas chooses (constellation)** |
| Approval / escalation | InputGuardrail tripwire | Tool-choice + guardrail | interrupt_before | **Salesforce Approval Process + auto-escalate** |
| Code-level inspection | Open source SDK | Open source SDK | Open source library | **Closed proprietary** |

The **structural difference** is that Agentforce treats agent behavior
as Salesforce metadata (Topics, Actions, Policies), not as code. This
has trade-offs:

- **Pro:** more auditable for compliance-heavy industries, follows
  Salesforce's mature change-management patterns
- **Pro:** less developer skill required (Salesforce admins can
  configure)
- **Con:** less flexible than code-defined agents
- **Con:** less buyer-visible into the actual runtime behavior

## Procurement assessment

For a procurement buyer evaluating Agentforce on the agentic-AI
rubric:

- The loop is **well-described architecturally** but proprietary
- Topic-bounded actions are a **genuine structural advantage**
- Lack of public step/cost ceiling documentation is a **real gap**
- The buyer is trading **runtime visibility for managed safety** —
  worth it for some, not for others
