"""Core analyzer. Reads a vendor folder, scores it against the rubric using
the Claude API, returns structured results."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

from anthropic import Anthropic

from .artifacts import ArtifactSlot, Taxonomy, load_taxonomy
from .rubric import Rubric, Question


try:
    from pypdf import PdfReader  # type: ignore
    _HAS_PYPDF = True
except ImportError:
    _HAS_PYPDF = False


MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 16000


@dataclass
class Evidence:
    file: str
    quote: str


@dataclass
class QuestionScore:
    question_id: str
    score: int  # 1-5
    confidence: str  # "high" | "medium" | "low"
    evidence: list[Evidence]
    reasoning: str
    gaps: str


@dataclass
class CoverageEntry:
    slot_id: str
    slot_name: str
    required: bool
    filename: str | None  # None if no file was matched to this slot
    detected_from: str | None = None  # filename heuristic or None if not provided

    @property
    def status(self) -> str:
        if self.filename:
            return "provided"
        return "missing_required" if self.required else "missing_optional"


@dataclass
class AnalysisResult:
    vendor_name: str
    vendor_path: str
    rubric_name: str
    rubric_version: int
    model: str
    analyzed_at_utc: str
    artifacts: list[str]
    coverage: list[CoverageEntry]
    scores: list[QuestionScore]
    overall_observations: str

    def required_missing(self) -> list[CoverageEntry]:
        return [c for c in self.coverage if c.status == "missing_required"]

    def optional_missing(self) -> list[CoverageEntry]:
        return [c for c in self.coverage if c.status == "missing_optional"]

    def provided(self) -> list[CoverageEntry]:
        return [c for c in self.coverage if c.status == "provided"]

    def category_average(self, rubric: Rubric, category_id: str) -> float:
        qids = {q.id for q in rubric.questions_for(category_id)}
        scores = [s.score for s in self.scores if s.question_id in qids]
        return sum(scores) / len(scores) if scores else 0.0

    def weighted_overall(self, rubric: Rubric) -> float:
        cat_avgs = []
        weights = []
        for cat in rubric.categories:
            cat_avgs.append(self.category_average(rubric, cat.id))
            weights.append(cat.weight)
        total_w = sum(weights)
        return sum(a * w for a, w in zip(cat_avgs, weights)) / total_w if total_w else 0.0

    def to_json(self) -> str:
        d = asdict(self)
        return json.dumps(d, indent=2)

    @classmethod
    def from_json(cls, text: str) -> "AnalysisResult":
        d = json.loads(text)
        scores = [
            QuestionScore(
                question_id=s["question_id"],
                score=int(s["score"]),
                confidence=s.get("confidence", "low"),
                evidence=[Evidence(file=e.get("file", ""), quote=e.get("quote", "")) for e in s.get("evidence", [])],
                reasoning=s.get("reasoning", ""),
                gaps=s.get("gaps", ""),
            )
            for s in d.get("scores", [])
        ]
        coverage = [
            CoverageEntry(
                slot_id=c["slot_id"],
                slot_name=c["slot_name"],
                required=c["required"],
                filename=c.get("filename"),
                detected_from=c.get("detected_from"),
            )
            for c in d.get("coverage", [])
        ]
        return cls(
            vendor_name=d["vendor_name"],
            vendor_path=d.get("vendor_path", ""),
            rubric_name=d.get("rubric_name", ""),
            rubric_version=d.get("rubric_version", 0),
            model=d.get("model", ""),
            analyzed_at_utc=d.get("analyzed_at_utc", ""),
            artifacts=d.get("artifacts", []),
            coverage=coverage,
            scores=scores,
            overall_observations=d.get("overall_observations", ""),
        )


# --- Artifact loading -------------------------------------------------------

TEXT_SUFFIXES = {
    ".md", ".markdown", ".json", ".ndjson", ".txt",
    ".yaml", ".yml", ".mmd",
    ".py", ".ts", ".js", ".go", ".java", ".rb",
}
IMAGE_SUFFIXES = {".png", ".svg", ".jpg", ".jpeg"}


def _extract_pdf_text(path: Path) -> str:
    """Best-effort PDF text extraction. Falls back gracefully if pypdf
    is missing or the PDF is scanned (no text layer)."""
    if not _HAS_PYPDF:
        return ""
    try:
        reader = PdfReader(str(path))
        parts = []
        for i, page in enumerate(reader.pages):
            try:
                txt = page.extract_text() or ""
            except Exception:  # noqa: BLE001 — pypdf raises a variety
                txt = ""
            if txt.strip():
                parts.append(f"--- page {i+1} ---\n{txt}")
        return "\n\n".join(parts)
    except Exception as exc:  # noqa: BLE001
        print(f"  Note: PDF extraction failed for {path.name}: {exc}")
        return ""


def load_artifacts(vendor_path: Path, taxonomy: Taxonomy) -> dict[str, str]:
    """Read every supported file in the vendor folder. Suffixes come from the
    artifact taxonomy so the analyzer and UI stay aligned.
    Returns {filename: text}. PDFs are text-extracted via pypdf. Images
    (PNG/SVG/JPG) are noted but not analyzed."""
    accepted = taxonomy.accepted_suffixes
    artifacts: dict[str, str] = {}
    image_only: list[str] = []
    pdf_no_text: list[str] = []
    for p in sorted(vendor_path.iterdir()):
        if not p.is_file():
            continue
        if p.name.startswith(("~$", ".")):  # Office lock / dotfiles
            continue
        suffix = p.suffix.lower()
        if suffix not in accepted:
            continue
        if suffix in TEXT_SUFFIXES:
            try:
                artifacts[p.name] = p.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                print(f"  Note: skipped {p.name} (not valid UTF-8: {exc})")
        elif suffix == ".pdf":
            text = _extract_pdf_text(p)
            if text:
                artifacts[p.name] = text
            else:
                pdf_no_text.append(p.name)
        elif suffix in IMAGE_SUFFIXES:
            image_only.append(p.name)

    if image_only:
        print(f"  Note: image artifacts present but not analyzed (user review needed): {', '.join(image_only)}")
    if pdf_no_text:
        if not _HAS_PYPDF:
            print(f"  Note: PDFs present but pypdf is not installed; skipped: {', '.join(pdf_no_text)}")
        else:
            print(f"  Note: PDFs had no extractable text layer (likely scanned); skipped: {', '.join(pdf_no_text)}")
    if not artifacts:
        raise SystemExit(f"No readable artifacts found in {vendor_path}")
    return artifacts


def compute_coverage(taxonomy: Taxonomy, artifact_filenames: list[str]) -> list[CoverageEntry]:
    """Match each loaded filename to a taxonomy slot and emit a coverage row
    per slot. A slot can be filled by 0 or 1 files; if multiple files match
    the same slot, the first match wins and the rest are flagged."""
    matched: dict[str, str] = {}  # slot_id -> filename
    for fname in artifact_filenames:
        slot = taxonomy.match_slot(fname)
        if slot is None:
            continue
        if slot.id in matched:
            print(f"  Note: {fname} also looks like '{slot.id}'; using {matched[slot.id]} for that slot.")
            continue
        matched[slot.id] = fname

    coverage: list[CoverageEntry] = []
    for slot in taxonomy.slots:
        if slot.ignored_by_analyzer:
            continue
        fname = matched.get(slot.id)
        coverage.append(
            CoverageEntry(
                slot_id=slot.id,
                slot_name=slot.name,
                required=slot.required,
                filename=fname,
                detected_from="filename_match" if fname else None,
            )
        )
    return coverage


# --- Prompt construction ----------------------------------------------------

def _artifacts_block(artifacts: dict[str, str]) -> str:
    parts = []
    for fname, content in artifacts.items():
        parts.append(f"=== FILE: {fname} ===\n{content}")
    return "\n\n".join(parts)


def _question_block(rubric: Rubric) -> str:
    parts = []
    for cat in rubric.categories:
        parts.append(f"## Category: {cat.name} (id={cat.id})")
        parts.append(f"Risk: {cat.risk}")
        for q in rubric.questions_for(cat.id):
            parts.append(f"\n### Question {q.id}: {q.question}")
            parts.append("Optimal answer signals:")
            for s in q.optimal_answer:
                parts.append(f"  - {s}")
            parts.append("Red flags:")
            for s in q.red_flags:
                parts.append(f"  - {s}")
            parts.append(f"Typical evidence sources: {', '.join(q.evidence_sources)}")
    return "\n".join(parts)


def _system_prompt() -> str:
    return (
        "You are an expert procurement analyst evaluating an agentic AI vendor. "
        "You produce sober, evidence-grounded assessments. You cite verbatim "
        "quotes from the vendor's artifacts when scoring. If the artifacts do "
        "not contain enough evidence to score a question, you say so honestly "
        "and lower the confidence rather than guessing.\n\n"
        "Scoring scale (1-5):\n"
        "  5 — Fully Implemented: optimal answers across the board, no red flags.\n"
        "  4 — Substantial: strong on 4 of 5 question dimensions, minor gaps.\n"
        "  3 — Partial: optimal on 2-3 dimensions, significant gaps, some red flags.\n"
        "  2 — Minimal: optimal on 1-2 dimensions, multiple red flags, vague.\n"
        "  1 — Not Addressed: not implemented, dismissive, major red flags.\n\n"
        "Output rules:\n"
        "  - You MUST call the submit_evaluation tool exactly once.\n"
        "  - Every evidence quote must be a verbatim substring of one of the "
        "    supplied artifact files. Do not paraphrase quotes.\n"
        "  - If you find a red flag, lead the reasoning with it.\n"
        "  - 'gaps' should name what's missing for the buyer to verify the answer; "
        "    write 'none notable' only when the artifacts truly answer the question.\n"
        "  - Confidence: 'high' = direct evidence in artifacts; 'medium' = inferred "
        "    with some support; 'low' = guessing because evidence is absent."
    )


def _user_prompt(rubric: Rubric, artifacts: dict[str, str], vendor_name: str) -> str:
    return (
        f"# Vendor under evaluation: {vendor_name}\n\n"
        f"# Rubric: {rubric.name}\n\n"
        f"{_question_block(rubric)}\n\n"
        "# Vendor artifacts\n\n"
        f"{_artifacts_block(artifacts)}\n\n"
        "Now score every question in the rubric. Cite verbatim evidence quotes "
        "from the files above. When evidence is absent or contradicts the optimal "
        "answer, score low and explain. Call submit_evaluation."
    )


def _eval_tool(rubric: Rubric) -> dict:
    question_ids = [q.id for q in rubric.questions]
    return {
        "name": "submit_evaluation",
        "description": (
            "Submit the structured evaluation of the vendor. Must include one "
            "score entry per rubric question, plus an overall observations field."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "scores": {
                    "type": "array",
                    "minItems": len(question_ids),
                    "maxItems": len(question_ids),
                    "items": {
                        "type": "object",
                        "properties": {
                            "question_id": {"type": "string", "enum": question_ids},
                            "score": {"type": "integer", "minimum": 1, "maximum": 5},
                            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                            "evidence": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "file": {"type": "string"},
                                        "quote": {"type": "string"},
                                    },
                                    "required": ["file", "quote"],
                                },
                            },
                            "reasoning": {"type": "string"},
                            "gaps": {"type": "string"},
                        },
                        "required": ["question_id", "score", "confidence", "evidence", "reasoning", "gaps"],
                    },
                },
                "overall_observations": {
                    "type": "string",
                    "description": "1-3 paragraph summary of the vendor's strengths, weaknesses, and notable signals.",
                },
            },
            "required": ["scores", "overall_observations"],
        },
    }


# --- Main analyze function --------------------------------------------------

def analyze(vendor_path: Path, rubric: Rubric, *, taxonomy: Taxonomy | None = None, client: Anthropic | None = None) -> AnalysisResult:
    if client is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit(
                "ANTHROPIC_API_KEY not set. Export it before running the analyzer."
            )
        client = Anthropic()
    if taxonomy is None:
        taxonomy = load_taxonomy()

    artifacts = load_artifacts(vendor_path, taxonomy)
    coverage = compute_coverage(taxonomy, list(artifacts.keys()))
    vendor_name = vendor_path.name

    provided_count = sum(1 for c in coverage if c.status == "provided")
    print(f"  Artifact coverage: {provided_count}/{len(coverage)} slots filled.")

    tool = _eval_tool(rubric)
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=_system_prompt(),
        tools=[tool],
        tool_choice={"type": "tool", "name": "submit_evaluation"},
        messages=[{"role": "user", "content": _user_prompt(rubric, artifacts, vendor_name)}],
    )

    tool_use = next((b for b in response.content if b.type == "tool_use"), None)
    if tool_use is None:
        raise RuntimeError(
            f"Model did not call submit_evaluation. Stop reason: {response.stop_reason}"
        )

    payload = tool_use.input or {}
    if response.stop_reason == "max_tokens":
        print(f"  WARNING: hit max_tokens={MAX_TOKENS}; output may be truncated.")

    raw_scores = payload.get("scores") or []
    expected_ids = [q.id for q in rubric.questions]
    seen_ids = {s.get("question_id") for s in raw_scores}
    missing_ids = [qid for qid in expected_ids if qid not in seen_ids]
    if missing_ids:
        print(f"  WARNING: model omitted scores for: {missing_ids}")

    scores = []
    for s in raw_scores:
        try:
            scores.append(QuestionScore(
                question_id=s["question_id"],
                score=int(s["score"]),
                confidence=s.get("confidence", "low"),
                evidence=[Evidence(file=e.get("file", ""), quote=e.get("quote", "")) for e in s.get("evidence", [])],
                reasoning=s.get("reasoning", ""),
                gaps=s.get("gaps", ""),
            ))
        except (KeyError, TypeError, ValueError) as exc:
            print(f"  WARNING: skipping malformed score entry: {exc!r} :: {s!r}")

    return AnalysisResult(
        vendor_name=vendor_name,
        vendor_path=str(vendor_path),
        rubric_name=rubric.name,
        rubric_version=rubric.version,
        model=MODEL,
        analyzed_at_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        artifacts=list(artifacts.keys()),
        coverage=coverage,
        scores=scores,
        overall_observations=payload.get("overall_observations", "_(observations missing — model output was truncated)_"),
    )
