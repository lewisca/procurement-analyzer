"""Side-by-side comparison of two AnalysisResult objects against the same rubric.

Computation is deterministic — no LLM call. The renderer (in report.py)
turns a Comparison into a markdown report similar in shape to the
single-vendor report, but laid out around two vendors.
"""
from __future__ import annotations

from dataclasses import dataclass

from .analyzer import AnalysisResult, QuestionScore
from .rubric import Rubric


@dataclass
class QuestionComparison:
    question_id: str
    question: str
    category_id: str
    left: QuestionScore | None
    right: QuestionScore | None

    @property
    def left_score(self) -> int:
        return self.left.score if self.left else 0

    @property
    def right_score(self) -> int:
        return self.right.score if self.right else 0

    @property
    def delta(self) -> int:
        """Positive means left vendor scores higher."""
        return self.left_score - self.right_score


@dataclass
class CategoryComparison:
    category_id: str
    category_name: str
    left_avg: float
    right_avg: float

    @property
    def delta(self) -> float:
        return self.left_avg - self.right_avg


@dataclass
class Comparison:
    left: AnalysisResult
    right: AnalysisResult
    rubric: Rubric
    categories: list[CategoryComparison]
    questions: list[QuestionComparison]

    @property
    def left_weighted(self) -> float:
        return self.left.weighted_overall(self.rubric)

    @property
    def right_weighted(self) -> float:
        return self.right.weighted_overall(self.rubric)

    @property
    def weighted_delta(self) -> float:
        return self.left_weighted - self.right_weighted

    def winner(self) -> str:
        """Returns 'left', 'right', or 'tie'."""
        if abs(self.weighted_delta) < 0.25:
            return "tie"
        return "left" if self.weighted_delta > 0 else "right"

    def biggest_differences(self, n: int = 5) -> list[QuestionComparison]:
        """Top N questions ordered by absolute delta — wherever the two
        vendors diverge most."""
        ranked = sorted(self.questions, key=lambda q: abs(q.delta), reverse=True)
        return [q for q in ranked if q.delta != 0][:n]


def compare(left: AnalysisResult, right: AnalysisResult, rubric: Rubric) -> Comparison:
    """Build a Comparison given two analyses scored against the same rubric."""
    left_by_id = {s.question_id: s for s in left.scores}
    right_by_id = {s.question_id: s for s in right.scores}

    questions: list[QuestionComparison] = []
    for q in rubric.questions:
        questions.append(
            QuestionComparison(
                question_id=q.id,
                question=q.question,
                category_id=q.category,
                left=left_by_id.get(q.id),
                right=right_by_id.get(q.id),
            )
        )

    categories: list[CategoryComparison] = []
    for cat in rubric.categories:
        categories.append(
            CategoryComparison(
                category_id=cat.id,
                category_name=cat.name,
                left_avg=left.category_average(rubric, cat.id),
                right_avg=right.category_average(rubric, cat.id),
            )
        )

    return Comparison(
        left=left,
        right=right,
        rubric=rubric,
        categories=categories,
        questions=questions,
    )
