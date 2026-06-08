"""Markdown report renderer.

Designed to be readable on its own (no HTML mixed in), so the markdown
file is portable to Notion, GitHub, Confluence, or a PDF export. The
web UI wraps this with a one-time "how to read" intro panel; everything
else lives here.
"""
from __future__ import annotations

from .analyzer import AnalysisResult, QuestionScore
from .artifacts import Taxonomy
from .compare import Comparison, QuestionComparison
from .rubric import Rubric


CATEGORY_PLAIN_ENGLISH = {
    "tool_call_correctness": "Does the agent invoke the right tools, the right way?",
    "loop_termination": "Can the agent get stuck or burn through money?",
    "state_coherence": "Does the agent stay consistent across a long run?",
}


def _score_chip(score: int | float) -> str:
    """Render an inline HTML chip for a score (1-5). Markdown processors pass
    inline HTML through, so this renders as a styled pill in the UI and as
    readable text in raw markdown."""
    bucket = max(1, min(5, round(score)))
    label = f"{score:.1f}" if isinstance(score, float) else f"{score} / 5"
    return f'<span class="score-chip score-chip-{bucket}">{label}</span>'


def _score_bar(score: int) -> str:
    """A small inline bar that fills to score/5. Use alongside the chip in tables."""
    pct = int(round(score / 5 * 100))
    return f'<span class="score-bar score-bar-{score}"><span style="width:{pct}%"></span></span>'


def _confidence_badge(confidence: str) -> str:
    return {
        "high": "_high confidence_",
        "medium": "_medium confidence_",
        "low": "_low confidence_",
    }.get(confidence, "")


def _score_label(score: int) -> str:
    """Plain-English label so a novice doesn't have to map 1-5 in their head."""
    return {
        1: "Critical gap",
        2: "Major gap",
        3: "Acceptable, with mitigations",
        4: "Strong",
        5: "Fully implemented",
    }.get(score, "")


def _verdict_pill(weighted: float) -> str:
    """Inline HTML pill for the executive summary verdict label."""
    if weighted >= 4.5:
        cls, label = "exec-verdict-strong", "Strong fit"
    elif weighted >= 3.5:
        cls, label = "exec-verdict-ok", "Acceptable with mitigations"
    elif weighted >= 2.5:
        cls, label = "exec-verdict-concerns", "Material concerns"
    else:
        cls, label = "exec-verdict-no", "Not recommended"
    return f'<span class="exec-verdict {cls}">{label}</span>'


def _scope_section() -> list[str]:
    """Section that runs between the Verdict and 'At a glance' on every report.
    Tells the reader what the rubric measures, what it doesn't, and where it
    fits in a real procurement decision. The honest framing makes the rest of
    the report more credible — and prevents the score from being misread as
    a final answer when it's only one input."""
    return [
        "## Scope of this evaluation",
        "",
        "This rubric measures **one dimension**: how procurement-ready a vendor's "
        "public posture is for an agentic AI deployment. The score is useful, "
        "but it is not the whole procurement decision.",
        "",
        "### What this rubric measures",
        "",
        "- Whether the vendor's documentation describes the technical mechanisms a buyer needs to verify (validation layers, step ceilings, audit logs, evaluation methodology, failure modes).",
        "- Whether evidence is **concrete** (source code, published quantitative results, verbatim policy language) or **abstract** (architectural prose without measurements).",
        "- Where the vendor's public posture has gaps a buyer will need to close under NDA before signing.",
        "",
        "### What this rubric does NOT measure",
        "",
        "- **Business fit.** Whether this vendor's product category matches the buyer's actual use case.",
        "- **Time-to-value.** A managed product can deploy in weeks; building equivalent on a framework can take 6–12 months.",
        "- **Team capability fit.** Some vendors require Python developers, some require platform admins, some require no-code users.",
        "- **Integration depth.** A vendor that scores well here may fail because it doesn't integrate with the buyer's existing systems.",
        "- **Vendor lock-in / portability.** Frameworks give maximum portability; enterprise platforms can lock in tightly.",
        "- **Total cost of ownership at scale.** Token-based, outcome-based, license-based, and per-action pricing models all have different cost curves.",
        "- **Vertical certifications.** FedRAMP, FDA SaMD, FINRA, and other regulatory bars are not in this rubric.",
        "- **Build-vs-buy economics.** This depends on the buyer's team and budget, not on vendor characteristics.",
        "",
        "### How to use this score",
        "",
        "A sound procurement decision is three layers:",
        "",
        "1. **Business-fit screen** — what's the use case, team capability, integration profile, regulatory bar, time-to-value tolerance?",
        "2. **Category selection** — build with a framework / foundation model + SDK / buy a managed product / extend an enterprise platform / pick a vertical specialist?",
        "3. **Vendor due diligence within the chosen category** — *this is the layer this report addresses*.",
        "",
        "This report is the right tool for comparing vendors **within the same category** "
        "(e.g., managed customer-experience agents like Sierra vs Decagon vs Cresta; or "
        "foundation-model + SDK choices like Anthropic vs OpenAI). It is **not** the right "
        "tool for choosing between fundamentally different categories — those decisions "
        "belong to Layers 1 and 2.",
        "",
        "If you have completed Layers 1–2 and this vendor is a candidate within the right "
        "category, the score below is meaningful. If you have not, complete those layers "
        "first before relying on this score alone.",
        "",
    ]


