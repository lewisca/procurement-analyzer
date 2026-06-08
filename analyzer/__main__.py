"""CLI entry point.

Usage:
  python -m analyzer <vendor_folder> [-o report.md] [--rubric path.yaml] [--json out.json]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analyzer import analyze
from .artifacts import load_taxonomy
from .env_loader import load_env
from .report import render_markdown
from .rubric import load_rubric

# Load .env so `python -m analyzer ...` works without manual env-var export.
load_env()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="analyzer", description="Procurement Analyzer — score an agentic AI vendor against a rubric.")
    parser.add_argument("vendor", type=Path, help="Path to vendor folder containing artifacts (.md, .json, .yaml, .txt).")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Markdown report output path. Defaults to reports/<vendor>_<timestamp>.md.")
    parser.add_argument("--rubric", type=Path, default=Path("rubric/horizontal_v1.yaml"), help="Path to rubric YAML.")
    parser.add_argument("--json", dest="json_out", type=Path, default=None, help="Optional: dump raw structured result JSON here.")
    args = parser.parse_args(argv)

    if not args.vendor.is_dir():
        print(f"error: vendor folder not found: {args.vendor}", file=sys.stderr)
        return 2
    if not args.rubric.is_file():
        print(f"error: rubric not found: {args.rubric}", file=sys.stderr)
        return 2

    rubric = load_rubric(args.rubric)
    taxonomy = load_taxonomy()
    print(f"Loaded rubric: {rubric.name} ({len(rubric.questions)} questions)")
    print(f"Loaded artifact taxonomy: {len(taxonomy.slots)} slots")

    print(f"Analyzing {args.vendor.name} (this calls Claude; takes ~30-60s)...")
    result = analyze(args.vendor, rubric, taxonomy=taxonomy)

    output_path = args.output
    if output_path is None:
        ts = result.analyzed_at_utc.replace(":", "-")
        output_path = Path("reports") / f"{result.vendor_name}_{ts}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown = render_markdown(result, rubric, taxonomy)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Report written: {output_path}")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(result.to_json(), encoding="utf-8")
        print(f"Raw result JSON written: {args.json_out}")

    weighted = result.weighted_overall(rubric)
    print(f"Weighted overall: {weighted:.2f} / 5.0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
