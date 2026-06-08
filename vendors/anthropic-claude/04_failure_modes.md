# Anthropic Claude — Failure Modes and Mitigations

_Anthropic publishes substantial safety research, model cards, and a
formal Responsible Scaling Policy. This document compiles
the relevant material for procurement evaluation._

_Sources: claude.com/blog/building-agents-with-the-claude-agent-sdk;
Anthropic system cards (Opus 4.x, Sonnet 4.x); anthropic.com
Responsible Scaling Policy; trust.anthropic.com (gated);
the claude-agent-sdk-python repo source._

## 1. Hallucinated tool name or argument

**Mitigation:** Strict tool use (`strict: true` on tool definitions)
constrains Claude's decoding to schema-conforming JSON. From the docs:

> "Add `strict: true` to your tool definitions to ensure Claude's
> tool calls always match your schema exactly."

This is structurally equivalent to OpenAI's strict mode — schema
violations are impossible for the model to emit when strict is
enabled.

**Anthropic note:** Claude Opus is *more likely* than Claude Sonnet
to recognize a missing parameter and ask a clarifying question rather
than guessing. From the docs:

> "If Claude Opus doesn't have enough context to fill in the required
> parameters, it is far more likely to respond with a clarifying
> question instead of making a tool call."

This is a model-level behavior, not a SDK enforcement — but it
materially reduces the hallucinated-parameter risk for Opus.

## 2. Wrong-tool selection / replanning

**Mitigation:** The Agent SDK has lifecycle hooks that fire before
and after tool execution. Specifically:

- `PreToolUse` — runs before a tool executes; can deny, allow,
  modify args, or surface to a user
- `PostToolUse` — runs after tool execution; can validate output,
  log, or transform
- `Stop` — runs when the agent stops; can audit final state

This is **finer-grained than OpenAI's input/output guardrails** — a
PreToolUse hook can inspect a specific tool name and arguments and
make a decision, then either allow, deny, or replace the call.

## 3. Runaway loop / step exhaustion

**Mitigation:** The Agent SDK enforces step / iteration limits via
the SDK's internal turn counter. Compaction (automatic context
summarization) prevents context overflow even on long runs.

**Specifically:** "automatic context 'compaction' that summarizes
previous messages as limits approach, preventing context overflow"
(from the Anthropic engineering blog).

**Gaps vs OpenAI / LangGraph:** Public material doesn't specify a
default max_turns or how to override it in the same explicit way as
the OpenAI Agents SDK. Developer should consult the SDK reference or
session docs.

## 4. Adversarial inputs / prompt injection / abuse

**Anthropic's evidence is among the deepest in the industry.**

### Frontier Red Team and Safety Research

Anthropic operates an internal **Frontier Red Team** that publishes
research on:

- Sabotage capability evaluations
- Sleeper-agent / deceptive-alignment research
- Constitutional AI and Constitutional Classifiers
- Universal jailbreak evaluations

### Responsible Scaling Policy (RSP)

Anthropic's RSP is the published deployment-gating policy. It
defines:

- **AI Safety Levels (ASL)** — capability thresholds with required
  safety mitigations at each level
- **Required evaluations** before deploying a model at each ASL
- **Deployment safeguards** required when capabilities cross
  thresholds (CBRN uplift, autonomous replication, etc.)
- **Public reporting** when significant safety-relevant capabilities
  are observed

Procurement-relevant: Like OpenAI's Preparedness Framework, the RSP
is a verifiable deployment-gating policy. Buyers can ask: "what ASL
is this model deployed at?"

### System cards per model

Anthropic publishes a system card for each major Claude model:

- Sonnet 4.x and Opus 4.x system cards include sections on dangerous
  capability evaluations, adversarial robustness, refusal rates,
  agentic-misuse evaluations.
- Cards include before/after measurements for safety mitigations.

### Tripwire-style hooks in the SDK

While not a guardrail framework per se, the `PreToolUse` and
`UserPromptSubmit` hooks let developers implement adversarial-input
detection in code:

```python
async def block_prompt_injection(input_data, ...):
    if detect_injection_attempt(input_data["prompt"]):
        return {"decision": "deny", "reason": "potential injection"}
    return {}
```

## 5. PII and sensitive data exposure

**Documented:**

- API customer data is **not used to train Anthropic's models** by
  default (per the privacy policy).
- Standard DPA available for GDPR / CCPA compliance.
- HIPAA-ready configuration with BAA available.

**Subtle but important:** Anthropic's training-data policy is one of
the firmer in the industry. The default is no training; opt-in flows
are explicit.

## 6. Cost runaway

**Pricing model:** Token-based, like OpenAI. Buyer bears cost-runaway
risk and must use available controls.

**Buyer controls:**

- `max_tokens` per request
- Tool registry restriction (`allowed_tools` / `disallowed_tools`)
- Compaction limits the context-token cost on long runs
- Console-level usage caps
- For subscription plans: separate Agent SDK monthly credit (as of
  June 15, 2026) prevents Agent SDK usage from eating interactive
  limits

Gap: no documented per-run cost-cap primitive in the SDK itself.
Compaction reduces context cost but does not bound dollar spend per
run.

## 7. State drift / context loss over long agents

**Mitigation:** Sessions are persisted as JSONL on the developer's
filesystem (or via Anthropic-hosted event log for Managed Agents).
First-class `resume`, `fork`, `rename`, `tag`, and `delete` operations
on sessions.

**Compaction** automatically summarizes earlier messages as the
context window fills. This keeps long-running agents coherent
without manual intervention but is a heuristic — important
early-session facts can be lost if compaction is too aggressive.

**Gap:** No explicit contradiction detector or fact-citation
requirement at the SDK level. Same gap as OpenAI.

## 8. Computer-use / agentic-internet risks

Anthropic was the first major LLM vendor to ship a **computer use**
capability (Claude can take screenshots, click, and type). The
Operator-equivalent safety analysis is documented in the relevant
system cards.

The SDK's `permission_mode="plan"` is a dry-run mode where the agent
shows what it would do without executing — useful for high-risk
operations.

## Summary

Anthropic's failure-mode posture is **roughly on par with OpenAI's**
in quantitative depth (system cards, RSP) and **deeper on
SDK-level safety primitives**:

| Capability | Anthropic | OpenAI |
|------------|-----------|--------|
| Strict-mode tool validation | ✅ | ✅ |
| Lifecycle hooks (PreToolUse/PostToolUse/Stop/etc.) | ✅ **first-class** | Input/output guardrails (different shape) |
| Permission modes (default / acceptEdits / bypassPermissions / plan) | ✅ | Per-tool tool_choice + dashboard caps |
| Sessions with fork / resume / tag | ✅ | Responses API state |
| Built-in AskUserQuestion as a tool | ✅ | Human-in-the-loop is developer-implemented |
| Subagents (formal Agent tool primitive) | ✅ | Handoffs (similar but different shape) |
| Per-model system cards | ✅ | ✅ |
| Deployment-gating policy | RSP | Preparedness Framework |
| Multi-cloud distribution | AWS Bedrock, GCP Vertex, Azure Foundry | Primarily Azure |