def _verdict_block(weighted: float) -> list[str]:
    """Plain-English verdict in 2-3 sentences plus recommended next action."""
    if weighted >= 4.5:
        return [
            "**Strong fit.** This vendor's documentation matches or exceeds what we'd expect from a production-ready agentic AI platform. Few gaps are unresolved.",
            "",
            "**Recommended next step.** Negotiate contract terms (DPA, model-change notice, exit/portability), verify the few remaining gaps listed below, and proceed to a paid pilot.",
        ]
    if weighted >= 3.5:
        return [
            "**Acceptable with mitigations.** The vendor is broadly capable but has notable gaps that should be resolved before contract signing.",
            "",
            "**Recommended next step.** Take the items in *Top concerns* and *What to do next* below back to the vendor. Require contractual or documented remediation. Do not skip a structured pilot.",
        ]
    if weighted >= 2.5:
        return [
            "**Material concerns.** The vendor has significant gaps across multiple risk categories. Proceeding without remediation is not advised.",
            "",
            "**Recommended next step.** Use the *Top concerns* list below as a discussion agenda with the vendor. Consider parallel evaluation of an alternative vendor. If proceeding, structure the engagement as a time-boxed pilot with explicit exit terms.",
        ]
    return [
        "**Not recommended.** Critical capabilities are missing or undisclosed. The risk of deploying this vendor in any consequential workflow is high.",
        "",
        "**Recommended next step.** Do not proceed without fundamental remediation. Look at alternative vendors who can answer the questions in this rubric.",
    ]


def _top_n(scores: list[QuestionScore], n: int, ascending: bool) -> list[QuestionScore]:
    return sorted(scores, key=lambda s: (s.score, s.question_id), reverse=not ascending)[:n]


def _question_summary(s: QuestionScore, rubric: Rubric) -> str:
    """One-line summary of a question score for the at-a-glance section."""
    q = next((q for q in rubric.questions if q.id == s.question_id), None)
    q_text = q.question if q else s.question_id
    # Try to give a one-liner from reasoning; fall back to the question text.
    reasoning = (s.reasoning or "").strip()
    if reasoning:
        first_sentence = reasoning.split(". ")[0].strip()
        if not first_sentence.endswith("."):
            first_sentence += "."
        return first_sentence
    return q_text


def _at_a_glance(result: AnalysisResult, rubric: Rubric) -> list[str]:
    lows = _top_n(result.scores, 3, ascending=True)
    highs = _top_n(result.scores, 3, ascending=False)
    out: list[str] = []
    out.append("## At a glance")
    out.append("")
    out.append("The three most pressing concerns and the three strongest signals from this evaluation. Use these as the agenda for your next vendor conversation.")
    out.append("")
    out.append("### Top concerns (lowest scores)")
    out.append("")
    if not lows:
        out.append("_No scored questions._")
    else:
        for s in lows:
            out.append(f"- **{s.question_id} · {s.score}/5 — {_score_label(s.score)}.** {_question_summary(s, rubric)}")
    out.append("")
    out.append("### Top strengths (highest scores)")
    out.append("")
    if not highs:
        out.append("_No scored questions._")
    else:
        for s in highs:
            out.append(f"- **{s.question_id} · {s.score}/5 — {_score_label(s.score)}.** {_question_summary(s, rubric)}")
    out.append("")
    return out


