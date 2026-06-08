"""Rubric loading. The rubric is YAML — see rubric/horizontal_v1.yaml."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Question:
    id: str
    category: str
    question: str
    optimal_answer: list[str]
    red_flags: list[str]
    evidence_sources: list[str]


@dataclass
class Category:
    id: str
    name: str
    risk: str
    weight: float


@dataclass
class Rubric:
    version: int
    name: str
    scoring_scale: dict
    categories: list[Category]
    questions: list[Question]
    raw: dict  # full parsed YAML for renderer access

    def questions_for(self, category_id: str) -> list[Question]:
        return [q for q in self.questions if q.category == category_id]

    def category(self, category_id: str) -> Category:
        return next(c for c in self.categories if c.id == category_id)


def load_rubric(path: str | Path) -> Rubric:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))

    categories = [
        Category(
            id=c["id"],
            name=c["name"],
            risk=c.get("risk", "").strip(),
            weight=c.get("weight", 1.0),
        )
        for c in data["categories"]
    ]

    questions = [
        Question(
            id=q["id"],
            category=q["category"],
            question=q["question"],
            optimal_answer=q.get("optimal_answer", []),
            red_flags=q.get("red_flags", []),
            evidence_sources=q.get("evidence_sources", []),
        )
        for q in data["questions"]
    ]

    return Rubric(
        version=data["version"],
        name=data["name"],
        scoring_scale=data["scoring_scale"],
        categories=categories,
        questions=questions,
        raw=data,
    )
