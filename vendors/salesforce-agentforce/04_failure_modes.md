# Salesforce Agentforce — Failure Modes and Mitigations

_Sourced from cirra.ai's Atlas Reasoning Engine writeup, the
Einstein Trust Layer documentation, and Salesforce's published
Agentforce material._

## 1. Hallucination

**Mitigation:** Multiple layers per Salesforce's documentation:

- **Einstein Trust Layer hallucination detection** — flags outputs
  that don't ground in retrieved data
- **Iterative refinement in Atlas** — "Atlas evaluates LLM-generated
  plans through self-reflection or built-in verification, fine-tuning
  solutions until valid outputs emerge"
- **Retrieval-grounded generation** — Atlas retrieves from Salesforce
  Data Cloud before responding; reduces ungrounded generation
- **Multi-model routing** — ensemble approach uses specialized models
  for specialized sub-tasks, reducing single-model failure modes

**Gap in public evidence:** Salesforce does not publish quantitative
hallucination rate measurements. Customer-facing claims like "85% AI
resolution" are aggregate outcome metrics, not hallucination-specific.

## 2. Wrong tool / Action selection

**Mitigation: Topic-bounded action sets.** This is Salesforce's
distinctive architectural choice:

> "Atlas begins by mapping user inputs to predefined Topics. Each
> topic includes relevant natural-language instructions, business
> policies, and an allowed set of Actions. This scoping mechanism
> constrains the reasoning problem and embeds guardrails directly
> into the agent's decision-making framework."

An agent on Topic 'process_refund' literally cannot invoke
'cancel_subscription' — it's not in the topic's allowed_actions.
This is **structurally stronger** than LangGraph or OpenAI's
allowlist patterns because Topics are first-class configuration
managed in the admin UI, not buried in developer code.

## 3. Runaway loop / step exhaustion

**Mitigation:** Atlas's ReAct loop has internal step bounds, but
Salesforce does not publicly document the default or how to
configure them. The Atlas writeup describes "iterative refinement"
which implies a loop ceiling, but specifics are not public.

**Gap:** Less explicit than OpenAI's max_turns or LangGraph's
recursion_limit. Buyer-side configurability is unclear from public
material.

**Cost-runaway mitigation:** Flex Credits pricing means each Action
has a known cost ($0.10 per standard action, $0.15 per voice action).
A runaway agent costs the buyer real money (20 credits × $0.005 per
action × N actions). Per-conversation tier has a per-conversation
cap ($2/conversation).

## 4. Adversarial inputs / prompt injection / abuse

**Einstein Trust Layer mitigation** (this is Salesforce's
strongest documented layer):

- **PII masking before LLM call** — sensitive data is encrypted and
  masked before it reaches the LLM
- **Toxicity detection** — output classifier flags toxic content
- **Prompt-injection defense** — explicit detection
- **Configurable guardrails** for regulated use cases
- **Zero data retention with third-party LLM providers** — Salesforce
  contractually prevents OpenAI / Anthropic from retaining customer
  data via its bilateral agreements

**Gap:** Salesforce does not publish quantitative red-team results
(unlike OpenAI's "5,000 hours / 400 testers" or Anthropic's Frontier
Red Team publications). The Trust Layer is described
architecturally, not quantitatively.

## 5. PII and sensitive data exposure

**Strong public posture:**

- **PII masking pre-LLM** — sensitive fields are masked before the
  LLM sees them, then unmasked in the final response to the user
- **Zero data retention with LLM providers** — contractually enforced
- **Data Cloud zero-copy architecture** — customer data is retrieved
  from source systems, never duplicated in Salesforce
- **Configurable PII detection rules** per customer policy

This is **the most rigorous PII-handling architecture** of any
vendor in this comparison. The "data is retrieved, never duplicated"
claim is structurally stronger than copy-into-vendor-storage models.

## 6. Cost runaway

**Three pricing models complicate this:**

| Model | Cost-runaway risk |
|-------|-------------------|
| Per-conversation ($2) | Bounded — buyer pays a fixed per-conversation fee regardless of action count |
| Flex Credits ($0.10/action, $0.15 voice) | Scales linearly with agent action count; runaway = real cost |
| Per-user license ($125/user/month) | Mostly fixed; usage costs separate |

Buyers should be aware: under Flex Credits, a misconfigured agent
that loops can run up significant cost. Salesforce does not publish
per-conversation hard caps under Flex Credits.

## 7. State drift / context loss over long interactions

**Mitigation:** Atlas maintains conversational context within a
session. Data Cloud provides cross-session persistent context (the
customer's full history is available on every interaction).

**Gap:** Salesforce does not document contradiction detection or
fact-citation requirements at the Atlas level. Per the published
material, state coherence relies on the LLM's own consistency plus
Trust Layer hallucination flagging — not a separate contradiction
detector.

## 8. Action-execution side-effect risk

**Mitigation:** Topic policies + 'transfer to human' fallback:

> "The system includes automatic 'transfer to human' fallback actions
> when confidence drops or policy violations threaten."

Combined with Salesforce's existing Approval Process framework,
high-risk Actions can be wired to require multi-step human
authorization.

## 9. FedRAMP / regulated-industry deployment risk

**This is unique to Salesforce.** Of the vendors in this comparison,
Salesforce is the only one with **FedRAMP authorization** — meaning
Agentforce can be deployed in US federal government and high-trust
state/local agency environments where other vendors cannot.

For regulated industries (financial services, healthcare, government),
this is often the deciding compliance factor.

## Summary

Salesforce Agentforce's failure-mode posture is **architecturally
strong on data handling and Action scoping** but **less quantitative
on capability evaluation than OpenAI or Anthropic**:

| Capability | Agentforce |
|------------|-----------|
| Topic-bounded action sets | ✅ Structurally enforced |
| Einstein Trust Layer (PII, toxicity, prompt injection) | ✅ Comprehensive |
| Zero data retention with LLM providers | ✅ Contractually enforced |
| Multi-model ensemble routing | ✅ |
| FedRAMP authorization | ✅ Unique |
| Quantitative red-team data | ❌ Not published |
| Per-model system cards | ❌ N/A (uses partner models) |
| Public agent loop source code | ❌ Closed |
| Per-run step / cost cap visibility | ⚠️ Not clearly documented |

The shape: **safety through configuration and architecture**, not
through code-level inspection. Procurement should verify Topic
configurations and Trust Layer audit visibility under NDA.