def _what_to_do_next(result: AnalysisResult, rubric: Rubric) -> list[str]:
    weighted = result.weighted_overall(rubric)
    lows = _top_n(result.scores, 3, ascending=True)
    out: list[str] = []
    out.append("## What to do next")
    out.append("")

    if weighted >= 4.5:
        out.append("This vendor passed most of the rubric. Your remaining work is contractual and verification, not technical.")
    elif weighted >= 3.5:
        out.append("This vendor is workable but needs concrete remediation on a few questions before you sign.")
    elif weighted >= 2.5:
        out.append("This vendor has material gaps. Use the asks below as a structured conversation with them — but actively evaluate alternatives in parallel.")
    else:
        out.append("This vendor is not ready. The asks below are a baseline; do not commit until they're answered.")
    out.append("")

    # Concrete asks tied to the lowest 3 scores.
    out.append("### Three concrete things to take back to the vendor")
    out.append("")
    if not lows:
        out.append("_No scored questions._")
    else:
        for i, s in enumerate(lows, start=1):
            q = next((q for q in rubric.questions if q.id == s.question_id), None)
            if q is None:
                continue
            gap = (s.gaps or "").strip()
            ask = f"**Ask about {q.id}.** Original question: \"_{q.question}_\". "
            if gap and gap.lower() not in {"none", "none notable", "n/a"}:
                ask += f"What you're missing: {gap}"
            else:
                ask += "Request concrete evidence (trace, doc, or code) addressing the optimal-answer points."
            out.append(f"{i}. {ask}")
    out.append("")

    # Required artifact gaps.
    req_missing = result.required_missing()
    if req_missing:
        out.append("### Required artifacts you didn't receive")
        out.append("")
        out.append("These are the foundational documents most enterprise buyers expect. Ask the vendor for them before proceeding:")
        out.append("")
        for c in req_missing:
            out.append(f"- **{c.slot_name}** — request from the vendor.")
        out.append("")

    return out


def _glossary() -> list[str]:
    """A small glossary of agentic-AI terms for a novice reader. Lives at the end
    of the report so it's appendix-style — useful if you need it, easy to skip."""
    out: list[str] = []
    out.append("## Glossary")
    out.append("")
    out.append("Quick definitions for terms used in this report. Skip if you already know them.")
    out.append("")
    items = [
        ("Agent", "An AI system that can take actions (call tools, run code, send messages), not just answer questions in chat."),
        ("Agent loop", "The repeating cycle of: plan → call a tool → read the result → decide the next action. Most production agents are loops, not one-shot calls."),
        ("Tool / function call", "When the agent calls a piece of code or a service — e.g. \"look up an order\", \"issue a refund\", \"send an email\". Each tool has typed arguments."),
        ("Tool schema", "The contract that defines each tool: its name, arguments, allowed values, and whether it has real-world side effects (destructive)."),
        ("Hallucination", "When the agent invents a fact or a tool argument that isn't grounded in the evidence — e.g. claims it confirmed an address that was never confirmed."),
        ("Loop (runaway)", "When the agent gets stuck in a repeating cycle — calling the same tool, or paraphrasing the same question — without making progress. Burns tokens and money."),
        ("Step budget", "A hard ceiling on how many actions the agent can take in one run. If reached, the agent stops gracefully and (ideally) escalates."),
        ("Token budget / cost cap", "A hard ceiling on the number of language-model tokens (or dollars) a run can consume. Prevents cost explosions from runaway loops."),
        ("Checkpoint", "A snapshot of the agent's state (known facts, decisions made, open tasks) saved at each step. Lets you inspect what the agent \"knew\" mid-run and replay if needed."),
        ("State coherence", "Whether the agent stays consistent over a long run — remembers facts established earlier, doesn't contradict itself, doesn't act on hallucinated facts."),
        ("Contradiction detection", "Logic that flags when a decision the agent makes contradicts a fact it established earlier (e.g. step 2: \"user is high-risk\"; step 7: refund issued anyway)."),
        ("Idempotency", "Property that running the same action twice produces the same result. Prevents double-charges if a network retry happens."),
        ("Dry-run / simulation mode", "A way to ask \"what would the agent do?\" without actually doing it. Critical for high-risk operations."),
        ("Approval gate", "A point in the agent's flow where a human must approve before a destructive action runs (refund, account closure, etc.)."),
        ("Red-team / adversarial testing", "Deliberately trying to break the agent — prompt injection, contradictory instructions, hallucinated tool params — to find vulnerabilities before attackers do."),
    ]
    for term, defn in items:
        out.append(f"- **{term}** — {defn}")
    out.append("")
    return out


