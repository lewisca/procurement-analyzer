"""Canonical artifact taxonomy. Loaded from rubric/artifact_taxonomy.yaml.

This module is the contract between the analyzer and a future UI:
the UI iterates `taxonomy.slots` to render upload slots, and the
analyzer respects the same `formats` / `ignored_by_analyzer` rules
when reading a vendor folder.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class ArtifactSlot:
    id: str
    name: str
    formats: list[str]
    required: bool
    description: str
    ask_vendor: str
    example_filenames: list[str]
    novice_explanation: str = ""
    example_snippet: str = ""
    ignored_by_analyzer: bool = False


@dataclass
class Taxonomy:
    version: int
    name: str
    slots: list[ArtifactSlot]

    @property
    def accepted_suffixes(self) -> set[str]:
        """Union of formats across non-ignored slots — used by the analyzer
        to decide which files in a vendor folder to read."""
        suffixes: set[str] = set()
        for slot in self.slots:
            if slot.ignored_by_analyzer:
                continue
            for fmt in slot.formats:
                suffixes.add(fmt.lower())
        return suffixes

    def slot(self, slot_id: str) -> ArtifactSlot:
        return next(s for s in self.slots if s.id == slot_id)

    def match_slot(self, filename: str) -> ArtifactSlot | None:
        """Best-effort detection of which slot a vendor filename belongs to.

        Strategy: strip leading sequence numbers / trailing version qualifiers,
        then score each slot by (a) slot-id substring match, (b) example-filename
        match, (c) word overlap with slot name. Requires format compatibility.
        Returns None when no slot is a confident match.
        """
        path = Path(filename)
        stem = _normalize_stem(path.stem)
        suffix = path.suffix.lower()

        best: ArtifactSlot | None = None
        best_score = 0
        for slot in self.slots:
            if slot.ignored_by_analyzer:
                continue
            if suffix not in {f.lower() for f in slot.formats}:
                continue
            score = 0
            slot_id_norm = slot.id.lower()
            if slot_id_norm in stem or stem in slot_id_norm:
                score += 10
            for ex in slot.example_filenames:
                ex_norm = _normalize_stem(Path(ex).stem)
                if ex_norm == stem:
                    score += 8
                elif ex_norm and (ex_norm in stem or stem in ex_norm):
                    score += 4
            name_words = set(re.findall(r"\w+", slot.name.lower()))
            stem_words = set(re.findall(r"\w+", stem))
            overlap = (name_words & stem_words) - {"and", "or", "the", "a", "of", "for"}
            if overlap:
                score += 2 * len(overlap)
            if score > best_score:
                best_score = score
                best = slot
        return best if best_score >= 4 else None


_LEADING_INDEX = re.compile(r"^[\d_\-\s]+")
_TRAILING_QUALIFIER = re.compile(
    r"[_\-\s]+(sample|example|reference|v\d+|2\d{3}.*|q[1-4].*|final|draft)$"
)


def _normalize_stem(stem: str) -> str:
    s = stem.lower().strip()
    s = _LEADING_INDEX.sub("", s)
    s = _TRAILING_QUALIFIER.sub("", s)
    s = re.sub(r"\s+", "_", s)
    return s


def load_taxonomy(path: str | Path = "rubric/artifact_taxonomy.yaml") -> Taxonomy:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    slots = [
        ArtifactSlot(
            id=s["id"],
            name=s["name"],
            formats=s["formats"],
            required=s.get("required", False),
            description=s.get("description", "").strip(),
            ask_vendor=s.get("ask_vendor", "").strip(),
            example_filenames=s.get("example_filenames", []),
            novice_explanation=s.get("novice_explanation", "").strip(),
            example_snippet=s.get("example_snippet", "").rstrip(),
            ignored_by_analyzer=s.get("ignored_by_analyzer", False),
        )
        for s in data["slots"]
    ]
    return Taxonomy(version=data["version"], name=data["name"], slots=slots)
