# OpenAI Agents — Failure Modes and Mitigations

_OpenAI publishes substantial failure-mode and safety material, but
it's distributed across model-level system cards, the Preparedness
Framework, and the Agents SDK source. This document compiles the
relevant material for an agentic-AI procurement evaluation._

_Sources: openai.com/security-and-privacy/; GPT-5 System Card (Aug 2025);
Operator System Card; o1 System Card; OpenAI Preparedness Framework v2
(April 2025); src/agents/run.py and src/agents/guardrail.py in the
openai-agents-python repo._

## 1. Hallucinated tool name or argument

**Mitigation:** OpenAI's `strict: true` schema mode constrains the
model at **decode time** to produce only JSON conforming to the
function's schema. This is structurally stronger than post-hoc
validation — schema-invalid output is impossible for the model to
emit when strict is enabled.

> "Enabling `strict: true` ensures function calls reliably conform to
> schemas rather than operating on a best-effort basis. This leverages
> structured outputs functionality." — function-calling docs

Default for Responses API: schemas are normalized to strict
automatically. Chat Completions: non-strict by default.

**What this protects against:** type mismatches, missing required
fields, unexpected fields, out-of-enum values.

**What it does NOT protect against:** semantically-wrong-but-valid
arguments (correct order_id, wrong order); business-rule violations;
foreign-key existence checks. These require developer-implemented
guardrails.

## 2. Runaway loop / max-turn exhaustion

**Mitigation:** The Agents SDK enforces a hard `max_turns` parameter
in the `Runner.run()` loop. From src/agents/run.py line 1058:

```python
current_turn += 1
if max_turns is not None and current_turn > max_turns:
    _error_tracing.attach_error_to_span(...)
    max_turns_error = MaxTurnsExceeded(f"Max turns ({max_turns}) exceeded")
    ...
    raise max_turns_error
```

- **Default:** `DEFAULT_MAX_TURNS` (10 in the current SDK).
- **Configurable:** Per-run via `max_turns=N` on `Runner.run()`.
- **Enforcement:** Runtime, in the agent runner. The model cannot
  bypass.
- **On limit hit:** Raises `MaxTurnsExceeded`. The SDK supports
  `error_handlers` that can intercept and synthesize a graceful final
  output instead of crashing.

This is **stronger than LangGraph's recursion_limit** because it
includes a first-class error-handler escape mechanism.

## 3. Tool error / repeated failure

**Mitigation:** Tool errors are returned to the model as `tool`
messages; the model can replan and retry. The SDK does not impose a
bounded retry counter — the `max_turns` ceiling is the only hard
backstop on a tool-error loop.

**Gap:** No first-class "circuit breaker" on repeated tool failures
(same tool, same error, N times). This is the developer's
responsibility.

## 4. Adversarial inputs / prompt injection / abuse

**This is where OpenAI's evidence is unusually deep.**

### Red team testing (GPT-5)

From the GPT-5 System Card:

> "Red teaming work for GPT-5 comprised more than 5,000 hours of work
> from over 400 external testers and experts."

Each red-team campaign aims to:
- Contribute to a specific hypothesis related to safety
- Measure the sufficiency of safeguards in adversarial scenarios
- Provide strong quantitative comparisons to previous models

System cards have been published for: GPT-5 (Aug 2025), o1, Operator
(computer-use agent), Deep Research.

### Preparedness Framework

OpenAI operates under a formal **Preparedness Framework v2**
(April 2025) defining risk thresholds and evaluation criteria across:
- Cybersecurity
- CBRN (chemical, biological, radiological, nuclear)
- Persuasion
- Model autonomy

External red-teaming, internal red-team testing, automated
evaluations, and alignment audits are required at defined
capability thresholds before deployment.

### Tripwire guardrails in the Agents SDK

From src/agents/guardrail.py:

```python
class GuardrailFunctionOutput:
    tripwire_triggered: bool
    """Whether the tripwire was triggered. If triggered, the agent's
    execution will be halted."""
```

Input and output guardrails run **in parallel with the agent**
(fail-fast). If a guardrail's tripwire fires, the run halts and the
caller receives the partial state including the planned but
un-executed action — enabling human review.

## 5. PII / sensitive data exposure

**Documented:**

- ChatGPT Enterprise, Business, Edu, and the API do not use customer
  data to train OpenAI models by default.
- Standard DPA available for GDPR/CCPA compliance.
- Encryption in transit and at rest.

**Strict mode side note:** Per the function calling docs, "Cached
schemas don't qualify for zero data retention." Buyers under
zero-retention contracts should confirm with their account team.

## 6. Token / cost runaway

**Mitigation:** Token-based pricing means the buyer pays per token.
This is the OPPOSITE of Sierra's outcome-based model — runaway
agents cost the buyer real money.

**Buyer protections:**
- `max_turns` (runtime cap on loop)
- Per-request `max_output_tokens`
- OpenAI dashboard usage caps (org-level monthly spend limit)
- Batch API and Flex pricing for 50% discount on non-realtime workloads
- Cached input pricing (90% discount on repeated context)

The buyer bears cost-runaway risk and must use the available controls
to bound it.

## 7. State drift / contradiction over long runs

**Mitigation:** The Responses API persists conversation state
server-side, addressable by `previous_response_id`. Cross-turn memory
is preserved without the developer reconstructing context.

**Gap:** OpenAI does not publish a contradiction detector or
fact-citation requirement at the SDK level. State coherence over
long agent runs is the developer's responsibility (via guardrails or
custom tracking).

## 8. Computer-use / agentic-internet risks

OpenAI has published a dedicated **Operator System Card** for the
computer-use tool, the highest-risk tool in the lineup. This is one
of the deeper public safety analyses for agentic capabilities — it
addresses risks like:

- Phishing-page interaction
- Unintended financial actions
- Out-of-scope navigation
- CAPTCHA / fraud-detection bypass

The level of public safety transparency on computer use is
considerably higher than peers.

## Summary

OpenAI's failure-mode posture is **exceptionally well-documented
relative to other agent vendors**:

- Strict mode is a structural (not advisory) mitigation against tool
  hallucination.
- `max_turns` enforcement is shipped, with graceful-handler hooks.
- Guardrails framework is first-class (InputGuardrail / OutputGuardrail
  with tripwires).
- Red team data is quantitative and published.
- A formal Preparedness Framework governs deployment thresholds.
- Per-model system cards document specific safety analyses.

The principal **gap** is that several protections are
developer-implemented (foreign-key validation, business-rule checks,
bounded retries, contradiction detection). The framework provides the
hooks; the application code wires them up.

For a procurement buyer: **OpenAI documents more than most managed
vendors AND ships open-source code for the SDK layer.** That's the
fairer comparison this rubric will pick up.