def render_markdown(result: AnalysisResult, rubric: Rubric, taxonomy: Taxonomy | None = None) -> str:
    out: list[str] = []

    # --- Header --------------------------------------------------------------
    out.append(f"# Procurement Evaluation — {result.vendor_name}")
    out.append("")
    out.append(f"_Analyzed {result.analyzed_at_utc} · Rubric: {result.rubric_name} v{result.rubric_version} · Model: {result.model}_")
    out.append("")

    # --- Verdict -------------------------------------------------------------
    weighted = result.weighted_overall(rubric)
    out.append("## Verdict")
    out.append("")
    out.append(f"**Weighted overall: {weighted:.2f} / 5.0**  ·  {_verdict_pill(weighted)}")
    out.append("")
    out.extend(_verdict_block(weighted))
    out.append("")

    # --- Scope of this evaluation -------------------------------------------
    # Explicit framing of what the rubric measures and doesn't, so the score
    # below isn't misread as a final procurement answer. Appears on every report.
    out.extend(_scope_section())

    # --- At a glance (top strengths / concerns) ------------------------------
    out.extend(_at_a_glance(result, rubric))

    # --- Artifact coverage ---------------------------------------------------
    out.append("## Artifact coverage")
    out.append("")
    provided = result.provided()
    req_missing = result.required_missing()
    opt_missing = result.optional_missing()
    out.append(f"**{len(provided)} of {len(result.coverage)} expected artifact slots filled.**")
    out.append("")
    if req_missing:
        names = ", ".join(f"`{c.slot_name}`" for c in req_missing)
        out.append(f"⚠ **Required artifacts missing:** {names}. Scores for related questions are based on partial evidence — see *What to do next* below.")
        out.append("")
    if opt_missing:
        names = ", ".join(f"`{c.slot_name}`" for c in opt_missing)
        out.append(f"Optional artifacts not provided: {names}.")
        out.append("")
    out.append("| Slot | Status | File |")
    out.append("|------|--------|------|")
    for c in result.coverage:
        if c.filename:
            status = "✓ provided"
            file_cell = f"`{c.filename}`"
        elif c.required:
            status = "⚠ required, missing"
            file_cell = "—"
        else:
            status = "○ optional, missing"
            file_cell = "—"
        out.append(f"| {c.slot_name} | {status} | {file_cell} |")
    out.append("")

    # --- Scorecard -----------------------------------------------------------
    out.append("## Scorecard by category")
    out.append("")
    out.append("Each row is a category from the rubric. The score is the average across the 5 questions in that category.")
    out.append("")
    out.append("| Category | What it measures | Avg score |")
    out.append("|----------|------------------|-----------|")
    for cat in rubric.categories:
        avg = result.category_average(rubric, cat.id)
        plain = CATEGORY_PLAIN_ENGLISH.get(cat.id, "")
        out.append(f"| **{cat.name}** | {plain} | {_score_chip(avg)} |")
    out.append(f"| **Weighted overall** | — | {_score_chip(weighted)} |")
    out.append("")

    # --- Overall observations -----------------------------------------------
    out.append("## Overall observations")
    out.append("")
    out.append(result.overall_observations)
    out.append("")

    # --- Per-category detail -------------------------------------------------
    scores_by_id = {s.question_id: s for s in result.scores}
    for cat in rubric.categories:
        out.append(f"## {cat.name}")
        out.append("")
        plain = CATEGORY_PLAIN_ENGLISH.get(cat.id, "")
        if plain:
            out.append(f"**What this category measures.** {plain}")
            out.append("")
        if cat.risk:
            out.append(f"**Why it matters.** {cat.risk}")
            out.append("")

        for q in rubric.questions_for(cat.id):
            s = scores_by_id.get(q.id)
            if s is None:
                out.append(f"### {q.id}: {q.question}")
                out.append("_No score returned for this question._")
                out.append("")
                continue
            out.append(f"### {q.id}: {q.question}")
            out.append("")
            out.append(f"{_score_chip(s.score)} **{_score_label(s.score)}** &nbsp;·&nbsp; {_confidence_badge(s.confidence)}")
            out.append("")
            out.append(f"**What the analyzer found.** {s.reasoning}")
            out.append("")
            if s.evidence:
                out.append("**Evidence cited from the vendor's documents.** _Verify these verbatim against the source files before acting._")
                for e in s.evidence:
                    quote = e.quote.replace("\n", " ").strip()
                    if len(quote) > 280:
                        quote = quote[:277] + "…"
                    out.append(f"  - `{e.file}` — \"{quote}\"")
                out.append("")
            if s.gaps and s.gaps.strip().lower() not in {"none", "none notable", "n/a"}:
                out.append(f"**Gaps for buyer to verify.** {s.gaps}")
                out.append("")
        out.append("")

    # --- What to do next -----------------------------------------------------
    out.extend(_what_to_do_next(result, rubric))

    # --- Glossary ------------------------------------------------------------
    out.extend(_glossary())

    # --- Footer --------------------------------------------------------------
    out.append("---")
    out.append("")
    out.append("### Artifacts analyzed")
    out.append("")
    for a in result.artifacts:
        out.append(f"- `{a}`")
    out.append("")
    out.append("### About this report")
    out.append("")
    out.append(
        "Generated by the Procurement Analyzer. Scores are produced by a large "
        "language model against a structured rubric and are intended to "
        "accelerate, not replace, a buyer's due-diligence judgement. Always "
        "verify cited evidence against the source artifacts before acting on "
        "the verdict."
    )

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Comparison renderer
# ---------------------------------------------------------------------------

