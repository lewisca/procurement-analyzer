# QuickBot — FAQ on Reliability

## "What if the agent makes a mistake?"

Modern LLMs are extremely reliable. In practice, our agents make the
right call >95% of the time. For the rare miss, our customers monitor
their support queues and step in if needed.

## "What if the agent gets stuck in a loop?"

Our agents are designed to not get stuck. If they do, the system stops
after the agent itself decides it's done.

## "Do you handle prompt injection?"

We use the latest models, which have prompt-injection protections built in by the providers. We haven't done specific red-team testing in-house yet but it's on our roadmap.

## "What if the agent issues the wrong refund?"

You can configure your CRM to require approval for any refund. We
recommend this for high-value transactions.

## "Does the agent contradict itself?"

We haven't seen that in practice. Agents are generally good at staying
consistent.

## "What if the agent hallucinates?"

Hallucination rates on the latest models are very low. We rely on the
model provider's improvements here.
