"""Procurement Analyzer — minimal Flask UI.

Run:
    python -m web.app                  # serves on http://127.0.0.1:5000

Needs ANTHROPIC_API_KEY in the environment.

Persistence: every analysis is auto-saved to ``runs/<slug>__<iso>.json``
so it can be re-opened or compared side-by-side later.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import markdown as md_lib
from flask import Flask, abort, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename

# Make the analyzer package importable when running `python -m web.app`.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env at the project root if present. See analyzer/env_loader.py for
# the behavior contract (override-empty, explicit-shell-wins).
from analyzer.env_loader import load_env  # noqa: E402
load_env(PROJECT_ROOT / ".env")

from analyzer.analyzer import AnalysisResult, analyze  # noqa: E402
from analyzer.artifacts import load_taxonomy  # noqa: E402
from analyzer.compare import compare  # noqa: E402
from analyzer.report import render_comparison_markdown, render_markdown  # noqa: E402
from analyzer.rubric import load_rubric  # noqa: E402


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB per request

RUBRIC = load_rubric(PROJECT_ROOT / "rubric" / "horizontal_v1.yaml")
TAXONOMY = load_taxonomy(PROJECT_ROOT / "rubric" / "artifact_taxonomy.yaml")
RUNS_DIR = PROJECT_ROOT / "runs"
RUNS_DIR.mkdir(exist_ok=True)


_RUN_FILENAME_RE = re.compile(r"^[A-Za-z0-9_\-]+__\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}\+\d{2}-\d{2}\.json$")


def _save_run(result: AnalysisResult) -> Path:
    """Persist an analysis to runs/ and return the file path."""
    slug = secure_filename(result.vendor_name) or "vendor"
    ts = result.analyzed_at_utc.replace(":", "-")
    path = RUNS_DIR / f"{slug}__{ts}.json"
    path.write_text(result.to_json(), encoding="utf-8")
    return path


def _list_runs() -> list[dict]:
    """List saved analyses, newest first."""
    rows = []
    for path in sorted(RUNS_DIR.glob("*.json"), reverse=True):
        if not _RUN_FILENAME_RE.match(path.name):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows.append(
            {
                "filename": path.name,
                "vendor_name": data.get("vendor_name", "unknown"),
                "analyzed_at_utc": data.get("analyzed_at_utc", ""),
                "model": data.get("model", ""),
                "weighted_overall": _quick_weighted(data),
            }
        )
    return rows


def _quick_weighted(data: dict) -> float:
    """Compute a weighted overall from a saved JSON dict without rehydrating
    the full dataclass — used for the runs list to keep it cheap."""
    cats = RUBRIC.categories
    scores_by_q = {s["question_id"]: int(s["score"]) for s in data.get("scores", [])}
    cat_avgs, weights = [], []
    for cat in cats:
        qids = {q.id for q in RUBRIC.questions_for(cat.id)}
        cat_scores = [scores_by_q[qid] for qid in qids if qid in scores_by_q]
        if cat_scores:
            cat_avgs.append(sum(cat_scores) / len(cat_scores))
            weights.append(cat.weight)
    if not weights:
        return 0.0
    return sum(a * w for a, w in zip(cat_avgs, weights)) / sum(weights)


def _load_run(filename: str) -> AnalysisResult:
    if not _RUN_FILENAME_RE.match(filename):
        abort(400, "Invalid run filename.")
    path = RUNS_DIR / filename
    if not path.is_file():
        abort(404, "Run not found.")
    return AnalysisResult.from_json(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    required = [s for s in TAXONOMY.slots if s.required and not s.ignored_by_analyzer]
    optional = [s for s in TAXONOMY.slots if not s.required and not s.ignored_by_analyzer]
    ignored = [s for s in TAXONOMY.slots if s.ignored_by_analyzer]
    runs = _list_runs()
    return render_template(
        "index.html",
        required=required,
        optional=optional,
        ignored=ignored,
        rubric_name=RUBRIC.name,
        question_count=len(RUBRIC.questions),
        recent_runs=runs[:5],
    )


@app.route("/analyze", methods=["POST"])
def analyze_route():
    vendor_name = (request.form.get("vendor_name") or "vendor").strip() or "vendor"
    vendor_slug = secure_filename(vendor_name) or "vendor"

    with tempfile.TemporaryDirectory(prefix="proc_analyzer_") as tmp:
        tmp_path = Path(tmp)
        any_file = False
        for field_name in request.files:
            for file_storage in request.files.getlist(field_name):
                if not file_storage or not file_storage.filename:
                    continue
                # Some browsers include a directory path in the filename when
                # files come from a folder pick or shift-multi-select. Strip
                # to just the basename so the slot matcher sees the clean name.
                raw_name = Path(file_storage.filename.replace("\\", "/")).name
                safe_name = secure_filename(raw_name)
                if not safe_name:
                    continue
                dest = tmp_path / safe_name
                if dest.exists():
                    stem, dot, ext = safe_name.rpartition(".")
                    safe_name = f"{stem}_{field_name}.{ext}" if dot else f"{safe_name}_{field_name}"
                    dest = tmp_path / safe_name
                file_storage.save(dest)
                any_file = True

        if not any_file:
            return render_template("error.html", message="No files uploaded. Please attach at least one artifact and try again."), 400

        try:
            result = analyze(tmp_path, RUBRIC, taxonomy=TAXONOMY)
        except SystemExit as exc:
            return render_template("error.html", message=str(exc)), 500
        except Exception as exc:  # noqa: BLE001
            return render_template("error.html", message=f"Analysis failed: {exc}"), 500

        result.vendor_name = vendor_name
        run_path = _save_run(result)
        markdown_text = render_markdown(result, RUBRIC, TAXONOMY)

    html_body = md_lib.markdown(markdown_text, extensions=["tables", "fenced_code", "sane_lists"])
    return render_template(
        "report.html",
        vendor_name=vendor_name,
        vendor_slug=vendor_slug,
        report_html=html_body,
        report_markdown=markdown_text,
        weighted=result.weighted_overall(RUBRIC),
        analyzed_at=result.analyzed_at_utc,
        run_filename=run_path.name,
    )


@app.route("/runs")
def runs_route():
    return render_template("runs.html", runs=_list_runs())


@app.route("/compare", methods=["GET"])
def compare_form():
    runs = _list_runs()
    preselect = request.args.get("with", "")
    return render_template("compare_form.html", runs=runs, preselect=preselect)


@app.route("/compare", methods=["POST"])
def compare_route():
    a_name = request.form.get("a")
    b_name = request.form.get("b")
    if not a_name or not b_name:
        return render_template("error.html", message="Pick two analyses to compare."), 400
    if a_name == b_name:
        return render_template("error.html", message="Pick two different analyses."), 400

    left = _load_run(a_name)
    right = _load_run(b_name)
    comp = compare(left, right, RUBRIC)
    markdown_text = render_comparison_markdown(comp)
    html_body = md_lib.markdown(markdown_text, extensions=["tables", "fenced_code", "sane_lists"])

    slug = secure_filename(f"{left.vendor_name}_vs_{right.vendor_name}") or "comparison"
    return render_template(
        "compare.html",
        left_name=left.vendor_name,
        right_name=right.vendor_name,
        left_weighted=comp.left_weighted,
        right_weighted=comp.right_weighted,
        weighted_delta=comp.weighted_delta,
        winner=comp.winner(),
        report_html=html_body,
        report_markdown=markdown_text,
        comparison_slug=slug,
    )


@app.route("/download/<vendor_slug>.md", methods=["POST"])
def download_markdown(vendor_slug: str):
    md = request.form.get("markdown", "")
    buf = io.BytesIO(md.encode("utf-8"))
    return send_file(
        buf,
        mimetype="text/markdown; charset=utf-8",
        as_attachment=True,
        download_name=f"{secure_filename(vendor_slug) or 'vendor'}.md",
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