def _comparison_verdict(comp: Comparison) -> list[str]:
    out: list[str] = []
    winner = comp.winner()
    delta = comp.weighted_delta
    a, b = comp.left.vendor_name, comp.right.vendor_name
    out.append(f"**Weighted overall: {a} {comp.left_weighted:.2f} / 5.0 · {b} {comp.right_weighted:.2f} / 5.0**")
    out.append("")
    if winner == "tie":
        out.append(f"**Effective tie.** The two vendors score within 0.25 points of each other (Δ {delta:+.2f}). Decide on factors outside this rubric: pricing, fit, references, or vertical extensions.")
    elif winner == "left":
        out.append(f"**{a} scores higher overall** (+{delta:.2f}). On the strength of this evaluation alone, prefer {a} — but read the *Biggest differences* section below to confirm the gap is in areas you care about.")
    else:
        out.append(f"**{b} scores higher overall** ({delta:+.2f}). On the strength of this evaluation alone, prefer {b} — but read the *Biggest differences* section below to confirm the gap is in areas you care about.")
    out.append("")
    return out


def _comparison_scorecard(comp: Comparison) -> list[str]:
    a, b = comp.left.vendor_name, comp.right.vendor_name
    out: list[str] = []
    out.append("## Scorecard side by side")
    out.append("")
    out.append(f"Category averages and the difference (positive = {a} ahead).")
    out.append("")
    out.append(f"| Category | What it measures | {a} | {b} | Δ |")
    out.append("|----------|------------------|----|----|---|")
    for cc in comp.categories:
        plain = CATEGORY_PLAIN_ENGLISH.get(cc.category_id, "")
        out.append(f"| **{cc.category_name}** | {plain} | {_score_chip(cc.left_avg)} | {_score_chip(cc.right_avg)} | {cc.delta:+.1f} |")
    out.append(f"| **Weighted overall** | — | {_score_chip(comp.left_weighted)} | {_score_chip(comp.right_weighted)} | **{comp.weighted_delta:+.2f}** |")
    out.append("")
    return out


def _comparison_biggest_diffs(comp: Comparison, rubric: Rubric) -> list[str]:
    out: list[str] = []
    out.append("## Biggest differences (per question)")
    out.append("")
    out.append("Where the two vendors diverge most. Start here when comparing — these are the questions a procurement conversation should focus on.")
    out.append("")
    diffs = comp.biggest_differences(n=5)
    if not diffs:
        out.append("_The two vendors scored the same on every question._")
        out.append("")
        return out

    a, b = comp.left.vendor_name, comp.right.vendor_name
    for qc in diffs:
        winner_name = a if qc.delta > 0 else b
        out.append(f"### {qc.question_id}: {qc.question}")
        out.append("")
        out.append(f"**{winner_name} leads by {abs(qc.delta)} points.** {a}: {qc.left_score}/5  ·  {b}: {qc.right_score}/5")
        out.append("")
        if qc.left:
            out.append(f"**{a} ({_score_label(qc.left_score)}).** {qc.left.reasoning}")
            out.append("")
        if qc.right:
            out.append(f"**{b} ({_score_label(qc.right_score)}).** {qc.right.reasoning}")
            out.append("")
    return out


