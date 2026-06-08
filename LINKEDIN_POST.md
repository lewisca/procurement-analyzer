# LinkedIn Post Draft

_Edit and post. Suggested image: a screenshot of the 5-vendor scorecard table from the comparison report. Suggested hashtags at the bottom._

---

I ran 5 of the most-evaluated agentic AI vendors through a 15-question procurement rubric.

Salesforce Agentforce came **last**.

Here's what that actually means — and what it doesn't.

---

**The scores:**

🥇 Anthropic Claude Agent SDK — 3.27 / 5
🥈 OpenAI Agents SDK — 3.20 / 5
🥉 LangGraph — 2.67 / 5
4. Sierra — 2.47 / 5
5. Salesforce Agentforce — 2.27 / 5

**The surprise:**

Salesforce holds the broadest enterprise compliance footprint of anyone in the set. SOC 2 Type II. ISO 27001. ISO 27018. PCI-DSS. HIPAA. FedRAMP. GDPR. It has Topic-bounded action sets that structurally prevent agents from going outside scope. It has contractual zero-data-retention with its underlying LLM partners.

And it still scored last.

How did the foundation model platforms end up on top?

---

**The pattern: public documentation depth wins.**

The rubric measures what's publicly verifiable. Anthropic publishes per-model system cards, the Responsible Scaling Policy, Frontier Red Team research with quantitative results, and the Agent SDK source on GitHub. OpenAI publishes similar depth — Preparedness Framework, system cards, "5,000 hours of work from 400+ external testers" red-team data for GPT-5.

Salesforce describes its Trust Layer architecturally but doesn't publish quantitative red-team data, doesn't expose a buyer-visible step or cost ceiling, doesn't show its Atlas Reasoning Engine source, and doesn't publish agentic-specific evaluations of the Atlas + Trust Layer composition.

The rubric correctly penalized "we ship more guardrails but won't show you" against "here's the actual code and the measurements."

For a procurement leader, "show your work" isn't a bias. It's a requirement.

---

**But here's the part that matters more:**

This rubric measures ONE dimension: how procurement-ready a vendor's public posture is. **It does not tell you which vendor to pick.**

These 5 vendors aren't substitutes. They solve fundamentally different business problems:

▸ **LangGraph** — Build it yourself with full developer control. For tech-mature teams that want flexibility and zero vendor lock-in.

▸ **Anthropic Agent SDK** — Build with shipped safety primitives. For tech teams that want production tooling without operating sandbox infra.

▸ **OpenAI Agents SDK** — Same archetype as Anthropic. Different model preference. Azure-centric distribution.

▸ **Sierra** — Don't have engineers? Get a working customer experience agent in 6 weeks. For non-technical buyers.

▸ **Salesforce Agentforce** — Extend our existing Salesforce CRM with AI agents, on our existing data. For Salesforce customers and regulated industries (FedRAMP).

A procurement leader asking "should I pick Anthropic or Salesforce?" is asking the wrong question. They aren't substitutes.

---

**The right procurement workflow has three layers:**

🔹 **Layer 1 — Business-fit screen.** What's the use case? Team capability? Integration profile? Regulatory bar? Time-to-value tolerance?

🔹 **Layer 2 — Category selection.** Build with a framework? Foundation model + SDK? Buy a managed product? Extend an enterprise platform? Pick a vertical specialist?

🔹 **Layer 3 — Vendor due diligence within the chosen category** ← *this is where the rubric plays.*

The rubric is the right tool for "we've narrowed to managed CX agents — compare Sierra vs Decagon vs Cresta" — not for "should we build on LangGraph or buy Salesforce?"

---

**What the rubric doesn't measure:**

❌ Time-to-value (Sierra: 6 weeks; LangGraph: 6 months)
❌ Team capability fit (Salesforce admins vs Python developers)
❌ Integration depth with existing systems
❌ Vendor lock-in / portability
❌ Total cost of ownership at scale
❌ Vertical certifications (FedRAMP, FDA SaMD, FINRA)
❌ Build-vs-buy economics

A 3.27 vs 2.27 spread is interesting. But it's one dimension. The full decision needs more.

---

**The honest takeaway:**

Public documentation depth correlates with procurement-readiness more than enterprise compliance breadth does. Salesforce's FedRAMP doesn't matter if the procurement team can't verify how the agent itself behaves.

But you also can't pick a vendor on this rubric alone. It tells you what's verifiable about the vendor's posture. It doesn't tell you whether the vendor fits the problem you're actually solving.

---

**What I built:**

A free tool that runs any agentic AI vendor's public documentation through the rubric and produces a structured report with verbatim evidence citations. The rubric is editable YAML. The methodology is open. You can drop in any vendor's public docs and get the same kind of analysis.

Repo (MIT-licensed): **https://github.com/lewisca/procurement-analyzer**

Sample reports for all five vendors above are in `examples/`. Methodology and rubric are in the YAML files — fully open for critique.

I'd love feedback from procurement and IT leaders evaluating agentic AI right now. Three specific asks:

1. Which rubric questions am I missing?
2. Which vendor archetypes should I add to the comparison? (Healthcare? Legal? Coding agents?)
3. What Layer 1 questions should the tool ask BEFORE the rubric runs?

If you're evaluating an agentic AI vendor and want to see what the rubric surfaces about them, send me a DM. Happy to run yours.

---

#AgenticAI #Procurement #EnterpriseAI #AIVendorEvaluation #LLM #AIAgents #DueDiligence #BuyerDueDiligence

---

## Notes for posting

- **Best time to post (LinkedIn for technical audience):** Tuesday-Thursday, 8-10am ET or 12-2pm ET
- **Add an image:** screenshot the scorecard table from the comparison report — visual hook gets ~30% more engagement than text-only
- **First-comment strategy:** add a follow-up comment with a link to the tool / repo within 5 minutes of posting (LinkedIn deprioritizes posts that start with external links, but comments are fine)
- **Engage with replies for the first 60 minutes** — LinkedIn's algorithm heavily favors early engagement
- **Tag thoughtfully:** if you know any procurement leaders or AI-buying decision-makers, tag 1-2 max (more looks spammy)
- **If you want to A/B test:** post a shorter version (300 words) on Twitter/X with a thread, and the long form here

## Suggested cuts if you want to shorten

If the post is too long for your audience, the safe cuts are:

- The "What the rubric doesn't measure" bullet list (the previous paragraph already covers this)
- The "Notes for posting" section above (don't include in actual post)
- One of the two "vendor archetype" lists (keep one)

Target length if cutting: 600-700 words. Current draft: ~750 words.