def _comparison_full_breakdown(comp: Comparison, rubric: Rubric) -> list[str]:
    out: list[str] = []
    a, b = comp.left.vendor_name, comp.right.vendor_name
    for cat in rubric.categories:
        out.append(f"## {cat.name}")
        out.append("")
        plain = CATEGORY_PLAIN_ENGLISH.get(cat.id, "")
        if plain:
            out.append(f"**What this category measures.** {plain}")
            out.append("")
        if cat.risk:
            out.append(f"**Why it matters.** {cat.risk}")
            out.append("")

        # Mini category scorecard
        cc = next(c for c in comp.categories if c.category_id == cat.id)
        out.append(f"_Category average — {a}: **{cc.left_avg:.1f}**, {b}: **{cc.right_avg:.1f}**, Δ {cc.delta:+.1f}._")
        out.append("")

        for q in rubric.questions_for(cat.id):
            qc = next((x for x in comp.questions if x.question_id == q.id), None)
            if qc is None:
                continue
            out.append(f"### {q.id}: {q.question}")
            out.append("")
            out.append(f"| Vendor | Score | Verdict |")
            out.append(f"|--------|-------|---------|")
            out.append(f"| {a} | {_score_chip(qc.left_score)} | {_score_label(qc.left_score)} |")
            out.append(f"| {b} | {_score_chip(qc.right_score)} | {_score_label(qc.right_score)} |")
            out.append("")
            if qc.left:
                out.append(f"**{a} — what the analyzer found.** {qc.left.reasoning}")
                if qc.left.gaps and qc.left.gaps.strip().lower() not in {"none", "none notable", "n/a"}:
                    out.append("")
                    out.append(f"_Gaps to verify with {a}._ {qc.left.gaps}")
                out.append("")
            if qc.right:
                out.append(f"**{b} — what the analyzer found.** {qc.right.reasoning}")
                if qc.right.gaps and qc.right.gaps.strip().lower() not in {"none", "none notable", "n/a"}:
                    out.append("")
                    out.append(f"_Gaps to verify with {b}._ {qc.right.gaps}")
                out.append("")
        out.append("")
    return out


def render_comparison_markdown(comp: Comparison) -> str:
    """Render a two-vendor head-to-head comparison report as markdown."""
    out: list[str] = []
    rubric = comp.rubric
    a, b = comp.left.vendor_name, comp.right.vendor_name

    # Header
    out.append(f"# Vendor Comparison — {a} vs {b}")
    out.append("")
    left_date = comp.left.analyzed_at_utc
    right_date = comp.right.analyzed_at_utc
    out.append(f"_{a} analyzed {left_date}  ·  {b} analyzed {right_date}_")
    out.append(f"_Rubric: {rubric.name} v{rubric.version}_")
    out.append("")

    # Verdict
    out.append("## Verdict")
    out.append("")
    out.extend(_comparison_verdict(comp))

    # Scope — same framing as single-vendor reports, with a note about
    # the additional risk of cross-category comparison.
    out.extend(_scope_section())
    out.append("**Note on this specific comparison.** Both vendors should be in the same Layer-2 category for the comparison below to be apples-to-apples. If one vendor is a framework and the other is a managed product (or one is a foundation-model SDK and the other an enterprise platform), the score difference reflects category posture more than vendor quality. Use the per-category and per-question detail to spot when this is happening.")
    out.append("")

    # Scorecard
    out.extend(_comparison_scorecard(comp))

    # Biggest differences
    out.extend(_comparison_biggest_diffs(comp, rubric))

    # Full per-category breakdown
    out.extend(_comparison_full_breakdown(comp, rubric))

    # Glossary (same as single-vendor report)
    out.extend(_glossary())

    # Footer
    out.append("---")
    out.append("")
    out.append("### About this comparison")
    out.append("")
    out.append(
        "Generated by the Procurement Analyzer. Both vendors were scored "
        "independently against the same rubric; this report compares the "
        "scores. As with the single-vendor report, scores are produced by a "
        "large language model and should accelerate, not replace, buyer "
        "judgement. Verify cited evidence in the source documents before "
        "acting."
    )
    return "\n".join(out)

